#!/usr/bin/env python3
"""Ingest SGExam subject listing pages into our papers datasets.

Example:
  python3 scripts/ingest_sgexam_subject.py \
    --url https://sgexam.com/primary-4-english/ \
    --level P4 --subject English --out docs/data/papers.p4.json

Notes:
- This is a best-effort parser based on SGExam URL slugs.
- We only store SGExam subject URLs (link-out only).
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import urllib.request


SUBJECT_MAP = {
    "math": "Maths",
    "maths": "Maths",
    "mathematics": "Maths",
    "english": "English",
    "science": "Science",
    "chinese": "Chinese",
}

# Small, high-impact normalizations for school slugs we already use elsewhere.
SCHOOL_SLUG_FIXES = {
    "acs-primary": "ACS-P",
    "acs-p": "ACS-P",
    "acsp": "ACS-P",
    "scgs": "SCGS",
    "mgs": "MGS",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "sg-primary-papers-ingest/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def title_case_words(s: str) -> str:
    parts = [p for p in re.split(r"\s+", s.strip()) if p]
    out = []
    for p in parts:
        low = p.lower()
        if low in ("wa", "sa", "ca"):
            out.append(low.upper())
        else:
            out.append(p[:1].upper() + p[1:])
    return " ".join(out)


def parse_subject_url(url: str) -> dict | None:
    # Example:
    # https://sgexam.com/subject/english/2025-p4-english-weighted-assessment-2-acs-primary-pdf/
    m = re.match(r"^https://sgexam\.com/subject/(?P<subj>[^/]+)/(?P<slug>[^/]+)/?$", url)
    if not m:
        return None

    subj_slug = m.group("subj").lower().strip()
    subj = SUBJECT_MAP.get(subj_slug, subj_slug.title())

    slug = m.group("slug").strip().strip("/")
    slug = re.sub(r"-pdf$", "", slug)

    # Extract year
    m2 = re.match(r"^(?P<year>\d{4})-(?P<rest>.+)$", slug)
    if not m2:
        return None
    year = int(m2.group("year"))
    rest = m2.group("rest")

    # Remove leading level+subject repetition (e.g. p4-english-...)
    rest = re.sub(r"^p\d-", "", rest)
    rest = re.sub(r"^(maths|math|english|science|chinese)-", "", rest, flags=re.I)

    # Split remaining into assessment + school
    parts = [p for p in rest.split("-") if p]
    if len(parts) < 2:
        return None

    # Special-case very short slugs like: ca1-acsj, sa2-mgs, ba3-acs
    # In these cases assessment is the first token, and school is the remainder.
    short_assess_re = re.compile(r"^(wa|sa|ca|ba|ta)\d+$", re.I)
    if len(parts) in (2, 3) and short_assess_re.match(parts[0]):
        assess_t = [parts[0]]
        school_t = parts[1:]
    else:
        # Heuristic: school is last 2-4 tokens, assessment is the rest.
        # We'll try from 2..5 tokens and pick the split that yields an assessment containing a known marker.
        markers = {"wa", "sa", "ca", "ba", "ta", "test", "quiz", "review", "exam", "assessment", "term", "weighted", "semestral", "end", "year", "practice", "prelim"}

        def score(assess_tokens: list[str]) -> int:
            return sum(1 for t in assess_tokens if t.lower() in markers or short_assess_re.match(t))

        best = None
        for school_len in (2, 3, 4, 5):
            if len(parts) <= school_len:
                continue
            a_t = parts[:-school_len]
            s_t = parts[-school_len:]
            sc = score(a_t)
            if best is None or sc > best[0]:
                best = (sc, a_t, s_t)

        if not best:
            assess_t = parts[:-2]
            school_t = parts[-2:]
        else:
            _, assess_t, school_t = best


    assessment_slug = "-".join(assess_t).strip("-")
    school_slug = "-".join(school_t).strip("-")

    # Build assessment label
    assessment = title_case_words(assessment_slug.replace("-", " "))

    # Build school label
    school = SCHOOL_SLUG_FIXES.get(school_slug.lower())
    if not school:
        school = title_case_words(school_slug.replace("-", " "))

    return {
        "year": year,
        "subject": subj,
        "assessment": assessment,
        "school": school,
        "sourceUrl": url,
        "notes": "Source: sgexam.com (link-out only).",
        "hasAnswers": None,
        "verified": False,
        "lastChecked": "",
        "topPick": False,
    }


def extract_subject_urls(html: str) -> list[str]:
    urls = set(re.findall(r"https://sgexam\.com/subject/[^\"'\s>]+", html))
    # normalize trailing slash
    out = []
    for u in urls:
        if not u.endswith("/"):
            u += "/"
        out.append(u)
    return sorted(out)


def compute_id(level: str, subject: str, year: int, assessment: str, school: str) -> str:
    lvl = level.lower()
    subj = subject.lower().replace(" ", "-")
    assess = re.sub(r"[^a-z0-9]+", "-", assessment.lower()).strip("-")
    sch = re.sub(r"[^a-z0-9]+", "-", school.lower()).strip("-")
    return f"{lvl}-{subj}-{year}-{assess}-{sch}".replace("--", "-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="SGExam listing page (e.g. https://sgexam.com/primary-4-english/)")
    ap.add_argument("--level", required=True, help="Level label, e.g. P4")
    ap.add_argument("--subject", required=True, help="Subject label, e.g. English")
    ap.add_argument("--out", required=True, help="Output dataset JSON file")
    ap.add_argument("--merge", action="store_true", help="Merge into existing file (default true if exists)")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    html = fetch(args.url)
    urls = extract_subject_urls(html)

    items = []
    for u in urls:
        it = parse_subject_url(u)
        if not it:
            continue
        it["level"] = args.level
        it["subject"] = args.subject  # override with requested subject
        it["id"] = compute_id(args.level, args.subject, it["year"], it["assessment"], it["school"])
        items.append(it)

    # Merge/dedup
    existing = []
    if out_path.exists() and (args.merge or True):
        existing = json.loads(out_path.read_text())

    by_id = {e.get("id"): e for e in existing if e.get("id")}
    for it in items:
        by_id[it["id"]] = it

    merged = list(by_id.values())
    merged.sort(key=lambda x: (-int(x.get("year") or 0), x.get("subject", ""), x.get("assessment", ""), x.get("school", "")))

    out_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n")
    print(f"Fetched {len(urls)} subject URLs, parsed {len(items)} items. Wrote {len(merged)} rows to {out_path}")


if __name__ == "__main__":
    main()
