# Network Observability & Source of Truth

Vendor-neutral reference architecture for a large multi-vendor network estate.

**Contains no client, environment, or proprietary detail.** Tooling names are open-source projects, not a vendor endorsement.

[![status](https://img.shields.io/badge/status-v2.0_shipped-3fb950)](https://gesh75.github.io/network-observability-architecture/)
[![pages](https://img.shields.io/badge/docs-live-58a6ff)](https://gesh75.github.io/network-observability-architecture/)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![posture](https://img.shields.io/badge/posture-read--only_until_approved-2ea44f)](#three-rules)

> **Live console:** https://gesh75.github.io/network-observability-architecture/
>
> Part of the **[GESH Lab hub](https://gesh75.github.io/)**. Pattern detail lives in [`ARCHITECTURE.md`](ARCHITECTURE.md).

## What this is

How to build visibility that can be handed over:

- Vendor telemetry into an open-source stack
- A source of truth (NetBox) that states what *should* exist
- Drift measured against it — discovery never writes intent
- Alerts gated on two independent signals
- Automation that stays read-only until a human approves the change
- An AI control plane that can read anything and change nothing

Collectors do **not** run on production network devices.

## v2.0 — shipped 2026-08-29

Same five-stage pipeline and three rules. The fabric is current, and the public page is an **interactive console** (still one HTML file).

| Stage | v1 | v2 add |
| --- | --- | --- |
| Sources | Vendor API + syslog | gNMI / OpenConfig, IPFIX/sFlow, WAN synthetics |
| Collect | API collectors + Vector | Grafana Alloy (OTLP), freshness SLOs, adaptive sampling |
| Store | NetBox, InfluxDB, Loki | Tempo (job traces), Mimir as scale path, git for dashboards |
| Visualize | Grafana as code | NetBox-enriched topology, SLO burn, freshness heatmap |
| Act | Chat + runbooks | Dual-signal gate, read-only AI, human-approved change plans |

Try it on the live page:

| View | What it proves |
| --- | --- |
| [Command](https://gesh75.github.io/network-observability-architecture/#/) | Freshness KPIs, drift strip, dual-signal gate, event tape |
| [Pipeline](https://gesh75.github.io/network-observability-architecture/#/pipeline) | Five stages, v1 vs v2, the three rules |
| [Estate](https://gesh75.github.io/network-observability-architecture/#/estate) | Kill a collector — silence is a failure, not good news |
| [Drift](https://gesh75.github.io/network-observability-architecture/#/drift) | Toggle writing discovery into NetBox and watch intent rot |
| [Alerts](https://gesh75.github.io/network-observability-architecture/#/alerts) | Both signals must agree before a page fires |
| [Control plane](https://gesh75.github.io/network-observability-architecture/#/control-plane) | Draft a check-mode plan; a human still approves it |
| [Roadmap](https://gesh75.github.io/network-observability-architecture/#/roadmap) | Shipped / next / planned |

## Three rules

1. **Intent versus actual.** NetBox holds intended state. Collectors report what is running. Drift is measured, never merged.
2. **Read-only until proven.** Writes run check-mode first, canary before fleet, with a recorded rollback.
3. **Read anything, change nothing.** The AI control plane answers in English. It cannot restart a collector, push config, or write NetBox.

## Files

| File | Role |
| --- | --- |
| `index.html` | Interactive architecture console. Semantic HTML, CSS, and a hash-routed lab. Zero runtime dependencies. |
| `architecture.png` | Open Graph / Twitter share card, **2000×1400** RGB PNG. |
| `ARCHITECTURE.md` | The pattern, written down. |
| `CHANGELOG.md` | What shipped. |
| `LICENSE` | MIT. |

A commit to `main` is the release. GitHub Pages serves `main` / root.

## Edit and preview

All tokens live on `:root` in `index.html`. Dark theme only. Honor `prefers-reduced-motion`. Keep it generic — no client names.

Social-card tags use **absolute** `https://gesh75.github.io/...` URLs. After replacing `architecture.png`, keep `og:image:width` / `height` in sync (2000×1400) and re-scrape LinkedIn/X if the Featured card is stale.

## Add to LinkedIn

Profile → **Featured** → **Add a link** → paste the Pages URL.

- **Title:** Network Observability & Source of Truth — Reference Architecture
- **Description:** The pattern I build: multi-vendor telemetry into an open-source stack, NetBox as the source of truth, alerts gated on two agreeing signals, and automation that stays read-only until a human approves the change.

## Sibling GESH projects

Observability does not live alone.

- [netlog-ai](https://github.com/gesh75/netlog-ai) — syslog becomes RCA
- [aegis](https://github.com/gesh75/aegis) — validate before deploy
- [argus](https://github.com/gesh75/argus) — test the perimeter
- [multivendor-ai-network-lab](https://github.com/gesh75/multivendor-ai-network-lab) — close the loop

## License

MIT. See [`LICENSE`](LICENSE).
