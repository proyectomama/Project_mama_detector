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
