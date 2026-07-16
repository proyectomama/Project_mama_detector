# mama-detector — Contexto para Claude Code

Plataforma académica multimodal de apoyo a la detección temprana de cáncer de mama
(mamografía + histopatología + genómica). No es un dispositivo médico certificado.

## Convenciones de commit
Mensajes en español: `tipo: descripción breve` (`feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `test`).

## Autoría — sin atribución a IA (regla firme)
Todo el trabajo es obra del equipo. **En ningún artefacto** (commits, PRs, issues, código,
comentarios, documentación) debe decir que lo hizo Claude, una IA, un "asistente" o un "agente":
sin trailer `Co-Authored-By: Claude`, sin `🤖 Generated with`, sin menciones de IA. Antes de
`git push`, verificar que ningún commit arrastró atribución. Detalle en
[`docs/psp/conventions.md`](docs/psp/conventions.md#autoría--sin-atribución-a-ia-regla-firme).

## Datos sensibles (PHI)
Nunca loguear identificadores de paciente/caso, rutas/nombres de archivos (DICOM/WSI),
resultados de predicción ni URLs de Storage. Nunca exponer URLs de Storage al cliente
sin signed URL generada server-side.

## Contratos
`packages/contracts/schemas/*.json` es la fuente de verdad. El código pydantic/TS es
generado con `just gen-contracts` — nunca se edita a mano.

## Arquitectura
Solo el `gateway` se expone al exterior. Los servicios de modalidad y fusión son internos.
Visión completa (diseño vs. implementado): [`docs/architecture/overview.md`](docs/architecture/overview.md).

## Mapa de docs

| Ruta | Contenido |
|------|-----------|
| `docs/requisitos.md` | Catálogo RF/RNF (fuente única de trazabilidad) |
| `docs/clinical/` | `tnm.md` — estadificación TNM (AJCC 8), qué es inferible desde imagen y qué no, contexto CO (GPC Minsalud, consenso CAC 2025) |
| `docs/handoff-tnm-ajcc8.md` | Handoff del frente TNM: hallazgos, trampas ya corregidas (`cNX`, `cMX`, redondeo `T1mi`), decisión ADR-0006 y trabajo pendiente |
| `docs/architecture/` | `overview.md` (diseño completo vs. rebanada implementada), `contracts.md`, `phi-and-security.md` |
| `docs/adr/` | Decisiones de arquitectura (ADR-0001 a 0006) |
| `docs/psp/` | Metodología PSP, convenciones, DoR/DoD, `traceability.md`, `defect-log.md`, plantilla de post-mortem |
| `docs/runbook.md` | Cómo correr el sistema en local (`uv`, `just up`, `just test`) |
| `docs/deployment/railway.md` | Borrador de despliegue en Railway |
| `docs/anteproyecto/` | Materiales fuente del Trabajo de Grado (anteproyecto, requisitos del profesor, alcance) |

## Gobernanza

- **Tracking:** GitHub Issues (no Jira). Cada issue declara a qué `RF-NNN`/`RNF-NNN` de
  `docs/requisitos.md` corresponde.
- **Definition of Ready / Done:** ver `docs/psp/definition-of-ready.md` y
  `docs/psp/definition-of-done.md` antes de empezar o cerrar trabajo.
- **Hook `commit-msg`:** valida `tipo(#N): descripción` / `tipo: descripción`
  (`.githooks/commit-msg`); se activa con `git config core.hooksPath .githooks`.
- **Plantillas de GitHub:** `.github/ISSUE_TEMPLATE/*` (tarea/historia/defecto) y
  `.github/pull_request_template.md` (checklist de DoD: tests, contratos sin diff, sin PHI,
  disclaimer clínico, trazabilidad, `Cierra #N`).
- Flujo completo en [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Subagentes de revisión (tooling de desarrollo)

> **Importante:** estos son *subagentes de Claude Code* para usar **mientras se programa** — revisan
> el código, los PRs y la documentación del repositorio. **NO son componentes de la plataforma
> desplegada** ni el "sistema multiagente" que exige el profesor. Ese sistema (Agentes Radiólogo,
> Patólogo, Gobernanza IA, Auditor) corre **en runtime, en la nube, con LangGraph**, analiza casos
> clínicos reales, y es **trabajo futuro** (RF-004, ver `docs/adr/0005-orquestacion-multiagente-langgraph.md`).
> Estos subagentes solo **comparten el nombre** de esos roles clínicos; son dos cosas distintas.

Cuatro subagentes read-only (`.claude/agents/`) disparables con slash commands sobre un
archivo/PR/módulo (`$ARGUMENTS`, o el diff actual si se omite):

| Comando | Revisa (durante el desarrollo) |
|---------|--------------------------------|
| `/mama-radiologo` | Plausibilidad clínica de mamografía/tomosíntesis, BI-RADS, densidad, umbrales de riesgo, calidad de Grad-CAM/XAI |
| `/mama-patologo` | Coherencia de resultados de histopatología, correlación radio-patológica, subtipos/grados |
| `/mama-gobernanza-ia` | Métricas clínicas objetivo, sesgo poblacional/equidad, calidad de la explicabilidad, fusión multimodal |
| `/mama-audit` | Trazabilidad issue↔requisito↔commit, PHI, marco legal CO, 6 principios OMS, cumplimiento de DoD |

Ninguno modifica código: son revisiones. El auditor (`/mama-audit`) además puede correr
verificaciones read-only (tests/estado) sin modificar nada.

## Alcance

Arquitectura completa **diseñada** (3 modalidades + fusión + 4 agentes + interoperabilidad
FHIR/DICOM/SNOMED + federado). Del Trabajo de Grado se **implementa y valida** solo una
**rebanada vertical**: mamografía 2D sobre CBIS-DDSM + Grad-CAM + orquestación multiagente con
LangGraph + endpoint DICOM/FHIR/SNOMED + métricas clínicas. Todo lo demás (foundation models
propios, aprendizaje federado, histopatología/genómica reales, Kubernetes/DGX, Spark, Edge AI)
es **trabajo futuro** documentado, no implementado. Ver el detalle y el mapeo diseño↔hoy↔futuro
en [`docs/architecture/overview.md`](docs/architecture/overview.md) y el catálogo de estados por
requisito en [`docs/requisitos.md`](docs/requisitos.md).
