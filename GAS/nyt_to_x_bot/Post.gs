function postToX(message) {
  Logger.log('X投稿開始: ' + message);

  // スクリプトプロパティから認証情報を取得
  const props = PropertiesService.getScriptProperties();
  const apiKey = props.getProperty('X_API_KEY');            // consumer_key
  const apiSecret = props.getProperty('X_API_SECRET');      // consumer_secret
  const accessToken = props.getProperty('X_ACCESS_TOKEN');  // access_token
  const accessTokenSecret = props.getProperty('X_ACCESS_TOKEN_SECRET'); // access_token_secret

  // 認証情報のチェック
  if (!apiKey || !apiSecret || !accessToken || !accessTokenSecret) {
    Logger.log('必要な認証情報が不足しています');
    return false;
  }

  // OAuth 1.0a用のパラメータ準備
  const nonce = Utilities.getUuid().replace(/-/g, '');
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const endpoint = 'https://api.twitter.com/2/tweets';

  // OAuth用パラメータ
  const oauthParams = {
    'oauth_consumer_key': apiKey,
    'oauth_token': accessToken,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': timestamp,
    'oauth_nonce': nonce,
    'oauth_version': '1.0'
  };

  // 投稿内容
  const tweetParams = {
    'text': message
  };

  // 署名作成のためのパラメータ結合
  const signatureParams = {...oauthParams};
  const paramString = Object.keys(signatureParams)
    .sort()
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(signatureParams[key])}`)
    .join('&');

  // 署名ベース文字列の作成
  const signatureBase = [
    'POST',
    encodeURIComponent(endpoint),
    encodeURIComponent(paramString)
  ].join('&');

  // 署名キーの作成
  const signingKey = `${encodeURIComponent(apiSecret)}&${encodeURIComponent(accessTokenSecret)}`;

  // 署名の生成
  const signature = Utilities.base64Encode(
    Utilities.computeHmacSignature(
      Utilities.MacAlgorithm.HMAC_SHA_1,
      signatureBase,
      signingKey
    )
  );

  // OAuth認証ヘッダーの作成
  oauthParams['oauth_signature'] = signature;
  const authHeader = 'OAuth ' + Object.keys(oauthParams)
    .map(key => `${encodeURIComponent(key)}="${encodeURIComponent(oauthParams[key])}"`)
    .join(', ');

  // APIリクエストの送信
  const options = {
    method: 'post',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify(tweetParams),
    muteHttpExceptions: true
  };

  try {
    Logger.log('APIリクエスト送信');
    const response = UrlFetchApp.fetch(endpoint, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();
    
    Logger.log('応答コード: ' + responseCode);
    Logger.log('応答内容: ' + responseText);

    return responseCode === 201 || responseCode === 200;
  } catch (error) {
    Logger.log('投稿エラー: ' + error);
    return false;
  }
}