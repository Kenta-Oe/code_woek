import feedparser
import openai
import tweepy
import time
from datetime import datetime, timedelta
from config import *

# OpenAI APIキーを設定
openai.api_key = OPENAI_API_KEY

# X API クライアントの初期化
x_client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)

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
            max_tokens=600,
            temperature=0.7,
        )
        translated_text = response.choices[0].message["content"].strip()
        print("Translation successful.")
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return "翻訳に失敗しました。"

def post_to_x(message):
    """Xにメッセージを投稿"""
    try:
        result = x_client.create_tweet(text=message)
        print(f"Successfully posted to X: {message}")
        return True
    except Exception as e:
        print(f"Error posting to X: {e}")
        return False

def main():
    """記事取得、翻訳、X投稿を実行"""
    articles = fetch_nyt_articles()
    if not articles:
        print("No articles found for yesterday.")
        return

    # すべての記事の翻訳をまとめて行う
    translated_articles = []
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Link: {article['link']}")
        print("Original Summary:", article['summary'])
        
        translated_summary = translate_article(article['summary'])
        translated_articles.append({
            "title": article['title'],
            "summary": translated_summary,
            "link": article['link']
        })

    # まとめた記事を1つのメッセージにする
    message = "New York Timesの昨日の記事一覧\n\n"
    for article in translated_articles:
        message += f"{article['title']}\n{article['summary']}\n{article['link']}\n\n"

    # まとめたメッセージを投稿
    post_to_x(message)
    print("Process completed successfully.")

if __name__ == "__main__":
    main()