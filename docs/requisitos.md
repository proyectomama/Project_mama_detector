# Catálogo de requisitos (RF/RNF)

Catálogo de requisitos funcionales y no funcionales de mama-detector, redactado siguiendo el
espíritu de **ISO/IEC/IEEE 29148** (especificación de requisitos de ingeniería de sistemas y
software). Es la **fuente única de verdad** para trazabilidad del proyecto: todo issue de GitHub,
commit, PR y evidencia de prueba debe poder rastrearse hasta un requisito de este catálogo.

## Convención

- **ID:** `RF-NNN` (funcional) / `RNF-NNN` (no funcional), numeración correlativa de 3 dígitos, sin reciclar IDs eliminados.
- **Estado:** uno de
  - `Propuesto` — requisito identificado y redactado, aún sin issue de trabajo abierto.
  - `Aprobado` — con issue de GitHub abierto y priorizado, pendiente de implementación.
  - `Implementado` — código mergeado a `main` que lo satisface (total o parcialmente; ver columna `Texto`/notas).
  - `Verificado` — implementado y validado con evidencia objetiva (test automatizado, métrica medida, revisión clínica).
- **Trazabilidad:** cada requisito debe enlazar, cuando exista, el/los issue(s) de GitHub (`#N`) que lo trabajan y el módulo (`services/<nombre>`, `packages/contracts`, `.claude/*`, etc.) donde vive su implementación. En este catálogo bootstrap la columna `Issue(s)` queda vacía (`—`) porque aún no se han creado issues.
- **Alcance real del TG** (ver `docs/anteproyecto/propuesta-alcance-tg.md`): la arquitectura completa está **diseñada**, pero solo se **implementa y valida** una rebanada vertical (mamografía 2D CBIS-DDSM + Grad-CAM + orquestación LangGraph de 4 agentes + endpoint DICOM/FHIR/SNOMED + métricas). El resto —foundation models propios, aprendizaje federado, Kubernetes/DGX, Spark, Edge AI, genómica— es trabajo futuro documentado, y así se refleja en el estado de cada requisito.
- El andamiaje de código actual (`services/*`) es un **mock**: el gateway orquesta las 3 modalidades y la fusión con lógica de placeholder, no con modelos entrenados.

## Requisitos funcionales (RF)

| ID | Texto | Estado | Módulo | Issue(s) |
|----|-------|--------|--------|----------|
| RF-001 | Ingesta de estudios de mamografía 2D en formato DICOM a través de un endpoint dedicado, con validación de conformidad del archivo (metadatos, transfer syntax, tamaño) antes de aceptar el estudio para procesamiento. | Propuesto | `services/mammography` | — |
| RF-002 | Clasificación de mamografía 2D mediante transfer learning entrenado sobre el dataset público **CBIS-DDSM**, produciendo una predicción de riesgo/hallazgo con su `score`. | Propuesto | `services/mammography` | — |
| RF-003 | Explicabilidad de la predicción de mamografía mediante **Grad-CAM**, generando un mapa de activación que señale las regiones de la imagen relevantes para el resultado. | Propuesto | `services/mammography` | — |
| RF-004 | Orquestación multiagente del sistema (**Agente Radiólogo, Agente Patólogo, Agente Gobernanza IA, Agente Auditor regulatorio**) a través de un gateway único; hoy la orquestación es un mock HTTP secuencial/paralelo simple, evolucionará a un grafo de agentes con LangGraph (ver ADR-0005). | Implementado parcial | `services/gateway` | — |
| RF-005 | Servicio de fusión multimodal que combina los resultados de las 3 modalidades (mamografía, histopatología, genómica) en un resultado único; la implementación actual usa un promedio simple (mock), quedando late fusion / attention fusion como trabajo futuro. | Implementado (mock) | `services/fusion` | — |
| RF-006 | Correlación histopatológica de los hallazgos radiológicos con datasets de referencia (**BreakHis, TCGA-BRCA**), para estratificación de riesgo y sugerencia de subtipos. | Propuesto (trabajo futuro) | `services/histopathology` | — |
| RF-007 | Endpoint interoperable que exponga y consuma los resultados clínicos bajo el contrato **HL7 FHIR / SNOMED CT**, permitiendo integración con sistemas de información hospitalaria. | Propuesto | `services/gateway` | — |
| RF-008 | Generación de un reporte clínico estructurado (clasificación **BI-RADS**, score de riesgo, recomendación) que incluya siempre el disclaimer "no es un dispositivo médico certificado". | Propuesto | `services/gateway` | — |

## Requisitos no funcionales (RNF)

