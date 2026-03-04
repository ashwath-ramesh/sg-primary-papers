# Singapore Papers (Research)

This repo documents research/notes on existing Singapore primary school exam paper sites (e.g. sgexam.com, sgtestpaper.com) and a plan for building a more polished, user-friendly alternative.

## What this repo is (and is not)
- ✅ UX, IA, feature, and SEO research
- ✅ Product requirements + sitemap + content model
- ✅ A GitHub Pages site for the documentation + prototype UI
- ❌ Not a mirror of copyrighted exam papers

## Local preview
Run a simple local web server from the repo root:

```bash
python3 -m http.server 8000 --directory docs
```

Then open: http://localhost:8000

The site content is served from `./docs`, and the typical entry point is `docs/index.html`
(available at `http://localhost:8000/index.html`).
