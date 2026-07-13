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
    assert result.modality == "mammography"
    assert 0.0 <= result.prediction.score <= 1.0


def test_stub_prediction_is_benign_placeholder():
    # El stub mock debe devolver score=0.1/benign (placeholder no clínico, B-013).
    from app.model import predict

    prediction = predict(None)
    assert prediction.score == 0.1
    assert prediction.label == "benign"
