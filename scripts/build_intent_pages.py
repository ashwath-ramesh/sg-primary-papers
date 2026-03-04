#!/usr/bin/env python3
"""Generate SEO-friendly intent landing pages.

Creates pages like:
- docs/p1/english/free-test-papers/index.html
- docs/p2/maths/past-year-papers/index.html

These pages are lightweight and funnel into browse.html with filters.
They only generate for (level, subject) combos that exist in the dataset.

Run:
  python3 scripts/build_intent_pages.py
"""

import json
from pathlib import Path

DATA = {
    'p1': Path('docs/data/papers.p1.json'),
    'p2': Path('docs/data/papers.p2.json'),
    'p3': Path('docs/data/papers.p3.json'),
}

# intent_key -> (title_template, description_template, browse_params)
INTENTS = {
    'past-year-papers': (
        'Singapore Primary {n} {subject} Past Year Papers (Free Download) — SG Primary Papers',
        'Browse Singapore Primary {n} {subject} past year papers. Filter by year, assessment type and school. Free downloads where available.',
        lambda level, subject: f'level={level}&subject={subject}',
    ),
    'free-test-papers': (
        'Singapore Primary {n} {subject} Test Papers (Free Download) — SG Primary Papers',
        'Browse Singapore Primary {n} {subject} test papers. Free downloads where available. Filter by year and school.',
        lambda level, subject: f'level={level}&subject={subject}&type=Test',
    ),
    'free-quiz-papers': (
        'Singapore Primary {n} {subject} Quiz Papers (Free Download) — SG Primary Papers',
        'Browse Singapore Primary {n} {subject} quiz papers. Free downloads where available. Filter by year and school.',
        lambda level, subject: f'level={level}&subject={subject}&type=Quiz',
    ),
    'latest-papers': (
        'Singapore Primary {n} {subject} Papers (Latest Available) — SG Primary Papers',
        'Browse the latest available Singapore Primary {n} {subject} papers. Filter by assessment type and school.',
        lambda level, subject: f'level={level}&subject={subject}&year=latest',
    ),
}


def rel_styles(depth: int) -> str:
    return '../' * depth + 'styles.css'


def rel_root(depth: int) -> str:
    return '../' * depth + 'index.html'


def write_page(level: str, subject: str, intent_key: str, years):
    # docs/p1/english/<intent>/index.html
    base = Path('docs') / level / subject.lower() / intent_key
    base.mkdir(parents=True, exist_ok=True)

    n = level[1:]
    title_t, desc_t, qp_fn = INTENTS[intent_key]
    title = title_t.format(n=n, subject=subject)
    desc = desc_t.format(n=n, subject=subject)

    # depth from this file to docs/: docs/<level>/<subject>/<intent>/index.html => 3
    css = rel_styles(3)
    home = rel_root(3)

    # simple “latest year” value for on-page copy
    latest = max(years) if years else ''

    browse_qs = qp_fn(level, subject)

    (base / 'index.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="stylesheet" href="{css}" />
  <script defer src="https://analytics.millisecondlabs.com/script.js" data-website-id="620b5939-4f56-49f3-9eac-0141f805d3a5"></script>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand"><a class="a" href="{home}" style="font-weight:900">SG Primary Papers</a> <span class="badge">Primary {n}</span></div>
      <div class="nav">
        <a href="../../../browse.html?{browse_qs}">Browse</a>
        <a href="../../../collections.html">Collections</a>
        <a href="../../../about.html">About</a>
      </div>
    </div>

    <div class="card">
      <h2 style="margin:0 0 8px">{subject} • Primary {n}</h2>
      <div class="small">Available years: {', '.join(map(str, sorted(years, reverse=True)[:8]))}{'…' if len(years) > 8 else ''}</div>

      <div class="row" style="margin-top:12px">
        <a class="btn" href="../../../browse.html?{browse_qs}">Open filtered list</a>
        <a class="btn secondary" href="../../../browse.html?level={level}&subject={subject}">All {subject}</a>
        <a class="btn secondary" href="../../../browse.html?level={level}&subject={subject}&year={latest}">Year {latest}</a>
      </div>

      <div class="footer">Tip: use Browse to filter by year, school, and type.</div>
    </div>
  </div>
</body>
</html>
''')


def main():
    generated = 0
    for level, path in DATA.items():
        items = json.loads(path.read_text())
        subjects = sorted({i['subject'] for i in items if i.get('subject')})
        for subject in subjects:
            years = sorted({int(i['year']) for i in items if i.get('subject') == subject and i.get('year')})
            if not years:
                continue
            for intent_key in INTENTS.keys():
                write_page(level, subject, intent_key, years)
                generated += 1
    print('generated', generated, 'intent pages')


if __name__ == '__main__':
    main()
