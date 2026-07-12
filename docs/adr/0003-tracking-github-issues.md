# ADR-0003: Tracking de trabajo en GitHub Issues (no Jira)

## Estado

Aceptada

## Contexto

El equipo aplica disciplina PSP (Personal Software Process) al desarrollo de `mama-detector`, lo
que exige trazabilidad completa entre requisito, unidad de trabajo, commit, pull request y
evidencia de verificación. En OncoScan esa trazabilidad se apoyó en Jira, una herramienta externa
con autenticación y administración propias, separada del código. Para un TG con un equipo pequeño
y sin necesidad de coordinar con herramientas corporativas externas, mantener un sistema de
tracking separado añade fricción de acceso (cuentas, permisos) y rompe la cercanía entre el issue
y el código que lo resuelve.

## Decisión

Se usa GitHub Issues como único sistema de tracking de trabajo para `mama-detector`, referenciado
directamente por número (`#N`) desde commits y pull requests. Cada requisito del catálogo
(`docs/requisitos.md`) debe enlazar el o los issues de GitHub que lo trabajan, y cada issue debe
declarar a qué RF/RNF corresponde (exigido por Definition of Ready). No se usa Jira ni ninguna otra
herramienta externa de tracking para este proyecto.

## Consecuencias

La trazabilidad queda nativa dentro del mismo repositorio: `#N` enlaza automáticamente issue,
commits y PRs en la interfaz de GitHub, sin necesidad de autenticación externa ni de sincronizar
dos sistemas. La convención de commit se ajusta a `tipo(#N): descripción` una vez existan issues
abiertos (durante el bootstrap inicial del repo, sin issues aún creados, se acepta la forma
`tipo: descripción`, que el hook `commit-msg` debe reconocer como válida). La limitación es que se
pierden capacidades de gestión de portafolio multi-proyecto propias de Jira, que no se necesitan
para el alcance de un TG de un solo repositorio.
