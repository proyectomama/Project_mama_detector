# Metodología PSP en mama-detector

Este documento adapta el **Personal Software Process (PSP)** de Watts Humphrey (SEI) al flujo de
trabajo de `mama-detector`, usando **GitHub Issues** como sistema de tracking (no Jira — ver
[`../adr/0003-tracking-github-issues.md`](../adr/0003-tracking-github-issues.md)). Es la
disciplina de proceso que el profesor exige, combinada con PMBOK a nivel de planificación general
del TG.

## Rol del auditor

El auditor de este proyecto actúa con la disciplina de un **auditor PSP/SEI**: en un sistema de
apoyo a la detección temprana de cáncer de mama, la **calidad y la trazabilidad pesan más que la
velocidad**. Un defecto no detectado no es solo deuda técnica — puede propagarse a una alerta
clínica incorrecta. El auditor (rol que ejerce `.claude/agents/mama-auditor.md`, disparable con
`/mama-audit`) no aprueba trabajo sin evidencia: cada afirmación de "cumple" se respalda con un
archivo, un test que corrió, o una entrada en la matriz de trazabilidad.

## Fase PSP ↔ artefacto real

PSP define fases disciplinadas de planeación, diseño, revisión, codificación, prueba y
post-mortem. En `mama-detector` cada fase tiene un artefacto real y verificable — no es un proceso
en el papel:

| Fase PSP | Artefacto real en el repo |
|----------|---------------------------|
| Planning | `docs/superpowers/plans/*` — plan de implementación por tarea/feature |
| Design | `docs/superpowers/specs/*` + `docs/adr/*` — spec técnica y decisiones de arquitectura |
| Design Review | `/mama-audit` — revisión del diseño contra requisitos, PHI y marco legal antes de codificar |
| Coding | `services/*` — implementación en cada servicio (gateway, mammography, histopathology, genomics, fusion) |
| Code Review | Pull Request + `/mama-audit` (y, según el módulo, `/mama-radiologo`, `/mama-patologo`, `/mama-gobernanza-ia`) |
| Testing | `uv run pytest` por servicio (ver [`../runbook.md`](../runbook.md)) |
| Post-mortem | `docs/psp/postmortems/` — una entrada por hito/sprint, usando [`post-mortem-template.md`](post-mortem-template.md) |

## Reglas

1. **Todo es trazable.** Cada cambio de código enlaza issue ↔ requisito (`RF-NNN`/`RNF-NNN`) ↔
   commit ↔ evidencia. La vista compacta vive en
   [`traceability.md`](traceability.md); la fuente única de los requisitos es
   [`../requisitos.md`](../requisitos.md).
2. **Todo se mide.** Tests que pasan (`uv run pytest`), diff cero de contratos generados cuando
   aplica (ver [`../architecture/contracts.md`](../architecture/contracts.md)), y — cuando el
   modelo real reemplace al mock — las métricas clínicas objetivo (sensibilidad >95%,
   especificidad >90%, AUC-ROC >0.97, recall >94%, precisión BI-RADS >93%; ver
   [`../requisitos.md`](../requisitos.md) RNF-002).
3. **Revisión antes de merge.** Ningún PR se integra a `main` sin pasar por la
   [Definition of Done](definition-of-done.md): checklist de PHI/seguridad clínica, tests, y —
   cuando el cambio toca salida clínica — el experto correspondiente
   (`/mama-radiologo`, `/mama-patologo`, `/mama-gobernanza-ia`).
4. **Todo defecto se registra.** Cualquier defecto encontrado en diseño, código o pruebas se
   asienta en [`defect-log.md`](defect-log.md) con su fase de inyección y de detección, **sin
   PHI** en la descripción (ver [`../architecture/phi-and-security.md`](../architecture/phi-and-security.md)).

## Ver también

- [`conventions.md`](conventions.md) — convención de commits, ramas y flujo issue→PR→merge.
- [`definition-of-ready.md`](definition-of-ready.md) / [`definition-of-done.md`](definition-of-done.md)
- [`../requisitos.md`](../requisitos.md) y [`traceability.md`](traceability.md)
