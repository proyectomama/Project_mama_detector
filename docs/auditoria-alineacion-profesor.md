# Auditoría de alineación con visión del profesor y alcance acordado

**Fecha de revisión:** 2026-07-12  
**Estado:** diagnóstico inicial; no sustituye una revisión o aprobación del profesor.  
**Alcance de la revisión:** repositorio `mama-detector`, el anteproyecto incluido y el resumen de correos del Trabajo de Grado.

## Propósito

Este documento registra la diferencia entre:

1. La **visión inicial** del profesor: plataforma clínica multimodal, multiagente y basada en IA avanzada.
2. El **alcance reducido aceptado en los correos**: arquitectura completa diseñada y una rebanada vertical implementada y evaluada.
3. La **evidencia actual** en el repositorio.

No debe interpretarse que todos los componentes de la visión inicial son incumplimientos: varios
se trasladaron explícitamente a trabajo futuro por las restricciones de tiempo, hardware y
presupuesto. Sí son brechas los elementos que pertenecen a la rebanada vertical acordada, los
artefactos de diseño comprometidos y la innovación exigida por el profesor.

## Fuentes revisadas

- Resumen de correos del TG aportado por el equipo: visión, alcance aprobado y observación del profesor sobre innovación.
- `docs/anteproyecto/anteproyecto.docx`.
- `docs/anteproyecto/resumen-requisitos-profesor.md`.
- `docs/anteproyecto/propuesta-alcance-tg.md`.
- `docs/requisitos.md`, `docs/architecture/*`, `docs/adr/*` y `docs/psp/*`.
- Código, contratos, contenedores, CI y pruebas en `services/*`, `packages/contracts` e `infra/`.

## Resumen ejecutivo

El repositorio está bien encaminado como **andamiaje técnico y de proceso**: tiene cinco
microservicios FastAPI, contratos compartidos generados desde JSON Schema, Compose, CI, pruebas
de contrato y documentación explícita de que la lógica es mock. Sin embargo, no es todavía una
implementación de la rebanada vertical acordada. En particular, no contiene un modelo entrenado
de mamografía, Grad-CAM, agentes LangGraph en runtime, endpoint DICOM/FHIR/SNOMED, ni evaluación
clínica.

El riesgo académico principal no es que falte la arquitectura completa originalmente planteada
(esa parte fue correctamente acotada), sino que falta definir y demostrar el **aporte innovador**
que el profesor pidió al aceptar el alcance.

## Mapa de cumplimiento

| Compromiso | Evidencia actual | Estado |
|---|---|---|
| Diseño de arquitectura multimodal, multiagente, interoperable y gobernada | Diagrama general, ADRs, requisitos y servicios mock | Parcial |
| Clasificador de mamografía 2D con CBIS-DDSM y transfer learning | `mammography` retorna una predicción fija | No iniciado |
| Explicabilidad Grad-CAM | No hay implementación, dependencia ni prueba XAI | No iniciado |
| Cuatro agentes clínicos de plataforma orquestados con LangGraph | Los cuatro archivos de `.claude/agents/` son tooling de desarrollo; los agentes de runtime, que son requisito central, están pendientes | No iniciado |
| Endpoint demostrable DICOM + HL7 FHIR + SNOMED CT | No hay ingesta DICOM, recursos FHIR ni codificación SNOMED | No iniciado |
| Evaluación por sensibilidad, especificidad, AUC-ROC, recall y precisión BI-RADS | No hay dataset, particiones, pipeline ni resultados medidos | No iniciado |
| Gobernanza, equidad y cumplimiento clínico | Política y requisitos documentados; sin controles técnicos ni monitorización | Parcial |
| PSP/TSP/PMBOK | PSP, DoR/DoD, defect log y plantillas presentes; trazabilidad sin issues y sin artefactos TSP/PMBOK completos | Parcial |
| Innovación diferencial solicitada por el profesor | No hay hipótesis, baseline, diferencial técnico ni protocolo experimental | Ausente |

## Brechas frente al alcance aprobado

### B-001 — No existe todavía el modelo de mamografía de la rebanada vertical

**Severidad:** bloqueante para afirmar que existe detección temprana basada en IA.  
**Compromiso:** clasificador de mamografía 2D sobre CBIS-DDSM mediante transfer learning.  
**Evidencia:** `services/mammography/app/model.py` devuelve siempre `Prediction(score=0.5, label="benign")`; el preprocesamiento devuelve `None`.

