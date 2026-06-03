import time
from .parser import page_url
from .scraper import scrape_page


def run(base_url: str, start: int = 1, end: int = 1) -> list[dict]:
    """Scrape the site home page (latest/recent movies)."""
    all_rows = []
    for page in range(start, end + 1):
        url = page_url(page, base_url)
        print(f"--- [home] Page {page}: {url}")
        rows = scrape_page(url)
        if rows is None:
            print(f"  [skip] page {page} could not be fetched.")
            continue
        for row in rows:
            row["page"] = page
        all_rows.extend(rows)
        if page < end:
            time.sleep(0.5)
    return all_rows
