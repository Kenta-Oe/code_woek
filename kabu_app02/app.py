from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import matplotlib

app = Flask(__name__)

# 日本語フォントの設定
font_path = 'C:/Windows/Fonts/msgothic.ttc'  # ご自身の環境に合わせて変更してください
font_prop = fm.FontProperties(fname=font_path)
matplotlib.rc('font', family=font_prop.get_name())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        code = code.zfill(4)
        ticker_symbol = code + '.T'
        data = yf.download(ticker_symbol, period='1y')

        if data.empty:
            signal = "データが取得できませんでした。正しい銘柄コードを入力してください。"
            return render_template('index.html', signal=signal)

        data['MA5'] = data['Close'].rolling(window=5).mean()
        data['MA20'] = data['Close'].rolling(window=20).mean()

        current_price = data['Close'].iloc[-1]

        # 過去1ヶ月、6ヶ月、1年の平均株価を計算
        data_last_1mo = data.tail(22)  # 約1ヶ月（22営業日）
        data_last_6mo = data.tail(22 * 6)  # 約6ヶ月
        data_last_1y = data  # 1年

        avg_price_1mo = data_last_1mo['Close'].mean()
        avg_price_6mo = data_last_6mo['Close'].mean()
        avg_price_1y = data_last_1y['Close'].mean()

        # シグナルの判定
        if data['MA5'].iloc[-1] > data['MA20'].iloc[-1]:
            signal = "買い時です。"
        else:
            signal = "まだ買い時ではありません。"

        # 銘柄名の取得
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        name = info.get('longName') or info.get('shortName') or '銘柄名不明'

        # グラフの作成
        graph_urls = {}
        graphs = {'1ヶ月': data_last_1mo, '6ヶ月': data_last_6mo, '1年': data_last_1y}

        for period_name, period_data in graphs.items():
            img = io.BytesIO()

            plt.figure(figsize=(5, 4))
            plt.plot(period_data.index, period_data['Close'], label='終値')
            plt.title(period_name)
            plt.xlabel('期間')
            plt.ylabel('円')

            # 日付のフォーマットと表示の調整
            ax = plt.gca()
            ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=7))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)

            plt.grid(True)
            plt.tight_layout()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            graph_urls[period_name] = base64.b64encode(img.getvalue()).decode()

        # 西暦（年）の取得
        latest_date = data.index[-1]
        year = latest_date.year

        return render_template('index.html', signal=signal, code=code, name=name,
                               current_price=round(current_price, 2),
                               avg_price_1mo=round(avg_price_1mo, 2),
                               avg_price_6mo=round(avg_price_6mo, 2),
                               avg_price_1y=round(avg_price_1y, 2),
                               ticker=ticker_symbol, graph_urls=graph_urls, year=year)
    else:
        return render_template('index.html')

@app.route('/get_current_price', methods=['POST'])
def get_current_price():
    ticker_symbol = request.form['ticker']
    data = yf.download(ticker_symbol, period='1d', interval='1m')
    if data.empty:
        return jsonify({'current_price': 'データ取得エラー'})
    current_price = data['Close'].iloc[-1]
    return jsonify({'current_price': round(current_price, 2)})

if __name__ == '__main__':
    app.run(debug=True)
