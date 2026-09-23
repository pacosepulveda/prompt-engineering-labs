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


### Si no utilizas Kiro

Kiro CLI es el entorno de referencia utilizado en las instrucciones del curso, pero **no es obligatorio para completar este laboratorio**.

Puedes utilizar otra herramienta equivalente, por ejemplo GitHub Copilot, Claude/Claude Code, ChatGPT/Codex u otro asistente LLM que te permita trabajar con los mismos prompts y archivos.

Cuando aparezca una instrucción específica de Kiro:

- `/chat new` significa iniciar una conversación o contexto nuevo;
- `@archivo` significa proporcionar ese archivo como contexto mediante el mecanismo equivalente de tu herramienta;
- si la herramienta no puede crear archivos directamente, puedes copiar su salida al archivo indicado.

Mantén constantes los inputs, reglas y criterios de evaluación. **Se evalúa el procedimiento y la evidencia obtenida, no la herramienta utilizada.**

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

Además, para **TKT-1042** aplicamos estas reglas de negocio deterministas:

```text
1. category = authentication
   porque el incidente describe HTTP 401 durante el refresh de sesión.

2. severity = P2
   porque:
   - environment = production
   - affected_users = 37 (>= 25)
   - existe impacto funcional confirmado:
     los usuarios deben volver a iniciar sesión.

3. suspected_cause = null
   porque no existe una causa raíz confirmada.
   La frase "maybe the new cache..." es una hipótesis, no una confirmación.

4. recommended_action = open_bug
   porque el incidente está suficientemente descrito para registrar un defecto,
   aunque la causa raíz siga sin confirmarse.
```

Y aplicamos una capa separada de **grounding**:

```text
5. summary y evidence solo pueden afirmar hechos soportados por incident.txt.

6. Una hipótesis del ticket no puede presentarse como hecho confirmado.
```

Importante:

```text
validate.py
→ comprueba sintaxis
→ comprueba JSON Schema
→ comprueba las reglas de negocio deterministas 1–4

grounding review
→ compara manualmente summary/evidence con incident.txt
```

No pretendemos que un validador determinista genérico decida si cualquier frase en lenguaje natural está respaldada por el ticket.

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
- respetar las reglas de negocio deterministas;
- mantener summary y evidence grounded en incident.txt;
- no convertir hipótesis en hechos;
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
3. deterministic business rules
```

Un resultado correcto termina con:

```text
SYNTAX_VALID
SCHEMA_VALID
SEMANTIC_VALID
GROUNDING_REVIEW_REQUIRED | compare summary/evidence with incident.txt
```

La última línea es deliberada: el programa no declara automáticamente que el texto libre está grounded. Ese control se revisa aparte.

---

# 6. Grounding review

Después de obtener `SEMANTIC_VALID`, compara manualmente:

```text
labs/m04/work/output.json
vs.
labs/m04/incident.txt
```

Comprueba:

```text
- summary no introduce hechos nuevos;
- cada elemento de evidence está respaldado por el ticket;
- "maybe the new cache..." no aparece como causa confirmada;
- no se inventan sistemas, fechas, owners, métricas o diagnósticos.
```

Anota el resultado en `worksheet.md`.

La distinción que buscamos es:

```text
schema válido
≠
semántica de negocio válida
≠
contenido grounded
```

---

# 7. Ver los tres tipos de fallo sin crear más archivos

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

# 8. Validator → Repair → Retry

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

# 9. Tool call como output estructurado

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

# 10. El runtime decide si puede ejecutarse

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

# 11. Comprueba el control del runtime

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

# 12. Conclusión

Completa:

```text
labs/m04/worksheet.md
```

Debes poder explicar:

```text
JSON válido ≠ schema válido
schema válido ≠ semántica correcta
semántica correcta ≠ contenido grounded
tool call propuesta ≠ ejecución autorizada
```

Y también:

> ¿qué responsabilidad pertenece al prompt, cuál al schema y cuál al runtime?
