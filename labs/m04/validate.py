#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))

TOOL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["tool", "arguments"],
    "properties": {
        "tool": {"type": "string", "enum": ["get_service_owner"]},
        "arguments": {
            "type": "object",
            "additionalProperties": False,
            "required": ["service"],
            "properties": {
                "service": {
                    "type": "string",
                    "enum": ["identity-api", "billing-api", "web-portal"]
                }
            }
        }
    }
}

OWNERS = {
    "identity-api": {"owner": "platform-identity", "runbook": "RB-ID-021"},
    "billing-api": {"owner": "payments-platform", "runbook": "RB-BILL-008"},
    "web-portal": {"owner": "web-experience", "runbook": "RB-WEB-014"},
}

def schema_errors(data, schema):
    validator = Draft202012Validator(schema)
    return sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))

def print_schema_errors(errors):
    for e in errors:
        path = ".".join(str(x) for x in e.absolute_path) or "<root>"
        print(f"SCHEMA_ERROR at {path}: {e.message}")

def semantic_errors(d):
    """Validate deterministic business rules for the training incident.

    Grounding of free-text fields such as summary/evidence is intentionally
    reviewed separately against incident.txt.
    """
    errors = []

    if d["incident_id"] == "TKT-1042":
        if d["category"] != "authentication":
            errors.append(
                "TKT-1042 describes HTTP 401 during session refresh; "
                "category must be authentication"
            )

        if d["severity"] != "P2":
            errors.append(
                "TKT-1042 is production, affects 37 users and has confirmed "
                "functional impact; severity must be P2"
            )

        if d["suspected_cause"] is not None:
            errors.append(
                "TKT-1042 has no confirmed root cause; suspected_cause must be null"
            )

        if d["recommended_action"] != "open_bug":
            errors.append(
                "TKT-1042 is sufficiently described for recommended_action=open_bug"
            )

    return errors

def validate_incident(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"SYNTAX_ERROR: {exc}")
        return 2

    print("SYNTAX_VALID")

    errors = schema_errors(data, SCHEMA)
    if errors:
        print_schema_errors(errors)
        return 3

    print("SCHEMA_VALID")

    sem = semantic_errors(data)
    if sem:
        for error in sem:
            print(f"SEMANTIC_ERROR: {error}")
        return 4

    print("SEMANTIC_VALID")
    print(
        "GROUNDING_REVIEW_REQUIRED | compare summary/evidence with incident.txt"
    )
    return 0

def validate_tool_call(path, execute=False):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"TOOL_CALL_SYNTAX_ERROR: {exc}")
        return 2

    errors = schema_errors(data, TOOL_SCHEMA)
    if errors:
        print_schema_errors(errors)
        return 3

    print("TOOL_CALL_VALID")

    if execute:
        service = data["arguments"]["service"]
        result = {
            "service": service,
            **OWNERS[service]
        }
        print("TOOL_RESULT:")
        print(json.dumps(result, indent=2))

    return 0

def demo():
    print("=== 1. SYNTAX ERROR ===")
    bad = '{"severity": "P2",}'
    try:
        json.loads(bad)
    except Exception as exc:
        print(f"SYNTAX_ERROR: {exc}")

    print("\n=== 2. SCHEMA ERROR ===")
    schema_bad = {
        "incident_id": "TKT-1042",
        "service": "identity-api",
        "environment": "production",
        "category": "authentication",
        "severity": "HIGH",
        "affected_users": 37,
        "summary": "Users receive HTTP 401 after idle sessions.",
        "evidence": ["37 users affected."],
        "suspected_cause": None,
        "recommended_action": "open_bug"
    }
    print("SYNTAX_VALID")
    print_schema_errors(schema_errors(schema_bad, SCHEMA))

    print("\n=== 3. SEMANTIC ERROR ===")
    semantic_bad = {
        "incident_id": "TKT-1042",
        "service": "identity-api",
        "environment": "production",
        "category": "authentication",
        "severity": "P3",
        "affected_users": 37,
        "summary": "Users receive HTTP 401 after idle sessions.",
        "evidence": ["37 users affected."],
        "suspected_cause": None,
        "recommended_action": "open_bug"
    }
    print("SYNTAX_VALID")
    errors = schema_errors(semantic_bad, SCHEMA)
    if not errors:
        print("SCHEMA_VALID")
    for error in semantic_errors(semantic_bad):
        print(f"SEMANTIC_ERROR: {error}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--tool-call", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    if args.demo:
        demo()
        return

    if not args.file:
        parser.error("file is required unless --demo is used")

    if args.tool_call:
        sys.exit(validate_tool_call(args.file, args.execute))

    sys.exit(validate_incident(args.file))

if __name__ == "__main__":
    main()
