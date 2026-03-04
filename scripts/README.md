# Scripts

These scripts support the static build for GitHub Pages.

## Prereqs
- Python 3 (already available)

## Data files
- `docs/data/papers.p1.json`
- `docs/data/papers.p2.json`
- `docs/data/papers.p3.json`
- `docs/data/papers.p4.json`

## Build steps (typical)

### 1) Normalize datasets

```bash
python3 scripts/normalize_data.py
```

### 2) Generate shareable paper pages

```bash
python3 scripts/build_paper_pages.py
```

### 3) Generate sitemap.xml

```bash
python3 scripts/build_sitemap.py
```

### 4) Sanity-check datasets

```bash
python3 scripts/check_data.py
```

## Notes
- This repo is **link-out only** (we do not host PDFs).
- The site is served from `main:/docs` via GitHub Pages.
