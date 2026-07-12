# Convenciones — commits, ramas y flujo de trabajo

## Convención de commits

Formato del primer renglón del mensaje:

```
tipo(#N): descripción
tipo: descripción
```

- `tipo` ∈ `feat | fix | chore | docs | refactor | style | test`.
- `#N` es el número del **issue de GitHub** que el commit trabaja. Es **opcional**: durante el
  bootstrap del repo (sin issues todavía) se usa la forma sin `(#N)`; una vez hay issues abiertos,
  todo commit que implemente uno los referencia.
- `descripción`: en **español**, en imperativo o pretérito ("agrega", "corrige", "elimina" — no
  "agregando" ni "added"), máximo **72 caracteres**, sin punto final.
- El **cuerpo** del commit (opcional, separado por línea en blanco) explica el **porqué**, no el
  qué — el diff ya muestra el qué. Útil sobre todo para `fix` (causa raíz) y `refactor` (motivo).

Ejemplos válidos:

```
feat(#12): agrega orquestacion del gateway
fix(#34): corrige umbral BI-RADS en la fusion mock
docs: actualiza el runbook con el aprendizaje de pythonpath
```

## Autoría — sin atribución a IA (regla firme)

Todo el trabajo del repo es **obra del equipo**. **En ningún artefacto** debe figurar que lo hizo
Claude, una IA, un "asistente", un "agente" ni herramienta similar. Esto aplica a **todo**:

- **Commits:** sin trailer `Co-Authored-By: Claude …`, sin `🤖 Generated with …`, sin mención de IA
  en asunto ni cuerpo.
- **Pull Requests e Issues:** título, descripción y comentarios se redactan como trabajo del equipo.
- **Código y comentarios:** nada de "generado por IA" ni firmas de asistente.
- **Documentación** (`docs/`, `README`, ADRs, etc.): se escribe en voz del equipo, sin atribución a IA.

Si se usa una herramienta de IA como apoyo, **igual se firma como obra del equipo**. Antes de
`git push`, verificar que ningún commit arrastró un trailer de atribución:

```bash
git log origin/main..HEAD --format='%B' | grep -i 'co-authored-by\|generated with' && echo "LIMPIAR ANTES DE PUSH" || echo "ok"
```

Si aparece, se limpia reescribiendo la historia **local** (aún sin pushear) antes de subir:

```bash
git filter-branch -f --msg-filter "sed '/Co-Authored-By: Claude/d; /🤖 Generated with/d'" origin/main..HEAD
```

## Hook `commit-msg`

El repo incluye `.githooks/commit-msg`, que valida el primer renglón contra la expresión regular:

```
^(feat|fix|chore|docs|refactor|style|test)(\(#[0-9]+\))?: .{1,72}$
```

(los commits `Merge …` y `Revert …` se dejan pasar sin validar). El hook **no se activa solo** —
cada clon del repo debe activarlo una vez:

```bash
git config core.hooksPath .githooks
```

Se puede verificar que el hook funciona con su propia suite:

```bash
bash .githooks/test-commit-msg.sh
```

## Convención de ramas

`tipo/descripcion-corta`, mismo catálogo de `tipo` que los commits, en minúsculas y con guiones:

```
feat/orquestacion-langgraph
fix/umbral-birads
docs/runbook-pythonpath
```

Cuando la rama implementa un issue concreto, se puede sufijar el número: `feat/12-orquestacion-langgraph`.

## Flujo issue → rama → PR → merge

1. **Issue**: se crea con la plantilla correspondiente (`tarea`, `historia` o `defecto` — ver
   `.github/ISSUE_TEMPLATE/`) y cumple la [Definition of Ready](definition-of-ready.md) antes de
   empezar a trabajarlo.
2. **Rama**: se crea desde `main` actualizado, con el nombre `tipo/descripcion` (o
   `tipo/N-descripcion` si referencia el issue).
3. **Commits**: `tipo(#N): descripción` por cada cambio lógico; `N` = el issue que se está
   trabajando.
4. **Pull Request**: se abre contra `main` usando `.github/pull_request_template.md`, con su
   checklist de la [Definition of Done](definition-of-done.md) completo y `Cierra #N`.
5. **Revisión**: al menos una revisión humana; si el cambio toca salida clínica o datos
   sensibles, se pasa además por el experto correspondiente (`/mama-radiologo`, `/mama-patologo`,
   `/mama-gobernanza-ia`, `/mama-audit`).
6. **Merge**: solo cuando el PR cumple la Definition of Done completa y el CI pasa (tests +
   verificación de contratos sin diff).

## Ver también

- [`psp-methodology.md`](psp-methodology.md) — fase PSP ↔ artefacto.
- [`definition-of-ready.md`](definition-of-ready.md) / [`definition-of-done.md`](definition-of-done.md)
- [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) — guía de contribución completa.
