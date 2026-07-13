# Track A — Arquitectura y documentación — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dejar el repo `mama-detector` con la arquitectura sana y la documentación técnica coherente, **sin** implementar modelos de IA, DICOM/FHIR runtime ni el grafo LangGraph (todo eso queda diseñado y documentado, no ejecutado).

**Architecture:** Dos partes. **Parte 1 (saneamiento):** corrige contradicciones y el riesgo de PHI del andamiaje mock. **Parte 2 (arquitectura documentada):** modela el contrato de dominio clínico y documenta —a nivel de diseño— la interoperabilidad, el grafo de agentes y los diagramas de arquitectura que faltan.

**Tech Stack:** JSON Schema + datamodel-code-generator (pydantic v2), FastAPI, pytest, Mermaid, Markdown.

## Global Constraints

- Repo: `W:\mama-detector` (independiente). Rama de trabajo: crear `docs/arquitectura-track-a` desde `main`.
- Commits en español `tipo: descripción` (o `tipo(#N): descripción` si hay issue). **Sin atribución a IA/Claude, sin `Co-Authored-By`.**
- Contratos: `packages/contracts/schemas/models.json` es la fuente de verdad. `python/mama_contracts/models.py` se **genera** con `just gen-contracts` (o `packages/contracts/generate.sh`); **nunca se edita a mano**. Tras regenerar, correr `git diff --exit-code` sobre el generado en CI debe pasar.
- `uv` no está en el PATH global: en Git Bash anteponer `export PATH="$HOME/.local/bin:$PATH"` antes de `uv`.
- Cada `pyproject.toml` de servicio ya lleva `[tool.pytest.ini_options] pythonpath = ["."]`.
- **PHI (RNF-001):** ningún `case_ref`, ruta/nombre de archivo, ni `result_json` puede aparecer en URL, logs, `stdout/stderr` ni en respuestas de API.
- **Alcance:** NO entrenar modelos, NO implementar validación DICOM real, emisión FHIR real ni runtime LangGraph. Solo arquitectura y documentación.

---

## PARTE 1 — Saneamiento (Fase 0)

### Task 1: Corregir el README (B-010)

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: nada.
- Produces: README que distingue lo implementado (mock) de lo diseñado, y no anuncia `apps/web` como existente.

- [ ] **Step 1: Reescribir `README.md`**

