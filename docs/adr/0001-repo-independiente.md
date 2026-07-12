# ADR-0001: Repo independiente para mama-detector

## Estado

Aceptada

## Contexto

`mama-detector` nace como el sistema de IA para el Trabajo de Grado de detección temprana de
cáncer de mama, en un equipo que ya opera OncoScan (plataforma de apoyo a detección de cáncer
pulmonar) bajo disciplina PSP. La opción más rápida hubiera sido anidar el nuevo proyecto como
subdirectorio o fork de OncoScan, reutilizando su historial y configuración de Git directamente.
Sin embargo, ambos proyectos tienen dominios clínicos, datasets, contratos de datos y ciclos de
vida académicos distintos (TG independiente, director y cronograma propios), y mezclar su
historial de commits o su gobernanza habría acoplado innecesariamente dos entregables que se
evalúan por separado.

## Decisión

`mama-detector` es un repositorio Git propio e independiente (remoto `origin` =
`https://github.com/proyectomama/Project_mama_detector.git`, rama principal `main`), sin
relación de fork ni de submódulo con OncoScan. Se reutiliza deliberadamente la **disciplina de
proceso** validada en OncoScan (PSP lean sobre GitHub Issues, ADRs, convención de commits,
subagentes expertos en `.claude/agents/`), pero no su código, su historial de Git ni su
configuración de repositorio.

## Consecuencias

El proyecto gana autosuficiencia total: puede clonarse, documentarse, evaluarse y entregarse al
director de TG sin dependencias del repositorio de OncoScan, y su historial de commits refleja
únicamente el trabajo de este TG. Como contrapartida, la disciplina de proceso (plantillas de
issue/PR, hooks, estructura de ADR, subagentes) debe mantenerse manualmente en paralelo entre
ambos repos en lugar de compartirse por herencia de Git; cualquier mejora de proceso descubierta
en uno debe portarse a mano al otro si se quiere conservar la paridad.
