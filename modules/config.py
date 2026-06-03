import sys
import warnings
from pathlib import Path

import cloudscraper

BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent.parent
DOWNLOAD_DIR = BASE_DIR / "download"
OUTPUT_DIR = BASE_DIR / "output"

KNOWN_LANGS = [
    "Telugu", "Tamil", "Hindi", "Malayalam", "Kannada",
    "Bengali", "Punjabi", "Marathi", "Gujarati", "Odia",
    "English", "Eng", "Korean", "Japanese", "Chinese",
]

warnings.filterwarnings("ignore", message="Unverified HTTPS request")


def make_session() -> cloudscraper.CloudScraper:
    """Return a session that bypasses Cloudflare bot protection."""
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "darwin", "mobile": False}
    )
    return scraper
