# Levanta todo el sistema (backend con mocks) en local
up:
    docker compose -f infra/docker-compose.yml up --build

# Genera el código de contratos (pydantic) desde los schemas
gen-contracts:
    cd packages/contracts && ./generate.sh

# Corre los tests de todos los servicios Python
test:
    cd services/mammography && uv run pytest -q
    cd services/histopathology && uv run pytest -q
    cd services/genomics && uv run pytest -q
    cd services/fusion && uv run pytest -q
    cd services/gateway && uv run pytest -q
