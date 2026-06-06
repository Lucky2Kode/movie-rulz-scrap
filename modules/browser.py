"""
Manages a shared Chrome session for scraping SSL-blocked sites.
Uses a single persistent page so cookies and session stay alive across requests.
"""
import subprocess
import time
import urllib.request

_CHROME_PORT = 9223
_chrome_proc = None
_playwright = None
_browser = None
_page = None


def _start_chrome():
    import os
    global _chrome_proc
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    exe = next((p for p in chrome_paths if os.path.exists(p)), None)
    if not exe:
        return False

    _chrome_proc = subprocess.Popen(
        [
            exe,
            f"--remote-debugging-port={_CHROME_PORT}",
            "--user-data-dir=/tmp/chrome-scraper",
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(10):
        time.sleep(0.5)
        if _chrome_is_up():
            return True
    return False


def _chrome_is_up() -> bool:
    try:
        urllib.request.urlopen(f"http://localhost:{_CHROME_PORT}/json/version", timeout=2)
        return True
    except Exception:
        return False


def _get_page():
    """Return the shared persistent page, starting Chrome if needed."""
    global _playwright, _browser, _page

    # Reconnect if Chrome died
    if _page is not None:
        try:
            _page.evaluate("1")  # cheap liveness check
            return _page
        except Exception:
            _page = None
            _browser = None

    if not _chrome_is_up():
        if not _start_chrome():
            return None

    from playwright.sync_api import sync_playwright
    if _playwright is None:
        _playwright = sync_playwright().start()

    _browser = _playwright.chromium.connect_over_cdp(f"http://localhost:{_CHROME_PORT}")
    _page = _browser.new_page()
    return _page


def fetch_html(url: str) -> str | None:
    """Fetch a page's HTML through the persistent Chrome session."""
    try:
        page = _get_page()
        if page is None:
            return None
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        # Wait for JS-driven redirects to settle, then wait for #main to appear
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        try:
            page.wait_for_selector("#main", timeout=15000)
        except Exception:
            pass
        return page.content()
    except Exception as e:
        print(f"  [browser error] {e}")
        # Reset page so next call gets a fresh one
        global _page
        _page = None
        return None


def fetch_bytes(url: str) -> bytes | None:
    """Download a file as bytes through the persistent Chrome session."""
    try:
        page = _get_page()
        if page is None:
            return None
        response = page.goto(url, timeout=20000, wait_until="commit")
        return response.body() if response and response.ok else None
    except Exception as e:
        print(f"  [browser fetch error] {e}")
        global _page
        _page = None
        return None
