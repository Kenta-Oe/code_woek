@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "generate_script" in request.form:
            try:
                title = request.form.get("title", "").strip()
                input_text = request.form.get("input_text", "").strip()
                urls = request.form.get("urls", "").strip().split("\n")
                
                if not title or not input_text:
                    flash("タイトルと入力テキストを必ず入力してください。")
                    return redirect(url_for("index"))
                
                source_text = fetch_url_content([url for url in urls if url.strip()])
                script_text = generate_script(title, input_text, source_text)
                filename = save_script_to_file(title, script_text)
                
                char_count = len(script_text)
                flash(f"台本生成完了。出力ファイルを確認してください。（{char_count}文字）")
                
                return render_template("index.html", 
                                    script_text=script_text,
                                    input_text=input_text,
                                    urls="\n".join(urls),
                                    title=title,
                                    filename=filename)
            except Exception as e:
                logger.error(f"処理全体エラー: {e}")
                flash("システムエラー発生。管理者に連絡してください。")
                return redirect(url_for("index"))
                
        elif "create_json" in request.form:
            script_text = request.form.get("script_text", "")
            title = request.form.get("title", "")
            if script_text and title:
                json_filename = create_json_script(title, script_text)
                if json_filename:
                    flash(f"JSONファイルを作成しました: {json_filename}")
                else:
                    flash("JSONファイルの作成に失敗しました。")
            
        elif "create_mp3" in request.form:
            try:
                subprocess.run(["python", r"C:\Users\takky\OneDrive\デスクトップ\code_work\code_woek\ai-podcaster_python\main.py"])
                flash("MP3ファイルの生成を開始しました。")
            except Exception as e:
                logger.error(f"MP3生成エラー: {e}")
                flash("MP3ファイルの生成中にエラーが発生しました。")
                
        elif "summarize" in request.form:
            script_text = request.form.get("script_text", "")
            if script_text:
                summary = summarize_script(script_text)
                return render_template("index.html",
                                    script_text=script_text,
                                    summary=summary,
                                    input_text=request.form.get("input_text", ""),
                                    urls=request.form.get("urls", ""),
                                    title=request.form.get("title", ""))
    
    return render_template("index.html",
                         script_text="",
                         input_text="",
                         urls="",
                         title="",
                         summary="")

@app.route("/history")
def history():
    scripts = []
    try:
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith(".txt"):
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    title = content.split("\n")[0].replace("タイトル: ", "")
                    scripts.append({
                        "filename": filename,
                        "title": title,
                        "content": content
                    })
    except Exception as e:
        logger.error(f"履歴取得エラー: {e}")
        flash("履歴の取得中にエラーが発生しました。")
    
    return render_template("history.html", scripts=scripts)

if __name__ == "__main__":
    app.run(port=5000)