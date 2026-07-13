"""Estrategia de fusión mock: promedio simple de scores.
Se reemplazará por una fusión real (p. ej. late/attention fusion) más adelante.
"""
from mama_contracts import FusionRequest, FusionResult


def fuse(req: FusionRequest) -> FusionResult:
    scores = {r.modality: r.prediction.score for r in req.results}
    avg = sum(scores.values()) / len(scores) if scores else 0.0
    # Umbral mock no clínico: malignant solo si el promedio SUPERA 0.5 (avg > 0.5).
    # Un promedio de exactamente 0.5 es benign, evitando la contradicción de B-013.
    label = "malignant" if avg > 0.5 else "benign"
    return FusionResult(score=avg, label=label, contributions=scores)
