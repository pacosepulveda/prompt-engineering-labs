# Context Bundle — Cloud Operations Assistant

This document contains information with different relevance, authority and freshness.
The assistant must answer only about INC-7782.

---

## SOURCE 1 — Current Incident Record

SOURCE: Incident Manager
TYPE: incident-state
AUTHORITY: high
FRESHNESS: current

incident_id: INC-7782
service: account-api
region: eu-central
status: degraded
availability: 99.94%
error_rate: 0.6%
p95_latency_ms: 820
baseline_p95_latency_ms: 420
affected_regions: eu-central
unaffected_regions: eu-west, us-east, ap-southeast
customer_impact: elevated_latency
data_loss_observed: false
rca_status: investigating
next_customer_update: 15:30 UTC

The service remains available. The primary customer-visible symptom is slower
account operations in eu-central. There is no current evidence of data loss.
No root cause has been confirmed.

---

## SOURCE 2 — Current Observability Snapshot

SOURCE: Observability Platform
TYPE: telemetry
AUTHORITY: high
FRESHNESS: current

Current p95 latency for account-api in eu-central is 820 ms. The normal baseline
for the same traffic window is approximately 420 ms. Availability is 99.94%
and application error rate is 0.6%.

Traffic and latency in eu-west, us-east and ap-southeast are within normal
operating ranges.

Distributed cache hit ratio has fallen from approximately 94% to 71%.
Cache eviction activity is higher than the previous seven-day baseline.

The operations team is investigating whether cache churn is contributing to
the latency increase. This is a hypothesis, not a confirmed root cause.

Database connection-pool utilization is 58%, within normal range. CPU
utilization is 48–63%. Memory-pressure alarms are not firing.

---

## SOURCE 3 — Customer Communication Policy

SOURCE: Operations Governance
TYPE: policy
AUTHORITY: highest
FRESHNESS: current

Customer communications must distinguish observation from diagnosis.

A root cause may only be communicated as confirmed when rca_status=confirmed.

When service availability remains above 99.8% and application error rate is
below 1%, Support should not describe the situation as a complete outage unless
an Incident Commander explicitly overrides this rule.

For regional incidents, Support should identify the affected region and must
not imply that unaffected regions have the same impact.

If there is no evidence of data loss, Support may state that no data loss has
been observed. This must not be converted into a guarantee that data loss is
impossible.

Customer messages should describe the current impact, state that investigation
is ongoing when applicable, and include the next published update time when one exists.

---

## SOURCE 4 — account-api Latency Runbook

SOURCE: SRE Runbook
TYPE: operational-runbook
AUTHORITY: high
FRESHNESS: current

For account-api latency incidents:
1. Confirm whether impact is global or regional.
2. Compare p95 latency with the service baseline.
3. Check application error rate and availability.
4. Check cache hit ratio against baseline.
5. If cache hit ratio is below 80%, inspect eviction rate, key churn, backend
   fetch latency and recent cache-policy changes.
6. Compare database-pool utilization and saturation signals.
7. Do not flush, restart or reconfigure the cache without Incident Commander approval.

A reduced cache hit ratio is a diagnostic signal. It is not by itself proof of root cause.

---

## SOURCE 5 — Historical Postmortem INC-6310

SOURCE: Postmortem Archive
TYPE: historical-incident
AUTHORITY: high
FRESHNESS: historical — 2025-11-04

INC-6310 affected account-api and produced elevated latency, HTTP timeouts and
degraded account operations.

The confirmed root cause of INC-6310 was exhaustion of a database connection
pool following a deployment that changed query concurrency. Cache hit ratio
remained within normal range during that historical event.

Remediation included increasing pool observability, reverting the query
concurrency change and adding an alert for pool saturation.

This root cause applies to INC-6310 only and must not be assumed to apply to
later incidents with similar symptoms.

The historical timeline also contains rollout, rollback, testing and
organizational follow-up details that do not describe the current state of INC-7782.

---

## SOURCE 6 — Q3 Product Release Notes

SOURCE: Product Management
TYPE: release-notes
AUTHORITY: medium
FRESHNESS: current-quarter

The Q3 release introduces a redesigned profile page, new notification
preferences, billing-history export improvements and several frontend asset
changes. None of these release-note items describes the current state of INC-7782.

Product Management expects the new profile experience to reduce support
contacts related to account settings. Documentation is being updated during the quarter.

---

## SOURCE 7 — Public Product FAQ

SOURCE: Customer Documentation
TYPE: product-documentation
AUTHORITY: medium
FRESHNESS: current

The account service provides profile management, session management and access
to customer settings.

The public FAQ does not expose internal SLO thresholds, incident response
procedures, cache architecture or operational runbooks. It is not an
authoritative source for the current state or root cause of an active incident.

---

## SOURCE 8 — Security Advisory SA-2026-044

SOURCE: Product Security
TYPE: security-advisory
AUTHORITY: highest
FRESHNESS: current

SA-2026-044 concerns an outdated image-processing dependency used by the
media-renderer service.

It does not involve account-api, distributed cache, customer profile storage
or session management. It has no known relationship with INC-7782.

---

## SOURCE 9 — Capacity Planning Notes

SOURCE: Platform Engineering
TYPE: planning
AUTHORITY: medium
FRESHNESS: 2026-Q2

Capacity planning discusses CPU headroom, database growth, projected traffic
and quarterly load-test targets.

The document notes that cache efficiency can affect account-api latency under
sustained traffic, but it does not state the root cause of any current incident.

---

## SOURCE 10 — Team Retrospective Notes

SOURCE: Engineering Retrospective
TYPE: team-notes
AUTHORITY: low
FRESHNESS: 2026-08

A retrospective comment says that most account-api latency incidents eventually
turn out to be cache or database related.

This is an informal generalization, not incident-specific evidence. It must not
be used as evidence of the root cause of INC-7782.

The retrospective also discusses on-call handover, dashboard naming, training,
ownership rotation and documentation cleanup.
