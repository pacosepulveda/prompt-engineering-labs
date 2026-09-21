#!/usr/bin/env python3
import json
import sys

if len(sys.argv) != 2 or sys.argv[1] != "CHG-482":
    print("Usage: python labs/m03/tool.py CHG-482")
    sys.exit(2)

result = {
    "change_id": "CHG-482",
    "release_blocking_tests": {
        "status": "FAIL",
        "failure": "AUTH-217: refresh token after idle session"
    },
    "known_issues": {
        "sev1_open": 0,
        "sev2_open": 0
    },
    "rollback": {
        "plan_exists": True,
        "last_rehearsal_days_ago": 12,
        "result": "PASS"
    },
    "monitoring": {
        "dashboard": "auth-token-lifecycle",
        "alerts_enabled": True,
        "owner": "platform-observability",
        "status": "PASS"
    },
    "security_review": {
        "review_id": "SEC-884",
        "status": "PASS",
        "open_blockers": 0
    }
}

print(json.dumps(result, indent=2))
