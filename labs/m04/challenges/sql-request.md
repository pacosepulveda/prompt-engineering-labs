# Reto opcional — SQL como artefacto

Dispones únicamente de:

```text
incidents(id, service, severity, created_at)
```

Recupera id, service, severity y created_at para:

```text
service = identity-api
created_at >= 2026-09-01
```

Genera:

```json
{
  "sql": "...",
  "params": {}
}
```

Restricciones:

- SELECT únicamente;
- no SELECT *;
- no concatenes valores dentro de la consulta;
- utiliza parámetros nombrados;
- no inventes tablas ni columnas;
- no ejecutes el SQL.
