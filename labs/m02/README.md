# M02 — Laboratorio: Del prompt ambiguo a una especificación evaluable

## Curso de Prompt Engineering Avanzado

**Modalidad:** práctica guiada en clase  
**Duración estimada:** 75–90 minutos  
**Entorno recomendado:** GitHub Codespaces + Kiro CLI  
**Programación obligatoria:** no  
**Caso:** triaje de incidencias de red con datos sintéticos

---

## 1. Objetivo

En esta práctica no vamos a buscar un “prompt perfecto”.

Vamos a trabajar como lo haríamos con cualquier otro componente de ingeniería:

1. crear un **baseline**;
2. definir qué significa una respuesta correcta;
3. construir una petición con requisitos explícitos;
4. probarla con varios casos;
5. identificar un fallo;
6. cambiar **una sola cosa**;
7. volver a ejecutar el mismo test set para comprobar si hemos mejorado sin introducir regresiones.

Al terminar deberías poder explicar por qué una petición profesional necesita algo más que una buena redacción.

---

## 2. Qué vas a practicar

Durante el laboratorio trabajarás con los seis elementos vistos en el módulo:

1. **Tarea**
2. **Contexto**
3. **Entrada**
4. **Restricciones**
5. **Output contract**
6. **Criterios de éxito**

También practicarás:

- grounding sobre información suministrada;
- separación entre hechos e hipótesis;
- control de formato;
- abstención cuando faltan datos;
- test sets;
- comparación controlada;
- detección de regresiones.

> En este laboratorio **no utilizaremos todavía agentes personalizados, MCP, skills ni steering**. Los veremos en módulos posteriores. Aquí queremos aislar el problema de diseño y evaluación de instrucciones.

---

## 3. Escenario

Trabajas con un equipo de **Network Operations**.

Quieres utilizar un LLM para realizar un primer triaje de incidencias antes de que un ingeniero revise el caso.

El sistema **no debe decidir cambios de red ni ejecutar acciones**. Solo debe:

- clasificar la severidad;
- mostrar las evidencias que justifican esa clasificación;
- indicar qué información falta;
- recomendar una siguiente comprobación **reversible y diagnóstica**.

Los datos del ejercicio son completamente sintéticos.

---

## 4. Preparar el entorno

Desde el Codespace del curso:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
kiro-cli
```

El entorno debe indicar que Kiro está autenticado.

### Mantén constante el modelo

Dentro de Kiro CLI puedes consultar o cambiar el modelo con:

```text
/model
```

Puedes utilizar cualquiera de los modelos disponibles en tu cuenta, pero:

> **No cambies de modelo durante el laboratorio.**

Si cambias simultáneamente prompt y modelo ya no podrás saber qué provocó la diferencia observada.

### Empieza cada ejecución en una conversación nueva

Antes de probar cada caso:

```text
/chat new
```

Esto evita que respuestas o instrucciones anteriores contaminen la siguiente prueba.

---

# Parte A — Crear un baseline

## 5. Primera ejecución

Comienza con la incidencia:

```text
labs/m02/cases/INC-117.md
```

En una conversación nueva escribe únicamente:

```text
Analiza @labs/m02/cases/INC-117.md y dime qué harías.
```

No añadas explicaciones adicionales.

### Observa la respuesta

Anota en tu hoja de trabajo:

- ¿ha asignado una severidad?
- ¿con qué criterio?
- ¿ha inventado alguna causa?
- ¿ha distinguido hechos de hipótesis?
- ¿la siguiente acción es reversible?
- ¿el formato sería suficientemente estable para que otra persona lo utilizase de forma repetible?

No intentes corregirlo todavía.

El objetivo de esta fase es obtener un **baseline**.

---

# Parte B — Diseñar la versión V1

## 6. Lee la política de triaje

Abre:

```text
labs/m02/context/triage-policy.md
```

Esta política será la fuente de verdad del ejercicio.

El modelo no debe utilizar una clasificación de severidad inventada ni conocimiento externo cuando contradiga esta política.

---

## 7. Crea tu prompt

Crea:

```text
labs/m02/work/prompt-v1.md
```

Puedes utilizar este esqueleto:

```markdown
# TAREA

