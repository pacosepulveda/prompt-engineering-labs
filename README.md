# Prompt Engineering Labs

Repositorio de prácticas para el curso de **Prompt Engineering**.

## Ruta recomendada para los alumnos

La ruta soportada durante el curso es **GitHub Codespaces**. No es necesario instalar Kiro, Python, Node.js ni otras herramientas localmente.

1. Abre este repositorio en GitHub.
2. Selecciona **Code > Codespaces > Create codespace on main**.
3. Espera a que VS Code Web termine de preparar el entorno.
4. Abre una terminal.
5. Ejecuta:

```bash
kiro-cli login --use-device-flow
```

6. Elige **GitHub** como método de autenticación, abre la URL que muestre la terminal e introduce el código temporal.
7. Comprueba el entorno:

```bash
./scripts/check-environment.sh
```

8. Inicia Kiro:

```bash
kiro-cli
```

Consulta [Inicio rápido para alumnos](docs/00_INICIO_RAPIDO.md) si necesitas instrucciones más detalladas.

## Uso de un entorno local

Si ya utilizas Kiro IDE, Kiro CLI, GitHub Copilot u otro entorno compatible, puedes clonar el repositorio y trabajar localmente. Durante las sesiones, la ruta que se dará por soportada será Codespaces para evitar problemas de versiones y dependencias.

## Estructura

```text
.
├── .devcontainer/        # Configuración automática de Codespaces
├── docs/                 # Guías de uso del entorno
├── labs/                 # Laboratorios del curso
├── scripts/              # Comprobaciones y utilidades
└── README.md
```

Los laboratorios M01–M10 están organizados en este repositorio y utilizan Codespaces como entorno común de referencia. Kiro es la herramienta de referencia en varias prácticas, pero cada laboratorio indica cuándo puede sustituirse por una alternativa equivalente.
