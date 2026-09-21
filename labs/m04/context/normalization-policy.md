# Incident Normalization Policy

Política ficticia para uso formativo.

## 1. Grounding

Utiliza únicamente información contenida en el ticket.

No inventes causas, owners, métricas, entornos o servicios.

## 2. Cause

`suspected_cause` debe ser `null` salvo que el ticket indique explícitamente que la causa está confirmada.

Expresiones como "maybe", "suspect", "probably" o "looks like" no confirman una causa.

## 3. Severity

### P1
Production + servicio completamente unavailable + affected_users >= 100.

### P2
Production + impacto funcional confirmado + affected_users >= 25, sin cumplir P1.

### P3
Impacto funcional limitado que no alcanza P1/P2.

### P4
Problema informativo o cosmético sin impacto funcional.

### UNDETERMINED
No hay evidencia suficiente para clasificar.

## 4. Missing fields

Añade a `missing_fields` información relevante ausente que impida una decisión operativa razonable, como `service`, `environment` o `affected_users`.

## 5. Sensitive data

Considera sensitive data passwords, bearer tokens, API keys y private credentials.

Si aparece:

```text
contains_sensitive_data = true
recommended_action = escalate_security
```

No reproduzcas el valor secreto en ningún campo.

## 6. Recommended action

Valores permitidos:

- `request_more_info`: falta información operativa esencial.
- `open_bug`: defecto suficientemente descrito sin necesidad de escalado de seguridad.
- `escalate_security`: aparece información sensible o indicador explícito de seguridad.
- `route_to_service_owner`: existe suficiente información para identificar el servicio y debe enrutarse al owner.

## 7. Evidence

Cada elemento debe corresponder a un hecho presente en el ticket.

No introducir inferencias como si fueran evidencias.
