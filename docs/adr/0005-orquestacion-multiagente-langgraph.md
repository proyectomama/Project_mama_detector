# ADR-0005: Orquestación multiagente con LangGraph

## Estado

Aceptada

## Contexto

El profesor exige que el sistema sea explícitamente multiagente, no solo multimodal: el resultado
clínico fusionado debe pasar por un proceso de revisión equivalente al de un equipo clínico real,
con roles diferenciados de interpretación radiológica, correlación patológica, gobernanza de IA y
auditoría regulatoria. Hoy (`services/gateway/app/main.py`) la orquestación entre modalidades y
fusión es un mock HTTP simple: llamadas paralelas (`asyncio.gather`) a los servicios de modalidad
seguidas de una llamada secuencial a `fusion`, sin ningún agente interviniendo sobre el resultado.
Ese mock demuestra el flujo de datos pero no satisface el requisito de orquestación multiagente
sobre el caso clínico.

## Decisión

La orquestación multiagente del flujo clínico real se implementa con **LangGraph**, como grafo de
cuatro agentes — Radiólogo, Patólogo, Gobernanza IA y Auditor regulatorio — que reciben el
`FusionResult` y producen el `ClinicalAlert` final, incluyendo el disclaimer clínico obligatorio
(RNF-008). Estos cuatro agentes son **componentes de la plataforma** (runtime, en la nube) y son
**trabajo futuro**.

**No confundir con el tooling de desarrollo.** En `.claude/agents/` existen cuatro subagentes de
Claude Code con los mismos nombres (radiólogo, patólogo, gobernanza IA, auditor), pero son una cosa
distinta: **herramientas de desarrollo** que revisan el repositorio (código, PRs, documentación)
mientras se programa, y **no forman parte de la plataforma desplegada**. La coincidencia de nombres
es solo nominal —cada capa tiene responsabilidades distintas: los subagentes auditan el repo; los
agentes LangGraph intervienen en el análisis clínico de un caso real.

## Consecuencias

El gateway evolucionará de la orquestación HTTP simple actual (`main.py`) a un grafo LangGraph que
recibe el `FusionResult` y enruta la decisión a través de los cuatro agentes antes de emitir el
`ClinicalAlert`, lo que introduce estado y lógica condicional donde hoy solo hay llamadas HTTP
secuenciales/paralelas. Esto es trabajo pendiente (RF-004, hoy en estado "Implementado parcial")
y requiere definir, en una iteración futura, el esquema de mensajes entre agentes, sus criterios
de escalamiento (por ejemplo, cuándo Gobernanza IA o Auditor regulatorio deben elevar el nivel de
alerta) y cómo se testea un grafo de agentes de forma determinista para mantener la cobertura de
pruebas del proyecto.
