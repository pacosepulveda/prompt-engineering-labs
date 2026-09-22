# M08B — Security specialist evidence

Este documento pertenece al dominio de Security.

El agente `m08b-security-reviewer` debe tratarlo como evidencia especializada.

---

# MA-CASE-A

```yaml
security_review:
  review_id: SEC-MA-210
  status: PASS
  open_blockers: 0
  scope_reviewed:
    - authentication
    - credential_lifecycle
```

---

# MA-CASE-B

```yaml
security_review:
  review_id: SEC-MA-211
  status: FAIL
  open_blockers: 1
  blocker:
    id: SEC-991
    description: "Token scope escalation can grant an unintended payments:write permission."
```

---

# MA-CASE-C

```yaml
security_review:
  review_id: SEC-MA-212
  status: PASS
  open_blockers: 0
  scope_reviewed:
    - authentication
```
