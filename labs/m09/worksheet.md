# M09 — Hoja de trabajo

## Agent Breaker
INPUT CONTROLADO POR:
OBJETIVO ORIGINAL:
COMPORTAMIENTO CONSEGUIDO:
CONTROL QUE FALLÓ:
¿Bastaría prompt hardening?:

## Trust boundaries
USER INPUT:
RETRIEVED DOCUMENT:
TOOL OUTPUT:
LLM PROPOSAL:
RUNTIME POLICY:
APPROVAL REGISTRY:
SIDE EFFECT:

## RAG poisoning
Documento problemático:
¿Por qué era relevante semánticamente?:
¿Por qué no era autoritativo?:
¿Entró en vulnerable?:
¿Entró en hardened?:
Control aplicado antes del modelo:

## Tool-output injection
Dato operativo válido:
Texto no confiable:
Action propuesta:
Approval ID propuesto:
¿Debe ese texto conceder permiso?:

## Runtime
Fake approval — vulnerable:
Fake approval — hardened:
Wrong-scope approval — vulnerable:
Wrong-scope approval — hardened:
Valid approval — vulnerable:
Valid approval — hardened:
¿Qué control cambió el resultado?:

## Security regression
VULNERABLE Security Failure Rate:
HARDENED Security Failure Rate:

untrusted_doc_not_in_context:
fake_approval_rejected:
wrong_scope_approval_rejected:
tool_output_cannot_authorize:
valid_approval_still_works:

## Control layers
A — documents=data:
B — trusted_source filter:
C — approval registry:
D — action allowlist:
E — human confirmation:
F — credentials outside prompt:

## Threat model
ASSET:
TRUST BOUNDARY:
THREAT:
CONTROL:
SECURITY PROPERTY:
TEST:

## Fairness paired test
URGENCY-A:
URGENCY-B:
¿Diferencia observada?:
¿Qué variable cambió?:
¿Basta este par para concluir que existe sesgo?:
¿Cómo ampliarías la evaluación?:

## Conclusión
Prompt hardening !=
Semantic relevance !=
Tool output !=
Model proposal !=
System prompt !=
Valid JSON !=
Red team finding !=
Model compromise !=
