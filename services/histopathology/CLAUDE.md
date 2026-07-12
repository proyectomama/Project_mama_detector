# histopathology — Contexto para Claude Code

Servicio de modalidad para histopatología (`modality="histopathology"`). Solo lo invoca el
`gateway`; no se expone al exterior.

- Endpoint: `POST /predict` (`app/main.py`) — recibe `PredictRequest{case_ref}`, corre
  `preprocessing.preprocess` + `model.predict`, devuelve `ModalityResult`.
- **La inferencia es un stub mock** en `app/model.py`: devuelve una `Prediction` conforme al
  contrato, sin modelo entrenado. Correlación real con BreakHis/TCGA-BRCA es RF-006, trabajo
  futuro (fuera del alcance vertical del TG).
- Consume `mama_contracts` (`PredictRequest`, `ModalityResult`, `Prediction`) generado desde
  `packages/contracts/schemas/*.json`. No editar contratos aquí.
- `req.case_ref` y cualquier ruta de WSI son PHI: nunca loguearlos.
