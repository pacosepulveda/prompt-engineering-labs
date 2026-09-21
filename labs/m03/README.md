# M03 — Laboratorio: Elegir la técnica adecuada

## Objetivo

En esta práctica vas a comparar varias técnicas avanzadas sobre **el mismo problema**.

La regla será:

> **No añadir complejidad si no resuelve un fallo observable.**

Trabajaremos con:

```text
zero-shot
→ few-shot
→ decomposition
→ tool result
→ candidatos
→ critique & revision
→ regression check
```

---

## Entorno

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

Mantén el mismo modelo durante las comparaciones.

Antes de ejecuciones independientes:

```text
/chat new
```

---

# 1. Escenario

Debes revisar si un cambio puede considerarse listo para producción.

Los cambios están en:

```text
labs/m03/change.md
```

El resultado permitido es:

```text
READY
BLOCKED
NEEDS_EVIDENCE
```

La IA prepara una recomendación para revisión humana. No autoriza el despliegue.

---

# 2. Política

Utiliza esta política durante la práctica.

## Gates obligatorios

### Tests

```text
PASS  → no hay tests release-blocking fallidos
FAIL  → existe al menos uno
UNKNOWN → no hay resultado detallado
```

### Known issues

```text
PASS  → no hay Sev1/Sev2 abiertos relacionados
FAIL  → existe al menos uno
UNKNOWN → falta evidencia
```

### Rollback

`PASS` si:

- existe plan;
- rehearsal correcto;
- realizado hace 30 días o menos.

### Monitoring

`PASS` si existen:

- dashboard;
- alertas activas;
- owner.

### Security review

Es obligatorio si el cambio afecta a:

- autenticación;
- autorización;
- secretos;
- lifecycle de tokens.

## Regla de decisión

```text
si existe algún FAIL
→ BLOCKED

si no existe FAIL pero hay algún UNKNOWN obligatorio
→ NEEDS_EVIDENCE

si todos los gates obligatorios son PASS
→ READY
```

---

# 3. Zero-shot

En una conversación nueva:

```text
Revisa CHG-482 de @labs/m03/change.md y dime si está listo para producción.
```

Anota:

- recomendación;
- criterio utilizado;
- supuestos;
- si la decisión es auditable.

Ahora repite incluyendo la política anterior.

Pregunta:

> ¿La mejora procede de una técnica sofisticada o simplemente de haber definido qué significa “ready”?

---

# 4. Few-shot

## Ejemplos pobres

Utiliza estos ejemplos:

```text
Ejemplo 1:
Tests PASS, rollback PASS, monitoring PASS → READY

Ejemplo 2:
Tests PASS, rollback PASS, monitoring PASS → READY

Ejemplo 3:
Tests PASS, rollback PASS, monitoring PASS → READY
```

Pide después la revisión de `CHG-482`.

Observa si la colección introduce un sesgo accidental.

## Ejemplos representativos

Sustituye los anteriores por:

```text
Ejemplo A:
Todos los gates obligatorios PASS → READY

Ejemplo B:
Un test release-blocking FAIL → BLOCKED

Ejemplo C:
Cambio de autenticación sin resultado de security review → NEEDS_EVIDENCE

Ejemplo D:
Rollback rehearsal de hace 31 días → BLOCKED
```

Repite la revisión.

Pregunta:

> ¿Qué puede enseñar few-shot y qué información no puede inventar?

---

# 5. Decomposition

En una conversación nueva:

```text
Analiza CHG-482 de @labs/m03/change.md utilizando la política.

No emitas todavía recomendación final.

Devuelve solo:

FACTS:
- hechos explícitos

GATES:
- gate: PASS | FAIL | UNKNOWN
  evidence: ...

MISSING_EVIDENCE:
- evidencia necesaria para resolver UNKNOWN relevantes
```

Compara con el prompt monolítico.

La pregunta no es solo:

> ¿respondió mejor?

También:

> ¿es ahora más fácil localizar por qué falla?

---

# 6. Obtener evidencia externa

El cambio hace referencia a sistemas externos.

Ejecuta:

```bash
python labs/m03/tool.py CHG-482
```

El script devuelve evidencia read-only simulada.

Copia el resultado y entrégaselo al modelo:

```text
TOOL_RESULT:
[PEGA AQUÍ LA SALIDA]

Reevalúa los gates aplicando exactamente la política.

Devuelve:
RECOMMENDATION:
GATES:
EVIDENCE:
NEXT_STEP:
```

Anota:

- qué gate cambió;
- si la recomendación cambió;
- qué evidencia concreta provocó el cambio.

---

# 7. Dos candidatos independientes

Crea dos conversaciones nuevas.

En ambas utiliza exactamente:

- la misma política;
- `CHG-482`;
- el mismo `TOOL_RESULT`;
- el mismo modelo.

Genera:

```text
Candidate A
Candidate B
```

con:

```text
RECOMMENDATION:
GATES:
EVIDENCE:
NEXT_STEP:
```

---

# 8. Critique con rúbrica

Evalúa ambos candidatos con esta rúbrica:

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| Policy accuracy | incorrecto | error menor | correcto |
| Grounding | inventa | soporte parcial | todo verificable |
| Missing data | incorrecto | menor omisión | correcto |
| Action safety | fuera de alcance | vaga | segura y concreta |
| Clarity | difícil de auditar | suficiente | claramente auditable |

Pide al modelo:

```text
Evalúa Candidate A y Candidate B con la rúbrica.

No generes una nueva respuesta.

Devuelve para cada candidato:
SCORE:
CONFIRMED_DEFECTS:
NO_CHANGE_NEEDED:
```

No elijas por estilo o longitud.

---

# 9. Critique & Revision

Escoge el candidato con mejor resultado verificable.

Pide:

```text
Corrige únicamente los defectos confirmados.

Conserva lo que ya cumple.

Devuelve:
RECOMMENDATION:
GATES:
EVIDENCE:
NEXT_STEP:
```

Compara antes y después.

Pregunta:

> ¿la revisión mejora exactitud o solo hace la respuesta más convincente?

---

# 10. Regression check

En el mismo archivo:

```text
labs/m03/change.md
```

encontrarás `CHG-530`.

Utiliza el procedimiento final que has construido.

Comprueba si:

- aplica correctamente la política;
- distingue `UNKNOWN` de `FAIL`;
- evita convertirse en un sistema que responde siempre `BLOCKED`.

---

# 11. Conclusión

Completa:

```text
labs/m03/worksheet.md
```

Debes poder explicar:

- cuándo zero-shot era suficiente;
- qué aportó few-shot;
- qué aportó decomposition;
- qué cambió al introducir evidencia externa;
- por qué dos candidatos coincidentes no demuestran verdad;
- por qué critique necesita una rúbrica;
- qué técnica eliminarías si no aportara mejora medible.
