# Roadmap de corrección y entrega del TG

**Fecha:** 2026-07-12  
**Propósito:** convertir el andamiaje actual en la rebanada vertical acordada, sin presentar como
implementados los componentes que permanecen como trabajo futuro.

## Norte del proyecto

**Contribución acordada por el equipo y aprobada por el director, pendiente de registrar como
evidencia:** un **copiloto de triaje mamográfico multiagente, gobernado, explicable y trazable**
para un contexto colombiano.

La propuesta no pretende competir con modelos comerciales de riesgo a cinco años ni entrenar un
foundation model. Demuestra cómo un modelo de mamografía 2D se integra con explicabilidad,
incertidumbre, reglas de gobernanza, auditoría e interoperabilidad para apoyar —no sustituir— al
profesional clínico.

## Estado de partida

- Base disponible: gateway, tres servicios de modalidad, fusión mock, contratos, Docker, CI y PSP.
- Pruebas actuales: 12 en verde; verifican contratos y mocks, no desempeño clínico.
- Rebanada aún pendiente: modelo CBIS-DDSM, Grad-CAM, DICOM/FHIR/SNOMED, LangGraph y evaluación.
- Datos reales de pacientes: fuera de alcance; hasta cerrar la seguridad se usan datos sintéticos o
  públicos anonimizados.
- Cómputo de entrenamiento: Kaggle con horas gratuitas como primera opción; AWS con GPU NVIDIA solo
  si se aprueba presupuesto. No se planifica entrenamiento local.
- Entrega académica inmediata: completar el anteproyecto en menos de 15 días; este frente documenta
  y formaliza el trabajo, pero no reduce la ruta técnica del roadmap.

## Alcance de implementación

| Se implementa y demuestra | Se diseña o documenta como futuro |
|---|---|
| Mamografía 2D, transfer learning y Grad-CAM | Foundation models propios, LLM médico propio e IA generativa |
| Grafo LangGraph de cuatro agentes de plataforma | Aprendizaje federado real y datos institucionales |
| Entrada DICOM y salida FHIR/SNOMED demostrable | Histopatología y genómica reales |
| Evaluación reproducible y controles de gobernanza | Kubernetes, DGX, Spark y Edge AI |

## Distinción obligatoria de agentes

| Capa | Rol |
|---|---|
| `.claude/agents/` | Herramientas de desarrollo para revisar código, documentación y PRs. No procesan casos ni cuentan como plataforma. |
| Plataforma LangGraph | Agentes runtime que evalúan un caso y dejan una decisión trazable: Radiólogo, Patólogo, Gobernanza IA y Auditor regulatorio. |

## Fases y entregables

### Fase 0 — Alinear y sanear la base

**Objetivo:** retirar contradicciones y riesgos antes de incorporar datos o IA real.

- **Tarea inicial de trazabilidad (antes de tocar código):** crear los issues de los frentes que se
  trabajan en esta fase — README/dashboard (B-010), coherencia del mock de fusión (B-013), PHI fuera
  de URL y respuesta (RNF-001) y alcance vigente / anteproyecto (B-008). A partir de ahí, usar la
  convención `tipo(#N): descripción` en los commits: ya no es bootstrap puro, cada commit debe
  referenciar su issue. La meta AUC-ROC ≥0.92 **no** genera issue: ya está decidida y se documenta
  como requisito (RNF-002).
- Corregir README: dashboard inexistente o incorporación explícita del dashboard reutilizado (B-010).
- Corregir la contradicción de labels del mock de fusión (B-013): cambiar el umbral de la fusión de
  `avg >= 0.5` a `avg > 0.5` y bajar el stub de mamografía a `score=0.1, label="benign"`. Los tests
  deben **validar** el cambio, no solo pasar: un caso con tres scores `0.5` debe esperar `benign`
  (falla con `>=`, pasa con `>`), y un test aparte debe comprobar que los stubs devuelven `0.1/benign`.
- Rediseñar `case_ref` (RNF-001): no usarlo en URL, respuesta ni logs; el servidor genera un
  `analysis_id` opaco. Añadir pruebas negativas de PHI, incluida una que verifique que `analysis_id`
  **no es igual** a `case_ref`. **Límite explícito de esta fase:** elimina PHI de URL y respuesta, pero
  no resuelve todavía autenticación, redacción centralizada de logs, signed URLs ni persistencia de
  auditoría; RNF-001 queda *parcial*, no cerrado.