**Falta para cerrar:** dataset y protocolo de partición reproducible, modelo entrenable, dependencias
de visión médica elegidas, pesos/versionado de artefactos, inferencia real y pruebas de integración.

### B-002 — No hay Grad-CAM ni otra evidencia de explicabilidad

**Severidad:** bloqueante para RF-003 y para la promesa de XAI clínica.  
**Compromiso:** explicación de cada predicción de mamografía mediante Grad-CAM.  
**Evidencia:** no hay código, contrato, endpoint, almacenamiento ni pruebas de mapas de activación.

**Falta para cerrar:** producir y asociar el mapa con la predicción, definir cómo se entrega de forma
segura, evaluar su fidelidad y revisar su plausibilidad radiológica.

### B-003 — La plataforma no implementa aún el sistema multiagente

**Severidad:** bloqueante para el requisito explícito de multiagencia.  
**Compromiso:** agentes de plataforma Radiólogo, Patólogo, Gobernanza IA y Auditor regulatorio,
orquestados con LangGraph. El sistema multiagente es un componente central de la innovación y no
debe sustituirse por el tooling de desarrollo ni por una cadena de prompts sin estado.

**Evidencia:** el gateway usa `asyncio.gather` para llamar tres servicios y luego fusiona el resultado.
El ADR-0005 confirma que LangGraph en runtime es trabajo pendiente. Los archivos en `.claude/agents/`
revisan código durante el desarrollo y no analizan casos clínicos.

**Falta para cerrar:** estado y mensajes del grafo, responsabilidades y criterios verificables de
cada agente, reglas de escalamiento, trazabilidad de la decisión, pruebas del grafo y protección
contra que una salida generativa se presente como diagnóstico. La propuesta de diseño se detalla en
la sección «Sistema multiagente de la plataforma» de este documento.

### B-004 — La interoperabilidad comprometida no está implementada

**Severidad:** bloqueante para el endpoint demostrable acordado.  
**Compromiso:** DICOM, HL7 FHIR y SNOMED CT con un endpoint funcional.

**Evidencia:** la petición actual solo contiene `case_ref`; no se valida ni procesa un archivo DICOM,
no existen perfiles/recursos FHIR y no hay códigos SNOMED.

**Falta para cerrar:** contrato de entrada DICOM y sus validaciones, recurso FHIR de salida elegido,
vocabulario SNOMED, ejemplos conformes y pruebas de interoperabilidad.

### B-005 — No hay evaluación clínica ni evidencia de las métricas objetivo

**Severidad:** bloqueante para validar el modelo.  
**Compromiso inicial comunicado por el profesor:** sensibilidad >95 %, especificidad >90 %,
AUC-ROC >0.97, recall >94 % y precisión BI-RADS >93 %, frente al dataset de referencia.

**Decisión confirmada por el equipo como aprobada por el director:** para la rebanada vertical
sobre CBIS-DDSM se usa **AUC-ROC >=0.92** como objetivo operativo. El valor inicial no se elimina:
se conserva como antecedente y como referencia de aspiración, sin afirmar que se alcanzará con el
hardware, dataset y plazo disponibles. Falta registrar la evidencia de aprobación.

**Evidencia:** las 12 pruebas actuales verifican contratos y orquestación mock; no prueban un modelo
ni calculan métricas clínicas.

**Falta para cerrar:** protocolo de evaluación congelado antes de medir, conjunto de prueba separado,
intervalos de confianza, matriz de confusión, definición operacional de BI-RADS y reporte honesto de
resultados aunque no alcancen los umbrales objetivo.

### B-006 — El requisito de innovación no se ha convertido en una propuesta verificable

**Severidad:** bloqueante para la diferenciación académica solicitada por el profesor.  
**Compromiso:** aportar valor tecnológico adicional; los sistemas existentes deben servir solo como referencia.

**Evidencia:** el repositorio cita Clairity Breast, Mammo-FM y OncoVision, pero no formula una
pregunta de investigación, hipótesis, contribución diferencial, baseline ni criterio de éxito.

