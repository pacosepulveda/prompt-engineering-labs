#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KB = ROOT / "knowledge.md"

STOPWORDS = {
    "a","an","and","are","as","at","be","before","by","for","from","how","in",
    "is","it","of","on","or","should","the","to","what","when","with","we"
}

EVAL_SET = [
    (
        "What should we inspect when account-api latency rises and cache hit ratio falls below 80 percent?",
        {"DOC-RUNBOOK-014"},
    ),
    (
        "What is the current rollback rehearsal requirement for account-api production changes?",
        {"DOC-POLICY-021"},
    ),
    (
        "When may Support describe an account-api incident as an outage?",
        {"DOC-SUPPORT-006"},
    ),
    (
        "What was the confirmed root cause of historical incident INC-6310?",
        {"DOC-POSTMORTEM-031"},
    ),
]

@dataclass
class Chunk:
    doc_id: str
    authority: str
    date: str
    status: str
    text: str

def tokens(text: str) -> list[str]:
    items = re.findall(r"[a-zA-Z0-9_-]+", text.lower())
    return [x for x in items if len(x) > 1 and x not in STOPWORDS]

def parse_documents(text: str) -> list[dict]:
    parts = re.split(r"(?=^## DOC-)", text, flags=re.MULTILINE)
    docs = []
    for part in parts:
        if not part.startswith("## DOC-"):
            continue
        doc_id_m = re.search(r"^DOC_ID:\s*(.+?)\s*$", part, re.MULTILINE)
        auth_m = re.search(r"^AUTHORITY:\s*(.+?)\s*$", part, re.MULTILINE)
        date_m = re.search(r"^DATE:\s*(.+?)\s*$", part, re.MULTILINE)
        status_m = re.search(r"^STATUS:\s*(.+?)\s*$", part, re.MULTILINE)
        docs.append({
            "doc_id": doc_id_m.group(1).strip() if doc_id_m else "UNKNOWN",
            "authority": auth_m.group(1).strip() if auth_m else "unknown",
            "date": date_m.group(1).strip() if date_m else "unknown",
            "status": status_m.group(1).strip() if status_m else "unknown",
            "text": part.strip(),
        })
    return docs

def section_chunks(docs: list[dict]) -> list[Chunk]:
    chunks = []
    for d in docs:
        body_parts = re.split(r"(?=^### )", d["text"], flags=re.MULTILINE)
        header = body_parts[0].strip()
        sections = body_parts[1:] or [d["text"]]
        for sec in sections:
            sec = sec.strip()
            if sec:
                chunks.append(Chunk(
                    d["doc_id"], d["authority"], d["date"], d["status"],
                    f"{header}\n\n{sec}".strip()
                ))
    return chunks

def fixed_chunks(docs: list[dict], chunk_words: int) -> list[Chunk]:
    chunks = []
    for d in docs:
        words = d["text"].split()
        for i in range(0, len(words), chunk_words):
            piece = " ".join(words[i:i+chunk_words]).strip()
            if piece:
                chunks.append(Chunk(
                    d["doc_id"], d["authority"], d["date"], d["status"], piece
                ))
    return chunks

def bm25(query: str, chunks: list[Chunk]) -> list[tuple[float, Chunk]]:
    q = tokens(query)
    docs = [tokens(c.text) for c in chunks]
    n = len(docs)
    if not n:
        return []

    df = {}
    for d in docs:
        for term in set(d):
            df[term] = df.get(term, 0) + 1

    avgdl = sum(len(d) for d in docs) / n
    k1 = 1.5
    b = 0.75
    ranked = []

    for chunk, d in zip(chunks, docs):
        counts = {}
        for term in d:
            counts[term] = counts.get(term, 0) + 1
        score = 0.0
        for term in q:
            if term not in counts:
                continue
            freq = counts[term]
            idf = math.log(1 + (n - df.get(term, 0) + 0.5) / (df.get(term, 0) + 0.5))
            denom = freq + k1 * (1 - b + b * len(d) / max(avgdl, 1))
            score += idf * (freq * (k1 + 1)) / denom
        ranked.append((score, chunk))

    return sorted(ranked, key=lambda x: x[0], reverse=True)

def build_chunks(strategy: str, chunk_words: int) -> list[Chunk]:
    docs = parse_documents(KB.read_text(encoding="utf-8"))
    return section_chunks(docs) if strategy == "section" else fixed_chunks(docs, chunk_words)

def retrieve(query: str, top_k: int, strategy: str, chunk_words: int):
    return bm25(query, build_chunks(strategy, chunk_words))[:top_k]

def render(query: str, results) -> str:
    out = ["# Retrieved context", "", f"QUERY: {query}", ""]
    for idx, (score, c) in enumerate(results, 1):
        out += [
            f"## Rank {idx}", "",
            f"SCORE: {score:.3f}",
            f"DOC_ID: {c.doc_id}",
            f"AUTHORITY: {c.authority}",
            f"DATE: {c.date}",
            f"STATUS: {c.status}", "",
            c.text, "", "---", "",
        ]
    return "\n".join(out)

def evaluate(top_k: int, strategy: str, chunk_words: int):
    hits = 0
    print(f"strategy={strategy} top_k={top_k} chunk_words={chunk_words}")
    print()
    for query, expected in EVAL_SET:
        results = retrieve(query, top_k, strategy, chunk_words)
        returned = {c.doc_id for _, c in results}
        ok = bool(returned & expected)
        hits += int(ok)
        print(("PASS" if ok else "MISS") + f" | {query}")
        print("  expected:", ", ".join(sorted(expected)))
        print("  returned:", ", ".join(c.doc_id for _, c in results))
    recall = hits / len(EVAL_SET)
    print()
    print(f"Recall@{top_k}: {recall:.2f} ({hits}/{len(EVAL_SET)})")

def main():
    parser = argparse.ArgumentParser(description="Small observable RAG retriever for M07.")
    parser.add_argument("--query")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--strategy", choices=["section", "fixed"], default="section")
    parser.add_argument("--chunk-words", type=int, default=80)
    parser.add_argument("--out")
    parser.add_argument("--eval", action="store_true")
    args = parser.parse_args()

    if args.eval:
        evaluate(args.top_k, args.strategy, args.chunk_words)
        return

    if not args.query:
        parser.error("--query is required unless --eval is used")

    results = retrieve(args.query, args.top_k, args.strategy, args.chunk_words)
    text = render(args.query, results)

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()
