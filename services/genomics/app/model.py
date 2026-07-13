"""Stub de inferencia. Devuelve un mock conforme al contrato."""
from mama_contracts import Prediction


def predict(_tensor) -> Prediction:
    # Placeholder no clínico: score bajo coherente con label="benign" (ver B-013).
    return Prediction(score=0.1, label="benign")
