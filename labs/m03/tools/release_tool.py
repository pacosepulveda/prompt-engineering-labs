#!/usr/bin/env python3
import argparse
import json
import sys

DATA = {
    "CHG-482": {
        "test-summary": {
            "change_id": "CHG-482",
            "total": 124,
            "passed": 123,
            "failed": 1,
            "release_blocking_failures": [
                {
                    "test_id": "AUTH-217",
                    "name": "refresh token after idle session",
                    "status": "failed"
                }
            ]
        },
        "security-review": {
            "change_id": "CHG-482",
            "status": "approved",
            "review_id": "SEC-884",
            "scope": "authentication and token lifecycle",
            "open_blockers": 0
        },
        "rollback-status": {
            "change_id": "CHG-482",
            "plan_exists": True,
            "last_rehearsal_days_ago": 12,
            "result": "passed"
        },
        "known-issues": {
            "change_id": "CHG-482",
            "sev1_open": 0,
            "sev2_open": 0,
            "related_issue_ids": []
        },
        "monitoring-status": {
            "change_id": "CHG-482",
            "dashboard": "auth-token-lifecycle",
            "alerts_enabled": True,
            "owner": "platform-observability",
            "status": "ready"
        }
    }
}

TOOLS = [
    "test-summary",
    "security-review",
    "rollback-status",
    "known-issues",
    "monitoring-status"
]

parser = argparse.ArgumentParser(description="Synthetic read-only evidence tool for M03.")
parser.add_argument("tool")
parser.add_argument("change_id", nargs="?")
args = parser.parse_args()

if args.tool == "list-tools":
    print(json.dumps({"tools": TOOLS}, indent=2))
    sys.exit(0)

if args.tool not in TOOLS:
    print(json.dumps({"error": "unknown_tool", "allowed_tools": TOOLS}, indent=2))
    sys.exit(2)

if not args.change_id:
    print(json.dumps({"error": "change_id_required"}, indent=2))
    sys.exit(2)

change = DATA.get(args.change_id)
if not change:
    print(json.dumps({"error": "change_not_found", "change_id": args.change_id}, indent=2))
    sys.exit(3)

print(json.dumps(change[args.tool], indent=2))
