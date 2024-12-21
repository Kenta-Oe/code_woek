/*******************************************************
 * Main.gs
 * - エントリーポイント
 * - トリガー（時間主導型）で毎朝8時に実行すると仮定
 *******************************************************/

/**
 * 毎日自動で実行されるメイン関数
 */
function fetchAndSummarizeCoinPostArticles() {
  // 1. 前日のCoinPostの記事リストを取得
  const articles = getYesterdayCoinPostArticles() // CoinPost.gs 内の関数を呼ぶ
  
  // 2. ファイル名を「日付のみ」にする
  //    例: 20231002_CoinPostSummary.txt
  const today = Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyyMMdd")
  const fileName = `${today}_CoinPostSummary.txt`
  
  // 3. 一つにまとめるための文字列バッファを用意
  //    記事が複数あれば、次々に追記していく
  let dailySummary = ""
  
  // 4. 記事ごとにChatGPTへ要約リクエスト → dailySummary へ追記
  articles.forEach((article) => {
    const title = article.title
    const link = article.link
    const content = article.content // 要約対象の本文
    
    const summary = getChatGptSummary(content) // ChatGPT.gs の関数を呼び出し
    // タイトル・リンク・要約をまとめて追記
    dailySummary += `タイトル: ${title}\n元リンク: ${link}\n要約:\n${summary}\n\n`
  })
  
  // 5. 最後に一度だけファイルを作成してまとめた内容を書き込む
  saveDailySummaryToDrive(fileName, dailySummary)
}


/**
 * まとめた要約を1つのテキストファイルとして Drive に保存する
 * @param {string} fileName 例: "20231002_CoinPostSummary.txt"
 * @param {string} content  まとめた要約テキスト（複数記事分）
 */
function saveDailySummaryToDrive(fileName, content) {
  // 保存したいフォルダのIDを指定する例（マイドライブ直下なら不要）
  const folderId = "1zw6JPUpLW2ZJQe9dzw1Qdk7g0ZR2qemg" 
  const folder = DriveApp.getFolderById(folderId)
  
  // テキストファイル作成
  folder.createFile(fileName, content, MimeType.PLAIN_TEXT)
}
