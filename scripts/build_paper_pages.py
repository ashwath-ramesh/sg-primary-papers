#!/usr/bin/env python3
import json, html
from pathlib import Path

DATA_FILES = [
  ('docs/data/papers.p1.json', 'Primary 1'),
  ('docs/data/papers.p2.json', 'Primary 2'),
]

TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand"><a class="a" href="../index.html" style="font-weight:900">SG Primary Papers</a> <span class="badge">{badge}</span></div>
      <div class="nav">
        <a href="../browse.html">Browse</a>
        <a href="../about.html">About</a>
      </div>
    </div>

    <div class="card">
      <h2 style="margin:0 0 6px">{h2}</h2>
      <div class="small">{meta}</div>
      <div class="row" style="margin-top:12px">
        <a class="btn" href="{source}" rel="nofollow noopener" target="_blank">Go to source link</a>
        <a class="btn secondary" href="../browse.html">Back to browse</a>
      </div>
      <div class="footer">{notes}</div>
    </div>

    <div class="footer">We don’t host files. Links may change on source sites.</div>
  </div>
</body>
</html>
'''


def esc(s):
  return html.escape(str(s or ''))


def main():
  out_dir = Path('docs/papers')
  out_dir.mkdir(parents=True, exist_ok=True)

  total = 0
  for path, badge in DATA_FILES:
    papers = json.loads(Path(path).read_text())
    for p in papers:
      title = f"{p['level']} {p['subject']} {p['year']} — {p['school']}"
      desc = f"{p['level']} {p['subject']} {p['year']} ({p.get('assessment','')}) source link."
      meta = f"{p.get('assessment','')} • {p.get('school','')} • {p.get('year','')}"
      page = TEMPLATE.format(
        title=esc(title),
        desc=esc(desc),
        badge=esc(badge),
        h2=esc(f"{p['level']} {p['subject']} ({p['year']})"),
        meta=esc(meta),
        source=esc(p['sourceUrl']),
        notes=esc(p.get('notes',''))
      )
      (out_dir / f"{p['id']}.html").write_text(page)
      total += 1

  print(f"Generated {total} paper pages")


if __name__ == '__main__':
  main()