**Falta para cerrar:** acordar una tesis de innovación viable dentro de la rebanada vertical, por
ejemplo una estrategia de gobernanza/equidad explicable para contexto colombiano, un flujo de
triage trazable de agentes o una comparación rigurosa de arquitectura y explicabilidad. Debe
expresarse como hipótesis, requisitos, experimento, baseline y métrica; no solo como tecnología
empleada.

## Decisiones de trabajo incorporadas

Estas decisiones fueron acordadas durante la revisión del repositorio. Según confirmación del
equipo, el alcance reducido y la meta AUC-ROC >=0.92 ya fueron aprobados por el director; falta
registrar la evidencia de esa aprobación.

1. El sistema **multiagente de la plataforma es central** para el TG y debe implementarse en
   runtime con LangGraph. No es opcional ni se reemplaza por los subagentes de `.claude/agents/`.
2. Los subagentes de `.claude/agents/` siguen siendo útiles, pero únicamente para revisar código,
   documentos y PRs durante el desarrollo. No procesan casos clínicos y no cuentan como agentes del
   producto.
3. La innovación aprobada se orienta a un **copiloto de triaje mamográfico gobernado, explicable
   y trazable para el contexto colombiano**, no a competir con plataformas comerciales en volumen
   de datos ni a entrenar un foundation model propio.
4. Para la rebanada vertical se adopta una meta operativa de **AUC-ROC >=0.92**. El umbral >0.97
   se mantiene documentado como expectativa inicial del profesor y antecedente histórico.
5. La tarea primaria es triaje de malignidad/hallazgo en mamografía 2D, no predicción de riesgo a
   cinco años. Los agentes usan un enfoque híbrido y reproducible; un LLM, si se incorpora, solo
   genera explicaciones ancladas a evidencia estructurada.
6. La plataforma no debe llamar “multimodal real” a los stubs de histopatología y genómica. En la
   demo vertical se debe declarar con precisión que el modelo usa mamografía 2D; las demás
   modalidades pertenecen al diseño evolutivo.

## Sistema multiagente de la plataforma

### Distinción obligatoria de capas

| Capa | Dónde vive | Finalidad | Qué no es |
|---|---|---|---|
| Tooling de desarrollo | `.claude/agents/` y `.claude/commands/` | Revisar implementación, seguridad, requisitos y documentación | No analiza pacientes ni integra el producto desplegado |
| Sistema multiagente de plataforma | `services/gateway` y el futuro módulo LangGraph | Coordinar una decisión clínica asistida sobre un caso y dejar evidencia auditable | No es un conjunto de perfiles conversacionales sin reglas, estado ni pruebas |

### Propuesta de responsabilidades ejecutables

El grafo debe recibir artefactos estructurados del modelo —predicción, incertidumbre, Grad-CAM,
validación DICOM, versión de modelo y limitaciones— y producir un reporte de apoyo, nunca un
diagnóstico autónomo.

| Agente de plataforma | Responsabilidad en la rebanada vertical | Resultado verificable |
|---|---|---|
| Radiólogo | Interpreta la salida de mamografía, calidad, incertidumbre y mapa Grad-CAM; propone nivel de triaje | Hallazgo estructurado y razón de escalamiento |
| Patólogo | Verifica si hay evidencia histopatológica disponible; si no existe, impide inferir subtipo, grado o confirmación por biopsia | `evidence_status` y límites explícitos de la conclusión |
| Gobernanza IA | Revisa aplicabilidad del modelo, incertidumbre, calidad de explicación, versión/dataset y limitaciones de generalización | Aprobación, abstención o escalamiento con razones trazables |
| Auditor regulatorio | Verifica presencia de disclaimer, trazabilidad, salida interoperable y reglas de seguridad antes de publicar el reporte | Decisión de emisión/bloqueo y lista de controles cumplidos |

Los agentes pueden combinar reglas deterministas y herramientas controladas. Si se incorpora un
LLM, sus salidas deben estar limitadas a evidencia estructurada, no pueden alterar la predicción del
modelo sin una regla explícita y deben poder reproducirse en pruebas. LangGraph debe conservar el
estado, las transiciones y las razones de cada decisión.

### Hipótesis de innovación propuesta

> Frente a un clasificador de mamografía aislado, un flujo multiagente gobernado que incorpora
> calidad de entrada, incertidumbre, explicabilidad, límites de evidencia y trazabilidad clínica
> puede aumentar la **seguridad y accionabilidad** del triaje sin presentar su salida como un
> diagnóstico autónomo.

