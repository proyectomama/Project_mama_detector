---
description: Dispara al experto en gobernanza de IA multimodal sobre un archivo/PR/módulo.
---

Despacha el subagente `mama-gobernanza-ia` (Agent tool, subagent_type: "mama-gobernanza-ia") para revisar el scope indicado: **$ARGUMENTS** (si está vacío, revisa el diff actual `git diff`).

Devuelve los hallazgos de gobernanza ordenados por severidad, con archivo:línea y recomendación. No modifiques código: es una revisión.
