# Changelog

## Unreleased

- Smoke CI for the Pages console (`scripts/check.py`: required files, PNG 2000×1400, inline script parse, HTML-entity landmine).
- `<noscript>` fallback to `ARCHITECTURE.md` if the console cannot boot.
- Drift lab: writing discovery into NetBox clears `core-rtr-b1` OS drift so the anti-pattern is visible.

## v2.0 — 2026-08-29

Shipped. Interactive architecture console on GitHub Pages.

- Five-stage pipeline upgraded: OTLP / Grafana Alloy, Tempo, gNMI, IPFIX/sFlow, adaptive sampling, SLO ownership, GitOps dashboards.
- Live labs: collector kill/revive (silence is a failure), intent-vs-actual drift with the discovery-write anti-pattern, dual-signal alert gate, read-only AI control plane with human-approved change plans.
- Docs: `ARCHITECTURE.md` is the pattern. `index.html` is how you operate it. Zero runtime dependencies.

## v1.1 — 2026-08-22

Last static-only push. Docs live. Repo was HTML + `architecture.png` + README + MIT.

## v1.0 — 2026-07-29

Reference page published. Five-stage pipeline, three rules, four design decisions.
