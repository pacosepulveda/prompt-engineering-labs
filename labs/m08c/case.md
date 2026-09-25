# M08C — FinOps Investigation Case

CASE_ID: COST-2026-09
SNAPSHOT_DATE: 2026-09-25

The FinOps team detected an unexpected increase in the weekly cloud run-rate.

Your objective is to determine:

- what changed;
- which services and resources explain the increase;
- which findings are confirmed evidence and which are hypotheses;
- what savings opportunities are supported by evidence;
- which governance gaps require human follow-up.

The investigation must use the read-only training tool:

```bash
python labs/m08c/cloud_ops.py ...
```

Use `--help` to discover its commands.

Do not ask the user to execute investigation commands for you.
Do not modify simulated cloud resources.

Write the final evidence-based report to:

```text
labs/m08c/work/COST-2026-09-report.md
```
