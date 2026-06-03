import re
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font
from pathlib import Path

BASE_URL = "https://www.5movierulz.graphics/bollywood-movie-free/"

# When packaged with PyInstaller --onefile, __file__ points to a temp dir.
# sys.executable always points to the actual binary/script location.
BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
DOWNLOAD_DIR = BASE_DIR / "download"


def page_url(page: int, base: str) -> str:
    base = base.rstrip("/") + "/"
    if page <= 1:
        return base
    return f"{base}page/{page}/"

KNOWN_LANGS = [
    "Telugu", "Tamil", "Hindi", "Malayalam", "Kannada",
    "Bengali", "Punjabi", "Marathi", "Gujarati", "Odia",
    "English", "Eng", "Korean", "Japanese", "Chinese",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def parse_entry(text: str) -> dict:
    text = text.strip()
    if not text:
        return None

    year_match = re.search(r'\((\d{4})\)', text)
    if year_match:
        year = year_match.group(1)
        # Everything before the year becomes the base title
        movie = re.sub(r'\s+', ' ', text[:year_match.start()]).strip()
        after_year = text[year_match.end():]
    else:
        year = "N/A"
        movie = re.sub(r'\s+', ' ', text).strip()
        after_year = text

    # Fallback: if title is empty, use full text
    if not movie:
        movie = re.sub(r'\s+', ' ', text).strip()

    # Append Season/Part/Episode qualifiers that appear after the year so that
    # "Movie (2023) Part 1" and "Movie (2023) Part 2" get distinct titles/keys.
    qualifier = re.search(
        r'\b((?:Season|S)\s*\d+(?:\s*(?:Part|P|Ep(?:isode)?)\s*\d+)?'
        r'|(?:Part|P|Ep(?:isode)?)\s*\d+)\b',
        after_year, re.IGNORECASE
    )
    if qualifier:
        movie = f"{movie} {qualifier.group(1).strip()}"

    # Check for bracket with multiple languages: [Telugu + Tamil + ...]
    bracket_match = re.search(r'\[([^\]]+)\]', after_year)
    if bracket_match:
        bracket_content = bracket_match.group(1)
        tokens = [t.strip() for t in re.split(r'\+|,', bracket_content)]
        lang_tokens = [t for t in tokens if any(
            lang.lower() in t.lower() for lang in KNOWN_LANGS
        )]
        if len(lang_tokens) >= 2:
            lang = "All"
        elif len(lang_tokens) == 1:
            lang = normalize_lang(lang_tokens[0])
        else:
            lang = detect_single_lang(after_year)
    else:
        lang = detect_single_lang(after_year)

    return {"movie": movie, "year": year, "lang": lang}


def detect_single_lang(text: str) -> str:
    for name in KNOWN_LANGS:
        if re.search(rf'\b{re.escape(name)}\b', text, re.IGNORECASE):
            return normalize_lang(name)
    return "Unknown"


def normalize_lang(lang: str) -> str:
    mapping = {"Eng": "English"}
    for key, val in mapping.items():
        if lang.strip().lower() == key.lower():
            return val
    # Capitalize properly
    return lang.strip().title()


def scrape(url: str) -> list[dict]:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    main = soup.find(id="main")
    if not main:
        print("Could not find #main element")
        return []

    items = main.select("div > div > ul > li")
    if not items:
        # Fallback: any li inside main
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

        # Extract image URL: li > div > div > a > img
        img_tag = li.select_one("div > div > a > img")
        if img_tag:
            # Handle lazy-loaded images (data-src takes priority over src)
            img_url = (
                img_tag.get("data-src")
                or img_tag.get("data-lazy-src")
                or img_tag.get("src")
                or ""
            )
            # Skip placeholder/base64 data URIs
            if img_url.startswith("data:"):
                img_url = img_tag.get("data-src") or img_tag.get("data-lazy-src") or ""
            entry["img_url"] = img_url.strip()
        else:
            entry["img_url"] = ""

        print(f"  {entry['movie']} | {entry['year']} | {entry['lang']} | img={'yes' if entry['img_url'] else 'no'}")
        results.append(entry)

    return results


def safe_filename(movie: str, year: str, ext: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", movie).strip()
    name = re.sub(r'\s+', " ", name)
    return f"{name} ({year}){ext}"


def download_images(rows: list[dict]):
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    # Group rows by page so each page gets its own subfolder
    pages: dict[int, list[dict]] = {}
    for row in rows:
        pages.setdefault(row.get("page", 0), []).append(row)

    for page_num, page_rows in sorted(pages.items()):
        folder = DOWNLOAD_DIR / f"page_{page_num}"
        folder.mkdir(exist_ok=True)
        print(f"  [page {page_num}] -> {folder}")

        seen: set[str] = set()
        for row in page_rows:
            url = row.get("img_url", "")
            if not url:
                continue

            # Deduplicate within the same page (multiple dub entries share one poster)
            key = f"{row['movie']}_{row['year']}"
            if key in seen:
                row["img_file"] = f"page_{page_num}/" + safe_filename(row["movie"], row["year"], Path(url.split("?")[0]).suffix or ".jpg")
                continue
            seen.add(key)

            ext = Path(url.split("?")[0]).suffix or ".jpg"
            filename = safe_filename(row["movie"], row["year"], ext)
            dest = folder / filename

            if dest.exists():
                print(f"    [skip] {filename}")
                row["img_file"] = f"page_{page_num}/{filename}"
                continue

            try:
                resp = requests.get(url, headers=HEADERS, timeout=20)
                resp.raise_for_status()
                dest.write_bytes(resp.content)
                print(f"    [saved] {filename}")
                row["img_file"] = f"page_{page_num}/{filename}"
                time.sleep(0.3)
            except Exception as e:
                print(f"    [error] {filename}: {e}")
                row["img_file"] = ""


def write_excel(rows: list[dict], out_path: Path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Movies"

    headers = ["Movie", "Year", "Lang", "Image File"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in rows:
        page = row.get("page")
        page_label = f"page {page}" if page else ""
        ws.append([row["movie"], row["year"], row["lang"], page_label])

    # Auto-fit column widths (approximate)
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 60)

    wb.save(out_path)
    print(f"\nSaved {len(rows)} entries to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape featured movies to Excel + download posters",
        usage="%(prog)s <url> <start> [end]",
    )
    parser.add_argument("url", help="Base category URL (e.g. https://site.com/category/featured/)")
    parser.add_argument("start", type=int, help="Start page number")
    parser.add_argument("end", nargs="?", type=int, help="End page number (optional, for range)")
    args = parser.parse_args()

    start = args.start
    end = args.end if args.end is not None else start
    if end < start:
        print(f"Error: end page ({end}) must be >= start page ({start})")
        raise SystemExit(1)

    print(f"Base URL : {args.url}")
    all_rows = []
    for page in range(start, end + 1):
        url = page_url(page, args.url)
        print(f"--- Page {page}: {url}")
        rows = scrape(url)
        for row in rows:
            row["page"] = page
        all_rows.extend(rows)
        if page < end:
            time.sleep(0.5)

    if not all_rows:
        print("No movie entries found.")
    else:
        print(f"\nDownloading images to {DOWNLOAD_DIR} ...\n")
        download_images(all_rows)
        out = BASE_DIR / "movies.xlsx"
        write_excel(all_rows, out)
