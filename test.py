from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    stealth_sync(page)

    page.goto("https://bot.sannysoft.com/")
    page.wait_for_timeout(10000)
    browser.close()
