# Guía práctica — Creación de agentes en Kiro CLI

## Kiro CLI 2.x (legacy) vs Kiro CLI 3.x (actual)

Fecha de referencia: septiembre de 2026.

---

## 1. Objetivo

Esta guía explica cómo crear agentes personalizados en Kiro y cómo distinguir entre el formato legacy de Kiro CLI 2.x y el formato actual de Kiro CLI 3.x.

La idea principal es evitar mezclar por accidente:

- nombres de tools antiguos y nuevos;
- `toolsSettings` y `permissions`;
- expresiones regulares y patrones glob;
- configuración legacy y configuración actual.

Kiro CLI 3.x mantiene compatibilidad hacia atrás con agentes legacy, pero para agentes nuevos es preferible utilizar el formato actual.

---

## 2. Comprobar la versión instalada

Antes de crear o modificar un agente:

```bash
kiro-cli --version
```

Cuando un repositorio se comparte entre varias personas o entornos, conviene fijar qué versión de Kiro se utilizará como referencia.

---

## 3. Dónde se guardan los agentes

### Agentes del workspace

```text
.kiro/agents/
```

Ejemplo:

```text
my-project/
├── .kiro/
│   └── agents/
│       └── reviewer.json
├── docs/
└── src/
```

Los agentes de workspace viajan con Git y son adecuados para proyectos compartidos.

### Agentes globales

```text
~/.kiro/agents/
```

Los agentes globales están disponibles para ese usuario en diferentes proyectos.

Si existe un agente global y otro de workspace con el mismo nombre, el agente del workspace tiene prioridad.

---

## 4. Iniciar Kiro desde el workspace correcto

Para que Kiro cargue los agentes definidos en `.kiro/agents/`, inicia el CLI desde la raíz del proyecto:

```bash
cd /ruta/al/proyecto
kiro-cli
```

Dentro de Kiro:

```text
/agent list
```

o:

```text
/agent
```

---

## 5. Agente mínimo en Kiro CLI 3.x

Archivo:

```text
.kiro/agents/doc-reviewer.json
```

Contenido:

```json
{
  "name": "doc-reviewer",
  "description": "Reviews project documentation",
  "tools": ["read"],
  "prompt": "You are a documentation reviewer. Analyze the requested documents and report inconsistencies without modifying files."
}
```

Este agente solo necesita capacidad de lectura.

---

## 6. Las cuatro piezas principales de un agente

En Kiro CLI 3.x conviene separar conceptualmente:

```text
PROMPT
→ qué papel tiene el agente y cómo debe comportarse

TOOLS
→ qué capacidades puede utilizar

PERMISSIONS
→ qué operaciones se permiten, preguntan o bloquean

RESOURCES
→ qué contexto se carga automáticamente
```

No conviene utilizar el prompt como sustituto de permisos técnicos.

Por ejemplo:

```text
"Do not delete files."
```

es una instrucción.

Una regla de permisos:

```json
{
  "capability": "shell",
  "match": ["rm -rf *"],
  "effect": "deny"
}
```

es un control técnico.

---

## 7. `tools` en Kiro CLI 3.x

El campo `tools` define las herramientas o categorías de herramientas que el agente puede utilizar.

Ejemplos:

```json
"tools": ["read"]
```

```json
"tools": ["read", "write"]
```

```json
"tools": ["read", "write", "shell"]
```

Las categorías actuales incluyen:

```text
read
write
shell
web
subagent
knowledge
todo_list
@mcp
@builtin
*
```

Por ejemplo:

```json
{
  "tools": [
    "read",
    "write",
    "shell",
    "todo_list"
  ]
}
```

### `todo_list` frente a `todo`

En el campo `tools`, `todo_list` es la categoría de task tracking.

La herramienta concreta de runtime aparece documentada como `todo`.

Son dos niveles de nomenclatura distintos:

```text
tools: ["todo_list"]
→ categoría

runtime
→ todo
```

---

## 8. Tools individuales y categorías

Kiro CLI 3.x permite utilizar nombres simplificados de tools y categorías.

Ejemplos de tools actuales:

```text
read
write
glob
grep
shell
web_fetch
web_search
code
knowledge
todo
```

También se puede utilizar:

```json
"tools": ["@builtin"]
```

para incluir todas las tools built-in, o:

```json
"tools": ["*"]
```

para incluir todas las herramientas disponibles.

En agentes con límites estrictos es preferible declarar únicamente las capacidades necesarias.

---

## 9. `allowedTools`

`allowedTools` define tools que pueden utilizarse sin solicitar confirmación al usuario.

Ejemplo:

