"""
Checks that every .i18n element with data-lang="de" is paired with a
data-lang="en" sibling, and vice versa, in the given HTML files.
This is a count + structural sanity check (not full DOM diffing) — good
enough to catch a forgotten translation when adding new content.

Usage:
  python3 check_i18n.py                    # all *.html in repo (except none by default)
  python3 check_i18n.py index.html ...   # explicit files
"""
import glob
import re
import sys

PATTERN = re.compile(
    r'<([a-zA-Z0-9]+)([^>]*\bclass="[^"]*\bi18n\b[^"]*"[^>]*\bdata-lang="(de|en)"[^>]*)>',
)

DEFAULT_GLOBS = [
    "index.html",
    "404.html",
    "businessplan/index.html",
    "galerie/index.html",
    "impressum/index.html",
    "datenschutz/index.html",
    "pakete/*/index.html",
]


def discover_html_files():
    paths = []
    for pattern in DEFAULT_GLOBS:
        paths.extend(glob.glob(pattern))
    return sorted(set(paths))


def check(path):
    html = open(path, encoding="utf-8").read()
    matches = PATTERN.findall(html)
    counts = {"de": 0, "en": 0}
    for tag, attrs, lang in matches:
        counts[lang] += 1
    ok = counts["de"] == counts["en"]
    status = "OK" if ok else "MISMATCH"
    print(f"{path}: de={counts['de']} en={counts['en']}  [{status}]")
    return ok


if __name__ == "__main__":
    paths = sys.argv[1:] or discover_html_files()
    if not paths:
        print("No HTML files found.", file=sys.stderr)
        sys.exit(1)
    all_ok = True
    for p in paths:
        if not check(p):
            all_ok = False
    sys.exit(0 if all_ok else 1)
