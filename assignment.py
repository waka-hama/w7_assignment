import sqlite3
import time
from playwright.sync_api import sync_playwright

# ファイルパスとdb名
DB_FILE = "assignment.db"
# dbに接続
con = sqlite3.connect(DB_FILE)
print(type(con))
# カーソルオブジェクト
cur = con.cursor()

# 既存データを削除
cur.execute("DROP TABLE IF EXISTS repositories;")
# テーブルを作成
cur.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT ,
        language TEXT,
        stars TEXT
    );
""")
# INSERT文を用意
sql_insert_repositories = "INSERT INTO repositories (name, language, stars) VALUES (?, ?, ?);"
# SELECT文を用意
sql_select = "SELECT * FROM repositories"

# サイトurl
url = "https://github.com/orgs/google/repositories"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1ページ目から99ページ目まで
    for x in range(1, 100):
        # urlの変更
        target_url = f"{url}?page={x}"
        page.goto(target_url)
        
        # 各リポジトリの<li>要素を取得
        repo_items = page.locator('ul li:has(h3 a[href^="/google/"]), ul li:has(h4 a[href^="/google/"])')
        time.sleep(1)
        count = repo_items.count()

        # リポジトリが0件ならループを終了させる
        if count ==0:
            break

        # 各<li>ごとの処理
        for i in range(count):
            item = repo_items.nth(i)
        
            # リポジトリ名
            name = item.locator('h3 a[href^="/google/"], h4 a[href^="/google/"]').inner_text().strip()
            # 言語
            lang_locator = item.locator('[data-testid="repo-language"], span:has(> span[style*="background-color"]) + span, div:has(> span[style*="background-color"])')
            # 言語が存在しない場合のエラー回避
            if lang_locator.count() > 0:      
                lang = lang_locator.first.inner_text().strip()
            else:
                lang = None
            # スター数
            stars_locator = item.locator('a[href$="/stargazers"]')
            # スター数が存在しない場合のエラー回避
            if stars_locator.count() > 0:
                stars = stars_locator.first.inner_text().strip()
            else:
                stars = None

            # 取得データをリストに入れる
            repo_list = [name, lang, stars]
        
            # SQLを実行
            cur.execute(sql_insert_repositories, repo_list)
        
        # コミット
        con.commit()
        # time.sleep(1)で実行したところ、ブロックされてしまったため10にしました
        time.sleep(10)
        
    # ブラウザを閉じる
    browser.close()

#selectで表示
cur.execute(sql_select)

for r in cur:
    print(r, type(r))

# dbへの接続を閉じる
con.close()