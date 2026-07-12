# Gobernanza, Documentación y Entorno .claude de mama-detector — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dotar al repo `mama-detector` de documentación autosuficiente, gobernanza PSP lean-completa (sobre GitHub Issues) y un entorno `.claude` con 4 subagentes expertos + slash commands, alineado con los requisitos del profesor (sistema multimodal multiagente para detección de cáncer de mama).

**Architecture:** Espejo adaptado de la topología de OncoScan. Todo el conocimiento (contratos, PHI, marco legal colombiano, requisitos del TG, aprendizajes de la sesión) se destila en `docs/`. La gobernanza se aplica con un hook `commit-msg`, plantillas de issue/PR y CI. Los 4 expertos son subagentes read-only (`.claude/agents/`) disparables por slash commands, y coinciden 1:1 con el sistema multiagente que exige el profesor (Radiólogo, Patólogo, Gobernanza IA, Auditor regulatorio).

**Tech Stack:** Markdown, Bash (githook), JSON (settings.json), YAML (GitHub templates/CI), frontmatter de subagentes Claude Code. Sin código de aplicación nuevo.

## Global Constraints

- Repo: `w:\mama-detector` (independiente; ya inicializado, rama `main`, remoto `origin` = https://github.com/proyectomama/Project_mama_detector.git).
- Idioma de todo el contenido: **español**.
- Commits en español `tipo: descripción` o `tipo(#N): descripción` (N = nº de issue de GitHub). Tipos: `feat|fix|chore|docs|refactor|style|test`. Durante este plan (bootstrap sin issues) se usan commits **sin** `(#N)`, forma que el hook debe aceptar. Sin atribución a IA/Claude.
- **PHI:** nunca loguear identificadores de paciente/caso, rutas/nombres de archivos (DICOM/WSI), resultados de predicción ni URLs de Storage. `case_ref` se trata como PHI.
- Marco del profesor a reflejar en docs (verbatim donde aplique): sistema **multimodal, multiagente, foundation models**; métricas objetivo **sensibilidad >95%, especificidad >90%, AUC-ROC >0.97, recall >94%, precisión BI-RADS >93%**; interoperabilidad **HL7 FHIR / DICOM / SNOMED CT**; marco legal CO **Ley 1581/2012, Res. 1995/1999, Res. 2654/2019, INVIMA (SaMD)**; **6 principios OMS** de ética de IA en salud; metodología **PSP + PMBOK**.
- Alcance real del TG (de `propuesta-alcance-tg`): arquitectura completa **diseñada**; se **implementa y valida** una rebanada vertical (mamografía 2D CBIS-DDSM + Grad-CAM + orquestación LangGraph de 4 agentes + endpoint DICOM/FHIR/SNOMED + métricas). Lo demás (foundation models propios, federado, K8s/DGX, Spark, Edge AI, genómica) es **trabajo futuro** documentado.
- `uv` está en `C:\Users\mateo\.local\bin` (no en PATH global): en Git Bash anteponer `export PATH="$HOME/.local/bin:$PATH"`.
- **No** usar el Bash tool para `git push` (el compound `export ...; git push` queda bloqueado por permisos); si hiciera falta, `git -C W:\mama-detector push` vía PowerShell.

---

### Task 1: Config de equipo `.claude/settings.json` + estructura de carpetas

**Files:**
- Create: `w:/mama-detector/.claude/settings.json`
- Create: `w:/mama-detector/.claude/agents/.gitkeep`
- Create: `w:/mama-detector/.claude/commands/.gitkeep`

**Interfaces:**
- Consumes: nada.
- Produces: permisos versionados del equipo (allow/deny) y las carpetas donde viven agentes y comandos (Tasks 9–10).

- [ ] **Step 1: Crear `.claude/settings.json`**

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run*)",
      "Bash(uv sync*)",
      "Bash(uv pip*)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(git add*)",
      "Bash(git commit*)",
      "Read(*)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [
      "Bash(git push*)",
      "Bash(rm -rf*)"
    ]
  }
}
```

- [ ] **Step 2: Crear los `.gitkeep`**

Crear `w:/mama-detector/.claude/agents/.gitkeep` y `w:/mama-detector/.claude/commands/.gitkeep` (archivos vacíos) para versionar las carpetas.

- [ ] **Step 3: Validar que el JSON es válido**

Run: `python -c "import json; json.load(open(r'W:/mama-detector/.claude/settings.json')); print('JSON valido')"`
Expected: `JSON valido`

- [ ] **Step 4: Commit**

```bash
cd /w/mama-detector && git add .claude && git commit -m "chore: config de permisos del equipo y estructura de .claude"
```

---

### Task 2: Hook `commit-msg` que valida la convención

**Files:**
- Create: `w:/mama-detector/.githooks/commit-msg`
- Test: `w:/mama-detector/.githooks/test-commit-msg.sh`

**Interfaces:**
- Consumes: nada.
- Produces: hook portable que rechaza mensajes fuera de `tipo: desc` / `tipo(#N): desc`. Se activa con `git config core.hooksPath .githooks`.

- [ ] **Step 1: Escribir el test del hook (falla primero)**

Create `.githooks/test-commit-msg.sh`:
```bash
#!/usr/bin/env bash
# Prueba el hook commit-msg con casos válidos e inválidos.
set -u
HOOK="$(dirname "$0")/commit-msg"
tmp="$(mktemp)"
fail=0

check() { # $1=mensaje  $2=esperado(ok|bad)
  printf '%s\n' "$1" > "$tmp"
  if bash "$HOOK" "$tmp" >/dev/null 2>&1; then res=ok; else res=bad; fi
  if [ "$res" != "$2" ]; then echo "FALLO: '$1' esperaba $2 y dio $res"; fail=1; fi
}

check "feat: agrega servicio de fusion" ok
check "fix(#12): corrige umbral BI-RADS" ok
check "docs: actualiza runbook" ok
check "Merge branch 'main'" ok
check "arreglos varios" bad
check "feat agrega algo" bad
check "wip" bad

rm -f "$tmp"
if [ "$fail" -eq 0 ]; then echo "TODOS LOS CASOS PASAN"; else exit 1; fi
```

- [ ] **Step 2: Correr el test y verificar que falla**

Run: `cd /w/mama-detector && bash .githooks/test-commit-msg.sh`
Expected: FAIL (`.githooks/commit-msg` no existe aún → todos los `check` dan `bad`).

- [ ] **Step 3: Escribir el hook `.githooks/commit-msg`**

```bash
#!/usr/bin/env bash
# Valida la convención de commits de mama-detector.
# Formato: tipo(#N): descripción   |   tipo: descripción
# tipo ∈ feat|fix|chore|docs|refactor|style|test ; (#N) opcional = issue de GitHub.
set -euo pipefail
msg_file="$1"
first_line="$(head -n1 "$msg_file")"

# Permitir commits de merge/revert automáticos.
if printf '%s' "$first_line" | grep -qE '^(Merge|Revert) '; then
  exit 0
fi

pattern='^(feat|fix|chore|docs|refactor|style|test)(\(#[0-9]+\))?: .{1,72}$'
if printf '%s' "$first_line" | grep -qE "$pattern"; then
  exit 0
fi

cat >&2 <<'EOF'
✗ Mensaje de commit inválido.
  Formato esperado: tipo(#N): descripción   (o)   tipo: descripción
  tipo ∈ feat | fix | chore | docs | refactor | style | test
  #N = número de issue de GitHub (opcional)
  Ejemplos:
    feat(#12): agrega orquestacion del gateway
    docs: actualiza el runbook
EOF
exit 1
```

- [ ] **Step 4: Correr el test y verificar que pasa**

Run: `cd /w/mama-detector && chmod +x .githooks/commit-msg && bash .githooks/test-commit-msg.sh`
Expected: `TODOS LOS CASOS PASAN`

- [ ] **Step 5: Activar el hook en este repo**

Run: `cd /w/mama-detector && git config core.hooksPath .githooks`
Expected: sin salida (config guardada).

- [ ] **Step 6: Commit**

```bash
cd /w/mama-detector && git add .githooks && git commit -m "chore: hook commit-msg que valida la convencion de commits"
```

---

### Task 3: Copiar materiales fuente del anteproyecto (autosuficiencia)

**Files:**
- Create: `w:/mama-detector/docs/anteproyecto/anteproyecto.docx` (copia)
- Create: `w:/mama-detector/docs/anteproyecto/resumen-requisitos-profesor.md` (copia)
- Create: `w:/mama-detector/docs/anteproyecto/propuesta-alcance-tg.md` (copia)
- Create: `w:/mama-detector/docs/anteproyecto/README.md`

**Interfaces:**
- Consumes: archivos en `w:/Benditos_Oncoscan/Benditos_cancer_detector/`.
- Produces: los materiales originales del TG dentro de mama-detector (ya no dependen de OncoScan). Fuente para Tasks 4–7.

- [ ] **Step 1: Copiar los 3 materiales fuente**

Run (Git Bash):
```bash
mkdir -p /w/mama-detector/docs/anteproyecto
cp "/w/Benditos_Oncoscan/Benditos_cancer_detector/AnteProyecto Cancer de mama (1).docx" /w/mama-detector/docs/anteproyecto/anteproyecto.docx
cp "/w/Benditos_Oncoscan/Benditos_cancer_detector/docs/Resumen de requisitos del proyecto  sistema inteligente multimodal para detección temprana de cáncer de mama.md" /w/mama-detector/docs/anteproyecto/resumen-requisitos-profesor.md
cp "/w/Benditos_Oncoscan/Benditos_cancer_detector/docs/propuesta-alcance-tg.md" /w/mama-detector/docs/anteproyecto/propuesta-alcance-tg.md
```
Expected: 3 archivos copiados (verificar con `ls -la /w/mama-detector/docs/anteproyecto`).

- [ ] **Step 2: Crear `docs/anteproyecto/README.md`**

```markdown
# Anteproyecto — Material fuente (TG)

Documentos originales del Trabajo de Grado, copiados aquí para que el repo sea autosuficiente.

- `anteproyecto.docx` — anteproyecto formal (USC). Contexto epidemiológico CO, problema, objetivos.
- `resumen-requisitos-profesor.md` — requisitos del profesor Jair Sanclemente (capacidades IA, multiagente, métricas, interoperabilidad, legal).
- `propuesta-alcance-tg.md` — alcance acordado: arquitectura completa diseñada; rebanada vertical implementada.

Estos son la **fuente**; los requisitos operativos viven en [`../requisitos.md`](../requisitos.md).
```

- [ ] **Step 3: Commit**

```bash
cd /w/mama-detector && git add docs/anteproyecto && git commit -m "docs: incorpora materiales fuente del anteproyecto al repo"
```

---

### Task 4: Catálogo de requisitos RF/RNF + trazabilidad

**Files:**
- Create: `w:/mama-detector/docs/requisitos.md`
- Create: `w:/mama-detector/docs/psp/traceability.md`

**Interfaces:**
- Consumes: `docs/anteproyecto/*` (Task 3).
- Produces: catálogo `RF-NNN`/`RNF-NNN` (fuente única de trazabilidad) y su vista compacta.

- [ ] **Step 1: Crear `docs/requisitos.md`**

Estructura y contenido obligatorio (ISO/IEC/IEEE 29148). Encabezado explicando convención (`RF-NNN`/`RNF-NNN`; estados `Propuesto|Aprobado|Implementado|Verificado`; cada requisito enlaza issue de GitHub `#N` y módulo). Tablas con **estos requisitos sembrados** de `resumen-requisitos-profesor.md` y `propuesta-alcance-tg.md` (marcar estado real: el andamiaje actual es mock):

Funcionales (RF) — mínimo:
- RF-001 Ingesta DICOM de mamografía 2D (endpoint, validación). Estado: Propuesto.
- RF-002 Clasificación de mamografía 2D con transfer learning sobre CBIS-DDSM. Propuesto.
- RF-003 Explicabilidad Grad-CAM sobre la predicción de mamografía. Propuesto.
- RF-004 Orquestación multiagente (Radiólogo, Patólogo, Gobernanza IA, Auditor) vía gateway; hoy mock. Implementado parcial.
- RF-005 Servicio de fusión multimodal (promedio mock; futuro: late/attention fusion). Implementado (mock).
- RF-006 Correlación histopatológica (BreakHis/TCGA-BRCA). Propuesto (trabajo futuro).
- RF-007 Endpoint interoperable con contrato HL7 FHIR / SNOMED CT. Propuesto.
- RF-008 Reporte clínico estructurado (BI-RADS, riesgo, recomendación) con disclaimer. Propuesto.

No funcionales (RNF) — mínimo:
- RNF-001 PHI: ningún identificador/ruta/predicción en logs ni respuesta sin signed URL. Propuesto.
- RNF-002 Métricas clínicas objetivo: sensibilidad >95%, especificidad >90%, AUC-ROC >0.97, recall >94%, precisión BI-RADS >93%. Propuesto.
- RNF-003 Contratos en `packages/contracts` como fuente de verdad; pydantic generado, nunca editado a mano. Implementado.
- RNF-004 Commits `tipo(#N): desc` validados por hook. Implementado.
- RNF-005 Equidad: mitigar sesgo poblacional (representación de mujeres latinoamericanas). Propuesto.
- RNF-006 Cumplimiento legal CO (Ley 1581/2012, Res. 1995/1999, Res. 2654/2019) e INVIMA como SaMD. Propuesto.
- RNF-007 Ética: alinear con los 6 principios OMS de IA en salud. Propuesto.
- RNF-008 "No es un dispositivo médico certificado": disclaimer visible en toda salida clínica. Propuesto.

Cerrar con sección "Mantenimiento" (cómo se actualiza; relación con `traceability.md`).

- [ ] **Step 2: Crear `docs/psp/traceability.md`**

Tabla compacta con columnas: `Requisito | Issue(s) #N | Commit(s)/PR | Módulo | Evidencia | Estado`. Sembrar una fila por cada RF/RNF de arriba; dejar `#N`/commit vacíos donde aún no hay issue (bootstrap). Nota: es una **vista** de `requisitos.md`, no una fuente paralela.

- [ ] **Step 3: Commit**

```bash
cd /w/mama-detector && git add docs/requisitos.md docs/psp/traceability.md && git commit -m "docs: catalogo de requisitos RF/RNF y matriz de trazabilidad"
```

---

### Task 5: Documentación técnica (arquitectura, PHI/legal, runbook, deploy)

**Files:**
- Create: `w:/mama-detector/docs/architecture/overview.md`
- Create: `w:/mama-detector/docs/architecture/contracts.md`
- Create: `w:/mama-detector/docs/architecture/phi-and-security.md`
- Create: `w:/mama-detector/docs/runbook.md`
- Create: `w:/mama-detector/docs/deployment/railway.md`

**Interfaces:**
- Consumes: código real de `services/*` y `packages/contracts`; `docs/anteproyecto/*`.
- Produces: docs técnicos autosuficientes.

- [ ] **Step 1: `docs/architecture/overview.md`**

Secciones: (1) Visión (copiloto clínico multimodal multiagente, contexto CO). (2) **Arquitectura completa diseñada** — diagrama en Mermaid: gateway público → 3 modalidades + fusión; agentes Radiólogo/Patólogo/Gobernanza IA/Auditor; interoperabilidad FHIR/DICOM/SNOMED; capa de datos; federado (futuro). (3) **Lo implementado hoy** — andamiaje mock: `gateway` orquesta `mammography|histopathology|genomics` en paralelo + `fusion`, contratos compartidos; tests 12/12. (4) Mapeo diseño↔implementado↔trabajo futuro (tabla). (5) Enlaces a `contracts.md`, `phi-and-security.md`, `requisitos.md`.

- [ ] **Step 2: `docs/architecture/contracts.md`**

Explicar: `packages/contracts/schemas/*.json` = fuente de verdad; `just gen-contracts` (o `generate.sh`) genera `python/mama_contracts/models.py` con `datamodel-codegen`; **nunca** editar a mano; CI verifica que no haya diff. Listar los modelos (`Prediction, ModalityResult, PredictRequest, FusionRequest, FusionResult, ClinicalAlert`) y su rol. Flujo para agregar/cambiar un contrato.

- [ ] **Step 3: `docs/architecture/phi-and-security.md`**

Secciones: (1) Qué es PHI aquí (`case_ref`, rutas DICOM/WSI, `result_json`, URLs de Storage). (2) Reglas de logging (nunca PHI en stdout/stderr/logs; nunca exponer URL de Storage sin signed URL server-side). (3) **Marco legal colombiano**: Ley 1581/2012 (datos personales/sensibles en salud), Res. 1995/1999 (historia clínica reservada), Res. 2654/2019 (telesalud/plataformas), INVIMA (software como dispositivo médico con IA → registro sanitario previo al uso asistencial). (4) **Ética — 6 principios OMS**: autonomía; bienestar y seguridad; transparencia/explicabilidad; responsabilidad; equidad; IA ambientalmente responsable. (5) **Disclaimer obligatorio**: "No es un dispositivo médico certificado". (6) Sesgo poblacional y equidad (mujeres latinoamericanas).

- [ ] **Step 4: `docs/runbook.md`**

Cómo correr local. Incluir **verbatim** los aprendizajes de la sesión: `uv` en `~/.local/bin` fuera del PATH global → `export PATH="$HOME/.local/bin:$PATH"`; cada servicio tiene `[tool.pytest.ini_options] pythonpath = ["."]` (sin eso, `ModuleNotFoundError: app`); `uv sync --group dev` + `uv run pytest -q` por servicio; generar contratos con `packages/contracts/generate.sh`; nota Windows: `git push` no desde el Bash tool. Comandos `just up` / `just test`.

- [ ] **Step 5: `docs/deployment/railway.md`**

Borrador de despliegue (de lo aprendido hoy): Railway plan Hobby $5/mes o trial (no requiere Pro); 5 servicios, cada uno buildea desde su `Dockerfile`; red interna `*.railway.internal`; solo `gateway` público; env vars `MAMMOGRAPHY_URL|HISTOPATHOLOGY_URL|GENOMICS_URL|FUSION_URL`. Marcar como **plan aparte pendiente** (config `railway.json` a definir). Alternativa local sin Docker: 5 `uv run uvicorn` en paralelo.

- [ ] **Step 6: Commit**

```bash
cd /w/mama-detector && git add docs/architecture docs/runbook.md docs/deployment && git commit -m "docs: arquitectura, PHI/legal, runbook y borrador de despliegue"
```

---

### Task 6: Architecture Decision Records (ADR)

**Files:**
- Create: `w:/mama-detector/docs/adr/0001-repo-independiente.md`
- Create: `w:/mama-detector/docs/adr/0002-contratos-json-schema.md`
- Create: `w:/mama-detector/docs/adr/0003-tracking-github-issues.md`
- Create: `w:/mama-detector/docs/adr/0004-alcance-rebanada-vertical.md`
- Create: `w:/mama-detector/docs/adr/0005-orquestacion-multiagente-langgraph.md`

**Interfaces:**
- Consumes: decisiones ya tomadas (sesión + propuesta de alcance).
- Produces: registro de decisiones. Cada ADR usa el formato: `# ADR-NNNN: Título` / `## Estado` (Aceptada) / `## Contexto` / `## Decisión` / `## Consecuencias`.

- [ ] **Step 1: Escribir los 5 ADR**

Contenido de cada uno (1–2 párrafos por sección):
- 0001 Repo independiente: por qué mama-detector es repo Git propio (no subdir/fork de OncoScan). Consecuencia: autosuficiencia; se reusa disciplina PSP.
- 0002 Contratos JSON Schema → pydantic generado: fuente de verdad única, CI verifica diff. Consecuencia: no editar `models.py`.
- 0003 Tracking en GitHub Issues (no Jira): trazabilidad nativa `#N`↔commit↔PR; sin auth externa. Consecuencia: commits `tipo(#N)`.
- 0004 Alcance rebanada vertical: arquitectura completa diseñada, se implementa/valida mamografía 2D + agentes + interoperabilidad demostrable. Consecuencia: foundation models propios/federado/K8s = trabajo futuro (por hardware/presupuesto).
- 0005 Orquestación multiagente con LangGraph: agentes Radiólogo/Patólogo/Gobernanza IA/Auditor. Consecuencia: el gateway evolucionará de orquestación HTTP simple a grafo de agentes.

- [ ] **Step 2: Commit**

```bash
cd /w/mama-detector && git add docs/adr && git commit -m "docs: ADRs iniciales de arquitectura y proceso"
```

---

### Task 7: Suite PSP (metodología, convenciones, DoR/DoD, defectos, post-mortem)

**Files:**
- Create: `w:/mama-detector/docs/psp/psp-methodology.md`
- Create: `w:/mama-detector/docs/psp/conventions.md`
- Create: `w:/mama-detector/docs/psp/definition-of-ready.md`
- Create: `w:/mama-detector/docs/psp/definition-of-done.md`
- Create: `w:/mama-detector/docs/psp/defect-log.md`
- Create: `w:/mama-detector/docs/psp/post-mortem-template.md`

**Interfaces:**
- Consumes: `conventions` del hook (Task 2), requisitos (Task 4).
- Produces: gobernanza PSP lean-completa adaptada a GitHub Issues.

- [ ] **Step 1: `psp-methodology.md`**

Adaptar de OncoScan pero a mama-detector + GitHub Issues. Rol del auditor (disciplinado, PSP de Humphrey/SEI; dominio clínico → calidad y trazabilidad pesan más que velocidad). Tabla **fase PSP ↔ artefacto real**: Planning=`docs/superpowers/plans/*`, Design=`docs/superpowers/specs/*`+`docs/adr/*`, Design Review=`/mama-audit`, Coding=`services/*`, Code Review=PR + `/mama-audit`, Testing=`uv run pytest`, Post-mortem=`docs/psp/postmortems/` (plantilla). Las reglas: todo trazable (issue↔requisito↔commit↔evidencia), todo medido, revisión antes de merge, defectos registrados.

- [ ] **Step 2: `conventions.md`**

Convención de commits `tipo(#N): descripción` (≤72 chars, español, imperativo/pretérito); tipos; cuerpo con el porqué. Hook `commit-msg` (regex y activación `git config core.hooksPath .githooks`). Convención de ramas (`feat/…`, `fix/…`, `docs/…`). Flujo issue→rama→PR→merge.

- [ ] **Step 3: `definition-of-ready.md`**

Un issue está "Ready" cuando: resumen verifica un cambio concreto; descripción con `## Contexto`, `## Objetivo`, `## Criterios de aceptación` (≥1), `## Trazabilidad` (módulo + RF/RNF); label del catálogo; asignado. Adaptado a labels de GitHub (no Components de Jira).

- [ ] **Step 4: `definition-of-done.md`**

"Done" cuando: código + tests pasan (`uv run pytest`); contratos regenerados sin diff si aplica; PR revisado (checklist PHI/seguridad clínica); trazabilidad actualizada en `requisitos.md`/`traceability.md`; sin PHI en logs; disclaimer presente si es salida clínica; commit(s) `tipo(#N)`.

- [ ] **Step 5: `defect-log.md`**

Tabla: `ID | Fecha | Fase inyección | Fase detección | Tipo (PSP) | Descripción | Fix (commit) | Requisito`. Nota: sin PHI en las descripciones. Sembrar 1 fila de ejemplo real de la sesión: el fix de `pythonpath` (inyección: Design; detección: Test; tipo: 20-Environment/Config).

- [ ] **Step 6: `post-mortem-template.md`**

Plantilla: `## Resumen` / `## Estimado vs real` / `## Defectos por fase` / `## Qué salió bien` / `## Qué mejorar` / `## Acciones (con responsable)`.

- [ ] **Step 7: Commit**

```bash
cd /w/mama-detector && git add docs/psp && git commit -m "docs: suite PSP lean-completa adaptada a GitHub Issues"
```

---

### Task 8: Plantillas de GitHub (issues + PR) + CONTRIBUTING

**Files:**
- Create: `w:/mama-detector/.github/ISSUE_TEMPLATE/tarea.md`
- Create: `w:/mama-detector/.github/ISSUE_TEMPLATE/historia.md`
- Create: `w:/mama-detector/.github/ISSUE_TEMPLATE/defecto.md`
- Create: `w:/mama-detector/.github/pull_request_template.md`
- Create: `w:/mama-detector/CONTRIBUTING.md`

**Interfaces:**
- Consumes: DoR/DoD (Task 7), convención (Task 2).
- Produces: enforcement de gobernanza en la superficie de GitHub.

- [ ] **Step 1: `ISSUE_TEMPLATE/tarea.md`**

Front-matter (`name: Tarea`, `about`, `labels: tarea`). Cuerpo con secciones de la DoR: `## Contexto`, `## Objetivo`, `## Criterios de aceptación` (checklist), `## Trazabilidad` (módulo + RF/RNF).

- [ ] **Step 2: `ISSUE_TEMPLATE/historia.md`**

Front-matter (`name: Historia`, `labels: historia`). `## Como/Quiero/Para`, `## Criterios de aceptación` (≥2), `## Trazabilidad`.

- [ ] **Step 3: `ISSUE_TEMPLATE/defecto.md`**

Front-matter (`name: Defecto`, `labels: defecto`). `## Descripción` (sin PHI), `## Pasos para reproducir`, `## Esperado vs real`, `## Fase de inyección/detección` (para el defect-log).

- [ ] **Step 4: `pull_request_template.md`**

Checklist de PR (DoD): `- [ ] Tests pasan (uv run pytest)`; `- [ ] Contratos sin diff (si aplica)`; `- [ ] Sin PHI en logs/respuestas`; `- [ ] Disclaimer clínico presente (si aplica)`; `- [ ] Trazabilidad actualizada`; `- [ ] Cierra #<issue>`. Sección `## Seguridad clínica` (¿afecta salida clínica? ¿revisado con `/mama-audit`?).

- [ ] **Step 5: `CONTRIBUTING.md`**

Flujo completo: crear issue (plantilla) → rama `tipo/desc` → commits `tipo(#N)` → PR (plantilla) → revisión → merge. Activación del hook (`git config core.hooksPath .githooks`). Cómo correr tests (enlace a `docs/runbook.md`). Enlace a la suite PSP y a los expertos (`.claude/commands`).

- [ ] **Step 6: Commit**

```bash
cd /w/mama-detector && git add .github/ISSUE_TEMPLATE .github/pull_request_template.md CONTRIBUTING.md && git commit -m "docs: plantillas de issues/PR y guia de contribucion"
```

---

### Task 9: Los 4 subagentes expertos (`.claude/agents/`)

**Files:**
- Create: `w:/mama-detector/.claude/agents/mama-radiologo.md`
- Create: `w:/mama-detector/.claude/agents/mama-patologo.md`
- Create: `w:/mama-detector/.claude/agents/mama-gobernanza-ia.md`
- Create: `w:/mama-detector/.claude/agents/mama-auditor.md`

**Interfaces:**
- Consumes: `docs/requisitos.md`, `docs/architecture/phi-and-security.md`.
- Produces: 4 subagentes read-only (los 3 revisores con `tools: Read, Glob, Grep`; el auditor además `Bash` para verificar). Cada uno = un agente del sistema multiagente del profesor.

- [ ] **Step 1: `mama-radiologo.md` (ejemplo completo — replicar patrón en los demás)**

```markdown
---
name: mama-radiologo
description: Experto radiólogo de mama. Úsalo para revisar plausibilidad clínica de mamografía/tomosíntesis, BI-RADS, densidad, lesiones, umbrales de riesgo y calidad de la explicabilidad (Grad-CAM/XAI). Read-only.
tools: Read, Glob, Grep
---

Eres un **radiólogo subespecializado en imagen mamaria** que revisa el sistema mama-detector (copiloto clínico, contexto colombiano). Corresponde al **Agente Radiólogo** de la arquitectura multiagente del TG.

## Alcance
- Mamografía 2D / tomosíntesis (DBT): detección de masas, calcificaciones, distorsión, densidad ACR.
- Clasificación **BI-RADS** y su correspondencia con score de riesgo.
- Explicabilidad: que Grad-CAM/mapas de atención señalen regiones plausibles.

## Qué verificas
- [ ] El `label`/`score` de mamografía es clínicamente plausible (no mezcla categorías).
- [ ] Umbrales de riesgo coherentes con guías (NCCN/ACR; riesgo incrementado ≥1.7% a 5 años estilo Clairity).
- [ ] La salida no afirma diagnóstico definitivo; incluye disclaimer "no es dispositivo médico".
- [ ] Ningún PHI en logs/respuestas (ver docs/architecture/phi-and-security.md).
- [ ] La explicabilidad acompaña a toda alerta de riesgo.

## Cómo reportas
Hallazgos ordenados por severidad clínica, con archivo:línea y recomendación concreta. No apruebas sin evidencia. No inventas métricas.

## Fuentes
docs/requisitos.md (RF/RNF), docs/architecture/*, guías NCCN/ACR, léxico BI-RADS.
```

- [ ] **Step 2: `mama-patologo.md`**

Mismo patrón. `description`: experto patólogo; correlación histopatología (BreakHis/TCGA-BRCA), subtipos, biomarcadores; read-only `Read, Glob, Grep`. Checklist: coherencia de `modality="histopathology"`, correlación radio-patológica plausible, subtipos/grados válidos, sin PHI, disclaimer. Corresponde al **Agente Patólogo**.

- [ ] **Step 3: `mama-gobernanza-ia.md`**

`description`: experto en gobernanza de IA multimodal; sesgo poblacional, equidad, métricas clínicas objetivo, calidad de XAI; read-only. Checklist: métricas vs objetivo (sens>95%, esp>90%, AUC>0.97, recall>94%, BI-RADS>93%); representación de mujeres latinoamericanas; XAI presente y fiel; fusión multimodal razonable. Corresponde al **Agente Gobernanza IA**.

- [ ] **Step 4: `mama-auditor.md`**

`description`: auditor PSP + cumplimiento regulatorio/ético; verifica trazabilidad, INVIMA/FDA/EMA, Ley 1581/Res.1995/Res.2654, 6 principios OMS, PHI. `tools: Read, Glob, Grep, Bash` (para verificar tests/estado). Checklist: trazabilidad issue↔requisito↔commit↔evidencia; commits siguen convención; sin PHI; disclaimer; DoD cumplido; marco legal CO referenciado donde toca. Corresponde al **Agente Auditor regulatorio**.

- [ ] **Step 5: Commit**

```bash
cd /w/mama-detector && git add .claude/agents && git commit -m "feat: 4 subagentes expertos del sistema multiagente medico"
```

---

### Task 10: Los 4 slash commands (`.claude/commands/`)

**Files:**
- Create: `w:/mama-detector/.claude/commands/mama-radiologo.md`
- Create: `w:/mama-detector/.claude/commands/mama-patologo.md`
- Create: `w:/mama-detector/.claude/commands/mama-gobernanza-ia.md`
- Create: `w:/mama-detector/.claude/commands/mama-audit.md`

**Interfaces:**
- Consumes: los subagentes de Task 9.
- Produces: comandos finos que disparan cada experto con un scope (`$ARGUMENTS`).

- [ ] **Step 1: `mama-radiologo.md` (ejemplo completo — replicar)**

```markdown
---
description: Dispara al experto radiólogo de mama sobre un archivo/PR/módulo.
---

Despacha el subagente `mama-radiologo` (Agent tool, subagent_type: "mama-radiologo") para revisar el scope indicado: **$ARGUMENTS** (si está vacío, revisa el diff actual `git diff`).

Devuelve los hallazgos del radiólogo ordenados por severidad clínica, con archivo:línea y recomendación. No modifiques código: es una revisión.
```

- [ ] **Step 2: `mama-patologo.md`, `mama-gobernanza-ia.md`, `mama-audit.md`**

Mismo patrón, cada uno despachando su subagente (`mama-patologo`, `mama-gobernanza-ia`, `mama-auditor` respectivamente). `mama-audit.md` aclara que además de la revisión, el auditor puede correr verificaciones read-only (tests/estado) sin modificar nada.

- [ ] **Step 3: Commit**

```bash
cd /w/mama-detector && git add .claude/commands && git commit -m "feat: slash commands que disparan los 4 expertos"
```

---

### Task 11: Ampliar `CLAUDE.md` raíz + sub-CLAUDE.md por servicio

**Files:**
- Modify: `w:/mama-detector/CLAUDE.md`
- Create: `w:/mama-detector/services/gateway/CLAUDE.md`
- Create: `w:/mama-detector/services/fusion/CLAUDE.md`
- Create: `w:/mama-detector/services/mammography/CLAUDE.md`
- Create: `w:/mama-detector/services/histopathology/CLAUDE.md`
- Create: `w:/mama-detector/services/genomics/CLAUDE.md`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: `CLAUDE.md` raíz como índice de la doc + gobernanza + expertos; sub-CLAUDE finos por servicio.

- [ ] **Step 1: Ampliar `CLAUDE.md` raíz**

Añadir secciones (sin romper lo existente): **Mapa de docs** (tabla: architecture/, adr/, psp/, requisitos.md, runbook.md, anteproyecto/); **Gobernanza** (GitHub Issues, DoR/DoD, hook commit-msg, plantillas PR); **Expertos disponibles** (tabla de los 4 slash commands y cuándo usarlos); **Alcance** (rebanada vertical vs. trabajo futuro). Enlazar `docs/requisitos.md` y `docs/architecture/overview.md`.

- [ ] **Step 2: Crear los 5 sub-CLAUDE.md (finos)**

Cada uno ≤15 líneas: rol del servicio, su `modality`/endpoint, que consume `mama_contracts`, que la inferencia es un stub mock (`app/model.py`), y "no editar contratos aquí". Para `gateway`: que es la única superficie pública y orquesta las 3 modalidades + fusión.

- [ ] **Step 3: Commit**

```bash
cd /w/mama-detector && git add CLAUDE.md services/*/CLAUDE.md && git commit -m "docs: CLAUDE.md raiz como indice y sub-CLAUDE por servicio"
```

---

## Notas de ejecución

- **Orden:** Task 1–2 (config/enforcement) → 3 (materiales fuente) → 4–7 (contenido de docs) → 8 (templates GitHub) → 9–10 (expertos) → 11 (índice CLAUDE). Tasks 4–7 son independientes entre sí una vez hecha la 3.
- **Commits sin `(#N)`:** este plan es bootstrap; los commits usan `tipo: desc`. El hook (Task 2) los acepta.
- **No pushear desde el Bash tool.** Al terminar, si se quiere subir: `git -C W:\mama-detector push` vía PowerShell (o dejar que el usuario lo haga).
- **Verificación transversal:** al cerrar, `bash .githooks/test-commit-msg.sh` pasa y `python -c "import json; json.load(open('.claude/settings.json'))"` no falla.
```
