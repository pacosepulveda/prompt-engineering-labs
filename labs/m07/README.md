# M07 — Laboratorio: RAG con corpus amplio, retrieval y contexto eficiente

## Objetivo

En esta práctica vas a trabajar con un sistema RAG local sobre un corpus suficientemente amplio como para que **no tenga sentido enviar toda la base de conocimiento al modelo**.

El flujo será:

```text
corpus
  ↓
metadata filter
  ↓
chunking
  ↓
BM25 retrieval
  ↓
top-k
  ↓
context budget
  ↓
retrieved.md
  ↓
Kiro
  ↓
respuesta grounded
```

La idea central es:

> **RAG no consiste en meter documentos en el prompt; consiste en recuperar únicamente la evidencia necesaria para cada pregunta.**

En este laboratorio verás de forma cuantitativa:

```text
tokens del corpus completo
vs.
tokens candidatos
vs.
tokens realmente enviados a Kiro
```

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
python -m pip install --user -r requirements.txt
./scripts/check-environment.sh
```

Los archivos son:

```text
labs/m07/
├── README.md
├── corpus.jsonl
├── rag.py
└── worksheet.md
```

Los resultados temporales se guardan en:

```text
labs/m07/work/
```

---

# 2. Examinar el tamaño del corpus

Ejecuta:

```bash
python labs/m07/rag.py --stats
```

Debes observar valores equivalentes a:

```text
DOCUMENTS=133
SECTION_CHUNKS=312
ESTIMATED_TOKENS≈16000
```

El número de tokens es una estimación con `o200k_base`; sirve para comparar órdenes de magnitud, no para predecir exactamente la facturación o tokenización de cada modelo.

Abre algunas líneas del corpus:

```bash
head -n 3 labs/m07/corpus.jsonl
```

Cada documento contiene metadata:

```text
DOC_ID
title
service
doc_type
authority
status
date
tags
text
```

El corpus mezcla:

- runbooks;
- políticas;
- documentación histórica;
- postmortems;
- arquitectura;
- capacidad;
- SLO;
- soporte;
- release notes;
- documentación compartida;
- documentos de otros servicios.

Hay ruido deliberado.

---

# 3. Primera recuperación: no pasar todo el corpus

Ejecuta:

```bash
mkdir -p labs/m07/work

python labs/m07/rag.py \
  --query "What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?" \
  --service account-api \
  --active-only \
  --top-k 4 \
  --max-context-tokens 1200 \
  --out labs/m07/work/retrieved.md
```

Observa el bloque:

```text
=== CONTEXT REPORT ===
```

Deberías ver aproximadamente:

```text
CORPUS_DOCUMENTS=133
CORPUS_CHUNKS=312
CORPUS_ESTIMATED_TOKENS≈16000

CANDIDATE_DOCUMENTS≈28
CANDIDATE_CHUNKS≈71

RETRIEVED_CHUNKS=4
RETRIEVED_ESTIMATED_TOKENS≈500

CONTEXT_REDUCTION_VS_CORPUS≈97%
```

No memorices las cifras exactas: pueden variar ligeramente si cambia el corpus o el tokenizer.

La idea es observar esta reducción:

```text
CORPUS COMPLETO
~16000 tokens
      ↓
METADATA FILTER
~4000 tokens candidatos
      ↓
RETRIEVAL + TOP-K + BUDGET
~500 tokens
      ↓
KIRO
```

---

# 4. Inspeccionar exactamente qué recibirá Kiro

Abre:

```bash
cat labs/m07/work/retrieved.md
```

Debe contener únicamente los chunks seleccionados.

No contiene los 133 documentos.

Comprueba que aparece:

```text
DOC-RUNBOOK-014
```

con la evidencia sobre:

- cache eviction rate;
- key churn;
- backend fetch latency;
- recent cache policy changes;
- comparación con baseline;
- cache hit ratio como señal, no causa confirmada.

---

# 5. Generación grounded

Inicia:

```bash
kiro-cli
```

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Answer the question using ONLY:
@labs/m07/work/retrieved.md

Question:
What should we inspect when account-api latency rises
and cache hit ratio falls below 80 percent?

Rules:
- Use only retrieved evidence.
- Cite supporting documents using [DOC_ID].
- Do not use information from the repository outside retrieved.md.
- Do not infer a root cause from a diagnostic signal.
- If the retrieved evidence is insufficient, say INSUFFICIENT_EVIDENCE.

Return:
ANSWER:
SOURCES:
```

La parte importante no es que Kiro conozca el tema.

La parte importante es:

```text
Kiro recibe ~500 tokens relevantes
en lugar de ~16000 tokens de corpus
```

---

# 6. Verificar grounding

Para cada afirmación importante:

```text
claim
→ DOC_ID
→ chunk recuperado
```

Una cita no es evidencia por sí sola.

Debe cumplirse:

```text
documento existe
+
fue recuperado
+
el chunk soporta el claim
```

Registra tres pares claim → fuente en `worksheet.md`.

---

# 7. Metadata filtering también forma parte del retrieval

Ejecuta la misma consulta sin filtro:

```bash
python labs/m07/rag.py \
  --query "What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?" \
  --top-k 4 \
  --max-context-tokens 1200
```

Después con:

```bash
python labs/m07/rag.py \
  --query "What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?" \
  --service account-api \
  --active-only \
  --top-k 4 \
  --max-context-tokens 1200
```

Compara:

```text
CANDIDATE_DOCUMENTS
CANDIDATE_CHUNKS
CANDIDATE_ESTIMATED_TOKENS
ranking
```

Un filtro no genera la respuesta.

Reduce el espacio de búsqueda antes del ranking.

---

# 8. Fuentes contradictorias

Genera contexto sin `--active-only`:

