# mammography — Contexto para Claude Code

Servicio de modalidad para mamografía 2D (`modality="mammography"`). Solo lo invoca el
`gateway`; no se expone al exterior.

- Endpoint: `POST /predict` (`app/main.py`) — recibe `PredictRequest{case_ref}`, corre
  `preprocessing.preprocess` + `model.predict`, devuelve `ModalityResult`.
- **La inferencia es un stub mock** en `app/model.py` (`Prediction(score=0.5, label="benign")`
  fijo). El modelo real (transfer learning sobre CBIS-DDSM + Grad-CAM) es RF-002/RF-003,
  trabajo futuro.
- Consume `mama_contracts` (`PredictRequest`, `ModalityResult`, `Prediction`) generado desde
  `packages/contracts/schemas/*.json`. No editar contratos aquí.
- `req.case_ref` y cualquier ruta DICOM son PHI: nunca loguearlos.
