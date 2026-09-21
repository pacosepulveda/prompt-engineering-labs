#!/usr/bin/env python3
import argparse
import math
from pathlib import Path

try:
    import tiktoken
except ImportError:
    raise SystemExit(
        "Missing dependency 'tiktoken'. Run: python -m pip install --user -r requirements.txt"
    )

PROFILES = {
    "FAST": {
        "input_per_m": 0.80,
        "cached_input_per_m": 0.08,
        "output_per_m": 3.20,
        "prefill_tps": 9000,
        "decode_tps": 110,
        "base_ttft_s": 0.12,
    },
    "DEEP": {
        "input_per_m": 4.00,
        "cached_input_per_m": 0.40,
        "output_per_m": 16.00,
        "prefill_tps": 3500,
        "decode_tps": 55,
        "base_ttft_s": 0.25,
    },
}

CONTEXT_WINDOW = 128_000
USER_TOKENS_PER_TURN = 90
ASSISTANT_TOKENS_PER_TURN = 220

def count_tokens(text):
    enc = tiktoken.get_encoding("o200k_base")
    return len(enc.encode(text))

def request_metrics(input_tokens, output_tokens, profile):
    p = PROFILES[profile]
    input_cost = input_tokens / 1_000_000 * p["input_per_m"]
    output_cost = output_tokens / 1_000_000 * p["output_per_m"]
    ttft = p["base_ttft_s"] + input_tokens / p["prefill_tps"]
    decode = output_tokens / p["decode_tps"]
    return input_cost + output_cost, ttft, decode, ttft + decode

def conversation_metrics(context_tokens, turns, output_tokens, profile, cached=False):
    p = PROFILES[profile]
    total_cost = 0.0
    last_input = 0
    total_input = 0

    for turn in range(1, turns + 1):
        history = (turn - 1) * (USER_TOKENS_PER_TURN + output_tokens)
        current_user = USER_TOKENS_PER_TURN
        last_input = context_tokens + history + current_user
        total_input += last_input

        if cached and turn > 1:
            cached_context_cost = (
                context_tokens / 1_000_000 * p["cached_input_per_m"]
            )
            dynamic_tokens = history + current_user
            dynamic_cost = dynamic_tokens / 1_000_000 * p["input_per_m"]
            input_cost = cached_context_cost + dynamic_cost
        else:
            input_cost = last_input / 1_000_000 * p["input_per_m"]

        output_cost = output_tokens / 1_000_000 * p["output_per_m"]
        total_cost += input_cost + output_cost

    ttft = p["base_ttft_s"] + last_input / p["prefill_tps"]
    decode = output_tokens / p["decode_tps"]

    return {
        "total_input_tokens": total_input,
        "last_turn_input_tokens": last_input,
        "total_cost": total_cost,
        "last_ttft_s": ttft,
        "last_decode_s": decode,
        "last_total_latency_s": ttft + decode,
    }

def fmt_money(v):
    return f"${v:.6f}"

def print_profile(name, tokens, output_tokens, turns):
    cost, ttft, decode, total = request_metrics(tokens + USER_TOKENS_PER_TURN, output_tokens, name)
    uncached = conversation_metrics(tokens, turns, output_tokens, name, cached=False)
    cached = conversation_metrics(tokens, turns, output_tokens, name, cached=True)

    print(f"\n[{name}]")
    print(f"single request estimated cost : {fmt_money(cost)}")
    print(f"single request estimated TTFT : {ttft:.3f} s")
    print(f"estimated decode time         : {decode:.3f} s")
    print(f"estimated total latency       : {total:.3f} s")
    print(f"{turns}-turn input tokens       : {uncached['total_input_tokens']:,}")
    print(f"{turns}-turn uncached cost       : {fmt_money(uncached['total_cost'])}")
    print(f"{turns}-turn cached-prefix cost  : {fmt_money(cached['total_cost'])}")
    if uncached["total_cost"] > 0:
        saving = 100 * (1 - cached["total_cost"] / uncached["total_cost"])
        print(f"estimated caching saving      : {saving:.1f}%")
    print(f"last-turn estimated TTFT      : {uncached['last_ttft_s']:.3f} s")

def main():
    parser = argparse.ArgumentParser(
        description="Reference context/cost/latency analyzer for M05."
    )
    parser.add_argument("file")
    parser.add_argument("--turns", type=int, default=1)
    parser.add_argument("--output-tokens", type=int, default=220)
    parser.add_argument("--profiles", action="store_true")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    tokens = count_tokens(text)
    words = len(text.split())
    chars = len(text)
    occupancy = tokens / CONTEXT_WINDOW * 100

    print("=== CONTEXT ===")
    print(f"file                  : {args.file}")
    print(f"characters            : {chars:,}")
    print(f"words                 : {words:,}")
    print(f"reference tokens      : {tokens:,}")
    print(f"128k window occupancy : {occupancy:.2f}%")
    print(f"turns simulated       : {args.turns}")
    print(f"output tokens / turn  : {args.output_tokens}")
    print()
    print("Reference tokenizer: o200k_base")
    print("Profiles are synthetic training profiles, not provider prices.")

    names = ["FAST", "DEEP"] if args.profiles else ["FAST"]
    for name in names:
        print_profile(name, tokens, args.output_tokens, args.turns)

if __name__ == "__main__":
    main()
