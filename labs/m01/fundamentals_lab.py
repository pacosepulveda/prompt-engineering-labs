#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import random

SAMPLES = [
    ("English", "Prompt engineering improves system reliability."),
    ("Spanish", "La ingeniería de prompts mejora la fiabilidad del sistema."),
    ("Code", 'result = analyze_incident({"status": "degraded"})'),
    ("Identifier", "identity-api/eu-central/TEL-9941"),
    ("Unicode", "Latency ↑ 42 ms 🚦 — revisión"),
]

CANDIDATES = {
    "stable": 2.5,
    "degraded": 2.1,
    "critical": 1.2,
    "resolved": 0.8,
    "unknown": 0.4,
}


def softmax(values: dict[str, float], temperature: float) -> dict[str, float]:
    if temperature <= 0:
        raise ValueError("temperature must be > 0")
    scaled = {k: v / temperature for k, v in values.items()}
    max_v = max(scaled.values())
    exps = {k: math.exp(v - max_v) for k, v in scaled.items()}
    total = sum(exps.values())
    return {k: v / total for k, v in exps.items()}


def apply_top_k(dist: dict[str, float], k: int | None) -> dict[str, float]:
    if k is None:
        return dist
    if k < 1:
        raise ValueError("top-k must be >= 1")
    ordered = sorted(dist.items(), key=lambda x: x[1], reverse=True)[:k]
    total = sum(p for _, p in ordered)
    return {token: p / total for token, p in ordered}


def apply_top_p(dist: dict[str, float], p: float | None) -> dict[str, float]:
    if p is None:
        return dist
    if not (0 < p <= 1):
        raise ValueError("top-p must be in (0, 1]")
    ordered = sorted(dist.items(), key=lambda x: x[1], reverse=True)
    kept = []
    cumulative = 0.0
    for token, prob in ordered:
        kept.append((token, prob))
        cumulative += prob
        if cumulative >= p:
            break
    total = sum(prob for _, prob in kept)
    return {token: prob / total for token, prob in kept}


def cmd_tokens() -> None:
    try:
        import tiktoken
    except ImportError:
        raise SystemExit(
            "Missing dependency 'tiktoken'. Run: "
            "python -m pip install --user -r requirements.txt"
        )

    enc = tiktoken.get_encoding("o200k_base")
    print("REFERENCE TOKENIZER: o200k_base")
    print("These counts may differ from the model/provider used in the course.")
    print()

    for label, text in SAMPLES:
        token_ids = enc.encode(text)
        pieces = [
            enc.decode_single_token_bytes(token_id).decode("utf-8", errors="replace")
            for token_id in token_ids
        ]
        print(f"=== {label} ===")
        print(f"TEXT: {text}")
        print(f"CHARACTERS: {len(text)}")
        print(f"TOKENS: {len(token_ids)}")
        print("PIECES:")
        for token_id, piece in zip(token_ids, pieces):
            print(f"  {token_id:>8}  {piece!r}")
        print()


def cmd_sampling(temperature: float, top_k: int | None, top_p: float | None, seed: int) -> None:
    dist = softmax(CANDIDATES, temperature)
    dist = apply_top_k(dist, top_k)
    dist = apply_top_p(dist, top_p)

    print('CONTEXT: "The incident is ..."')
    print("SIMULATION ONLY — these are not probabilities from a real LLM.")
    print(f"temperature={temperature}")
    print(f"top_k={top_k if top_k is not None else 'disabled'}")
    print(f"top_p={top_p if top_p is not None else 'disabled'}")
    print()
    print("DISTRIBUTION:")

    ordered = sorted(dist.items(), key=lambda x: x[1], reverse=True)
    for token, probability in ordered:
        bar = "█" * max(1, round(probability * 40))
        print(f"{token:<10} {probability:>7.2%} {bar}")

    rng = random.Random(seed)
    population = [token for token, _ in ordered]
    weights = [prob for _, prob in ordered]
    samples = rng.choices(population, weights=weights, k=8)
    print()
    print("8 SAMPLED NEXT TOKENS:")
    print(" | ".join(samples))


def cmd_context(variant: str) -> None:
    clean = """# CURRENT INCIDENT

SOURCE: Incident Manager
AUTHORITY: high
FRESHNESS: current

incident_id: INC-101
service: identity-api
status: degraded
affected_users: 37
symptom: HTTP 401 during session refresh after approximately 30 minutes idle
rca_status: investigating

# CURRENT TELEMETRY

SOURCE: Observability
AUTHORITY: high
FRESHNESS: current

cache_hit_ratio: 71%
baseline_cache_hit_ratio: 94%

The cache change is being investigated as a possible contributor.
No root cause has been confirmed.
"""

    noisy_extra = """
# HISTORICAL INCIDENT INC-044

SOURCE: Postmortem Archive
AUTHORITY: high
FRESHNESS: historical

A previous identity-api incident produced HTTP 401 responses.
The confirmed root cause for INC-044 was an expired signing key.

This root cause applies to INC-044 only.

# INFORMAL TEAM NOTE

SOURCE: Team chat
AUTHORITY: low
FRESHNESS: current

"These idle-session 401 incidents are usually stale cache metadata.
I'd just call that the root cause."
"""

    print(clean.rstrip())
    if variant == "noisy":
        print()
        print(noisy_extra.rstrip())


def cmd_evidence() -> None:
    print("""# TRAINING EVIDENCE

PRODUCT: Telvora EdgeSync 9.4
ERROR: TEL-9941
SOURCE: Telvora EdgeSync 9.4 Training Runbook / ERR-17

MEANING:
Session refresh metadata mismatch.

CONFIRMED_CAUSE:
Not confirmed.

ALLOWED_NEXT_STEP:
Capture refresh diagnostics and correlate them with the session metadata
returned by the affected node.

RESTRICTIONS:
Do not restart the service or change session policy solely from TEL-9941.
""")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tokens")

    sampling = sub.add_parser("sampling")
    sampling.add_argument("--temperature", type=float, default=1.0)
    sampling.add_argument("--top-k", type=int)
    sampling.add_argument("--top-p", type=float)
    sampling.add_argument("--seed", type=int, default=7)

    context = sub.add_parser("context")
    context.add_argument("--variant", choices=["clean", "noisy"], required=True)
    sub.add_parser("evidence")

    args = parser.parse_args()
    if args.command == "tokens":
        cmd_tokens()
    elif args.command == "sampling":
        cmd_sampling(args.temperature, args.top_k, args.top_p, args.seed)
    elif args.command == "context":
        cmd_context(args.variant)
    elif args.command == "evidence":
        cmd_evidence()


if __name__ == "__main__":
    main()
