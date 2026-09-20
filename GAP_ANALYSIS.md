# Gap analysis — network-observability-architecture

> Merge note (2026-09-20): `origin/main` was merged into this Cursor gap-scan
> branch. Unique scan/fix work from the PR is kept. Do not drop later main
> changes in other files.


**Date:** 2026-09-05
**Scope:** docs / GitHub Pages console (no backend). Ranked by evidence, not taste.
**Method:** read the tree, parse the inline script, curl the live host and sibling repos, inspect git history. No dependency upgrades. No new product features.

## What this repo is

Seven files and a 60 KB hash-routed lab in `index.html`. A commit to `main` is the release. Sibling GESH apps (`netlog-ai`, `aegis`, `argus`) have CI; this one did not.

## P0 — ship-stopping or already shipped

| ID | Gap | Evidence |
| --- | --- | --- |
| P0-1 | **No CI.** A syntax error in the inline script publishes a blank Pages shell. This already happened. | `.github/` did not exist. `git show 949aee3` / `1d2b1d8`: *“HTML entities had collapsed the escape helper and killed the page script”* / *“Pages rendered a blank shell.”* Live `index.html` still encodes entities as `\u0026amp;` so a formatter that writes `&amp;` will break boot again. |
| P0-2 | **Empty shell if JS dies.** `#view` is filled only by the IIFE. There was no fallback to the written pattern. | `index.html` body is chrome + `<div class="wrap" id="view"></div>` + footer. No `<noscript>` on the live page (`curl` 2026-09-05). Same failure mode as P0-1, for users rather than authors. |

## P1 — correctness / a11y / latent security

| ID | Gap | Evidence |
| --- | --- | --- |
| P1-1 | **Drift lab contradicts itself.** Toggle “write discovery into NetBox” rewrites the intended-OS *cell* for `core-rtr-b1` but `driftOf()` still scores OS drift, so the row stays “1 field” and the headline count does not drop. The anti-pattern (mistake becomes policy) is not visible in the table. | `index.html` `drift()` uses `intendedB1` only in the Intended column; `driftOf()` compares `d.intendedOs` (`IOS-XR 7.11.2`) forever. |
| P1-2 | **Hamburger is not a disclosure button.** Mobile nav works after `1d2b1d8`, but `#ham` never sets `aria-expanded` / `aria-controls`. | `index.html` click handler toggles `.open` and the label text only. |
| P1-3 | **No main landmark.** Skip link targets `#view`, which is a `div`. | `index.html` around the `#view` wrapper. |
| P1-4 | **Latent XSS if `esc()` regresses.** Operator text is interpolated via `innerHTML`. The only guard is `esc()`. | `index.html` `plane()` / `ask()`. If P0-1 recurs and someone “fixes” `esc` to pass `node --check` while returning raw `&`, chat input is unescaped. |
| P1-5 | **No route-level test.** `node --check` cannot see a dead hash route or a tick that re-renders and kills the menu (the `949aee3` `patchLive` fix). | `views` map in `index.html`; no Playwright/e2e job. |

## P2 — DX, docs, dead weight

| ID | Gap | Notes |
| --- | --- | --- |
| P2-1 | README Files table omits `.nojekyll` and (now) `scripts/check.py`. | Docs drift, not a broken link. |
| P2-2 | `ARCHITECTURE.md` license line is the word “MIT.” with no link to `LICENSE`. | Cosmetic. |
| P2-3 | No `canonical` / `robots.txt` / sitemap. | Fine for a single Pages URL; add only if the hub starts deep-linking copies. |
| P2-4 | No CSP meta. | GitHub Pages; not worth a false sense of safety. |
| P2-5 | `ROADMAP` tone map includes `now`, never used. | Dead branch in `roadmap()`, not user-visible. |
| P2-6 | Cloud-West site hosts no collector. | Intentional empty-state demo. Do not delete. |
| P2-7 | `prefers-reduced-motion` is CSS-only; `setInterval(tick, 2000)` and `scrollTo(0,0)` still run. | README claims the media query is honored. Numbers updating is not a motion bug; skip unless someone asks. |
| P2-8 | LinkedIn profile returns HTTP 999 to anonymous curl. | Anti-bot, not a dead link. Browser and the in-profile Featured card still apply. |
| P2-9 | No issue templates / CODEOWNERS. | One-maintainer Pages repo. Skip. |
| P2-10 | Closed draft PR #1 is stale vs v2.0. | Informational only. |

## Proved this scan

- `architecture.png` is 2000×1400 RGB, matching `og:image:*` (not a gap).
- `node --check` on the extracted `<script>` passes on `main`.
- Live Pages, OG image, GESH hub, and all six sibling GitHub URLs return HTTP 200.
- Every relative markdown link in `README.md` resolves.
- No API keys, tokens, or private-key smells in the tree.
- No `.github/workflows` on `main` before this PR. Sibling repos already run CI.

## Skipped (on purpose)

- Splitting `index.html` into modules or adding a bundler.
- Dependency upgrades (there are no runtime dependencies).
- Playwright / visual regression (next job, not this one).
- Inventing collectors, Alloy kits, or any v2.1 product work.
- “Fixing” Cloud-West, `tone.now`, or LinkedIn 999.
- CodeQL / Dependabot on a single static HTML file.

## Fixes in this PR (3, all small)

1. **`scripts/check.py` + `.github/workflows/ci.yml`** — required files, PNG size vs OG tags, `<noscript>`, `node --check`, fail if HTML entities re-enter the script.
2. **`<noscript>` in `index.html`** — points at `ARCHITECTURE.md` if the IIFE does not run.
3. **`driftOf()` honors `writeDiscovery`** — overwriting intent for `core-rtr-b1` clears that OS drift so the lab matches its own copy.

## Next recommended agent job

Add a headless Playwright smoke that opens each of the seven hash routes and asserts `#view` is non-empty after load, then toggles the Drift anti-pattern and expects `core-rtr-b1` OS drift to disappear.
