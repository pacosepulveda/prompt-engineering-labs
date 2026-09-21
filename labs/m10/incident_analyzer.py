"""Small incident analysis module used by the M10 AI Engineering capstone."""


def _format_summary_legacy(service, status, affected_users, error_rate):
    """Build the existing human-readable summary.

    This helper is intentionally old-fashioned. Its current behavior is part of
    the regression contract even if its implementation is later refactored.
    """
    parts = [f"{service}: {status}"]

    if affected_users is not None:
        parts.append(f"{affected_users} users affected")

    if error_rate is not None:
        parts.append(f"error rate {error_rate:.1f}%")

    return "; ".join(parts)


def analyze_incident(incident):
    """Normalize a small incident record without performing external actions."""
    if not isinstance(incident, dict):
        raise TypeError("incident must be a dict")

    service = incident.get("service", "unknown")
    status = incident.get("service_status", "unknown")
    affected_users = incident.get("affected_users")
    error_rate = incident.get("error_rate")
    security_signal = bool(incident.get("security_signal", False))

    requires_human_review = (
        status == "unavailable"
        or security_signal
        or (
            isinstance(affected_users, int)
            and not isinstance(affected_users, bool)
            and affected_users >= 100
        )
    )

    return {
        "service": service,
        "status": status,
        "summary": _format_summary_legacy(
            service,
            status,
            affected_users,
            error_rate,
        ),
        "requires_human_review": requires_human_review,
    }
