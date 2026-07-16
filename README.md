# mama-detector

Plataforma académica de apoyo a la detección temprana de cáncer de mama.
**No es un dispositivo médico certificado.**

## Alcance: arquitectura diseñada vs. implementación actual

Este repositorio distingue de forma explícita entre lo **diseñado** y lo **implementado**:

- **Arquitectura completa (diseñada):** sistema multimodal (mamografía 2D + histopatología +
  genómica), fusión multimodal, orquestación multiagente en runtime (LangGraph) e
  interoperabilidad clínica (DICOM/FHIR/SNOMED). Ver
  [`docs/architecture/overview.md`](docs/architecture/overview.md).
- **Implementación actual (mock):** cinco microservicios FastAPI (gateway + 3 modalidades +
  fusión) con **lógica de placeholder, sin modelos entrenados**. El gateway orquesta las
  modalidades y la fusión con predicciones fijas conformes al contrato. La rebanada vertical real
  (modelo CBIS-DDSM, Grad-CAM, agentes LangGraph, endpoint DICOM/FHIR/SNOMED, evaluación) es
  trabajo pendiente descrito en [`docs/roadmap-tg.md`](docs/roadmap-tg.md) y
  [`docs/alcance-vigente.md`](docs/alcance-vigente.md).

## Estructura del árbol actual

- `services/*` — microservicios FastAPI (gateway + 3 modalidades + fusión), hoy **mock**.
- `packages/contracts` — contratos compartidos (fuente de verdad de los tipos, JSON Schema →
  pydantic generado).
- `federated/` — andamiaje de aprendizaje federado (diseño/trabajo futuro).
- `infra/` — orquestación local (docker-compose).
- `docs/` — requisitos, arquitectura, ADRs, PSP, roadmap y alcance vigente.

### Dashboard (aún no vive en este árbol)

**No existe `apps/web` en este repositorio.** La interfaz de usuario está planificada como
**reutilización, en la medida de lo posible, de un dashboard existente**, no como un producto nuevo
creado desde cero. Todavía **no está incorporada a este árbol**; su integración es trabajo futuro
(ver [`docs/roadmap-tg.md`](docs/roadmap-tg.md)).

## Correr en local

```bash
just up      # levanta todo el sistema con mocks (docker-compose)
just test    # corre los tests de los servicios
```

Ver [`docs/runbook.md`](docs/runbook.md) para el detalle (`uv`, PATH y comandos por servicio).
