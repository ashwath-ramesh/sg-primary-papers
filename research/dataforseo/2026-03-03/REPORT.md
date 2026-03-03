# DataForSEO competitor / market-share analysis (SG Primary papers)

Date: **2026-03-03** (UTC)

This run uses the **DataForSEO MCP server** (Google, location: Singapore, language: English) to answer the key “how do we steal SEO traffic from competitors?” questions and to create a baseline that can be repeated periodically and compared over time.

> Note on “secure storage”:
> - These exports are **raw datasets** (JSON) intended for git history + diffs.
> - **Do not commit secrets** (API creds, tokens). None are included in these outputs, but keep the repo private if the data is sensitive.
> - If repo size becomes an issue, move `raw/*.json` to Git LFS or store encrypted artifacts elsewhere and commit only derived summaries.

---

## What we pulled (datasets)

All datasets live under:

- `research/dataforseo/2026-03-03/raw/` (raw JSON)
- `research/dataforseo/2026-03-03/derived/` (TSV summaries)

### A) Competitor organic keyword footprints (baseline dataset)
For each domain below we exported **up to 1000 ranked keywords** (include_subdomains=true).

Domains:
- sgtestpaper.com
- sgexam.com
- seriousaboutschool.com
- testpapersfree.com
- freetestpaper.com
- kiasuparents.com
- smiletutor.sg
- familytutor.sg

Files:
- `raw/ranked_keywords__*.json`
- `derived/ranked_keywords__*.top200_by_search_volume.tsv`

### B) Competitor discovery (domain-to-domain)
A “competitor domains” export (seeded from sgtestpaper.com as a baseline reference point).

File:
- `raw/competitors_domain__sgtestpaper_com.json`

### C) SERP snapshots for the exact queries in COMPETITOR_LANDSCAPE_SERPAPI.md
Files:
- `raw/serp__*.json`

Queries pulled (depth=50):
- singapore primary 1 test papers free download
- singapore primary 2 test papers free download
- P1 exam papers singapore PDF
- P2 exam papers singapore PDF
- "free test papers" singapore primary
- kiasu parents exam papers primary
- buy primary school exam papers singapore

### D) Keyword expansion (idea generation)
Files:
- `raw/keyword_ideas__*.json`

Seeds:
- primary test papers
- primary exam papers
- past year papers
- P1 maths exam papers
- P6 science prelim papers

---

## Most important questions (and what these datasets answer)

Below are the questions we care about, mapped to the datasets we pulled and what you should look at.

### 1) “What keywords (and pages) drive competitor traffic in SG?”
**Answer source:** `raw/ranked_keywords__*.json` + `derived/*.tsv`

**How to use it:**
- For each competitor, sort by search volume and look at:
  - the **keyword themes** (P-level, subject, year)
  - the **ranking URL templates** (hub pages vs deep PDF vs category pages)

**Baseline observation (cross-competitor overlap):**
A lot of shared demand is extremely literal and “free-download”-driven. In the top-10 rankings across these 8 domains, the highest-overlap keyword themes include:
- “free test papers / free exam papers” variants
- subject + level combos (P1 maths, P2 math, P3 english, P6 science…)

### 2) “Which keywords are the easiest wins?”
**Answer source:** `raw/serp__*.json` + ranked keywords

**How to use it:**
- For target keywords, check who ranks top 10 and **what kind** of pages win:
  - thin category pages
  - tuition lead-gen pages
  - forum/UGC threads
  - direct PDF URLs

**Win condition:**
- SERPs where top results are weak (thin pages, low topical authority, messy UX) → build a better structured hub + clean indexable pages.

### 3) “What are we missing entirely (content gaps)?”
**Answer source:** keyword ideas + competitor ranked keywords

**How to use it:**
- Take `keyword_ideas__*.json`, cluster into intents:
  - free downloads
  - answer keys
  - topical worksheets vs exam papers
  - revision schedules / how-to-use papers
  - print bundles
- Cross-check which competitor domains appear in SERPs for each cluster.

### 4) “What SERP features dominate and where do forums/UGC win?”
**Answer source:** `raw/serp__*.json`

**How to use it:**
- Extract “People Also Ask” / related blocks (where present) and treat them as **content brief inputs**.
- Identify when UGC outranks library sites → create pages that answer those questions plainly and comprehensively.

### 5) “Which competitors have breadth vs depth (and where to attack)?”
**Answer source:** ranked keywords per domain

**How to use it:**
- Breadth: count unique keywords (and clusters) the domain ranks for.
- Depth: how often they rank in top 3 / top 10 for those terms.

### 6) “How do we track share-of-voice over time?”
**Answer source:** SERP snapshots (repeatable)

**How to use it:**
- Lock a tracking set of ~200–500 keywords (clustered) and run the same SERP pulls weekly/monthly.
- Compute share-of-voice = weighted positions across tracked keywords.

---

## Quick “what’s hot” signal from this run (cross-competitor overlap)

From the ranked-keywords exports, the most repeated top-10 keyword themes across competitors include:
- free test papers / free exam papers (multiple variants)
- “singapore free test paper” variants
- level+subject combos (P1 math, P2 math, P3 english, P6 science)
- “top schools exam papers”

This tells us:
1) Demand is strongly template-able (level × subject × year × free/paid intent).
2) Winning likely requires **scaled page generation** + **tight internal linking** + **excellent UX** for downloads.

---

## Next steps (recommended for the *next* periodic run)

1) Add your own domain as a first-class target (ranked keywords + competitors-domain).
2) Expand SERP tracking queries from 7 → 200+ (clustered list).
3) Add DataForSEO On-Page parsing/lighthouse runs for the top 3 URLs per SERP cluster.
4) Produce a single comparison summary file per run:
   - top gained/lost keywords by competitor
   - new entrants in top 10
   - SERP feature shifts

---

## Reproducibility

This run was generated via mcporter calls against the `dataforseo` MCP server.

If you want, I can:
- add a `run_dataforseo_competitor_scan.sh` script into the repo,
- and a `COMPARE.md` template so each new date folder includes the same sections for easy diffs.
