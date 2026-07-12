# Runbook — Correr `mama-detector` en local

Guía operativa para levantar el sistema (backend con mocks) en una máquina de desarrollo. Incluye,
tal cual, los aprendizajes de la sesión de bootstrap del repo.

## Requisitos

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) como gestor de dependencias/entornos.
- Docker + Docker Compose (solo si se usa `just up`; no es obligatorio para correr tests).
- [`just`](https://github.com/casey/just) (opcional, pero recomendado — atajos de `justfile`).

## Aprendizaje: `uv` fuera del PATH

En esta máquina, `uv` está instalado en `~/.local/bin` y **no** está en el PATH global de Git
Bash. Antes de cualquier comando `uv` en una sesión nueva de Git Bash:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Sin esto, `uv: command not found`.

## Aprendizaje: `pythonpath` en cada servicio

Cada servicio (`services/mammography`, `services/histopathology`, `services/genomics`,
`services/fusion`, `services/gateway`) tiene en su `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

Esto es necesario porque los tests importan `app` (p. ej. `from app import model`) desde la raíz
del servicio. **Sin esta línea, `uv run pytest` falla con `ModuleNotFoundError: app`.** Si se crea
un servicio nuevo o se reestructura uno existente, hay que replicar esta configuración.

## Correr los tests de un servicio

Desde la raíz del repo (`W:\mama-detector`), por cada servicio:

```bash
export PATH="$HOME/.local/bin:$PATH"
cd services/mammography
uv sync --group dev
uv run pytest -q
```

Repetir `cd services/<nombre> && uv sync --group dev && uv run pytest -q` para
`histopathology`, `genomics`, `fusion` y `gateway`. Cada `pyproject.toml` declara
`mama-contracts` como dependencia editable apuntando a `packages/contracts` (vía
`[tool.uv.sources]`), así que `uv sync` la resuelve automáticamente en local.

Atajo con `just` (corre los 5 servicios en secuencia):

```bash
just test
```

Los contratos compartidos tienen su propia suite de tests (3 tests), que se ejecuta por separado:

```bash
cd packages/contracts
uv run pytest -q
```

Nota: `just test` solo corre la matriz de los 5 servicios (9 tests). Para una verificación completa, ejecutar ambos.

## Generar los contratos compartidos

Los modelos pydantic de `mama_contracts` se generan desde
`packages/contracts/schemas/models.json` (nunca se editan a mano — ver
[`architecture/contracts.md`](architecture/contracts.md)):

```bash
export PATH="$HOME/.local/bin:$PATH"
cd packages/contracts
./generate.sh
```

Atajo:

```bash
just gen-contracts
```

## Levantar todo el sistema con Docker Compose

```bash
just up
```

Equivale a `docker compose -f infra/docker-compose.yml up --build`. Levanta los 5 servicios
(`mammography`, `histopathology`, `genomics`, `fusion`, `gateway`) desde sus respectivos
`Dockerfile`; solo `gateway` publica puerto al host (`8080:8000`). Los demás se comunican por la
red interna de Compose usando el nombre del servicio como host
(`http://mammography:8000`, etc. — ver `services/gateway/app/config.py`).

## Alternativa sin Docker: 5 procesos `uv run uvicorn`

Si no se quiere levantar Docker, cada servicio puede correr como proceso local independiente
(ver también [`deployment/railway.md`](deployment/railway.md) para el equivalente en producción):

```bash
export PATH="$HOME/.local/bin:$PATH"
(cd services/mammography && uv run uvicorn app.main:app --port 8001) &
(cd services/histopathology && uv run uvicorn app.main:app --port 8002) &
(cd services/genomics && uv run uvicorn app.main:app --port 8003) &
(cd services/fusion && uv run uvicorn app.main:app --port 8004) &
(cd services/gateway && MAMMOGRAPHY_URL=http://localhost:8001 \
  HISTOPATHOLOGY_URL=http://localhost:8002 \
  GENOMICS_URL=http://localhost:8003 \
  FUSION_URL=http://localhost:8004 \
  uv run uvicorn app.main:app --port 8000) &
```

## Nota Windows: `git push`

**No** correr `git push` desde el Bash tool en este entorno (el compound
`export PATH=...; git push` queda bloqueado por permisos). Si hace falta pushear, usar PowerShell
directamente:

```powershell
git -C W:\mama-detector push
```

o dejar que lo haga el usuario.

## Ver también

- [`architecture/overview.md`](architecture/overview.md) — qué hace cada servicio.
- [`architecture/contracts.md`](architecture/contracts.md) — contratos compartidos.
- [`deployment/railway.md`](deployment/railway.md) — despliegue en Railway (borrador).
