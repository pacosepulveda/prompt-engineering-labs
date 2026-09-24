#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

Service = Literal["identity-api", "billing-api", "web-portal"]
IncidentId = Literal["INC-2041"]
Action = Literal["restart_service"]

ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / "work"
DB_PATH = WORK_DIR / "ops.db"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def audit(
    conn: sqlite3.Connection,
    event_type: str,
    subject: str,
    outcome: str,
    detail: str,
) -> None:
    conn.execute(
        """
        INSERT INTO audit(timestamp, event_type, subject, outcome, detail)
        VALUES (?, ?, ?, ?, ?)
        """,
        (now_iso(), event_type, subject, outcome, detail),
    )


def init_db(force: bool = False) -> None:
    if force and DB_PATH.exists():
        DB_PATH.unlink()

    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS services (
                service TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                region TEXT NOT NULL,
                availability REAL NOT NULL,
                error_rate REAL NOT NULL,
                p95_latency_ms INTEGER NOT NULL,
                baseline_p95_latency_ms INTEGER NOT NULL,
                rca_status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS incidents (
                incident_id TEXT PRIMARY KEY,
                service TEXT NOT NULL,
                environment TEXT NOT NULL,
                status TEXT NOT NULL,
                summary TEXT NOT NULL,
                affected_users INTEGER NOT NULL,
                FOREIGN KEY(service) REFERENCES services(service)
            );

            CREATE TABLE IF NOT EXISTS changes (
                change_id TEXT PRIMARY KEY,
                incident_id TEXT NOT NULL,
                service TEXT NOT NULL,
                action TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL,
                maintenance_window TEXT NOT NULL,
                created_at TEXT NOT NULL,
                executed_at TEXT,
                FOREIGN KEY(incident_id) REFERENCES incidents(incident_id),
                FOREIGN KEY(service) REFERENCES services(service)
            );

            CREATE TABLE IF NOT EXISTS policies (
                policy_id TEXT PRIMARY KEY,
                service TEXT NOT NULL,
                environment TEXT NOT NULL,
                action TEXT NOT NULL,
                version TEXT NOT NULL,
                status TEXT NOT NULL,
                effective_date TEXT NOT NULL,
                create_requirements_json TEXT NOT NULL,
                execution_requirements_json TEXT NOT NULL,
                required_change_status TEXT NOT NULL,
                maintenance_window_required TEXT NOT NULL,
                approval_authority TEXT NOT NULL,
                approval_via_mcp_available INTEGER NOT NULL,
                important TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                outcome TEXT NOT NULL,
                detail TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )

        if conn.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO services VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        "identity-api",
                        "degraded",
                        "eu-central",
                        99.94,
                        0.6,
                        820,
                        420,
                        "investigating",
                    ),
                    (
                        "billing-api",
                        "healthy",
                        "eu-central",
                        99.99,
                        0.08,
                        210,
                        205,
                        "not_applicable",
                    ),
                    (
                        "web-portal",
                        "healthy",
                        "global",
                        99.98,
                        0.12,
                        310,
                        295,
                        "not_applicable",
                    ),
                ],
            )
            conn.execute(
                "INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "INC-2041",
                    "identity-api",
                    "production",
                    "investigating",
                    (
                        "Users experience intermittent session refresh failures "
                        "and must sign in again."
                    ),
                    37,
                ),
            )
            conn.execute(
                "INSERT INTO changes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "CR-0043",
                    "INC-2041",
                    "identity-api",
                    "restart_service",
                    (
                        "Pre-approved controlled restart for the training "
                        "maintenance window."
                    ),
                    "approved",
                    "open",
                    now_iso(),
                    None,
                ),
            )
            conn.execute(
                "INSERT INTO meta(key, value) VALUES ('next_change_number', '1001')"
            )
            audit(
                conn,
                "LAB_INITIALIZED",
                "ops-lab",
                "OK",
                "Synthetic Telvora Ops state initialized",
            )

        if conn.execute("SELECT COUNT(*) FROM policies").fetchone()[0] == 0:
            conn.execute(
                """
                INSERT INTO policies (
                    policy_id,
                    service,
                    environment,
                    action,
                    version,
                    status,
                    effective_date,
                    create_requirements_json,
                    execution_requirements_json,
                    required_change_status,
                    maintenance_window_required,
                    approval_authority,
                    approval_via_mcp_available,
                    important
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "POL-CHANGE-017",
                    "identity-api",
                    "production",
                    "restart_service",
                    "3.2",
                    "ACTIVE",
                    "2026-08-15",
                    json.dumps([
                        "open incident for the same service",
                        "non-empty operational reason",
                    ]),
                    json.dumps([
                        "change status = approved",
                        "change service matches target service",
                        "change action = restart_service",
                        "maintenance_window = open",
                    ]),
                    "approved",
                    "open",
                    "change-management",
                    0,
                    "Creating a change request does not approve or execute it.",
                ),
            )


def row_to_dict(row: sqlite3.Row | None) -> dict | None:
    return dict(row) if row is not None else None


def get_incident_data(incident_id: str) -> dict:
    init_db()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM incidents WHERE incident_id = ?",
            (incident_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"Unknown incident: {incident_id}")

    return row_to_dict(row)


def get_service_health_data(service: str) -> dict:
    init_db()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM services WHERE service = ?",
            (service,),
        ).fetchone()

    if row is None:
        raise ValueError(f"Unsupported service: {service}")

    return row_to_dict(row)


def get_change_policy_data(service: str, action: str) -> dict:
    init_db()

    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM policies
            WHERE service = ?
              AND action = ?
              AND environment = 'production'
              AND status = 'ACTIVE'
            ORDER BY effective_date DESC
            LIMIT 1
            """,
            (service, action),
        ).fetchone()

    if row is None:
        raise ValueError(
            f"No active production policy for {service} / {action}"
        )

    policy = dict(row)
    policy["create_request_requires"] = json.loads(
        policy.pop("create_requirements_json")
    )
    policy["execution_requires"] = json.loads(
        policy.pop("execution_requirements_json")
    )
    policy["approval_via_mcp_available"] = bool(
        policy["approval_via_mcp_available"]
    )
    return policy


