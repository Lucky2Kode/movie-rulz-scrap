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

# Home page (latest movies) — URL optional, defaults to config
python main.py home [start] [end] [--url URL]

# Featured / category pages — URL optional, defaults to config
python main.py featured [start] [end | all] [--url URL]

# Bollywood listing — URL optional, defaults to config
python main.py bollywood [start] [end | all] [--url URL]

# Malayalam listing — URL optional, defaults to config
python main.py malayalam [start] [end | all] [--url URL]

# Tamil listing — URL optional, defaults to config
python main.py tamil [start] [end | all] [--url URL]

# Hollywood listing — URL optional, defaults to config
python main.py hollywood [start] [end | all] [--url URL]

# Telugu listing — URL optional, defaults to config
python main.py telugu [start] [end | all] [--url URL]

# Search by keyword
python main.py search <url> <query> [--pages N]
```

Default URLs are set in `modules/config.py` — change them there to update globally.

### Examples

```bash
# Home — scrape page 1 (uses default URL)
python main.py home

# Home — scrape pages 1 to 3
python main.py home 1 3

# Featured — scrape pages 1 to 5
python main.py featured 1 5

# Featured — scrape all pages
python main.py featured 1 all

# Bollywood — scrape pages 1 to 41
python main.py bollywood 1 41

# Malayalam — scrape page 1
python main.py malayalam 1

# Malayalam — scrape pages 1 to 45
python main.py malayalam 1 45

# Malayalam — scrape all pages
python main.py malayalam 1 all

# Tamil — scrape page 1
python main.py tamil 1

# Tamil — scrape pages 1 to 45
python main.py tamil 1 45

# Tamil — scrape all pages
python main.py tamil 1 all

# Hollywood — scrape page 1
python main.py hollywood 1

# Hollywood — scrape pages 1 to 20
python main.py hollywood 1 20

# Hollywood — scrape all pages
python main.py hollywood 1 all

# Telugu — scrape page 1
python main.py telugu 1

# Telugu — scrape pages 1 to 20
python main.py telugu 1 20

# Telugu — scrape all pages
python main.py telugu 1 all

# Override URL explicitly
python main.py home 1 3 --url https://www.5movierulz.graphics/
python main.py featured 1 5 --url https://www.5movierulz.graphics/category/featured/
python main.py bollywood 1 10 --url https://www.5movierulz.graphics/bollywood-movie-free/
python main.py malayalam 1 10 --url https://www.5movierulz.discount/category/malayalam-featured
python main.py tamil 1 10 --url https://www.5movierulz.discount/category/tamil-featured
python main.py hollywood 1 10 --url https://www.5movierulz.discount/category/hollywood-featured
python main.py telugu 1 10 --url https://www.5movierulz.discount/category/telugu-featured

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
- **Named tab** (Home / Featured / Bollywood / Malayalam / Tamil / Hollywood / Telugu) — full listing, newest entries at the top, no duplicates ever
- **Daily Summary** — newest date at top, shows date and total movies added per day

### Poster images — `downloads/`

```
downloads/
├── home/
│   ├── 06-02-2026/     ← one folder per day (new movies only)
│   └── 06-03-2026/
├── featured/
│   ├── 06-02-2026/
│   └── 06-03-2026/
├── bollywood/
│   ├── 06-02-2026/
│   └── 06-03-2026/
├── malayalam/
│   ├── 06-02-2026/
│   └── 06-03-2026/
├── tamil/
│   ├── 06-02-2026/
│   └── 06-03-2026/
├── hollywood/
│   ├── 06-02-2026/
│   └── 06-03-2026/
└── telugu/
    ├── 1/              ← page-based folders
    ├── 2/
    └── 3/
```

### Daily deduplication

Running the scraper multiple times is safe — it is fully idempotent:
- Movies already in the Excel file are skipped (never added twice)
- Images already on disk are never re-downloaded
- Each day a new date folder is created; only that day's new movies go into it
- The **Daily Summary** tab is automatically updated after every run (newest date at top)

---

## Modules

| File | Purpose |
|---|---|
| `modules/config.py` | Paths, default URLs, known languages |
| `modules/parser.py` | Text parsing, language detection |
| `modules/scraper.py` | HTTP fetch with Cloudflare bypass |
| `modules/browser.py` | Persistent Chrome session via Playwright |
| `modules/downloader.py` | Poster image downloads |
| `modules/exporter.py` | Excel read/write with deduplication and multi-tab support |
| `modules/trailer.py` | YouTube trailer URL search via yt-dlp |
| `modules/home.py` | Home page module |
| `modules/featured.py` | Featured/category page module |
| `modules/bollywood.py` | Bollywood listing module |
| `modules/malayalam.py` | Malayalam listing module |
| `modules/tamil.py` | Tamil listing module |
| `modules/hollywood.py` | Hollywood listing module |
| `modules/telugu.py` | Telugu listing module |
| `modules/search.py` | Search module |