# CONTEXTO

# ENTRADA

# RESTRICCIONES

# OUTPUT CONTRACT

# CRITERIOS DE ÉXITO
```

Tu prompt debe dejar suficientemente claro:

- qué debe hacer el modelo;
- quién consumirá el resultado;
- que existe una política que debe aplicar;
- que la incidencia será suministrada como entrada;
- qué afirmaciones están permitidas y cuáles no;
- qué debe hacer si faltan datos;
- qué formato debe devolver;
- cómo podemos decidir si el resultado es correcto.

### Importante

No codifiques manualmente las respuestas de cada incidencia dentro del prompt.

Queremos diseñar una regla reutilizable, no resolver el test set mediante excepciones.

---

## 8. Formato mínimo esperado

El resultado debe contener exactamente estas cuatro secciones, en este orden:

```text
SEVERITY:
EVIDENCE:
MISSING_DATA:
NEXT_CHECK:
```

### Reglas mínimas

- `SEVERITY` solo puede ser `P1`, `P2`, `P3` o `UNDETERMINED`.
- `EVIDENCE` debe utilizar únicamente información presente en la incidencia y en la política.
- `MISSING_DATA` debe indicar datos relevantes ausentes. Si no falta ninguno, debe indicarlo explícitamente.
- `NEXT_CHECK` debe contener una comprobación diagnóstica y reversible.
- No se puede afirmar una causa raíz si `rca_status` no es `confirmed`.
- No debe recomendar reinicios, rollbacks, cambios de configuración ni otras acciones que modifiquen el servicio.

---

# Parte C — Probar V1 sobre un test set

## 9. Casos principales

Utiliza estos cuatro casos:

```text
labs/m02/cases/INC-117.md
labs/m02/cases/INC-204.md
labs/m02/cases/INC-305.md
labs/m02/cases/INC-411.md
```

Para cada caso:

1. ejecuta `/chat new`;
2. mantén el mismo modelo;
3. utiliza el mismo `prompt-v1.md`;
4. cambia únicamente la incidencia.

Mensaje recomendado:

```text
Aplica exactamente @labs/m02/work/prompt-v1.md.
La política aplicable es @labs/m02/context/triage-policy.md.
La entrada es @labs/m02/cases/INC-117.md.
No modifiques archivos ni ejecutes acciones. Devuelve únicamente el resultado solicitado.
```

Cambia únicamente el nombre de la incidencia en las siguientes ejecuciones.

---

## 10. Evalúa cada respuesta

Utiliza seis criterios. Cada uno vale **0 o 1 punto**.

| Criterio | 1 punto si... |
|---|---|
| Severidad | aplica correctamente la política |
| Grounding | las evidencias existen realmente en los datos suministrados |
| RCA | no convierte sospechas en causa confirmada |
| Missing data | detecta ausencias relevantes sin inventarlas |
| Next check | propone una comprobación diagnóstica, relevante y reversible |
| Output contract | respeta las cuatro secciones y los valores permitidos |

Máximo:

```text
6 puntos por incidencia
24 puntos en el test set principal
```

Registra tus resultados en:

```text
labs/m02/worksheet.md
```

---

# Parte D — Stress test

## 11. Prueba casos menos cómodos

Ahora prueba la misma V1, sin modificarla todavía, con:

```text
labs/m02/cases/INC-512.md
labs/m02/cases/INC-613.md
```

Estos casos contienen condiciones que suelen revelar problemas de diseño:

- información de distinta fiabilidad;
- hipótesis no confirmadas;
- reglas que dependen de varias condiciones simultáneamente;
- valores próximos a umbrales.

Evalúalos utilizando exactamente la misma rúbrica.

---

# Parte E — Diagnóstico

## 12. Clasifica el fallo

Si alguna respuesta falla, no edites inmediatamente el prompt.

Primero identifica la causa más probable.

Utiliza una de estas categorías:

### A. Instrucción

El modelo no entendió claramente qué tarea debía realizar.

### B. Contexto

Faltaba una regla, prioridad o dato necesario para resolver la tarea.

### C. Restricción

El modelo realizó una inferencia o acción que debía estar prohibida.

### D. Output contract

La respuesta puede ser razonable para una persona, pero no cumple el formato esperado.

### E. Criterio de éxito

No habíamos definido de forma suficientemente observable qué significaba “correcto”.

### F. Modelo / comportamiento no determinista

La especificación parece suficiente, pero el modelo falla de forma puntual.

> No todo fallo se arregla haciendo el prompt más largo.

---

# Parte F — Crear V2 con un cambio controlado

## 13. Duplica V1

```bash
cp labs/m02/work/prompt-v1.md labs/m02/work/prompt-v2.md
```

Ahora cambia **una sola cosa**.

Ejemplos válidos:

- aclarar la prioridad entre dos reglas;
- reforzar cuándo debe utilizar `UNDETERMINED`;
- indicar cómo tratar una hipótesis no confirmada;
- hacer más preciso el contrato de salida;
- convertir un criterio vago en uno observable.

No hagas cinco mejoras simultáneas.

En tu hoja de trabajo escribe:

```text
Hipótesis:
Creo que el fallo se debe a ______________________.

