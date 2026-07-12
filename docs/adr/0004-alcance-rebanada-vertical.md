# ADR-0004: Alcance de TG como rebanada vertical

## Estado

Aceptada

## Contexto

El profesor planteó la visión de un sistema multimodal, multiagente y basado en foundation
models, que combina mamografía 2D, histopatología y genómica, con aprendizaje federado entre
instituciones, despliegue en Kubernetes sobre GPU de alto rendimiento (tipo DGX), procesamiento
distribuido con Spark y Edge AI (ver `docs/anteproyecto/propuesta-alcance-tg.md`). El equipo
dispone de equipos personales y, a lo sumo, una GPU de gama de consumo y niveles gratuitos de
cómputo en la nube — infraestructura suficiente para hacer transfer learning sobre una modalidad
y correr una orquestación de agentes, pero muy lejos de lo necesario para entrenar foundation
models propios o montar entrenamiento distribuido, en un plazo de TG de ~4 meses.

## Decisión

Se diseña la arquitectura completa (las 3 modalidades, fusión multimodal, orquestación
multiagente, interoperabilidad clínica y aprendizaje federado) y se documenta con diagramas y
ADRs, pero solo se **implementa y valida** una rebanada vertical: clasificación de mamografía 2D
por transfer learning sobre CBIS-DDSM con explicabilidad Grad-CAM, orquestación multiagente con
LangGraph (Radiólogo, Patólogo, Gobernanza IA, Auditor regulatorio), un endpoint interoperable
DICOM/HL7 FHIR/SNOMED CT demostrable, y evaluación con las métricas clínicas objetivo
(sensibilidad, especificidad, AUC-ROC, precisión BI-RADS) frente al dataset de referencia. El
resto —foundation models propios, aprendizaje federado, histopatología y genómica con modelos
reales, Kubernetes/DGX, Spark, Edge AI— queda documentado en `docs/requisitos.md` y
`docs/architecture/overview.md` como trabajo futuro, explícitamente fuera del alcance del TG.

## Consecuencias

El TG entrega un artefacto demostrable y defendible dentro del cómputo disponible, con una
arquitectura completa diseñada que respalda la visión original del profesor sin comprometerse a
implementarla entera. El costo es que varios requisitos funcionales (RF-006 histopatología,
componentes de genómica, RF-007 interoperabilidad completa) quedan en estado `Propuesto` o
`Implementado (mock)` en el catálogo de requisitos en lugar de `Verificado`, y el equipo debe
comunicar con claridad — en la defensa del TG y en la documentación — la frontera exacta entre lo
diseñado y lo implementado, para evitar sobre-representar el alcance real ante el evaluador.