def next_change_id(conn: sqlite3.Connection) -> str:
    row = conn.execute(
        "SELECT value FROM meta WHERE key = 'next_change_number'"
    ).fetchone()
    number = int(row[0])

    conn.execute(
        "UPDATE meta SET value = ? WHERE key = 'next_change_number'",
        (str(number + 1),),
    )

    return f"CR-{number:04d}"


def create_change_request_data(
    incident_id: str,
    service: str,
    action: str,
    reason: str,
) -> dict:
    init_db()
    reason = reason.strip()

    if len(reason) < 15:
        raise ValueError("reason must contain at least 15 characters")

    if action != "restart_service":
        raise ValueError("Only restart_service is supported in this lab")

    with connect() as conn:
        incident = conn.execute(
            "SELECT * FROM incidents WHERE incident_id = ?",
            (incident_id,),
        ).fetchone()

        if incident is None:
            raise ValueError(f"Unknown incident: {incident_id}")

        if incident["status"] not in {"open", "investigating", "monitoring"}:
            raise ValueError(f"Incident {incident_id} is not active")

        if incident["service"] != service:
            raise ValueError(
                f"Incident {incident_id} belongs to "
                f"{incident['service']}, not {service}"
            )

        change_id = next_change_id(conn)
        created_at = now_iso()

        conn.execute(
            "INSERT INTO changes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                change_id,
                incident_id,
                service,
                action,
                reason,
                "pending_approval",
                "open",
                created_at,
                None,
            ),
        )

        audit(
            conn,
            "CHANGE_CREATED",
            change_id,
            "PENDING_APPROVAL",
            f"{action} requested for {service} under {incident_id}",
        )

    return {
        "change_id": change_id,
        "incident_id": incident_id,
        "service": service,
        "action": action,
        "status": "pending_approval",
        "maintenance_window": "open",
        "created_at": created_at,
        "message": (
            "Change request created. It is NOT approved "
            "and has NOT been executed."
        ),
    }


