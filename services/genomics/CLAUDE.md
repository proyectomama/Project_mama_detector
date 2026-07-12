# genomics — Contexto para Claude Code

Servicio de modalidad para datos genómicos (`modality="genomics"`). Solo lo invoca el
`gateway`; no se expone al exterior.

- Endpoint: `POST /predict` (`app/main.py`) — recibe `PredictRequest{case_ref}`, corre
  `preprocessing.preprocess` + `model.predict`, devuelve `ModalityResult`.
- **La inferencia es un stub mock** en `app/model.py`: devuelve una `Prediction` conforme al
  contrato, sin modelo entrenado. Integración real con TCGA-BRCA/METABRIC queda **fuera del
  alcance** de la rebanada vertical del TG (restricción de presupuesto/hardware).
- Consume `mama_contracts` (`PredictRequest`, `ModalityResult`, `Prediction`) generado desde
  `packages/contracts/schemas/*.json`. No editar contratos aquí.
- `req.case_ref` es PHI: nunca loguearlo.
