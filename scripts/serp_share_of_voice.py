#!/usr/bin/env python3
"""Compute a simple share-of-voice (SoV) report from SERP snapshots.

Reads:
- research/serp_tracking/<date>/raw/serp__*.json

Writes:
- research/serp_tracking/<date>/share_of_voice.json
- research/serp_tracking/<date>/SUMMARY.md

SoV scoring (simple + stable): score += 1 / rank_group for each organic result.
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone


def load_serp_items(path: Path):
    data = json.loads(path.read_text(encoding='utf-8'))
    return data.get('items', [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', required=True)
    ap.add_argument('--base', default='research/serp_tracking')
    ap.add_argument('--top', type=int, default=20)
    args = ap.parse_args()

    outdir = Path(args.base) / args.date
    rawdir = outdir / 'raw'
    files = sorted(rawdir.glob('serp__*.json'))

    domain_score = defaultdict(float)
    domain_counts = defaultdict(int)
    keywords = 0

    for f in files:
        items = load_serp_items(f)
        keywords += 1
        for it in items:
            if it.get('type') != 'organic':
                continue
            dom = (it.get('domain') or '').lower().strip()
            rank = it.get('rank_group')
            if not dom or not rank:
                continue
            domain_score[dom] += 1.0 / float(rank)
            domain_counts[dom] += 1

    ranked = sorted(domain_score.items(), key=lambda x: x[1], reverse=True)
    report = {
        'date': args.date,
        'generatedAtUtc': datetime.now(timezone.utc).isoformat(),
        'keywordsAnalyzed': keywords,
        'scoring': 'sum(1/rank_group) across organic results',
        'domains': [
            {
                'domain': dom,
                'score': round(score, 6),
                'organicResultCount': domain_counts[dom],
            }
            for dom, score in ranked
        ],
    }

    (outdir / 'share_of_voice.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

    top = ranked[: args.top]
    lines = [
        f"# Share of voice (SG Google) — {args.date}",
        "",
        f"Keywords analyzed: **{keywords}**",
        "Scoring: **sum(1/rank_group)** across organic results",
        "",
        "## Top domains",
        "",
    ]
    for i, (dom, score) in enumerate(top, start=1):
        lines.append(f"{i}. **{dom}** — score {score:.3f} (organic results: {domain_counts[dom]})")

    (outdir / 'SUMMARY.md').write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(f"Wrote {outdir/'SUMMARY.md'}")


if __name__ == '__main__':
    main()
