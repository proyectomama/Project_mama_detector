# Alcance vigente del Trabajo de Grado

**Fecha:** 2026-07-12
**Estado:** referencia interna vigente del alcance acordado.
**Trazabilidad:** B-008 (alcance vigente / reconciliación con el anteproyecto).

> Este documento es la **referencia interna actual** de alcance del TG. No edita ni reescribe los
> documentos históricos del profesor (`docs/anteproyecto/*`): los complementa y reconcilia con el
> alcance recortado ya acordado. Cuando exista el issue de GitHub que trabaja B-008, su número se
> registra en [`requisitos.md`](requisitos.md) y [`psp/traceability.md`](psp/traceability.md).

## 1. Tarea clínica primaria

**Triaje de hallazgo/malignidad en mamografía 2D.** El sistema apoya —no reemplaza— la decisión
del profesional. **No** es predicción de riesgo a cinco años (es un problema clínico y una métrica
distintos, y queda fuera de este alcance). No es un dispositivo médico certificado.

## 2. Rebanada vertical (se implementa y valida)

- Modelo de **mamografía 2D** con transfer learning sobre el dataset público **CBIS-DDSM**.
- **Grad-CAM** asociado a cada predicción (explicabilidad).
- Orquestación **multiagente con LangGraph** de los cuatro agentes de plataforma en runtime
  (Radiólogo, Patólogo, Gobernanza IA, Auditor regulatorio). Es un componente **central** del TG y
  no se sustituye por los subagentes de `.claude/agents/` (que son tooling de desarrollo).
- Interoperabilidad **demostrable**: entrada **DICOM** validada; salida **FHIR** (`DiagnosticReport`
  con `Observation` codificada en **SNOMED CT**). No requiere conexión a un hospital real.
- **Evaluación** reproducible con protocolo congelado antes de medir.

## 3. Trabajo futuro (se diseña o documenta, no se implementa)

- Foundation models propios, LLM médico propio e IA generativa.
- Aprendizaje federado real entre instituciones.
- Modelos reales de **histopatología** y **genómica** (hoy son stubs mock).
- **Kubernetes, DGX, Spark, Edge AI** y entrenamiento distribuido.

## 4. Meta operativa aprobada

- **AUC-ROC ≥ 0.92** sobre CBIS-DDSM, con protocolo de evaluación congelado antes de medir. Se
  miden y reportan sensibilidad, especificidad y recall como métricas complementarias; no se
  afirma concordancia BI-RADS si el protocolo/dataset no la habilita.
- La meta inicial/histórica del profesor (sens. >95 %, esp. >90 %, **AUC-ROC >0.97**, recall >94 %,
  precisión BI-RADS >93 %) se conserva como **antecedente y referencia de aspiración**, fuera del
  alcance de validación del TG.

### Evidencia de aprobación — pendiente

Según confirmación del equipo, el director **ya aprobó** el alcance reducido y la meta
AUC-ROC ≥ 0.92. **Falta registrar la evidencia formal** de esa aprobación (correo, acta o minuta de
recapitulación, sin reproducir datos personales). Hasta registrarla, la meta vive como **requisito**
(RNF-002, estado `Propuesto`) pero su aprobación no está aún soportada por evidencia verificable.

## 5. Estadificación TNM — función desacoplada (no altera este alcance)

Tras la solicitud del director del 2026-07-15 de *identificar y validar el TNM*, se decidió adoptar
**AJCC 8** e implementar un motor de estadificación (ADR-0006; RF-009 → #6, RF-010 → #7).

> **Mismo estado de evidencia que §4 — no confundir.** ADR-0006 está **aceptada por el equipo el
> 2026-07-15, no por el director**: él **aún no ha respondido** el hilo del 2026-07-15. Igual que la
> meta de §4, este alcance espera evidencia registrada. Y es la **misma** evidencia: responder ese
> hilo cierra ambas.

**Este frente no modifica el alcance de arriba**, y conviene ser explícito sobre por qué:

- **No cambia la tarea clínica primaria** (§1): la plataforma sigue haciendo **triaje de sospecha**
  en mamografía. El motor de estadificación se dispara sobre un cáncer **ya confirmado por biopsia**,
  no sobre la salida del modelo. Estadificar porque el modelo dijo `malignant` sería exactamente el
  error a evitar.
- **No cambia la meta operativa** (§4): AUC-ROC ≥0.92 mide el **triaje** sobre CBIS-DDSM. El motor de
  estadificación es **determinista, sin ML**, y por tanto **no tiene AUC**: se verifica por
  **cobertura exhaustiva de la tabla de verdad**, no por métrica estadística. Son dos formas de
  evidencia distintas y no se mezclan.
- **No se valida TNM contra CBIS-DDSM**: el dataset **no tiene etiquetas TNM**, ni ganglionares, ni
  de metástasis, ni biomarcadores. Afirmar "validamos el TNM" con CBIS-DDSM sería del mismo tipo de
  defecto que afirmar una métrica no medida.
- **La rebanada vertical (§2) no crece por esto.** El motor es una función **desacoplada** del
  pipeline de mamografía: recibe datos clínicos estructurados y calcula.

**La única excepción:** la **estimación de `cT`** (RF-010) **sí toca el pipeline de mamografía**
—requiere segmentación de la lesión y `PixelSpacing` del DICOM— y sale marcada como **estimación
radiológica** con prefijo `c`, nunca `pT`. `cN` y `cM` **no son inferibles** desde una mamografía, y
sin `N` ni `M` no hay estadio.

**Sobre el perfil regulatorio:** emitir un estadio es una afirmación clínica de **mayor riesgo que un
triaje** y sube el perfil SaMD ante INVIMA (ver notas en RNF-006/RNF-007 de
[`requisitos.md`](requisitos.md)). Detalle clínico en [`clinical/tnm.md`](clinical/tnm.md).

## 6. Documentos relacionados

- [`roadmap-tg.md`](roadmap-tg.md) — roadmap de corrección y entrega por fases.
- [`auditoria-alineacion-profesor.md`](auditoria-alineacion-profesor.md) — brechas frente al alcance
  aprobado (incluye B-008).
- [`requisitos.md`](requisitos.md) — catálogo RF/RNF (RNF-002 registra la meta AUC-ROC ≥ 0.92).
- [`anteproyecto/propuesta-alcance-tg.md`](anteproyecto/propuesta-alcance-tg.md) — propuesta de
  alcance (documento histórico, no se reescribe aquí).
- [`adr/0006-estadificacion-tnm-ajcc8-pronostica.md`](adr/0006-estadificacion-tnm-ajcc8-pronostica.md)
  — decisión de estadificación TNM (AJCC 8, tabla pronóstica). Ver §5.
- [`clinical/tnm.md`](clinical/tnm.md) — fuente clínica única de TNM: qué es inferible desde imagen
  y qué no.
