import re
from .config import KNOWN_LANGS


def page_url(page: int, base: str) -> str:
    base = base.rstrip("/") + "/"
    if page <= 1:
        return base
    return f"{base}page/{page}/"


def search_url(page: int, base: str, query: str) -> str:
    base = base.rstrip("/") + "/"
    encoded = query.replace(" ", "+")
    if page <= 1:
        return f"{base}?s={encoded}"
    return f"{base}page/{page}/?s={encoded}"


def parse_entry(text: str) -> dict:
    text = text.strip()
    if not text:
        return None

    year_match = re.search(r'\((\d{4})\)', text)
    if year_match:
        year = year_match.group(1)
        movie = re.sub(r'\s+', ' ', text[:year_match.start()]).strip()
        after_year = text[year_match.end():]
    else:
        year = "N/A"
        movie = re.sub(r'\s+', ' ', text).strip()
        after_year = text

    if not movie:
        movie = re.sub(r'\s+', ' ', text).strip()

    qualifier = re.search(
        r'\b((?:Season|S)\s*\d+(?:\s*(?:Part|P|Ep(?:isode)?)\s*\d+)?'
        r'|(?:Part|P|Ep(?:isode)?)\s*\d+)\b',
        after_year, re.IGNORECASE
    )
    if qualifier:
        movie = f"{movie} {qualifier.group(1).strip()}"

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
    return lang.strip().title()


def safe_filename(movie: str, year: str, ext: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", movie).strip()
    name = re.sub(r'\s+', " ", name)
    return f"{name}{ext}"
