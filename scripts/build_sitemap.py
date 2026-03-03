#!/usr/bin/env python3
"""Generate docs/sitemap.xml including paper pages."""

from pathlib import Path

BASE = "https://jukebox7398.github.io/sg-primary-papers"


def main():
    urls = [
        f"{BASE}/",
        f"{BASE}/browse.html",
        f"{BASE}/about.html",
    ]

    papers_dir = Path('docs/papers')
    if papers_dir.exists():
        for p in sorted(papers_dir.glob('*.html')):
            urls.append(f"{BASE}/papers/{p.name}")

    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        out.append(f"  <url><loc>{u}</loc></url>")
    out.append('</urlset>')

    Path('docs/sitemap.xml').write_text('\n'.join(out) + '\n')
    print(f"Wrote docs/sitemap.xml with {len(urls)} URLs")


if __name__ == '__main__':
    main()
