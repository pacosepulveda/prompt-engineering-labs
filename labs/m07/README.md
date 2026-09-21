# M07 — Laboratorio: RAG, retrieval y respuestas con evidencia

## Objetivo

En esta práctica vas a construir el flujo esencial de un sistema RAG sin depender de una base vectorial ni de servicios externos.

Trabajaremos con:

```text
pregunta
   ↓
retrieval
   ↓
chunks recuperados
   ↓
LLM
   ↓
respuesta con fuentes
```

El objetivo no es “meter documentos en el prompt”.

Queremos comprobar:

```text
¿recuperamos la evidencia correcta?
¿podemos citarla?
¿sabemos abstenernos si no está?
¿qué hacemos cuando las fuentes se contradicen?
¿cómo afectan chunking y top-k?
```

La idea central es:

> **Una respuesta RAG no puede ser mejor que la evidencia que recupera.**

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
```

Los archivos del laboratorio son:

```text
labs/m07/
├── README.md
├── knowledge.md
├── rag.py
└── worksheet.md
```

El script utiliza únicamente la librería estándar de Python.

---

# 2. La base de conocimiento

Abre:

```text
labs/m07/knowledge.md
```

Contiene documentación ficticia de operaciones:

- políticas actuales;
- runbooks;
- documentación histórica;
- postmortems;
- notas de producto;
- documentación de soporte.

Cada documento incluye:

```text
DOC_ID
AUTHORITY
DATE
STATUS
```

Estos metadatos serán importantes más adelante.

---

# 3. Retrieval antes de generación

Ejecuta:

```bash
python labs/m07/rag.py   --query "What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?"   --top-k 3
```

No preguntes todavía al LLM.

Observa:

```text
rank
score
DOC_ID
authority
date
chunk
```

Responde en `worksheet.md`:

```text
¿El primer chunk contiene la evidencia necesaria?

¿Aparecen documentos irrelevantes?

¿La información recuperada es suficiente para contestar?
```

Este paso separa dos problemas que suelen confundirse:

```text
retrieval quality
≠
generation quality
```

---

# 4. Crear una respuesta grounded

Genera un archivo de contexto recuperado:

```bash
mkdir -p labs/m07/work

python labs/m07/rag.py   --query "What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?"   --top-k 3   --out labs/m07/work/retrieved.md
```

Inicia Kiro:

```bash
kiro-cli
```

y utiliza:

```text
/chat new
```

Prompt:

```text
Answer the question using ONLY:
@labs/m07/work/retrieved.md

Question:
What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?

Rules:
- Use only retrieved evidence.
- Cite supporting documents using [DOC_ID].
- Do not cite a source that does not support the statement.
- If the evidence is insufficient, say INSUFFICIENT_EVIDENCE.
- Do not infer a root cause from a diagnostic signal.

Return:
ANSWER:
SOURCES:
```

Comprueba que las citas corresponden realmente a los chunks recuperados.

---

# 5. Una respuesta con cita incorrecta sigue siendo incorrecta

No basta con que el modelo produzca:

```text
[DOC-123]
```

La cita debe cumplir:

```text
la fuente existe
+
fue recuperada
+
contiene evidencia para esa afirmación
```

Revisa cada afirmación importante de la respuesta.

Anota:

```text
Claim 1 → fuente
Claim 2 → fuente
Claim 3 → fuente
```

Si no puedes hacer esa correspondencia, la respuesta no está realmente grounded.

---

# 6. Fuentes contradictorias

Ahora ejecuta:

```bash
python labs/m07/rag.py   --query "What is the current rollback rehearsal requirement for account-api production changes?"   --top-k 4   --out labs/m07/work/retrieved.md
```

Abre:

```text
labs/m07/work/retrieved.md
```

Deberías encontrar documentación que no dice exactamente lo mismo.

Pregunta a Kiro:

```text
Use ONLY @labs/m07/work/retrieved.md.

Question:
What is the current rollback rehearsal requirement for account-api production changes?

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

### Pregunta

¿Debe el sistema:

```text
A) combinar ambas reglas
B) elegir la fuente vigente
C) elegir la que aparece primero
D) elegir la que tenga mayor similarity score
```

Justifica tu respuesta.

---

# 7. Cuando la respuesta no existe

