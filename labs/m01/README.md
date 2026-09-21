# M01 — Laboratorio: Observar cómo se comporta un LLM

## Objetivo

Antes de diseñar prompts avanzados necesitamos un modelo mental correcto de lo que ocurre al utilizar un LLM.

En esta práctica vas a observar cinco ideas:

```text
texto ≠ tokens
generación ≠ búsqueda en una base de datos
sampling cambia variabilidad, no verdad
contexto influye en la respuesta
fluidez ≠ evidencia
```

El laboratorio combina un pequeño simulador local con un LLM.

No necesitas ninguna API de pago.

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
python -m pip install --user -r requirements.txt
./scripts/check-environment.sh
```

Los archivos del laboratorio son:

```text
labs/m01/
├── README.md
├── fundamentals_lab.py
└── worksheet.md
```

---

### Si no utilizas Kiro

Kiro CLI es el entorno de referencia utilizado en las instrucciones del curso, pero **no es obligatorio para completar este laboratorio**.

Puedes utilizar otra herramienta equivalente, por ejemplo GitHub Copilot, Claude/Claude Code, ChatGPT/Codex u otro asistente LLM.

Cuando aparezca:

```text
/chat new
```

utiliza una conversación o contexto nuevo en tu herramienta.

Mantén el mismo modelo durante las comparaciones de comportamiento.

**Se evalúan las observaciones y conclusiones, no la herramienta utilizada.**

---

# 2. Del texto a los tokens

Ejecuta:

```bash
python labs/m01/fundamentals_lab.py tokens
```

El script utiliza `o200k_base` como **tokenizer de referencia**.

No representa necesariamente el tokenizer exacto del modelo que estés utilizando.

Observa los ejemplos de:

```text
inglés
español
código
identificadores técnicos
Unicode / emoji
```

Responde en:

```text
labs/m01/worksheet.md
```

### Preguntas

1. ¿Una palabra equivale siempre a un token?
2. ¿Dos textos con un número parecido de caracteres ocupan necesariamente el mismo número de tokens?
3. ¿Por qué no deberíamos estimar costes o límites contando palabras?

---

# 3. La cadena conceptual de un LLM

Completa en la hoja de trabajo:

```text
texto
→ __________
→ token IDs
→ __________
→ capas Transformer
→ __________
→ distribución de probabilidad
→ __________
→ siguiente token
```

Utiliza estos conceptos una sola vez:

```text
tokenizer
embeddings
logits
sampling/decoding
```

Después responde:

> ¿En qué punto de esa cadena aparece una “consulta a una base de datos de hechos”?

---

# 4. Simular next-token prediction

Ejecuta:

```bash
python labs/m01/fundamentals_lab.py sampling
```

El script utiliza una distribución ficticia de posibles continuaciones para:

```text
"The incident is ..."
```

No es la salida de ningún modelo real.

Su objetivo es hacer observable el proceso de selección.

Verás algo parecido a:

```text
stable
degraded
critical
resolved
unknown
```

con probabilidades diferentes.

Pregunta:

> Si el modelo produce el token más probable, ¿eso demuestra que la afirmación sea verdadera?

---

# 5. Temperature

Compara:

```bash
python labs/m01/fundamentals_lab.py sampling --temperature 0.3
```

con:

```bash
python labs/m01/fundamentals_lab.py sampling --temperature 1.0
```

y:

```bash
python labs/m01/fundamentals_lab.py sampling --temperature 1.8
```

Anota:

```text
¿qué ocurre con la distribución?
¿se concentra o se aplana?
¿aparecen más alternativas plausibles?
```

No concluyas:

```text
temperature baja = verdad
```

Temperature modifica la distribución de muestreo.

No convierte el modelo en una fuente factual.

---

# 6. Top-k y Top-p

Prueba:

```bash
python labs/m01/fundamentals_lab.py sampling \
  --temperature 1.0 \
  --top-k 2
```

Después:

```bash
python labs/m01/fundamentals_lab.py sampling \
  --temperature 1.0 \
  --top-p 0.75
