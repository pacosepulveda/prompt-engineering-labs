# M10.1 — Laboratorio: Vibe Coding disciplinado

## Objetivo

Vas a construir con Kiro una pequeña aplicación web local para gestionar incidencias de Telvora. El objetivo no es escribir el código manualmente, sino practicar **buenas prácticas de vibe coding**: describir el resultado, limitar el alcance, pedir una propuesta antes de generar, construir una vertical slice, probar lo generado, hacer iteraciones acotadas, crear checkpoints y entender el producto antes de darlo por terminado.

La aplicación final permitirá crear incidencias, indicar servicio/título/descripción/severidad, cambiar su estado, filtrar y conservar los datos al recargar.

La solución será deliberadamente pequeña:

```text
HTML + CSS + JavaScript + localStorage
sin backend, cloud, autenticación ni dependencias externas
```

---

## 1. Preparar el entorno

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
mkdir -p labs/m10-vibe/work
kiro-cli
```

En Kiro:

```text
/chat new
```

Si usas otro coding agent, sigue el mismo flujo.

---

## 2. Empezar por el outcome, no por la tecnología

Envía este prompt:

```text
Quiero construir una pequeña aplicación web local para gestionar incidencias operativas de Telvora.

Debe permitir:
- crear una incidencia;
- indicar servicio, título y severidad;
- cambiar su estado;
- ver las incidencias;
- conservar los datos al recargar la página.

Es una aplicación local para una demo formativa.

No necesito autenticación, backend, cloud, servicios externos ni base de datos externa. Quiero mantener la solución pequeña y fácil de entender.

Antes de crear archivos, dime brevemente:
1. qué vas a construir;
2. qué tecnología mínima propones;
3. qué archivos necesitas;
4. qué decisiones estás asumiendo.

No escribas código todavía.
```

La propuesta esperada es una aplicación estática con `index.html`, `styles.css` y `app.js`, usando `localStorage`. Si propone React, backend, base de datos o paquetes, responde:

```text
Simplifica la propuesta. Para esta aplicación usa únicamente HTML, CSS, JavaScript y localStorage. No necesitamos framework, backend ni dependencias. Mantén la estructura mínima. No escribas código todavía.
```

No continúes hasta entender y aceptar la propuesta.

---

## 3. Construir una vertical slice

Ahora pide una primera versión pequeña pero completa:

```text
Implementa la primera vertical slice en labs/m10-vibe/work/.

Debe permitir únicamente:
- crear una incidencia con título, servicio y severidad P1/P2/P3/P4;
- mostrar las incidencias creadas;
- cambiar el estado entre OPEN, IN_PROGRESS y RESOLVED;
- guardar y recuperar los datos usando localStorage.

Usa solo HTML, CSS y JavaScript, sin dependencias. La interfaz debe ser clara y profesional. No añadas todavía filtros, estadísticas ni otras funcionalidades. No crees archivos innecesarios.

