function getChatGptSummary(content) {
  Logger.log('要約関数開始');
  
  // APIキー確認
  const apiKey = PropertiesService.getScriptProperties().getProperty("OPENAI_API_KEY");
  if (!apiKey) {
    Logger.log('APIキーが設定されていません');
    return "APIキーエラー";
  }

  const promptText = `
あなたは優秀な要約者です。以下の記事内容を200文字程度で要約してください。
---
${content}
---
`;

  const url = "https://api.openai.com/v1/chat/completions";
  const payload = {
    model: "gpt-4",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: promptText }
    ],
    temperature: 0.7
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
    return "要約取得失敗";
  }
}