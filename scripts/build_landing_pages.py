#!/usr/bin/env python3
"""Generate lean landing pages for SEO/shareability.

Creates:
- docs/p1/<subject>/<year>/index.html
- docs/p2/<subject>/<year>/index.html

These pages are intentionally minimal and link to Browse with filters applied.
"""

import json
from pathlib import Path

DATA = {
  'p1': Path('docs/data/papers.p1.json'),
  'p2': Path('docs/data/papers.p2.json'),
  'p3': Path('docs/data/papers.p3.json'),
  'p4': Path('docs/data/papers.p4.json'),
  'p5': Path('docs/data/papers.p5.json'),
}

# Generate for whatever subjects exist in each dataset (e.g. Science for P4/P5).


def write_page(level, subject, year):
    base = Path(f'docs/{level}/{subject.lower()}/{year}')
    base.mkdir(parents=True, exist_ok=True)
    (base / 'index.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Primary {level[1:]} {subject} {year} Papers — SG Primary Papers</title>
  <meta name="description" content="Browse Primary {level[1:]} {subject} papers for {year} by assessment type and school." />
  <link rel="stylesheet" href="../../../styles.css" />
  <script defer src="https://analytics.millisecondlabs.com/script.js" data-website-id="620b5939-4f56-49f3-9eac-0141f805d3a5"></script>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand"><a class="a" href="../../../index.html" style="font-weight:900">SG Primary Papers</a> <span class="badge">Primary {level[1:]}</span></div>
      <div class="nav">
        <a href="../../../browse.html?level={level}&subject={subject}&year={year}">Browse</a>
        <a href="../../../collections.html">Collections</a>
        <a href="../../../about.html">About</a>
      </div>
    </div>

    <div class="card">
      <h2 style="margin:0 0 8px">Primary {level[1:]} {subject} — {year}</h2>
      <div class="row" style="margin-top:12px">
        <a class="btn" href="../../../browse.html?level={level}&subject={subject}&year={year}">Browse {year}</a>
        <a class="btn secondary" href="../../../browse.html?level={level}&subject={subject}&year={year}&type=Test">Tests</a>
        <a class="btn secondary" href="../../../browse.html?level={level}&subject={subject}&year={year}&type=Quiz">Quizzes</a>
        <a class="btn secondary" href="../../../browse.html?level={level}&subject={subject}&year={year}&type=SA">SA</a>
      </div>
      <div class="footer">Minimal page. Use Browse for filters.</div>
    </div>
  </div>
</body>
</html>
''')


def main():
    count = 0
    for level, path in DATA.items():
        items = json.loads(path.read_text())
        subjects = sorted({i.get('subject') for i in items if i.get('subject')})
        for subject in subjects:
            years = sorted({int(i['year']) for i in items if i.get('subject') == subject and i.get('year')}, reverse=True)
            for y in years:
                write_page(level, subject, y)
                count += 1
    print('generated', count, 'year landing pages')


if __name__ == '__main__':
    main()
