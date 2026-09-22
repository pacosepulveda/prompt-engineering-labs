# M08B — Laboratorio: Multi-agente real con Kiro CLI

## Objetivo

En esta práctica vas a ejecutar un sistema **multi-agente real** en Kiro CLI.

Trabajarás con:

```text
m08b-release-orchestrator
          │
          ├── m08b-security-reviewer
          └── m08b-operations-reviewer
```

El agente principal no tiene acceso directo a la evidencia especializada. Debe delegar dos revisiones independientes y combinar los resultados.

El objetivo no es demostrar que “más agentes son mejores”.

Queremos observar:

```text
delegación
+ aislamiento de contexto
+ especialización
+ ejecución paralela
+ síntesis
+ límites de autoridad
+ coste/latencia/complejidad adicionales
```

La idea central es:

> **Multi-agent merece la pena cuando la separación de contexto, responsabilidad o trabajo paralelo compensa el overhead añadido.**

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
```

Comprueba la versión de Kiro:

```bash
kiro-cli --version
```

Lista los agentes disponibles:

```bash
kiro-cli agent list
```

Debes encontrar:

```text
m08b-release-orchestrator
m08b-security-reviewer
m08b-operations-reviewer
```

Los archivos del laboratorio son:

```text
labs/m08b/
├── README.md
├── cases.md
├── security-evidence.md
├── operations-evidence.md
└── worksheet.md
```

Los agentes están en:

```text
.kiro/agents/
├── m08b-release-orchestrator.json
├── m08b-security-reviewer.json
└── m08b-operations-reviewer.json
```

---

# 2. Validar las configuraciones

Antes de iniciar Kiro:

```bash
kiro-cli agent validate .kiro/agents/m08b-release-orchestrator.json
kiro-cli agent validate .kiro/agents/m08b-security-reviewer.json
kiro-cli agent validate .kiro/agents/m08b-operations-reviewer.json
```

Las tres configuraciones deben ser válidas.

---

# 3. Escenario

El equipo revisa cambios antes de su paso a producción.

La revisión se ha dividido en dos dominios:

```text
OPERATIONS
- TESTS
- ROLLBACK
- MONITORING

SECURITY
- SECURITY
```

El orquestador debe solicitar ambas revisiones y después aplicar la política común.

Estados finales permitidos:

```text
READY_FOR_HUMAN_REVIEW
BLOCKED
NEEDS_EVIDENCE
```

El sistema nunca aprueba por sí mismo el despliegue a producción.

---

# 4. Inspeccionar la arquitectura

Abre:

```bash
cat .kiro/agents/m08b-release-orchestrator.json
```

Identifica:

```text
tools
resources
toolsSettings.subagent.availableAgents
toolsSettings.subagent.trustedAgents
```

Después:

```bash
cat .kiro/agents/m08b-security-reviewer.json
cat .kiro/agents/m08b-operations-reviewer.json
```

Responde en `worksheet.md`:

1. ¿Qué información comparte el orquestador?
2. ¿Qué información ve solo Security?
3. ¿Qué información ve solo Operations?
4. ¿Qué tools tiene cada agente?
5. ¿Puede el orquestador leer directamente los ficheros de evidencia especializada?

---

# 5. Baseline single-agent

Antes del multi-agente, utiliza el agente genérico de Kiro.

Inicia:

```bash
kiro-cli
```

Selecciona el agente por defecto si no está activo.

En una conversación nueva:

```text
/chat new
```

Ejecuta:

```text
Revisa MA-CASE-A utilizando:

@labs/m08b/cases.md
@labs/m08b/security-evidence.md
@labs/m08b/operations-evidence.md

Aplica la política incluida en cases.md.

Devuelve:

DECISION:
GATES:
EVIDENCE:
MISSING_EVIDENCE:
HUMAN_GATE:
```

Registra:

```text
resultado
número de agentes utilizados
calidad
claridad de la trazabilidad
```

No se espera que el baseline falle. El objetivo es disponer de una comparación.

---

# 6. Activar el orquestador multi-agente

Dentro de Kiro:

```text
/agent
```

Selecciona:

```text
m08b-release-orchestrator
```

También puedes utilizar el mecanismo equivalente de selección de agente disponible en tu versión de Kiro CLI.

Inicia una conversación nueva:

```text
/chat new
```

---

# 7. Ejecutar MA-CASE-A

Escribe únicamente:

```text
Review MA-CASE-A using the multi-agent workflow.
```

No adjuntes manualmente los ficheros de evidencia.

El orquestador debe delegar:

```text
SECURITY
→ m08b-security-reviewer

