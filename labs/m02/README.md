# M02 — Laboratorio: Del prompt ambiguo a una especificación evaluable

## Objetivo

En esta práctica vas a trabajar con un prompt como si fuera un componente de ingeniería:

```text
baseline
  ↓
prompt V1
  ↓
prueba con varios casos
  ↓
detección de un fallo
  ↓
cambio controlado
  ↓
prompt V2
  ↓
regression test
```

No buscamos un “prompt perfecto”. Buscamos un comportamiento que puedas explicar y evaluar.

---

## Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

Mantén el mismo modelo durante toda la comparación.

Antes de cada prueba independiente:

```text
/chat new
```

---

# 1. Escenario

Trabajas con un equipo de **Network Operations**.

Quieres utilizar un LLM para realizar un primer triaje de incidencias.

El modelo debe:

- asignar severidad;
- justificarla con hechos del caso;
- indicar información relevante ausente;
- proponer una comprobación diagnóstica y reversible.

El modelo no debe:

- inventar causas;
- tratar hipótesis como hechos;
- recomendar cambios de red;
- completar datos ausentes mediante suposiciones.

La política está en:

```text
labs/m02/policy.md
```

Los tres casos están en:

```text
labs/m02/cases.md
```

---

# 2. Baseline

Utiliza únicamente el caso `INC-117`.

En una conversación nueva:

```text
Analiza el caso INC-117 de @labs/m02/cases.md y dime qué harías.
```

No añadas la política todavía.

En `labs/m02/worksheet.md` anota:

- qué severidad asigna;
- qué criterio parece utilizar;
- si inventa alguna causa;
- si distingue hechos de hipótesis;
- si la siguiente acción es reversible;
- si el formato sería reutilizable.

La pregunta es:

> ¿Puede el modelo saber qué significa “correcto” si todavía no le hemos dado la política?

---

# 3. Crear prompt V1

Lee:

```text
labs/m02/policy.md
```

Crea:

```text
labs/m02/work/prompt-v1.md
```

Tu prompt debe incluir explícitamente:

1. **Tarea**
2. **Contexto**
3. **Entrada**
4. **Restricciones**
5. **Output contract**
6. **Criterios de éxito**

El output debe contener exactamente:

```text
SEVERITY:
EVIDENCE:
MISSING_DATA:
NEXT_CHECK:
```

Reglas mínimas:

- `SEVERITY`: `P1`, `P2`, `P3` o `UNDETERMINED`;
- `EVIDENCE`: solo hechos del caso y la política;
- `MISSING_DATA`: información relevante ausente;
- `NEXT_CHECK`: una única comprobación diagnóstica y reversible;
- no afirmar una RCA si no está confirmada;
- no recomendar reinicios, rollbacks ni cambios de configuración.

---

# 4. Test set

Prueba el mismo `prompt-v1.md` con:

```text
INC-117
INC-305
INC-613
```

Para cada caso:

1. ejecuta `/chat new`;
2. usa el mismo modelo;
3. usa la misma política;
4. cambia únicamente el caso.

Mensaje recomendado:

```text
Aplica exactamente @labs/m02/work/prompt-v1.md.

Política:
@labs/m02/policy.md

Analiza únicamente el caso INC-117 de:
@labs/m02/cases.md

No modifiques archivos ni ejecutes acciones.
```

Cambia solo el identificador del caso.

---

# 5. Evaluación

Puntúa cada respuesta con 0 o 1 en estos criterios:

| Criterio | 1 punto si... |
|---|---|
| Severidad | aplica correctamente la política |
| Grounding | la evidencia existe realmente |
| RCA | no convierte hipótesis en causa confirmada |
| Missing data | detecta ausencias relevantes |
| Next check | es diagnóstico y reversible |
| Output contract | respeta las cuatro secciones |

Máximo:

```text
6 puntos por caso
18 puntos en total
```

Registra los resultados en:

```text
labs/m02/worksheet.md
```

---

# 6. Diagnosticar antes de modificar

Si una respuesta falla, no cambies inmediatamente el prompt.

Clasifica primero el problema:

```text
INSTRUCTION
CONTEXT
CONSTRAINT
OUTPUT_CONTRACT
SUCCESS_CRITERIA
MODEL_VARIANCE
```

Escribe qué evidencia te hace pensar que el fallo pertenece a esa categoría.

---

# 7. Crear V2 con un solo cambio

Duplica tu prompt:

```bash
cp labs/m02/work/prompt-v1.md labs/m02/work/prompt-v2.md
```

Modifica **una sola cosa**.

Por ejemplo:

- aclarar cuándo usar `UNDETERMINED`;
- reforzar que una hipótesis no es una RCA;
- aclarar una condición lógica `AND`;
- precisar el formato esperado.

Antes de probar escribe:

```text
Hipótesis:
Creo que el fallo se debe a...

Cambio:
Voy a modificar...

Resultado esperado:
Espero que mejore... sin empeorar...
```

---

# 8. Regression test

Repite exactamente los tres casos con `prompt-v2.md`.

Compara:

```text
V1 vs V2
```

Responde:

- ¿desapareció el fallo?
- ¿mejoró la puntuación total?
- ¿apareció alguna regresión?
- ¿el prompt se volvió innecesariamente más complejo?
- ¿el problema debería resolverse realmente con prompting?

---

# 9. Resultado final

Al terminar debes tener:

```text
labs/m02/work/prompt-v1.md
labs/m02/work/prompt-v2.md
labs/m02/worksheet.md
```

Y debes poder justificar:

> **qué cambiaste, por qué lo cambiaste y qué evidencia demuestra si funcionó.**
