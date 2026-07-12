# Matriz de trazabilidad (PSP)

> Esta tabla es una **vista** compacta y orientada a evidencia de `docs/requisitos.md`, que es la
> **fuente única de verdad** del catálogo de requisitos. No es una fuente paralela: no agregues,
> elimines ni redactes requisitos aquí. Cuando cambie el estado de un requisito en
> `docs/requisitos.md`, actualiza la fila correspondiente en el mismo commit/PR.
>
> Columnas: `Requisito` (ID de `docs/requisitos.md`) · `Issue(s) #N` (issues de GitHub que lo trabajan)
> · `Commit(s)/PR` (hashes cortos o números de PR que lo implementan) · `Módulo` (dónde vive) ·
> `Evidencia` (test, métrica medida, revisión clínica) · `Estado` (igual que en `requisitos.md`).
>
> En este bootstrap no existen issues todavía: `Issue(s) #N` y `Commit(s)/PR` quedan vacíos (`—`).

## Requisitos funcionales (RF)

| Requisito | Issue(s) #N | Commit(s)/PR | Módulo | Evidencia | Estado |
|-----------|-------------|---------------|--------|-----------|--------|
| RF-001 — Ingesta DICOM de mamografía 2D | — | — | `services/mammography` | — | Propuesto |
| RF-002 — Clasificación mamografía 2D (CBIS-DDSM, transfer learning) | — | — | `services/mammography` | — | Propuesto |
| RF-003 — Explicabilidad Grad-CAM sobre mamografía | — | — | `services/mammography` | — | Propuesto |
| RF-004 — Orquestación multiagente vía gateway | — | — | `services/gateway` | Tests 12/12 del andamiaje mock | Implementado parcial |
| RF-005 — Servicio de fusión multimodal | — | — | `services/fusion` | Tests del andamiaje mock (promedio) | Implementado (mock) |
| RF-006 — Correlación histopatológica (BreakHis/TCGA-BRCA) | — | — | `services/histopathology` | — | Propuesto (trabajo futuro) |
| RF-007 — Endpoint interoperable HL7 FHIR / SNOMED CT | — | — | `services/gateway` | — | Propuesto |
| RF-008 — Reporte clínico estructurado (BI-RADS, riesgo, disclaimer) | — | — | `services/gateway` | — | Propuesto |

## Requisitos no funcionales (RNF)

| Requisito | Issue(s) #N | Commit(s)/PR | Módulo | Evidencia | Estado |
|-----------|-------------|---------------|--------|-----------|--------|
| RNF-001 — PHI fuera de logs/respuestas sin signed URL | — | — | transversal | — | Propuesto |
| RNF-002 — Métricas clínicas objetivo (sens/esp/AUC/recall/BI-RADS) | — | — | `services/mammography` | — | Propuesto |
| RNF-003 — Contratos JSON Schema → pydantic generado, fuente única | — | — | `packages/contracts` | CI verifica diff cero | Implementado |
| RNF-004 — Commits `tipo(#N): desc` validados por hook | — | — | `.githooks/commit-msg` | `bash .githooks/test-commit-msg.sh` | Implementado |
| RNF-005 — Equidad y mitigación de sesgo poblacional | — | — | `services/mammography`, `.claude/agents/mama-gobernanza-ia.md` | — | Propuesto |
| RNF-006 — Cumplimiento legal CO (Ley 1581, Res. 1995, Res. 2654, INVIMA) | — | — | transversal | — | Propuesto |
| RNF-007 — Alineación con 6 principios OMS de ética de IA en salud | — | — | transversal | — | Propuesto |
| RNF-008 — Disclaimer "no es dispositivo médico certificado" visible | — | — | `services/gateway` | — | Propuesto |
