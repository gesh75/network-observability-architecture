# Gap analysis — network-observability-architecture

Scanned `origin/main` at `73e3dd1` (`docs: v2.0 shipped`). This repo is a static GitHub Pages console: seven tracked files, no runtime dependencies, no application backend.

**Method.** Read every tracked file. Extracted the inline script from `index.html` and ran `node --check` (passes today). Confirmed `architecture.png` is 2000×1400 RGB. `curl -I -L`’d the live Pages URL, the PNG, `ARCHITECTURE.md`, the GESH Lab hub, and all sibling GitHub links (all HTTP 200). LinkedIn returns 999 to this user-agent (bot filter, not treated as a break). `git ls-files` on `origin/main` has no `.github/`. Searched for secret-like strings (none; README “tokens” means CSS custom properties). Compared README / `ARCHITECTURE.md` / console data. Inspected the two blank-page hotfixes (`949aee3`, `1d2b1d8`).

Out of scope stayed out: dependency upgrades, new product features, rewriting the console, Playwright/e2e suites.

## P0

### P0-1 — Pages can ship a blank console; nothing parses the script

- **Files:** missing `.github/workflows/*`; product is `index.html` (inline `<script>` starting ~line 177).
- **Evidence:**
  - `git ls-files` on `origin/main` is `.nojekyll`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LICENSE`, `README.md`, `architecture.png`, `index.html`. There is no workflow, no test, no `scripts/`.
  - README line 69: “A commit to `main` is the release. GitHub Pages serves `main` / root.”
  - `949aee3` *fix: restore console boot*: “HTML entities had collapsed the escape helper and killed the page script.” The previous `esc()` used `"&amp;"` / `"&lt;"` literals inside the script tag; they decoded into invalid JS (`"\"":"""`).
  - `1d2b1d8` *fix: boot the architecture console*: same outage class — “The escape helper had been HTML-decoded into invalid JS, so Pages rendered a blank shell.”
  - Today `node --check` on the extracted script **passes**. The gap is that no check runs before `main` is the site.
- **Why P0.** The published artifact is one HTML file. A syntax error blanks every view. It already happened twice in one day.
- **Smallest fix.** A no-dep smoke that extracts the script, runs `node --check`, and rejects raw HTML entities inside `<script>`. Landed in this PR.

## P1

### P1-1 — `prefers-reduced-motion` is documented and does not win

- **Files:** `index.html` lines 31 and 144; README line 73 (“Honor `prefers-reduced-motion`”).
- **Evidence.** `html{scroll-behavior:smooth}` (specificity `0,0,1`) vs `@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}` (specificity `0,0,0`). The `*` rule cannot override `html`. Hash changes call `window.scrollTo(0,0)`, which follows CSS `scroll-behavior` on the root scroller.
- **Smallest fix.** Set `html{scroll-behavior:auto}` inside the reduced-motion query. Landed in this PR.

### P1-2 — Drift anti-pattern toggle is cosmetic

- **Files:** `index.html` `drift()` (~561) and `driftOf()` (~267).
- **Evidence.** `data-discovery` flips `state.writeDiscovery` and only substitutes the intended-OS *cell* for `core-rtr-b1`. `driftOf()` still compares `d.intendedOs` vs `d.actualOs`, so the score chip and the cards below still show OS drift after “Discovery is writing NetBox.” The lab does not change the drift count.
- **Skipped here.** Behavioral change to the teaching lab; needs a deliberate assertion (count goes to N−1, or the OS row disappears).

### P1-3 — Hamburger has no expanded state

- **Files:** `index.html` `#ham` (line 162) and the click handler (~764).
- **Evidence.** The button toggles `.open` on `#chrome` and swaps `aria-label` between “Open menu” / “Close menu”, but never sets `aria-expanded` or `aria-controls="mob"`. `1d2b1d8` already had to fix mobile nav routing (`if(t.tagName==="A") return` swallowed hash changes).
- **Skipped here.** Two-attribute a11y patch; next agent can do it with the route smoke.

### P1-4 — README sibling list lags the console

- **Files:** `README.md` “Sibling GESH projects”; `index.html` `SUITE` (~218).
- **Evidence.** README lists four repos. The Roadmap view lists six (`napalm-live-lab`, `multivendor-cli-configurator` are missing from README). All six GitHub URLs return 200.
- **Skipped here.** Copy sync only; not a break.

### P1-5 — Roadmap / status copied in three places

- **Files:** `CHANGELOG.md`, `ARCHITECTURE.md` “Roadmap after v2.0”, `index.html` `ROADMAP`.
- **Evidence.** Same versions and dates appear in all three. A date slip will not fail any check. No single source.
- **Skipped here.** Dedup would be a rewrite of how status is published.

### P1-6 — No local preview command

- **Files:** `README.md` “Edit and preview”.
- **Evidence.** The section says what not to break. It does not say `python3 -m http.server` (or equivalent). Closed unmerged PR #1 tried to add this and never landed.
- **Smallest fix.** One command plus the new smoke. Landed in this PR.

## P2

| ID | Area | Gap | Evidence | Why skipped |
| --- | --- | --- | --- | --- |
| P2-1 | Dead code | Unused `.btn.warn` and `.cols2` | Selectors exist only in the `<style>` block; no `class="btn warn"` / `cols2` in markup or JS | Deletion landed (safe, no behavior). |
| P2-2 | Dead code | `tone.now` never used | `ROADMAP` statuses are `shipped` / `next` / `planned` only | Harmless lookup table; leave it. |
| P2-3 | Correctness | Unknown hashes render Command | `views[state.route] \|\| command` — `#/nope` looks like home | Need a tiny 404 view; not a ship blocker. |
| P2-4 | DX | No-JS users get an empty `#view` | `#view` is filled only by the IIFE | Interactive lab by design; a `<noscript>` would be a feature. |
| P2-5 | Security | No CSP | No remote scripts/styles today; XSS surface is the local `esc()` path | CSP is extra product; `esc()` is already unicode-escaped. |
| P2-6 | Docs | No `SECURITY.md` / `CONTRIBUTING.md` | Static MIT page, no issue templates | Fine until someone else commits. |
| P2-7 | CI | No link or OG re-scrape check | Live links were 200 at scan time; OG tags match the PNG | Periodic, not every PR. |
| P2-8 | A11y | `setInterval(tick, 2000)` ignores reduced motion | Freshness heatmap still animates | Lab signal; don’t freeze the demo without a design call. |

## Fixes in this PR (3)

1. **`scripts/check.py` + `.github/workflows/ci.yml`** — extract/parse the console script, reject the `esc()` entity-collapse regression, require boot DOM ids, assert PNG 2000×1400 matches `og:image` tags, assert the reduced-motion `html` override. README “Edit and preview” now names the preview and check commands.
2. **`index.html` reduced-motion** — `html{scroll-behavior:auto}` inside the existing media query so the documented contract holds.
3. **Delete unused `.btn.warn` and `.cols2`** — no references.

## What I proved

- Console JS parses; required ids exist; PNG and OG dimensions match.
- Live Pages, hub, and sibling GitHub URLs respond 200.
- No secret material in-tree.
- The blank-page failure mode is real (two consecutive commits) and was unguarded.

## What I skipped

- Drift-lab behavior, hamburger `aria-expanded`, README sibling sync, roadmap dedup, unknown-route 404, `<noscript>`, CSP, e2e/Playwright, dependency or stack upgrades, any new architecture content.

## Next recommended agent job

Add a no-browser hash-route smoke that mounts the extracted script, visits each `NAV` path, and asserts `#view` is non-empty (plus Estate kill/revive and the Alerts AND-gate), so a render exception cannot ship another blank console.
