import json
from selenium.webdriver import Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup

# 設定ファイルからログイン情報を取得
login_info = json.load(open("/path/to/your/login_info.json", "r", encoding="utf-8"))

# ログインサイト名
site_name = "https://example.com/login"

# ログイン画面URL
url_login = login_info["broker"]["url"]

# ユーザー名とパスワードの指定
USER = login_info["broker"]["id"]
PASS = login_info["broker"]["pass"]

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
    ec.presence_of_element_located((By.XPATH, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[2]/td[1]/p/span[1]'))
)

# 保有商品の金額の取得
max_attempts = 20
attempts = 0

while attempts < max_attempts:
    try:
        # 要素がロードされるのを待つ
        set_value01 = browser.find_element(By.XPATH, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[8]/td[1]/p/span[1]').text
        set_value02 = browser.find_element(By.XPATH, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[6]/td[1]/p/span[1]').text
        set_value03 = browser.find_element(By.XPATH, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[9]/td[1]/p/span[1]').text
        set_value04 = browser.find_element(By.XPATH, '//*[@id="balance_data_actual_data"]/section/table[1]/tbody/tr[2]/td[1]/p/span[1]').text

        # 要素のテキストが '-' でないことを確認
        if set_value01 != '-':
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

response = requests.get('https://example.com/session_error.html')
soup = BeautifulSoup(response.content, 'html.parser')

span_element = soup.find('span', class_='amount-class')
print(span_element)

# ログインできたか確認（画面キャプチャ取る）
browser.save_screenshot("/path/to/your/screenshot/home.png")

browser.quit()
