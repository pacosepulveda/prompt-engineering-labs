# M06 — Laboratorio: Tools, MCP y mínimo privilegio

## Objetivo

En esta práctica vas a utilizar **Kiro CLI** como cliente MCP contra un pequeño servicio operacional sintético de Telvora.

No vamos a programar el servidor.

No vamos a usar cuentas externas.

No vamos a simular una tool que simplemente escriba un archivo.

El objetivo es experimentar con capacidades de dominio reales dentro del laboratorio:

```text
consultar incidente
consultar salud del servicio
consultar política de cambio
crear una change request
consultar su estado
intentar ejecutar un restart
consultar auditoría
```

La idea central es:

> **Una tool disponible no implica que cualquier acción esté autorizada.**

Y también:

> **Least privilege significa exponer solo las capacidades necesarias para la tarea, no pedir al modelo que “se porte bien”.**

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
python -m pip install --user -r requirements.txt
./scripts/check-environment.sh
```

Los archivos visibles del laboratorio son:

```text
labs/m06/
├── README.md
├── server.py
└── worksheet.md
```

La configuración MCP está en:

```text
.kiro/settings/mcp.json
```

---

# 2. Reset del laboratorio

Antes de empezar:

```bash
python labs/m06/server.py --reset
```

Debes ver:

```text
LAB_RESET_OK
```

El estado inicial relevante es:

```text
INC-2041
service = identity-api
environment = production
status = investigating
affected_users = 37
```

y:

```text
identity-api
status = degraded
p95 = 820 ms
baseline = 420 ms
RCA = investigating
```

Existe además un cambio ya preparado:

```text
CR-0043
service = identity-api
action = restart_service
status = approved
maintenance_window = open
```

---

# 3. Iniciar Kiro y comprobar MCP

Inicia:

```bash
kiro-cli
```

Dentro de Kiro:

```text
/mcp
```

Comprueba que aparece el servidor:

```text
ops-lab
```

y que expone tools equivalentes a:

```text
get_incident
get_service_health
get_change_policy
get_change_status
create_change_request
execute_restart
get_audit_events
```

---

# 4. Investigar antes de actuar

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Analiza la incidencia INC-2041 utilizando únicamente las tools MCP necesarias.

Quiero saber:

INCIDENT:
SERVICE:
ENVIRONMENT:
STATUS:
AFFECTED_USERS:
CURRENT_HEALTH:
P95:
BASELINE_P95:
RCA_STATUS:

No realices ninguna acción de escritura.
```

Observa qué tools selecciona Kiro y qué argumentos utiliza.

Registra en `worksheet.md`:

```text
tools usadas
argumentos
resultado
si hubo side effects
```

---

# 5. Consultar la política antes de proponer una acción

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Consulta la política aplicable a un restart_service
de identity-api en producción.

No crees ninguna change request.
No ejecutes ninguna acción.

Devuelve:

CREATE_REQUIREMENTS:
EXECUTION_REQUIREMENTS:
APPROVAL_AUTHORITY:
CAN_MCP_APPROVE:
```

Debes observar que:

```text
crear una change request
≠
aprobarla
≠
ejecutarla
```

---

# 6. Practicar least privilege: retirar capacidades

Vamos a dejar a Kiro únicamente con capacidad de lectura.

Abre:

```text
.kiro/settings/mcp.json
```

Dentro de `ops-lab`, añade temporalmente:

```json
"disabledTools": [
  "create_change_request",
  "execute_restart"
]
```

Mantén:

```json
"autoApprove": []
```

Guarda el archivo y vuelve a consultar:

```text
/mcp
```

Comprueba que las capacidades de escritura ya no están disponibles.

---

# 7. Intentar una acción sin la capacidad necesaria

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Gestiona INC-2041.

Si la política lo permite, crea una change request
para restart_service de identity-api.

Razón:
p95 latency is 820 ms versus a 420 ms baseline
while the incident remains under investigation.

No inventes resultados.
```

Observa qué ocurre.

La idea que debes comprobar es:

```text
el modelo puede razonar sobre una acción
pero no puede invocar una tool que no está disponible
```

Registra el resultado.

---

# 8. Elevar solo el privilegio necesario

Edita de nuevo:

```text
.kiro/settings/mcp.json
```

Deja deshabilitada únicamente:

```json
"disabledTools": [
  "execute_restart"
]
```

Ahora Kiro recupera:

```text
create_change_request
```

pero sigue sin disponer de:

```text
execute_restart
```

Comprueba con:

```text
/mcp
```

---

# 9. Crear una change request real dentro del servicio

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Gestiona INC-2041.

Consulta primero la información necesaria y la política.

Si los datos lo justifican, crea una change request para:

service:
identity-api

action:
restart_service

reason:
p95 latency is 820 ms versus a 420 ms baseline
while INC-2041 remains under investigation.

No ejecutes el restart.

