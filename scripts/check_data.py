#!/usr/bin/env python3
"""Sanity checks for datasets.

Run:
  python3 scripts/check_data.py
"""

import json
from pathlib import Path
from collections import Counter

FILES = [
    Path('docs/data/papers.p1.json'),
    Path('docs/data/papers.p2.json'),
]

REQUIRED = ['id', 'level', 'subject', 'year', 'assessment', 'school', 'sourceUrl']


def main():
    all_items = []
    for f in FILES:
        if not f.exists():
            continue
        items = json.loads(f.read_text())
        print(f"{f}: {len(items)}")
        all_items.extend(items)

        # missing fields
        for r in REQUIRED:
            missing = [i for i in items if not i.get(r)]
            if missing:
                print(f"  WARN missing {r}: {len(missing)}")

        # duplicate ids
        ids = [i.get('id') for i in items]
        dup = [k for k, v in Counter(ids).items() if v > 1]
        if dup:
            print(f"  WARN duplicate ids: {len(dup)}")

    print("\nOverall")
    print(" total:", len(all_items))
    print(" levels:", Counter([i.get('level') for i in all_items]).most_common())
    print(" subjects:", Counter([i.get('subject') for i in all_items]).most_common())
    print(" years (top):", Counter([i.get('year') for i in all_items]).most_common(10))


if __name__ == '__main__':
    main()
