# Contribuir a mama-detector

Guía operativa para contribuir código o documentación a este repo. La gobernanza completa
(metodología, DoR/DoD, defectos) vive en [`docs/psp/`](docs/psp/); este documento es el flujo
práctico paso a paso.

## 0. Activar el hook de commits (una sola vez por clon)

El repo valida el formato de los mensajes de commit con un hook versionado. Activarlo antes del
primer commit:

```bash
git config core.hooksPath .githooks
```

Se puede verificar que funciona con:

```bash
bash .githooks/test-commit-msg.sh
```

## 1. Crear un issue

Todo cambio parte de un issue de GitHub creado con la plantilla correspondiente:

- **Tarea** (`.github/ISSUE_TEMPLATE/tarea.md`) — trabajo técnico sin valor de usuario directo.
- **Historia** (`.github/ISSUE_TEMPLATE/historia.md`) — funcionalidad con valor observable.
- **Defecto** (`.github/ISSUE_TEMPLATE/defecto.md`) — comportamiento incorrecto de código ya
  mergeado. **Sin PHI** en la descripción.

El issue debe cumplir la [Definition of Ready](docs/psp/definition-of-ready.md) (contexto,
objetivo, criterios de aceptación, trazabilidad a `RF-NNN`/`RNF-NNN`, label, asignado) antes de
empezar a trabajarlo.

## 2. Crear una rama

Desde `main` actualizado, con el nombre `tipo/descripcion-corta` (mismo catálogo de tipos que los
commits), sufijado con el número de issue si aplica:

```bash
git checkout -b feat/12-orquestacion-langgraph
```

## 3. Commits

Formato `tipo(#N): descripción`, en español, ≤72 caracteres, sin atribución a IA/Claude:

```
feat(#12): agrega orquestacion del gateway
fix(#34): corrige umbral BI-RADS en la fusion mock
docs: actualiza el runbook con el aprendizaje de pythonpath
```

`tipo` ∈ `feat | fix | chore | docs | refactor | style | test`. El hook `commit-msg` rechaza
cualquier mensaje que no matchee. Ver [`docs/psp/conventions.md`](docs/psp/conventions.md) para el
detalle completo.

**Sin atribución a IA — en ningún lado.** Todo es obra del equipo: ni commits, ni PRs, ni issues,
ni código/comentarios, ni documentación deben decir que lo hizo Claude, una IA, un "asistente" o
un "agente" (sin `Co-Authored-By: Claude`, sin `🤖 Generated with`). Antes de `git push`:

```bash
git log origin/main..HEAD --format='%B' | grep -i 'co-authored-by\|generated with' && echo "LIMPIAR ANTES DE PUSH" || echo "ok"
```

## 4. Correr los tests

Cada servicio tiene su propia suite (`uv run pytest`). Antes de la primera corrida en una sesión
nueva de Git Bash, `uv` puede no estar en el PATH — ver
[`docs/runbook.md`](docs/runbook.md) para el paso a paso completo (PATH de `uv`, `pythonpath`,
regeneración de contratos, comandos `just`).

## 5. Abrir el Pull Request

Contra `main`, usando `.github/pull_request_template.md` (se precarga automáticamente). El PR debe
cumplir la [Definition of Done](docs/psp/definition-of-done.md) completa:

- Tests pasan en cada servicio tocado.
- Contratos regenerados sin diff, si se tocó `packages/contracts`.
- Sin PHI en logs, respuestas, nombres de rama o mensajes de commit.
- Disclaimer clínico presente si la salida expone score, riesgo, BI-RADS o alerta.
- Trazabilidad actualizada en `docs/requisitos.md` y `docs/psp/traceability.md`.
- `Cierra #<issue>` en la descripción del PR.

## 6. Revisión

Al menos una revisión humana. Si el cambio afecta salida clínica o datos sensibles, además debe
pasar por el subagente de revisión correspondiente. Estos son **herramientas de desarrollo** de
Claude Code (revisan el repo mientras se programa) — **no** son el sistema multiagente de la
plataforma (ese es runtime/nube, trabajo futuro; ver `docs/adr/0005-orquestacion-multiagente-langgraph.md`).
Disponibles como slash commands en `.claude/commands/`:

| Comando | Cuándo usarlo |
|---|---|
| `/mama-radiologo` | Plausibilidad clínica de mamografía, BI-RADS, explicabilidad (Grad-CAM/XAI) |
| `/mama-patologo` | Correlación histopatológica, subtipos, biomarcadores |
| `/mama-gobernanza-ia` | Métricas objetivo, sesgo/equidad poblacional, calidad de XAI |
| `/mama-audit` | Trazabilidad, cumplimiento regulatorio/ético, PHI, DoD |

## 7. Merge

Solo cuando el PR cumple la Definition of Done completa y el CI pasa (tests + verificación de
contratos sin diff).

## Referencias

- [`docs/psp/psp-methodology.md`](docs/psp/psp-methodology.md) — metodología PSP adaptada, fase ↔ artefacto.
- [`docs/psp/conventions.md`](docs/psp/conventions.md) — convención de commits y ramas en detalle.
- [`docs/psp/definition-of-ready.md`](docs/psp/definition-of-ready.md) / [`docs/psp/definition-of-done.md`](docs/psp/definition-of-done.md)
- [`docs/psp/defect-log.md`](docs/psp/defect-log.md) — registro de defectos por fase.
- [`docs/runbook.md`](docs/runbook.md) — cómo correr y probar el sistema en local.