Cambio:
Voy a modificar _________________________________.

Resultado esperado:
Espero que mejore _______________________________
sin empeorar ____________________________________.
```

---

# Parte G — Regression test

## 14. Ejecuta exactamente los mismos casos

Repite con `prompt-v2.md`:

```text
INC-117
INC-204
INC-305
INC-411
INC-512
INC-613
```

Utiliza otra vez conversaciones nuevas y el mismo modelo.

Compara V1 y V2.

Preguntas:

1. ¿ha desaparecido el fallo?
2. ¿ha mejorado la puntuación total?
3. ¿ha empeorado algún caso que antes funcionaba?
4. ¿el cambio ha aumentado innecesariamente el tamaño o complejidad del prompt?
5. ¿el problema era realmente de prompting?

---

# Parte H — Conclusiones

## 15. Entrega de la práctica

Al finalizar debes tener:

```text
labs/m02/work/prompt-v1.md
labs/m02/work/prompt-v2.md
labs/m02/worksheet.md
```

Debes ser capaz de explicar:

- qué diferencia hay entre V1 y V2;
- qué fallo intentabas corregir;
- qué evidencia demuestra que la V2 es mejor o no;
- si apareció alguna regresión;
- qué parte del problema no resolverías simplemente añadiendo más instrucciones al prompt.

---

# Reto opcional — Portabilidad entre herramientas

Si queda tiempo y utilizas habitualmente otra herramienta como Kiro IDE, GitHub Copilot, ChatGPT o Claude:

1. utiliza exactamente tu `prompt-v2.md`;
2. utiliza exactamente uno de los casos del test set;
3. no cambies la política;
4. compara el resultado con Kiro CLI.

No buscamos decidir qué producto es “mejor”.

Busca diferencias en:

- seguimiento de restricciones;
- grounding;
- formato;
- abstención;
- interpretación de criterios.

La conclusión importante es:

> **Un prompt no existe aislado: su comportamiento depende también del modelo, el harness, el contexto y las herramientas que lo rodean.**

---

# Checklist final

- [ ] He creado un baseline.
- [ ] He utilizado los seis elementos de una petición efectiva.
- [ ] He utilizado la política como fuente de verdad.
- [ ] He probado V1 con más de un caso.
- [ ] He utilizado conversaciones nuevas para reducir contaminación.
- [ ] He mantenido el mismo modelo.
- [ ] He identificado un fallo antes de modificar el prompt.
- [ ] He cambiado una sola cosa en V2.
- [ ] He ejecutado un regression test.
- [ ] Puedo justificar con evidencia si V2 es mejor que V1.