- Establecer `docs/alcance-vigente.md` como **referencia interna actual** de alcance (B-008), sin
  editar ni reescribir los documentos históricos del profesor. Debe dejar constancia de que la meta
  **AUC-ROC ≥0.92 está aprobada según la confirmación del equipo, pero falta registrar la evidencia**
  de esa aprobación, y reconciliar el alcance recortado con el anteproyecto (B-008). La meta ≥0.92 ya
  está decidida y vive como **requisito** (RNF-002 actualizado), no como issue.

**Salida:** demo mock claramente no clínica, sin exposición de PHI en URL/respuesta y con backlog
trazable por issue. Los controles de seguridad aún no cubiertos quedan documentados como deuda.

### Frente inmediato — Anteproyecto (menos de 15 días)

**Objetivo:** que el documento formal corresponda al alcance ya aprobado y al plan técnico.

- Registrar la aprobación del alcance y de la meta operativa AUC-ROC >=0.92 mediante una referencia
  a correo, acta o validación del director, sin copiar datos personales.
- Actualizar título, objetivos, alcance, metodología, cronograma y presupuesto para reflejar la
  rebanada vertical y el cómputo en Kaggle/AWS.
- Formular la pregunta de investigación, hipótesis de innovación y baseline de comparación.
- Completar estado del arte, marco legal, referencias APA y matriz de soluciones comparables.

**Salida:** anteproyecto coherente con el repositorio y listo para revisión; no sustituye las fases
técnicas posteriores.

### Fase 1 — Modelo y protocolo de evaluación

**Objetivo:** disponer de un baseline reproducible de mamografía 2D.

- Definir tarea, etiquetas, partición por paciente, preprocesamiento y versionado de CBIS-DDSM.
- Implementar transfer learning e inferencia real en `services/mammography`.
- Congelar el protocolo antes de medir: test separado, intervalos de confianza y matriz de confusión.
- Implementar Grad-CAM asociado a cada predicción.
- Medir AUC-ROC, sensibilidad, especificidad, recall y las métricas que las etiquetas permitan.

**Meta operativa aprobada:** AUC-ROC **>=0.92**. No afirmar concordancia BI-RADS si el
protocolo/dataset no la habilita.

**Salida:** modelo baseline, pesos/versiones registrados, reporte de evaluación y ejemplos XAI.

### Frente paralelo — Estadificación TNM (AJCC 8)

