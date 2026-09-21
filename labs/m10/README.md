# M10 — Laboratorio Capstone: De la intención al cambio verificado

## Objetivo

En esta práctica vas a completar un cambio de software utilizando IA sin aceptar como evidencia la frase:

```text
"ya está hecho"
```

El flujo será:

```text
change request
   ↓
spec verificable
   ↓
baseline
   ↓
cambio acotado
   ↓
quality gate
   ↓
repair dirigido por fallos
   ↓
diff review
   ↓
evidencia
   ↓
aceptación humana
```

La idea central es:

> **Generated ≠ Verified ≠ Accepted.**

---

# 1. Entorno

Desde el Codespace:

```bash
cd /workspaces/prompt-engineering-labs
git pull
./scripts/check-environment.sh
```

Los archivos del laboratorio son:

```text
labs/m10/
├── README.md
├── AGENTS.md
├── incident_analyzer.py
├── test_incident.py
└── verify.py
```

No necesitas instalar dependencias nuevas.

---

# 2. Change Request

Debes implementar:

```text
CR-FEAT-010 — Incident severity
```

La función pública existente es:

```python
analyze_incident(incident)
```

No debes cambiar su nombre ni sus parámetros.

El resultado actual contiene:

```text
service
status
summary
requires_human_review
```

El cambio debe añadir:

```text
severity
```

sin alterar los campos ni comportamientos existentes.

---

# 3. Reglas de severity

Aplica en este orden.

## P1

```text
security_signal = true
OR
service_status = unavailable
OR
affected_users >= 100
```

## P2

Si no hay P1:

```text
service_status = degraded
AND
(
  affected_users >= 25
  OR
  error_rate >= 5.0
)
```

## P3

```text
service_status = degraded
```

sin cumplir P1/P2.

## P4

```text
service_status = available
```

sin cumplir P1.

## UNDETERMINED

Cuando:

```text
service_status
```

no permite aplicar las categorías anteriores.

---

# 4. Restricciones de ingeniería

Lee antes:

```text
labs/m10/AGENTS.md
```

Las restricciones incluyen:

- preservar `analyze_incident(incident)`;
- no modificar tests;
- no debilitar el quality gate;
- standard library only;
- no network;
- no `eval`;
- no `exec`;
- cambio mínimo;
- evidencia antes de declarar completion.

Estas restricciones forman parte de la especificación.

---

# 5. Baseline

Antes de pedir ningún cambio a la IA:

```bash
python labs/m10/verify.py baseline
```

Resultado esperado:

```text
PASS | 10 regression tests
QUALITY_GATE=PASS
```

Este es el comportamiento que ya funciona.

Ahora ejecuta:

```bash
python labs/m10/verify.py full
```

Debe fallar.

No intentes arreglar nada todavía.

Observa:

```text
qué tests fallan
por qué fallan
qué comportamiento falta
```

El estado inicial debe ser:

```text
10 regression tests → PASS
6 feature tests → FAIL
```

---

# 6. Revisar el código antes de generar

Abre:

```text
labs/m10/incident_analyzer.py
labs/m10/test_incident.py
```

Identifica:

```text
PUBLIC API
EXISTING OUTPUT
LEGACY HELPER
FEATURE TESTS
```

Responde mentalmente:

> ¿Cuál es el cambio mínimo que satisface la feature sin tocar el contrato existente?

---

# 7. Delegar a Kiro

Inicia:

```bash
kiro-cli
```

Utiliza una conversación nueva:

```text
/chat new
```

Prompt recomendado:

```text
Implement CR-FEAT-010 in labs/m10.

Read first:
@labs/m10/README.md
@labs/m10/AGENTS.md
@labs/m10/incident_analyzer.py
@labs/m10/test_incident.py

Requirements:
- preserve analyze_incident(incident)
- preserve all existing output fields and behavior
- add severity according to the specification
- modify only incident_analyzer.py
- do not modify tests
- do not weaken verify.py
- make the smallest reasonable change

Workflow:
1. inspect the existing implementation and tests
2. run the baseline gate
3. inspect the full-gate failures
4. implement the change
5. run the full quality gate
6. if it fails, repair only the observed failure
7. show me the final evidence and diff summary

Do not commit anything.
```

Observa qué comandos y modificaciones propone el agente.

Aprueba únicamente acciones dentro del alcance del laboratorio.

---

# 8. No aceptar self-report

Aunque Kiro responda:

```text
Implementation complete.
All requirements satisfied.
```

ejecuta tú mismo:

```bash
python labs/m10/verify.py full
```

La única condición de éxito técnico es:

