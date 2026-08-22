# Network Observability & Source of Truth — Reference Architecture

A vendor-neutral reference architecture for network observability and
source-of-truth management. The published artifact is a single self-contained
page — no build step, no runtime dependencies.

**Contains no client, environment, or proprietary detail.** Tooling names are
open-source projects, not a vendor endorsement. Safe to publish publicly.

**Live:** https://gesh75.github.io/network-observability-architecture/

## Repository layout

| File | Role |
| --- | --- |
| `index.html` | The page: semantic HTML plus all CSS in `<head>`. No JavaScript. |
| `architecture.png` | Open Graph / Twitter preview image, **2000×1400** RGB PNG. |
| `LICENSE` | MIT. |
| `README.md` | This file — how to preview, edit, publish, and avoid stale cards. |

There is no `package.json`, bundler, or CI. A commit to `main` is the release.

## What the page documents

`index.html` is the architecture, not a stub. Edit it in place. Sections, in order:

1. **Hero** — title, lede, byline (LinkedIn + GitHub).
2. **The pipeline** — five read-only-by-default stages: Sources → Collect → Store → Visualize → Act.
   - Store names three systems: NetBox (intent), InfluxDB (metrics), Loki (logs).
   - Collect calls out scheduled API collectors and `rsyslog` → Vector, with no agent on production devices.
3. **Three rules** — intent vs actual; read-only until proven; AI control plane that reads anything and changes nothing.
4. **Design decisions** — dual-signal alerts, collector freshness, source of truth ≠ discovery, handover/runbooks.
5. **Footer** — vendor-neutral disclaimer and stack tags (NetBox, Grafana, InfluxDB, Loki, Vector, Ansible, Python, MCP).

Do not fork this content into a second markdown architecture page. The HTML is the source of truth; a duplicate will drift.

## Local preview

Any static file server is enough. From the repo root:

```bash
python3 -m http.server 8080
```

Open http://127.0.0.1:8080/. Opening `index.html` via `file://` also works for layout checks.

Social-card tags use **absolute** `https://gesh75.github.io/...` URLs. Local preview will not show Open Graph images; crawlers only see them on the Pages URL.

## Edit the page

All design tokens live on `:root` in `index.html` (`--bg`, `--panel`, `--tx`, `--blue`, `--pur`, `--grn`, `--amb`, `--cor`, and the rest). Grids use `repeat(auto-fit, minmax(...))`:

- Pipeline stages: `minmax(215px, 1fr)`
- Principles: `minmax(290px, 1fr)`
- Decision cards: `minmax(300px, 1fr)`

Constraints when editing — these match the current markup, not aspirations:

- **No JavaScript.** There is no `<script>` today; do not add one.
- **No external requests at runtime.** No webfonts, analytics, or CDN CSS. The only outbound `href`s are the byline LinkedIn and GitHub links.
- **Dark theme only.** There is no light-theme media query.
- **Honor `prefers-reduced-motion`.** The existing query disables transitions and smooth scroll.
- **Keep it generic.** No client names, environment hostnames, or proprietary product detail.
- **Check narrow and wide.** Grids are expected to collapse to one column at **390px** (zero horizontal overflow) and hold the multi-column layout at **1600px**.

## Social previews

Commit `5c8bb0a` added deterministic link previews. The tags in `<head>` must stay consistent with the file on disk:

| Tag | Current value (must match the file) |
| --- | --- |
| `og:url` | `https://gesh75.github.io/network-observability-architecture/` |
| `og:image` / `twitter:image` | `.../architecture.png` |
| `og:image:width` / `og:image:height` | `2000` / `1400` |
| `og:image:type` | `image/png` |
| `twitter:card` | `summary_large_image` |

When replacing the image:

1. Overwrite `architecture.png` at **2000×1400**.
2. Keep the `og:image:*` dimensions in sync if the size changes.
3. Update `og:image:alt` if the diagram’s meaning changes.
4. Expect crawler cache. After Pages publishes the new PNG, re-scrape the URL in LinkedIn/Twitter/Facebook card debuggers, or wait for their TTL.

The GitHub repo **About → Website** field is currently empty. Setting it to the Pages URL makes the live page discoverable from the repo header; it is not required for Pages itself.

## Deploy to GitHub Pages

The site is already published from **`main` / root** (no `/docs` folder, no Actions workflow). After the first push:

```bash
git add index.html architecture.png
git commit -m "docs: update reference architecture page"
git push origin main
```

Pages serves the new `index.html` within a minute or two.

First-time bootstrap (empty directory only):

```bash
cd network-observability-architecture
git init
git add .
git commit -m "feat: network observability reference architecture"
git branch -M main
git remote add origin git@github.com:gesh75/network-observability-architecture.git
git push -u origin main
```

Then: **repo → Settings → Pages → Source: `main` / root → Save.**

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `404` on the github.io URL | Pages source is `main` / root, not a `/docs` folder or a different branch. The site root file must be named `index.html`. |
| Page updates but the social card does not | `architecture.png` is cached by crawlers. Confirm the PNG is reachable at the `og:image` URL, then re-scrape. |
| Card image is cropped or blank | File is not 2000×1400, or `og:image:width` / `height` no longer match the PNG. |
| Horizontal scroll on a phone | A new grid or long unwrapped string broke the `minmax` collapse. Test at 390px. |
| Preview looks unstyled | You opened a copy that is not `index.html`, or CSS in `<head>` was split into an external file that was not committed. |

## Add to LinkedIn

Profile → **Featured** → **Add a link** → paste the Pages URL.

- **Title:** Network Observability & Source of Truth — Reference Architecture
- **Description:** The pattern I build: multi-vendor telemetry into an open-source stack, NetBox as the source of truth, alerts gated on two agreeing signals, and automation that stays read-only until a human approves the change.

LinkedIn reads the `og:*` tags. If the Featured preview is stale after an image change, use LinkedIn’s post inspector on the Pages URL.

## License

MIT. See `LICENSE`.
