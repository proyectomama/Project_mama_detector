# Plantilla de post-mortem

Copiar esta plantilla a `docs/psp/postmortems/AAAA-MM-DD-titulo-corto.md` al cierre de cada
hito/sprint (o de cualquier incidente relevante). Completar todas las secciones — un post-mortem
vacío no cumple la fase "Post-mortem" de [`psp-methodology.md`](psp-methodology.md).

```markdown
# Post-mortem — <título del hito>

Fecha: <AAAA-MM-DD>
Periodo cubierto: <rango de fechas o issues #N..#M>

## Resumen

Qué se planeó hacer en este hito y qué se logró, en 2–4 frases.

## Estimado vs real

| Métrica | Estimado | Real | Nota |
|---------|----------|------|------|
| Issues cerrados | | | |
| Tiempo (h) | | | |
| Tests agregados | | | |

## Defectos por fase

Resumen de las filas de [`defect-log.md`](defect-log.md) correspondientes a este periodo:
cuántos defectos, en qué fase se inyectaron mayoritariamente, en qué fase se detectaron, y si hay
un patrón (p. ej. "todos los defectos de Environment/Config se detectan en Test, nunca antes").

## Qué salió bien

Prácticas o decisiones que ayudaron y conviene repetir.

## Qué mejorar

Puntos de fricción, retrabajo o defectos evitables con mejor disciplina.

## Acciones (con responsable)

| Acción | Responsable | Fecha límite |
|--------|-------------|--------------|
| | | |
```
