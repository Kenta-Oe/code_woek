#
# 楽天証券サイトへログインしてデータを取得する
#

import json
from selenium.webdriver import Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from io import StringIO

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



page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

table = soup.select_one("#table_possess_data > span > table")

import pandas as pd
df = pd.read_html(str(table))[0]

browser.quit()
