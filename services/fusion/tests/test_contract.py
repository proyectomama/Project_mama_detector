from fastapi.testclient import TestClient
from mama_contracts import FusionResult
from app.main import app

client = TestClient(app)

PAYLOAD = {
    "results": [
        {"modality": "mammography", "prediction": {"score": 0.8, "label": "malignant"}},
        {"modality": "histopathology", "prediction": {"score": 0.4, "label": "benign"}},
        {"modality": "genomics", "prediction": {"score": 0.6, "label": "malignant"}},
    ]
}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_fuse_averages_and_reports_contributions():
    resp = client.post("/fuse", json=PAYLOAD)
    assert resp.status_code == 200
    result = FusionResult.model_validate(resp.json())
    assert result.score == 0.6  # (0.8 + 0.4 + 0.6) / 3
    assert set(result.contributions) == {"mammography", "histopathology", "genomics"}


def test_borderline_average_is_benign():
    # Tres scores exactamente en 0.5 dan promedio 0.5. Con el umbral estricto
    # (avg > 0.5) el resultado es benign; con el antiguo (avg >= 0.5) sería
    # malignant. Este caso valida el cambio de umbral de B-013.
    payload = {
        "results": [
            {"modality": "mammography", "prediction": {"score": 0.5, "label": "benign"}},
            {"modality": "histopathology", "prediction": {"score": 0.5, "label": "benign"}},
            {"modality": "genomics", "prediction": {"score": 0.5, "label": "benign"}},
        ]
    }
    resp = client.post("/fuse", json=payload)
    assert resp.status_code == 200
    result = FusionResult.model_validate(resp.json())
    assert result.score == 0.5
    assert result.label == "benign"
