#!/usr/bin/env python3
"""Apply manual top picks list to datasets.

Edit: docs/data/top_picks.json
Run:
  python3 scripts/apply_top_picks.py
  python3 scripts/build_paper_pages.py
"""

import json
from pathlib import Path

TOP = set(json.loads(Path('docs/data/top_picks.json').read_text()))

FILES = [
  Path('docs/data/papers.p1.json'),
  Path('docs/data/papers.p2.json'),
]


def main():
  total = 0
  marked = 0
  for f in FILES:
    items = json.loads(f.read_text())
    for it in items:
      total += 1
      it['topPick'] = it.get('id') in TOP
      if it['topPick']:
        marked += 1
    f.write_text(json.dumps(items, indent=2, ensure_ascii=False))
  print('top picks marked', marked, 'out of', total)


if __name__ == '__main__':
  main()
