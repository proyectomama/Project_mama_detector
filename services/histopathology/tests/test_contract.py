from fastapi.testclient import TestClient
from mama_contracts import ModalityResult
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_predict_returns_valid_modality_result():
    resp = client.post("/predict", json={"case_ref": "CASE-1"})
    assert resp.status_code == 200
    result = ModalityResult.model_validate(resp.json())
    assert result.modality == "histopathology"
    assert 0.0 <= result.prediction.score <= 1.0
