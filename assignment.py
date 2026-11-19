import sqlite3
from playwright.sync_api import sync_playwright

# ファイルパスとdb名
DB_FILE = "assignment.db"

# dbに接続
con = sqlite3.connect(DB_FILE)
print(type(con))

# カーソルオブジェクト
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        language TEXT,
        stars TEXT
    );
""")
# SQLを用意
sql_insert_repositories = "INSERT INTO repositories (name, language, stars) VALUES (?, ?, ?);"

# サイトurl
url = "https://github.com/orgs/google/repositories"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    # 各リポジトリの<li>要素を取得
    repo_items = page.locator('ul li:has(h3 a[href^="/google/"])')
    repo_items.first.wait_for()

    # 各<li>ごとの処理
    count = repo_items.count()
    for i in range(count):
        item = repo_items.nth(i)

        # リポジトリ名
        name = item.locator('h4 a[href^="/google/"]').inner_text().strip()
        # 言語
        lang = item.locator('[data-testid="repo-language"], span:has(> span[style*="background-color"]) + span, div:has(> span[style*=background-color"])').inner_text().strip()
        # スター数
        stars = item.locator('a[href$="/stargazers"]').inner_text().strip()
        print(f"リポジトリ名：{name} | 言語：{lang} | スター数：{stars}")



    #sql実行
    #コミット

    # ブラウザを閉じる
    browser.close()

# dbへの接続を閉じる
con.close()