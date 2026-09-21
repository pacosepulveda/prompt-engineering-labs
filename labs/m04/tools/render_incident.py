#!/usr/bin/env python3
import csv, io, json, sys
from pathlib import Path
import yaml

if len(sys.argv) != 2:
    print("Usage: render_incident.py <validated-json>")
    sys.exit(2)

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

print("=== YAML ===")
print(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))

print("=== CSV ===")
fields = ["incident_id","service","environment","category","severity","affected_users","contains_sensitive_data","recommended_action"]
buf = io.StringIO()
writer = csv.DictWriter(buf, fieldnames=fields)
writer.writeheader()
writer.writerow({k: data.get(k) for k in fields})
print(buf.getvalue().strip())

print("=== MARKDOWN ===")
print(f"# {data['incident_id']}")
print()
print(f"- Service: {data['service']}")
print(f"- Environment: {data['environment']}")
print(f"- Category: {data['category']}")
print(f"- Severity: {data['severity']}")
print(f"- Action: {data['recommended_action']}")
print()
print(data["summary"])