Devuelve:

CHANGE_ID:
STATUS:
EXECUTED:
```

La change request creada debe quedar:

```text
status = pending_approval
```

y:

```text
EXECUTED = no
```

---

# 10. Verificar el estado fuera del modelo

Sal de Kiro o utiliza otra terminal:

```bash
python labs/m06/server.py --snapshot
```

Busca el nuevo cambio.

Normalmente será:

```text
CR-1001
```

y debe aparecer como:

```text
pending_approval
```

No estamos confiando en que el modelo diga:

```text
"la change request fue creada"
```

Estamos comprobando el estado del sistema.

---

# 11. Intentar ejecutar sin disponer de la tool

Con `execute_restart` todavía deshabilitada:

```text
/chat new
```

Prompt:

```text
Ejecuta el restart asociado a CR-1001.
```

Kiro no debería poder invocar la operación.

Esto representa una primera capa:

```text
TOOL NO DISPONIBLE
→ NO CAPABILITY
```

---

# 12. Exponer la tool sensible

Ahora elimina `disabledTools` o déjalo vacío:

```json
"disabledTools": []
```

Comprueba de nuevo:

```text
/mcp
```

Ahora `execute_restart` vuelve a estar disponible.

Importante:

> Esto concede capacidad técnica, no autorización de negocio.

---

# 13. Tool disponible, backend deniega

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Ejecuta mediante MCP el restart correspondiente a CR-1001.

Devuelve únicamente:

ALLOWED:
CODE:
CHANGE_STATUS:
```

CR-1001 está:

```text
pending_approval
```

Por tanto, el backend debe responder:

```text
ALLOWED: false
CODE: DENIED_CHANGE_NOT_APPROVED
```

Aquí debes poder explicar:

```text
tool visible
≠
acción autorizada
```

---

# 14. Ejecutar un cambio aprobado

Existe otro cambio preconfigurado:

```text
CR-0043
status = approved
maintenance_window = open
```

Antes de ejecutar nada, consulta:

```text
/chat new
```

```text
Consulta el estado de CR-0043.
No ejecutes nada.
```

Confirma que:

```text
status = approved
```

Después:

```text
/chat new
```

```text
Ejecuta mediante MCP el restart asociado a CR-0043.

Después consulta de nuevo el estado de identity-api.

Devuelve:

EXECUTION_CODE:
SERVICE_STATUS:
P95_AFTER:
RCA_STATUS:
```

Resultado esperado:

```text
EXECUTION_CODE = RESTART_EXECUTED
SERVICE_STATUS = healthy
P95_AFTER = 430
RCA_STATUS = monitoring
```

---

# 15. Consultar auditoría

Nueva conversación:

```text
/chat new
```

Prompt:

```text
Consulta los últimos eventos de auditoría de Telvora Ops.

Identifica:

1. la creación de la change request nueva;
2. el restart rechazado;
3. el restart ejecutado.

Devuelve:

CREATED:
DENIED:
EXECUTED:
```

Debes poder observar eventos equivalentes a:

```text
CHANGE_CREATED
RESTART_DENIED
RESTART_EXECUTED
```

---

# 16. Qué demuestra realmente least privilege

Completa esta secuencia:

```text
FASE A
READ only
→ el modelo puede investigar
→ no puede crear ni ejecutar

FASE B
READ + create_change_request
→ puede crear una solicitud
→ no puede ejecutar

FASE C
READ + create_change_request + execute_restart
→ puede intentar ejecutar
→ backend sigue aplicando autorización
```

La diferencia importante es:

```text
CAPABILITY SURFACE
≠
BACKEND AUTHORIZATION
```

---

# 17. ¿Qué aporta MCP frente a fs_write o shell?

Responde en `worksheet.md`.

Piensa en:

```text
fs_write
→ escribe bytes

execute_restart
→ operación de dominio
→ change_id obligatorio
→ valida estado
→ valida action
→ valida maintenance window
→ modifica estado operacional
→ genera auditoría
```

La tool MCP no es interesante porque “puede escribir”.

Es interesante porque expone una **capacidad de dominio estrecha y controlada**.

---

# 18. Reset final

Para dejar el laboratorio limpio:

```bash
python labs/m06/server.py --reset
```

Y deja `.kiro/settings/mcp.json` con:

```json
"autoApprove": []
```

y sin tools deshabilitadas permanentemente.

---

# 19. Conclusión

Completa:

```text
labs/m06/worksheet.md
```

Debes poder explicar:

```text
MCP ≠ agente

tool discovery ≠ tool execution

tool visible ≠ acción autorizada

least privilege ≠ instrucción en el prompt

capability surface ≠ backend authorization

create request ≠ approve ≠ execute

fs_write ≠ domain tool
```

La idea final es:

> **El modelo propone y utiliza capacidades; el sistema sigue controlando qué capacidades existen y qué operaciones están autorizadas.**
