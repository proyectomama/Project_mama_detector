# fusion — Contexto para Claude Code

Combina los `ModalityResult` de las 3 modalidades en un resultado clínico único. Solo lo
invoca el `gateway`; no se expone al exterior.

- Endpoint: `POST /fuse` (`app/main.py`) — recibe `FusionRequest`, devuelve `FusionResult`.
- Estrategia actual (`app/strategy.py`): **mock**, promedio simple de los `score` de las 3
  modalidades; `label="malignant"` solo si el promedio **supera** 0.5 (`avg > 0.5`, umbral
  estricto no clínico — un promedio de 0.5 exacto es `benign`, ver B-013). Late/attention fusion
  es trabajo futuro (RF-005).
- Consume `mama_contracts` (`FusionRequest`, `FusionResult`) generado desde
  `packages/contracts/schemas/*.json`. No editar contratos aquí.
- No hay `app/model.py`: la "inferencia" de fusión vive en `strategy.py` y también es un stub.