```text
PASS | tests unchanged
PASS | syntax and forbidden-call policy
PASS | public API preserved: analyze_incident(incident)
PASS | 10 regression + 6 feature tests
QUALITY_GATE=PASS
```

---

# 9. Repair dirigido por fallos

Si falla algún gate, no pidas:

```text
"revísalo y mejóralo"
```

Utiliza exactamente la evidencia observada.

Ejemplo:

```text
The quality gate fails with:

[PEGA SOLO EL FALLO]

Fix only the defect that explains this failure.

Constraints:
- preserve public API
- do not edit tests
- do not weaken verify.py
- keep the change minimal

Then rerun the full quality gate.
```

La reparación debe responder a un fallo concreto.

---

# 10. Diff review

Cuando el gate pase:

```bash
git diff -- labs/m10
```

No preguntes primero al modelo si el diff es correcto.

Revísalo tú.

Comprueba:

### Scope

```text
¿solo cambió incident_analyzer.py?
```

### API

```text
¿analyze_incident(incident) sigue intacta?
```

### Regression

```text
¿los campos existentes se conservan?
```

### Feature

```text
¿severity sigue exactamente la prioridad P1 → P2 → P3 → P4 → UNDETERMINED?
```

### Complexity

```text
¿el cambio es mayor de lo necesario?
```

### Security

```text
¿aparecieron imports, network, eval, exec o side effects innecesarios?
```

El quality gate automatiza una parte del review.

No sustituye esta revisión.

---

# 11. Legacy: ¿refactorizamos también?

El archivo contiene:

```python
_format_summary_legacy(...)
```

Puede parecer tentador pedir:

```text
"Ya que estamos, moderniza también este código."
```

Decide si debería formar parte de:

```text
CR-FEAT-010
```

Justifica tu decisión.

Si quisieras refactorizarlo en otro cambio, ¿qué evidencia utilizarías para demostrar equivalencia?

Pista:

```text
characterization tests
→ refactor
→ mismos tests
```

---

# 12. Documentación grounded

Cuando el diff y el gate estén revisados, crea:

```text
labs/m10/work/release-note.md
```

Pide a Kiro:

```text
Create labs/m10/work/release-note.md.

Use only:
- the actual git diff for labs/m10
- the observed output of: python labs/m10/verify.py full

Include:
CHANGE:
VERIFICATION:
COMPATIBILITY:
KNOWN_LIMITATIONS:

Rules:
- do not claim anything that is not supported by the diff or gate output
- do not claim production readiness
- do not invent CI, review, deployment or performance results
```

Revisa la release note.

Busca frases como:

```text
"production-ready"
"fully secure"
"no regressions possible"
"deployed successfully"
```

si no existe evidencia para ellas.

---

# 13. Change evidence

Crea también:

```text
labs/m10/work/evidence.md
```

Incluye manualmente:

```text
CHANGE REQUEST:
CR-FEAT-010

BASELINE:
resultado observado

FULL GATE BEFORE:
resultado observado

FULL GATE AFTER:
resultado observado

FILES CHANGED:
resultado de git diff --name-only

HUMAN DIFF REVIEW:
ACCEPT | REPAIR | REJECT

RATIONALE:
...
```

Este archivo representa el paso que un comentario del agente no puede sustituir:

```text
accountability humana
```

---

# 14. ¿Qué automatizarías en CI?

Clasifica estos controles.

## Automatizar

```text
syntax
unit tests
regression tests
forbidden calls
test integrity
public API check
```

## Mantener revisión humana

Decide para:

```text
scope
arquitectura
mantenibilidad
calidad del diff
riesgo
aceptación
merge
deployment
```

Pregunta:

> ¿Qué parte podría bloquear automáticamente un pipeline y qué parte requiere criterio?

---

# 15. Espectro de delegación

Identifica qué has hecho en cada fase:

```text
VIBE CODING
AI-ASSISTED
QUALITY-GATED
CODING AGENT
AGENTIC WORKFLOW
```

No es obligatorio utilizar el máximo nivel de delegación.

Para este cambio responde:

> ¿En qué punto dejarías de aumentar autonomía y por qué?

---

# 16. Conclusión del curso

Este laboratorio reutiliza ideas de todo el curso:

```text
M02 → especificación y criterios de éxito
M03 → repair basado en fallos
M04 → contratos y validación
M05 → contexto relevante
M06 → tools y límites
M07 → evidencia y grounding
M08 → agentes y autoridad
M09 → código/output no confiable hasta verificar
M10 → integración en un flujo de ingeniería
```

Debes poder defender esta afirmación:

> **La competencia avanzada no consiste en conseguir que la IA escriba más código, sino en diseñar un proceso en el que podamos decidir con evidencia qué código aceptar.**
