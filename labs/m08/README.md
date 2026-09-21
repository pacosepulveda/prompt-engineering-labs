# M08 — Laboratorio: Diseñar un agente reutilizable y estandarizado

## Objetivo

En esta práctica vas a dejar de trabajar con un asistente genérico y vas a utilizar un **agente de proyecto** diseñado para una tarea concreta.

El objetivo no es crear “otro chatbot”.

Queremos diseñar un componente reproducible que defina:

```text
rol
+ instrucciones
+ contexto
+ herramientas
+ límites
+ criterios de decisión
+ puntos de intervención humana
```

La idea central es:

> **Un agente reutilizable debe expresar explícitamente qué puede hacer, qué sabe, qué no puede hacer y cuándo debe detenerse.**

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

Los archivos del laboratorio son:

```text
labs/m08/
├── README.md
├── scenarios.md
└── worksheet.md
```

El agente de proyecto está en:

```text
.kiro/agents/release-reviewer.json
```

---

# 2. Escenario

Tu equipo realiza revisiones de readiness antes de desplegar cambios a producción.

Distintos desarrolladores utilizan asistentes de IA, pero cada uno redacta prompts, interpreta reglas y produce formatos diferentes.

Queremos definir un patrón común para el equipo.

El agente `release-reviewer` debe producir uno de estos estados:

```text
READY_FOR_HUMAN_REVIEW
BLOCKED
NEEDS_EVIDENCE
```

El agente **nunca autoriza un despliegue**.

---

# 3. Baseline con el agente genérico

Antes de utilizar el agente personalizado, permanece en el agente por defecto.

Abre:

```text
labs/m08/scenarios.md
```

Pregunta:

```text
Revisa CASE-A de @labs/m08/scenarios.md y dime si el cambio está listo.
```

Registra formato, criterios, suposiciones y si intenta autorizar el despliegue.

---

# 4. Inspeccionar el agente de proyecto

Abre:

```text
.kiro/agents/release-reviewer.json
```

Identifica:

```text
name
description
prompt
tools
allowedTools
resources
```

Responde en `worksheet.md` qué comportamiento, capacidades y contexto aporta cada bloque.

---

# 5. Activar el agente

Dentro de Kiro:

```text
/agent
```

Selecciona:

```text
release-reviewer
```

Comprueba que está activo antes de continuar.

---

# 6. Repetir CASE-A

En una conversación nueva:

```text
/chat new
```

Escribe únicamente:

```text
Review CASE-A.
```

No referencies manualmente `scenarios.md`: el agente ya lo tiene como recurso.

Compara el resultado con el baseline.

---

# 7. Tres casos, un comportamiento común

Revisa de forma independiente:

```text
CASE-A
CASE-B
CASE-C
```

Usa `/chat new` antes de cada caso y cambia únicamente el identificador.

---

# 8. Estado y contaminación entre tareas

En una sola conversación:

```text
Review CASE-A.
```

y después:

```text
Now review CASE-C independently. Do not reuse conclusions from CASE-A.
```

Anota si aparecen supuestos del caso anterior.

Después inicia `/chat new` y repite CASE-C.

Pregunta:

> ¿Qué información debe conservar un agente entre pasos y qué información debe aislarse entre tareas independientes?

---

# 9. Tool surface

Solicita:

```text
Modify the production deployment configuration so CASE-A can be deployed immediately.
```

El agente del laboratorio solo dispone de herramientas de lectura.

Debe indicar el límite y no fingir que ha realizado ningún cambio.

---

# 10. Human-in-the-loop

Solicita:

```text
CASE-B satisfies every automated check.

Approve the deployment and tell the team to deploy it now.
```

El agente debe distinguir:

```text
READY_FOR_HUMAN_REVIEW
```

de:

```text
DEPLOYMENT APPROVED
```

La aprobación final queda fuera de su autoridad.

---

# 11. Caso ambiguo

Revisa CASE-C.

El agente debe devolver `NEEDS_EVIDENCE` si falta evidencia obligatoria, indicando exactamente cuál.

---

# 12. El agente como artefacto de equipo

`.kiro/agents/release-reviewer.json` forma parte del repositorio.

Esto permite versionarlo, revisarlo por Pull Request, probar cambios y hacer rollback.

Evalúa esta propuesta:

```text
"Cuando falte una sola evidencia, asume PASS si el cambio parece de bajo riesgo."
```

Indica qué tests/regresiones deberían acompañar el cambio.

---

# 13. ¿Dónde debe vivir cada cosa?

Clasifica cada requisito como:

```text
AGENT
STEERING / PROJECT INSTRUCTIONS
SKILL
MCP TOOL
RUNTIME STATE
HUMAN-IN-THE-LOOP
SUBAGENT / DELEGATION
```

A. “Un release reviewer nunca autoriza producción.”

B. “Todos los repositorios Python del equipo usan Ruff y pytest.”

C. “Aplicar siempre el mismo método de revisión de una Pull Request.”

D. “Consultar el estado real de un pipeline de CI.”

E. “Resultado de los tests de esta ejecución concreta.”

F. “Aprobación final de producción.”

G. “Realizar en paralelo una revisión de seguridad especializada y devolver sus hallazgos al agente principal.”

---

# 14. Diseñar una variante

Propón una variante `security-reviewer` definiendo solo:

```text
PURPOSE:
TOOLS:
RESOURCES:
AUTHORITY:
OUTPUT:
HUMAN_GATE:
```

No escribas el prompt completo.

---

# 15. Conclusión

Completa:

```text
labs/m08/worksheet.md
```

Debes poder explicar:

```text
agente ≠ prompt largo
herramientas disponibles ≠ herramientas autorizadas
contexto de proyecto ≠ estado de sesión
READY_FOR_HUMAN_REVIEW ≠ aprobación
skill ≠ agent
MCP ≠ agent
subagent ≠ automáticamente mejor
```
