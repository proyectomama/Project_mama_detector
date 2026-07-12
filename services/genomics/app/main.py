from fastapi import FastAPI
from mama_contracts import PredictRequest, ModalityResult
from app import model, preprocessing

app = FastAPI(title="genomics-service")

MODALITY = "genomics"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=ModalityResult)
def predict(req: PredictRequest) -> ModalityResult:
    tensor = preprocessing.preprocess(req.case_ref)
    prediction = model.predict(tensor)
    return ModalityResult(modality=MODALITY, prediction=prediction)
