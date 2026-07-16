import asyncio
import uuid

import httpx
from fastapi import FastAPI
from mama_contracts import (
    AnalyzeRequest,
    ModalityResult,
    FusionRequest,
    FusionResult,
    ClinicalAlert,
)
from app import config

app = FastAPI(title="gateway-service")


def _level(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


async def _predict(client: httpx.AsyncClient, url: str, case_ref: str) -> ModalityResult:
    resp = await client.post(f"{url}/predict", json={"case_ref": case_ref})
    resp.raise_for_status()
    return ModalityResult.model_validate(resp.json())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=ClinicalAlert)
async def analyze(req: AnalyzeRequest) -> ClinicalAlert:
    # `case_ref` es PHI: se usa solo internamente para consultar las modalidades.
    # Nunca aparece en la URL, en la respuesta ni en logs (RNF-001).
    case_ref = req.case_ref
    async with httpx.AsyncClient(timeout=30) as client:
        results = await asyncio.gather(*[
            _predict(client, url, case_ref) for url in config.MODALITY_URLS.values()
        ])
        fusion_req = FusionRequest(results=list(results))
        resp = await client.post(f"{config.FUSION_URL}/fuse", json=fusion_req.model_dump())
        resp.raise_for_status()
        fusion = FusionResult.model_validate(resp.json())
    # Identificador opaco generado server-side, no correlacionable con `case_ref`.
    analysis_id = uuid.uuid4().hex
    return ClinicalAlert(analysis_id=analysis_id, level=_level(fusion.score), fusion=fusion)
