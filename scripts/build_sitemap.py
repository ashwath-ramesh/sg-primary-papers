#!/usr/bin/env python3
"""Generate docs/sitemap.xml including paper pages."""

from pathlib import Path

BASE = "https://jukebox7398.github.io/sg-primary-papers"


def main():
    urls = [
        f"{BASE}/",
        f"{BASE}/start-here.html",
        f"{BASE}/browse.html",
        f"{BASE}/collections.html",
        f"{BASE}/reliability.html",
        f"{BASE}/about.html",
    ]

    # Level/subject landing pages
    for p in sorted(Path('docs/p1').glob('*.html')):
        urls.append(f"{BASE}/p1/{p.name}")
    for p in sorted(Path('docs/p2').glob('*.html')):
        urls.append(f"{BASE}/p2/{p.name}")

    # Year landing pages (docs/p1/<subject>/<year>/index.html, etc.)
    for p in sorted(Path('docs/p1').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")
    for p in sorted(Path('docs/p2').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")

    # FAQ / guides
    for p in sorted(Path('docs/faq').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")

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
