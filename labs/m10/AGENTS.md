# M10 — Repository Instructions

These instructions apply to the files in this directory.

## Public API

Preserve:

```python
analyze_incident(incident)
```

Do not rename it or change its parameters.

Existing output fields and their values remain part of the regression contract.

## Scope

For CR-FEAT-010:

- modify `incident_analyzer.py`;
- do not modify `test_incident.py`;
- do not weaken `verify.py`;
- make the smallest change that satisfies the specification.

## Constraints

- Python standard library only.
- No network access from application code.
- No `eval`.
- No `exec`.
- No shell execution from application code.
- Do not add dependencies.
- Do not remove existing behavior merely to make a new test pass.

## Verification

Before claiming completion:

```bash
python labs/m10/verify.py baseline
python labs/m10/verify.py full
```

Then inspect:

```bash
git diff -- labs/m10
```

## Completion

"Done" requires observed evidence:

- quality gate passes;
- regression tests pass;
- feature tests pass;
- diff remains within scope.

Do not treat the model's own statement that the task is complete as verification.
