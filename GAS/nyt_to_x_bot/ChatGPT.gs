function translateWithChatGpt(content) {
  Logger.log('翻訳関数開始');
  
  const apiKey = PropertiesService.getScriptProperties().getProperty("OPENAI_API_KEY");
  if (!apiKey) {
    Logger.log('APIキーが設定されていません');
    return "APIキーエラー";
  }

  const promptText = `
以下の英語の記事内容を日本語に翻訳してください。
---
${content}
---
`;

  const url = "https://api.openai.com/v1/chat/completions";
  const payload = {
    model: "o1-mini",  // o1-miniを使用
    messages: [
      { role: "user", content: "あなたは英語から日本語への翻訳が得意なアシスタントです。" },
      { role: "user", content: promptText }
    ]
  };

  Logger.log('ChatGPTリクエスト準備完了');

  const options = {
    method: "post",
    contentType: "application/json",
    headers: {
      Authorization: `Bearer ${apiKey}`
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    Logger.log('ChatGPTにリクエスト送信');
    const response = UrlFetchApp.fetch(url, options);
    const json = JSON.parse(response.getContentText());
    
    // OpenAIのエラー応答チェック
    if (json.error) {
      Logger.log('ChatGPTエラーレスポンス: ' + JSON.stringify(json.error));
      return "ChatGPTエラー";
    }
    
    const answer = json.choices[0].message.content;
    Logger.log('ChatGPT応答受信成功');
    return answer.trim();
    
  } catch (error) {
    Logger.log("ChatGPT APIエラー: " + error);
    Logger.log("エラー詳細: " + error.toString());
    return "翻訳取得失敗";
  }
}