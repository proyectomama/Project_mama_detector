---
description: Dispara al experto radiólogo de mama sobre un archivo/PR/módulo.
---

Despacha el subagente `mama-radiologo` (Agent tool, subagent_type: "mama-radiologo") para revisar el scope indicado: **$ARGUMENTS** (si está vacío, revisa el diff actual `git diff`).

Devuelve los hallazgos del radiólogo ordenados por severidad clínica, con archivo:línea y recomendación. No modifiques código: es una revisión.