La comparación experimental no debe prometer una mejora artificial de AUC por tener agentes. Debe
comparar el mismo modelo base contra el modelo integrado al flujo gobernado y medir, además de la
capacidad de clasificación, calibración, cobertura de casos aceptados, abstenciones/escalamientos,
errores de alta confianza y completitud de la evidencia del reporte.

## Síntesis del estado del arte revisado

Los enlaces compartidos muestran cuatro familias de soluciones:

- **Predicción de riesgo y segunda lectura:** Clairity estima riesgo a cinco años y declara que no
  diagnostica cáncer ni reemplaza al profesional; Google, Hera-MI y brAInray se enfocan en apoyo a
  lectura, calidad, BI-RADS o flujo DICOM.
- **Modelos visuales de gran escala:** MammoDINO, Mammo-FM y el sistema 2D+DBT de Park/Witowski
  usan datasets de cientos de miles o millones de imágenes. Son baselines de estado del arte, no
  metas realistas para entrenar desde cero en un TG.
- **Multimodalidad clínica:** OncoVision fusiona mamografía y datos clínicos; por ello la
  rebanada mamográfica debe evitar afirmaciones de fusión multimodal real hasta disponer de datos y
  evaluación por modalidad.
- **Agentes, gobernanza y seguridad:** AgentClinic, AMIE y MIRA refuerzan que un agente clínico
  debe evaluarse en decisiones secuenciales y con herramientas; ROADMAP aporta una referencia para
  describir modelos/datasets; el trabajo de imágenes sintéticas destaca la necesidad de procedencia
  e integridad de la imagen. Estos son los referentes más útiles para la innovación propuesta.

Las páginas divulgativas y comerciales sirven para contextualizar; los preprints, artículos
revisados y documentación primaria deben sustentar el marco teórico y las afirmaciones de desempeño.

## Brechas de diseño y documentación

### B-007 — La arquitectura completa está documentada solo a alto nivel

**Severidad:** alta.  
**Compromiso:** diseño completo documentado mediante diagramas UML y ADRs.

**Evidencia:** existe un diagrama general Mermaid y ADRs útiles, pero no se hallaron diagramas UML
ni diseños detallados de secuencia clínica, modelo de datos, ciclo de vida del estudio, mensajes
del grafo de agentes, integración FHIR/DICOM o amenazas de seguridad.

**Falta para cerrar:** diagramas de contexto/contenedores, secuencia de análisis, modelo de datos,
máquina de estados del grafo y especificaciones de integración; mantenerlos coherentes con los ADRs.

### B-008 — El anteproyecto formal y el alcance aprobado se contradicen

**Severidad:** alta para evaluación académica.  
**Evidencia:** el documento `anteproyecto.docx` conserva objetivos de entrenar modelos multimodales,
foundation models y aprendizaje federado. El alcance acordado limita la implementación a mamografía
2D y deja esos componentes como futuro. Además, `propuesta-alcance-tg.md` todavía solicita el visto
bueno del profesor, mientras el resumen de correos dice que el alcance fue aceptado.

**Falta para cerrar:** establecer un documento de alcance vigente, registrar la aceptación del
profesor y actualizar título, objetivo general, objetivos específicos, metodología y cronograma del
anteproyecto para que no prometan lo que se dejó fuera de alcance.

### B-009 — El estado del arte y la bibliografía no están convertidos en un artefacto académico

**Severidad:** alta.  
**Evidencia:** hay enlaces y resúmenes de referencias, pero el anteproyecto formal mantiene vacías
las secciones de marco teórico, metodología y referencias. No hay matriz de comparación de baselines
ni discusión crítica que sitúe la innovación propuesta.

**Falta para cerrar:** revisión de literatura con fuentes primarias, referencias APA, síntesis de
brechas del estado del arte y relación directa con la hipótesis de innovación.

### B-010 — El README anuncia un dashboard que no existe en el árbol actual

**Severidad:** media.  
**Evidencia:** `README.md` lista `apps/web` como dashboard Next.js, pero no existe el directorio.

**Falta para cerrar:** incorporar el dashboard reutilizado o corregir el README y el plan para que
no se anuncie como parte del repositorio.

