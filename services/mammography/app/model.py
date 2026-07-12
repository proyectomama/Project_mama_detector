"""Stub de inferencia. Devuelve un mock conforme al contrato."""
from mama_contracts import Prediction


def predict(_tensor) -> Prediction:
    # TODO(modelo-real): reemplazar por inferencia real.
    return Prediction(score=0.5, label="benign")