def get_change_status_data(change_id: str) -> dict:
    init_db()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM changes WHERE change_id = ?",
            (change_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"Unknown change: {change_id}")

    return row_to_dict(row)


def execute_restart_data(change_id: str) -> dict:
    init_db()

    with connect() as conn:
        change = conn.execute(
            "SELECT * FROM changes WHERE change_id = ?",
            (change_id,),
        ).fetchone()

        if change is None:
            audit(
                conn,
                "RESTART_DENIED",
                change_id,
                "DENIED",
                "Unknown change request",
            )
            return {
                "allowed": False,
                "code": "DENIED_UNKNOWN_CHANGE",
                "change_id": change_id,
            }

        policy = conn.execute(
            """
            SELECT *
            FROM policies
            WHERE service = ?
              AND action = ?
              AND environment = 'production'
              AND status = 'ACTIVE'
            ORDER BY effective_date DESC
            LIMIT 1
            """,
            (change["service"], change["action"]),
        ).fetchone()

        if policy is None:
            audit(
                conn,
                "RESTART_DENIED",
                change_id,
                "DENIED",
                "No active policy for requested action",
            )
            return {
                "allowed": False,
                "code": "DENIED_NO_ACTIVE_POLICY",
                "change_id": change_id,
            }

        if change["action"] != "restart_service":
            audit(
                conn,
                "RESTART_DENIED",
                change_id,
                "DENIED",
                "Wrong action",
            )
            return {
                "allowed": False,
                "code": "DENIED_ACTION_MISMATCH",
                "change_id": change_id,
            }

        if change["status"] != policy["required_change_status"]:
            audit(
                conn,
                "RESTART_DENIED",
                change_id,
                "DENIED",
                (
                    f"Change status is {change['status']}; "
                    f"{policy['required_change_status']} is required"
                ),
            )
            return {
                "allowed": False,
                "code": "DENIED_CHANGE_NOT_APPROVED",
                "change_id": change_id,
                "change_status": change["status"],
                "required_status": policy["required_change_status"],
                "message": "Backend authorization denied execution.",
            }

        if change["maintenance_window"] != policy["maintenance_window_required"]:
            audit(
                conn,
                "RESTART_DENIED",
                change_id,
                "DENIED",
                (
                    "Maintenance window does not satisfy policy: "
                    f"{policy['maintenance_window_required']} required"
                ),
            )
            return {
                "allowed": False,
                "code": "DENIED_MAINTENANCE_WINDOW_CLOSED",
                "change_id": change_id,
            }

        service = change["service"]

        conn.execute(
            """
            UPDATE services
            SET status = 'healthy',
                availability = 99.99,
                error_rate = 0.10,
                p95_latency_ms = 430,
                rca_status = 'monitoring'
            WHERE service = ?
            """,
            (service,),
        )

        executed_at = now_iso()

        conn.execute(
            """
            UPDATE changes
            SET status = 'executed', executed_at = ?
            WHERE change_id = ?
            """,
            (executed_at, change_id),
        )

        conn.execute(
            """
            UPDATE incidents
            SET status = 'monitoring'
            WHERE incident_id = ?
            """,
            (change["incident_id"],),
        )

        audit(
            conn,
            "RESTART_EXECUTED",
            change_id,
            "EXECUTED",
            f"Controlled restart executed for {service}",
        )

    return {
        "allowed": True,
        "code": "RESTART_EXECUTED",
        "change_id": change_id,
        "service": service,
        "executed_at": executed_at,
        "message": (
            "Synthetic controlled restart executed "
            "and service health updated."
        ),
    }


