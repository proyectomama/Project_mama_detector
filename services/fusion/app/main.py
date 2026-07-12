from fastapi import FastAPI
from mama_contracts import FusionRequest, FusionResult
from app import strategy

app = FastAPI(title="fusion-service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/fuse", response_model=FusionResult)
def fuse(req: FusionRequest) -> FusionResult:
    return strategy.fuse(req)