```json
{
  "tools": ["read", "write", "shell"],
  "allowedTools": ["read"]
}
```

Interpretación:

```text
read
→ preaprobado

write / shell
→ disponibles, pero pueden requerir autorización
```

`allowedTools` no sustituye a `permissions` cuando se necesitan reglas por ruta, comando o capacidad.

---

## 10. `permissions` en Kiro CLI 3.x

El mecanismo actual para controlar qué puede hacer un agente es:

```json
"permissions": {
  "rules": [
    ...
  ]
}
```

Cada regla contiene:

```text
capability
match
effect
```

Ejemplo:

```json
{
  "permissions": {
    "rules": [
      {
        "capability": "shell",
        "match": ["pytest *", "python -m pytest *"],
        "effect": "allow"
      },
      {
        "capability": "fs_write",
        "match": ["reports/**"],
        "effect": "allow"
      },
      {
        "capability": "shell",
        "match": ["rm -rf *", "sudo *"],
        "effect": "deny"
      }
    ]
  }
}
```

Capacidades principales:

```text
fs_read
fs_write
shell
web_fetch
web_search
mcp
subagent
all
```

Efectos:

```text
allow
ask
deny
```

---

## 11. Kiro CLI 3.x usa glob en `permissions.match`

Uno de los cambios importantes al migrar desde CLI 2.x es el formato de los patrones.

### CLI 2.x

Era habitual encontrar:

```json
"allowedCommands": [
  "^git status$",
  "^python script\\.py .*"
]
```

Esos patrones son expresiones regulares.

### CLI 3.x

Las reglas de `permissions` utilizan patrones glob:

```json
{
  "capability": "shell",
  "match": [
    "git status",
    "python script.py *"
  ],
  "effect": "allow"
}
```

Conversión típica:

```text
CLI 2.x regex:
^git status$

CLI 3.x glob:
git status
```

```text
CLI 2.x regex:
^npm test.*

CLI 3.x glob:
npm test*
```

No conviene copiar expresiones regulares directamente dentro de `permissions.match`.

---

## 12. Agente de análisis completo en Kiro CLI 3.x

```json
{
  "name": "incident-analyzer",
  "description": "Investigates an application incident and writes a report",
  "tools": [
    "read",
    "write",
    "shell",
    "todo_list"
  ],
  "resources": [
    "file://labs/incident/policy.md",
    "file://labs/incident/context.md"
  ],
  "permissions": {
    "rules": [
      {
        "capability": "shell",
        "match": [
          "python labs/incident/tool.py *"
        ],
        "effect": "allow"
      },
      {
        "capability": "fs_write",
        "match": [
          "labs/incident/work/**"
        ],
        "effect": "allow"
      },
      {
        "capability": "fs_read",
        "match": [
          "labs/incident/secrets/**"
        ],
        "effect": "deny"
      },
      {
        "capability": "shell",
        "match": [
          "rm -rf *",
          "sudo *"
        ],
        "effect": "deny"
      }
    ]
  },
  "prompt": "Investigate the requested incident end-to-end. Use the available evidence tools yourself. Do not ask the user to execute investigation commands. Write the final report to labs/incident/work/report.md."
}
```

Este patrón separa claramente:

```text
rol
→ prompt

capacidades
→ tools

contexto
→ resources

límites
→ permissions
```

---

## 13. `resources`

Los recursos añaden contexto automáticamente al agente.

Ejemplo:

```json
"resources": [
  "file://README.md",
  "file://docs/**/*.md"
]
```

Para archivos concretos:

```json
"resources": [
  "file://policy.md",
  "file://cases.md"
]
```

En versiones actuales también existen recursos como:

```text
skill://
knowledgeBase
```

Los resources son especialmente útiles cuando existe contexto que debe estar disponible siempre, sin obligar al usuario a referenciar manualmente los archivos en cada prompt.

---

## 14. Agente solo lectura

```json
{
  "name": "policy-reviewer",
  "description": "Reviews a case using a fixed policy",
  "tools": ["read"],
  "resources": [
    "file://policy.md",
    "file://cases.md"
  ],
  "prompt": "Evaluate exactly one requested case. Use only explicit evidence. Never invent missing facts."
}
```

Este patrón es apropiado cuando el agente debe analizar pero nunca modificar.

---

## 15. Agente con escritura limitada

```json
{
  "name": "report-writer",
  "description": "Analyzes evidence and writes a report",
  "tools": ["read", "write"],
  "permissions": {
    "rules": [
      {
        "capability": "fs_write",
        "match": ["work/**"],
        "effect": "allow"
      },
      {
        "capability": "fs_write",
        "match": [".kiro/**"],
        "effect": "deny"
      }
    ]
  },
  "prompt": "Analyze the available evidence and write the final report under work/."
}
```

