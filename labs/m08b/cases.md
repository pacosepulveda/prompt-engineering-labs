# M08B — Release policy and shared cases

## Release Review Policy

SOURCE: Engineering Governance  
AUTHORITY: highest  
STATUS: active

La revisión final combina cuatro gates:

```text
TESTS
ROLLBACK
MONITORING
SECURITY
```

### Ownership de los gates

```text
m08b-operations-reviewer
→ TESTS
→ ROLLBACK
→ MONITORING

m08b-security-reviewer
→ SECURITY

m08b-release-orchestrator
→ combina los informes
→ aplica la decisión final
```

## Reglas

### TESTS

```text
PASS
→ todos los release-blocking tests pasan.

FAIL
→ al menos un release-blocking test falla.

UNKNOWN
→ falta el resultado final.
```

### ROLLBACK

`PASS` cuando:

```text
plan_exists = true
rehearsal_result = PASS
last_rehearsal_days_ago <= 30
```

`FAIL` cuando existe evidencia explícita de incumplimiento.

`UNKNOWN` cuando falta evidencia necesaria.

### MONITORING

`PASS` cuando existen:

```text
dashboard
alerts_enabled = true
owner
```

Usa `FAIL` para un requisito explícitamente incumplido y `UNKNOWN` si falta evidencia.

### SECURITY

La revisión de seguridad es obligatoria cuando cualquier campo del security scope es `true`:

```text
authentication
authorization
credential_lifecycle
secrets
```

Cuando es obligatoria:

```text
PASS
→ review aprobado y sin blockers abiertos.

FAIL
→ review rechazado o existe al menos un blocker abierto.

UNKNOWN
→ resultado final no disponible.
```

Cuando no es obligatoria:

```text
NOT_APPLICABLE
```

## Decisión final

```text
any mandatory FAIL
→ BLOCKED

no FAIL + any mandatory UNKNOWN
→ NEEDS_EVIDENCE

all mandatory gates PASS or NOT_APPLICABLE
→ READY_FOR_HUMAN_REVIEW
```

`READY_FOR_HUMAN_REVIEW` nunca significa aprobación final de producción.

---

# MA-CASE-A — Identity session hardening

```yaml
change_id: MA-810
service: identity-api

security_scope:
  authentication: true
  authorization: false
  credential_lifecycle: true
  secrets: false
```

---

# MA-CASE-B — Payment token refactor

```yaml
change_id: MA-811
service: payments-api

security_scope:
  authentication: false
  authorization: true
  credential_lifecycle: true
  secrets: true
```

---

# MA-CASE-C — Catalog authentication middleware update

```yaml
change_id: MA-812
service: catalog-api

security_scope:
  authentication: true
  authorization: false
  credential_lifecycle: false
  secrets: false
```
