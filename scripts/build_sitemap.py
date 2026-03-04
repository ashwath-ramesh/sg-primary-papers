#!/usr/bin/env python3
"""Generate docs/sitemap.xml including paper pages."""

from pathlib import Path

# Canonical base URL for sitemap/robots.
# For GitHub Pages project sites this includes the repo name.
BASE = "https://sgprimarypapers.millisecondlabs.com"


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
    for p in sorted(Path('docs/p3').glob('*.html')):
        urls.append(f"{BASE}/p3/{p.name}")
    for p in sorted(Path('docs/p4').glob('*.html')):
        urls.append(f"{BASE}/p4/{p.name}")
    for p in sorted(Path('docs/p5').glob('*.html')):
        urls.append(f"{BASE}/p5/{p.name}")

    # Year landing pages (docs/p1/<subject>/<year>/index.html, etc.)
    for p in sorted(Path('docs/p1').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")
    for p in sorted(Path('docs/p2').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")
    for p in sorted(Path('docs/p3').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")
    for p in sorted(Path('docs/p4').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")
    for p in sorted(Path('docs/p5').glob('**/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")

    # Any top-level directory landing page (e.g. free-test-papers-..., past-year-..., collections/)
    for p in sorted(Path('docs').glob('*/index.html')):
        rel = p.relative_to('docs')
        urls.append(f"{BASE}/{rel.as_posix()}")

    # FAQ / guides (may be nested)
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
