"""Estrategia de fusión mock: promedio simple de scores.
Se reemplazará por una fusión real (p. ej. late/attention fusion) más adelante.
"""
from mama_contracts import FusionRequest, FusionResult


def fuse(req: FusionRequest) -> FusionResult:
    scores = {r.modality: r.prediction.score for r in req.results}
    avg = sum(scores.values()) / len(scores) if scores else 0.0
    label = "malignant" if avg >= 0.5 else "benign"
    return FusionResult(score=avg, label=label, contributions=scores)
