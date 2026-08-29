# Architecture — Network Observability & Source of Truth

Generic reference pattern. No client, environment, or proprietary detail.
Tooling names are open-source projects, not an endorsement of any vendor.

**Status:** v2.0 shipped 2026-08-29.
**Live:** https://gesh75.github.io/network-observability-architecture/

This document is the pattern. The [console](https://gesh75.github.io/network-observability-architecture/) is how you feel it.

## Constraint

Collectors live on organization-owned hosts. Devices keep exporting what they already export: vendor API, syslog, gNMI, IPFIX/sFlow. A third-party agent on a core router is an availability and support-boundary problem disguised as convenience.

## Pipeline

```
Sources → Collect → Store → Visualize → Act
```

Every stage is read-only by default, scheduled on organization-owned hosts, and monitored for its own freshness. A dead feed raises an alert rather than going quiet.

| Stage | Question | v2 fabric |
| --- | --- | --- |
| **Sources** | What exists in the estate? | Vendor APIs, syslog, gNMI/OpenConfig, IPFIX/sFlow, WAN synthetics |
| **Collect** | How does it arrive without lying? | Grafana Alloy (OTLP), Vector for syslog, scheduled API collectors, adaptive sampling, heartbeat + freshness SLO |
| **Store** | Where does each answer live? | NetBox (intent), InfluxDB now / Mimir as scale path (metrics), Loki (logs), Tempo (job traces), git (dashboards + unit files) |
| **Visualize** | Who owns the red graph? | Grafana as code. Every panel has a named owner, an SLO, and NetBox labels (site, circuit, runbook) |
| **Act** | What is allowed to page, and what is allowed to change? | Dual-signal gate. Read-only AI control plane. Human-approved change plans: check-mode, canary, recorded rollback, append-only audit |

Tempo does not replace NetFlow. It traces collector hops and approved change jobs so a write has a beginning, a middle, and a verdict. Packet-level truth stays in flow and syslog.

OTLP is the interchange, not a vendor. Alloy is a distribution. Vendor APIs still get collected — they get normalized at the edge.

## Three rules

### 1. Intent versus actual

NetBox holds intended state: what should exist. Collectors report actual state: what is running. The gap is measured and reported. Discovery never writes NetBox. If you merge them, the database documents last Tuesday’s mistakes as policy.

### 2. Read-only until proven

Scheduled jobs back configuration up to git and score every device against a hardening baseline. Anything that writes runs in check-mode first, canary before fleet, with a recorded rollback. If it only works while one person is present, it is a liability, not a platform.

### 3. Read anything, change nothing

A single control plane reads every system and answers in plain English. It cannot restart a collector, push configuration, open tickets, or write NetBox. Writes execute only inside a human-approved plan, fully audit-logged. Stale feeds are disclosed, never hidden.

## Design decisions people usually get wrong

**Alerts that survive contact with humans.** An alert fires only when two independent signals agree. One hot counter is a yellow for the owner, not a page. A channel people mute is worse than no alerting at all.

**Collectors that admit when they die.** Every feed reports its own freshness on a cadence. Silence is a failure state. The most dangerous dashboard is one that is quietly three weeks stale. Freshness pages the collector owner, not the WAN on-call.

**Source of truth is not discovery.** NetBox records what the network is supposed to be. Discovery reports what it is. Conflating the two produces a database that documents your mistakes instead of your intent.

**Built to be handed over.** Organization-owned infrastructure, version control, runbooks, an escalation ladder, a documented restore path. Restore from the git-tracked unit file. Do not hotfix on the box. Do not tight-loop a 429.

**Cost scales with insight.** Adaptive sampling at the collector. Freshness SLOs protect the signal; retention tiers protect the bill.

## Dual-signal gate

Example — WAN loss:

- Signal A: interface error-delta (metrics)
- Signal B: syslog / IPFIX drop (logs + flow)
- Page only when both fire
- Runbook uses the circuit ID from NetBox, not from memory
- A carrier maintenance window is an annotation, not a ticket

Collector death is also dual-signal: heartbeat miss **and** missing ingest. One empty graph is not a page.

## Change plan shape

The control plane may draft. A human approves. Execution remains human (or gated automation under that approval).

```
PLAN
title: <short>
check-mode: <what dry-run proves>
canary: <one device / one site>
rollback: <how we undo>
risk: <one sentence>
```

## What this is not

- Not a vendor bake-off.
- Not a packet broker.
- Not a closed loop that writes the network.
- Not a merge with [aegis](https://github.com/gesh75/aegis) (pre-deploy validation stays a sibling) or [argus](https://github.com/gesh75/argus) (the perimeter tester).
- Not a warehouse that keeps every counter forever.

## Roadmap after v2.0

| Version | When | What |
| --- | --- | --- |
| v2.1 | 2026-Q4 | Alloy + Grafana as-code kit — pipelines, dashboard JSON, alert rules, freshness recording rules. Mimir as the metrics scale path beside InfluxDB. |
| v2.2 | 2027-Q1 | gNMI and flow first-class. gnmic subscriptions with freshness tags. IPFIX/sFlow distilled at the edge. WAN synthetics on the same dual-signal gate. |
| v3.0 | 2027 | What-if against intent. Batfish (or equivalent) scored against NetBox before a plan is offered. Closed loop stays human-gated. |

## License

MIT.
