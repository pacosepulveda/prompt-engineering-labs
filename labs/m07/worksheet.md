# M07 — Hoja de trabajo

## 1. Retrieval inicial

```text
Consulta:

Top-k:

Primer documento recuperado:

¿Contiene la evidencia necesaria?:

¿Aparecen documentos irrelevantes?:

¿La evidencia recuperada es suficiente?:
```

---

## 2. Grounding

```text
Claim 1:
Fuente:

Claim 2:
Fuente:

Claim 3:
Fuente:

¿Alguna cita no soporta realmente la afirmación?:
```

---

## 3. Conflicto de fuentes

```text
Fuente vigente:

Fuente superseded/histórica:

Regla aplicada para resolver el conflicto:

Respuesta final:
```

---

## 4. No-answer

```text
Pregunta:

¿Existe la respuesta explícita en el contexto recuperado?:

¿El modelo se abstuvo?:

¿Qué dato faltaba?:
```

---

## 5. Query formulation

```text
Consulta genérica:

Consulta específica:

¿Qué cambió en el ranking?:

¿Qué consulta utilizarías y por qué?:
```

---

## 6. Top-k

| top-k | Evidencia necesaria | Ruido | Observaciones |
|---:|---|---|---|
| 1 | | | |
| 3 | | | |
| 5 | | | |

```text
Top-k elegido:
Justificación:
```

---

## 7. Chunking

```text
Section chunks:

Fixed chunks:

¿Alguna regla quedó partida?:

Estrategia preferida:

Justificación:
```

---

## 8. Evaluación

```text
Configuración inicial:
strategy =
top-k =
chunk-words =

Recall@k:
```

```text
Configuración alternativa:
strategy =
top-k =
chunk-words =

Recall@k:

¿Mejoró retrieval?:

¿Aumentó el contexto/ruido?:
```

---

## 9. Diagnóstico

```text
Ejemplo de retrieval failure:


Ejemplo de generation failure:
```

---

## 10. Conclusión

Completa:

```text
Retrieval failure ≠

Similarity score ≠

Citation ≠

Top-k alto ≠

Documento recuperado ≠

No-answer es válido cuando...
```
