# Step-by-Step Guide

## Step 1 — First-Time Setup (run once only)

Create the virtual environment and install all dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

---

## Step 2 — Activate the Virtual Environment

Run this every time you open a new terminal before using the scraper:

```bash
source venv/bin/activate
```

Your prompt will change to show `(venv)` confirming it's active:
```
(venv) Movierulz %
```

To deactivate when done:
```bash
deactivate
```

---

## Step 3 — Run the Scraper

### `home` — Scrape the home page (no page args)

Scrapes `https://www.5movierulz.discount/` directly — the home/latest movies page.

```bash
# Scrape home page (uses default URL)
python main.py home

# Skip image downloads
python main.py home --no-images

# Skip trailer fetch
python main.py home --no-trailers

# Skip both
python main.py home --no-images --no-trailers
```

**Output:**
- Excel → `output/home.xlsx` (Home tab + Daily Summary tab)
- Images → `downloads/home/MM-DD-YYYY/` (date-based, new movies only)

---

### `home` with page numbers — Scrape paginated movies listing

When page numbers are passed, scrapes `https://www.5movierulz.discount/movies/page/{n}` and writes to a **separate** Excel file.

```bash
# Scrape page 1 of movies listing
python main.py home 1

# Scrape pages 1 to 5
python main.py home 1 5

# Skip image downloads
python main.py home 1 5 --no-images

# Skip both
python main.py home 1 5 --no-images --no-trailers
```

**Output:**
- Excel → `output/homeNpages.xlsx` (HomeNPages tab + Daily Summary tab)
- Images → `downloads/homeNpages/1/`, `downloads/homeNpages/2/` … (page-based folders)

---

### `featured` — Scrape a category/listing page

Scrapes a specific category like featured, Telugu, etc.

The URL is optional — defaults to `DEFAULT_FEATURED_URL` set in `modules/config.py`.
Pass only page numbers; the scraper automatically appends `page/{number}/` to the base URL.

```bash
# Scrape page 1 only (uses default URL)
python main.py featured 1

# Scrape a range of pages (pages 1 to 5, uses default URL)
python main.py featured 1 5

# Scrape ALL pages automatically (stops when no more movies found)
python main.py featured 1 all

# Scrape all pages, skip images
python main.py featured 1 all --no-images

# Scrape all pages, skip trailers
python main.py featured 1 all --no-trailers

# Scrape all pages, skip both
python main.py featured 1 all --no-images --no-trailers

# Override with a different category URL
python main.py featured 1 10 --url https://www.5movierulz.graphics/telugu-movie-free/
```

**Output:**
- Excel → `output/featured.xlsx` (Featured tab + Daily Summary tab)
- Images → `downloads/featured/MM-DD-YYYY/` (one folder per day, new movies only)

---

### `bollywood` — Scrape the Bollywood listing

Scrapes the Bollywood movies listing page.

The URL is optional — defaults to `DEFAULT_BOLLYWOOD_BASE_URL` set in `modules/config.py`.
Pass only page numbers; the scraper automatically appends `page/{number}/` to the base URL.

```bash
# Scrape page 1 only (uses default URL)
python main.py bollywood 1

# Scrape a range of pages (pages 1 to 41)
python main.py bollywood 1 41

# Scrape ALL pages automatically
python main.py bollywood 1 all

# Skip image downloads
python main.py bollywood 1 41 --no-images

# Skip trailer fetch
python main.py bollywood 1 41 --no-trailers

# Skip both
python main.py bollywood 1 41 --no-images --no-trailers

# Override with a different URL
python main.py bollywood 1 10 --url https://www.5movierulz.graphics/bollywood-movie-free/
```

**Output:**
- Excel → `output/bollywood.xlsx` (Bollywood tab + Daily Summary tab)
- Images → `downloads/bollywood/MM-DD-YYYY/` (one folder per day, new movies only)

---

### `malayalam` — Scrape the Malayalam listing

Scrapes the Malayalam featured movies listing page.

The URL is optional — defaults to `DEFAULT_MALAYALAM_BASE_URL` set in `modules/config.py`.
Pass only page numbers; the scraper automatically appends `page/{number}` to the base URL.

