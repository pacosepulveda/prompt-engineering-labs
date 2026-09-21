# M09 — Laboratorio: De prompt injection a un sistema resiliente

Objetivo: comprobar que manipular el modelo no debe equivaler a comprometer el sistema.

Archivos:
- README.md
- scenarios.md
- security_lab.py
- worksheet.md

Todo el entorno es sintético y no modifica sistemas reales.

Flujo principal:
1. Realiza el warm-up en https://play.lakera.ai/agent-breaker.
2. Revisa scenarios.md e identifica trust boundaries.
3. Compara retrieval vulnerable y hardened:
   python labs/m09/security_lab.py --retrieve vulnerable --out labs/m09/work/retrieved.md
   python labs/m09/security_lab.py --retrieve hardened --out labs/m09/work/retrieved.md
4. Usa CASE-TOOL-OUTPUT para crear labs/m09/work/proposal.json sin ejecutar acciones.
5. Compara runtimes:
   python labs/m09/security_lab.py --demo
   python labs/m09/security_lab.py --proposal labs/m09/work/proposal.json --mode vulnerable
   python labs/m09/security_lab.py --proposal labs/m09/work/proposal.json --mode hardened
6. Comprueba una aprobación válida:
   python labs/m09/security_lab.py --approved-example
7. Ejecuta security regression:
   python labs/m09/security_lab.py --regression --mode vulnerable
   python labs/m09/security_lab.py --regression --mode hardened
8. Completa threat model, capas de control y paired fairness test en worksheet.md.

Ideas clave:
- prompt hardening != security boundary
- semantic relevance != authority
- retrieved content != trusted instruction
- tool output != authorization
- model proposal != permission
- system prompt != secret store
- valid JSON != valid business action
- model compromise != system compromise
- red team finding != regression test
