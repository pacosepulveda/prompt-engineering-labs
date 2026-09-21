# Resolución rápida de problemas

## `kiro-cli: command not found`

Abre una nueva terminal. Si continúa:

```bash
export PATH="$HOME/.local/bin:$PATH"
kiro-cli --version
```

Si todavía falla, vuelve a crear o reconstruir el Codespace.

## Kiro no está autenticado

```bash
kiro-cli login
```

En un Codespace se utiliza el flujo de dispositivo: copia la URL y el código que muestre la terminal y completa la autorización en el navegador.

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
