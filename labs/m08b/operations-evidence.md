# M08B — Operations specialist evidence

Este documento pertenece al dominio de Operations.

El agente `m08b-operations-reviewer` debe tratarlo como evidencia especializada.

---

# MA-CASE-A

```yaml
tests:
  release_blocking: PASS

rollback:
  plan_exists: true
  rehearsal_result: PASS
  last_rehearsal_days_ago: 7

monitoring:
  dashboard: identity-session-health
  alerts_enabled: true
  owner: identity-sre
```

---

# MA-CASE-B

```yaml
tests:
  release_blocking: PASS

rollback:
  plan_exists: true
  rehearsal_result: PASS
  last_rehearsal_days_ago: 12

monitoring:
  dashboard: payments-token-health
  alerts_enabled: true
  owner: payments-platform
```

---

# MA-CASE-C

```yaml
tests:
  release_blocking: UNKNOWN
  note: "The pipeline completed, but the final release-blocking test summary is not attached."

rollback:
  plan_exists: true
  rehearsal_result: PASS
  last_rehearsal_days_ago: 6

monitoring:
  dashboard: catalog-auth
  alerts_enabled: true
  owner: catalog-platform
```