```bash
# Scrape page 1 only (uses default URL)
python main.py malayalam 1

# Scrape a range of pages (pages 1 to 45)
python main.py malayalam 1 45

# Scrape ALL pages automatically
python main.py malayalam 1 all

# Skip image downloads
python main.py malayalam 1 45 --no-images

# Skip trailer fetch
python main.py malayalam 1 45 --no-trailers

# Skip both
python main.py malayalam 1 45 --no-images --no-trailers

# Override with a different URL
python main.py malayalam 1 10 --url https://www.5movierulz.discount/category/malayalam-featured
```

**Output:**
- Excel → `output/malayalam.xlsx` (Malayalam tab + Daily Summary tab)
- Images → `downloads/malayalam/MM-DD-YYYY/` (one folder per day, new movies only)

---

### `tamil` — Scrape the Tamil listing

Scrapes the Tamil featured movies listing page.

The URL is optional — defaults to `DEFAULT_TAMIL_BASE_URL` set in `modules/config.py`.
Pass only page numbers; the scraper automatically appends `page/{number}` to the base URL.

```bash
# Scrape page 1 only (uses default URL)
python main.py tamil 1

# Scrape a range of pages (pages 1 to 45)
python main.py tamil 1 45

# Scrape ALL pages automatically
python main.py tamil 1 all

# Skip image downloads
python main.py tamil 1 45 --no-images

# Skip trailer fetch
python main.py tamil 1 45 --no-trailers

# Skip both
python main.py tamil 1 45 --no-images --no-trailers

# Override with a different URL
python main.py tamil 1 10 --url https://www.5movierulz.discount/category/tamil-featured
```

**Output:**
- Excel → `output/tamil.xlsx` (Tamil tab + Daily Summary tab)
- Images → `downloads/tamil/MM-DD-YYYY/` (one folder per day, new movies only)

---

### `hollywood` — Scrape the Hollywood listing

Scrapes the Hollywood featured movies listing page.

The URL is optional — defaults to `DEFAULT_HOLLYWOOD_BASE_URL` set in `modules/config.py`.
Pass only page numbers; the scraper automatically appends `page/{number}` to the base URL.

```bash
# Scrape page 1 only (uses default URL)
python main.py hollywood 1

# Scrape a range of pages (pages 1 to 20)
python main.py hollywood 1 20

# Scrape ALL pages automatically
python main.py hollywood 1 all

# Skip image downloads
python main.py hollywood 1 20 --no-images

# Skip trailer fetch
python main.py hollywood 1 20 --no-trailers

# Skip both
python main.py hollywood 1 20 --no-images --no-trailers

# Override with a different URL
python main.py hollywood 1 10 --url https://www.5movierulz.discount/category/hollywood-featured
```

**Output:**
- Excel → `output/hollywood.xlsx` (Hollywood tab + Daily Summary tab)
- Images → `downloads/hollywood/MM-DD-YYYY/` (one folder per day, new movies only)

---

### `telugu` — Scrape the Telugu listing

Scrapes the Telugu featured movies listing page.

The URL is optional — defaults to `DEFAULT_TELUGU_BASE_URL` set in `modules/config.py`.
Pass only page numbers; the scraper automatically appends `page/{number}` to the base URL.
Images are saved in **page-based folders** (`downloads/telugu/1/`, `downloads/telugu/2/`, etc.).

```bash
# Scrape page 1 only (uses default URL)
python main.py telugu 1

# Scrape a range of pages (pages 1 to 20)
python main.py telugu 1 20

# Scrape ALL pages automatically
python main.py telugu 1 all

# Skip image downloads
python main.py telugu 1 20 --no-images

# Skip trailer fetch
python main.py telugu 1 20 --no-trailers

# Skip both
python main.py telugu 1 20 --no-images --no-trailers

# Override with a different URL
python main.py telugu 1 10 --url https://www.5movierulz.discount/category/telugu-featured
```

**Output:**
- Excel → `output/telugu.xlsx` (Telugu tab + Daily Summary tab)
- Images → `downloads/telugu/{page}/` (one folder per page number)

---

### `search` — Search movies by keyword

