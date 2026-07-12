import httpx
import respx
from fastapi.testclient import TestClient
from mama_contracts import ClinicalAlert
from app.main import app
from app import config

client = TestClient(app)


def _modality_response(modality: str, score: float) -> httpx.Response:
    return httpx.Response(200, json={
        "modality": modality,
        "prediction": {"score": score, "label": "malignant" if score >= 0.5 else "benign"},
    })


@respx.mock
def test_analyze_orchestrates_modalities_and_fusion():
    respx.post(f"{config.MODALITY_URLS['mammography']}/predict").mock(
        return_value=_modality_response("mammography", 0.9))
    respx.post(f"{config.MODALITY_URLS['histopathology']}/predict").mock(
        return_value=_modality_response("histopathology", 0.9))
    respx.post(f"{config.MODALITY_URLS['genomics']}/predict").mock(
        return_value=_modality_response("genomics", 0.9))
    respx.post(f"{config.FUSION_URL}/fuse").mock(return_value=httpx.Response(200, json={
        "score": 0.9, "label": "malignant",
        "contributions": {"mammography": 0.9, "histopathology": 0.9, "genomics": 0.9},
    }))

    resp = client.post("/cases/CASE-1/analyze")
    assert resp.status_code == 200
    alert = ClinicalAlert.model_validate(resp.json())
    assert alert.case_ref == "CASE-1"
    assert alert.level == "high"
    assert alert.fusion.score == 0.9
