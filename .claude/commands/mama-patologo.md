---
description: Dispara al experto patólogo de mama sobre un archivo/PR/módulo.
---

Despacha el subagente `mama-patologo` (Agent tool, subagent_type: "mama-patologo") para revisar el scope indicado: **$ARGUMENTS** (si está vacío, revisa el diff actual `git diff`).

Devuelve los hallazgos del patólogo ordenados por severidad clínica, con archivo:línea y recomendación. No modifiques código: es una revisión.
