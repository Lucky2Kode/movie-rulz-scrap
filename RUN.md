# Running the Scraper (No Python Required)

The `dist/scrape_movies` file is a standalone executable for macOS — no Python or dependencies needed.

## First-Time Setup

Open Terminal and make the file executable:

```bash
chmod +x dist/scrape_movies
```

## Usage

```
./dist/scrape_movies <url> <start_page> [end_page]
```

| Argument | Required | Description |
|---|---|---|
| `url` | Yes | Base category URL of the movie listing page |
| `start_page` | Yes | Page number to start scraping from |
| `end_page` | No | Page number to stop at (scrapes a range if provided) |

## Examples

**Scrape page 1 only:**
```bash
./dist/scrape_movies https://www.5movierulz.graphics/bollywood-movie-free/ 1
```

**Scrape pages 2 to 5:**
```bash
./dist/scrape_movies https://www.5movierulz.graphics/bollywood-movie-free/ 2 5
```

## Output

After running, two things are created in the same folder:

- `movies.xlsx` — Excel file with columns: Movie, Year, Lang, Image File
- `download/page_1/`, `download/page_2/`, ... — Poster images organized by page

## Notes

- This binary runs on Apple Silicon Macs (M1/M2/M3/M4). For Intel Macs, rebuild from source using PyInstaller.
- Re-running the script skips already-downloaded images (`[skip]` shown in output).
