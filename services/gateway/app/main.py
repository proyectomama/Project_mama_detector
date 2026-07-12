import asyncio

import httpx
from fastapi import FastAPI
from mama_contracts import ModalityResult, FusionRequest, FusionResult, ClinicalAlert
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


@app.post("/cases/{case_ref}/analyze", response_model=ClinicalAlert)
async def analyze(case_ref: str) -> ClinicalAlert:
    async with httpx.AsyncClient(timeout=30) as client:
        results = await asyncio.gather(*[
            _predict(client, url, case_ref) for url in config.MODALITY_URLS.values()
        ])
        fusion_req = FusionRequest(results=list(results))
        resp = await client.post(f"{config.FUSION_URL}/fuse", json=fusion_req.model_dump())
        resp.raise_for_status()
        fusion = FusionResult.model_validate(resp.json())
    return ClinicalAlert(case_ref=case_ref, level=_level(fusion.score), fusion=fusion)
