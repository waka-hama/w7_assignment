from playwright.sync_api import sync_playwright

url = "https://github.com/orgs/google/repositories"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    browser.close()