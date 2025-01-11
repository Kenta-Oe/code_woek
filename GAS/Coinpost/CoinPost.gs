// CoinPost.gs
function getYesterdayCoinPostArticles() {
  Logger.log('記事取得開始');
  const url = 'https://coinpost.jp/?feed=rss2';  // RSSフィードのURL
  
  try {
    Logger.log('RSSフィードにアクセス: ' + url);
    const response = UrlFetchApp.fetch(url);
    const xml = response.getContentText();
    Logger.log('RSSフィード取得成功');
    
    const document = XmlService.parse(xml);
    const root = document.getRootElement();
    const channel = root.getChild('channel');
    const items = channel.getChildren('item');
    
    Logger.log('記事数: ' + items.length);
    
    const articles = [];
    
    items.forEach(item => {
      const title = item.getChild('title').getText();
      const link = item.getChild('link').getText();
      const content = item.getChild('description').getText()
        .replace(/<[^>]+>/g, '') // HTMLタグを削除
        .replace(/\s+/g, ' ') // 複数の空白を1つに
        .trim();
      
      Logger.log('記事取得: ' + title);
      
      articles.push({
        title: title,
        link: link,
        content: content
      });
    });
    
    Logger.log('取得完了 - 記事数: ' + articles.length);
    return articles;
    
  } catch (error) {
    Logger.log('RSSフィード取得エラー: ' + error);
    return [];
  }
}