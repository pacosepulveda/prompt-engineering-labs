# M03 — Laboratorio: Técnicas avanzadas para una revisión de readiness

## Curso de Prompt Engineering Avanzado

**Modalidad:** práctica guiada en clase  
**Duración estimada:** 100–120 minutos  
**Entorno recomendado:** GitHub Codespaces + Kiro CLI  
**Programación obligatoria:** no  
**Caso:** revisión de readiness de un cambio de software con evidencias incompletas

---

## 1. Objetivo

En M02 trabajamos el prompt como una especificación evaluable.

En M03 vamos a responder una pregunta distinta:

> **¿Qué técnica merece la pena añadir cuando un prompt simple ya no es suficiente?**

No utilizaremos técnicas avanzadas porque “suenen mejor”. Cada técnica debe resolver un fallo observado.

Durante el laboratorio compararemos:

1. **zero-shot**;
2. **few-shot**;
3. **decomposition**;
4. **tool-aware prompting** mediante un tool loop manual;
5. **múltiples candidatos**;
6. **critique & revision**;
7. **meta-prompting** apoyado en resultados observados.

---

## 2. Qué NO vamos a hacer

En este laboratorio:

- no pediremos cadenas privadas de razonamiento;
- no utilizaremos “piensa paso a paso” como requisito;
- no crearemos todavía agentes personalizados;
- no configuraremos MCP;
- no construiremos RAG;
- no automatizaremos el workflow con código.

Cuando necesitemos justificar una respuesta pediremos hechos, criterios, evidencia, datos ausentes y conclusión.

---

## 3. Escenario

Formas parte de un equipo que revisa cambios antes de desplegarlos a producción.

El cambio principal es **CHG-482**, relacionado con la renovación de tokens de una aplicación SaaS.

La IA **no autoriza el despliegue**. Produce una recomendación para revisión humana:

```text
READY
BLOCKED
NEEDS_EVIDENCE
```

La recomendación debe basarse únicamente en la política, la información del cambio y las evidencias obtenidas mediante las herramientas permitidas.

---

## 4. Preparar el entorno

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

Comprueba el modelo con:

```text
/model
```

Mantén el mismo modelo durante cada comparación y utiliza:

```text
/chat new
```

antes de ejecuciones independientes.

---

# Parte A — Zero-shot

En una conversación nueva:

```text
Revisa @labs/m03/cases/CHG-482.md y dime si está listo para producción.
```

Registra en `labs/m03/worksheet.md`:

- recomendación;
- criterios aparentes;
- supuestos;
- evidencia ignorada o ausente;
- auditabilidad.

---

# Parte B — Política explícita

Lee:

```text
labs/m03/context/release-policy.md
```

En una conversación nueva:

```text
Aplica @labs/m03/context/release-policy.md a
@labs/m03/cases/CHG-482.md.

Devuelve:
RECOMMENDATION:
GATES:
MISSING_EVIDENCE:
NEXT_STEP:

No inventes evidencias.
```

Compara con zero-shot.

---

# Parte C — Few-shot

Primero utiliza:

```text
labs/m03/examples/few-shot-poor.md
```

Después repite con:

```text
labs/m03/examples/few-shot-good.md
```

Prompt recomendado:

```text
La política aplicable es @labs/m03/context/release-policy.md.

Usa como ejemplos de comportamiento:
@labs/m03/examples/few-shot-good.md

Ahora revisa:
@labs/m03/cases/CHG-482.md

Devuelve:
RECOMMENDATION:
GATES:
MISSING_EVIDENCE:
NEXT_STEP:
```

Evalúa si los ejemplos mejoran interpretación, missing data, consistencia y respeto a reglas.

---

# Parte D — Decomposition

En una conversación nueva:

```text
Usa:
- política: @labs/m03/context/release-policy.md
- cambio: @labs/m03/cases/CHG-482.md

No emitas todavía una recomendación final.

FASE 1 — FACTS
Extrae únicamente hechos explícitos del cambio.
No completes campos ausentes.

FASE 2 — GATE ASSESSMENT
Para cada gate de la política indica:
PASS | FAIL | UNKNOWN
y cita la evidencia utilizada.

FASE 3 — MISSING EVIDENCE
Enumera únicamente la evidencia necesaria para convertir los UNKNOWN
relevantes en PASS o FAIL.

Devuelve solo esas tres fases.
```

