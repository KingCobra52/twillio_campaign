"""Resolve every internal link/resource in site/ the way GitHub Pages would,
with the site mounted at /twillio_campaign/."""
import os, re, sys
from urllib.parse import urljoin, urlsplit

ROOT = os.path.abspath("site")
BASE = "/twillio_campaign/"
ATTR = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.I)
ID = re.compile(r'\sid\s*=\s*"([^"]+)"', re.I)

pages = {}
for dirpath, _, names in os.walk(ROOT):
    for n in names:
        if n.endswith(".html"):
            p = os.path.join(dirpath, n)
            pages[p] = open(p, encoding="utf-8").read()

ids = {p: set(ID.findall(t)) for p, t in pages.items()}

def to_disk(url_path):
    """Map a served URL path to a file on disk, or None."""
    if not url_path.startswith(BASE):
        return None
    rel = url_path[len(BASE):]
    cand = os.path.join(ROOT, rel)
    if rel.endswith("/") or rel == "":
        cand = os.path.join(cand, "index.html")
    if os.path.isdir(cand):
        cand = os.path.join(cand, "index.html")
    return cand if os.path.isfile(cand) else None

problems = []
checked = 0
for page, text in sorted(pages.items()):
    rel = os.path.relpath(page, ROOT)
    served = BASE + rel.replace(os.sep, "/")
    for url in ATTR.findall(text):
        if url.startswith(("mailto:", "http://", "https://", "data:", "#")):
            if url.startswith("#"):
                checked += 1
                if url[1:] not in ids[page]:
                    problems.append(f"{rel}: anchor {url} has no matching id")
            continue
        checked += 1
        target = urljoin(served, url)
        path, _, frag = target.partition("#")
        disk = to_disk(path)
        if disk is None:
            problems.append(f"{rel}: {url!r} -> {path} NOT FOUND")
        elif frag and disk in ids and frag not in ids[disk]:
            problems.append(f"{rel}: {url!r} fragment #{frag} missing in target")

print(f"checked {checked} links across {len(pages)} pages")
if problems:
    print("\nPROBLEMS:")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print("all internal links and anchors resolve")