Searches the site for a specific movie name or keyword.

```bash
# Search for a movie (1 result page)
python main.py search https://www.5movierulz.graphics/ "RRR"

# Search across multiple result pages
python main.py search https://www.5movierulz.graphics/ "Pushpa" --pages 3

# Search with language filter
python main.py search https://www.5movierulz.graphics/ "Telugu 2026" --pages 2

# Search, skip images
python main.py search https://www.5movierulz.graphics/ "KGF" --pages 2 --no-images

# Search, skip trailers
python main.py search https://www.5movierulz.graphics/ "KGF" --pages 2 --no-trailers
```

**Output:**
- Excel → `output/search_RRR.xlsx` (named after the search query)
- Images → `downloads/search_RRR/1/`

---

## Output Structure

### Excel files (`output/`)

Each Excel file has **two tabs**:

**Tab 1 — Movies**

| Movie | Year | Lang | Page | Image File | Trailer URL | Date Added |
|---|---|---|---|---|---|---|
| Pushpa 2 | 2024 | Telugu | 1 | downloads/home/... | youtube.com/... | 2026-06-02 |

- Newest entries always appear at the **top**
- Duplicate movies are **never added twice**

**Tab 2 — Daily Summary** (auto-updated after every run, newest date at top)

| Date | New Movies Added |
|---|---|
| 2026-06-06 | 16 |
| 2026-06-05 | 24 |
| 2026-06-02 | 6 |

---

### Image folders (`downloads/`)

```
downloads/
├── home/
│   ├── 06-02-2026/        ← date-based (python main.py home)
│   │   ├── Pushpa 2.jpg
│   │   └── RRR.jpg
│   └── 06-03-2026/
├── homeNpages/
│   ├── 1/                 ← page-based (python main.py home 1 5)
│   ├── 2/
│   └── 3/
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
    ├── 1/                 ← page-based (python main.py telugu 1 5)
    ├── 2/
    └── 3/
```

---

## Changing Default URLs

All default URLs are defined in `modules/config.py`:

```python
DEFAULT_HOME_URL = "https://www.5movierulz.discount/"
DEFAULT_FEATURED_URL = "https://www.5movierulz.graphics/category/featured/"
DEFAULT_BOLLYWOOD_BASE_URL = "https://www.5movierulz.graphics/bollywood-movie-free/"
DEFAULT_MALAYALAM_BASE_URL = "https://www.5movierulz.discount/category/malayalam-featured"
DEFAULT_TAMIL_BASE_URL = "https://www.5movierulz.discount/category/tamil-featured"
DEFAULT_HOLLYWOOD_BASE_URL = "https://www.5movierulz.discount/category/hollywood-featured"
DEFAULT_TELUGU_BASE_URL = "https://www.5movierulz.discount/category/telugu-featured"
```

Change any value here — it takes effect everywhere without touching any other file.

---

## Daily Usage (Recommended)

Run these once a day to track new movies:

```bash
source venv/bin/activate
python main.py home
python main.py featured 1 5
python main.py bollywood 1 5
python main.py malayalam 1 5
python main.py tamil 1 5
python main.py hollywood 1 5
python main.py telugu 1 5
```

**How deduplication works:**
- Movies already in the Excel file are never added twice
- Images already on disk are never re-downloaded
- Each day a new date folder is created — only that day's new movies go into it
- Running the same command twice on the same day is completely safe

**What each run does:**
- First run of the day → downloads new posters + trailers, writes new rows to Excel, updates Daily Summary tab
- Second run same day → skips all already-seen movies, adds only brand-new entries
- Next day → creates a new date folder, appends new movies to the same Excel file

**Excel tabs:**
- **Home / HomeNPages / Featured / Bollywood / Malayalam / Tamil / Hollywood / Telugu** — full listing per command, newest entries at the top, no duplicates ever
- **Daily Summary** — newest date always at top, shows total movies added per day

---

## Get Help

```bash
python main.py --help
python main.py home --help
python main.py featured --help
python main.py bollywood --help
python main.py malayalam --help
python main.py tamil --help
python main.py hollywood --help
python main.py telugu --help
python main.py search --help
```