## Brechas técnicas y de seguridad

### B-011 — El manejo actual de PHI contradice la política documentada

**Severidad:** alta; bloqueante ante cualquier dato real.  
**Evidencia:** `case_ref` se recibe dentro de la URL `POST /cases/{case_ref}/analyze` y se devuelve
en `ClinicalAlert`. Esto contradice RNF-001, que prohíbe exponerlo en respuestas; la ruta también
puede quedar en logs de acceso de Uvicorn. No hay autenticación, autorización, signed URLs,
redacción de logs ni almacenamiento seguro.

**Falta para cerrar:** rediseñar el identificador expuesto, aplicar autenticación/autorización,
redacción y retención de logs, acceso mediante URLs firmadas cuando corresponda y pruebas negativas
de PHI. Hasta entonces, usar exclusivamente datos sintéticos.

### B-012 — Contratos aún no representan el dominio clínico requerido

**Severidad:** alta.  
**Evidencia:** el schema permite strings libres para `modality`, `label` y `level`; no contiene
BI-RADS, disclaimer, explicabilidad, procedencia del modelo, código SNOMED, recurso FHIR, estado de
gobernanza ni versionado del modelo.

**Falta para cerrar:** modelar las restricciones y campos clínicos mínimos de la rebanada vertical;
versionar el contrato y regenerar los consumidores desde el schema fuente.

### B-013 — La fusión mock presenta semántica clínica inconsistente

**Severidad:** media, pero bloqueante si se mostrara como resultado clínico.  
**Evidencia:** cada modalidad stub devuelve `score=0.5` y `label="benign"`, mientras la fusión
clasifica como `malignant` todo promedio mayor o igual a 0.5. Un caso default queda etiquetado de
forma contradictoria.

**Falta para cerrar:** aislar claramente el mock de cualquier demo clínica o definir una semántica
temporal coherente; cuando exista modelo, justificar y calibrar umbrales con datos de validación.

### B-014 — Gobernanza y equidad se declaran, pero no se pueden verificar

**Severidad:** alta.  
**Evidencia:** se documentan Ley 1581, Resoluciones 1995/2654, INVIMA y principios OMS. No existen
métricas por subgrupo, monitorización de drift/desempeño, revisión clínica/ética, política de
versionado del modelo ni controles técnicos de auditoría.

**Falta para cerrar:** protocolo de evaluación de sesgo, limitaciones explícitas de generalización a
población colombiana, registro de versión/dataset/modelo, revisión humana y evidencia de cumplimiento
proporcional al alcance académico.

## Brechas de proceso y trazabilidad

### B-015 — La trazabilidad PSP está preparada, pero todavía vacía

**Severidad:** media.  
**Evidencia:** `docs/requisitos.md`, DoR, DoD, plantillas, hook y defect log están presentes, pero
no hay issues enlazados en los requisitos ni evidencia de PR/commit para los requisitos sustantivos.
Solo hay un defecto de configuración registrado.

**Falta para cerrar:** crear y priorizar issues por RF/RNF, actualizar la matriz con evidencia real,
registrar defectos y realizar post-mortems por hito.

### B-016 — TSP y PMBOK no tienen evidencia operativa suficiente

**Severidad:** media.  
**Evidencia:** PSP está adaptado documentalmente, pero no se encontraron registros de estimación de
esfuerzo/tiempo, roles o métricas de equipo TSP, ni registro de riesgos, hitos, presupuesto y control
de cambios propio de PMBOK.

**Falta para cerrar:** decidir qué artefactos mínimos exige el curso y versionarlos en el repositorio
o enlazarlos desde una fuente institucional controlada.

## Componentes correctamente acotados como trabajo futuro

No se consideran incumplimientos del alcance reducido, siempre que se mantengan explícitamente como
trabajo futuro y no se presenten como implementados:

- Foundation models propios, LLM médicos e IA generativa.
- Aprendizaje federado real entre instituciones.
- Modelos reales de histopatología y genómica.
- Kubernetes, DGX, Spark, Edge AI y entrenamiento distribuido.
- Bases de datos institucionales y despliegue asistencial.

El diseño de estos componentes aún debe ganar detalle para satisfacer la promesa de “arquitectura
completa diseñada”, pero su ausencia de código es coherente con el recorte aprobado.