La idea es permitir:

```text
work/**
```

sin otorgar escritura general sobre todo el repositorio.

---

## 16. Agente con shell restringido

```json
{
  "name": "diagnostic-agent",
  "description": "Runs safe diagnostic commands",
  "tools": ["read", "shell"],
  "permissions": {
    "rules": [
      {
        "capability": "shell",
        "match": [
          "python tools/diagnose.py *",
          "git status",
          "git diff*"
        ],
        "effect": "allow"
      },
      {
        "capability": "shell",
        "match": [
          "git push*",
          "rm -rf *",
          "sudo *"
        ],
        "effect": "deny"
      }
    ]
  },
  "prompt": "Investigate problems using only the permitted diagnostic commands."
}
```

Este patrón permite investigación activa sin conceder shell ilimitado.

---

## 17. Agentes multi-agent

Un orquestador necesita la capacidad:

```json
"tools": ["subagent"]
```

Ejemplo:

```json
{
  "name": "review-orchestrator",
  "description": "Delegates independent reviews and consolidates the result",
  "tools": ["subagent"],
  "toolsSettings": {
    "subagent": {
      "availableAgents": [
        "security-reviewer",
        "operations-reviewer"
      ],
      "trustedAgents": [
        "security-reviewer",
        "operations-reviewer"
      ]
    }
  },
  "prompt": "Delegate security to security-reviewer and operations to operations-reviewer. Wait for both results and synthesize the final decision."
}
```

### Por qué aparece `toolsSettings` en un agente V3

En CLI 3.x, `toolsSettings` está deprecado para restricciones de shell y filesystem.

Sin embargo, sigue soportado para configuración específica de determinadas tools, incluido `subagent`:

```text
toolsSettings.subagent.availableAgents
toolsSettings.subagent.trustedAgents
```

Por tanto:

```text
permissions
+
toolsSettings.subagent
```

pueden coexistir legítimamente.

---

## 18. Especialistas para un sistema multi-agent

### Security

```json
{
  "name": "security-reviewer",
  "description": "Security specialist",
  "tools": ["read"],
  "resources": [
    "file://security-policy.md",
    "file://security-evidence.md"
  ],
  "prompt": "Evaluate only the security part of the requested case. Do not evaluate operations."
}
```

### Operations

```json
{
  "name": "operations-reviewer",
  "description": "Operations specialist",
  "tools": ["read"],
  "resources": [
    "file://operations-policy.md",
    "file://operations-evidence.md"
  ],
  "prompt": "Evaluate only operations evidence. Do not evaluate security."
}
```

El aislamiento de contexto puede ser parte deliberada de la arquitectura.

---

## 19. Formato Markdown en Kiro CLI 3.x

Además de JSON, las versiones actuales soportan agentes en Markdown con frontmatter.

Ejemplo:

```text
.kiro/agents/backend-dev.md
```

Contenido:

```markdown
---
name: backend-dev
description: Backend development specialist
tools: ["read", "write", "shell"]
permissions:
  rules:
    - capability: shell
      match: ["npm *", "git *"]
      effect: allow
---

You are a backend developer.

Always:
- run tests before finishing;
- do not modify production infrastructure;
- explain important design decisions.
```

Este formato resulta cómodo cuando el system prompt es largo.

---

## 20. Formato legacy de Kiro CLI 2.x

Un agente clásico de CLI 2.x podía tener esta forma:

```json
{
  "name": "backend-dev",
  "description": "Backend development agent",
  "prompt": "You are a backend developer.",
  "tools": [
    "fs_read",
    "fs_write",
    "execute_bash",
    "grep",
    "glob"
  ],
  "toolsSettings": {
    "execute_bash": {
      "allowedCommands": [
        "^git status$",
        "^npm test"
      ],
      "deniedCommands": [
        "^rm -rf"
      ],
      "denyByDefault": false
    },
    "fs_read": {
      "allowedPaths": [
        "src/**"
      ],
      "deniedPaths": [
        ".env"
      ]
    },
    "fs_write": {
      "allowedPaths": [
        "src/**"
      ]
    }
  }
}
```

Características principales:

```text
tool IDs individuales
+
toolsSettings
+
regex para restricciones shell
```

---

## 21. Equivalente actual en Kiro CLI 3.x

