# Inicio rápido para alumnos

## Qué necesitas

Para la ruta oficial del curso solo necesitas:

- un navegador moderno;
- una cuenta personal de GitHub;
- acceso a Internet.

No es necesario instalar localmente Kiro, Python, Node.js ni los servidores MCP que utilicemos en los laboratorios.

---

## 1. Abrir el entorno

En la página del repositorio en GitHub:

1. Pulsa **Code**.
2. Abre la pestaña **Codespaces**.
3. Pulsa **Create codespace on main**.
4. Espera a que se abra VS Code en el navegador y finalice la preparación automática.

La primera creación puede tardar algunos minutos porque el entorno instala Kiro CLI automáticamente.

---

## 2. Iniciar sesión en Kiro

Abre una terminal en VS Code Web y ejecuta:

```bash
kiro-cli login
```

Selecciona **GitHub**.

Como Codespaces es un entorno remoto, Kiro utilizará un **device flow**:

1. la terminal mostrará una URL y un código temporal;
2. abre la URL en el navegador;
3. introduce el código;
4. autoriza Kiro;
5. vuelve a la terminal.

No es necesario configurar redirecciones de puertos para completar el inicio de sesión.

---

## 3. Comprobar que todo funciona

Ejecuta:

```bash
./scripts/check-environment.sh
```

Deberías ver Git, Python, Node.js y Kiro CLI disponibles. El script también comprobará si Kiro está autenticado.

Si Kiro aparece como no autenticado, ejecuta de nuevo:

```bash
kiro-cli login
```

---

## 4. Iniciar Kiro

Desde la raíz del repositorio:

```bash
kiro-cli
```

A partir de aquí sigue las instrucciones del laboratorio correspondiente.

---

## Si ya utilizas Kiro o Copilot

Puedes trabajar con tu entorno habitual clonando este repositorio. Sin embargo, para poder avanzar juntos durante la sesión, la configuración soportada por el instructor será GitHub Codespaces.

---

## Al terminar la clase

Detén el Codespace cuando ya no lo estés utilizando para no consumir innecesariamente tu cuota de Codespaces.
