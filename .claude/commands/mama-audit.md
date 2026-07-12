---
description: Dispara al auditor PSP + regulatorio para revisar trazabilidad, cumplimiento legal y estado.
---

Despacha el subagente `mama-auditor` (Agent tool, subagent_type: "mama-auditor") para revisar el scope indicado: **$ARGUMENTS** (si está vacío, revisa el diff actual `git diff`).

Devuelve los hallazgos del auditor ordenados por severidad, con archivo:línea y recomendación. El auditor es read-only y puede ejecutar verificaciones de tests, estado del repo, trazabilidad y cumplimiento normativo sin modificar nada.
