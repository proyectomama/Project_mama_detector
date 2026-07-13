# Prompt de handoff — estado y roadmap de `mama-detector`

> Pega este prompt en una sesión nueva para retomar el trabajo con todo el contexto.
> Este documento conserva el diagnóstico inicial; el roadmap vigente es
> [`roadmap-tg.md`](roadmap-tg.md), complementado por
> [`auditoria-alineacion-profesor.md`](auditoria-alineacion-profesor.md).
> **Decisiones posteriores:** el equipo confirma aprobación del alcance y AUC-ROC >=0.92; la
> contribución se orienta a un copiloto de triaje mamográfico multiagente, gobernado, explicable y
> trazable. Falta registrar la evidencia de aprobación. No tratar como vigente la sección
> “Decisión ABIERTA” de este documento sin contrastarla con el roadmap actual.

---

## Contexto

Trabajas en `mama-detector` (repo Git independiente en `W:\mama-detector`): plataforma
académica multimodal (mamografía + histopatología + genómica) de apoyo a la detección temprana
de cáncer de mama, para un Trabajo de Grado. **No es un dispositivo médico certificado.**

**Estado actual (verificado):** el andamiaje está completo y sano — 5 microservicios FastAPI
(gateway + 3 modalidades + fusión), contratos compartidos generados desde JSON Schema, docker-compose,
CI, ADRs, artefactos PSP y anteproyecto. **12 pruebas pasan** (contratos + orquestación). Toda la
lógica de IA es **mock** y está documentada como tal. El siguiente trabajo NO es más andamiaje: es
la rebanada vertical clínica + alineación académica.

**Diagnóstico de referencia:** `docs/auditoria-alineacion-profesor.md` — 16 hallazgos (B-001…B-016).
La distinción clave del auditor (y que hay que preservar frente al profesor): separar lo que se
**recortó legítimamente** a trabajo futuro (federated learning, histopatología/genómica reales,
foundation models, K8s/DGX/Spark) de lo que **sí es brecha** (la rebanada vertical acordada, los
artefactos comprometidos y la innovación exigida).

## Convenciones (obligatorias)

