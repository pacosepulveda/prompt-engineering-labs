# M05 — Laboratorio: Context Engineering, coste y rendimiento

## Objetivo

En este laboratorio vas a optimizar el contexto de una aplicación LLM sin limitarte a “recortar texto”.

Trabajaremos con cuatro dimensiones a la vez:

```text
calidad
coste
latencia
tamaño de contexto
```

El objetivo no es conseguir el prompt más corto.

El objetivo es conseguir:

> **el contexto mínimo que conserva la evidencia necesaria para responder correctamente.**

---

## Entorno

Desde el Codespace:

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
labs/m05/
├── README.md
├── context.md
├── analyze.py
└── worksheet.md
```

Durante el ejercicio crearás:

```text
labs/m05/context-optimized.md
```

---

# 1. Escenario

Estás diseñando un asistente interno para un equipo de Cloud Operations.

El asistente recibe contexto procedente de:

- estado actual de incidencias;
- telemetría;
- runbooks;
- políticas;
- postmortems históricos;
- documentación de producto;
- avisos de seguridad;
- notas de versiones.

Un usuario pregunta:

```text
Prepare an operations brief for INC-7782.

Include:
1. current status;
2. evidence supporting that status;
3. what Support can safely tell customers;
4. one next diagnostic check.

Do not claim a root cause unless it is confirmed.
```

El problema es que el sistema está enviando **todo el contexto disponible** al modelo.

---

# 2. Medir antes de optimizar

Ejecuta:

```bash
python labs/m05/analyze.py labs/m05/context.md
```

El script mostrará:

- caracteres;
- palabras;
- reference tokens;
- porcentaje aproximado de ventana ocupado;
- coste estimado con dos perfiles de modelo;
- TTFT estimado;
- coste de una conversación de varios turnos;
- efecto estimado de prompt caching.

> Los perfiles de coste y rendimiento son sintéticos y se utilizan para comparar estrategias.  
> Los `reference tokens` se calculan con un tokenizer de referencia y no representan necesariamente la facturación exacta de Kiro o de un proveedor concreto.

Registra los valores principales en:

```text
labs/m05/worksheet.md
```

---

# 3. Baseline con contexto completo

Inicia una conversación nueva:

```text
/chat new
```

Utiliza:

```text
Context:
@labs/m05/context.md

Task:
Prepare an operations brief for INC-7782.

Include:
1. current status;
2. evidence supporting that status;
3. what Support can safely tell customers;
4. one next diagnostic check.

Rules:
- Use only the supplied context.
- Do not claim a root cause unless it is confirmed.
- Distinguish current evidence from historical information.
- If sources conflict, prefer the source with greater authority and freshness.

Return:
STATUS:
EVIDENCE:
CUSTOMER_MESSAGE:
NEXT_CHECK:
```

Evalúa la respuesta con estos cinco criterios:

| Criterio | 1 punto si... |
|---|---|
| Current status | describe correctamente el estado actual |
| Grounding | utiliza evidencia presente en fuentes actuales |
| Freshness | no confunde información histórica con el incidente actual |
| RCA discipline | no presenta hipótesis como causa confirmada |
| Support message | el mensaje respeta la política de comunicación |

Máximo:

```text
5 puntos
```

No optimices todavía.

---

# 4. Clasificar el contexto

Abre:

```text
labs/m05/context.md
```

Cada sección tiene:

```text
SOURCE
TYPE
AUTHORITY
FRESHNESS
```

Clasifica mentalmente cada sección como:

```text
KEEP
COMPRESS
DROP
```

Utiliza estas preguntas:

### Relevancia

¿Ayuda a responder esta tarea concreta?

### Autoridad

¿Es una fuente suficientemente fiable para la afirmación que queremos hacer?

### Frescura

¿Describe el incidente actual o un evento histórico?

### Redundancia

¿La misma información ya aparece en una fuente mejor ?

### Riesgo de contaminación

¿Puede inducir al modelo a mezclar incidentes, causas o
 políticas?

---

# 5. Crear un context pack optimizado

Crea:

```text
labs/m05/context-optimized.md
```

Restriccción:

```text
máximo 1.200 reference tokens
```

Puedes:

- conservar fragmentos literales;
- eliminar secciones;
- comprimir información;
- eliminar redundancia.

Debes mantener claramente:

```text
source
authority
freshness
```

No puedes:

- inventar información;
- convertir hipótesis en hechos;
- eliminar una restriccción necesaria para responder;
- cambiar métricas.

---

# 6. Medir el contexto optimizado

Ejecuta:

```bash
python labs/m05/analyze.py labs/m05/context-optimized.md
```

Compara:

```text
FULL CONTEXT
vs
OPTIMITED CONTEXT
```

Registra:

- reference tokens;
- reducción porcentual;
- TTFT estimado;
- coste por petición;
- coste en conversación multi-turno.

---

# 7. Repetir exactamente la misma tarea

Abre una conversación nueva:

```text
/chat new
```

Utiliza exactamente el mismo prompt del baseline, cambiando solo:

```text
@labs/m05/context.md
```

por:

```text
@labs/m05/context-optimized.md
```

Puntúa otra vez sobre 5.

La optimización es satisfactoria si:

```text
reduce contexto
sin degradar la calidad necesaria
```

Una reducción de tokens que baja la puntuación no es automáticamente una mejora.

---

# 8. Contexto acumulado en una conversación

Ahora ejecuta:

```bash
python labs/m05/analyze.py \
  labs/m05/context.md \
  --turns 10 \
  --output-tokens 220
