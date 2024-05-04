import json
from selenium.webdriver import Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
from bs4 import BeautifulSoup


# 設定ファイルからログイン情報を取得
login_info = json.load(open("fail_path", "r", encoding="utf-8"))

# ログインサイト名
site_name = "URL"

# ログイン画面URL
url_login = login_info["bank_syouken"]["url"]

# ユーザー名とパスワードの指定
USER = login_info["bank_syouken"]["id"]
PASS = login_info["bank_syouken"]["pass"]

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
WebDriverWait(browser, 20).until(
    # 保有商品の金額を取得するための待機
    ec.presence_of_element_located((By.XPATH, 'browser_XPATH'))
)


# 保有商品の金額の取得
max_attempts = 20
attempts = 0

while attempts < max_attempts:
    try:
        # 要素がロードされるのを待つ
        set_value01 = browser.find_element(By.XPATH, 'browser_XPATH').text
        set_value02 = browser.find_element(By.XPATH, 'browser_XPATH').text
        set_value03 = browser.find_element(By.XPATH, 'browser_XPATH').text
        set_value04 = browser.find_element(By.XPATH, 'browser_XPATH').text

        # 要素のテキストが '-' でないことを確認
        if set_value01 != '-' and set_value02 != '-' and set_value03 != '-' and set_value04 != '-':
            print(f'日本円預かり金: {set_value01}')
            print(f'投資信託: {set_value02}')
            print(f'外貨預り金合計: {set_value03}')
            print(f'米国株式: {set_value04}')
            break
        else:
            print("値が '-' なので再試行します。")
    except TimeoutException:
        print("指定した要素が見つかりません。再試行します。")
    
    attempts += 1


response = requests.get('URL')
soup = BeautifulSoup(response.content, 'html.parser')

span_element = soup.find('span', class_='pcmm-m1-home-assets-table__amount')
print(span_element)

# ログインできたか確認（画面キャプチャ取る）
browser.save_screenshot("../screenshot/sec_rakuten/home.png")

browser.quit()

