import feedparser
import openai
import os
from datetime import datetime, timedelta

# 環境変数から設定を取得
NYT_RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI APIキーを設定
openai.api_key = OPENAI_API_KEY

def fetch_nyt_articles():
    """NYTのRSSフィードを取得して、前日の記事を抽出"""
    print("Fetching NYT RSS feed...")
    articles = []
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.date()

    # RSSフィードを取得
    feed = feedparser.parse(NYT_RSS_URL)
    for entry in feed.entries:
        published_date = None
        if "published_parsed" in entry:
            published_date = datetime(*entry.published_parsed[:6]).date()
        elif "updated_parsed" in entry:
            published_date = datetime(*entry.updated_parsed[:6]).date()

        if published_date == yesterday_date:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            })
    print(f"Found {len(articles)} articles for {yesterday_date}")
    return articles

def translate_article(content):
    """ChatGPTで記事を翻訳"""
    print("Translating article summary...")
    prompt = f"""
    以下の英語の文章を日本語に翻訳してください:
    {content}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは翻訳が得意なアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        translated_text = response.choices[0].message["content"].strip()
        print("Translation successful.")
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return "翻訳に失敗しました。"

def main():
    """記事取得と翻訳を実行"""
    articles = fetch_nyt_articles()
    if not articles:
        print("No articles found for yesterday.")
        return

    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Link: {article['link']}")
        print("Original Summary:", article['summary'])
        translated_summary = translate_article(article['summary'])
        print("Translated Summary:", translated_summary)

if __name__ == "__main__":
    main()
