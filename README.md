# Movierulz Featured Movies Scraper

A Python script that scrapes the featured movies listing, extracts movie metadata (title, year, language), downloads poster images, and saves everything into an Excel file.

---

## What It Does

1. Fetches the featured movies page(s) from the site
2. Parses each movie entry to extract:
   - **Movie name** — title without year or quality tags
   - **Year** — release year from the listing
   - **Language** — single language (e.g. `Tamil`) or `All` when multiple languages are listed
3. Downloads the poster image for each unique movie into the `download/` folder
4. Writes all entries to `movies.xlsx` with columns: `Movie | Year | Lang | Image File`

---

## Project Structure

```
Movierulz/
├── scrape_movies.py   # Main scraper script
├── movies.xlsx        # Output Excel file (created on first run)
├── download/          # Downloaded poster images (created on first run)
│   ├── Arjun Son of Vyjayanthi (2026).jpg
│   └── ...
├── venv/              # Python virtual environment
└── README.md
```

---

## Setup

**Requirements:** Python 3.8+

Create the virtual environment and install dependencies (one-time setup):

```bash
python3 -m venv venv
venv/bin/pip install requests beautifulsoup4 openpyxl
```

---

## Commands

### Scrape page 1 (default)
```bash
venv/bin/python scrape_movies.py
```

### Scrape a specific page
```bash
venv/bin/python scrape_movies.py 3
```
Fetches: `https://www.5movierulz.graphics/category/featured/page/3/`

### Scrape a range of pages
```bash
venv/bin/python scrape_movies.py 2 5
```
Fetches pages 2, 3, 4, and 5 in sequence and combines all results into a single Excel file.

---

## Language Detection Logic

Each movie listing looks like:

```
Arjun Son of Vyjayanthi (2026) HDRip Tamil (Original) Full Movie Watch Online Free
Project Hail Mary (2026) HDRip Original Audios [Telugu + Tamil + Hindi + Malayalam + Kannada + Eng] Dubbed Full Movie Watch Online Free
```

| Condition | Result |
|---|---|
| Single language in listing | That language (e.g. `Tamil`, `Hindi`) |
| Multiple languages in `[Lang1 + Lang2 + ...]` | `All` |
| No recognisable language found | `Unknown` |

Supported languages: Telugu, Tamil, Hindi, Malayalam, Kannada, Bengali, Punjabi, Marathi, Gujarati, Odia, English, Korean, Japanese, Chinese.

---

## Image Downloads

- Posters are saved as `Movie Name (Year).jpg` in the `download/` folder
- If the same movie appears multiple times (different dub versions), the poster is downloaded only once
- Already-downloaded posters are skipped on subsequent runs (`[skip]` in output)
- A short delay (0.3s) is added between image downloads

---

## Output

**Console output** shows progress for each page:
```
--- Page 2: https://www.5movierulz.graphics/category/featured/page/2/
  Love Mocktail 3 | 2026 | Kannada | img=yes
  Enola Holmes | 2020 | All | img=yes
  ...

Downloading images to .../download ...
  [saved] Love Mocktail 3 (2026).jpg
  [skip]  Dacoit (2026).jpg already exists
  ...

Saved 16 entries to .../movies.xlsx
```

**movies.xlsx** columns:

| Movie | Year | Lang | Image File |
|---|---|---|---|
| Love Mocktail 3 | 2026 | Kannada | Love Mocktail 3 (2026).jpg |
| Project Hail Mary | 2026 | All | Project Hail Mary (2026).jpg |
