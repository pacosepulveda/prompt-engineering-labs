# M04 — Laboratorio: De texto libre a contratos verificables y tool calls controladas

## Curso de Prompt Engineering Avanzado

**Modalidad:** práctica guiada en clase  
**Entorno recomendado:** GitHub Codespaces + Kiro CLI  
**Programación obligatoria:** no  
**Caso:** normalización y enrutado de incidencias de producto

---

# 1. Objetivo

En este laboratorio vamos a pasar de una respuesta pensada para humanos a una salida que pueda consumir software.

Trabajaremos con este flujo:

```text
Texto libre
    ↓
Prompt estructurado
    ↓
JSON
    ↓
Validación
    ↓
Reparación si falla
    ↓
Dato fiable
    ↓
Tool call propuesta por el modelo
    ↓
Runtime valida y ejecuta
```

La idea principal es:

> **El modelo propone. El runtime controla. La herramienta ejecuta.**

---

# 2. Qué vas a practicar

- output contracts;
- JSON y JSON Schema;
- diferencia entre JSON válido y datos válidos;
- validación sintáctica;
- validación de esquema;
- validación semántica;
- recuperación `validator → repair → retry`;
- formatos deterministas a partir de datos ya validados;
- tool calling mediante contratos explícitos;
- separación entre decisión del modelo y ejecución del runtime;
- creación de un prompt reutilizable como artefacto.

---

# 3. Escenario

Un equipo de soporte recibe incidencias en texto libre.

Queremos normalizarlas a una estructura común antes de:

- abrir bugs;
- solicitar más información;
- escalar un posible incidente de seguridad;
- enrutar la incidencia al owner de un servicio.

Los datos son sintéticos.

La IA no debe ejecutar acciones directamente.

---

# 4. Preparar el entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

Mantén el mismo modelo durante las comparaciones.

Antes de ejecuciones independientes:

```text
/chat new
```

---

# Parte A — Pedir JSON no es tener un contrato

## 5. Primer intento

Abre:

```text
labs/m04/cases/TKT-1042.txt
```

En una conversación nueva:

```text
Analiza @labs/m04/cases/TKT-1042.txt y devuelve la información como JSON.
```

Observa nombres de campos, tipos, valores inventados, campos ausentes, estabilidad del formato y si añade Markdown alrededor del JSON.

Registra tus observaciones en:

```text
labs/m04/worksheet.md
```

---

# Parte B — Definir el contrato

## 6. Examina el JSON Schema

Abre:

```text
labs/m04/contracts/incident.schema.json
```

El schema define campos obligatorios, tipos, enumeraciones, valores permitidos y restricciones estructurales.

También abre:

```text
labs/m04/context/normalization-policy.md
```

El schema define **estructura**. La política define reglas **semánticas**.

---

## 7. Crea un prompt de extracción V1

Crea:

```text
labs/m04/work/incident-extractor-v1.md
```

Utiliza esta estructura:

```markdown
# TASK
# SOURCE OF TRUTH
# INPUT
# POPULATION RULES
# OUTPUT CONTRACT
# SUCCESS CRITERIA
```

Debe indicar como mínimo:

- que solo puede utilizar información presente en la entrada;
- que no puede inventar una causa;
- cómo representar datos ausentes;
- que debe respetar los valores permitidos;
- que debe devolver **solo JSON**;
- que los posibles secretos no deben reproducirse literalmente;
- que la política semántica también debe respetarse.

No copies manualmente la respuesta esperada del caso.

---

# Parte C — Generar y validar

## 8. Genera incident-v1.json

En una conversación nueva:

```text
Aplica exactamente @labs/m04/work/incident-extractor-v1.md.

Contrato estructural:
@labs/m04/contracts/incident.schema.json

Política semántica:
@labs/m04/context/normalization-policy.md

Entrada:
@labs/m04/cases/TKT-1042.txt

Crea el archivo:
labs/m04/work/incident-v1.json

No modifiques ningún otro archivo.
```

---

## 9. Validación de esquema

```bash
python labs/m04/tools/validate_incident.py   labs/m04/work/incident-v1.json   --schema-only
```

Puedes obtener `SCHEMA_VALID` o errores de schema.

Un JSON puede ser sintácticamente válido y aun así violar el contrato.

---

## 10. Validación completa

```bash
python labs/m04/tools/validate_incident.py   labs/m04/work/incident-v1.json
```

Esta comprobación añade reglas semánticas.

---

# Parte D — Syntax vs Schema vs Semantics

## 11. Casos preparados

```bash
python labs/m04/tools/validate_incident.py labs/m04/samples/invalid-syntax.json
python labs/m04/tools/validate_incident.py labs/m04/samples/invalid-schema.json
python labs/m04/tools/validate_incident.py labs/m04/samples/invalid-semantic.json
```

Clasifica cada fallo como:

```text
SYNTAX
SCHEMA
SEMANTIC
```

