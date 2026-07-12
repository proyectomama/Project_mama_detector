# ADR-0002: Contratos como JSON Schema, pydantic generado

## Estado

Aceptada

## Contexto

Los cinco servicios del sistema (`gateway`, `mammography`, `histopathology`, `genomics`,
`fusion`) intercambian mensajes estructurados (`Prediction`, `ModalityResult`, `PredictRequest`,
`FusionRequest`, `FusionResult`, `ClinicalAlert`) que deben mantenerse idénticos en todos los
servicios que los consumen. Escribir estos modelos a mano por separado en cada servicio, en
Python, es la vía más rápida a corto plazo pero garantiza divergencia: basta con que un servicio
actualice un campo y otro no para introducir un bug de contrato silencioso, especialmente
peligroso cuando esos contratos transportan campos considerados PHI (`case_ref`).

## Decisión

La fuente de verdad única de los contratos es un JSON Schema en
`packages/contracts/schemas/models.json`. De ahí se genera automáticamente, vía
`datamodel-codegen`, el módulo pydantic `packages/contracts/python/mama_contracts/models.py`, que
todos los servicios importan como el paquete `mama_contracts`. `models.py` nunca se edita a mano:
todo cambio de contrato se hace en el JSON Schema y se regenera con `./generate.sh` (o
`just gen-contracts`). El job `contracts-up-to-date` de CI (`.github/workflows/backend.yml`)
regenera el archivo en cada push/PR y falla si hay diff contra lo commiteado, haciendo estructuralmente
imposible mergear un `models.py` desincronizado del schema.

## Consecuencias

Los cinco servicios quedan garantizados en sincronía de contrato por construcción, y el flujo de
cambio de un modelo es explícito y auditable (editar schema → regenerar → revisar diff → commitear
schema y `models.py` juntos). El costo es un paso extra de tooling (`uv run datamodel-codegen`) en
el flujo de desarrollo y la disciplina de nunca tocar el archivo generado, aun cuando sea tentador
parchear un campo directamente en Python para ir más rápido; cualquier PR que lo haga será
rechazado por el chequeo de CI de diff.
