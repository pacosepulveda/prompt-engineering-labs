# M06 — Laboratorio: Construir y utilizar un servidor MCP real

## Objetivo

En esta práctica vas a conectar un LLM con herramientas externas mediante un servidor **Model Context Protocol (MCP)** real.

Construiremos un servidor mínimo con dos tools:

```text
get_service_status
        ↓
     READ ONLY

create_change_request
        ↓
       WRITE
```

El objetivo no es aprender una librería concreta.

Queremos entender esta separación:

```text
usuario
   ↓
LLM / agente
   ↓
descubre una tool
   ↓
propone argumentos
   ↓
host valida / solicita aprobación
   ↓
MCP
   ↓
servidor ejecuta
   ↓
resultado observable
```

La idea central es:

> **MCP estandariza cómo un modelo descubre e invoca capacidades; no concede autoridad automáticamente.**

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
labs/m06/
├── README.md
├── server.py
└── worksheet.md
```

La configuración MCP del proyecto está en:

```text
.kiro/settings/mcp.json
```

---

# 2. Examinar el servidor

Abre:

```text
labs/m06/server.py
```

Busca las dos funciones decoradas como tools:

```text
get_service_status
create_change_request
```

Antes de ejecutarlas, responde en `worksheet.md`:

```text
¿Qué argumentos acepta cada tool?
¿Qué tipo devuelve?
¿Cuál tiene side effects?
¿Qué información de la función verá el modelo?
```

Fíjate especialmente en:

- nombre de función;
- docstring;
- type hints;
- valores permitidos.

El SDK MCP utiliza esa información para describir la herramienta al cliente.

---

# 3. Entender stdio

Ejecuta directamente:

```bash
python labs/m06/server.py
```

No debería aparecer una interfaz ni abrirse un puerto. El proceso queda esperando.

Pulsa `Ctrl+C` para detenerlo.

¿Por qué parece que “no ocurre nada”?

Porque el servidor utiliza **stdio**:

```text
Kiro inicia el proceso
      ↓
escribe mensajes MCP en stdin
      ↓
server.py
      ↓
devuelve mensajes MCP por stdout
```

---

# 4. Ver la configuración de Kiro

Abre:

```text
.kiro/settings/mcp.json
```

Encontrarás una entrada para `ops-lab` que indica a Kiro qué comando debe utilizar para arrancar el servidor.

No contiene credenciales.

---

# 5. Conectar desde Kiro CLI

Inicia:

```bash
kiro-cli
```

Dentro de Kiro:

```text
/mcp
```

Comprueba que aparece el servidor `ops-lab` y sus tools.

---

# 6. Primera llamada: READ

En una conversación nueva:

```text
/chat new
```

Pregunta:

```text
Usa las herramientas MCP disponibles para consultar el estado actual de
identity-api.

No modifiques nada.

Devuelve:
STATUS:
EVIDENCE:
RCA_STATUS:
```

Cuando Kiro proponga la llamada, observa antes de aprobar:

```text
tool
arguments
```

Después aprueba la llamada y registra el resultado.

---

# 7. El contrato limita los argumentos

Pregunta:

```text
Consulta mediante MCP el estado de legacy-api.
No inventes el resultado.
```

`legacy-api` no pertenece al conjunto de servicios admitidos por la tool.

Observa qué ocurre y explica por qué es preferible restringir el contrato a valores que el servidor sabe procesar.

---

# 8. Segunda tool: una operación con side effect

Solicita:

```text
Crea mediante MCP una change request para identity-api.

change_type:
restart_service

reason:
p95 latency is significantly above baseline

No ejecutes el restart. Solo crea la change request.
```

Antes de aprobar, revisa:

```text
tool
service
change_type
reason
```

La tool `create_change_request` **sí tiene un side effect**.

No reinicia ningún servicio real, pero escribe una change request sintética en:

```text
labs/m06/work/changes.jsonl
```

Aprueba únicamente si los argumentos son correctos.

---

# 9. Verificar el efecto fuera del LLM

En otra terminal:

```bash
cat labs/m06/work/changes.jsonl
```

Comprueba que existe un registro.

No confiamos únicamente en que el modelo diga que la operación se realizó: verificamos un efecto observable.

---

# 10. Least privilege: ocultar la tool de escritura

Abre:

```text
.kiro/settings/mcp.json
```

Dentro de `ops-lab`, añade temporalmente:

```json
"disabledTools": [
  "create_change_request"
]
```

Guarda el archivo y consulta:

```text
/mcp
```

Ahora intenta de nuevo:

```text
Crea una change request para reiniciar identity-api.
```

Observa qué ocurre cuando esa capacidad ya no está disponible para el modelo.

Después elimina `disabledTools` para dejar el laboratorio en su estado inicial.

---

# 11. Auto-approval

La configuración inicial contiene:

```json
"autoApprove": []
```

Responde:

```text
¿Auto-aprobarías get_service_status?
¿Auto-aprobarías create_change_request?
¿Por qué?
```

Basa la decisión en:

```text
side effects
alcance
sensibilidad
confianza en el servidor
impacto de un argumento incorrecto
```

---

# 12. MCP vs acceso directo a shell

Completa:

| Aspecto | Shell genérico | Tool MCP específica |
|---|---|---|
| Descubrimiento de capacidad | | |
| Schema de argumentos | | |
| Descripción semántica | | |
| Superficie de permisos | | |
| Portabilidad entre hosts | | |
| Side effects fáciles de identificar | | |

---

# 13. Inspeccionar el contrato como parte del diseño

Vuelve a `server.py`.

Analiza:

- nombre de la tool;
- docstring;
- argumentos;
- valores permitidos;
- side effects.

Después explica por qué una tool genérica:

```text
do_action(command: str)
```

sería un contrato mucho peor.

---

# 14. Conclusión

Completa:

```text
labs/m06/worksheet.md
```

Debes poder explicar:

```text
MCP ≠ agente
MCP ≠ autorización
tool call ≠ permiso
schema ≠ seguridad completa
client-side disabledTools ≠ autorización de backend
```

Y también por qué una tool pequeña, explícita y de mínimo privilegio suele ser mejor que una tool genérica extremadamente poderosa.
