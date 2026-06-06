import time
from .scraper import scrape_page


def _page_url(page: int, base: str) -> str:
    """Build page URL without trailing slash after page number (required by .discount domain)."""
    base = base.rstrip("/") + "/"
    if page <= 1:
        return base
    return f"{base}page/{page}"


ALL_PAGES = -1
MAX_RETRIES = 2


def run(base_url: str, start: int = 1, end: int = 1) -> list[dict]:
    """
    Scrape Hollywood movies listing.
    Pass end=ALL_PAGES (-1) to scrape all pages until none are left.
    """
    all_rows = []
    page = start
    consecutive_errors = 0

    while True:
        url = _page_url(page, base_url)
        print(f"--- [hollywood] Page {page}: {url}")

        rows = None
        for attempt in range(1, MAX_RETRIES + 1):
            rows = scrape_page(url)
            if rows is not None:
                break
            if attempt < MAX_RETRIES:
                print(f"  [retry {attempt}/{MAX_RETRIES}] waiting 2s ...")
                time.sleep(2)

        if rows is None:
            consecutive_errors += 1
            print(f"  [skip] page {page} failed after {MAX_RETRIES} retries ({consecutive_errors} consecutive error(s))")
            if consecutive_errors >= 3:
                print("  3 consecutive errors — stopping.")
                break
            page += 1
            time.sleep(1)
            continue

        consecutive_errors = 0

        if not rows:
            print(f"  No results on page {page} — end of pages.")
            break

        for row in rows:
            row["page"] = page
        all_rows.extend(rows)
        print(f"  [{len(rows)} movies found, {len(all_rows)} total]")

        if end != ALL_PAGES and page >= end:
            break

        page += 1
        time.sleep(0.5)

    return all_rows
