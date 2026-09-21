#!/usr/bin/env bash
set -u

PASS=0
WARN=0

ok()   { printf '✅ %s\n' "$1"; PASS=$((PASS+1)); }
warn() { printf '⚠️  %s\n' "$1"; WARN=$((WARN+1)); }

printf '\nComprobación del entorno del curso\n'
printf '%s\n' '----------------------------------'

if command -v git >/dev/null 2>&1; then
  ok "Git: $(git --version)"
else
  warn 'Git no está disponible.'
fi

if command -v python >/dev/null 2>&1; then
  ok "Python: $(python --version 2>&1)"
else
  warn 'Python no está disponible.'
fi

if command -v node >/dev/null 2>&1; then
  ok "Node.js: $(node --version)"
else
  warn 'Node.js no está disponible.'
fi

if python -c "import jsonschema" >/dev/null 2>&1; then
  ok 'Python package: jsonschema'
else
  warn 'Falta jsonschema. Ejecuta: python -m pip install --user -r requirements.txt'
fi

if python -c "import yaml" >/dev/null 2>&1; then
  ok 'Python package: PyYAML'
else
  warn 'Falta PyYAML. Ejecuta: python -m pip install --user -r requirements.txt'
fi

if command -v kiro-cli >/dev/null 2>&1; then
  ok "Kiro CLI: $(kiro-cli --version 2>&1 | head -n 1)"
  if kiro-cli whoami >/dev/null 2>&1; then
    ok 'Kiro: sesión autenticada.'
  else
    warn 'Kiro está instalado, pero todavía no has iniciado sesión. Ejecuta: kiro-cli login'
  fi
else
  warn 'Kiro CLI no está disponible. Reconstruye el Codespace o ejecuta el instalador oficial.'
fi

printf '\nResultado: %d comprobaciones correctas, %d avisos.\n' "$PASS" "$WARN"

if [ "$WARN" -eq 0 ]; then
  printf 'El entorno está listo para los laboratorios.\n\n'
else
  printf 'Revisa los avisos anteriores antes de comenzar.\n\n'
fi
