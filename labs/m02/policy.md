# Network Operations — Triage Policy

Política ficticia para uso formativo.

## P1 — Critical

Clasifica como `P1` si se cumple al menos una:

1. `service_status = unavailable`
2. `affected_sites >= 3`
3. `packet_loss >= 15%` **y** `duration_minutes >= 5`

## P2 — Major

Si no existe ninguna condición P1, clasifica como `P2` si se cumple al menos una:

1. `packet_loss >= 5%`
2. `p95_latency_ms > 1.25 × sla_latency_ms` **y** `user_impact = confirmed`

## P3 — Minor

Utiliza `P3` únicamente cuando existen datos suficientes para descartar P1/P2 y la incidencia sigue abierta con servicio disponible o degradado.

`P3` no es una categoría por defecto cuando faltan datos críticos.

## UNDETERMINED

Utiliza `UNDETERMINED` cuando faltan datos necesarios para aplicar o descartar razonablemente P1/P2.

## Root Cause

Solo puede afirmarse una causa raíz cuando:

```text
rca_status = confirmed
```

Una sospecha o nota no confirmada puede mencionarse únicamente como hipótesis.

## NEXT_CHECK

Debe ser una acción diagnóstica y reversible.

No recomendar:

- reinicios;
- rollbacks;
- cambios de configuración;
- cambios de routing;
- despliegues;
- modificaciones del servicio.
