# Running the Movierulz Scraper

Two ways to run: using Python directly, or using the prebuilt macOS binary (no Python needed).

---

## Option A — Run with Python

### Step 1: Set up the virtual environment (one-time only)

```bash
python3 -m venv venv
venv/bin/pip install requests beautifulsoup4 openpyxl
```

### Step 2: Run a module

```bash
venv/bin/python main.py <module> <url> <options>
```

---

## Modules

### `featured` — Scrape a category/listing page

Scrapes a specific movie category (e.g. Bollywood, Telugu, Hollywood).

```bash
# Scrape page 1 only
venv/bin/python main.py featured https://www.5movierulz.graphics/bollywood-movie-free/ 1

# Scrape pages 1 to 3
venv/bin/python main.py featured https://www.5movierulz.graphics/bollywood-movie-free/ 1 3

# Scrape Telugu movies, pages 2 to 5
venv/bin/python main.py featured https://www.5movierulz.graphics/telugu-movie-free/ 2 5
```

---

### `home` — Scrape the site home page

Scrapes the latest/recent movies listed on the main page.

```bash
# Scrape home page 1
venv/bin/python main.py home https://www.5movierulz.graphics/ 1

# Scrape home pages 1 and 2
venv/bin/python main.py home https://www.5movierulz.graphics/ 1 2
```

---

### `search` — Search movies by keyword

Searches the site for a movie name or keyword.

```bash
# Search for "RRR" (1 result page)
venv/bin/python main.py search https://www.5movierulz.graphics/ "RRR"

# Search for "Pushpa" across 3 result pages
venv/bin/python main.py search https://www.5movierulz.graphics/ "Pushpa" --pages 3

# Search for Telugu movies from 2026
venv/bin/python main.py search https://www.5movierulz.graphics/ "Telugu 2026" --pages 2
```

---

### `--no-images` flag

Add this to any command to skip downloading poster images and only generate the Excel file.

```bash
venv/bin/python main.py featured https://www.5movierulz.graphics/bollywood-movie-free/ 1 3 --no-images

venv/bin/python main.py search https://www.5movierulz.graphics/ "RRR" --no-images
```

---

## Output

After every run, two things are created in the project folder:

| What | Where | Example |
|---|---|---|
| Excel file | `output/<module>.xlsx` | `output/featured.xlsx` |
| Poster images | `download/<module>_<page>/` | `download/featured_1/RRR (2022).jpg` |

**Excel columns:** Movie | Year | Lang | Page | Image File

---

## Console output example

```
--- [featured] Page 1: https://www.5movierulz.graphics/bollywood-movie-free/
  RRR | 2022 | All | img=yes
  Pushpa The Rise | 2021 | Telugu | img=yes
  KGF Chapter 2 | 2022 | All | img=yes

Downloading images to .../download ...
  [featured_1] -> download/featured_1
    [saved] RRR (2022).jpg
    [saved] Pushpa The Rise (2021).jpg
    [skip]  KGF Chapter 2 (2022).jpg

Saved 3 entries to output/featured.xlsx
```

---

## Get help

```bash
# All commands
venv/bin/python main.py --help

# Help for a specific module
venv/bin/python main.py featured --help
venv/bin/python main.py home --help
venv/bin/python main.py search --help
```

---

## Option B — Run with the prebuilt binary (no Python needed)

The `dist/scrape_movies` file is a standalone executable for macOS (Apple Silicon — M1/M2/M3/M4).

### Step 1: Make it executable (one-time only)

```bash
chmod +x dist/scrape_movies
```

### Step 2: Run it

```bash
# Scrape a category page
./dist/scrape_movies https://www.5movierulz.graphics/bollywood-movie-free/ 1

# Scrape a range of pages
./dist/scrape_movies https://www.5movierulz.graphics/bollywood-movie-free/ 1 3
```

> **Note:** The binary uses the original single-file interface (url + page numbers only).
> For the full `home` / `featured` / `search` modules, use Option A with Python.

> **Intel Mac users:** The binary only runs on Apple Silicon. Rebuild from source using PyInstaller:
> ```bash
> venv/bin/pip install pyinstaller
> venv/bin/pyinstaller scrape_movies.spec
> ```
