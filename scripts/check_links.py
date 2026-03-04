#!/usr/bin/env python3
"""Lightweight link checker to support 'verified' + 'lastChecked' fields.

Defaults to a small sample to stay polite.

Usage:
  python3 scripts/check_links.py --limit 100

Notes:
- This does NOT download PDFs; it requests the HTML page URL we link to.
- Keep concurrency low.
"""

import argparse
import json
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

DATA_FILES = [
    Path('docs/data/papers.p1.json'),
    Path('docs/data/papers.p2.json'),
    Path('docs/data/papers.p3.json'),
    Path('docs/data/papers.p4.json'),
]

UA = {
    'User-Agent': 'SGPrimaryPapersBot/0.1 (link-check; contact via GitHub issues)'
}


def check(url: str, timeout=15) -> bool:
    try:
        r = requests.get(url, headers=UA, timeout=timeout)
        return 200 <= r.status_code < 400
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=100)
    ap.add_argument('--sleep', type=float, default=0.25)
    args = ap.parse_args()

    now = time.strftime('%Y-%m-%d', time.gmtime())

    remaining = args.limit
    for path in DATA_FILES:
        items = json.loads(path.read_text())

        changed = False
        for it in items:
            if remaining <= 0:
                break
            if it.get('verified') and it.get('lastChecked') == now:
                continue

            ok = check(it['sourceUrl'])
            it['verified'] = bool(ok)
            it['lastChecked'] = now
            changed = True
            remaining -= 1
            time.sleep(args.sleep)

        if changed:
            path.write_text(json.dumps(items, indent=2, ensure_ascii=False))

    print('Checked', args.limit - remaining, 'links; date', now)


if __name__ == '__main__':
    main()
