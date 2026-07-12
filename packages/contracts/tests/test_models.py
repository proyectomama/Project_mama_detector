from mama_contracts import (
    Prediction, ModalityResult, PredictRequest,
    FusionRequest, FusionResult, ClinicalAlert,
)


def test_modality_result_roundtrips():
    result = ModalityResult(
        modality="mammography",
        prediction=Prediction(score=0.5, label="benign"),
    )
    assert result.model_dump() == {
        "modality": "mammography",
        "prediction": {"score": 0.5, "label": "benign"},
    }


def test_clinical_alert_nests_fusion():
    alert = ClinicalAlert(
        case_ref="CASE-1",
        level="low",
        fusion=FusionResult(score=0.5, label="benign", contributions={"mammography": 0.5}),
    )
    assert alert.fusion.label == "benign"


def test_predict_and_fusion_requests_build():
    PredictRequest(case_ref="CASE-1")
    FusionRequest(results=[
        ModalityResult(modality="genomics", prediction=Prediction(score=0.1, label="benign")),
    ])