```markdown
# mama-detector

Plataforma académica de apoyo a la detección temprana de cáncer de mama.
**No es un dispositivo médico certificado.**

Sistema **diseñado** como multimodal (mamografía + histopatología + genómica) con fusión y
orquestación multiagente. **Implementado hoy:** andamiaje de microservicios con lógica *mock*
(sin modelos entrenados). Ver el alcance real en
[`docs/anteproyecto/propuesta-alcance-tg.md`](docs/anteproyecto/propuesta-alcance-tg.md) y el
estado por componente en [`docs/architecture/overview.md`](docs/architecture/overview.md).

## Estructura

- `services/*` — microservicios FastAPI: `gateway` (único público) + `mammography`,
  `histopathology`, `genomics`, `fusion` (internos). Lógica mock.
- `packages/contracts` — contratos compartidos (JSON Schema → pydantic generado; fuente de verdad).
- `infra/` — orquestación local (docker-compose).
- `federated/` — andamiaje de federated learning (diseño/futuro, sin código).
- `docs/` — arquitectura, ADRs, PSP, requisitos y anteproyecto.

> **Dashboard web (`apps/web`):** aún no existe en el árbol. Se reutilizará el design system del
> dashboard de OncoScan; su incorporación es un frente aparte (no incluido todavía).

## Correr en local

```bash
just up      # levanta el sistema (mock) con docker-compose
just test    # corre los tests de los servicios
```
```

- [ ] **Step 2: Verificar que no queda ninguna afirmación de `apps/web` como existente**

Run: `grep -n "apps/web" README.md`
Expected: solo la línea del bloque `>` que aclara que **no existe** todavía.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: README distingue implementado (mock) vs disenado y aclara apps/web inexistente"
```

---

### Task 2: Coherencia clínica del mock de fusión (B-013)

**Files:**
- Modify: `services/mammography/app/model.py`
- Modify: `services/histopathology/app/model.py`
- Modify: `services/genomics/app/model.py`
- Modify: `services/fusion/app/strategy.py`
- Test: `services/fusion/tests/test_contract.py` (añadir caso por defecto)

**Interfaces:**
- Consumes: `mama_contracts` (`Prediction`, `FusionRequest`, `FusionResult`).
- Produces: mocks coherentes — un caso por defecto sale `benign` tanto por modalidad como por fusión; el umbral de fusión deja de etiquetar el borde 0.5 como `malignant`.

- [ ] **Step 1: Escribir el test que fija la coherencia (falla primero)**

En `services/fusion/tests/test_contract.py`, añadir:
```python
def test_default_mock_case_is_coherently_benign():
    payload = {"results": [
        {"modality": "mammography", "prediction": {"score": 0.1, "label": "benign"}},
        {"modality": "histopathology", "prediction": {"score": 0.1, "label": "benign"}},
        {"modality": "genomics", "prediction": {"score": 0.1, "label": "benign"}},
    ]}
    result = FusionResult.model_validate(client.post("/fuse", json=payload).json())
    assert result.label == "benign"
```

- [ ] **Step 2: Correr y verificar que pasa (el umbral actual ya da benign para 0.1)**

Run: `cd services/fusion && uv run pytest -q`
Expected: PASS. (Este test ancla la coherencia; el cambio de raíz es en los stubs y el umbral, abajo.)

- [ ] **Step 3: Hacer coherentes los stubs de modalidad**

En cada uno de `services/{mammography,histopathology,genomics}/app/model.py`, cambiar el retorno mock a un valor inequívocamente benigno:
```python
def predict(_tensor) -> Prediction:
    # Mock NO clínico: valor placeholder inequívoco. Se reemplaza por inferencia real (RF-002).
    return Prediction(score=0.1, label="benign")
```

- [ ] **Step 4: Corregir el umbral de fusión para que el borde no sea maligno**

En `services/fusion/app/strategy.py`, cambiar la comparación:
```python
    label = "malignant" if avg > 0.5 else "benign"
```
(antes era `>= 0.5`). Mantener el resto igual.

- [ ] **Step 5: Correr los tests de fusión y de las 3 modalidades**

Run:
```bash
cd services/fusion && uv run pytest -q
cd ../mammography && uv run pytest -q
cd ../histopathology && uv run pytest -q
cd ../genomics && uv run pytest -q
```
Expected: PASS en los 4. (El test existente `test_fuse_averages_and_reports_contributions` usa payload 0.8/0.4/0.6 → avg 0.6 > 0.5 → sigue `malignant`; el nuevo caso por defecto → `benign`.)

- [ ] **Step 6: Actualizar la descripción del mock en `overview.md`**

En `docs/architecture/overview.md`, sección 3, actualizar la línea de `fusion` para reflejar `label = "malignant"` si el promedio **> 0.5** y que el caso por defecto (stubs) es coherentemente `benign`.

- [ ] **Step 7: Commit**

```bash
git add services/mammography/app/model.py services/histopathology/app/model.py services/genomics/app/model.py services/fusion/app/strategy.py services/fusion/tests/test_contract.py docs/architecture/overview.md
git commit -m "fix: coherencia clinica del mock de fusion (caso por defecto benigno, umbral > 0.5)"
```

---

### Task 3: Rediseñar `case_ref` para no exponer PHI (B-011, RNF-001)

**Files:**
- Modify: `packages/contracts/schemas/models.json`
- Regenerate: `packages/contracts/python/mama_contracts/models.py`
- Modify: `packages/contracts/python/mama_contracts/__init__.py`
- Modify: `services/gateway/app/main.py`
- Modify: `services/gateway/tests/test_orchestration.py`
- Modify: `packages/contracts/tests/test_models.py`
- Modify: `docs/architecture/overview.md` (endpoint), `docs/requisitos.md` (estado RNF-001)

**Interfaces:**
- Consumes: `mama_contracts`.
- Produces:
  - Nuevo `AnalyzeRequest{case_ref: str}` (el `case_ref` viaja en el **cuerpo**, no en la URL).
  - `ClinicalAlert` deja de exponer `case_ref` y expone `analysis_id: str` (opaco, generado server-side).
  - Gateway: `POST /analyze` (sin path param). No loguea `case_ref`.

- [ ] **Step 1: Editar el schema fuente**

En `packages/contracts/schemas/models.json`, dentro de `$defs`:

Añadir `AnalyzeRequest`:
```json
    "AnalyzeRequest": {
      "type": "object",
      "properties": { "case_ref": { "type": "string" } },
      "required": ["case_ref"]
    },
```
Reemplazar `ClinicalAlert` por (quita `case_ref`, añade `analysis_id`):
```json
    "ClinicalAlert": {
      "type": "object",
      "properties": {
        "analysis_id": { "type": "string" },
        "level": { "type": "string" },
        "fusion": { "$ref": "#/$defs/FusionResult" }
      },
      "required": ["analysis_id", "level", "fusion"]
    }
```

- [ ] **Step 2: Regenerar los modelos**

Run:
```bash
export PATH="$HOME/.local/bin:$PATH"
cd packages/contracts && ./generate.sh
```
Expected: `python/mama_contracts/models.py` ahora contiene `class AnalyzeRequest` y `ClinicalAlert` con `analysis_id` (sin `case_ref`).

- [ ] **Step 3: Exportar `AnalyzeRequest` en `__init__.py`**

En `packages/contracts/python/mama_contracts/__init__.py`, añadir `AnalyzeRequest` al import desde `.models` y al `__all__`.

- [ ] **Step 4: Reescribir el test del gateway (falla primero)**

Reemplazar el cuerpo de `services/gateway/tests/test_orchestration.py::test_analyze_orchestrates_modalities_and_fusion` para usar el nuevo endpoint y verificar ausencia de PHI:
```python
@respx.mock
def test_analyze_orchestrates_and_hides_phi():
    for modality in ("mammography", "histopathology", "genomics"):
        respx.post(f"{config.MODALITY_URLS[modality]}/predict").mock(
            return_value=_modality_response(modality, 0.9))
    respx.post(f"{config.FUSION_URL}/fuse").mock(return_value=httpx.Response(200, json={
        "score": 0.9, "label": "malignant",
        "contributions": {"mammography": 0.9, "histopathology": 0.9, "genomics": 0.9},
    }))

    resp = client.post("/analyze", json={"case_ref": "CASE-SECRETO-1"})
    assert resp.status_code == 200
    alert = ClinicalAlert.model_validate(resp.json())
    assert alert.level == "high"
    assert alert.analysis_id  # opaco, no vacío
    # Prueba negativa de PHI: el case_ref no puede aparecer en la respuesta
    assert "CASE-SECRETO-1" not in resp.text
```
(Ajustar el import a `from mama_contracts import ClinicalAlert` si no estaba.)

- [ ] **Step 5: Correr el test y verificar que falla**

Run: `cd services/gateway && uv run pytest -q`
Expected: FAIL (aún existe `/cases/{case_ref}/analyze`, no `/analyze`).

- [ ] **Step 6: Reescribir el endpoint del gateway**

En `services/gateway/app/main.py`:
```python
import asyncio
from uuid import uuid4

import httpx
from fastapi import FastAPI
from mama_contracts import AnalyzeRequest, ModalityResult, FusionRequest, FusionResult, ClinicalAlert
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
    # PHI: case_ref viaja en el cuerpo, no se loguea ni se devuelve. Se emite un id opaco.
    async with httpx.AsyncClient(timeout=30) as client:
        results = await asyncio.gather(*[
            _predict(client, url, req.case_ref) for url in config.MODALITY_URLS.values()
        ])
        fusion_req = FusionRequest(results=list(results))
        resp = await client.post(f"{config.FUSION_URL}/fuse", json=fusion_req.model_dump())
        resp.raise_for_status()
        fusion = FusionResult.model_validate(resp.json())
    return ClinicalAlert(analysis_id=uuid4().hex, level=_level(fusion.score), fusion=fusion)
```

- [ ] **Step 7: Actualizar el test de contratos**

En `packages/contracts/tests/test_models.py`, `test_clinical_alert_nests_fusion` construye hoy `ClinicalAlert(case_ref="CASE-1", level="low", ...)`. Cambiarlo a:
```python
def test_clinical_alert_nests_fusion():
    alert = ClinicalAlert(
        analysis_id="a1", level="low",
        fusion=FusionResult(score=0.5, label="benign", contributions={"mammography": 0.5}),
    )
    assert alert.fusion.label == "benign"
```

- [ ] **Step 8: Correr los tests (gateway + contratos) y verificar que pasan**

Run:
```bash
cd services/gateway && uv run pytest -q
cd ../../packages/contracts && uv run pytest -q
```
Expected: PASS en ambos.

- [ ] **Step 9: Actualizar docs (endpoint + estado de RNF-001)**

- `docs/architecture/overview.md`: cambiar toda referencia a `POST /cases/{case_ref}/analyze` por `POST /analyze` (cuerpo `AnalyzeRequest`, respuesta con `analysis_id`), y añadir una nota de que el `case_ref` no viaja en URL ni en la respuesta.
- `docs/requisitos.md`: cambiar el estado de **RNF-001** de `Propuesto` a `Implementado (parcial)` con nota: "`case_ref` fuera de URL y de respuesta; falta redacción de logs y signed URLs cuando existan datos reales."

- [ ] **Step 10: Commit**

```bash
git add packages/contracts services/gateway docs/architecture/overview.md docs/requisitos.md
git commit -m "fix: sacar case_ref de URL y respuesta; emitir analysis_id opaco (RNF-001)"
```

---

### Task 4: Documento de alcance vigente y reconciliación de la métrica (B-008 lado-repo)

**Files:**
- Create: `docs/alcance-vigente.md`
- Modify: `docs/requisitos.md` (RNF-002)

**Interfaces:**
- Consumes: `docs/auditoria-alineacion-profesor.md`, `docs/roadmap-tg.md`.
- Produces: un documento único de alcance vigente en el repo y un RNF-002 sin contradicción de métrica.

- [ ] **Step 1: Crear `docs/alcance-vigente.md`**

Debe contener, en Markdown:
- **Alcance implementado/validado (rebanada vertical):** mamografía 2D CBIS-DDSM + Grad-CAM + grafo LangGraph de 4 agentes + endpoint DICOM/FHIR/SNOMED + evaluación.
- **Diseñado y documentado como futuro:** foundation models, aprendizaje federado, histopatología/genómica reales, K8s/DGX/Spark/Edge.
- **Meta operativa acordada:** AUC-ROC **>=0.92** (acordada con el equipo/director, **pendiente de constancia** — enlazar a `docs/roadmap-tg.md` sección "Única evidencia pendiente").
- **Tarea clínica primaria:** triaje de hallazgo/malignidad en mamografía 2D; NO predicción de riesgo a 5 años.
- Enlaces a `roadmap-tg.md` y `auditoria-alineacion-profesor.md`.

- [ ] **Step 2: Reconciliar RNF-002 en `docs/requisitos.md`**

Reemplazar el texto de **RNF-002** para reflejar la meta vigente sin borrar el historial de la meta original:
```
| RNF-002 | Meta operativa **acordada (pendiente de constancia del director, ver docs/alcance-vigente.md)**: **AUC-ROC >=0.92** para el triaje de mamografía 2D sobre CBIS-DDSM. Las metas originales del profesor (sensibilidad >95%, especificidad >90%, AUC-ROC >0.97, recall >94%, precisión BI-RADS >93%) quedan como referencia aspiracional; el reporte de evaluación medirá y reportará estas métricas de forma honesta aunque no alcancen dichos umbrales. | Propuesto | `services/mammography` | — |
```

- [ ] **Step 3: Verificar que no quedan dos metas contradictorias sin contexto**

Run: `grep -rn "0.97\|>=0.92\|>0.97" docs/`
Expected: toda mención a 0.97 aparece explícitamente como "referencia aspiracional" o histórica; 0.92 es la meta vigente. Corregir cualquier mención suelta.

- [ ] **Step 4: Commit**

```bash
git add docs/alcance-vigente.md docs/requisitos.md
git commit -m "docs: documento de alcance vigente y reconciliacion de la meta AUC-ROC (0.92 vigente)"
```

---

## PARTE 2 — Arquitectura documentada

### Task 5: Modelar el contrato de dominio clínico (B-012, RF-008)

**Files:**
- Modify: `packages/contracts/schemas/models.json`
- Regenerate: `packages/contracts/python/mama_contracts/models.py`
- Modify: `packages/contracts/python/mama_contracts/__init__.py`
- Modify: `services/gateway/app/main.py` (construir el reporte mock)
- Modify: `services/gateway/tests/test_orchestration.py`
- Modify: `packages/contracts/tests/test_models.py`
- Modify: `docs/architecture/contracts.md`

**Interfaces:**
- Consumes: `mama_contracts`.
- Produces: `ClinicalAlert` enriquecido con campos clínicos mínimos. Tipos nuevos con enums restringidos. El gateway rellena valores mock que cumplen el contrato.
  - `TriageLevel` = enum `["low","medium","high"]`
  - `BiRads` = enum `["0","1","2","3","4","5","6"]`
  - `GovernanceStatus` = enum `["approved_for_display","needs_review","blocked"]`
  - `ModelProvenance` = `{name: str, version: str}`
  - `Explanation` = `{method: enum ["grad-cam"], available: bool, uri: str|null}`
  - `ClinicalAlert` = `{analysis_id, triage_level: TriageLevel, fusion, birads: BiRads|null, model_provenance, explanation, governance_status: GovernanceStatus, disclaimer: const}`

> Nota de diseño: los value sets clínicos exactos (semántica BI-RADS, códigos SNOMED) son
> **estructura**, pendientes de validación clínica. Este task fija la forma del contrato, no la
> verdad clínica. `level` (string libre) se reemplaza por `triage_level` (enum).

- [ ] **Step 1: Editar el schema fuente**

En `packages/contracts/schemas/models.json`, añadir a `$defs`:
```json
    "TriageLevel": { "type": "string", "enum": ["low", "medium", "high"] },
    "BiRads": { "type": "string", "enum": ["0", "1", "2", "3", "4", "5", "6"] },
    "GovernanceStatus": { "type": "string", "enum": ["approved_for_display", "needs_review", "blocked"] },
    "ModelProvenance": {
      "type": "object",
      "properties": { "name": { "type": "string" }, "version": { "type": "string" } },
      "required": ["name", "version"]
    },
    "Explanation": {
      "type": "object",
      "properties": {
        "method": { "type": "string", "enum": ["grad-cam"] },
        "available": { "type": "boolean" },
        "uri": { "type": ["string", "null"] }
      },
      "required": ["method", "available", "uri"]
    },
```
Reemplazar `ClinicalAlert`:
```json
    "ClinicalAlert": {
      "type": "object",
      "properties": {
        "analysis_id": { "type": "string" },
        "triage_level": { "$ref": "#/$defs/TriageLevel" },
        "fusion": { "$ref": "#/$defs/FusionResult" },
        "birads": { "anyOf": [{ "$ref": "#/$defs/BiRads" }, { "type": "null" }] },
        "model_provenance": { "$ref": "#/$defs/ModelProvenance" },
        "explanation": { "$ref": "#/$defs/Explanation" },
        "governance_status": { "$ref": "#/$defs/GovernanceStatus" },
        "disclaimer": { "type": "string", "const": "No es un dispositivo médico certificado" }
      },
      "required": ["analysis_id", "triage_level", "fusion", "birads", "model_provenance", "explanation", "governance_status", "disclaimer"]
    }
```

- [ ] **Step 2: Regenerar y exportar**

Run:
```bash
export PATH="$HOME/.local/bin:$PATH"
cd packages/contracts && ./generate.sh
```
Añadir a `__init__.py` (import + `__all__`): `TriageLevel`, `BiRads`, `GovernanceStatus`, `ModelProvenance`, `Explanation`.
Expected: `models.py` contiene los nuevos tipos y el `ClinicalAlert` enriquecido.

- [ ] **Step 3: Actualizar el test del gateway (falla primero)**

En `services/gateway/tests/test_orchestration.py`, extender las aserciones del test de análisis:
```python
    assert alert.triage_level == "high"
    assert alert.disclaimer == "No es un dispositivo médico certificado"
    assert alert.governance_status in ("approved_for_display", "needs_review", "blocked")
    assert alert.explanation.method == "grad-cam"
    assert alert.model_provenance.name  # no vacío
```
(Quitar la aserción antigua `alert.level`.)

- [ ] **Step 4: Correr y verificar que falla**

Run: `cd services/gateway && uv run pytest -q`
Expected: FAIL (el gateway aún construye el `ClinicalAlert` viejo).

- [ ] **Step 5: Construir el reporte mock en el gateway**

En `services/gateway/app/main.py`, reemplazar el `return` de `analyze` (y los imports de contratos):
```python
from mama_contracts import (
    AnalyzeRequest, ModalityResult, FusionRequest, FusionResult,
    ClinicalAlert, ModelProvenance, Explanation,
)
...
    return ClinicalAlert(
        analysis_id=uuid4().hex,
        triage_level=_level(fusion.score),
        fusion=fusion,
        birads=None,  # mock: sin modelo no se afirma BI-RADS
        model_provenance=ModelProvenance(name="mock", version="0.0.0"),
        explanation=Explanation(method="grad-cam", available=False, uri=None),
        governance_status="needs_review",  # mock: nada aprobado para display sin modelo real
        disclaimer="No es un dispositivo médico certificado",
    )
```
(`_level` ya devuelve `low|medium|high`, compatible con `TriageLevel`.)

- [ ] **Step 6: Actualizar el test de contratos para el `ClinicalAlert` enriquecido**

En `packages/contracts/tests/test_models.py`, actualizar `test_clinical_alert_nests_fusion` (y los imports) para el nuevo contrato:
```python
from mama_contracts import (
    Prediction, ModalityResult, PredictRequest, FusionRequest, FusionResult,
    ClinicalAlert, ModelProvenance, Explanation,
)

def test_clinical_alert_nests_fusion():
    alert = ClinicalAlert(
        analysis_id="a1",
        triage_level="low",
        fusion=FusionResult(score=0.1, label="benign", contributions={"mammography": 0.1}),
        birads=None,
        model_provenance=ModelProvenance(name="mock", version="0.0.0"),
        explanation=Explanation(method="grad-cam", available=False, uri=None),
        governance_status="needs_review",
        disclaimer="No es un dispositivo médico certificado",
    )
    assert alert.fusion.label == "benign"
```

- [ ] **Step 7: Correr los tests (gateway + contratos) y verificar que pasan**

Run:
```bash
cd services/gateway && uv run pytest -q
cd ../../packages/contracts && uv run pytest -q
```
Expected: PASS en ambos.

- [ ] **Step 8: Documentar el contrato en `docs/architecture/contracts.md`**

Añadir una sección "Contrato de dominio clínico" que liste cada tipo nuevo, su enum/forma, y la nota de que los value sets clínicos (BI-RADS, SNOMED) son estructura pendiente de validación clínica. Marcar que `disclaimer` es constante (RNF-008) y `governance_status`/`explanation` habilitan RF-004/RF-003 a futuro.

- [ ] **Step 9: Commit**

```bash
git add packages/contracts services/gateway docs/architecture/contracts.md
git commit -m "feat: contrato de dominio clinico (triage_level, birads, gobernanza, provenance, disclaimer)"
```

---

### Task 6: Especificación de interoperabilidad DICOM/FHIR/SNOMED (B-004 diseño, RF-001/007)

**Files:**
- Create: `docs/architecture/interoperability.md`
- Modify: `docs/architecture/overview.md` (enlace)

**Interfaces:**
- Consumes: contrato de Task 5.
- Produces: especificación de diseño (sin runtime) del endpoint interoperable.

- [ ] **Step 1: Crear `docs/architecture/interoperability.md`**

Debe contener:
- **Entrada DICOM:** qué se valida antes de aceptar un estudio (SOP Class UID de mamografía, Transfer Syntax soportadas, presencia de píxel data, límite de tamaño), y qué se extrae (solo lo necesario para inferencia; nada de PHI a logs). Un ejemplo de tabla de tags mínimos.
- **Salida FHIR:** un `DiagnosticReport` con `Observation` embebida; el `Observation.code` y el hallazgo se codifican en **SNOMED CT**; el `triage_level`/`birads`/`disclaimer` del contrato clínico se mapean a campos FHIR. Incluir un ejemplo JSON de `DiagnosticReport` conforme (mock, con `analysis_id`, sin PHI).
- **Mapeo contrato→FHIR:** tabla `ClinicalAlert` (Task 5) → recurso/campo FHIR.
- **Alcance:** demostrable académicamente, sin conexión a hospital real; runtime = trabajo futuro (RF-001, RF-007).

- [ ] **Step 2: Enlazar desde `overview.md`**

En `docs/architecture/overview.md` sección 5 (Enlaces), añadir `interoperability.md`.

- [ ] **Step 3: Commit**

```bash
git add docs/architecture/interoperability.md docs/architecture/overview.md
git commit -m "docs: especificacion de interoperabilidad DICOM/FHIR/SNOMED (diseno, RF-001/007)"
```

---

### Task 7: Diseño del grafo multiagente LangGraph (B-003 diseño, RF-004)

**Files:**
- Create: `docs/architecture/agent-graph.md`
- Modify: `docs/adr/0005-orquestacion-multiagente-langgraph.md` (enlace al diseño detallado)

**Interfaces:**
- Consumes: contrato de Task 5 (`governance_status`, `explanation`, `triage_level`).
- Produces: diseño del grafo (sin implementación runtime).

- [ ] **Step 1: Crear `docs/architecture/agent-graph.md`**

Debe contener:
- **Estado compartido** del grafo (schema del estado: `analysis_id`, entradas por modalidad, hallazgos por agente, decisión, razones/traza).
- **Los 4 agentes** con responsabilidad mínima y criterios **deterministas** de salida (Radiólogo, Patólogo, Gobernanza IA, Auditor regulatorio — tabla igual a la del `roadmap-tg.md` Fase 3).
- **Reglas de abstención/escalamiento** y **gating de emisión** (el Auditor bloquea si falta disclaimer/traza/seguridad → `governance_status = blocked`).
- **Restricción sobre LLM:** si se usa, solo para explicación anclada a artefactos estructurados; no puede alterar una predicción sin regla explícita y testeable.
- **Diagrama de máquina de estados en Mermaid** (`stateDiagram-v2`) con los nodos de los 4 agentes, transiciones nominales, abstención, falta de evidencia y bloqueo de emisión.

- [ ] **Step 2: Enlazar desde el ADR-0005**

En `docs/adr/0005-orquestacion-multiagente-langgraph.md`, añadir una referencia a `../architecture/agent-graph.md` como el diseño detallado (el ADR mantiene la decisión; el nuevo doc mantiene el diseño).

- [ ] **Step 3: Commit**

```bash
git add docs/architecture/agent-graph.md docs/adr/0005-orquestacion-multiagente-langgraph.md
git commit -m "docs: diseno del grafo multiagente LangGraph con maquina de estados (RF-004)"
```

---

### Task 8: Completar los diagramas de arquitectura y la coherencia (Fase 5 docs)

**Files:**
- Create: `docs/architecture/sequence-analysis.md`
- Create: `docs/architecture/data-model.md`
- Modify: `docs/architecture/overview.md` (tabla de mapeo + enlaces)

**Interfaces:**
- Consumes: Tasks 3, 5, 6, 7 (endpoint, contrato clínico, interop, grafo).
- Produces: diagramas de secuencia y modelo de datos, y un `overview.md` coherente con el estado post-saneamiento.

- [ ] **Step 1: Crear `docs/architecture/sequence-analysis.md`**

Diagrama de secuencia Mermaid (`sequenceDiagram`) del flujo de análisis actualizado: Cliente → `POST /analyze` (cuerpo `AnalyzeRequest`) → gateway llama en paralelo a las 3 modalidades → fusión → construcción del `ClinicalAlert` clínico (con `analysis_id`, disclaimer, governance_status) → respuesta. Incluir la nota de que el `case_ref` no sale del gateway. Marcar dónde intervendrá el grafo de agentes (Task 7) a futuro.

- [ ] **Step 2: Crear `docs/architecture/data-model.md`**

Diagrama Mermaid (`erDiagram` o `classDiagram`) de los tipos de `packages/contracts` tras Task 5: `AnalyzeRequest`, `Prediction`, `ModalityResult`, `FusionRequest`, `FusionResult`, `ClinicalAlert`, `ModelProvenance`, `Explanation`, y los enums. Señalar cuáles campos son PHI y no deben exponerse.

- [ ] **Step 3: Actualizar la tabla de mapeo y enlaces en `overview.md`**

- Actualizar la fila del Gateway (endpoint `POST /analyze`, contrato clínico) y la de Contratos (dominio clínico modelado) en la tabla de la sección 4.
- Añadir a la sección 5 los enlaces a `sequence-analysis.md`, `data-model.md`, `interoperability.md`, `agent-graph.md`.

- [ ] **Step 4: Verificar coherencia global de docs**

Run: `grep -rn "cases/{case_ref}\|/cases/" docs/ services/`
Expected: **sin resultados** (ninguna referencia al endpoint viejo con PHI en la URL).

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/sequence-analysis.md docs/architecture/data-model.md docs/architecture/overview.md
git commit -m "docs: diagramas de secuencia y modelo de datos; overview coherente post-saneamiento"
```

---

## Cierre

- [ ] **Correr toda la batería y verificar verde**

Run:
```bash
export PATH="$HOME/.local/bin:$PATH"
just test
cd packages/contracts && uv run pytest -q
git diff --exit-code packages/contracts/python/mama_contracts/models.py
```
Expected: todos los tests PASS y el generado sin diff contra el schema.

- [ ] **Abrir PR de la rama `docs/arquitectura-track-a` a `main`** (o merge según el flujo del equipo).

## Notas de ejecución

- **Orden:** Parte 1 (Tasks 1-4) antes que Parte 2. Task 5 depende de que Task 3 ya haya movido `ClinicalAlert` a `analysis_id`. Tasks 6-8 dependen de Task 5.
- **Doble regeneración de contratos:** Task 3 y Task 5 editan el schema; en ambas hay que correr `generate.sh` y no editar `models.py` a mano.
- **Sin runtime clínico:** este plan no entrena ni implementa DICOM/FHIR/LangGraph reales. Si un test o doc empieza a exigir eso, está fuera del track A.
