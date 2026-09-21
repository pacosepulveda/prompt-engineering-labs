#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "incident.schema.json"

SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_]+", re.I),
    re.compile(r"bearer\s+[A-Za-z0-9._\-]+", re.I),
    re.compile(r"password\s*[:=]\s*\S+", re.I),
]

def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"SYNTAX_ERROR: {exc}")
        sys.exit(2)

def schema_errors(data):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))

def contains_literal_secret(value):
    strings = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, list):
        strings.extend(x for x in value if isinstance(x, str))
    return any(p.search(s) for s in strings for p in SECRET_PATTERNS)

def semantic_errors(d):
    errors = []
    if d["contains_sensitive_data"] and d["recommended_action"] != "escalate_security":
        errors.append("contains_sensitive_data=true requires recommended_action=escalate_security")
    if contains_literal_secret(d["summary"]) or contains_literal_secret(d["evidence"]):
        errors.append("output reproduces a secret-like value")
    if d["contains_sensitive_data"] and d["category"] != "security":
        errors.append("sensitive data requires category=security")
    if d["service"] == "unknown":
        if "service" not in d["missing_fields"]:
            errors.append("service=unknown requires 'service' in missing_fields")
        if d["recommended_action"] not in ("request_more_info", "escalate_security"):
            errors.append("unknown service requires request_more_info unless security escalation takes priority")

    env, users = d["environment"], d["affected_users"]
    summary = d["summary"].lower()
    functional = d["category"] in ("availability","performance","authentication","data")
    unavailable = "unavailable" in summary or "complete outage" in summary

    if env == "production" and unavailable and isinstance(users, int) and users >= 100:
        expected = "P1"
    elif env == "production" and functional and isinstance(users, int) and users >= 25:
        expected = "P2"
    elif functional:
        expected = "P3"
    elif d["category"] == "other":
        expected = "P4"
    else:
        expected = d["severity"]

    if d["category"] != "security" and d["severity"] != expected:
        errors.append(f"severity should be {expected} according to the training policy")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--schema-only", action="store_true")
    args = parser.parse_args()

    data = load_json(args.file)
    errors = schema_errors(data)
    if errors:
        for e in errors:
            path = ".".join(str(x) for x in e.absolute_path) or "<root>"
            print(f"SCHEMA_ERROR at {path}: {e.message}")
        sys.exit(3)

    print("SCHEMA_VALID")
    if args.schema_only:
        return

    sem = semantic_errors(data)
    if sem:
        for e in sem:
            print(f"SEMANTIC_ERROR: {e}")
        sys.exit(4)

    print("SEMANTIC_VALID")

if __name__ == "__main__":
    main()