```

Compara qué candidatos siguen disponibles.

Responde:

```text
Top-k limita por:
Top-p limita por:
```

Pregunta:

> ¿Existe una configuración universalmente correcta para todos los modelos y tareas?

---

# 7. Variabilidad en un LLM real

Inicia Kiro:

```bash
kiro-cli
```

o utiliza tu herramienta alternativa.

En una conversación nueva pregunta:

```text
Give three plausible causes of intermittent HTTP 401 responses
after a user session has been idle for 30 minutes.
Do not assume that any cause is confirmed.
```

Guarda una nota de la respuesta.

Inicia una conversación nueva:

```text
/chat new
```

y repite exactamente el mismo prompt.

Hazlo una tercera vez.

No buscamos comprobar cuál es la causa correcta.

Compara:

```text
orden
vocabulario
causas propuestas
nivel de detalle
```

Pregunta:

> ¿Respuesta diferente significa necesariamente peor respuesta?

---

# 8. Contexto limpio vs contexto contaminado

Genera el primer contexto:

```bash
mkdir -p labs/m01/work

python labs/m01/fundamentals_lab.py context \
  --variant clean \
  > labs/m01/work/context.md
```

En una conversación nueva utiliza:

```text
Use only the supplied context.

Context:
[pega el contenido de labs/m01/work/context.md]

Return:

STATUS:
RCA_CONFIRMED:
EVIDENCE:
```

Registra el resultado.

Ahora genera:

```bash
python labs/m01/fundamentals_lab.py context \
  --variant noisy \
  > labs/m01/work/context.md
```

Repite exactamente la misma tarea en una conversación nueva.

El contexto noisy contiene información histórica y opiniones que **no describen el incidente actual**.

Compara:

```text
¿cambió la respuesta?
¿apareció una causa histórica como si fuera actual?
¿qué información tenía mayor autoridad?
```

La idea no es todavía optimizar contexto —eso llegará más adelante—, sino observar que:

> **el comportamiento del modelo depende del contexto que recibe.**

---

# 9. Fluidez no es evidencia

En una conversación nueva pregunta:

```text
What does error TEL-9941 mean in Telvora EdgeSync 9.4?
Give the exact root cause and the official remediation command.
```

`Telvora EdgeSync 9.4` y `TEL-9941` son elementos ficticios del laboratorio.

Observa la respuesta.

Clasifícala como:

```text
ABSTENTION
UNSUPPORTED_CLAIM
MIXED
```

Una respuesta extensa y técnicamente convincente no constituye evidencia.

---

# 10. Grounding

Ahora ejecuta:

```bash
python labs/m01/fundamentals_lab.py evidence
```

Obtendrás una ficha ficticia y explícita para el mismo error.

En una conversación nueva proporciona esa ficha y pregunta:

```text
Use only the supplied evidence.

What does TEL-9941 mean?

Return:

MEANING:
CONFIRMED_CAUSE:
ALLOWED_NEXT_STEP:
SOURCE:
```

Compara con la respuesta anterior.

Pregunta:

> ¿Qué cambió: los pesos del modelo o el contexto disponible?

---

# 11. Knowledge cutoff y actualidad

Responde sin buscar en Internet:

```text
¿Puede el hecho de que un modelo sea "nuevo" garantizar que conozca
el estado actual de una API, producto o vulnerabilidad?
```

Después completa:

```text
Conocimiento paramétrico:
Evidencia recuperada:
```

Identifica cuál utilizarías para responder con fiabilidad a:

```text
"¿Cuál es la versión soportada actualmente?"
```

---

# 12. Elegir el control adecuado

Relaciona cada problema con el control principal.

Problemas:

```text
A. Necesito un cálculo exacto.
B. Necesito información actual.
C. Necesito una respuesta basada en documentación corporativa.
D. La respuesta puede desencadenar una acción en producción.
E. Quiero comprobar si dos perfiles equivalentes reciben decisiones diferentes.
```

Controles:

```text
CALCULATOR / CODE
WEB / RETRIEVAL
RAG / GROUNDED CONTEXT
AUTHORIZATION + HITL
PAIRED / COUNTERFACTUAL EVALUATION
```

No todos los problemas de un LLM se resuelven cambiando el prompt.

---

# 13. Conclusión

Completa:

```text
labs/m01/worksheet.md
```

Debes poder explicar:

```text
token ≠ palabra
context window ≠ memoria persistente
probabilidad alta ≠ verdad
temperature baja ≠ factualidad
respuesta fluida ≠ evidencia
contexto disponible ≠ conocimiento actualizado
prompting ≠ control determinista
```

La idea que conecta M01 con el resto del curso es:

> **Para diseñar sistemas fiables con LLMs primero debemos saber qué comportamientos pertenecen al modelo y cuáles deben resolverse con contexto, herramientas, evaluación o controles externos.**
