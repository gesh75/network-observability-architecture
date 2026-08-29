# Network Observability & Source of Truth — Reference Architecture

Vendor-neutral reference architecture for network observability and source-of-truth management.

**Contains no client, environment, or proprietary detail.** Tooling names are open-source
projects. Safe to publish publicly.

**Status:** v2.0 (2026-08-29) · Pages live · MIT

## What this is

How to build visibility into a large multi-vendor network estate:

- Vendor telemetry into an open-source stack
- A source of truth (NetBox) that states what *should* exist
- Drift measured against it — discovery never writes intent
- Alerts gated on two independent signals
- Automation that stays read-only until a human approves the change
- An AI control plane that can read anything and change nothing

## v2.0 (this revision)

Same five-stage pipeline and three rules. The fabric is current:

| Stage | v1 | v2 add |
| --- | --- | --- |
| Sources | Vendor API + syslog | gNMI / OpenConfig, IPFIX/sFlow, WAN synthetics |
| Collect | API collectors + Vector | Grafana Alloy (OTLP), freshness SLOs, adaptive sampling |
| Store | NetBox, InfluxDB, Loki | Tempo (job traces), Mimir as scale path, git for dashboards |
| Visualize | Grafana as code | NetBox-enriched topology, SLO burn, freshness heatmap |
| Act | Chat + runbooks | Dual-signal gate, read-only AI, human-approved change plans |

Collectors still do **not** run on production network devices.

## Live

Docs: https://gesh75.github.io/network-observability-architecture/

Repo: https://github.com/gesh75/network-observability-architecture

## Files

- `index.html` — self-contained reference page (zero dependencies)
- `architecture.png` — share card
- `LICENSE` — MIT

To edit content, open `index.html`. Dark theme only, by design. Responsive at 390px and 1600px.

## Add to LinkedIn

Profile → **Featured** → **Add a link** → paste the Pages URL.

- **Title:** Network Observability & Source of Truth — Reference Architecture
- **Description:** The pattern I build: multi-vendor telemetry into an open-source stack, NetBox as the source of truth, alerts gated on two agreeing signals, and automation that stays read-only until a human approves the change.
