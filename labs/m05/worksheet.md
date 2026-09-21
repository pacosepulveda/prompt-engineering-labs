# M05 — Hoja de trabajo

## Modelo utilizado

```text
Modelo:
```

---

# 1. Baseline

```text
FULL reference tokens:

FAST single-request cost:

FAST estimated TTFT:

10-turn uncached cost:

10-turn cached-prefix cost:
```

## Calidad baseline

| Criterio | 0/1 |
|---|---:|
| Current status | |
| Grounding | |
| Freshness | |
| RCA discipline | |
| Support message | |
| **Total /5** | |

---

# 2. Context classification

```text
KEEP:


COMPRESS:


DROP:


Sección con mayor riesgo de contaminación:
```

---

# 3. Context optimizado

```text
OPTIMIZED reference tokens:

Reducción %:

FAST single-request cost:

FAST estimated TTFT:

10-turn uncached cost:

10-turn cached-prefix cost:
```

## Calidad optimizada

| Criterio | 0/1 |
|---|---:|
| Current status | |
| Grounding | |
| Freshness | |
| RCA discipline | |
| Support message | |
| **Total /5** | |

```text
¿Se mantuvo la calidad?:

¿Qué información eliminaste sin pérdida?:

¿Qué información no podías eliminar?:
```

---

# 4. Caching

```text
STATIC:


DYNAMIC:


¿Por qué el bloque STATIC es mejor candidato para caching?:
```

---

# 5. Routing

```text
Tarea A — extracción:
Perfil elegido:
Justificación:


Tarea B — análisis:
Perfil elegido:
Justificación:
```

---

# 6. Unit economics

```text
Requests/day: 5000
Days/month: 30
Requests/month: 150000

FULL monthly cost:

OPTIMIZED monthly cost:

Estimated saving:
```

---

# 7. Conclusión

```text
Mayor fuente de ahorro observada:


Principal riesgo de un contexto demasiado grande:


Diferencia entre pruning y caching:


Métrica de calidad que mantendrías en producción:


¿Qué significa para ti "calidad suficiente por unidad de coste y latencia"?:
```
