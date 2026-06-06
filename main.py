import sys
import argparse
from datetime import date
from modules import home, featured, search, bollywood, malayalam
from modules.downloader import download_images
from modules.exporter import filter_new, append_new, daily_summary
from modules.trailer import fetch_trailers
from modules.config import OUTPUT_DIR, DOWNLOAD_DIR, DEFAULT_HOME_URL, DEFAULT_FEATURED_URL, DEFAULT_BOLLYWOOD_BASE_URL, DEFAULT_MALAYALAM_BASE_URL


def cmd_home(args):
    rows = home.run(args.url, args.start, args.end)
    today = date.today().strftime("%m-%d-%Y")
    _finish(rows, "home", args, subdir=today)


def cmd_featured(args):
    rows = featured.run(args.url, args.start, args.end)
    today = date.today().strftime("%m-%d-%Y")
    _finish(rows, "featured", args, subdir=today)


def cmd_bollywood(args):
    rows = bollywood.run(args.url, args.start, args.end)
    today = date.today().strftime("%m-%d-%Y")
    _finish(rows, "bollywood", args, subdir=today)


def cmd_malayalam(args):
    rows = malayalam.run(args.url, args.start, args.end)
    today = date.today().strftime("%m-%d-%Y")
    _finish(rows, "malayalam", args, subdir=today)


def cmd_search(args):
    rows = search.run(args.url, args.query, args.pages)
    _finish(rows, f"search_{args.query.replace(' ', '_')}", args)


def _finish(rows: list[dict], label: str, args, subdir: str = None, sheet_name: str = None):
    if not rows:
        print("No movie entries found.")
        return

    out = OUTPUT_DIR / f"{label}.xlsx"
    effective_sheet = sheet_name or label.capitalize()

    # Filter to new movies first, then only download images for those
    new_rows = filter_new(rows, out, sheet_name=effective_sheet)
    if not new_rows:
        print("\nNo new movies to add.")
        daily_summary(out)
        return

    if not args.no_images:
        print(f"\nDownloading images for {len(new_rows)} new movie(s) ...\n")
        download_images(new_rows, label=label, subdir=subdir)

    if not args.no_trailers:
        fetch_trailers(new_rows)

    new_rows = append_new(new_rows, out, sheet_name=effective_sheet)
    daily_summary(out)

    if new_rows:
        print(f"\n  New titles added today:")
        for r in new_rows:
            print(f"    - {r['movie']} ({r['year']}) [{r['lang']}]")


def main():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Movierulz scraper — home / featured / search",
    )
    parser.add_argument("--no-images", action="store_true", help="Skip image downloads")
    sub = parser.add_subparsers(dest="command", required=True)

    # home
    p_home = sub.add_parser("home", help="Scrape the site home page (latest movies)")
    p_home.add_argument("--url", default=DEFAULT_HOME_URL, help=f"Site base URL (default: {DEFAULT_HOME_URL})")
    p_home.add_argument("start", type=int, nargs="?", default=1, help="Start page (default: 1)")
    p_home.add_argument("end", type=int, nargs="?", default=None, help="End page (default: same as start)")
    p_home.add_argument("--no-images", action="store_true", dest="no_images", help="Skip image downloads")
    p_home.add_argument("--no-trailers", action="store_true", dest="no_trailers", help="Skip trailer URL fetch")
    p_home.set_defaults(func=cmd_home)

    # featured
    p_feat = sub.add_parser("featured", help="Scrape a featured/category listing page")
    p_feat.add_argument("--url", default=DEFAULT_FEATURED_URL, help=f"Category base URL (default: {DEFAULT_FEATURED_URL})")
    p_feat.add_argument("start", type=int, nargs="?", default=1, help="Start page (default: 1)")
    p_feat.add_argument("end", nargs="?", default=None, help="End page number, or 'all' to scrape every page")
    p_feat.add_argument("--no-images", action="store_true", dest="no_images", help="Skip image downloads")
    p_feat.add_argument("--no-trailers", action="store_true", dest="no_trailers", help="Skip trailer URL fetch")
    p_feat.set_defaults(func=cmd_featured)

    # bollywood
    p_boll = sub.add_parser("bollywood", help="Scrape Bollywood movies listing")
    p_boll.add_argument("start", type=int, nargs="?", default=1, help="Start page (default: 1)")
    p_boll.add_argument("end", nargs="?", default=None, help="End page number, or 'all' to scrape every page")
    p_boll.add_argument("--url", default=DEFAULT_BOLLYWOOD_BASE_URL, help=f"Base URL (default: {DEFAULT_BOLLYWOOD_BASE_URL})")
    p_boll.add_argument("--no-images", action="store_true", dest="no_images", help="Skip image downloads")
    p_boll.add_argument("--no-trailers", action="store_true", dest="no_trailers", help="Skip trailer URL fetch")
    p_boll.set_defaults(func=cmd_bollywood)

    # malayalam
    p_mal = sub.add_parser("malayalam", help="Scrape Malayalam movies listing")
    p_mal.add_argument("start", type=int, nargs="?", default=1, help="Start page (default: 1)")
    p_mal.add_argument("end", nargs="?", default=None, help="End page number, or 'all' to scrape every page")
    p_mal.add_argument("--url", default=DEFAULT_MALAYALAM_BASE_URL, help=f"Base URL with YYYY placeholder (default: {DEFAULT_MALAYALAM_BASE_URL})")
    p_mal.add_argument("--no-images", action="store_true", dest="no_images", help="Skip image downloads")
    p_mal.add_argument("--no-trailers", action="store_true", dest="no_trailers", help="Skip trailer URL fetch")
    p_mal.set_defaults(func=cmd_malayalam)

    # search
    p_search = sub.add_parser("search", help="Search movies by keyword")
    p_search.add_argument("url", help="Site base URL (e.g. https://site.com/)")
    p_search.add_argument("query", help="Search keyword (e.g. \"RRR\" or \"2026 Telugu\")")
    p_search.add_argument("--pages", type=int, default=1, help="Number of result pages to fetch (default: 1)")
    p_search.add_argument("--no-images", action="store_true", dest="no_images", help="Skip image downloads")
    p_search.add_argument("--no-trailers", action="store_true", dest="no_trailers", help="Skip trailer URL fetch")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()

    # Normalize end page defaults
    if args.command == "featured":
        if args.end is None:
            args.end = args.start
        elif str(args.end).lower() == "all":
            args.end = featured.ALL_PAGES
        else:
            args.end = int(args.end)
            if args.end < args.start:
                print(f"Error: end page ({args.end}) must be >= start page ({args.start})")
                sys.exit(1)

    if args.command == "home":
        if args.end is None:
            args.end = args.start
        if args.end < args.start:
            print(f"Error: end page ({args.end}) must be >= start page ({args.start})")
            sys.exit(1)

    if args.command == "bollywood":
        if args.end is None:
            args.end = args.start
        elif str(args.end).lower() == "all":
            args.end = bollywood.ALL_PAGES
        else:
            args.end = int(args.end)
            if args.end < args.start:
                print(f"Error: end page ({args.end}) must be >= start page ({args.start})")
                sys.exit(1)

    if args.command == "malayalam":
        if args.end is None:
            args.end = args.start
        elif str(args.end).lower() == "all":
            args.end = malayalam.ALL_PAGES
        else:
            args.end = int(args.end)
            if args.end < args.start:
                print(f"Error: end page ({args.end}) must be >= start page ({args.start})")
                sys.exit(1)

    args.func(args)



if __name__ == "__main__":
    main()
