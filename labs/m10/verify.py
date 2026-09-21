#!/usr/bin/env python3
"""Deterministic quality gate for the M10 capstone."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import inspect
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "incident_analyzer.py"
TESTS = ROOT / "test_incident.py"

EXPECTED_TEST_SHA256 = "56259a66967f71a552f6165cf7a6869ecdeca54a31c4587423f46e61d8ecadcc"

FORBIDDEN_CALLS = {"eval", "exec"}
FORBIDDEN_IMPORT_ROOTS = {
    "socket",
    "requests",
    "httpx",
    "urllib",
    "http",
    "ftplib",
    "telnetlib",
}


def fail(message: str) -> None:
    print(f"FAIL | {message}")
    raise SystemExit(1)


def check_test_integrity() -> None:
    actual = hashlib.sha256(TESTS.read_bytes()).hexdigest()
    if actual != EXPECTED_TEST_SHA256:
        fail("test_incident.py was modified")
    print("PASS | tests unchanged")


def check_source_policy() -> None:
    try:
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        fail(f"syntax error: {exc}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALLS:
                fail(f"forbidden call: {node.func.id}")

        if isinstance(node, ast.Import):
            roots = {alias.name.split(".")[0] for alias in node.names}
            bad = roots & FORBIDDEN_IMPORT_ROOTS
            if bad:
                fail(f"network-related import: {sorted(bad)}")

        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in FORBIDDEN_IMPORT_ROOTS:
                fail(f"network-related import: {root}")

    print("PASS | syntax and forbidden-call policy")


def check_public_api() -> None:
    sys.path.insert(0, str(ROOT))
    if "incident_analyzer" in sys.modules:
        del sys.modules["incident_analyzer"]
    module = importlib.import_module("incident_analyzer")
    signature = inspect.signature(module.analyze_incident)
    if list(signature.parameters) != ["incident"]:
        fail(f"public API changed: analyze_incident{signature}")
    print("PASS | public API preserved: analyze_incident(incident)")


def run_suite(name: str) -> bool:
    sys.path.insert(0, str(ROOT))
    loader = unittest.TestLoader()

    if name == "baseline":
        suite = loader.loadTestsFromName(
            "test_incident.TestIncidentRegression"
        )
    else:
        suite = unittest.TestSuite([
            loader.loadTestsFromName("test_incident.TestIncidentRegression"),
            loader.loadTestsFromName("test_incident.TestSeverityFeature"),
        ])

    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return result.wasSuccessful()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["baseline", "full"])
    args = parser.parse_args()

    print(f"=== M10 QUALITY GATE: {args.mode.upper()} ===")
    check_test_integrity()
    check_source_policy()
    check_public_api()

    if not run_suite(args.mode):
        raise SystemExit(1)

    if args.mode == "baseline":
        print("PASS | 10 regression tests")
    else:
        print("PASS | 10 regression + 6 feature tests")

    print("QUALITY_GATE=PASS")


if __name__ == "__main__":
    main()
