# Contratos compartidos (`packages/contracts`)

## Fuente de verdad

Los contratos de datos que comparten los 5 servicios (`gateway`, `mammography`, `histopathology`,
`genomics`, `fusion`) **no se escriben a mano en Python**. La fuente de verdad única es el JSON
Schema en:

```
packages/contracts/schemas/models.json
```

De ahí se **genera automáticamente** el módulo pydantic que todos los servicios importan como
`mama_contracts`:

```
packages/contracts/python/mama_contracts/models.py
```

La generación usa [`datamodel-codegen`](https://github.com/koxudaxi/datamodel-code-generator) vía
el script `packages/contracts/generate.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
uv run datamodel-codegen \
  --input schemas/models.json \
  --input-file-type jsonschema \
  --output python/mama_contracts/models.py \
  --output-model-type pydantic_v2.BaseModel \
  --use-standard-collections \
  --use-schema-description \
  --disable-timestamp
```

También invocable como `just gen-contracts` desde la raíz del repo (ver `justfile`).

## Regla dura: nunca editar `models.py` a mano

`python/mama_contracts/models.py` es **generado**. Cualquier cambio manual se pierde en la
siguiente regeneración y, peor, diverge silenciosamente del schema que los demás servicios asumen
como contrato. Si un modelo necesita cambiar, el cambio se hace en
`packages/contracts/schemas/models.json` y se regenera.

## CI verifica que no haya diff

El job `contracts-up-to-date` de `.github/workflows/backend.yml` regenera el archivo en cada push
y PR, y falla si hay diferencias contra lo commiteado:

```yaml
- name: Regenerar contratos y verificar que no hay diff
  working-directory: packages/contracts
  run: |
    uv sync --group dev
    ./generate.sh
    git diff --exit-code python/mama_contracts/models.py
```

Esto hace imposible mergear un `models.py` desincronizado del schema fuente.

## Los 7 modelos

Definidos en `packages/contracts/schemas/models.json` (`$defs`), consumidos vía
`from mama_contracts import ...`:

| Modelo | Rol | Campos clave |
|---|---|---|
| `Prediction` | Resultado atómico de un modelo de IA para un caso: score de riesgo y etiqueta. | `score` (0–1), `label` |
| `ModalityResult` | Envuelve la `Prediction` de una modalidad concreta. Es lo que devuelve cada servicio de modalidad en `POST /predict` y lo que el gateway junta antes de fusionar. | `modality` (`mammography`/`histopathology`/`genomics`), `prediction: Prediction` |
| `PredictRequest` | Petición de predicción que el gateway envía a cada servicio de modalidad (**red interna**). Referencia el caso por `case_ref` (PHI); a futuro incorporará la referencia al estudio DICOM/WSI. | `case_ref` |
| `AnalyzeRequest` | Petición pública que el cliente envía al gateway en `POST /analyze`. Lleva el `case_ref` (PHI) en el **cuerpo**, nunca en la URL (RNF-001). | `case_ref` |
| `FusionRequest` | Petición que el gateway envía a `fusion`: la lista de resultados de las modalidades ya predichas. | `results: list[ModalityResult]` |
| `FusionResult` | Resultado del servicio de fusión: score y label combinados, más el desglose de contribución por modalidad (hoy, el peso implícito del promedio). | `score`, `label`, `contributions: dict[str, float]` |
| `ClinicalAlert` | Salida final del gateway al cliente: un `analysis_id` **opaco generado server-side** (no expone `case_ref`, RNF-001), el nivel de alerta clínico y el resultado de fusión. Es donde debe vivir el disclaimer clínico (RNF-008) cuando se implemente. | `analysis_id`, `level` (`low`/`medium`/`high`), `fusion: FusionResult` |

## Tipo de estadificación TNM (diseñado, aún no en el schema)

RF-009 (#6) introduce un tipo de **estadificación TNM (AJCC 8)** en `models.json`. Todavía **no está
en el schema**: lo que sigue es el diseño acordado en
[`../adr/0006-estadificacion-tnm-ajcc8-pronostica.md`](../adr/0006-estadificacion-tnm-ajcc8-pronostica.md),
para que quien lo implemente no rehaga las decisiones. La fuente clínica es
[`../clinical/tnm.md`](../clinical/tnm.md).

**Campos:** `cT`/`cN`/`cM`, **grado Nottingham**, **RE**, **RP**, **HER2**, y **contexto de
tratamiento**.

**Reglas que el contrato debe hacer cumplir** — cada una corrige un error concreto:

| Regla | Por qué |
|---|---|
| **`cMX` no existe.** Las únicas categorías M válidas son `cM0`, `cM1`, `pM1`. Un contrato que acepte `cMX` está **mal formado**. `pM0` tampoco es válido: todo `M0` es clínico. | AJCC 8 no define `MX` para mama. |
| **`cNX` ≠ "no evaluado".** AJCC 8 lo reserva para cuando la **cuenca ganglionar fue extirpada**. Si nadie evaluó la axila, la categoría es **ausente** (`null`/`"unknown"`), no `cNX`. | `cN0` es una afirmación **positiva**: la evaluación se hizo y salió negativa. |
| **Dato ausente = `null`/`"unknown"`, nunca `X`.** | Ver las dos filas anteriores. |
| **`contexto de tratamiento` es obligatorio.** Decide si aplica la tabla **clínica** o la **patológica**. | Las dos tablas dan resultados **distintos** para la misma combinación: no es un detalle opcional. |
| **Sin valores por defecto para `cM0`/`cN0`.** Ante entrada obligatoria ausente → **"estadio no determinable"**. | Un `M0`/`N0` asumido por silencio convierte "no sabemos" en "no hay enfermedad": **fabrica un hallazgo clínico**. Es el modo de fallo más peligroso del tipo. |
| **`cT` estimado ≠ `pT`.** Si `cT` viene de imagen (RF-010), va marcado como **estimación radiológica** con incertidumbre y prefijo `c`. | El prefijo `p` exige pieza patológica. |
| **Casos sin grupo asignable** se representan explícitamente: grado nuclear (no Nottingham), posneoadyuvancia (`ypT`/`ypN`), respuesta patológica completa. | Forzar un valor sería inventar un estadio. |

**Origen del dato:** grado, RE, RP y HER2 entran como **dato estructurado del informe de patología** —
el sistema los **recibe**, no los infiere. El estadio pronóstico **no necesita un modelo**: necesita
**un campo en el contrato**. En particular, **RF-006 (histopatología) no es prerrequisito** de RF-009.

**PHI:** este tipo transporta datos clínicos sensibles. Aplican las mismas reglas que a `case_ref`
(ver más abajo y [`phi-and-security.md`](phi-and-security.md)): no se loguea.

## Flujo para agregar o cambiar un contrato

1. Editar `packages/contracts/schemas/models.json` (agregar/modificar el `$defs` correspondiente;
   respetar JSON Schema draft 2020-12).
2. Regenerar en local: `cd packages/contracts && ./generate.sh` (requiere `uv`; ver
   [`../runbook.md`](../runbook.md) para el PATH de `uv`).
3. Revisar el diff generado en `python/mama_contracts/models.py` — nunca tocarlo a mano.
4. Actualizar los servicios que consumen el modelo cambiado (`from mama_contracts import ...`).
5. Correr los tests de cada servicio afectado (`uv run pytest -q`).
6. Commitear schema + `models.py` regenerado juntos, en el mismo commit — así el job
   `contracts-up-to-date` de CI no encuentra diff.

## Relación con PHI

`case_ref` (dentro de `PredictRequest` y `AnalyzeRequest`) se trata como PHI en todo el sistema. A
partir de RNF-001, `case_ref` **no** viaja en la URL ni se devuelve al cliente: la salida
`ClinicalAlert` expone únicamente un `analysis_id` opaco generado server-side. Ver
[`phi-and-security.md`](phi-and-security.md) para las reglas de logging que aplican a estos
modelos.
