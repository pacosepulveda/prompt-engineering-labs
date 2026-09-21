# Few-shot examples — Representative design

## Example A — READY
Input: tests PASS; no Sev1/Sev2; rollback rehearsal PASS 7 days ago; monitoring ready; no security scope.  
Output: `RECOMMENDATION: READY`

## Example B — BLOCKED
Input: one release-blocking test FAILED; no Sev1/Sev2; rollback PASS; monitoring ready; no security scope.  
Output: `RECOMMENDATION: BLOCKED`

## Example C — NEEDS_EVIDENCE
Input: tests PASS; no Sev1/Sev2; rollback PASS; monitoring ready; authentication change; security review result unavailable.  
Output: `RECOMMENDATION: NEEDS_EVIDENCE`

## Example D — Boundary
Input: tests PASS; no Sev1/Sev2; rollback plan exists; last successful rehearsal 31 days ago; monitoring ready; no security scope.  
Output: `RECOMMENDATION: BLOCKED`
