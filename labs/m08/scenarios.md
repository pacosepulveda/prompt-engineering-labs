# Release Review Standard and Scenarios

## Release Review Policy

SOURCE: Engineering Governance
AUTHORITY: highest
STATUS: active

A release review evaluates four mandatory gates:

```text
TESTS
ROLLBACK
MONITORING
SECURITY
```

### TESTS

`PASS` when all release-blocking tests pass.

`FAIL` when at least one release-blocking test fails.

`UNKNOWN` when detailed results are unavailable.

### ROLLBACK

`PASS` when:
- rollback plan exists;
- latest rehearsal passed;
- rehearsal occurred within the previous 30 days.

Otherwise use `FAIL` if evidence explicitly violates a requirement, or `UNKNOWN` if evidence is missing.

### MONITORING

`PASS` when:
- dashboard exists;
- alerts are enabled;
- an owner is identified.

### SECURITY

Security review is mandatory when the change affects authentication, authorization, credential lifecycle or secrets.

When mandatory:
- `PASS` → approved review with no open blockers
- `FAIL` → rejected review or open blocker
- `UNKNOWN` → review result unavailable

When not mandatory:
- `NOT_APPLICABLE`

## Decision Rule

```text
any mandatory FAIL
→ BLOCKED

no FAIL + any mandatory UNKNOWN
→ NEEDS_EVIDENCE

all mandatory gates PASS or NOT_APPLICABLE
→ READY_FOR_HUMAN_REVIEW
```

`READY_FOR_HUMAN_REVIEW` is not production approval.

Final production approval is always a human decision.

---

# CASE-A — Authentication cache change

```yaml
change_id: CHG-810
service: identity-api

security_scope:
  authentication: true
  authorization: false
  credential_lifecycle: true
  secrets: false

tests:
  release_blocking: PASS

rollback:
  plan_exists: true
  rehearsal_result: PASS
  last_rehearsal_days_ago: 9

monitoring:
  dashboard: identity-api-auth
  alerts_enabled: true
  owner: identity-sre

security_review:
  status: not_provided
```

---

# CASE-B — Static frontend asset change

```yaml
change_id: CHG-811
service: web-portal

security_scope:
  authentication: false
  authorization: false
  credential_lifecycle: false
  secrets: false

tests:
  release_blocking: PASS

rollback:
  plan_exists: true
  rehearsal_result: PASS
  last_rehearsal_days_ago: 4

monitoring:
  dashboard: web-frontend
  alerts_enabled: true
  owner: web-experience

security_review:
  status: NOT_APPLICABLE
```

---

# CASE-C — Billing API refactor

```yaml
change_id: CHG-812
service: billing-api

security_scope:
  authentication: false
  authorization: false
  credential_lifecycle: false
  secrets: false

tests:
  release_blocking: UNKNOWN
  note: "The pipeline was started but the final test summary is not attached."

rollback:
  plan_exists: true
  rehearsal_result: PASS
  last_rehearsal_days_ago: 14

monitoring:
  dashboard: billing-api
  alerts_enabled: true
  owner: payments-platform

security_review:
  status: NOT_APPLICABLE
```
