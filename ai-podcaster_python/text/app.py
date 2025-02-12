from flask import Flask, render_template, request, flash, redirect, url_for
import subprocess
import os
import json
import logging
from datetime import datetime
import openai
from config import OUTPUT_DIR, JSON_OUTPUT_DIR, LOG_DIR, SECRET_KEY, DEBUG, OPENAI_API_KEY

# Flaskアプリケーションの設定
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG

# ロギングの設定
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_podcast_script(title, input_text, urls):
    try:
        # 固定の挨拶文
        opening_greeting = "こんにちは、皆さん。ようこそ、私はホストのAIアシスタントです。"
        closing_message = "今後もこうしたニュースの背景や影響について、皆さんと一緒に考えていきたいと思います。もしこのエピソードについてご意見や質問がありましたら、ぜひお寄せください。また、ポッドキャストを楽しんでいただけたなら、評価やレビューもお願いします。それでは、次回もお楽しみに。ありがとうございました。"

        # プロンプトの作成
        prompt = f"""
あなたはプロのPodcastの話し手です。
提供された情報をもとに、8000文字程度のPodcast用の台本を作成してください。
・出力は普通の丁寧語で口語のみとし、目次やタイトルは除外する（一連の文章だけの出力とする）
・最大限のリソースを使用してハルシネーションを防止すること
・出力はすべてソースのあるものから行い、あいまいな情報は使用しない
・起承転結を踏襲すること
・上記の条件を何があっても必ず逸脱しないこと

台本の構成：
{opening_greeting}
（メインコンテンツ）
{closing_message}

以下の情報をもとに台本を作成してください：

タイトル: {title}

参考情報:
{input_text}

参考URL:
{urls}

"""

        # ChatGPT APIを使用して台本を生成
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # 生成された台本
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"台本生成エラー: {e}")
        raise

def generate_summary(script_text):
    try:
        prompt = """
あなたは要約のプロフェッショナルです。
提供されたPodcast台本を、簡潔で分かりやすい形で要約してください。
重要なポイントを漏らさず、全体の内容が把握できるようにまとめてください。

以下の台本を要約してください：

"""
        # ChatGPT APIを使用して要約を生成
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": prompt + script_text}
            ]
        )
        
        # 生成された要約
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"要約生成エラー: {e}")
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    script_text = ""
    summary = ""
    title = ""
    input_text = ""
    urls = ""

    if request.method == "POST":
        title = request.form.get("title", "")
        input_text = request.form.get("input_text", "")
        urls = request.form.get("urls", "")

        try:
            if "generate_script" in request.form:
                # タイムスタンプを生成
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 台本を生成
                script_text = generate_podcast_script(title, input_text, urls)
                script_text = f"生成日時: {timestamp}\n\n" + script_text
                
                # ファイル名を生成
                filename = f"podcast_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                # ファイルに保存
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"タイトル: {title}\n")
                    f.write(f"参考URL: {urls}\n")
                    f.write(script_text)
                
                logger.info(f"台本生成成功: {filename}")
                flash("台本が生成されました。")

            elif "create_json" in request.form and input_text:
                # 台本生成
                script_text = generate_podcast_script(title, input_text, urls)
                
                # JSON形式に変換して保存
                script_data = create_json_script(script_text, title, urls)
                if script_data:
                    flash("JSONファイルが生成されました。")
                    logger.info("JSONファイル生成成功")

            elif "summarize" in request.form and script_text:
                # 要約を生成
                summary = generate_summary(script_text)
                flash("要約が生成されました。")
                logger.info("要約生成成功")

            elif "create_mp3" in request.form:
                # MP3生成プロセスを実行
                script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                main_script_path = os.path.join(script_dir, "main.py")
                process = subprocess.run(["python", main_script_path], capture_output=True, text=True)
                
                if process.returncode == 0:
                    flash("MP3の生成を開始しました。")
                    logger.info("MP3生成プロセス開始")
                else:
                    flash("MP3の生成中にエラーが発生しました。")
                    logger.error(f"MP3生成エラー: {process.stderr}")

        except Exception as e:
            logger.error(f"処理エラー: {e}")
            flash("処理中にエラーが発生しました。")

    return render_template("index.html",
                         script_text=script_text,
                         summary=summary,
                         title=title,
                         input_text=input_text,
                         urls=urls)

@app.route("/history")
def history():
    scripts = []
    try:
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(".txt"):
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    scripts.append({
                        "filename": filename,
                        "content": content
                    })
    except Exception as e:
        logger.error(f"履歴取得エラー: {e}")
        flash("履歴の取得中にエラーが発生しました。")
    
    return render_template("history.html", scripts=scripts)

def create_json_script(script_text, title="", reference=""):
    try:
        # スクリプトを行ごとに分割
        lines = script_text.strip().split('\n')
        script_data = {
            "title": title,
            "description": lines[0] if lines else "",
            "reference": reference,
            "script": []
        }

        current_speaker = "ナレーター"
        for line in lines:
            if line.strip():
                if ":" in line:
                    parts = line.split(":", 1)
                    current_speaker = parts[0].strip()
                    text = parts[1].strip()
                else:
                    text = line.strip()

                script_data["script"].append({
                    "text": text,
                    "speaker": current_speaker,
                    "speed": 1.0
                })

        # ファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"script_{timestamp}.json"
        filepath = os.path.join(JSON_OUTPUT_DIR, filename)

        # JSONファイルとして保存
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(script_data, f, ensure_ascii=False, indent=4)

        return script_data
    except Exception as e:
        logger.error(f"JSON変換エラー: {e}")
        return None

if __name__ == "__main__":
    app.run()