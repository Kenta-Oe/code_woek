function getYesterdayNYTArticles() {
  Logger.log('記事取得開始');
  const url = 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml';
  
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
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    yesterday.setHours(0, 0, 0, 0);
    
    items.forEach(item => {
      const pubDate = new Date(item.getChild('pubDate').getText());
      if (pubDate.toDateString() === yesterday.toDateString()) {
        const title = item.getChild('title').getText();
        const link = item.getChild('link').getText();
        const description = item.getChild('description').getText()
          .replace(/<[^>]+>/g, '') // HTMLタグを削除
          .replace(/\s+/g, ' ') // 複数の空白を1つに
          .trim();
        
        Logger.log('記事取得: ' + title);
        
        articles.push({
          title: title,
          link: link,
          summary: description
        });
      }
    });
    
    Logger.log('取得完了 - 記事数: ' + articles.length);
    return articles;
    
  } catch (error) {
    Logger.log('RSSフィード取得エラー: ' + error);
    return [];
  }
}