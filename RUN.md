# Quick Start

## 1. Activate the virtual environment

```bash
source venv/bin/activate
```

Your prompt will show `(venv)` when active. After that just use `python`.

## 2. Run

```bash
# Home page
python main.py home https://www.5movierulz.graphics/

# Featured category — single page
python main.py featured https://www.5movierulz.graphics/category/featured/ 1

# Featured category — page range
python main.py featured https://www.5movierulz.graphics/category/featured/ 1 5

# Featured category — all pages
python main.py featured https://www.5movierulz.graphics/category/featured/ all

# Search
python main.py search https://www.5movierulz.graphics/ "Pushpa" --pages 3
```

## Skip options

```bash
--no-images     Don't download posters
--no-trailers   Don't fetch YouTube trailer URLs
```

## Output

- `output/home.xlsx` / `output/featured.xlsx` — Excel with Movies + Daily Summary tabs
- `download/home/06-02-2026/` — posters grouped by date
- `download/featured/1/` — posters grouped by page number
