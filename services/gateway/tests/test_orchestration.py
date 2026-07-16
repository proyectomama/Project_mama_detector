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

    resp = client.post("/analyze", json={"case_ref": "CASE-1"})
    assert resp.status_code == 200
    alert = ClinicalAlert.model_validate(resp.json())
    assert alert.level == "high"
    assert alert.fusion.score == 0.9


@respx.mock
def test_analyze_response_never_exposes_case_ref():
    for modality in ("mammography", "histopathology", "genomics"):
        respx.post(f"{config.MODALITY_URLS[modality]}/predict").mock(
            return_value=_modality_response(modality, 0.9))
    respx.post(f"{config.FUSION_URL}/fuse").mock(return_value=httpx.Response(200, json={
        "score": 0.9, "label": "malignant",
        "contributions": {"mammography": 0.9, "histopathology": 0.9, "genomics": 0.9},
    }))

    case_ref = "CASE-SECRET-123"
    resp = client.post("/analyze", json={"case_ref": case_ref})
    assert resp.status_code == 200
    body = resp.json()

    # RNF-001: el case_ref (PHI) no puede aparecer en la respuesta, ni por clave ni por valor.
    assert "case_ref" not in body
    assert case_ref not in resp.text

    # El servidor genera un analysis_id opaco, presente y distinto del case_ref.
    assert "analysis_id" in body
    assert body["analysis_id"]
    assert body["analysis_id"] != case_ref
