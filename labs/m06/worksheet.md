# M06 — Hoja de trabajo

## 1. Contratos

### get_service_status

```text
Argumentos:

Tipo de resultado:

Side effects:

Información que verá el modelo:
```

### create_change_request

```text
Argumentos:

Tipo de resultado:

Side effects:

Información que verá el modelo:
```

---

## 2. READ call

```text
Tool:

Argumentos:

Resultado:

¿Requirió aprobación?:

¿Había side effects?:
```

---

## 3. Argumento inválido

```text
Solicitud:
legacy-api

¿Qué ocurrió?:

¿Qué parte del contrato limitaba el valor?:
```

---

## 4. WRITE call

```text
Tool:

Service:

Change type:

Reason:

¿Aprobaste?:

Change ID:

¿Se verificó en changes.jsonl?:
```

---

## 5. Least privilege

```text
¿Qué ocurrió al deshabilitar create_change_request?:

¿Qué riesgo reduce disabledTools?:

¿Qué riesgo NO elimina?:
```

---

## 6. Auto-approval

```text
¿Auto-aprobarías get_service_status?:

Justificación:

¿Auto-aprobarías create_change_request?:

Justificación:
```

---

## 7. MCP vs shell

| Aspecto | Shell genérico | MCP específica |
|---|---|---|
| Descubrimiento | | |
| Schema de argumentos | | |
| Descripción semántica | | |
| Superficie de permisos | | |
| Portabilidad | | |
| Side effects | | |

---

## 8. Diseño de tools

```text
¿Por qué get_service_status(service) es mejor que do_action(command)?

¿Qué argumentos eliminarías si no fueran necesarios?

¿Dónde aplicarías autorización real en producción?
```

---

## 9. Conclusión

```text
MCP ≠

Tool call ≠

disabledTools ≠

Una tool read-only puede...

Una tool con side effects debe...

El principio de mínimo privilegio aplicado a MCP significa...
```