Pregunta:

> ¿Podría un “JSON mode” resolver los tres tipos de error?

---

# Parte E — Validator → Repair → Retry

## 12. Reparar utilizando errores verificables

Si `incident-v1.json` falla, copia únicamente los errores del validador.

En Kiro:

```text
/chat new
```

y utiliza:

```text
Archivo actual:
@labs/m04/work/incident-v1.json

Contrato:
@labs/m04/contracts/incident.schema.json

Política:
@labs/m04/context/normalization-policy.md

Errores del validador:
[PEGA LOS ERRORES]

Corrige únicamente los defectos que explican esos errores.
No inventes información nueva.

Escribe el resultado en:
labs/m04/work/incident-v2.json
```

Valida otra vez hasta obtener:

```text
SCHEMA_VALID
SEMANTIC_VALID
```

Si V1 ya era válida, practica el ciclo con `invalid-schema.json` o `invalid-semantic.json`.

---

# Parte F — Probar el contrato con otros casos

## 13. Casos adicionales

Usa el mismo prompt con:

```text
labs/m04/cases/TKT-1057.txt
labs/m04/cases/TKT-1099.txt
```

Guarda:

```text
labs/m04/work/TKT-1057.json
labs/m04/work/TKT-1099.json
```

Valida ambos.

En `TKT-1099`, el modelo debe poder indicar:

```json
"contains_sensitive_data": true
```

sin copiar el secreto literal.

---

# Parte G — Formatos deterministas

## 14. Renderizado

Una vez validado un JSON:

```bash
python labs/m04/tools/render_incident.py   labs/m04/work/incident-v2.json
```

El script genera YAML, CSV y Markdown a partir de la misma representación canónica.

Compara:

```text
LLM → YAML
LLM → CSV
LLM → Markdown
```

con:

```text
JSON validado
→ serializer
→ YAML / CSV / Markdown
```

---

# Parte H — Tool calling como contrato

## 15. Nuevo caso

Abre:

```text
labs/m04/cases/TKT-1120.txt
labs/m04/contracts/tool-call.schema.json
labs/m04/context/tool-catalog.md
```

El modelo no conoce el owner del servicio. Debe solicitar una herramienta.

---

## 16. Proponer una tool call

```text
Normaliza primero mentalmente la incidencia, pero no muestres razonamiento privado.

Entrada:
@labs/m04/cases/TKT-1120.txt

Política:
@labs/m04/context/normalization-policy.md

Catálogo:
@labs/m04/context/tool-catalog.md

Contrato de tool call:
@labs/m04/contracts/tool-call.schema.json

Necesitas obtener la información necesaria para enrutar el ticket.

Crea únicamente:
labs/m04/work/tool-call.json

No ejecutes herramientas.
```

---

## 17. El runtime controla

```bash
python labs/m04/tools/execute_tool.py   labs/m04/work/tool-call.json
```

El runtime parsea JSON, valida schema, verifica allowlist, valida argumentos y ejecuta una herramienta local read-only.

Si es válido, verás:

```text
TOOL_CALL_VALID
```

seguido de `TOOL_RESULT`.

---

## 18. Tool call inválida

```bash
python labs/m04/tools/execute_tool.py   labs/m04/samples/invalid-tool-call.json
```

Pregunta:

> Si el modelo propone una llamada, ¿significa que debemos ejecutarla?

---

# Parte I — Utilizar el resultado

## 19. Crear una acción final

Copia el `TOOL_RESULT`.

```text
Incidencia:
@labs/m04/cases/TKT-1120.txt

Resultado de herramienta:
[PEGA TOOL_RESULT]

Genera únicamente:

ACTION:
OWNER:
RUNBOOK:
RATIONALE:

No inventes valores que no aparezcan en la incidencia o en TOOL_RESULT.
```

---

# Parte J — Prompt como artefacto reutilizable

## 20. Crea una plantilla

Guarda una versión final:

```text
labs/m04/work/incident-extractor-template.md
```

Debe contener propósito, fuente de verdad, placeholder de entrada, reglas de población, referencia al contrato y criterios de éxito.

No incluyas información específica de un ticket concreto.

---

# 21. Hoja de trabajo

Completa:

```text
labs/m04/worksheet.md
```

Debes poder explicar:

- diferencia entre sintaxis, schema y semántica;
- por qué JSON válido no implica output correcto;
- qué aporta validator→repair→retry;
- cuándo serializar con código;
- por qué una tool call no debe ejecutarse directamente;
- qué responsabilidad pertenece al prompt, schema y runtime.

---

# Reto opcional — SQL como artefacto

Abre:

```text
labs/m04/challenges/sql-request.md
```

Genera una consulta SQL parametrizada, sin ejecutarla.

Evalúa:

- consulta y parámetros separados;
- ausencia de concatenación de datos no confiables;
- uso exclusivo de tablas/columnas permitidas;
- output limitado al artefacto solicitado.
