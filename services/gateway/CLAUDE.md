# gateway — Contexto para Claude Code

Única superficie pública del sistema. Orquesta las 3 modalidades (`mammography`,
`histopathology`, `genomics`) en paralelo y el servicio `fusion`; los demás servicios son
internos y no deben exponerse.

- Endpoint: `POST /analyze` (`app/main.py`) — recibe `AnalyzeRequest{case_ref}` en el **cuerpo**
  (nunca en la URL, RNF-001), llama `POST /predict` en las 3 modalidades vía
  `httpx`/`asyncio.gather`, arma un `FusionRequest`, llama `POST /fuse` en `fusion`, y devuelve un
  `ClinicalAlert` con un `analysis_id` opaco generado server-side (nivel `low|medium|high` sobre el
  score fusionado). El `case_ref` **no** viaja en la respuesta.
- Consume `mama_contracts` (`AnalyzeRequest`, `ModalityResult`, `FusionRequest`, `FusionResult`,
  `ClinicalAlert`) generado desde `packages/contracts/schemas/*.json`. No editar contratos aquí.
- URLs de los servicios internos en `app/config.py` (`MODALITY_URLS`, `FUSION_URL`).
- `case_ref` (uso interno) y cualquier resultado de predicción son PHI: nunca loguearlos ni
  exponerlos en la respuesta.
