# M07 — Hoja de trabajo

## 1. Corpus

```text
Documentos:

Chunks:

Tokens estimados del corpus:
```

---

## 2. Primera recuperación

```text
Consulta:

Filtro service:

Active only:

Top-k:

Context budget:

Candidate documents:

Candidate chunks:

Retrieved chunks:

Retrieved tokens:

Reducción frente al corpus:

Primer documento:
```

---

## 3. Grounding

```text
Claim 1:
Fuente:

Claim 2:
Fuente:

Claim 3:
Fuente:

¿Alguna cita no soporta el claim?:
```

---

## 4. Metadata filtering

| Ejecución | Candidate docs | Candidate chunks | Candidate tokens | Primer resultado |
|---|---:|---:|---:|---|
| Sin filtro | | | | |
| service=account-api + ACTIVE | | | | |

```text
¿Qué aporta el filtro?:
```

---

## 5. Conflicto de fuentes

```text
Fuente ACTIVE:

Regla actual:

Fuente SUPERSEDED:

Regla histórica:

¿Por qué gana la fuente actual?:
```

---

## 6. No-answer

```text
Pregunta:

Documento principal recuperado:

¿El valor solicitado aparece?:

Respuesta correcta:

¿Por qué una cifra plausible sería un fallo?:
```

---

## 7. Top-k

| top-k | Retrieved chunks | Retrieved tokens | Evidencia | Ruido |
|---:|---:|---:|---|---|
| 2 | | | | |
| 4 | | | | |
| 8 | | | | |

```text
Top-k preferido:
Justificación:
```

---

## 8. Context budget

| Max context tokens | Chunks incluidos | Tokens reales del paquete | Observaciones |
|---:|---:|---:|---|
| 500 | | | |
| 1200 | | | |
| 1600 | | | |

```text
¿Qué puede ocurrir con un presupuesto demasiado bajo?:

¿Qué puede ocurrir con uno demasiado alto?:
```

---

## 9. Query + metadata

```text
Consulta genérica:

Consulta específica:

Filtros:

¿Qué cambió?:
```

---

## 10. Chunking

```text
Section:

Fixed:

¿Alguna regla/excepción quedó separada?:

Estrategia elegida:

Justificación:
```

---

## 11. Evaluación

```text
Strategy:

Top-k:

Context budget:

Recall@k:

¿Qué mide?:

¿Qué NO mide?:
```

---

## 12. Diagnóstico

```text
Ejemplo de retrieval failure:

Ejemplo de generation failure:

¿Cómo distinguirlos?:
```

---

## 13. Conclusión

Completa:

```text
RAG ≠

Retrieval failure ≠

Metadata filter ≠

Similarity score ≠

Citation ≠

Top-k alto ≠

Más contexto ≠

Documento recuperado ≠

No-answer es válido cuando...

Token budget sirve para...
```
