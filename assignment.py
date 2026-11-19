import sqlite3
from playwright.sync_api import sync_playwright

# ファイルパスとdb名
path = './db/'
db_name = 'assignment.sqlite'

# dbに接続
con = sqlite3.connect(path + db_name)
print(type(con))

# カーソルオブジェクト
cur = con.cursor()

# SQLを用意
sql_create_table_repositories = 'CREATE TABLE repositories(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, language TEXT, stars TEXT);'
sql_insert_repositories = "INSERT INTO repositories (name, language, stars) VALUES (?, ?, ?);"

# サイトurl
url = "https://github.com/orgs/google/repositories"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    # ブラウザを閉じる
    browser.close()

# dbへの接続を閉じる
con.close()