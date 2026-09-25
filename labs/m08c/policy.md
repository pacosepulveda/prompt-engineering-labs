# M08C — FinOps Investigation Policy

## Evidence discipline

Every important conclusion must be classified as one of:

- **CONFIRMED** — directly supported by tool output or an explicit policy rule;
- **SUPPORTED HYPOTHESIS** — strongly suggested by evidence but not fully proven;
- **UNKNOWN** — evidence is insufficient.

Never convert missing evidence into a confirmed fact.

## Temporary resources

A non-production resource with an `expires_on` date earlier than the case snapshot date and state `running` is a confirmed lifecycle-policy violation.

The investigator may recommend stopping it, but may not stop or modify the resource.

## Ownership

Every resource must have a non-empty `owner` tag.

A missing owner tag is a governance finding. Do not infer an authoritative owner from a change actor or free-text note.

## Rightsizing

A compute resource is a supported rightsizing candidate when both conditions hold over the supplied observation period:

```text
avg_cpu_pct < 15
p95_cpu_pct < 30
```

The investigator may estimate savings using the training pricing data, but may not resize the resource.

## Active performance investigations

Do not recommend reverting a compute resize solely for cost reasons when all of the following are true:

- the change log says the resource is still under an active observation window;
- `p95_cpu_pct >= 60`;
- no policy violation is present.

Flag it for owner review instead.

## Human gate

The agent may investigate, quantify, prioritize and recommend.

The agent may not:

- stop resources;
- resize resources;
- change tags;
- approve financial actions;
- claim that a recommendation has been implemented.

## Final report

The report must contain:

1. Executive summary
2. Cost delta and primary drivers
3. Confirmed findings
4. Supported hypotheses / unknowns
5. Quantified savings opportunities
6. Governance findings
7. Recommended next actions
8. Evidence trace
9. Human decisions required
