# Definition of Ready (DoR)

Un issue de GitHub está **"Ready"** — se puede empezar a trabajar — cuando cumple **todo** lo
siguiente. Adaptado a `mama-detector` sobre GitHub Issues: se usan **labels** de GitHub para
clasificar el issue (no "Components" de Jira, que no existe en este tracker).

- [ ] **Resumen (título) verifica un cambio concreto.** El título del issue describe un resultado
  observable ("Agrega validación de DICOM en el endpoint de mamografía"), no una vaguedad
  ("Mejorar mamografía").
- [ ] **Descripción con estructura completa** (según el tipo de issue — ver
  `.github/ISSUE_TEMPLATE/`):
  - `## Contexto` — por qué se necesita el cambio.
  - `## Objetivo` — qué se logra al cerrarlo.
  - `## Criterios de aceptación` — al menos **uno**, verificable (checklist, no prosa).
  - `## Trazabilidad` — módulo afectado (`services/<nombre>`, `packages/contracts`, etc.) y el
    `RF-NNN`/`RNF-NNN` de [`../requisitos.md`](../requisitos.md) que el issue mueve de estado.
- [ ] **Label del catálogo.** El issue tiene asignado al menos un label de tipo
  (`tarea` | `historia` | `defecto`) y, cuando aplica, un label de módulo/área
  (p. ej. `gateway`, `mammography`, `phi`, `psp`). Los labels de GitHub cumplen aquí el rol que en
  Jira cumplirían los "Components": clasifican dónde vive el trabajo sin necesitar un campo
  estructurado adicional.
- [ ] **Asignado.** El issue tiene un responsable (`assignee`) antes de empezar el trabajo; un
  issue sin asignar no está listo para codificarse, aunque esté bien descrito.

## Qué NO es Ready

- Un issue que dice "investigar X" sin criterio de cierre verificable — eso es spike/investigación,
  no una tarea lista para PR.
- Un issue sin `## Trazabilidad`: si no se puede decir qué requisito o módulo toca, no está listo.
- Un issue sobre salida clínica sin mención de si dispara el disclaimer o afecta PHI — eso debe
  quedar explícito en `## Contexto` antes de codificar.

## Ver también

- [`definition-of-done.md`](definition-of-done.md) — cuándo se considera cerrado el trabajo.
- [`../../.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/) — plantillas que ya incluyen
  estas secciones.
