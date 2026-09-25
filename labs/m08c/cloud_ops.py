#!/usr/bin/env python3
"""Read-only cloud evidence tool for M08C."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CASE_ID = "COST-2026-09"
SNAPSHOT_DATE = "2026-09-25"

def rows(name: str):
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def money(v):
    return round(float(v), 2)

def emit(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def ensure_case(case_id):
    if case_id != CASE_ID:
        raise SystemExit(f"Unknown case: {case_id}")

def cmd_summary(args):
    ensure_case(args.case)
    data = rows("costs.csv")
    prev = sum(money(r["previous_week_eur"]) for r in data)
    curr = sum(money(r["current_week_eur"]) for r in data)
    services = {}
    for r in data:
        s = services.setdefault(r["service"], {"previous": 0.0, "current": 0.0})
        s["previous"] += money(r["previous_week_eur"])
        s["current"] += money(r["current_week_eur"])
    by_service = []
    for service, vals in services.items():
        p, c = round(vals["previous"], 2), round(vals["current"], 2)
        by_service.append({
            "service": service,
            "previous_week_eur": p,
            "current_week_eur": c,
            "delta_eur": round(c - p, 2),
        })
    by_service.sort(key=lambda x: x["delta_eur"], reverse=True)
    emit({
        "case_id": CASE_ID,
        "snapshot_date": SNAPSHOT_DATE,
        "previous_week_run_rate_eur": round(prev, 2),
        "current_week_run_rate_eur": round(curr, 2),
        "delta_eur": round(curr - prev, 2),
        "delta_pct": round(((curr - prev) / prev) * 100, 1),
        "by_service": by_service,
    })

def cmd_resource_costs(args):
    out = []
    for r in rows("costs.csv"):
        if args.service and r["service"] != args.service:
            continue
        p, c = money(r["previous_week_eur"]), money(r["current_week_eur"])
        out.append({
            "service": r["service"],
            "resource_id": r["resource_id"],
            "previous_week_eur": p,
            "current_week_eur": c,
            "delta_eur": round(c - p, 2),
        })
    out.sort(key=lambda x: x["delta_eur"], reverse=True)
    emit(out)

def find_one(name, key, value):
    for r in rows(name):
        if r[key] == value:
            return r
    raise SystemExit(f"No record for {value}")

def cmd_resource(args):
    emit(find_one("resources.csv", "resource_id", args.id))

def cmd_changes(args):
    data = rows("changes.csv")
    if args.resource:
        data = [r for r in data if r["resource_id"] == args.resource]
    emit(data)

def cmd_metrics(args):
    r = find_one("metrics.csv", "resource_id", args.resource)
    out = dict(r)
    out["observation_days"] = int(out["observation_days"])
    out["avg_cpu_pct"] = float(out["avg_cpu_pct"])
    out["p95_cpu_pct"] = float(out["p95_cpu_pct"])
    emit(out)

def cmd_pricing(args):
    r = find_one("pricing.csv", "instance_type", args.instance_type)
    emit({
        "instance_type": r["instance_type"],
        "weekly_run_rate_eur": money(r["weekly_run_rate_eur"]),
    })

def build_parser():
    p = argparse.ArgumentParser(description="Read-only evidence interface for M08C FinOps investigation")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("cost-summary", help="Show case-level and service-level cost deltas")
    s.add_argument("--case", required=True)
    s.set_defaults(func=cmd_summary)
    s = sub.add_parser("resource-costs", help="Rank resource-level cost deltas")
    s.add_argument("--service")
    s.set_defaults(func=cmd_resource_costs)
    s = sub.add_parser("resource", help="Show resource metadata and tags")
    s.add_argument("--id", required=True)
    s.set_defaults(func=cmd_resource)
    s = sub.add_parser("changes", help="Show recent changes, optionally for one resource")
    s.add_argument("--resource")
    s.set_defaults(func=cmd_changes)
    s = sub.add_parser("metrics", help="Show utilization evidence for a compute resource")
    s.add_argument("--resource", required=True)
    s.set_defaults(func=cmd_metrics)
    s = sub.add_parser("pricing", help="Show normalized weekly training price for an instance type")
    s.add_argument("--instance-type", required=True)
    s.set_defaults(func=cmd_pricing)
    return p

def main():
    args = build_parser().parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
