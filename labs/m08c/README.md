# M08C — Reto: investigación FinOps autónoma

## Objetivo

En M08 y M08B has trabajado con agentes reutilizables, límites, delegación y multi-agente.

En este reto el foco cambia:

> **dar al agente un objetivo y dejar que realice una investigación larga por sí mismo.**

No vas a ejecutar manualmente una lista de comprobaciones.

El agente deberá decidir qué evidencia necesita, consultar herramientas, correlacionar resultados, cuantificar hallazgos y preparar un informe final.

---

## Escenario

El equipo FinOps ha detectado un aumento inesperado del run-rate semanal de cloud.

El caso es:

```text
COST-2026-09
```

El agente dispone de:

- un brief del caso;
- una política de investigación;
- una herramienta read-only que simula consultas a billing, inventario, cambios, métricas y pricing;
- permiso para escribir únicamente el informe del laboratorio.

No dispone de capacidad para modificar recursos cloud.

---

## Preparación

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

Crea una conversación nueva:

```text
/chat new
```

Selecciona:

```text
/agent
```

Y activa:

```text
m08c-cost-investigator
```

---

## La tarea

Envía únicamente:

```text
Investigate COST-2026-09 and prepare the final FinOps investigation report.
```

No ejecutes tú las consultas de investigación.

No le indiques qué comandos debe utilizar ni en qué orden.

Observa cómo trabaja el agente.

---

## Qué debes observar

Durante la ejecución, fíjate en si el agente:

- descubre cómo utilizar `cloud_ops.py`;
- empieza por caracterizar la anomalía antes de saltar a una causa;
- identifica los principales drivers del incremento;
- decide qué recursos merecen investigación adicional;
- consulta cambios, métricas, tags y pricing cuando lo necesita;
- cambia el siguiente paso según lo que encuentra;
- distingue evidencia confirmada, hipótesis y desconocidos;
- cuantifica oportunidades de ahorro;
- respeta el human gate y no afirma haber modificado recursos;
- escribe por sí mismo el informe final.

No existe una secuencia exacta de tool calls obligatoria.

Lo importante es que las decisiones estén fundamentadas en evidencia.

---

## Resultado

Al terminar debe existir:

```text
labs/m08c/work/COST-2026-09-report.md
```

Puedes abrirlo directamente desde VS Code o comprobarlo con:

```bash
cat labs/m08c/work/COST-2026-09-report.md
```

---

## Reflexión final

Responde brevemente:

1. ¿Qué decisiones tomó el agente que no estaban escritas en tu prompt?
2. ¿Qué tool call cambió de forma más clara el siguiente paso de la investigación?
3. ¿Qué conclusión habría sido peligrosa si el agente hubiese confundido hipótesis con evidencia?
4. ¿Qué acciones quedaron correctamente reservadas para una persona?
5. ¿En qué se diferencia esta ejecución de pedir a un modelo que resuma tres documentos?