Cuando termines, dime qué archivos has creado y cómo ejecutar la aplicación. No hagas más cambios.
```

Abre otra terminal y ejecuta:

```bash
cd /workspaces/prompt-engineering-labs/labs/m10-vibe/work
python -m http.server 8080
```

Abre el puerto 8080 desde Codespaces y comprueba manualmente:

```text
crear P1
crear P3
cambiar una a IN_PROGRESS
cambiar otra a RESOLVED
recargar la página
comprobar que siguen existiendo
```

No continúes hasta que esta versión funcione.

Si falla algo, no uses "arréglalo". Describe exactamente el fallo. Por ejemplo:

```text
Al recargar la página, las incidencias desaparecen.
Corrige únicamente la persistencia. Mantén la interfaz, la estructura y el resto del comportamiento. No añadas funcionalidades. Explica brevemente la causa al terminar.
```

La regla es:

```text
fallo observado → corrección enfocada
```

---

## 4. Crear un checkpoint

Cuando la vertical slice funcione:

```bash
cd /workspaces/prompt-engineering-labs
git add labs/m10-vibe/work
git commit -m "M10 vibe baseline"
git status
```

El checkpoint es un estado conocido y funcional al que puedes volver.

---

## 5. Una intención por iteración

Vuelve a Kiro. Realiza estas iteraciones por separado y prueba la aplicación después de cada una.

### A. Descripción

```text
Añade una descripción opcional a cada incidencia. Debe introducirse al crearla y mostrarse de forma legible. No cambies ninguna otra funcionalidad y conserva los datos ya guardados si es posible. No añadas filtros ni otras mejoras.
```

### B. Filtros

```text
Añade filtros por estado y severidad, con opción ALL. Ambos filtros deben poder combinarse y no deben modificar los datos. No cambies el formulario ni añadas otras funcionalidades.
```

Prueba `P1 + OPEN`, `P3 + RESOLVED`, `ALL + OPEN` y `ALL + ALL`.

### C. Resumen

```text
Añade un resumen visual que muestre únicamente: total, abiertas, en progreso y resueltas. Los valores deben actualizarse al cambiar el estado. No añadas gráficos, librerías ni otras funcionalidades.
```

### D. Mejora visual concreta

Solo si hace falta:

```text
La severidad no se distingue suficientemente al revisar muchas incidencias. Mejora únicamente la jerarquía visual de P1, P2, P3 y P4. Mantén estructura y funcionalidades. No añadas dependencias.
```

Evita prompts como `hazlo mejor`. Una iteración debe tener una intención concreta.

Cuando todo vuelva a funcionar:

```bash
cd /workspaces/prompt-engineering-labs
git add labs/m10-vibe/work
git commit -m "M10 vibe incident dashboard"
git diff HEAD~1..HEAD -- labs/m10-vibe/work
```

---

## 6. Revisar lo que la IA ha construido

Pide a Kiro, sin permitir modificaciones:

```text
Revisa únicamente labs/m10-vibe/work y dime:
1. qué archivos forman la aplicación;
2. qué dependencias externas utiliza;
3. dónde se almacenan los datos;
4. si existe alguna llamada de red;
5. qué funcionalidades contiene que yo no haya pedido explícitamente.
No modifiques ningún archivo.
```

La solución esperada debería tener aproximadamente tres archivos, cero dependencias externas, `localStorage`, cero llamadas de red y ninguna funcionalidad importante fuera de alcance.

Después pide:

```text
Explícame labs/m10-vibe/work como si mañana tuviera que mantenerla yo. Explica qué hace cada archivo, cómo se representa una incidencia, cómo se genera su id, cómo se guarda/carga localStorage, cómo funcionan filtros y contadores y qué limitaciones conocidas tiene. No modifiques archivos.
```

Debes poder explicar este flujo:

```text
formulario
→ objeto incident
→ array en memoria
→ localStorage
→ render
→ filtros / resumen
```

---

## 7. Comprobación final y solución esperada

La estructura de referencia es:

```text
labs/m10-vibe/work/
├── index.html
├── styles.css
└── app.js
```

Cada incidencia debería representar al menos:

```text
id
title
service
description
severity
status
createdAt
```

Estados: `OPEN`, `IN_PROGRESS`, `RESOLVED`.

Severidades: `P1`, `P2`, `P3`, `P4`.

Persistencia: `localStorage`.

Comprueba manualmente:

```text
[ ] crear incidencias
[ ] cambiar estado
[ ] recargar sin perder datos
[ ] filtrar por estado
[ ] filtrar por severidad
[ ] combinar filtros
[ ] contadores correctos
[ ] título vacío rechazado
[ ] servicio vacío rechazado
[ ] descripción larga utilizable
[ ] cero dependencias externas innecesarias
```

No debe ser necesario `npm install`, `pip install`, Docker, servidor de base de datos, API externa, cloud ni autenticación.

---

## 8. Sobreconstrucción, regresiones y criterio para detenerse

Si Kiro empieza a introducir frameworks, backend, SQLite, APIs, Docker, autenticación o muchos archivos, deténlo:

```text
Detente. Estamos construyendo una herramienta local pequeña. Mantén únicamente HTML, CSS, JavaScript y localStorage. Antes de modificar nada, dime qué eliminarías para volver a la solución mínima.
```

Si una iteración rompe algo:

```text
Después del último cambio ha dejado de funcionar: [COMPORTAMIENTO OBSERVADO]. Antes funcionaba. Corrige únicamente esa regresión. No añadas funcionalidades ni refactorices otras partes.
```

Puedes revisar o descartar cambios no confirmados con:

```bash
git status
git diff -- labs/m10-vibe/work
git restore labs/m10-vibe/work
```

Detente cuando el outcome inicial esté cumplido, la aplicación funcione, entiendas lo construido y no haya cambios que aporten valor al objetivo. No añadas funcionalidades simplemente porque Kiro pueda implementarlas.

La idea central de la práctica es:

> **Vibe coding no tiene por qué significar desarrollar sin criterio. Podemos delegar gran parte de la implementación a la IA y conservar el control sobre alcance, evolución y comprensión del producto.**

En el capstone M10.2 aumentarás el nivel de control con especificación verificable, tests, quality gates, diff review y evidencia. El nivel de disciplina adecuado depende del propósito y del riesgo del software.
