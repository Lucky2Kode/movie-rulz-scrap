from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests.exceptions import SSLError, ConnectionError
from .config import make_session
from . import browser
from .parser import parse_entry


def _fetch_with_requests(url: str) -> str | None:
    try:
        session = make_session()
        resp = session.get(url, timeout=20)
        resp.raise_for_status()
        actual_host = urlparse(resp.url).hostname
        expected_host = urlparse(url).hostname
        if actual_host and expected_host and actual_host != expected_host:
            return None
        return resp.text
    except (SSLError, ConnectionError):
        return None


def _fetch(url: str) -> str | None:
    html = _fetch_with_requests(url)
    if html is None:
        print("  [ssl fallback] using real Chrome browser")
        html = browser.fetch_html(url)
    return html


FETCH_ERROR = None  # distinct from [] (empty page) vs None (fetch failed)


def scrape_page(url: str) -> list[dict] | None:
    """
    Returns:
      list[dict]  — successfully scraped rows (may be empty if page has no movies)
      None        — fetch failed (network/SSL error); caller should not treat as end-of-pages
    """
    html = _fetch(url)
    if html is None:
        print("  Could not fetch page.")
        return None  # fetch error — not the same as empty page

    soup = BeautifulSoup(html, "html.parser")

    main = soup.find(id="main")
    if not main:
        print("  Could not find #main element — page structure may have changed.")
        return []  # page loaded but no listing found = genuine end of pages

    items = main.select("div > div > ul > li")
    if not items:
        items = main.find_all("li")

    results = []
    for li in items:
        div = li.find("div")
        if not div:
            continue
        text = div.get_text(separator=" ", strip=True)
        if not text:
            continue
        entry = parse_entry(text)
        if not entry:
            continue

        img_tag = li.select_one("div > div > a > img")
        if img_tag:
            img_url = (
                img_tag.get("data-src")
                or img_tag.get("data-lazy-src")
                or img_tag.get("src")
                or ""
            )
            if img_url.startswith("data:"):
                img_url = img_tag.get("data-src") or img_tag.get("data-lazy-src") or ""
            entry["img_url"] = img_url.strip()
        else:
            entry["img_url"] = ""

        print(f"  {entry['movie']} | {entry['year']} | {entry['lang']} | img={'yes' if entry['img_url'] else 'no'}")
        results.append(entry)

    return results
