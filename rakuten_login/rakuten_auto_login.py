#
# 楽天証券サイトへログインしてデータを取得する
#

import json
from selenium.webdriver import Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
from bs4 import BeautifulSoup


# 設定ファイルからログイン情報を取得
login_info = json.load(open("login_info.json", "r", encoding="utf-8"))

# ログインサイト名
site_name = "sec_rakuten"

# ログイン画面URL
url_login = login_info[site_name]["url"]

# ユーザー名とパスワードの指定
USER = login_info[site_name]["id"]
PASS = login_info[site_name]["pass"]

# Safariを起動する
browser = Safari()

# ログイン画面取得
browser.get(url_login)

# 入力
e = browser.find_element(by=By.ID, value="form-login-id")
e.clear()
e.send_keys(USER)
e = browser.find_element(by=By.ID, value="form-login-pass")
e.clear()
e.send_keys(PASS)

# ログイン
frm = browser.find_element(by=By.NAME, value="loginform")
frm.submit()

# ページロード完了まで待機
#WebDriverWait(browser, 20).until(
    # 保有商品の金額を取得するための待機
#    ec.presence_of_element_located((By.CSS_SELECTOR, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[2]/td[1]/p/span[1]}')
# ))



# 保有商品の金額の取得
#set_value = browser.find_element(By.CSS_SELECTOR, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[2]/td[1]/p/span[1]}').text

#print(f'保有商品の金額: {asset_value}')


response = requests.get('https://www.rakuten-sec.co.jp/session_error.html')
soup = BeautifulSoup(response.content, 'html.parser')

span_element = soup.find('span', class_='pcmm-m1-home-assets-table__amount')
print(span_element)

# ログインできたか確認（画面キャプチャ取る）
browser.save_screenshot("../screenshot/sec_rakuten/home.png")

browser.quit()

