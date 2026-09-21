# Release Readiness Policy

Política ficticia para uso formativo.

## Resultado permitido

```text
READY
BLOCKED
NEEDS_EVIDENCE
```

La salida es una recomendación para revisión humana. No autoriza el despliegue.

## Gates obligatorios

### Gate A — Release-blocking tests
PASS si no hay tests release-blocking fallidos. FAIL si existe al menos uno. UNKNOWN sin detalle suficiente.

### Gate B — Known issues
PASS si no existen issues relacionados Sev1/Sev2 abiertos. FAIL si existe alguno. UNKNOWN sin evidencia.

### Gate C — Rollback readiness
PASS si existe plan, se ensayó hace 30 días o menos y el rehearsal pasó. FAIL si hay evidencia explícita de incumplimiento. UNKNOWN si falta evidencia.

### Gate D — Monitoring readiness
PASS si existe dashboard, alertas activas y owner. FAIL si existe evidencia de que monitoring no está preparado. UNKNOWN si faltan datos.

### Gate E — Security review
Obligatorio si el cambio afecta autenticación, autorización, secretos o lifecycle de tokens/credenciales.

Cuando aplica:
- PASS si está aprobado y sin blockers abiertos;
- FAIL si está rechazado o existen blockers;
- UNKNOWN si no se dispone del resultado.

Cuando no aplica: NOT_APPLICABLE.

## Regla de decisión

```text
1. Si algún gate obligatorio = FAIL
   → BLOCKED

2. Si no existe FAIL y algún gate obligatorio = UNKNOWN
   → NEEDS_EVIDENCE

3. Si todos los gates obligatorios = PASS
   → READY
```

NOT_APPLICABLE no bloquea.

## Evidencia

No conviertas “tests executed”, “rollback documented”, “security review requested” o “monitoring exists” en PASS sin la evidencia requerida.

No completes información ausente mediante suposiciones.

## Siguiente paso

La IA puede recomendar obtener evidencia, corregir un gate fallido, repetir pruebas o solicitar nueva revisión.

No puede autorizar el deployment, ejecutar el cambio, modificar la política ni ignorar un gate.
