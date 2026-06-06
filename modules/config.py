import sys
import warnings
from pathlib import Path

import cloudscraper

BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent.parent

# Change these URLs here to switch default scrape targets
# DEFAULT_HOME_URL = "https://www.5movierulz.graphics/"  # previous
DEFAULT_HOME_URL = "https://www.5movierulz.discount/"
DEFAULT_FEATURED_URL = "https://www.5movierulz.graphics/category/featured/"
DEFAULT_BOLLYWOOD_BASE_URL = "https://www.5movierulz.graphics/bollywood-movie-free/"
# DEFAULT_MALAYALAM_BASE_URL = "https://www.5movierulz.graphics/category/malayalam-movie-YYYY/"  # previous
# DEFAULT_MALAYALAM_BASE_URL = "https://www.5movierulz.discount/category/malayalam-movies-YYYY"  # previous
DEFAULT_MALAYALAM_BASE_URL = "https://www.5movierulz.discount/category/malayalam-featured"
DEFAULT_TAMIL_BASE_URL = "https://www.5movierulz.discount/category/tamil-featured"
DEFAULT_HOLLYWOOD_BASE_URL = "https://www.5movierulz.discount/category/hollywood-featured"
DEFAULT_TELUGU_BASE_URL = "https://www.5movierulz.discount/category/telugu-featured"
DOWNLOAD_DIR = BASE_DIR / "downloads"
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
