# Network Observability & Source of Truth — Reference Architecture

A single-file, self-contained page describing a vendor-neutral reference architecture for
network observability and source-of-truth management.

**Contains no client, environment, or proprietary detail.** Tooling names are open-source
projects. Safe to publish publicly.

## Deploy to GitHub Pages

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

Live at `https://gesh75.github.io/network-observability-architecture/` within a minute or two.

## Add to LinkedIn

Profile → **Featured** → **Add a link** → paste the Pages URL.

- **Title:** Network Observability & Source of Truth — Reference Architecture
- **Description:** The pattern I build: multi-vendor telemetry into an open-source stack,
  NetBox as the source of truth, alerts gated on two agreeing signals, and automation that
  stays read-only until a human approves the change.

## Notes

- No build step, no dependencies, no external requests — one HTML file.
- Responsive: verified at 390px (all grids collapse to one column, zero horizontal overflow)
  and at 1600px desktop.
- Dark theme only, by design.
- To edit content, open `index.html` — the markup is plain semantic HTML with all CSS inline
  in `<head>`.
