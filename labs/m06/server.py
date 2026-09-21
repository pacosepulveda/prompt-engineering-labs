#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from mcp.server import MCPServer

Service = Literal["identity-api", "billing-api", "web-portal"]
ChangeType = Literal["restart_service", "change_cache_policy"]

mcp = MCPServer("ops-lab")

SERVICES = {
    "identity-api": {
        "status": "degraded",
        "region": "eu-central",
        "availability": 99.94,
        "error_rate": 0.6,
        "p95_latency_ms": 820,
        "baseline_p95_latency_ms": 420,
        "rca_status": "investigating",
    },
    "billing-api": {
        "status": "healthy",
        "region": "eu-central",
        "availability": 99.99,
        "error_rate": 0.08,
        "p95_latency_ms": 210,
        "baseline_p95_latency_ms": 205,
        "rca_status": "not_applicable",
    },
    "web-portal": {
        "status": "healthy",
        "region": "global",
        "availability": 99.98,
        "error_rate": 0.12,
        "p95_latency_ms": 310,
        "baseline_p95_latency_ms": 295,
        "rca_status": "not_applicable",
    },
}

WORK_DIR = Path(__file__).resolve().parent / "work"
CHANGE_LOG = WORK_DIR / "changes.jsonl"


@mcp.tool()
def get_service_status(service: Service) -> dict:
    """Read the current synthetic operational status of one supported service.

    This tool is read-only and has no side effects.
    Use it when current service status or telemetry is required.
    """
    if service not in SERVICES:
        raise ValueError(f"Unsupported service: {service}")

    return {
        "service": service,
        **SERVICES[service],
    }


@mcp.tool()
def create_change_request(
    service: Service,
    change_type: ChangeType,
    reason: str,
) -> dict:
    """Create a synthetic change request for later human approval.

    SIDE EFFECT: appends one record to labs/m06/work/changes.jsonl.
    This tool does NOT restart services or apply configuration changes.
    Use it only when the user explicitly asks to create a change request.
    """
    reason = reason.strip()
    if len(reason) < 10:
        raise ValueError("reason must contain at least 10 characters")

    WORK_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "change_id": f"CR-{uuid4().hex[:8].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending_approval",
        "service": service,
        "change_type": change_type,
        "reason": reason,
    }

    with CHANGE_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")

    return record


if __name__ == "__main__":
    mcp.run()