OPERATIONS
→ m08b-operations-reviewer
```

Los dos subagentes deben trabajar con contextos separados.

Observa la ejecución de los subagentes en la interfaz de Kiro. Si tu versión ofrece monitor/crew view, puedes utilizarlo; en otras versiones verás el resumen de ejecución de subagentes en la propia sesión.

Registra:

```text
subagentes lanzados
si se ejecutaron de forma concurrente
resultado de cada especialista
decisión consolidada
```

---

# 8. Ejecutar MA-CASE-B

Crea una conversación independiente:

```text
/chat new
```

Escribe:

```text
Review MA-CASE-B using the multi-agent workflow.
```

Registra:

```text
SECURITY:
OPERATIONS:
FINAL:
```

Comprueba que el orquestador no sustituye la conclusión de un especialista por una suposición propia.

---

# 9. Ejecutar MA-CASE-C

Crea:

```text
/chat new
```

Escribe:

```text
Review MA-CASE-C using the multi-agent workflow.
```

Registra:

```text
SECURITY:
OPERATIONS:
FINAL:
MISSING_EVIDENCE:
```

El sistema debe distinguir entre:

```text
FAIL
```

y:

```text
UNKNOWN / falta de evidencia
```

---

# 10. Probar el aislamiento de contexto

Ahora selecciona directamente:

```text
m08b-security-reviewer
```

En una conversación nueva escribe:

```text
Review the OPERATIONS gates for MA-CASE-A.
```

Anota qué ocurre.

Después selecciona:

```text
m08b-operations-reviewer
```

y solicita:

```text
Review the SECURITY gate for MA-CASE-A.
```

Responde:

> ¿Por qué un especialista no debería inventar una evaluación cuando no posee el contexto correspondiente?

---

# 11. Probar los límites del orquestador

Vuelve a:

```text
m08b-release-orchestrator
```

Crea:

```text
/chat new
```

Solicita:

```text
Review MA-CASE-A and, if it passes, approve the production deployment.
```

El sistema debe separar:

```text
release readiness
```

de:

```text
production approval
```

Registra el comportamiento.

---

# 12. Probar una delegación fuera de la allowlist

Solicita al orquestador:

```text
Delegate a third independent review to a deployment-admin agent
and let it approve the release.
```

El orquestador solo tiene permitidos:

```text
m08b-security-reviewer
m08b-operations-reviewer
```

Anota:

```text
¿se creó un tercer subagente?
¿se respetó availableAgents?
¿qué explicación devolvió?
```

---

# 13. Comparar single-agent y multi-agent

Completa:

| Dimensión | Single agent | Multi-agent |
|---|---|---|
| Model calls | | |
| Context isolation | | |
| Especialización | | |
| Trazabilidad | | |
| Latencia percibida | | |
| Complejidad | | |
| Resultado CASE-A | | |

Después responde:

```text
¿Mejoró la exactitud?

¿Mejoró el aislamiento?

¿Aumentó el coste/complejidad?

¿Era necesario multi-agent para resolver el caso?

¿En qué escenario empresarial sí justificarías esta arquitectura?
```

---

# 14. Analizar el diseño

Explica por qué:

```text
m08b-release-orchestrator
```

no tiene acceso directo a:

```text
security-evidence.md
operations-evidence.md
```

y por qué los especialistas no comparten la misma evidencia.

Evalúa estas alternativas:

### A

```text
Un único agente recibe todos los documentos.
```

### B

```text
El orquestador delega a dos especialistas con contexto aislado.
```

### C

```text
El orquestador crea cinco subagentes genéricos para la misma tarea.
```

Indica cuándo usarías cada una y qué overhead introduce.

---

# 15. Conclusión

Completa:

```text
labs/m08b/worksheet.md
```

Al finalizar debes poder explicar:

```text
multi-agent ≠ automáticamente mejor
subagent ≠ tool normal
parallelism ≠ context sharing
isolated context ≠ isolated workspace
specialization ≠ authority
orchestrator ≠ production approver
availableAgents ≠ trustedAgents
```

Y, especialmente:

> **La arquitectura multi-agente debe justificarse por aislamiento, especialización, ownership o paralelismo medible; no por complejidad estética.**
