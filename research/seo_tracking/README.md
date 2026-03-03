# SEO tracking keywords

This folder contains the tracked keyword set used for periodic SERP pulls and share-of-voice comparisons.

- `keywords.csv` is the canonical list.
- Keep it **stable**: only add/remove intentionally, because comparisons over time depend on it.

## How this list is constructed

We include a mix of:
1) **High-intent head terms** ("free test papers", "exam papers pdf", "past year papers")
2) **Level × subject** modifiers (P1/P2 × English/Maths/Chinese)
3) **Singapore modifiers** ("Singapore")
4) **Year modifiers** for recency intent (e.g. 2024/2025)

This is intentionally biased toward the queries that actually lead to downloads and therefore traffic.

## Update rules

- Add new clusters rather than random one-offs.
- Prefer stable wording parents actually type (plain English).
- When a query cluster proves valuable, expand it systematically (years, synonyms).
