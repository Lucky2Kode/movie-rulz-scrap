import time
from .scraper import scrape_page


def _movies_page_url(page: int, base: str) -> str:
    """Build paginated movies URL: base/movies/page/{page}"""
    base = base.rstrip("/")
    return f"{base}/movies/page/{page}"


def run(base_url: str, start: int = None, end: int = None) -> list[dict]:
    """
    Scrape the site home page or paginated movies listing.
    - No start/end → scrapes base_url directly (home page)
    - start/end given → scrapes base/movies/page/{n} for each page
    """
    all_rows = []

    if start is None:
        # Home page mode — scrape the base URL as-is
        url = base_url.rstrip("/") + "/"
        print(f"--- [home] {url}")
        rows = scrape_page(url)
        if rows is None:
            print("  [skip] home page could not be fetched.")
            return all_rows
        for row in rows:
            row["page"] = 1
        all_rows.extend(rows)
    else:
        # Paginated mode — scrape movies/page/{n}
        for page in range(start, end + 1):
            url = _movies_page_url(page, base_url)
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
