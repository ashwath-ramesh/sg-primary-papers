# SG Primary Papers — Design Principles (SG parent aesthetic, 2026)

This document is the **single source of truth** for UI/UX decisions in SG Primary Papers.
If a change conflicts with these principles, the change should be rejected or revised.

## Product vibe
- **Calm, competent, modern.** No “tuition flyer” energy.
- **Trust-first.** Parents should feel this is safe, curated, and not spam.
- **Fast-first.** Speed is a feature.

## MVP scope assumption
- MVP is **link-out only** (we index metadata and point to sources).
- Start with **P1** and scale levels later.

---

## 1) Layout & spacing
- Use a **single centered container** with generous whitespace.
- Prefer **2-column layouts on desktop** and **single column on mobile**.
- Keep sections short; avoid long walls of links.

**Rules of thumb**
- Max content width: ~1040px.
- Card radius: ~16px.
- Spacing scale: 8px baseline (8/12/16/24/32...).

## 2) Typography
- Use **system UI font** (fast + familiar).
- Headlines: bold, slightly condensed feel via tight letter-spacing.
- Body: readable, neutral, not tiny.

**Targets**
- H1: 36–44px responsive, tight line-height.
- Body: ~14–16px.
- Muted text: used for explanations, not for critical info.

## 3) Color system
- Background: **white**.
- Text: near-black.
- Borders: soft grey.
- Brand accent: **clean blue**.
- Optional secondary accent: **calm green** (success/positive states).

**Never**
- Neon colors
- Red-heavy UI (reads as aggressive)
- Multiple competing accents

## 4) Components

### Cards
- Use cards to group meaning (filters, results, detail panel).
- Subtle border + subtle shadow (don’t overdo shadows).

### Buttons
- Primary button: brand blue.
- Secondary button: white with border.
- Keep labels short and action-based.

### Inputs/Filters
- Filters should feel like a “control panel”, not a form.
- Prefer **few filters + search** over 20 dropdowns.

## 5) Content design (microcopy)
- Keep copy **direct** and **non-salesy**.
- Use Singaporean parent vocabulary: “P1”, “WA1/WA2/WA3”, “EOY”, “Prelim”.
- Avoid jargon like “faceted navigation” in the UI.

## 6) Trust signals (critical)
- Clearly state: **link-out only**.
- Provide a straightforward path for **corrections/takedown**.
- Avoid aggressive ads/overlays/popups entirely.

## 7) Accessibility & usability
- All pages must work on mobile.
- Color contrast must remain readable in sunlight.
- Tap targets: >= 44px height.
- No hover-only interactions.

## 8) Performance rules
- No heavy frameworks for MVP.
- Prefer plain HTML/CSS/JS.
- Keep assets minimal.

## 9) What “polished” means here
- Consistent spacing
- Consistent button styles
- Consistent headings
- No layout jumps
- No clutter

---

## Implementation notes
- CSS tokens live in: `docs/styles.css` (`:root` variables).
- New pages must reuse the existing layout primitives:
  - `.container`, `.header`, `.card`, `.row`, `.btn`, `.table`

## UI checklist (must pass before merging)
For every new/edited page in `/docs`:
- [ ] Uses `.container`, `.header`, `.card` (no random layouts)
- [ ] Mobile looks correct at ~390px wide (no horizontal scroll)
- [ ] Clear purpose in the first screen (no link-dump)
- [ ] Copy is neutral + direct (no salesy spam tone)
- [ ] Trust signal present where relevant (link-out only, takedown path)
- [ ] Buttons are consistent (`.btn` / `.btn.secondary`)
- [ ] Text contrast remains readable in bright light
- [ ] Page has `<title>` and (where sensible) a meta description
- [ ] No heavy libraries/frameworks added for MVP

## Change control
- If you change colors/typography/spacing, update both:
  - `docs/styles.css`
  - this file (DESIGN_PRINCIPLES.md)
