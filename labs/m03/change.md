# Cambios — M03

## CHG-482 — Token refresh cache update

```yaml
change_id: CHG-482
service: account-api
component: token-refresh-cache
production_target: true

summary:
  - "Reduce repeated token refresh lookups by caching token lifecycle metadata."
  - "Changes refresh-token handling after idle sessions."

security_scope:
  authentication: true
  authorization: false
  secrets: false
  token_lifecycle: true

tests:
  status: executed
  detailed_results: external

rollback:
  plan: documented
  rehearsal_evidence: external

monitoring:
  dashboard: referenced
  detailed_status: external

security_review:
  review_id: SEC-884
  status: external

known_issues:
  status: external
```

---

## CHG-530 — Login session timeout update

```yaml
change_id: CHG-530
service: customer-portal
component: session-policy
production_target: true

security_scope:
  authentication: true
  authorization: false
  secrets: false
  token_lifecycle: true

release_blocking_tests:
  status: PASS

known_issues:
  sev1_open: 0
  sev2_open: 0

rollback:
  plan_exists: true
  last_rehearsal_days_ago: 5
  result: PASS

monitoring:
  dashboard: customer-login
  alerts_enabled: true
  owner: portal-sre
  status: PASS

security_review:
  status: not_provided
```