Ejecuta:

```bash
python labs/m07/rag.py   --query "What is the maximum configured database connection pool size for account-api?"   --top-k 3   --out labs/m07/work/retrieved.md
```

Ahora:

```text
Use ONLY @labs/m07/work/retrieved.md.

Question:
What is the maximum configured database connection pool size for account-api?

If the retrieved evidence does not explicitly contain the answer, return:

INSUFFICIENT_EVIDENCE

Do not estimate.
Do not use general knowledge.
```

La respuesta correcta debe depender de la evidencia, no de la capacidad general del modelo para producir una cifra plausible.

---

# 8. Query formulation también forma parte del sistema

Compara:

```bash
python labs/m07/rag.py   --query "rollback"   --top-k 3
```

con:

```bash
python labs/m07/rag.py   --query "current account-api production rollback rehearsal requirement"   --top-k 3
```

Observa:

- ranking;
- scores;
- documentos recuperados.

### Pregunta

¿El problema está siempre en:

```text
documentos
```

o puede estar también en:

```text
la consulta utilizada para retrieval
```

---

# 9. Top-k: recall frente a ruido

Ejecuta la misma consulta con:

```bash
--top-k 1
```

y:

```bash
--top-k 5
```

Compara.

Un `top-k` mayor puede:

```text
+ aumentar probabilidad de recuperar la evidencia
- introducir más ruido
- aumentar contexto
- introducir contradicciones
```

Un `top-k` menor puede:

```text
+ ser más preciso
- perder una fuente necesaria
```

No existe un valor universal.

---

# 10. Chunking

Hasta ahora hemos utilizado:

```text
--strategy section
```

que conserva secciones semánticas del documento.

Compara con:

```bash
python labs/m07/rag.py   --query "When may Support describe an account-api incident as an outage?"   --top-k 3   --strategy fixed   --chunk-words 55
```

y:

```bash
python labs/m07/rag.py   --query "When may Support describe an account-api incident as an outage?"   --top-k 3   --strategy section
```

Observa:

- coherencia de los chunks;
- si una regla queda partida;
- cantidad de contexto necesario;
- facilidad para citar.

La pregunta no es:

> ¿qué chunk size es siempre mejor?

Sino:

> ¿qué unidad de información necesita esta colección documental?

---

# 11. Evaluar retrieval por separado

El script incluye un pequeño conjunto de consultas con documento esperado.

Ejecuta:

```bash
python labs/m07/rag.py   --eval   --top-k 3   --strategy section
```

Obtendrás una métrica:

```text
Recall@3
```

Esto evalúa:

```text
¿apareció una fuente relevante entre los primeros resultados?
```

No evalúa:

- calidad de redacción;
- exactitud completa de la respuesta;
- fidelidad de las citas;
- utilidad para el usuario.

Por tanto, en un sistema RAG necesitamos evaluar al menos dos capas:

```text
retrieval
generation
```

---

# 12. Un pequeño test de regresión

Cambia:

```text
--top-k
--strategy
--chunk-words
```

y vuelve a ejecutar:

```bash
python labs/m07/rag.py --eval ...
```

Busca una configuración que:

- mantenga buen Recall@k;
- produzca chunks comprensibles;
- no recupere contexto excesivo.

Anota tu decisión.

---

# 13. ¿Por qué esto sigue siendo RAG sin embeddings?

Nuestro retriever utiliza ranking léxico BM25.

El patrón sigue siendo:

```text
Retrieve
→ Augment
→ Generate
```

En un sistema real podríamos sustituir el retriever por:

```text
embeddings + vector search
hybrid lexical + vector
reranking
metadata filters
```

sin cambiar el principio fundamental:

> **primero recuperamos evidencia; después generamos sobre esa evidencia.**

---

# 14. Conclusión

Completa:

```text
labs/m07/worksheet.md
```

Debes poder explicar:

```text
retrieval failure ≠ generation failure
similarity score ≠ authority
citation ≠ proof
top-k alto ≠ mejor
chunk pequeño ≠ mejor
documento recuperado ≠ documento vigente
no-answer es una salida válida
```

Y especialmente:

> **un sistema RAG fiable necesita saber cuándo tiene evidencia suficiente y cuándo no.**
