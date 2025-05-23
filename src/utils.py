from playwright.sync_api import sync_playwright


def with_playwright_page(tab_url: str, headless: bool = False):
    """
    Launches a Playwright page and handles cookie acceptance.
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless, args=["--disable-http2"])
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    page.goto(tab_url, wait_until="domcontentloaded", timeout=15000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)

    try:
        page.get_by_role("link", name="Allow All").click(timeout=3000)
        page.wait_for_timeout(1000)
    except Exception:
        pass

    return page, browser, playwright
