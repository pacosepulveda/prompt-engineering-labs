# Resolución rápida de problemas

## `kiro-cli: command not found`

Abre una nueva terminal. Si continúa:

```bash
export PATH="$HOME/.local/bin:$PATH"
kiro-cli --version
```

Si todavía falla, vuelve a crear o reconstruir el Codespace.

## `Failed to open browser for authentication`

En Codespaces no uses el login que intenta abrir un navegador directamente. Ejecuta:

```bash
kiro-cli login --use-device-flow
```

La terminal mostrará una URL y un código temporal. Abre la URL en tu navegador local, introduce el código y completa la autorización.

## Kiro no está autenticado

```bash
kiro-cli login --use-device-flow
```

## Quiero comprobar mi sesión

```bash
kiro-cli whoami
```

## Kiro se comporta de forma anómala

```bash
kiro-cli doctor
```

## El entorno no coincide con el del resto de la clase

Si estás utilizando un entorno local, cambia temporalmente a la ruta oficial del curso creando un GitHub Codespace desde el repositorio.