## Verificación realizada

La revisión ejecutó las suites disponibles: **12 pruebas pasaron** (3 de contratos y 9 de servicios).
La cobertura actual verifica modelos de datos, health checks y orquestación HTTP mock. No constituye
validación de desempeño clínico, seguridad, interoperabilidad ni comportamiento multiagente.

## Priorización recomendada

1. Acordar y registrar con el director el alcance vigente, la hipótesis de innovación y la métrica
   AUC-ROC propuesta; luego alinear el anteproyecto.
2. Diseñar el estado, reglas, contratos y pruebas del sistema multiagente de plataforma antes de
   integrar LangGraph en el gateway.
3. Convertir la rebanada vertical en requisitos trazables con issues y criterios de aceptación.
4. Implementar la ruta clínica mínima: DICOM seguro, modelo CBIS-DDSM, Grad-CAM y evaluación.
5. Implementar el grafo LangGraph y el contrato FHIR/SNOMED demostrable sobre resultados
   estructurados del modelo.
6. Completar la evidencia de gobernanza, equidad, seguridad y PSP/PMBOK antes de una demo clínica.

## Acuerdos indispensables con el director

Estos puntos no deben quedar implícitos ni resolverse solo dentro del código. El equipo confirma que
el alcance y AUC ya están aprobados; se debe registrar esa evidencia. Los demás deben validarse o
quedar explícitos en correo, acta o comentario de aprobación del anteproyecto.

1. **Alcance aprobado y su evidencia.** Registrar que la implementación se limita a mamografía 2D
   con CBIS-DDSM, Grad-CAM, multiagencia, interoperabilidad demostrable y evaluación; el resto se
   mantiene como diseño/trabajo futuro.
2. **Contribución de innovación.** Registrar que el aporte es el copiloto de triaje multiagente
   gobernado, explicable y trazable, en vez de afirmar una nueva IA fundacional o competir con
   productos comerciales.
3. **Pregunta y tarea clínica exacta.** Registrar que el modelo base predice malignidad/hallazgo
   para triaje en mamografía 2D. No se deben mezclar detección actual y riesgo a cinco años: son
   problemas clínicos y métricas diferentes.
4. **Métricas y criterio de éxito.** Registrar la aprobación de AUC-ROC >=0.92 como objetivo
   operativo; acordar qué métricas restantes son obligatorias, cómo se calcula cada una y qué ocurre
   si CBIS-DDSM no posee etiquetas adecuadas para una métrica como precisión BI-RADS.
5. **Rol de los cuatro agentes.** Validar que el Patólogo opere como verificador de evidencia y
   límite de conclusiones mientras no exista histopatología real, y que la plataforma sea apoyo a la
   decisión, no diagnóstico autónomo.
6. **Interoperabilidad demostrable.** Acordar qué evidencia mínima basta: tipo de entrada DICOM,
   recurso FHIR de salida, alcance de SNOMED y si se requiere conexión a un sistema hospitalario real
   o una demostración conforme al estándar.
7. **Datos y validez externa.** Confirmar que el uso de CBIS-DDSM sirve para el prototipo, pero no
   permite reclamar desempeño o equidad en población colombiana; definir cómo se reportará esa
   limitación.
8. **Forma de evaluación académica.** Acordar qué artefactos entregarán evidencia: protocolo,
   resultados, demo, diagramas, ADRs, trazabilidad PSP/TSP/PMBOK y revisión clínica.

## Preguntas pendientes del equipo

La única pregunta pendiente es dónde reside la evidencia de aprobación del alcance y AUC. Si fue
verbal, debe generarse una minuta o correo de recapitulación. En ambos casos se registra la
referencia sin reproducir datos personales ni contenido sensible.

## Referencias internas

- `docs/requisitos.md` — fuente de verdad de RF/RNF.
- `docs/architecture/overview.md` — diseño, estado actual y trabajo futuro.
- `docs/adr/0004-alcance-rebanada-vertical.md` — recorte de alcance.
- `docs/adr/0005-orquestacion-multiagente-langgraph.md` — distinción entre agentes de plataforma y tooling de desarrollo.
- `docs/architecture/phi-and-security.md` — políticas PHI, legal y ética.
- `docs/psp/traceability.md` — vista de evidencia PSP.
