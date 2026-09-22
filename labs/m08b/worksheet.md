# M08B — Hoja de trabajo

## 1. Arquitectura

```text
Orquestador:
Subagente Security:
Subagente Operations:

Contexto del orquestador:
Contexto exclusivo de Security:
Contexto exclusivo de Operations:

Tools del orquestador:
Tools de Security:
Tools de Operations:
```

## 2. Baseline single-agent

```text
Caso:
Decisión:
Número de agentes:
Trazabilidad:
Observaciones:
```

## 3. Multi-agent

| Caso | Security | Operations | Decisión final | Correcto |
|---|---|---|---|---|
| MA-CASE-A | | | | |
| MA-CASE-B | | | | |
| MA-CASE-C | | | | |

## 4. Paralelismo y aislamiento

```text
¿Se lanzaron dos subagentes?:
¿Trabajaron con contexto aislado?:
¿El orquestador accedió directamente a la evidencia especializada?:
¿Qué se compartió realmente entre agentes?:
```

## 5. Prueba de especialización

```text
Security intentando evaluar Operations:
Resultado:

Operations intentando evaluar Security:
Resultado:

¿Por qué no deben inferir el dominio que no poseen?:
```

## 6. Human gate

```text
Petición:
Review MA-CASE-A and, if it passes, approve the production deployment.

Respuesta:
¿Autorizó producción?:
¿Por qué?:
```

## 7. availableAgents

```text
Petición de tercer agente:
Resultado:
¿Se creó?:
¿Qué controla availableAgents?:
¿Qué diferencia tiene con trustedAgents?:
```

## 8. Single vs multi-agent

| Dimensión | Single agent | Multi-agent |
|---|---|---|
| Model calls | | |
| Context isolation | | |
| Especialización | | |
| Trazabilidad | | |
| Latencia percibida | | |
| Complejidad | | |
| Calidad del resultado | | |

## 9. Decisión arquitectónica

```text
¿Era necesario multi-agent para resolver estos tres casos?:

¿Qué valor aporta aun cuando la respuesta sea la misma?:

¿Qué overhead introduce?:

¿En qué escenario empresarial justificarías esta arquitectura?:
```

## 10. Conclusión

```text
Multi-agent ≠

Subagent ≠

Parallelism ≠

Context isolation ≠

Specialization ≠

Orchestrator ≠

availableAgents ≠

trustedAgents ≠
```
