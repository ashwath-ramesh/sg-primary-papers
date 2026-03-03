#!/usr/bin/env python3
"""Normalize dataset fields for consistent filtering/UX.

- standardize assessment labels (spacing/casing)
- add assessmentType (coarse grouping)
- normalize school names (light)

Run:
  python3 scripts/normalize_data.py
"""

import json
import re
from pathlib import Path

DATA_FILES = [
    Path('docs/data/papers.p1.json'),
    Path('docs/data/papers.p2.json'),
]


def norm_assessment(a: str) -> str:
    a = (a or '').strip()
    if not a:
        return a
    a = a.replace('_', '-')
    a = re.sub(r'\s+', ' ', a)
    low = a.lower()

    if low in ('quizes', 'quizzes', 'quiz'):
        return 'Quiz'

    m = re.fullmatch(r'(test)\s*([0-9]+)', low)
    if m:
        return f"Test {m.group(2)}"

    m = re.fullmatch(r'(quiz)\s*([0-9]+)', low)
    if m:
        return f"Quiz {m.group(2)}"

    if low in ('review', 'reviews'):
        return 'Review'

    if low == 'sa1':
        return 'SA1'

    return a[:1].upper() + a[1:]


def assessment_type(label: str) -> str:
    l = (label or '').strip().lower()
    if not l:
        return ''
    if l.startswith('sa') or 'semestral' in l or 'holistic' in l:
        return 'SA'
    if l.startswith('ca'):
        return 'CA'
    if l.startswith('wa'):
        return 'WA'
    if l.startswith('test'):
        return 'Test'
    if l.startswith('quiz'):
        return 'Quiz'
    if l.startswith('review') or 'revision' in l:
        return 'Review'
    return 'Other'


def norm_school(s: str) -> str:
    s = (s or '').strip()
    s = re.sub(r'\s+', ' ', s)
    repl = {'Scgs': 'SCGS', 'Acs': 'ACS', 'Mgs': 'MGS'}
    t = s.title()
    if t in repl:
        return repl[t]
    return s


def process(path: Path):
    items = json.loads(path.read_text())
    for it in items:
        it['assessment'] = norm_assessment(it.get('assessment', ''))
        it['assessmentType'] = assessment_type(it.get('assessment', ''))
        it['school'] = norm_school(it.get('school', ''))

    # stable sort
    items.sort(key=lambda x: (-int(x.get('year') or 0), x.get('subject', ''), x.get('assessment', ''), x.get('school', '')))
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    return len(items)


def main():
    total = 0
    for p in DATA_FILES:
        if p.exists():
            total += process(p)
    print(f"Normalized {total} rows across {len([p for p in DATA_FILES if p.exists()])} datasets")


if __name__ == '__main__':
    main()
