# M04 — Hoja de trabajo

## Modelo utilizado

```text
Modelo:
```

# A. "Devuelve JSON"

```text
¿JSON sintácticamente válido?
¿Añadió Markdown?
¿Campos estables?
¿Tipos estables?
¿Inventó información?
¿Qué contrato existía realmente?
```

# B. Validación V1

| Capa | Resultado | Error observado |
|---|---|---|
| Syntax | | |
| Schema | | |
| Semantic | | |

# C. Tipos de fallo

| Archivo | Syntax | Schema | Semantic | Causa |
|---|---|---|---|---|
| invalid-syntax.json | | | | |
| invalid-schema.json | | | | |
| invalid-semantic.json | | | | |

# D. Repair loop

```text
Error inicial:
Cambio realizado:
Resultado del retry:
¿Cambió algo no relacionado con el error?
```

# E. Casos adicionales

| Caso | Schema valid | Semantic valid | Sensitive data handled | Acción |
|---|---|---|---|---|
| TKT-1057 | | | | |
| TKT-1099 | | | | |

# F. Formatos

```text
¿Cuándo usarías LLM para transformar formato?
¿Cuándo usarías un serializer determinista?
```

# G. Tool call

```text
Tool propuesta:
Argumentos:
¿Pasó schema?
¿Pasó allowlist?
TOOL_RESULT:
```

# H. Responsabilidades

```text
PROMPT es responsable de:
JSON SCHEMA es responsable de:
VALIDADOR SEMÁNTICO es responsable de:
RUNTIME es responsable de:
TOOL es responsable de:
```

# Conclusión

```text
¿Qué diferencia hay entre JSON válido y output válido?
¿Qué problema resuelve validator → repair → retry?
¿Por qué una tool call no debe ejecutarse automáticamente?
¿Qué guardarías en el repositorio como artefacto reutilizable?
```