**No desplaza la Fase 1 ni ninguna otra fase.** Nace de la solicitud del director del 2026-07-15 de
*identificar y validar el TNM*. Decisión en ADR-0006; requisitos **RF-009** (#6) y **RF-010** (#7).

**Por qué es un frente paralelo y no una fase:** el motor de estadificación es **determinista, sin
ML**, y está **desacoplado** del modelo de mamografía — recibe datos clínicos estructurados y
calcula. No compite por el recurso escaso de la Fase 1 (entrenamiento y protocolo de evaluación) ni
depende de él.

**Secuencia, por dependencia:**

1. **Contrato primero.** El tipo de estadificación entra en `packages/contracts/schemas/models.json`
   junto con la **Fase 2**, que ya toca contratos. Sin contrato no hay motor.
2. **Motor después** (RF-009), con **cobertura exhaustiva** de la tabla de verdad.
3. **Estimación de `cT`** (RF-010) **solo cuando exista el baseline de la Fase 1**: es la única pieza
   del frente que toca el pipeline de mamografía (requiere segmentación y `PixelSpacing`).

**Límites que este frente no cruza** — son parte del entregable, no advertencias:

- **No se afirma que se "valida el TNM" con CBIS-DDSM:** el dataset **no tiene etiquetas TNM**.
- **No se infiere `cN` ni `cM`** desde una mamografía; sin `N` ni `M` **no hay estadio**.
- **El motor se dispara sobre cáncer confirmado por biopsia**, nunca sobre la salida del modelo.
- **La meta AUC-ROC ≥0.92 no aplica aquí:** un motor determinista no tiene AUC. Su evidencia es
  cobertura exhaustiva, no métrica estadística.

**Salida:** motor verificado por tabla de verdad completa + tipo de contrato + `docs/clinical/tnm.md`
como fuente clínica. **Valor académico añadido:** es verificación **completa** —no muestreo—, y
contrasta a propósito con la evaluación estadística del modelo de mamografía: dos formas distintas de
evidencia en un mismo TG, un artefacto PSP excepcionalmente fuerte.

### Fase 2 — Contrato e interoperabilidad clínica demostrable

**Objetivo:** reemplazar contratos genéricos por una interfaz demostrable y segura.

- Validar entrada DICOM y extraer solo los datos necesarios para inferencia.
- Extender JSON Schema con tipos restringidos, disclaimer, procedencia de modelo, explicación,
  nivel de triaje, estado de gobernanza y referencias interoperables.
- Generar los contratos Pydantic desde el schema; nunca editar el generado.
- Emitir una salida FHIR/SNOMED de alcance acordado y probar ejemplos conformes.

**Interoperabilidad acordada:** DICOM validado como entrada; `DiagnosticReport` FHIR con
`Observation` codificada en SNOMED CT como salida demostrable. No se requiere conexión a un
hospital real.

**Salida:** flujo DICOM → análisis → reporte estructurado, con pruebas de contrato e
interoperabilidad.

### Fase 3 — Sistema multiagente de plataforma

**Objetivo:** implementar el requisito multiagente en runtime, no como cuatro perfiles decorativos.

| Agente | Responsabilidad mínima |
|---|---|
| Radiólogo | Integra predicción, Grad-CAM, calidad e incertidumbre; propone triaje. |
| Patólogo | Declara si existe evidencia patológica; bloquea conclusiones histológicas si no existe. |
| Gobernanza IA | Evalúa aplicabilidad, incertidumbre, versión del modelo y limitaciones del dataset. |
| Auditor regulatorio | Comprueba disclaimer, trazabilidad, seguridad e interoperabilidad antes de emitir. |

- Definir estado compartido, transiciones, reglas de abstención/escalamiento y registro de razones.
- Implementar el grafo LangGraph en el gateway.
- Probar caminos nominales, abstención, falta de evidencia, errores de contrato y bloqueo de emisión.
- Si hay LLM, limitarlo a explicaciones ancladas a artefactos estructurados; no puede alterar una
  predicción sin una regla explícita y testeable.

**Salida:** decisión de triaje reproducible y auditable por caso sintético/de prueba.

### Fase 4 — Demostrar la innovación y gobernanza

**Objetivo:** evaluar el sistema, no solo el clasificador.

- Comparar el mismo modelo base contra el flujo multiagente gobernado.
- Medir calibración, cobertura de casos aceptados, abstenciones/escalamientos, errores de alta
  confianza y completitud de evidencia, además del desempeño diagnóstico.
- Documentar límites de validez externa: CBIS-DDSM no prueba desempeño ni equidad para población
  colombiana.
- Crear model card/datasheet, control de versión de dataset/modelo y revisión humana simulada.

**Salida:** hipótesis, baseline, experimento, resultados y limitaciones defendibles en la sustentación.

### Fase 5 — Cerrar evidencia académica

**Objetivo:** que la implementación y el anteproyecto cuenten la misma historia.

- Diagramas de contexto, secuencia, datos y máquina de estados del grafo; ADRs actualizados.
- Marco teórico con fuentes primarias, matriz de estado del arte y referencias APA.
- Trazabilidad issue → requisito → commit/PR → prueba/métrica.
- Artefactos PSP/TSP/PMBOK que exija el curso: riesgos, hitos, estimación, defectos y post-mortem.

**Salida:** repositorio, informe y demo consistentes entre sí.

## Aprobaciones necesarias del director

Según confirmación del equipo, el director ya aprobó el alcance reducido y la meta AUC-ROC >=0.92.
Falta registrar esa evidencia. Los puntos siguientes deben figurar explícitamente en esa aprobación
o validarse en la siguiente revisión:

1. Alcance exacto de la rebanada vertical y constancia de que el resto es trabajo futuro.
2. Hipótesis de innovación propuesta y el rol central de la multiagencia.
3. Tarea clínica primaria: triaje de malignidad/hallazgo en mamografía 2D; queda fuera la
   predicción de riesgo a cinco años.
4. Objetivo operativo **AUC-ROC >=0.92** y definición de las demás métricas/criterios de éxito.
5. Definición mínima de DICOM, FHIR y SNOMED para una demostración académica.
6. Forma de evaluar la entrega: resultados, demo, revisión clínica, diagramas y evidencia PSP/TSP/PMBOK.
7. **Alcance del TNM (ADR-0006, aceptada por el equipo el 2026-07-15 — no por el director).** Debe
   quedar explícito que el sistema **no puede inferir el TNM desde una mamografía** (`cN` no es
   inferible; `cM0` es juicio clínico) y que **no se valida TNM contra CBIS-DDSM** (no tiene esas
   etiquetas). Lo que sí se entrega: un motor **determinista** que **calcula** el estadio pronóstico
   con datos clínicos **recibidos**, más una **propuesta** de `cT` desde imagen. Se adopta **AJCC 8**
   (el Anexo 9 de la GPC del Minsalud reproduce AJCC 7).

## Decisiones operativas resueltas

| Tema | Decisión |
|---|---|
| Tarea primaria | Triaje de hallazgo/malignidad en mamografía 2D, no riesgo a cinco años |
| Agentes | Híbridos y reproducibles: reglas, modelos y herramientas; LLM solo para explicación anclada a evidencia |
| Cómputo | Kaggle gratuito como primera opción; AWS GPU si se aprueba presupuesto; sin entrenamiento local |
| Interoperabilidad | DICOM de entrada y `DiagnosticReport` FHIR + `Observation` SNOMED CT de salida |
| Interfaz | Reutilizar al máximo el dashboard existente, sin crear otro producto desde cero |
| Horizonte | El anteproyecto debe completarse en menos de 15 días; el roadmap técnico mantiene su alcance |
| Estadificación TNM | **AJCC 8** (no el Anexo 9 de la GPC, que es AJCC 7). Se implementa la tabla **pronóstica**, no solo la anatómica: el motor **recibe** grado Nottingham + RE/RP/HER2 como dato estructurado. Determinista, sin ML, desacoplado del modelo (ADR-0006) |

## Única evidencia pendiente

Localizar o registrar la evidencia de aprobación del director para el alcance y AUC-ROC >=0.92. Si
la aprobación fue verbal, crear una minuta o enviar un correo de recapitulación para que quede un
registro verificable.

**Oportunidad de doble propósito:** ya existe un **hilo vivo** con el director (correo del
2026-07-15, asunto TNM), todavía **sin responder**. Responder ese hilo con la **delimitación del
TNM** (punto 7 de las aprobaciones) **más** la **recapitulación del alcance y de AUC-ROC >=0.92**
cierra **ambas cosas de una vez**: es la misma evidencia que necesitan RNF-002 y ADR-0006. Sin
reproducir datos personales del hilo en el repositorio (Ley 1581/2012): citarlo por **fecha y
asunto**.

## Criterio de finalización del roadmap

El roadmap se considera cumplido cuando exista una demo con datos públicos/sintéticos donde un estudio
DICOM válido recorra el modelo de mamografía, Grad-CAM y el grafo multiagente, produzca una salida
FHIR/SNOMED trazable con disclaimer, y esté acompañada de un protocolo y reporte de evaluación
reproducible. No se debe declarar uso asistencial, validación colombiana ni certificación médica.

## Documentos relacionados

- `docs/auditoria-alineacion-profesor.md` — evidencia de brechas, decisiones y preguntas.
- `docs/handoff-estado-y-roadmap.md` — contexto de continuidad anterior; algunas decisiones abiertas
  fueron precisadas en este roadmap y aún deben ser aprobadas por el director.
- `docs/requisitos.md` — fuente de verdad de RF/RNF; actualizarla solo tras crear issues y contar
  con evidencia o aprobación pertinente.
- `docs/alcance-vigente.md` — referencia interna del alcance vigente y de la meta AUC-ROC ≥0.92
  (aprobada, evidencia pendiente); no reescribe los documentos históricos del profesor.
- `docs/adr/0006-estadificacion-tnm-ajcc8-pronostica.md` — decisión de estadificación TNM (AJCC 8,
  tabla pronóstica); aceptada por el equipo, pendiente de validación del director.
- `docs/clinical/tnm.md` — fuente clínica única de TNM: qué es inferible desde imagen y qué no.
- `docs/handoff-tnm-ajcc8.md` — continuidad del frente TNM: hallazgos, trampas ya corregidas y
  trabajo pendiente.
