# Movierulz Movie Scraper

A modular Python scraper that fetches movie listings from a Movierulz-style site, downloads poster images, fetches YouTube trailer URLs, and tracks everything in an Excel file with daily change history.

---

## Setup

**Requirements:** Python 3.10+

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 openpyxl cloudscraper playwright yt-dlp
playwright install chromium
```

---

## Usage

```bash
source venv/bin/activate

# Home page (latest movies)
python main.py home <url>

# Featured / category pages
python main.py featured <url> <start> [end | all]

# Search by keyword
python main.py search <url> <query> [--pages N]
```

### Examples

```bash
# Scrape home page
python main.py home https://www.5movierulz.graphics/

# Scrape featured page 1
python main.py featured https://www.5movierulz.graphics/category/featured/ 1

# Scrape featured pages 1 to 5
python main.py featured https://www.5movierulz.graphics/category/featured/ 1 5

# Scrape all featured pages
python main.py featured https://www.5movierulz.graphics/category/featured/ all

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

### Poster images — `download/`

```
download/
├── home/
│   ├── 06-02-2026/     ← one folder per day
│   └── 06-03-2026/
└── featured/
    ├── 1/              ← one folder per page
    └── 715/
```

---

## Modules

| File | Purpose |
|---|---|
| `modules/config.py` | Paths, headers, known languages |
| `modules/parser.py` | Text parsing, language detection |
| `modules/scraper.py` | HTTP fetch with Cloudflare bypass |
| `modules/browser.py` | Persistent Chrome session via Playwright |
| `modules/downloader.py` | Poster image downloads |
| `modules/exporter.py` | Excel read/write with deduplication |
| `modules/trailer.py` | YouTube trailer URL search via yt-dlp |
| `modules/home.py` | Home page module |
| `modules/featured.py` | Featured/category page module |
| `modules/search.py` | Search module |
