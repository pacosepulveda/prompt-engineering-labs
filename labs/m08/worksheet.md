# M08 — Hoja de trabajo

## 1. Baseline

```text
Formato:
Criterios utilizados:
¿Separó evidencia/suposiciones?:
¿Intentó autorizar deployment?:
Variabilidad o ambigüedad observada:
```

## 2. Agent configuration

```text
PROMPT define:
TOOLS disponibles:
ALLOWED TOOLS:
RESOURCES:
MODEL fijado:
```

## 3. Casos

| Caso | Decisión esperada | Decisión obtenida | Correcto |
|---|---|---|---|
| CASE-A | | | |
| CASE-B | | | |
| CASE-C | | | |

## 4. State

```text
¿Apareció contaminación al pasar de CASE-A a CASE-C en el mismo chat?:
¿Cambió al utilizar /chat new?:
¿Qué estado conservarías?:
¿Qué estado aislarías?:
```

## 5. Tool surface

```text
Petición de modificación:
¿Pudo ejecutarla?:
Respuesta del agente:
¿Por qué limitar tools es más fuerte que una instrucción "no modifiques"?:
```

## 6. Human gate

```text
CASE-B:
Resultado automático:
Decisión que sigue siendo humana:
¿Por qué?:
```

## 7. Diseño

| Requisito | Categoría |
|---|---|
| A — No autorizar producción | |
| B — Ruff + pytest en todos los repos Python | |
| C — Método reusable de PR review | |
| D — Consultar CI real | |
| E — Resultado de tests actual | |
| F — Aprobar producción | |
| G — Security review especializada paralela | |

## 8. Variante security-reviewer

```text
PURPOSE:
TOOLS:
RESOURCES:
AUTHORITY:
OUTPUT:
HUMAN_GATE:
```

## 9. Cambio propuesto al agente

```text
Propuesta:
"Si falta una sola evidencia, asumir PASS si el cambio parece de bajo riesgo."

¿Aceptarías?:
Por qué:
Regression cases:
Quién debe revisarlo:
```

## 10. Conclusión

```text
Agent ≠
Skill ≠
MCP ≠
Runtime state ≠
READY_FOR_HUMAN_REVIEW ≠
Subagent merece la pena cuando...
```