---

# Parte E — Tool-aware prompting

En M03 haremos un tool loop manual y auditable:

```text
TOOL_REQUEST
     ↓
runtime / humano ejecuta
     ↓
TOOL_RESULT
     ↓
modelo decide si necesita otra evidencia
     ↓
FINAL
```

Consulta el catálogo:

```bash
python labs/m03/tools/release_tool.py list-tools
```

En Kiro:

```text
Tienes que revisar CHG-482.

Política:
@labs/m03/context/release-policy.md

Información inicial:
@labs/m03/cases/CHG-482.md

Catálogo de herramientas:
@labs/m03/context/tool-catalog.md

REGLAS:
- No inventes resultados de herramientas.
- Si falta evidencia necesaria, devuelve únicamente un TOOL_REQUEST.
- Solicita una sola herramienta cada vez.
- Espera a recibir TOOL_RESULT antes de continuar.
- Cuando exista evidencia suficiente, devuelve FINAL.
- No expongas razonamiento privado.

Formato de petición:

TOOL_REQUEST:
tool: <nombre>
change_id: <id>
purpose: <qué evidencia verificable necesitas>

Formato final:

FINAL:
RECOMMENDATION:
GATES:
EVIDENCE:
MISSING_EVIDENCE:
NEXT_STEP:
```

Ejecuta cada herramienta solicitada en una segunda terminal:

```bash
python labs/m03/tools/release_tool.py test-summary CHG-482
```

Pega la salida precedida por:

```text
TOOL_RESULT:
```

Registra el trace en `worksheet.md`.

---

# Parte F — Múltiples candidatos

Conserva la evidencia obtenida y genera tres revisiones independientes en tres conversaciones nuevas.

Utiliza exactamente la misma política, cambio, tool results y modelo.

Después evalúa A, B y C con:

```text
labs/m03/context/review-rubric.md
```

No selecciones por estilo o longitud.

---

# Parte G — Critique & Revision

Escoge el candidato con mejor puntuación verificable.

Pide primero crítica sin reescritura:

```text
Actúa como revisor.

No reescribas todavía la respuesta.

Evalúa el candidato únicamente contra:
@labs/m03/context/review-rubric.md

Devuelve solo:

CONFIRMED_DEFECTS:
- defecto
  criterion:
  evidence:

NO_CHANGE_NEEDED:
- elementos que ya cumplen

No inventes defectos para justificar una revisión.
```

Después:

```text
Corrige únicamente los defectos de CONFIRMED_DEFECTS.

Conserva todo lo que aparece en NO_CHANGE_NEEDED.

Devuelve:
RECOMMENDATION:
GATES:
EVIDENCE:
RISKS:
NEXT_STEP:
```

---

# Parte H — Meta-prompting

No pidas simplemente “hazme un prompt mejor”.

Utiliza fallos observados:

```text
Prompt/procedimiento actual:
[PEGA LA VERSIÓN UTILIZADA]

Fallos observados:
[PEGA SOLO FALLOS REALES]

Criterios:
@labs/m03/context/review-rubric.md

Propón el CAMBIO MÍNIMO al prompt que corrija esos fallos.

No añadas reglas que no respondan a un fallo observado.

Devuelve:
CHANGE:
RATIONALE:
EXPECTED_EFFECT:
REGRESSION_RISK:
```

Comprueba regresiones con:

```text
labs/m03/cases/CHG-509.md
labs/m03/cases/CHG-530.md
```

---

## Resultado de aprendizaje

Al finalizar debes poder explicar qué problema resuelve cada técnica y por qué:

- zero-shot es el baseline;
- few-shot enseña comportamiento, no hechos;
- decomposition mejora trazabilidad;
- tool calls + results producen evidencia observable;
- consenso no equivale a verdad;
- critique necesita criterios;
- meta-prompting necesita evals.

No hay entrega fuera de clase.
