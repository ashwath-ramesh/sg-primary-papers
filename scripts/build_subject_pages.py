#!/usr/bin/env python3
"""Generate level/subject hub pages (e.g. docs/p4/english.html, docs/p5/science.html).

These are simple, indexable pages that funnel into Browse + intent pages.
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


def write_subject(level: str, subject: str, years):
    # docs/p4/english.html
    out = Path('docs') / level / f"{subject.lower()}.html"
    n = level[1:]
    years_sorted = sorted(years, reverse=True)
    years_str = ', '.join(map(str, years_sorted[:12])) + ('…' if len(years_sorted) > 12 else '')

    out.write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Primary {n} {subject} Papers (Free Download) — SG Primary Papers</title>
  <meta name="description" content="Browse Singapore Primary {n} {subject} papers. Filter by year, assessment type and school." />
  <link rel="stylesheet" href="../styles.css" />
  <script defer src="https://analytics.millisecondlabs.com/script.js" data-website-id="620b5939-4f56-49f3-9eac-0141f805d3a5"></script>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand"><a class="a" href="../index.html" style="font-weight:900">SG Primary Papers</a> <span class="badge">Primary {n}</span></div>
      <div class="nav">
        <a href="../browse.html">Browse</a>
        <a href="../collections.html">Collections</a>
        <a href="../start-here.html">Start here</a>
        <a href="../about.html">About</a>
      </div>
    </div>

    <div class="card">
      <h2 style="margin:0 0 8px">Primary {n} {subject} papers</h2>
      <div class="small">Years available: {years_str}</div>

      <div class="row" style="margin-top:12px">
        <a class="btn" href="../browse.html?level=P{n}&subject={subject}">Browse all</a>
        <a class="btn secondary" href="{subject.lower()}/past-year-papers/">Past year</a>
        <a class="btn secondary" href="{subject.lower()}/free-test-papers/">Tests</a>
        <a class="btn secondary" href="{subject.lower()}/free-quiz-papers/">Quizzes</a>
        <a class="btn secondary" href="{subject.lower()}/latest-papers/">Latest</a>
      </div>

      <div class="footer">We don’t host PDFs. We link to sources.</div>
    </div>
  </div>
</body>
</html>
''')


def main():
    generated = 0
    for level, path in DATA.items():
        items = json.loads(path.read_text())
        subjects = sorted({i.get('subject') for i in items if i.get('subject')})
        for subject in subjects:
            years = {int(i['year']) for i in items if i.get('subject') == subject and i.get('year')}
            if not years:
                continue
            write_subject(level, subject, years)
            generated += 1
    print(f"Generated {generated} subject pages")


if __name__ == '__main__':
    main()
