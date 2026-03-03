#!/usr/bin/env python3
"""Run periodic SERP pulls for our tracked keyword set via DataForSEO MCP (mcporter).

Usage:
  python3 scripts/run_serp_tracking.py --date 2026-03-03 --limit 20

Defaults:
- Input: research/seo_tracking/keywords.csv
- Output: research/serp_tracking/<date>/raw/serp__<slug>.json

This script is intentionally resumable: it skips outputs that already exist.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone

DEFAULT_KEYWORDS = Path('research/seo_tracking/keywords.csv')


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9]+', '_', s)
    s = re.sub(r'^_+|_+$', '', s)
    return s[:120] or 'query'


def run_mcporter_serp(keyword: str) -> dict:
    args = {
        'search_engine': 'google',
        'location_name': 'Singapore',
        'language_code': 'en',
        'keyword': keyword,
        'depth': 50,
        'device': 'desktop',
    }
    cmd = [
        'mcporter', 'call', 'dataforseo.serp_organic_live_advanced',
        '--args', json.dumps(args),
        '--output', 'json',
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"mcporter failed: {res.stderr.strip()}")
    return json.loads(res.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    ap.add_argument('--keywords', default=str(DEFAULT_KEYWORDS))
    ap.add_argument('--limit', type=int, default=0, help='0 = no limit')
    ap.add_argument('--sleep', type=float, default=0.6, help='seconds between calls')
    args = ap.parse_args()

    keywords_path = Path(args.keywords)
    outdir = Path('research/serp_tracking') / args.date
    rawdir = outdir / 'raw'
    rawdir.mkdir(parents=True, exist_ok=True)

    # Load keywords
    kws = []
    with keywords_path.open(newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            kw = (row.get('keyword') or '').strip()
            if kw:
                kws.append(row)

    if args.limit and args.limit > 0:
        kws = kws[: args.limit]

    manifest = {
        'date': args.date,
        'generatedAtUtc': datetime.now(timezone.utc).isoformat(),
        'input': str(keywords_path),
        'countPlanned': len(kws),
        'params': {
            'search_engine': 'google',
            'location_name': 'Singapore',
            'language_code': 'en',
            'depth': 50,
            'device': 'desktop',
        },
    }
    (outdir / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

    done = 0
    skipped = 0
    for row in kws:
        kw = row['keyword']
        slug = slugify(kw)
        out = rawdir / f'serp__{slug}.json'
        if out.exists():
            skipped += 1
            continue
        try:
            data = run_mcporter_serp(kw)
            out.write_text(json.dumps(data, indent=2), encoding='utf-8')
            done += 1
        except Exception as e:
            err = {'keyword': kw, 'error': str(e)}
            (rawdir / f'serp__{slug}.error.json').write_text(json.dumps(err, indent=2), encoding='utf-8')
        time.sleep(args.sleep)

    print(f"SERP pulls complete. wrote={done} skipped={skipped} out={outdir}")


if __name__ == '__main__':
    main()
