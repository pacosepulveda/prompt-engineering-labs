# M02 — Hoja de trabajo

## Modelo utilizado

```text
Modelo:
```

---

## Baseline — INC-117

### Observaciones

```text
¿Asignó severidad?

¿Con qué criterio?

¿Inventó alguna causa?

¿Diferenció hechos e hipótesis?

¿Propuso una comprobación reversible?

¿El formato fue estable?
```

---

# V1

## Hipótesis de diseño

```text
¿Qué propiedades intentas garantizar con prompt-v1.md?
```

## Test set principal

| Caso | Severidad esperada según tu lectura de la política | Severidad modelo | Grounding | RCA | Missing data | Next check | Output | Total /6 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| INC-117 |  |  |  |  |  |  |  |  |
| INC-204 |  |  |  |  |  |  |  |  |
| INC-305 |  |  |  |  |  |  |  |  |
| INC-411 |  |  |  |  |  |  |  |  |

## Stress test

| Caso | Severidad esperada según tu lectura de la política | Severidad modelo | Grounding | RCA | Missing data | Next check | Output | Total /6 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| INC-512 |  |  |  |  |  |  |  |  |
| INC-613 |  |  |  |  |  |  |  |  |

### Total V1

```text
/ 36
```

---

# Diagnóstico

```text
Caso que quieres mejorar:

Categoría del fallo:
[ ] Instrucción
[ ] Contexto
[ ] Restricción
[ ] Output contract
[ ] Criterio de éxito
[ ] Modelo / comportamiento no determinista

Evidencia del fallo:
```

---

# Cambio V2

```text
Hipótesis:

Creo que el fallo se debe a:


Cambio:

Voy a modificar:


Resultado esperado:

Espero que mejore:

sin empeorar:
```

---

# Regression test — V2

| Caso | Resultado V1 /6 | Resultado V2 /6 | Mejora / igual / regresión | Observaciones |
|---|---:|---:|---|---|
| INC-117 |  |  |  |  |
| INC-204 |  |  |  |  |
| INC-305 |  |  |  |  |
| INC-411 |  |  |  |  |
| INC-512 |  |  |  |  |
| INC-613 |  |  |  |  |

### Total V2

```text
/ 36
```

---

# Conclusión

```text
¿Qué cambió entre V1 y V2?


¿Hay evidencia de mejora?


¿Apareció alguna regresión?


¿Qué parte trasladarías a código determinista si esto fuese producción?


¿Qué has aprendido sobre la diferencia entre "un prompt que funciona" y
"un comportamiento evaluado"?
```