```bash
python labs/m07/rag.py \
  --query "What is the current rollback rehearsal requirement for account-api production changes?" \
  --service account-api \
  --top-k 5 \
  --max-context-tokens 1400 \
  --out labs/m07/work/retrieved.md
```

Deberían aparecer, entre otras:

```text
DOC-POLICY-021
STATUS=ACTIVE
30 days
```

y:

```text
DOC-HANDBOOK-008
STATUS=SUPERSEDED
90 days
```

Pregunta a Kiro:

```text
Use ONLY @labs/m07/work/retrieved.md.

Question:
What is the current rollback rehearsal requirement
for account-api production changes?

Source precedence:
1. ACTIVE beats SUPERSEDED.
2. Higher authority beats lower authority.
3. For equally authoritative active sources, newer date wins.
4. Historical documents may explain history but cannot override current policy.

Return:
ANSWER:
WHY_THIS_SOURCE_WINS:
SOURCES:
```

La respuesta correcta es:

```text
30 days
```

La similarity score ayuda a recuperar.

No decide autoridad.

---

# 9. Cuando la respuesta no existe

Ejecuta:

```bash
python labs/m07/rag.py \
  --query "What is the maximum configured database connection pool size for account-api?" \
  --service account-api \
  --active-only \
  --top-k 4 \
  --max-context-tokens 1200 \
  --out labs/m07/work/retrieved.md
```

El documento relevante explica que ese valor no está definido en la documentación.

Pregunta:

```text
Use ONLY @labs/m07/work/retrieved.md.

Question:
What is the maximum configured database connection pool size for account-api?

If the evidence does not explicitly contain the value, return:

INSUFFICIENT_EVIDENCE

Do not estimate.
Do not use general knowledge.
```

Una cifra plausible sería un fallo.

---

# 10. Top-k frente a contexto

Prueba:

```bash
python labs/m07/rag.py \
  --query "current account-api production rollback rehearsal requirement" \
  --service account-api \
  --top-k 2 \
  --max-context-tokens 1400
```

y después:

```bash
python labs/m07/rag.py \
  --query "current account-api production rollback rehearsal requirement" \
  --service account-api \
  --top-k 8 \
  --max-context-tokens 1400
```

Observa:

```text
RETRIEVED_CHUNKS
RETRIEVED_ESTIMATED_TOKENS
ruido
contradicciones
cobertura
```

Más chunks no implican automáticamente mejor contexto.

---

# 11. Presupuesto de contexto

Mantén `top-k 8` y compara:

```text
--max-context-tokens 500
```

con:

```text
--max-context-tokens 1600
```

El retriever intenta respetar el presupuesto y deja fuera chunks cuando añadirlos excedería el límite.

Esto representa un problema real de RAG:

> **No solo importa qué documentos son relevantes; también debemos decidir cuánto contexto merece entrar en el prompt.**

---

# 12. Query formulation

Compara:

```bash
python labs/m07/rag.py \
  --query "rollback" \
  --top-k 4 \
  --max-context-tokens 1200
```

con:

```bash
python labs/m07/rag.py \
  --query "current account-api production rollback rehearsal requirement" \
  --service account-api \
  --top-k 4 \
  --max-context-tokens 1200
```

Observa cómo:

```text
query
+
metadata
```

cambian el conjunto candidato y el ranking.

---

# 13. Chunking

Compara:

```bash
python labs/m07/rag.py \
  --query "When may Support describe an account-api incident as an outage?" \
  --service account-api \
  --active-only \
  --strategy section \
  --top-k 4
```

con:

```bash
python labs/m07/rag.py \
  --query "When may Support describe an account-api incident as an outage?" \
  --service account-api \
  --active-only \
  --strategy fixed \
  --chunk-words 25 \
  --top-k 4
```

Pregunta:

```text
¿la regla y su excepción siguen juntas?
¿qué chunk es más fácil de citar?
¿qué estrategia usa mejor el presupuesto?
```

No existe un chunk size universal.

---

# 14. Evaluar retrieval por separado

Ejecuta:

```bash
python labs/m07/rag.py \
  --eval \
  --top-k 4 \
  --strategy section \
  --max-context-tokens 1200
```

La configuración de referencia debería alcanzar:

```text
Recall@4 = 1.00
```

en el pequeño conjunto de evaluación incluido.

Esto significa:

```text
la fuente esperada apareció en el contexto recuperado
```

No significa:

```text
la respuesta final es correcta
la cita es fiel
el prompt es perfecto
el sistema está listo para producción
```

---

# 15. ¿Es esto un RAG real?

Sí.

El patrón ejecutado es:

```text
Retrieve
→ Augment
→ Generate
```

No necesita obligatoriamente una base vectorial.

Aquí utilizamos:

```text
metadata filtering
+
BM25 lexical retrieval
+
chunking
+
top-k
+
context budget
```

En una arquitectura de producción podríamos sustituir o ampliar el retriever con:

```text
embeddings
vector search
hybrid lexical + vector
semantic reranking
query rewriting
ACL filters
multiple indexes
```

sin cambiar la idea esencial:

> **el modelo recibe un contexto seleccionado, no la base de conocimiento completa.**

---

# 16. Conclusión

Completa:

```text
labs/m07/worksheet.md
```

Debes poder explicar:

```text
RAG ≠ enviar todo el corpus

retrieval failure ≠ generation failure

metadata filter ≠ ranking

similarity score ≠ authority

citation ≠ proof

top-k alto ≠ mejor

más contexto ≠ mejor contexto

documento recuperado ≠ documento vigente

no-answer = salida válida

token budget = decisión de diseño
```

La idea final es:

> **RAG es context engineering dinámico: recuperar, seleccionar y presupuestar la evidencia que realmente necesita cada consulta.**