- Commits en español: `tipo: descripción breve` (`feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `test`). **Sin atribución a IA/Claude.**
- **PHI:** nunca loguear identificadores de paciente/caso, rutas/nombres de archivos (DICOM/WSI),
  resultados de predicción ni URLs de Storage. Solo datos sintéticos hasta cerrar B-011.
- Contratos: `packages/contracts/schemas/*.json` es la fuente de verdad. El código pydantic/TS es
  **generado** (`just gen-contracts`); nunca se edita a mano.

---

## Roadmap accionable (todo MENOS la innovación)

### Fase 0 — Quick-wins (horas, hazlos primero: quitan riesgo/vergüenza inmediata)

- **B-010 — README miente.** El README anuncia `apps/web` (dashboard Next.js) que no existe en el
  árbol. Corregir el README/plan o incorporar el dashboard. Acción mínima: corregir el README.
- **B-013 — Fusión clínicamente incoherente.** `services/fusion/app/strategy.py` etiqueta
  `malignant` si `avg >= 0.5`, pero los stubs devuelven `0.5`/`benign`: un caso por defecto sale
  "benign" por modalidad y "malignant" por fusión. Aislar el mock de cualquier demo o definir una
  semántica temporal coherente (y marcarla explícitamente como no-clínica).
- **B-011 — PHI expuesto.** `POST /cases/{case_ref}/analyze` recibe `case_ref` en la URL y lo
  devuelve en `ClinicalAlert` (queda en logs de Uvicorn y en la respuesta). Rediseñar: sacar el
  identificador de la URL, no devolverlo crudo, redactar logs, y añadir pruebas negativas de PHI.
  Barato ahora, carísimo con datos reales.

### Fase 1 — Rebanada vertical clínica (el grueso del trabajo; convertir en issues trazables)

- **B-001 — Modelo de mamografía.** Clasificador 2D sobre CBIS-DDSM con transfer learning:
  dataset y partición reproducible, dependencias de visión médica, versionado de pesos, inferencia
  real reemplazando `services/mammography/app/model.py`, pruebas de integración.
- **B-002 — Explicabilidad Grad-CAM.** Producir y asociar el mapa de activación a cada predicción;
  definir entrega segura, evaluar fidelidad y plausibilidad radiológica.
- **B-004 — Interoperabilidad demostrable.** Contrato de entrada DICOM con validaciones, recurso
  HL7 FHIR de salida, codificación SNOMED CT, ejemplos conformes y pruebas de interoperabilidad.
- **B-005 — Evaluación clínica.** Protocolo congelado antes de medir, conjunto de prueba separado,
  matriz de confusión, AUC-ROC/sensibilidad/especificidad/recall/precisión BI-RADS con intervalos de
  confianza, y reporte honesto aunque no alcance los umbrales objetivo.

### Fase 2 — Multiagente y contratos clínicos

- **B-003 — Sistema multiagente LangGraph.** Hoy el gateway solo hace `asyncio.gather` + fusión.
  Implementar el grafo (estado, mensajes, responsabilidades y criterios deterministas de los agentes
  Radiólogo/Patólogo/Gobernanza IA/Auditor, escalamiento, trazabilidad, pruebas del grafo, y
  protección contra presentar salida generativa como diagnóstico). *Nota: este entregable puede
  quedar acoplado a la tesis de innovación — ver la decisión abierta abajo antes de sobre-construir.*
- **B-012 — Contratos con dominio clínico.** El schema permite strings libres para `modality`/`label`/
  `level`. Modelar BI-RADS, disclaimer, explicabilidad, procedencia/versionado del modelo, código
  SNOMED, recurso FHIR y estado de gobernanza; versionar el contrato y regenerar consumidores.

### Fase 3 — Gobernanza y proceso (en paralelo; cuentan para la nota)

- **B-014 — Gobernanza/equidad verificable.** Hoy declarada, no medible. Métricas por subgrupo,
  monitorización de drift, límites de generalización a población colombiana, registro de
  versión/dataset/modelo, revisión humana.
- **B-007 — Diseño detallado.** Diagramas de contexto/contenedores, secuencia de análisis, modelo de
  datos, máquina de estados del grafo, especificaciones de integración; coherentes con los ADRs.
- **B-009 — Estado del arte académico.** Revisión de literatura con fuentes primarias, referencias
  APA, matriz de comparación de baselines y discusión crítica.
- **B-015 / B-016 — Trazabilidad PSP y TSP/PMBOK.** Crear issues por RF/RNF con criterios de
  aceptación, actualizar la matriz con evidencia real (PR/commits), registrar defectos y post-mortems;
  decidir qué artefactos TSP/PMBOK mínimos exige el curso y versionarlos.

### Alineación académica (transversal, alta prioridad)

- **B-008 — Anteproyecto contradictorio.** `anteproyecto.docx` aún promete modelos multimodales,
  foundation models y federated learning; el alcance acordado los deja como futuro. Además
  `propuesta-alcance-tg.md` pide visto bueno que los correos dicen ya concedido. Establecer un
  documento de alcance vigente, registrar la aceptación del profesor y actualizar título, objetivos,
  metodología y cronograma para no prometer lo recortado.

---

## Decisión ABIERTA — no ejecutar sin decidir con el profesor

**B-006 — Tesis de innovación.** Es el hallazgo existencial: el profesor exige un aporte innovador
verificable (hipótesis, baseline, experimento, métrica), no solo "tecnología empleada". Está
**deliberadamente sin fijar**. Antes de construir B-003/B-014 en profundidad, hay que elegir la
dirección **con el profesor**. Opciones sobre la mesa (no elegidas):

1. **Orquestación multiagente trazable y gobernada** para triage de mama en contexto colombiano, con
   explicabilidad y equidad como controles verificables. (Fusiona B-003 + B-014 en el aporte.)
2. **Explicabilidad clínica (XAI)** como eje: Grad-CAM + medición de fidelidad + plausibilidad
   radiológica como contribución diferencial. (Centra el aporte en B-002.)
3. **Otra dirección** a definir.

Cualquiera debe expresarse como pregunta de investigación → hipótesis → requisitos → experimento →
baseline → métrica de éxito. **Tarea del asistente: ayudar a formularla cuando el equipo/profesor
elija; no darla por decidida.**

---

## Prioridad recomendada para arrancar

1. Fase 0 (quick-wins) — inmediato, sin depender de nadie.
2. B-008 (alineación del anteproyecto) — protege la evaluación académica.
3. Fase 1 (rebanada vertical) convertida en issues trazables.
4. La tesis de innovación (B-006) se resuelve con el profesor en paralelo, y recién entonces se
   profundiza B-003/B-014 en la dirección elegida.
