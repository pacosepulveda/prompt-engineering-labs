# Tool Catalog — M03

Herramientas ficticias de solo lectura.

```bash
python labs/m03/tools/release_tool.py <tool> <change_id>
```

Tools disponibles:

- `test-summary`
- `security-review`
- `rollback-status`
- `known-issues`
- `monitoring-status`

Ejemplo:

```bash
python labs/m03/tools/release_tool.py test-summary CHG-482
```

Restricciones:

- todas son read-only;
- no existe una tool deploy;
- no existe una tool para modificar la política;
- un tool result es evidencia; una suposición del modelo no lo es.
