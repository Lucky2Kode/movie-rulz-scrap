# Movierulz Movie Scraper

A modular Python scraper that fetches movie listings from a Movierulz-style site, downloads poster images, fetches YouTube trailer URLs, and tracks everything in an Excel file with daily change history.

---

## Setup

**Requirements:** Python 3.10+

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

---

## Usage

```bash
source venv/bin/activate

# Home page (latest movies) — URL optional, defaults to movierulz.com
python main.py home [start] [end] [--url URL]

# Featured / category pages — URL optional, defaults to featured category
python main.py featured [start] [end | all] [--url URL]

# Search by keyword
python main.py search <url> <query> [--pages N]
```

Default URLs are set in `modules/config.py` — change them there to update globally.

### Examples

```bash
# Scrape home page (uses default URL)
python main.py home

# Scrape home pages 1 to 3 (uses default URL)
python main.py home 1 3

# Scrape featured page 1 (uses default URL)
python main.py featured 1

# Scrape featured pages 1 to 5 (uses default URL)
python main.py featured 1 5

# Scrape all featured pages
python main.py featured 1 all

# Override URL explicitly
python main.py home 1 3 --url https://www.movierulz.com/
python main.py featured 1 5 --url https://www.5movierulz.graphics/category/featured/

# Search for a movie
python main.py search https://www.5movierulz.graphics/ "Pushpa" --pages 2
```

### Optional flags

```bash
--no-images     Skip image downloads
--no-trailers   Skip YouTube trailer fetch
```

---

## Output

### Excel files — `output/`

| Column | Description |
|---|---|
| Movie | Title |
| Year | Release year |
| Lang | Language(s) |
| Page | Page number scraped from |
| Image File | Relative path to poster |
| Trailer URL | YouTube trailer link |
| Date Added | Date first seen |

Each file has two tabs:
- **Movies** — full listing, newest entries at the top
- **Daily Summary** — count of new movies added per day

### Poster images — `downloads/`

```
downloads/
├── home/
│   ├── 06-02-2026/     ← one folder per day (new movies only)
│   └── 06-03-2026/
└── featured/
    ├── 06-02-2026/     ← one folder per day (new movies only)
    └── 06-03-2026/
```

### Daily deduplication

Running the scraper multiple times is safe — it is fully idempotent:
- Movies already in the Excel file are skipped (never added twice)
- Images already on disk are never re-downloaded
- Each day a new date folder is created; only that day's new movies go into it
- The **Daily Summary** tab is automatically updated after every run

---

## Modules

| File | Purpose |
|---|---|
| `modules/config.py` | Paths, default URLs, known languages |
| `modules/parser.py` | Text parsing, language detection |
| `modules/scraper.py` | HTTP fetch with Cloudflare bypass |
| `modules/browser.py` | Persistent Chrome session via Playwright |
| `modules/downloader.py` | Poster image downloads |
| `modules/exporter.py` | Excel read/write with deduplication |
| `modules/trailer.py` | YouTube trailer URL search via yt-dlp |
| `modules/home.py` | Home page module |
| `modules/featured.py` | Featured/category page module |
| `modules/search.py` | Search module |
