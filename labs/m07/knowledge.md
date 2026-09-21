# Knowledge Base — Operations

---

## DOC-RUNBOOK-014 — account-api Latency Runbook

DOC_ID: DOC-RUNBOOK-014  
AUTHORITY: high  
DATE: 2026-09-01  
STATUS: ACTIVE

### Scope

This runbook applies to latency degradation affecting `account-api`.

It is intended for active operational diagnosis. A diagnostic signal must not
be presented as a confirmed root cause unless the incident record explicitly
marks the root cause as confirmed.

### Cache diagnostics

When p95 latency is elevated, compare it with the service baseline.

If cache hit ratio falls below 80%, inspect:

- cache eviction rate;
- key churn;
- backend fetch latency;
- recent cache policy changes.

Compare these values with the pre-incident baseline.

A reduced cache hit ratio is a diagnostic signal. It does not by itself prove
that the cache is the root cause.

### Safe actions

Reading telemetry, checking dashboards and comparing baselines are safe
diagnostic actions.

Do not flush, restart or reconfigure the cache without explicit approval from
the Incident Commander.

---

## DOC-POLICY-021 — Production Change Readiness Policy

DOC_ID: DOC-POLICY-021  
AUTHORITY: highest  
DATE: 2026-08-15  
STATUS: ACTIVE

### Rollback readiness

For `account-api` production changes, a rollback plan must exist and the latest
successful rollback rehearsal must have completed within the previous 30 days.

A rehearsal older than 30 days does not satisfy the production readiness gate.

The rehearsal must have succeeded. A scheduled rehearsal or a documented plan
without execution does not count as evidence.

### Security-sensitive changes

Changes affecting authentication, authorization, secrets or token lifecycle
also require an approved security review with no open blockers.

### Evidence

References such as "tests executed", "rollback documented" or "security review
requested" do not count as PASS unless the required result is available.

---

## DOC-HANDBOOK-008 — Legacy Deployment Handbook

DOC_ID: DOC-HANDBOOK-008  
AUTHORITY: medium  
DATE: 2025-02-10  
STATUS: SUPERSEDED

### Historical rollback rule

This handbook previously allowed `account-api` production changes when a
successful rollback rehearsal had been completed within the previous 90 days.

The 90-day requirement was used before the 2026 Production Change Readiness
Policy was introduced.

### Current use

This document is retained for historical reference only.

It must not override active production policy.

---

## DOC-SUPPORT-006 — Customer Incident Communication Policy

DOC_ID: DOC-SUPPORT-006  
AUTHORITY: highest  
DATE: 2026-07-22  
STATUS: ACTIVE

### Outage terminology

For `account-api`, if service availability remains above 99.8% and application
error rate remains below 1%, Support should describe the event as a
`degradation`, not a `complete outage`.

An Incident Commander may explicitly override this classification when there
is customer impact not captured by those metrics.

### Regional impact

For incidents limited to one region, Support must identify the affected region
and must not imply that unaffected regions have the same impact.

### Root cause

Support may communicate a root cause as confirmed only when the incident
record explicitly contains:

```text
rca_status = confirmed
```

An engineering hypothesis is not a confirmed root cause.

---

## DOC-POSTMORTEM-031 — Historical Incident INC-6310

DOC_ID: DOC-POSTMORTEM-031  
AUTHORITY: high  
DATE: 2025-11-04  
STATUS: HISTORICAL

### Symptoms

INC-6310 affected `account-api`.

Symptoms included elevated latency, timeouts and degraded account operations.

### Confirmed cause

The confirmed root cause for INC-6310 was database connection-pool exhaustion
following a deployment that increased query concurrency.

This root cause applies only to INC-6310.

It must not be used as evidence of the root cause of another incident merely
because symptoms are similar.

### Remediation

The team rolled back the query-concurrency change and added improved database
pool saturation monitoring.

The postmortem does not specify the maximum configured connection-pool size.

---

## DOC-CAPACITY-012 — account-api Capacity Planning Notes

DOC_ID: DOC-CAPACITY-012  
AUTHORITY: medium  
DATE: 2026-06-30  
STATUS: ACTIVE

### Capacity planning

Capacity planning for `account-api` tracks:

- CPU headroom;
- memory;
- request rate;
- database utilization;
- cache efficiency.

The document contains quarterly growth projections and load-test targets.

### Database

Database connection-pool utilization is considered an important saturation
signal.

The planning document intentionally does not define the production maximum
connection-pool size because that value is managed by the runtime
configuration and may differ by environment.

---

## DOC-RELEASE-040 — Q3 Product Release Notes

DOC_ID: DOC-RELEASE-040  
AUTHORITY: medium  
DATE: 2026-09-05  
STATUS: ACTIVE

### Product changes

The Q3 release introduces:

- redesigned account profile pages;
- new notification preferences;
- billing-history export filters;
- updated frontend assets.

These release notes describe product functionality, not operational policy.

### account-api

The release notes mention performance improvements in several customer-facing
flows but do not define incident thresholds, rollback policy or runbook
procedures.

---

## DOC-FAQ-003 — Customer Account FAQ

DOC_ID: DOC-FAQ-003  
AUTHORITY: low  
DATE: 2026-05-10  
STATUS: ACTIVE

### General information

The account service provides profile management, session management and access
to customer settings.

Customers experiencing difficulties are advised to retry after a short period
and contact Support if the problem continues.

### Operational scope

This public FAQ does not expose internal incident thresholds, rollback
requirements, infrastructure configuration or diagnostic runbooks.

---

## DOC-SECURITY-017 — Security Advisory SA-2026-044

DOC_ID: DOC-SECURITY-017  
AUTHORITY: highest  
DATE: 2026-09-12  
STATUS: ACTIVE

### Affected component

SA-2026-044 affects the `media-renderer` service and an image-processing
dependency.

It does not affect:

- account-api;
- distributed cache;
- session management;
- customer profile storage.

### Relationship to account-api

There is no known relationship between this advisory and current account-api
latency investigations.

---

## DOC-RETRO-011 — Operations Retrospective Notes

DOC_ID: DOC-RETRO-011  
AUTHORITY: low  
DATE: 2026-08-20  
STATUS: ACTIVE

### Team observations

The team discussed alert quality, documentation cleanup and on-call handover.

An informal comment in the retrospective states:

> "Most account-api latency incidents eventually turn out to be cache or
> database related."

This is a generalization and is not valid evidence of the root cause of a
specific incident.

### Documentation

The team recommended making active policies easier to distinguish from legacy
documents in the internal knowledge base.
