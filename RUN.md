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

### `home` — Scrape the home page (latest movies)

Scrapes the main page of the site for the most recently added movies.

The URL is optional — defaults to `DEFAULT_HOME_URL` set in `modules/config.py`.

```bash
# Basic run — scrape page 1 (uses default URL)
python main.py home

# Scrape multiple pages (uses default URL)
python main.py home 1 3

# Skip image downloads (faster, Excel only)
python main.py home --no-images

# Skip trailer fetch
python main.py home --no-trailers

# Skip both images and trailers
python main.py home --no-images --no-trailers

# Override with a different URL
python main.py home 1 3 --url https://www.movierulz.com/
```

**Output:**
- Excel → `output/home.xlsx`
- Images → `downloads/home/06-02-2026/` (one folder per day, new movies only)

---

### `featured` — Scrape a category/listing page

Scrapes a specific category like featured, Bollywood, Telugu, etc.

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
- Excel → `output/featured.xlsx`
- Images → `downloads/featured/1/`, `downloads/featured/2/`, ... (one folder per page)

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

**Tab 2 — Daily Summary**

| Date | New Movies Added |
|---|---|
| 2026-06-02 | 24 |
| 2026-06-03 | 6 |

---

### Image folders (`downloads/`)

```
downloads/
├── home/
│   ├── 06-02-2026/        ← movies added on June 2
│   │   ├── Pushpa 2.jpg
│   │   └── RRR.jpg
│   └── 06-03-2026/        ← movies added on June 3 (new only)
└── featured/
    ├── 1/                 ← images from page 1
    ├── 2/                 ← images from page 2
    └── 715/               ← images from page 715
```

---

## Daily Usage (Recommended)

Run the home scraper once a day to track new movies:

```bash
source venv/bin/activate
python main.py home
```

- First run of the day → downloads new movie posters + trailers, updates Excel
- Second run same day → skips everything already downloaded, adds only brand-new entries
- Next day → creates a new date folder, appends to the same Excel file

---

## Get Help

```bash
python main.py --help
python main.py home --help
python main.py featured --help
python main.py search --help
```
