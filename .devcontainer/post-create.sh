#!/usr/bin/env bash
set -euo pipefail

printf '\n== Preparando entorno del curso ==\n'

# El instalador oficial de Kiro CLI instala el binario para el usuario actual.
if ! command -v kiro-cli >/dev/null 2>&1; then
  echo 'Instalando Kiro CLI...'
  curl -fsSL https://cli.kiro.dev/install | bash
else
  echo 'Kiro CLI ya está instalado.'
fi

# El instalador utiliza ~/.local/bin en Linux. Lo añadimos al PATH de las
# nuevas terminales y también a la sesión actual del postCreateCommand.
if ! grep -Fq 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
export PATH="$HOME/.local/bin:$PATH"

chmod +x scripts/*.sh 2>/dev/null || true

printf '\n== Versiones disponibles ==\n'
printf 'Git:     '; git --version || true
printf 'GitHub:  '; gh --version 2>/dev/null | head -n 1 || echo 'gh no disponible'
printf 'Python:  '; python --version || true
printf 'Node:    '; node --version || true
printf 'Kiro:    '; kiro-cli --version || true

printf '\nEntorno preparado. Para comenzar:\n'
printf '  1. kiro-cli login --use-device-flow\n'
printf '  2. ./scripts/check-environment.sh\n'
printf '  3. kiro-cli\n\n'
