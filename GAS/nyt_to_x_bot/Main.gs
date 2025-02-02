function fetchAndTranslateNYTArticles() {
  Logger.log('処理開始');
  
  // 1. 記事取得
  const articles = getYesterdayNYTArticles();
  Logger.log('取得記事数: ' + articles.length);
  
  if (articles.length === 0) {
    Logger.log('記事が取得できませんでした');
    return;
  }

  // 2. ファイル名準備
  const today = Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyyMMdd");
  const fileName = `${today}_NYTSummary.txt`;
  Logger.log('作成するファイル名: ' + fileName);
  
  // 3. 翻訳用のバッファ準備
  let dailySummary = "";
  let xPostContent = "";
  
  // 4. 記事ごとの処理
  for (let i = 0; i < articles.length; i++) {
    const article = articles[i];
    Logger.log(`記事${i + 1}の処理開始: ${article.title}`);
    
    // 翻訳処理
    Logger.log('翻訳開始');
    const translatedSummary = translateWithChatGpt(article.summary);
    Logger.log('翻訳結果: ' + translatedSummary);
    
    // バッファに追加
    dailySummary += `タイトル: ${article.title}\n元リンク: ${article.link}\n翻訳:\n${translatedSummary}\n\n`;
    xPostContent += `📰${article.title}\n\n${translatedSummary}\n\n🔗${article.link}\n\n`;
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

  // 7. メール送信
  Logger.log('メール送信開始');
  try {
    sendSummaryEmail(fileName, dailySummary);
    Logger.log('メール送信成功');
  } catch (error) {
    Logger.log('メール送信エラー: ' + error);
  }
  
  Logger.log('全処理完了');
}

function saveDailySummaryToDrive(fileName, content) {
  Logger.log('Drive保存関数開始');
  const folderId = "YOUR_NYT_FOLDER_ID";
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

function sendSummaryEmail(fileName, content) {
  Logger.log('メール送信関数開始');
  const emailAddress = 'takkyuuomoro@gmail.com';
  const subject = `NYTニュース要約 - ${fileName}`;
  
  try {
    GmailApp.sendEmail(
      emailAddress,
      subject,
      content,
      {
        name: 'NYTニュース要約bot'
      }
    );
    Logger.log('メール送信成功');
  } catch (error) {
    Logger.log('メール送信エラー: ' + error);
    throw error;
  }
}