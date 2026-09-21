#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts" / "tool-call.schema.json").read_text(encoding="utf-8"))

DATA = {
    "identity-api": {"owner": "platform-identity", "runbook": "RB-ID-021"},
    "billing-api": {"owner": "payments-platform", "runbook": "RB-BILL-008"},
    "web-portal": {"owner": "web-experience", "runbook": "RB-WEB-014"},
}

def fail(msg, code=2):
    print(msg)
    sys.exit(code)

if len(sys.argv) != 2:
    fail("Usage: execute_tool.py <tool-call.json>")

try:
    call = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"TOOL_CALL_SYNTAX_ERROR: {exc}")

errors = sorted(Draft202012Validator(SCHEMA).iter_errors(call), key=lambda e: list(e.absolute_path))
if errors:
    for e in errors:
        path = ".".join(str(x) for x in e.absolute_path) or "<root>"
        print(f"TOOL_CALL_SCHEMA_ERROR at {path}: {e.message}")
    sys.exit(3)

ALLOWED = {"get_service_owner","get_runbook"}
if call["tool"] not in ALLOWED:
    fail("TOOL_CALL_DENIED: tool not in allowlist", 4)

service = call["arguments"]["service"]
record = DATA.get(service)
if not record:
    fail("TOOL_CALL_ARGUMENT_ERROR: unknown service", 4)

print("TOOL_CALL_VALID")
if call["tool"] == "get_service_owner":
    result = {"service":service,"owner":record["owner"],"runbook":record["runbook"]}
else:
    result = {"service":service,"runbook":record["runbook"]}

print("TOOL_RESULT:")
print(json.dumps(result, indent=2))
