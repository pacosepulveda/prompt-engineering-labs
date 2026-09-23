# M06 — Hoja de trabajo

## 1. Discovery

```text
Servidor MCP:

Tools descubiertas:

¿Cuáles son READ?:

¿Cuáles tienen side effects?:
```

---

## 2. Investigación de INC-2041

```text
Tools utilizadas:

Service:

Environment:

Status:

Affected users:

P95:

Baseline:

RCA status:

¿Hubo side effects?:
```

---

## 3. Política

```text
Requisitos para crear change request:

Requisitos para ejecutar restart:

Autoridad de aprobación:

¿Puede MCP aprobar el cambio?:
```

---

## 4. Least privilege — READ only

```text
Tools WRITE deshabilitadas:

¿Qué pidió el usuario?:

¿Qué pudo hacer Kiro?:

¿Qué NO pudo hacer?:

¿Por qué esto es más fuerte que escribir "no ejecutes" en el prompt?:
```

---

## 5. Elevación mínima

```text
Tool WRITE habilitada:

Tool sensible todavía deshabilitada:

Change ID creado:

Estado:

¿Fue ejecutado?:
```

---

## 6. Verificación externa

```text
Comando utilizado:

¿Aparece la change request?:

Estado observado:
```

---

## 7. Capability vs authorization

### Intento con CR pendiente

```text
Change ID:

Tool disponible:

Resultado:

Código de denegación:

¿Qué control actuó?:
```

### Intento con CR aprobado

```text
Change ID:

Estado previo:

Resultado:

Service status después:

P95 después:
```

---

## 8. Auditoría

```text
Evento de creación:

Evento denegado:

Evento ejecutado:

¿Por qué es útil una auditoría fuera de la respuesta del modelo?:
```

---

## 9. MCP vs filesystem

| Aspecto | fs_write / shell genérico | Tool MCP de dominio |
|---|---|---|
| Intención semántica | | |
| Schema de argumentos | | |
| Estado de negocio | | |
| Validación de política | | |
| Autorización | | |
| Auditoría | | |
| Superficie de privilegio | | |

---

## 10. Conclusión

Completa:

```text
MCP ≠

Tool discovery ≠

Tool visible ≠

Least privilege ≠

Capability surface ≠

create request ≠

fs_write ≠
```

Explica en una frase:

```text
¿Por qué una tool pequeña y de dominio puede ser más segura
que dar acceso genérico a shell/filesystem?
```
