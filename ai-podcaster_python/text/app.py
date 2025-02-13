from flask import Flask, render_template, request, flash
import subprocess
import os
import json
import logging
from datetime import datetime
import openai
from config import OUTPUT_DIR, JSON_OUTPUT_DIR, LOG_DIR, SECRET_KEY, DEBUG, OPENAI_API_KEY, BASE_DIR

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

def generate_podcast_script(input_text, urls):
    try:
        # 固定の挨拶文
        opening_greeting = "こんにちは、皆さん。ようこそ、私はホストの山田です。"
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
        
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"台本生成エラー: {e}")
        raise

def generate_summary(script_text):
    try:
        prompt = """
あなたは要約のプロフェッショナルです。
提供されたPodcast台本を、200文字程度で要約してください。
以下の条件を必ず守ってください：
・重要なポイントを漏らさず、全体の内容が把握できるようにまとめること
・箇条書きは使用せず、段落形式で出力すること
・必ず200文字程度に収めること（±20文字程度は許容）
・文末は「です。」「ます。」などの丁寧語で統一すること

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
        summary = response.choices[0].message.content
        
        # 要約の文字数をログに記録
        logger.info(f"生成された要約の文字数: {len(summary)}文字")
        
        return summary
    except Exception as e:
        logger.error(f"要約生成エラー: {e}")
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    script_text = request.form.get("current_script", "")  # 現在の台本を取得
    summary = request.form.get("current_summary", "")     # 現在の要約を取得
    input_text = request.form.get("input_text", "")
    urls = request.form.get("urls", "")

    if request.method == "POST":
        try:
            if "generate_script" in request.form:
                script_text = generate_podcast_script(input_text, urls)
                flash("台本が生成されました。")
                logger.info("台本生成成功")

            elif "create_json" in request.form:
                script_text = generate_podcast_script(input_text, urls)
                script_data = create_json_script(script_text, urls)
                if script_data:
                    flash("JSONファイルが生成されました。")
                    logger.info("JSONファイル生成成功")

            elif "summarize" in request.form:
                script_text = request.form.get("current_script", "")
                if script_text:
                    summary = generate_summary(script_text)
                    flash("要約が生成されました。")
                    logger.info("要約生成成功")
                else:
                    flash("要約する台本がありません。先に台本を生成してください。")
                    logger.warning("要約失敗: 台本が存在しません")

            elif "create_mp3" in request.form:
                main_script_path = os.path.join(os.path.dirname(BASE_DIR), "main.py")
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
                         input_text=input_text,
                         urls=urls)

@app.route("/history")
def history():
    return render_template("history.html")

def create_json_script(script_text, reference=""):
    try:
        # スクリプトを行ごとに分割
        lines = script_text.strip().split('\n')
        script_data = {
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