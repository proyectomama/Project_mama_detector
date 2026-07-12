# Definition of Done (DoD)

Un cambio está **"Done"** — se puede mergear a `main` — cuando cumple **todo** lo siguiente:

- [ ] **Código y tests pasan.** `uv run pytest` en cada servicio tocado (y en
  `packages/contracts` si se modificaron contratos) — ver [`../runbook.md`](../runbook.md) para el
  comando exacto por servicio.
- [ ] **Contratos regenerados sin diff (si aplica).** Si el cambio toca
  `packages/contracts/schemas/*.json`, se corrió `packages/contracts/generate.sh` y el diff de
  `python/mama_contracts/models.py` resultante es exactamente el que se está commiteando — nunca
  se edita `models.py` a mano (ver [`../architecture/contracts.md`](../architecture/contracts.md)).
- [ ] **PR revisado con checklist PHI/seguridad clínica.** Al menos una revisión humana, y si el
  cambio afecta salida clínica o el manejo de datos sensibles, revisión del experto correspondiente
  (`/mama-radiologo`, `/mama-patologo`, `/mama-gobernanza-ia` o `/mama-audit`). El checklist del PR
  (`.github/pull_request_template.md`) está completo.
- [ ] **Trazabilidad actualizada.** Si el cambio mueve el estado de un requisito, se actualiza en
  el mismo PR tanto [`../requisitos.md`](../requisitos.md) (fuente única) como
  [`traceability.md`](traceability.md) (vista), con el número de issue/PR y evidencia.
- [ ] **Sin PHI en logs.** Ningún `case_ref`, ruta de archivo DICOM/WSI, `result_json` ni URL de
  Storage sin signed URL aparece en logs, mensajes de commit, nombres de rama, ni en el propio PR
  (ver [`../architecture/phi-and-security.md`](../architecture/phi-and-security.md)).
- [ ] **Disclaimer presente (si es salida clínica).** Toda respuesta que exponga score, riesgo,
  BI-RADS o alerta clínica incluye el disclaimer "No es un dispositivo médico certificado"
  (RNF-008).
- [ ] **Commit(s) siguen la convención.** Todo commit del PR respeta `tipo(#N): descripción` (ver
  [`conventions.md`](conventions.md)); el hook `commit-msg` los habría aceptado.

## Nota

La DoD aplica igual sin importar el tamaño del cambio: un fix de una línea en un mensaje de log
que filtra PHI está sujeto al mismo checklist que una feature nueva. La disciplina PSP mide todo
el trabajo, no solo el "grande".

## Ver también

- [`definition-of-ready.md`](definition-of-ready.md) — cuándo un issue puede empezar a trabajarse.
- [`../../.github/pull_request_template.md`](../../.github/pull_request_template.md) — checklist
  operativo en el propio PR.