def get_audit_events_data(limit: int = 10) -> list[dict]:
    init_db()

    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not 1 <= limit <= 20
    ):
        raise ValueError("limit must be an integer between 1 and 20")

    with connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM audit
            ORDER BY event_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def snapshot() -> dict:
    init_db()

    with connect() as conn:
        service = conn.execute(
            """
            SELECT * FROM services
            WHERE service = 'identity-api'
            """
        ).fetchone()

        incident = conn.execute(
            """
            SELECT * FROM incidents
            WHERE incident_id = 'INC-2041'
            """
        ).fetchone()

        changes = conn.execute(
            """
            SELECT change_id, incident_id, service, action,
                   status, maintenance_window, executed_at
            FROM changes
            ORDER BY change_id
            """
        ).fetchall()

        policies = conn.execute(
            """
            SELECT policy_id, service, environment, action,
                   version, status, effective_date,
                   create_requirements_json,
                   execution_requirements_json,
                   required_change_status,
                   maintenance_window_required,
                   approval_authority,
                   approval_via_mcp_available,
                   important
            FROM policies
            ORDER BY service, action, effective_date DESC
            """
        ).fetchall()

        audit_rows = conn.execute(
            """
            SELECT event_id, event_type, subject, outcome, detail
            FROM audit
            ORDER BY event_id DESC
            LIMIT 10
            """
        ).fetchall()

    return {
        "service": dict(service),
        "incident": dict(incident),
        "changes": [dict(row) for row in changes],
        "policies": [
            {
                **dict(row),
                "create_requirements": json.loads(
                    row["create_requirements_json"]
                ),
                "execution_requirements": json.loads(
                    row["execution_requirements_json"]
                ),
                "approval_via_mcp_available": bool(
                    row["approval_via_mcp_available"]
                ),
            }
            for row in policies
        ],
        "audit": [dict(row) for row in audit_rows],
    }


def run_mcp() -> None:
    from mcp.server import MCPServer

    mcp = MCPServer("telvora-ops")

    @mcp.tool()
    def get_incident(incident_id: IncidentId) -> dict:
        """Read one operational incident. READ ONLY."""
        return get_incident_data(incident_id)

    @mcp.tool()
    def get_service_health(service: Service) -> dict:
        """Read current service health and telemetry. READ ONLY."""
        return get_service_health_data(service)

    @mcp.tool()
    def get_change_policy(service: Service, action: Action) -> dict:
        """Read the production change policy. READ ONLY."""
        return get_change_policy_data(service, action)

    @mcp.tool()
    def get_change_status(change_id: str) -> dict:
        """Read the status of a change request. READ ONLY."""
        return get_change_status_data(change_id)

    @mcp.tool()
    def create_change_request(
        incident_id: IncidentId,
        service: Service,
        action: Action,
        reason: str,
    ) -> dict:
        """Create a PENDING change request.

        WRITE SIDE EFFECT.
        This tool does NOT approve or execute the change.
        """
        return create_change_request_data(
            incident_id,
            service,
            action,
            reason,
        )

    @mcp.tool()
    def execute_restart(change_id: str) -> dict:
        """Execute a controlled synthetic restart only if backend policy allows it.

        WRITE SIDE EFFECT.
        The backend requires an APPROVED change and an open maintenance window.
        """
        return execute_restart_data(change_id)

    @mcp.tool()
    def get_audit_events(limit: int = 10) -> list[dict]:
        """Read recent Telvora Ops audit events. READ ONLY."""
        return get_audit_events_data(limit)

    mcp.run()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Telvora Ops MCP training service"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="reset the synthetic lab state",
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="show current synthetic lab state",
    )
    args = parser.parse_args()

    if args.reset:
        init_db(force=True)
        print("LAB_RESET_OK")
        print(json.dumps(snapshot(), indent=2))
        return

    if args.snapshot:
        print(json.dumps(snapshot(), indent=2))
        return

    init_db()
    run_mcp()


if __name__ == "__main__":
    main()
