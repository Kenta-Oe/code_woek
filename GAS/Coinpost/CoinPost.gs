/*******************************************************
 * CoinPost.gs
 * - CoinPostのRSSフィードを取得
 * - 前日投稿の記事のみを抽出して返す
 *******************************************************/

function getYesterdayCoinPostArticles() {
  const rssUrl = "https://coinpost.jp/?feed=rss"

  const xml = UrlFetchApp.fetch(rssUrl).getContentText()
  const document = XmlService.parse(xml)
  const root = document.getRootElement()

  // RSS 2.0 構造を前提に items を解析
  const channel = root.getChild("channel")
  const items = channel.getChildren("item")  // itemタグ一覧

  // 前日の0:00～23:59を判定するための日付処理
  const today = new Date()
  const yesterday = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1)
  const startOfYesterday = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 0, 0, 0)
  const endOfYesterday = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 23, 59, 59)

  // 返却用の配列
  const articleArray = []

  items.forEach((item) => {
    const title = item.getChild("title").getText()
    const link = item.getChild("link").getText()
    const pubDateStr = item.getChild("pubDate").getText() // 例: "Tue, 12 Sep 2023 06:30:00 +0000"
    const pubDate = new Date(pubDateStr)

    // content: RSSにより<description>やcontent:encodedを取得
    // CoinPostの場合、content:encoded が詳細を含む可能性あり
    const encodedTag = item.getChild("encoded", item.getNamespace("content"))
    let content = ""
    if (encodedTag) {
      content = encodedTag.getText()
    } else {
      // なければdescription使うなど
      const descTag = item.getChild("description")
      content = descTag ? descTag.getText() : ""
    }

    // pubDateが前日の範囲かどうかチェック
    if (pubDate >= startOfYesterday && pubDate <= endOfYesterday) {
      // 前日の記事と判定
      articleArray.push({
        title,
        link,
        content
      })
    }
  })

  return articleArray
}
