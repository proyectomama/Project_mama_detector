# gateway — Contexto para Claude Code

Única superficie pública del sistema. Orquesta las 3 modalidades (`mammography`,
`histopathology`, `genomics`) en paralelo y el servicio `fusion`; los demás servicios son
internos y no deben exponerse.

- Endpoint: `POST /cases/{case_ref}/analyze` (`app/main.py`) — llama `POST /predict` en las 3
  modalidades vía `httpx`/`asyncio.gather`, arma un `FusionRequest`, llama `POST /fuse` en
  `fusion`, y devuelve un `ClinicalAlert` (nivel `low|medium|high` sobre el score fusionado).
- Consume `mama_contracts` (`ModalityResult`, `FusionRequest`, `FusionResult`, `ClinicalAlert`)
  generado desde `packages/contracts/schemas/*.json`. No editar contratos aquí.
- URLs de los servicios internos en `app/config.py` (`MODALITY_URLS`, `FUSION_URL`).
- `case_ref` y cualquier resultado de predicción son PHI: nunca loguearlos.
