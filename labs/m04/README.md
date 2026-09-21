# M04 — Laboratorio: Contratos verificables y tool calls controladas

## Objetivo

En esta práctica vas a transformar una incidencia escrita en lenguaje natural en un objeto que pueda consumir software.

Trabajaremos con una única cadena:

```text
incidencia
  ↓
JSON libre
  ↓
JSON Schema
  ↓
validación
  ↓
repair
  ↓
objeto válido
  ↓
tool call
  ↓
runtime valida
  ↓
ejecución controlada
```

La idea central es:

> **Pedir JSON no crea un contrato. Y una tool call propuesta por un modelo no equivale a permiso para ejecutarla.**

---

## Entorno

```bash
cd /workspaces/prompt-engineering-labs
git pull
python -m pip install --user -r requirements.txt
kiro-cli
```

Los archivos del laboratorio son:

```text
labs/m04/
├── README.md
├── incident.txt
├── schema.json
├── validate.py
└── worksheet.md
```

Los archivos que tú generes puedes guardarlos en:

```text
labs/m04/work/
```

---

# 1. Primer intento: “devuelve JSON”

En una conversación nueva:

```text
Analiza @labs/m04/incident.txt y devuelve la información como JSON.
```

Observa:

- nombres de campos;
- tipos;
- valores inventados;
- campos ausentes;
- si añade texto o Markdown;
- si el mismo prompt produciría una estructura fiable para una aplicación.

Anota tus observaciones.

---

# 2. El contrato

Abre:

```text
labs/m04/schema.json
```

El schema define la estructura requerida.

Además, aplica estas reglas semánticas:

```text
1. No inventar una causa.
2. suspected_cause = null salvo causa explícitamente confirmada.
3. P2 cuando:
   - environment = production
   - affected_users >= 25
   - existe impacto funcional confirmado
4. P3 para impacto funcional limitado que no alcanza P2.
5. evidence solo puede contener hechos del ticket.
6. recommended_action debe ser open_bug para este caso si la extracción es correcta.
```

---

# 3. Crear un prompt estructurado

Crea:

```text
labs/m04/work/prompt.md
```

Debe incluir:

```text
TASK
SOURCE OF TRUTH
INPUT
RESTRICTIONS
OUTPUT CONTRACT
SUCCESS CRITERIA
```

Incluye explícitamente:

- usar solo información del ticket;
- no inventar causa;
- devolver solo JSON;
- cumplir `schema.json`;
- respetar las reglas semánticas;
- no añadir comentarios ni Markdown.

---

# 4. Generar output.json

Pide a Kiro:

```text
Aplica @labs/m04/work/prompt.md.

Contrato:
@labs/m04/schema.json

Entrada:
@labs/m04/incident.txt

Crea únicamente:
labs/m04/work/output.json
```

---

# 5. Validar

Ejecuta:

```bash
python labs/m04/validate.py labs/m04/work/output.json
```

El validador comprueba:

```text
1. JSON syntax
2. JSON Schema
3. semantic rules
```

Un resultado correcto termina con:

```text
SYNTAX_VALID
SCHEMA_VALID
SEMANTIC_VALID
```

---

# 6. Ver los tres tipos de fallo sin crear más archivos

Ejecuta:

```bash
python labs/m04/validate.py --demo
```

El script muestra tres ejemplos incorporados:

```text
SYNTAX ERROR
SCHEMA ERROR
SEMANTIC ERROR
```

Responde:

> ¿Qué parte podría evitar JSON Mode?  
> ¿Qué parte podría evitar Structured Outputs?  
> ¿Qué parte sigue necesitando validación de negocio?

---

# 7. Validator → Repair → Retry

Si tu `output.json` falla, copia únicamente los errores del validador.

En una conversación nueva:

```text
Archivo actual:
@labs/m04/work/output.json

Contrato:
@labs/m04/schema.json

Errores:
[PEGA LOS ERRORES]

Corrige únicamente los defectos que explican esos errores.
No inventes información nueva.

Sobrescribe:
labs/m04/work/output.json
```

Valida otra vez:

```bash
python labs/m04/validate.py labs/m04/work/output.json
```

Si tu primera salida ya era válida, utiliza uno de los errores mostrados por `--demo` para discutir qué capa lo detectaría. No necesitas romper tu propio archivo.

---

# 8. Tool call como output estructurado

El objeto validado contiene:

```text
service = identity-api
```

Ahora necesitas el owner del servicio.

No pidas al modelo que lo invente.

Utiliza este contrato:

```json
{
  "tool": "get_service_owner",
  "arguments": {
    "service": "identity-api"
  }
}
```

Crea:

```text
labs/m04/work/tool-call.json
```

con este prompt:

```text
Necesito obtener el owner del servicio de la incidencia.

Incidencia validada:
@labs/m04/work/output.json

Genera únicamente una tool call JSON.

Herramienta permitida:
get_service_owner

Argumentos permitidos:
service = identity-api | billing-api | web-portal

No ejecutes la herramienta.
No añadas otros campos.
```

---

# 9. El runtime decide si puede ejecutarse

Ejecuta:

```bash
python labs/m04/validate.py \
  labs/m04/work/tool-call.json \
  --tool-call \
  --execute
```

El script:

```text
parsea
→ valida estructura
→ comprueba allowlist
→ valida argumentos
→ ejecuta una función local read-only
```

Si todo es correcto verás:

```text
TOOL_CALL_VALID
TOOL_RESULT:
...
```

---

# 10. Comprueba el control del runtime

Edita temporalmente `tool-call.json` y cambia:

```json
"tool": "get_service_owner"
```

por:

```json
"tool": "deploy_fix"
```

Vuelve a ejecutar:

```bash
python labs/m04/validate.py \
  labs/m04/work/tool-call.json \
  --tool-call \
  --execute
```

El runtime debe rechazarlo.

Después restaura la tool call válida.

La pregunta clave es:

> ¿Por qué el hecho de que un LLM proponga una acción no significa que el sistema deba permitirla?

---

# 11. Conclusión

Completa:

```text
labs/m04/worksheet.md
```

Debes poder explicar:

```text
JSON válido ≠ schema válido
schema válido ≠ semántica correcta
tool call propuesta ≠ ejecución autorizada
```

Y también:

> ¿qué responsabilidad pertenece al prompt, cuál al schema y cuál al runtime?
