# Research notes: sgexam.com vs sgtestpaper.com

## What they are (high level)

### sgexam.com
- Focus: **Primary school only**.
- Navigation pattern: **Level → Subject page** (e.g. `primary-6-english`) which is basically a **year-grouped link list**.
- Each PDF appears to be its own page under `/subject/<subject>/<slug>/` with a direct PDF link.
- Extra “side quests” on homepage (grammar practice site, math game) which dilutes the core value prop.

### sgtestpaper.com
- Focus: **Primary + Secondary + JC**.
- Navigation pattern: **Level pages (P6/P5/...) → Year/Subject pages** (e.g. `/primary/subject2025/y25p6english.html`).
- Heavy emphasis on:
  - “1-click download” packages (zip / bundles)
  - Paid products (softcopy/hardcopy) via `etestpaper.com` shop
  - Extras: eMCQ, worked solutions, worksheet updates, blog articles
- Content is dense/link-heavy; some pages contain obvious SEO filler text.

## Information architecture (IA) observations

Common dimensions across both sites:
- **Level**: P1–P6 (primary is the core), plus secondary/JC on sgtestpaper.
- **Subject**: English, Maths, Science, Chinese, Higher Chinese.
- **Year**: typically 2018–2025+.
- **Assessment type**:
  - Prelim / EOY (SA2)
  - WA1 / WA2 / WA3
  - Other: term assessments, class tests, bite-sized assessments, timed practice.
- **School** (big on sgexam lists: ACSJ, Nan Hua, Rosyth, etc.)

Pain points we can beat:
- Link dumps instead of **search + filters**.
- No clear “what am I downloading?” metadata (pages, marks breakdown, answer key present?).
- Weak trust signals (source provenance, update history, clear licensing/copyright stance).
- Mobile UX is functional but not "polished".

## Monetisation patterns

### sgexam.com
- Moderately ad/upsell driven.
- Uses internal value-add properties (grammar site, math game) to retain users.

### sgtestpaper.com
- Strong funnel to paid:
  - bundles
  - softcopy/hardcopy
  - discount codes
- Free individual downloads to drive traffic, upsell for convenience.

## Feature ideas for a more polished site

Core UX improvements:
- **Faceted search**: Level → Subject → Year → Assessment → School.
- Paper detail page with structured metadata:
  - school, year, subject, assessment, paper type, answer key, file size
  - tags + related papers
- Fast, predictable URLs.
- “Collections” (e.g. *Best Prelim Papers for P6 Maths 2025*).

Value-add (optional, depending on legal/content sourcing):
- Interactive practice derived from *original* questions you create (not copied).
- Progress tracking / bookmarking.
- Teacher/parent guides.

## Notes on legality (important)
Both sites distribute school exam papers. For the new site, we should decide early:
- Are we **hosting files** or only **indexing and linking**?
- Do we have permissions/licenses for any hosted content?

My recommendation: start with **index + metadata + links**, and add **original** practice content to avoid copyright landmines.
