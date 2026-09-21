# Network Operations — Triage Policy

Esta política es ficticia y se utiliza únicamente con fines formativos.

## 1. Principio general

Selecciona la **severidad más alta** cuya condición esté explícitamente satisfecha por los datos de la incidencia.

No completes datos ausentes mediante suposiciones.

---

## 2. P1 — Critical

Clasifica como `P1` si se cumple **al menos una** de estas condiciones:

1. `service_status = unavailable`
2. `affected_sites >= 3`
3. `packet_loss >= 15%` **y** `duration_minutes >= 5`

---

## 3. P2 — Major

Si no se cumple ninguna condición P1, clasifica como `P2` cuando se cumple **al menos una**:

1. `packet_loss >= 5%`
2. `p95_latency_ms > 1.25 × sla_latency_ms` **y** `user_impact = confirmed`

---

## 4. P3 — Minor

Si se dispone de datos suficientes para descartar P1 y P2, utiliza `P3` para una incidencia abierta con servicio disponible o degradado que no alcance los umbrales anteriores.

`P3` **no es una categoría por defecto cuando faltan datos críticos**.

---

## 5. UNDETERMINED

Utiliza `UNDETERMINED` cuando no existan datos suficientes para aplicar o descartar de forma razonable las reglas P1/P2.

No conviertas un reporte no confirmado en una métrica confirmada.

---

## 6. Root Cause

Solo puede afirmarse una causa raíz cuando:

```text
rca_status = confirmed
```

Notas, sospechas, comentarios de campo o hipótesis pueden mencionarse únicamente como información no confirmada.

---

## 7. Siguiente comprobación

`NEXT_CHECK` debe ser una acción:

- diagnóstica;
- reversible;
- de lectura u observación.

Ejemplos válidos:

- consultar telemetría;
- revisar contadores;
- comparar con una línea base;
- comprobar el estado de una dependencia;
- obtener una métrica ausente.

No recomendar como `NEXT_CHECK`:

- reinicios;
- rollbacks;
- cambios de configuración;
- cambios de routing;
- despliegues;
- acciones físicas;
- cualquier modificación del servicio.

---

## 8. Grounding

La clasificación y la evidencia deben basarse únicamente en:

1. esta política;
2. los datos de la incidencia suministrada.

No utilices supuestos externos para reemplazar datos ausentes.
