import time
from pathlib import Path
import requests as _requests
from requests.exceptions import SSLError, ConnectionError
from .config import DOWNLOAD_DIR, make_session
from . import browser
from .parser import safe_filename

_PLAIN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.5movierulz.discount/",
}


def _download_bytes(url: str) -> bytes | None:
    # 1. Try cloudscraper (Cloudflare bypass)
    try:
        resp = make_session().get(url, timeout=20)
        resp.raise_for_status()
        return resp.content
    except (SSLError, ConnectionError):
        pass
    except Exception:
        return None

    # 2. Try plain requests with browser-like headers (faster than browser)
    try:
        resp = _requests.get(url, headers=_PLAIN_HEADERS, timeout=30, verify=False)
        resp.raise_for_status()
        return resp.content
    except Exception:
        pass

    # 3. Last resort: real Chrome browser
    return browser.fetch_bytes(url)


def download_images(rows: list[dict], label: str = "page", subdir: str = None):
    """
    Download poster images for the given rows.

    Folder structure:
      - subdir given  → download/<label>/<subdir>/   (e.g. home/06-02-2026/)
      - no subdir     → download/<label>/<page_num>/ (e.g. featured/1/)
    """
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    # Group rows: by fixed subdir (date) or by page number
    if subdir:
        groups = {subdir: rows}
    else:
        groups: dict = {}
        for row in rows:
            groups.setdefault(str(row.get("page", 0)), []).append(row)

    for group_key, group_rows in sorted(groups.items()):
        folder = DOWNLOAD_DIR / label / group_key
        folder.mkdir(parents=True, exist_ok=True)
        print(f"  [{label}/{group_key}] -> {folder}")

        seen: set[str] = set()
        for row in group_rows:
            url = row.get("img_url", "")
            if not url:
                continue

            key = f"{row['movie']}_{row['year']}"
            ext = Path(url.split("?")[0]).suffix or ".jpg"
            filename = safe_filename(row["movie"], row["year"], ext)

            if key in seen:
                row["img_file"] = f"{label}/{group_key}/{filename}"
                continue
            seen.add(key)

            dest = folder / filename
            if dest.exists():
                print(f"    [skip] {filename}")
                row["img_file"] = f"{label}/{group_key}/{filename}"
                continue

            data = _download_bytes(url)
            if data:
                dest.write_bytes(data)
                print(f"    [saved] {filename}")
                row["img_file"] = f"{label}/{group_key}/{filename}"
                time.sleep(0.3)
            else:
                print(f"    [error] {filename}: download failed")
                row["img_file"] = ""