```json
{
  "name": "backend-dev",
  "description": "Backend development agent",
  "prompt": "You are a backend developer.",
  "tools": [
    "read",
    "write",
    "shell"
  ],
  "permissions": {
    "rules": [
      {
        "capability": "shell",
        "match": [
          "git status",
          "npm test*"
        ],
        "effect": "allow"
      },
      {
        "capability": "shell",
        "match": [
          "rm -rf *"
        ],
        "effect": "deny"
      },
      {
        "capability": "fs_read",
        "match": [
          ".env"
        ],
        "effect": "deny"
      },
      {
        "capability": "fs_write",
        "match": [
          "src/**"
        ],
        "effect": "allow"
      }
    ]
  }
}
```

---

## 22. Comparación rápida: CLI 2.x vs CLI 3.x

| Concepto | CLI 2.x | CLI 3.x |
|---|---|---|
| Lectura | `fs_read` | `read` |
| Escritura | `fs_write` | `write` |
| Shell | `execute_bash` | `shell` |
| Restricciones shell | `toolsSettings` | `permissions.rules` |
| Restricciones filesystem | `toolsSettings` | `permissions.rules` |
| Patrones legacy shell | Regex | Glob en `permissions` |
| JSON | Sí | Sí |
| Markdown | — | Sí |
| Subagents | Sí | Sí |
| Resources | Sí | Ampliados |
| Config legacy | Nativa | Backward-compatible |

Los nombres legacy continúan siendo aceptados por CLI 3.x para mantener compatibilidad.

---

## 23. Compatibilidad hacia atrás

Kiro CLI 3.x mantiene compatibilidad con agentes creados para versiones anteriores.

Por ejemplo:

```json
"tools": [
  "fs_read",
  "fs_write",
  "execute_bash",
  "grep",
  "glob"
]
```

puede continuar funcionando.

Eso no significa que sea el formato recomendado para nuevos agentes.

Para configuraciones nuevas, la referencia actual utiliza:

```json
"tools": [
  "read",
  "write",
  "shell"
]
```

junto con:

```text
permissions.rules
```

---

## 24. Migrar un agente legacy

Kiro CLI 3.x incluye:

```text
/upgrade-agent
```

También puede utilizarse:

```text
/upgrade-agent run
```

El proceso:

1. analiza agentes de workspace y globales;
2. muestra cuáles necesitan migración;
3. crea copias de seguridad `.json.bak`;
4. añade la configuración nueva;
5. informa de patrones que no pudieron convertirse exactamente.

Después de una migración:

```text
/upgrade-agent diagnostics
```

Es especialmente importante revisar avisos como:

```text
regex-shell-pattern
unconvertible-pattern
unmapped-allowed-tool
```

porque la conversión regex → glob no siempre puede ser automática.

---

## 25. Diagnóstico

Para comprobar el entorno:

```bash
kiro-cli diagnostic
```

Dentro del TUI:

```text
/agent schema
```

permite consultar el esquema esperado.

Para listar agentes:

```text
/agent list
```

Para activar uno:

```text
/agent swap nombre-del-agente
```

También puede utilizarse el selector interactivo:

```text
/agent
```

---

## 26. Si un agente no aparece

Comprobar en este orden:

1. Kiro se inició desde la raíz del workspace correcto.
2. El archivo está en `.kiro/agents/`.
3. El JSON es sintácticamente válido.
4. El archivo contiene una configuración de agente reconocible.
5. Los nombres de tools son válidos.
6. Los `resources` apuntan a rutas existentes.
7. No existe un conflicto con un agente global del mismo nombre.
8. La configuración coincide con el esquema mostrado por `/agent schema`.
9. `kiro-cli diagnostic` no muestra errores relevantes.
10. `/upgrade-agent diagnostics` no muestra problemas de migración.

Síntomas habituales de un agente inválido:

```text
no aparece en /agent list
fallback al agente default
tools ausentes
warnings de schema
```

---

## 27. Error frecuente: mezclar V2 y V3

Ejemplo confuso:

```json
{
  "tools": [
    "read",
    "write",
    "shell"
  ],
  "toolsSettings": {
    "execute_bash": {
      "allowedCommands": [
        "^python script.py .*"
      ]
    }
  }
}
```

Aquí se está mezclando:

```text
tools V3
+
restricción shell V2
```

Aunque Kiro mantiene compatibilidad legacy, para un agente nuevo es preferible:

```json
{
  "tools": [
    "read",
    "write",
    "shell"
  ],
  "permissions": {
    "rules": [
      {
        "capability": "shell",
        "match": [
          "python script.py *"
        ],
        "effect": "allow"
      }
    ]
  }
}
```

---

## 28. Construcción incremental recomendada

