"""Stub de inferencia. Devuelve un mock conforme al contrato."""
from mama_contracts import Prediction


def predict(_tensor) -> Prediction:
    return Prediction(score=0.5, label="benign")
