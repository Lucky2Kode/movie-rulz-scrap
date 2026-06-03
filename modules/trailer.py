import time


def get_trailer_url(movie: str, year: str = "") -> str:
    """
    Search YouTube for '<movie> <year> trailer' and return the first result URL.
    Returns empty string if nothing found.
    """
    query = f"{movie} {year} trailer".strip()
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if result and result.get("entries"):
                video_id = result["entries"][0].get("id", "")
                if video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"  [trailer] {movie} -> {url}")
                    return url
    except Exception as e:
        print(f"  [trailer error] {movie}: {e}")
    return ""


def fetch_trailers(rows: list[dict], delay: float = 0.5) -> list[dict]:
    """
    Fetch trailer URLs for a list of movie rows.
    Adds/updates the 'trailer_url' key on each row in-place.
    Returns the same list.
    """
    print(f"\nFetching trailers for {len(rows)} movie(s) ...\n")
    for i, row in enumerate(rows):
        row["trailer_url"] = get_trailer_url(row.get("movie", ""), row.get("year", ""))
        if i < len(rows) - 1:
            time.sleep(delay)
    return rows
