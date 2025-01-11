function fetchAndSummarizeCoinPostArticles() {
  Logger.log('処理開始');
  
  // 1. 記事取得
  const articles = getYesterdayCoinPostArticles();
  Logger.log('取得記事数: ' + articles.length);
  
  if (articles.length === 0) {
    Logger.log('記事が取得できませんでした');
    return;
  }

  // 2. ファイル名準備
  const today = Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyyMMdd");
  const fileName = `${today}_CoinPostSummary.txt`;
  Logger.log('作成するファイル名: ' + fileName);
  
  // 3. 要約用のバッファ準備
  let dailySummary = "";
  let xPostContent = "";
  
  // 4. 記事ごとの処理
  for (let i = 0; i < articles.length; i++) {
    const article = articles[i];
    Logger.log(`記事${i + 1}の処理開始: ${article.title}`);
    
    // 記事の内容確認
    Logger.log('記事内容の長さ: ' + article.content.length);
    Logger.log('記事内容のサンプル: ' + article.content.substring(0, 100));
    
    // 要約処理
    Logger.log('要約開始');
    const summary = getChatGptSummary(article.content);
    Logger.log('要約結果: ' + summary);
    
    // バッファに追加
    dailySummary += `タイトル: ${article.title}\n元リンク: ${article.link}\n要約:\n${summary}\n\n`;
    xPostContent += `📰${article.title}\n\n${summary}\n\n🔗${article.link}\n\n`;
  }
  
  // 5. Drive保存
  Logger.log('Drive保存開始');
  try {
    saveDailySummaryToDrive(fileName, dailySummary);
    Logger.log('Drive保存成功');
  } catch (error) {
    Logger.log('Drive保存エラー: ' + error);
  }

  // 6. X投稿
  if (xPostContent) {
    Logger.log('X投稿開始');
    try {
      const result = postToX(xPostContent);
      Logger.log('X投稿結果: ' + result);
    } catch (error) {
      Logger.log('X投稿エラー: ' + error);
    }
  }
  
  Logger.log('全処理完了');
}

function saveDailySummaryToDrive(fileName, content) {
  Logger.log('Drive保存関数開始');
  // 保存したいフォルダのIDを指定する例（マイドライブ直下なら不要）
  const folderId = "1zw6JPUpLW2ZJQe9dzw1Qdk7g0ZR2qemg";
  Logger.log('対象フォルダID: ' + folderId);
  
  try {
    const folder = DriveApp.getFolderById(folderId);
    Logger.log('フォルダ取得成功');
    
    // テキストファイル作成
    const file = folder.createFile(fileName, content, MimeType.PLAIN_TEXT);
    Logger.log('ファイル作成成功: ' + file.getName());
    
  } catch (error) {
    Logger.log('Drive保存詳細エラー: ' + error);
    throw error;
  }
}