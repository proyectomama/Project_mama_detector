from mama_contracts import (
    Prediction, ModalityResult, PredictRequest, AnalyzeRequest,
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
        analysis_id="a1b2c3",
        level="low",
        fusion=FusionResult(score=0.5, label="benign", contributions={"mammography": 0.5}),
    )
    assert alert.fusion.label == "benign"


def test_clinical_alert_has_no_case_ref_field():
    # RNF-001: ClinicalAlert ya no expone case_ref (PHI); usa un analysis_id opaco.
    assert "case_ref" not in ClinicalAlert.model_fields
    assert "analysis_id" in ClinicalAlert.model_fields


def test_predict_and_fusion_requests_build():
    PredictRequest(case_ref="CASE-1")
    AnalyzeRequest(case_ref="CASE-1")
    FusionRequest(results=[
        ModalityResult(modality="genomics", prediction=Prediction(score=0.1, label="benign")),
    ])