| ID | Texto | Estado | Módulo | Issue(s) |
|----|-------|--------|--------|----------|
| RNF-001 | **PHI:** ningún identificador de paciente/caso (`case_ref`), ruta o nombre de archivo DICOM/WSI, `result_json` de predicción, ni URL de Storage sin firmar puede aparecer en logs, `stdout`/`stderr` ni en respuestas de API sin pasar por signed URL generada server-side. | Propuesto | transversal (todos los `services/*`) | — |
| RNF-002 | Meta operativa **aprobada por el director** para la rebanada vertical: **AUC-ROC ≥0.92** sobre el dataset de referencia (CBIS-DDSM), con protocolo de evaluación congelado antes de medir. Se miden y reportan sensibilidad, especificidad y recall como métricas complementarias; no se afirma concordancia BI-RADS si el protocolo/dataset no la habilita. Las metas aspiracionales de la visión inicial del profesor (sens. >95%, esp. >90%, AUC-ROC >0.97, recall >94%, precisión BI-RADS >93%) quedan como referencia de largo plazo, fuera del alcance de validación del TG. Falta registrar la evidencia formal de esta aprobación (ver `docs/alcance-vigente.md`). | Propuesto | `services/mammography` (y futuras modalidades) | — |
| RNF-003 | Los contratos de datos compartidos entre servicios viven en `packages/contracts/schemas/*.json` como fuente de verdad única; los modelos pydantic en `python/mama_contracts/models.py` se generan automáticamente y **nunca se editan a mano**. | Implementado | `packages/contracts` | — |
| RNF-004 | Todo commit debe seguir la convención `tipo(#N): descripción` (o `tipo: descripción` durante el bootstrap sin issues), validada automáticamente por el hook `commit-msg`. | Implementado | `.githooks/commit-msg` | — |
| RNF-005 | El sistema debe gestionar la equidad y mitigar el sesgo poblacional de los modelos, procurando representación adecuada de mujeres latinoamericanas y evitando modelos entrenados solo en poblaciones no representativas del contexto colombiano. | Propuesto | `services/mammography`, `.claude/agents/mama-gobernanza-ia.md` | — |
| RNF-006 | Cumplimiento del marco legal colombiano: **Ley 1581 de 2012** (protección de datos personales/sensibles), **Resolución 1995 de 1999** (reserva de la historia clínica), **Resolución 2654 de 2019** (plataformas tecnológicas en salud), y registro ante **INVIMA** como software con IA (SaMD) previo a uso asistencial. | Propuesto | transversal / `docs/architecture/phi-and-security.md` | — |
| RNF-007 | El diseño y operación del sistema deben alinearse con los **6 principios de ética de IA en salud de la OMS**: autonomía, bienestar y seguridad, transparencia/explicabilidad, responsabilidad, equidad, e IA ambientalmente responsable. | Propuesto | transversal / `docs/architecture/phi-and-security.md` | — |
| RNF-008 | Toda salida clínica visible al usuario (reporte, alerta, score) debe mostrar el disclaimer **"No es un dispositivo médico certificado"** de forma visible, sin excepción. | Propuesto | `services/gateway` | — |

## Mantenimiento

- **Agregar un requisito nuevo:** asignar el siguiente ID correlativo (`RF-00N`/`RNF-00N`), añadir la fila a la tabla correspondiente con estado `Propuesto`, y crear el issue de GitHub que lo trabaje (actualizando la columna `Issue(s)` con `#N`).
- **Cambiar el estado de un requisito:** actualizar la fila en este archivo cuando el issue asociado avance (`Aprobado` al priorizarlo, `Implementado` al mergear el PR que lo satisface, `Verificado` al tener evidencia objetiva — test automatizado o métrica medida — de que se cumple).
- **Nunca eliminar ni renumerar** un ID existente, aunque el requisito se descarte; en ese caso se marca su estado como `Propuesto` con una nota `[Descartado]` en el texto, para no romper trazabilidad histórica.
- **Relación con `docs/psp/traceability.md`:** ese archivo es una **vista** derivada de este catálogo (una fila por requisito, con columnas orientadas a evidencia de PSP: issue, commit/PR, evidencia). Este archivo (`requisitos.md`) es la fuente única; `traceability.md` nunca debe editarse con información que contradiga esta tabla — se actualiza en el mismo commit/PR que actualiza aquí el estado de un requisito.
- **Definition of Ready / Definition of Done** (ver `docs/psp/definition-of-ready.md` y `docs/psp/definition-of-done.md`) exigen que todo issue declare explícitamente a qué RF/RNF de este catálogo corresponde.
