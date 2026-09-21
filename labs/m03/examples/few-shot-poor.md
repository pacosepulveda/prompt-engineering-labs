# Few-shot examples — Poor design

Ejemplos deliberadamente mal diseñados.

## Example 1
Input: all release tests passed; no Sev1/Sev2; rollback rehearsal passed yesterday; monitoring ready; no security-sensitive scope.  
Output: `RECOMMENDATION: READY`

## Example 2
Input: all tests passed; rollback rehearsed last week; no major known issues; monitoring ready.  
Output: `RECOMMENDATION: READY`

## Example 3
Input: tests are green; no major issues; rollback tested; monitoring ready.  
Output: `RECOMMENDATION: READY`

Problemas deliberados:

- una única clase domina;
- no hay missing-data cases;
- no hay BLOCKED;
- no hay frontera;
- gates inconsistentes.
