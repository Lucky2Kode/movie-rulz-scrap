import time
from .parser import search_url
from .scraper import scrape_page


def run(base_url: str, query: str, pages: int = 1) -> list[dict]:
    """Search for movies by keyword across one or more result pages."""
    all_rows = []
    for page in range(1, pages + 1):
        url = search_url(page, base_url, query)
        print(f"--- [search] Page {page}: {url}")
        rows = scrape_page(url)
        if rows is None:
            print(f"  [skip] page {page} could not be fetched.")
            continue
        if not rows:
            print(f"  No results on page {page}, stopping.")
            break
        for row in rows:
            row["page"] = page
        all_rows.extend(rows)
        if page < pages:
            time.sleep(0.5)
    return all_rows