No conviene empezar con una configuración grande.

### Paso 1 — agente mínimo

```json
{
  "name": "my-agent",
  "description": "Does one well-defined job",
  "tools": ["read"],
  "prompt": "..."
}
```

Comprobar:

```text
/agent list
```

### Paso 2 — añadir resources

```json
"resources": [
  "file://context.md"
]
```

Volver a comprobar.

### Paso 3 — añadir escritura

```json
"tools": ["read", "write"]
```

Añadir permisos de escritura limitados.

### Paso 4 — añadir shell

```json
"tools": ["read", "write", "shell"]
```

Permitir solo los comandos necesarios.

### Paso 5 — añadir subagents si existe una razón arquitectónica

```json
"tools": ["subagent"]
```

Este proceso incremental facilita mucho la depuración.

---

## 29. Ejemplo mínimo reusable

```json
{
  "name": "case-reviewer",
  "description": "Reviews structured cases using explicit evidence",
  "tools": ["read"],
  "resources": [
    "file://cases.md",
    "file://policy.md"
  ],
  "prompt": "Review exactly one requested case using only explicit evidence. Never infer missing facts."
}
```

Uso:

```text
/agent
→ case-reviewer
```

Prompt:

```text
Review CASE-A.
```

---

## 30. Ejemplo de trabajo autónomo

```json
{
  "name": "autonomous-investigator",
  "description": "Investigates a case and writes the final report",
  "tools": [
    "read",
    "write",
    "shell",
    "todo_list"
  ],
  "resources": [
    "file://case.md",
    "file://policy.md"
  ],
  "permissions": {
    "rules": [
      {
        "capability": "shell",
        "match": [
          "python tools/investigate.py *"
        ],
        "effect": "allow"
      },
      {
        "capability": "fs_write",
        "match": [
          "work/**"
        ],
        "effect": "allow"
      },
      {
        "capability": "shell",
        "match": [
          "rm -rf *",
          "sudo *"
        ],
        "effect": "deny"
      }
    ]
  },
  "prompt": "Own the investigation end-to-end. Use the available tools yourself. Do not ask the user to execute investigation commands. Write the final report under work/."
}
```

Este patrón permite demostrar un agent loop:

```text
objetivo
→ observar
→ decidir
→ tool call
→ observar resultado
→ replanificar
→ continuar
→ producir artefacto
```

---

## 31. Seguridad y mínimo privilegio

Una buena configuración combina:

```text
prompt
+
tools mínimas
+
permissions
+
human gate
```

Ejemplo:

```json
{
  "capability": "shell",
  "match": ["git push*", "rm -rf *", "sudo *"],
  "effect": "deny"
}
```

La regla general es:

> Si una restricción es importante, siempre que sea posible debe expresarse mediante permisos y arquitectura, no únicamente mediante lenguaje natural.

---

## 32. Checklist final

Antes de considerar terminado un agente:

```text
[ ] kiro-cli --version comprobado
[ ] archivo en .kiro/agents/
[ ] JSON o Markdown válido
[ ] tools correctas para la versión
[ ] permissions usa glob en CLI 3.x
[ ] resources existen
[ ] shell restringido al mínimo necesario
[ ] escritura restringida al mínimo necesario
[ ] human gate definido si procede
[ ] /agent list muestra el agente
[ ] /agent schema no muestra incompatibilidades
[ ] kiro-cli diagnostic sin errores relevantes
[ ] agente probado en una conversación nueva
```

---

## 33. Regla práctica

Para agentes nuevos:

```text
Kiro CLI 3.x
→ tags modernos
→ permissions.rules
→ glob
→ resources
```

Para agentes legacy que ya funcionan:

```text
pueden mantenerse temporalmente
porque CLI 3.x conserva compatibilidad
```

Cuando se evolucionen:

```text
migrar conscientemente
+
revisar los avisos de conversión
```

No mezclar ambas generaciones por accidente.

---

## 34. Referencias oficiales

- Kiro — Custom agents: https://kiro.dev/docs/custom-agents/
- Kiro — Agent configuration reference: https://kiro.dev/docs/custom-agents/configuration-reference/
- Kiro CLI 3.0 — Migration guide: https://kiro.dev/docs/cli/v3/migration-guide/
- Kiro CLI 3.0 — Upgrading agent configs: https://kiro.dev/docs/cli/v3/upgrade-agent/
- Kiro — Troubleshooting custom agents: https://kiro.dev/docs/cli/custom-agents/troubleshooting/
- Kiro CLI — Built-in tools: https://kiro.dev/docs/cli/reference/built-in-tools/