```

Después:

```bash
python labs/m05/analyze.py \
  labs/m05/context-optimized.md \
  --turns 10 \
  --output-tokens 220
```

El script simula:

- reenvío del contexto en cada turno;
- crecimiento del historial;
- coste acumulado;
- último TTFT estimado;
- ahorro si el prefijo estable puede reutilizarse mediante caching.

Observa que una conversación larga no cuesta únicamente:

```text
tokens del último mensaje
```

Cada turno puede volver a incorporar:

```text
system/context
+ historial anterior
+ nuevo input
```

---

# 9. Prompt caching: qué es estable y qué es dinámico

Divide conceptualmente tu `context-optimized.md` en dos bloques.

## STATIC

Información reutilizable entre peticiones:

- políticas;
- instrucciones;
- runbooks estables.

## DYNAMIC

Información que cambia por petición:

- telemetría actual;
- estado del incidente;
- hora del último update.

Anota en la hoja:

```text
STATIC:
...

DYNAMIC:
...
```

Pregunta:

> Si un proveedor ofrece prompt caching, ¿qué bloque intentarías mantener estable y por qué?

---

# 10. Modelo répido vs modelo más costoso

El script utiliza dos perfiles de entrenamiento:

```text
FAST
DEEP
```

Ejecuta:

```bash
python labs/m05/analyze.py \
  labs/m05/context-optimized.md \
  --turns 10 \
  --output-tokens 220 \
  --profiles
```

Compara:

- coste;
- TTFT;
- tiempo de generación;
- coste acumulado.

Ahora decide:

### Tarea A

```text
Extraer:
incident_id
region
availability
error_rate
p95_latency
```

### Tarea B

```text
Analizar evidencia contradictoria y redactar una recomendación operativa
respetando políticas, frescura y nivel de autoridad de las fuentes.
```

¿Utilizarías necesariamente el mismo modelo para A y B?

Justifica tu decisión en términos de:

```text
calidad requerida
riesgo
coste
latencia
```

---

# 11. Unit economics

Imagina:

```text
5.000 solicitudes al día
30 días al mes
```

Utiliza los costes estimados por el script para calcular:

```text
coste mensual FULL
coste mensual OPTIMITED
ahorro mensual estimado
```

Puedes hacerlo con calculadora o Python.

Después responde:

> ¿Qué variable ha producido más ahorro: reducir output, reducir contexto, usar caching o cambiar de perfil de modelo?

No hay una respuesta universal. Utiliza los números de tu experimento.

---

# 12. Conclusión

Completa:

```text
labs/m05/worksheet.md
```

Debes poder explicar:

```text
más contexto ≠ mejor contexto
menos tokens ≀ mejor sistema
caching ≠ pruning
modelo más potente ≠ modelo obligatorio
coste por request ≀ coste real de una conversación
```

La decisión final debe basarse en:

> **calidad suficiente por unidad de coste y latencia.**
