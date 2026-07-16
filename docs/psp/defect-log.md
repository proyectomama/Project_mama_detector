# Registro de defectos (PSP)

Registro de defectos encontrados en cualquier fase del proceso (diseño, código, prueba), siguiendo
la práctica PSP de asentar **fase de inyección** (dónde se originó) y **fase de detección** (dónde
se encontró) por separado — la distancia entre ambas es la señal de proceso más importante a
mejorar. Ver [`psp-methodology.md`](psp-methodology.md) para las fases.

> **Nota:** las descripciones de esta tabla **no contienen PHI** — sin `case_ref` real, sin rutas
> de estudios DICOM/WSI reales, sin resultados de predicción reales (ver
> [`../architecture/phi-and-security.md`](../architecture/phi-and-security.md)). D-001 es de
> infraestructura/andamiaje; **D-002…D-008 son defectos de diseño clínico** (semántica de categorías
> TNM y alcance del motor de estadificación): tratan de **definiciones**, no de datos de pacientes,
> y por eso tampoco contienen PHI.

## Tabla

| ID | Fecha | Fase inyección | Fase detección | Tipo (PSP) | Descripción | Fix (commit) | Requisito |
|----|-------|-----------------|-----------------|------------|--------------|---------------|-----------|
| D-001 | 2026-07-12 | Design | Test | 20-Environment/Config | Los servicios (`services/*`) importan `app` en sus tests (p. ej. `from app import model`), pero sin declarar `pythonpath = ["."]` en `[tool.pytest.ini_options]` de cada `pyproject.toml`, `uv run pytest` falla con `ModuleNotFoundError: app` al no resolver el paquete desde la raíz del servicio. | `40af3c5` | — |
| D-002 | 2026-07-15 | Design | Design Review | 70-Data | **`cNX` usado como "no evaluado".** El diseño de estadificación proponía emitir `cNX` ante datos ganglionares faltantes. AJCC 8 reserva `cNX` para cuando la **cuenca ganglionar fue extirpada** y por eso no puede examinarse; además `cN0` es una afirmación **positiva** (la evaluación se hizo y salió negativa), no un default. Correcto: dato ausente → `null`/`"unknown"`. De haber llegado al contrato, habría codificado una categoría clínica falsa. | — | RF-009 |
| D-003 | 2026-07-15 | Design | Design Review | 70-Data | **`cMX` propuesto como categoría de dato faltante.** `cMX` **no existe** en AJCC 8: las únicas categorías M válidas son `cM0`, `cM1` y `pM1` (y `pM0` es inválido — todo `M0` es clínico). Un contrato que aceptara `cMX` estaría mal formado. | — | RF-009 |
| D-004 | 2026-07-15 | Design | Design Review | 10-Documentation | **Justificación equivocada de por qué `cM` no es inferible.** Se documentó que *"`cM` exige estadificación sistémica (TC, gammagrafía ósea, PET)"*. `cM0` significa **"sin signos ni síntomas"**: es una **valoración clínica** sobre historia y examen físico y **no exige** TC/PET. La conclusión (no inferible) era correcta, pero por la razón equivocada — un razonamiento errado que sostiene una conclusión correcta se propaga al siguiente que lo reutilice. | — | RF-009 |
| D-005 | 2026-07-15 | Design | Design Review | 10-Documentation | **Se documentó como no verificada una tabla que sí lo estaba.** Se afirmó que la tabla anatómica no se había cotejado celda por celda por ser el manual de pago. Al cotejar, las **19 filas** del Anexo 9 de la GPC coinciden con las *Anatomic Staging Groupings* de AJCC 8: la tabla anatómica **no cambió** entre AJCC 7 y 8 — lo que cambió es **qué tabla se debe usar**. La advertencia falsa habría causado retrabajo. | — | RF-009 |
| D-006 | 2026-07-15 | Design | Design Review | 10-Documentation | **Material educativo tomado como fuente normativa.** Se dio por resuelto el acceso a las tablas mediante láminas educativas del ACS (Hortobagyi P2P, webinar de Gress). Son **no normativas** y **anteriores** a la errata *Critical* del 2018-02-02, que reemplazó el capítulo entero. La fuente normativa es el **capítulo 48 corregido**. Codificar tablas pronósticas desde las láminas habría implementado una edición superada. | — | RF-009 |
| D-007 | 2026-07-15 | Design | Design Review | 10-Documentation | **Cláusula de licencia leída de más suelto.** Se documentó que bastaba con citar la fuente. El capítulo dice que el contenido no puede *"be sold, distributed, published, or **incorporated into any software**"* sin licencia escrita del ACS: menciona **software** explícitamente. La postura vigente (deuda consciente para el TG académico; evaluación a fondo antes de cualquier alianza clínica) está en ADR-0006. | — | RF-009 |
| D-008 | 2026-07-15 | Design | Design Review | 80-Function | **Confundir *inferir* con *recibir* (defecto de fondo).** Se concluyó que sin biomarcadores no se podían calcular las tablas pronósticas y que por tanto no debían codificarse. Falso: el motor es una función y no le importa el origen del dato — si grado Nottingham y RE/RP/HER2 entran como **dato estructurado del informe de patología**, el estadio pronóstico se calcula sin ML y sin inferencia, que es como opera cualquier sistema clínico real. **Impacto de alcance:** de este error salían dos corolarios equivocados — que RF-006 (histopatología) era prerrequisito, y que la pregunta de licencia era irrelevante. Es el defecto de mayor alcance de la sesión: de no detectarse, habría recortado el alcance del motor a la tabla anatómica, que es justo la que AJCC 8 desaconseja donde hay biomarcadores (el caso de Colombia). | — | RF-009 |

## Lectura de D-002…D-008 (frente TNM, 2026-07-15)

Los siete se **inyectaron en `Design`** y se **detectaron en `Design Review`**, dentro de la misma
sesión y **antes de llegar a código o al contrato**. Esa distancia inyección↔detección corta es el
resultado que PSP busca: **ninguno alcanzó `Coding` ni `Testing`**, donde habrían costado bastante
más — D-002/D-003 habrían quedado congelados en el JSON Schema y en el pydantic generado, y D-008
habría recortado el alcance del motor antes de que nadie notara por qué.

Causa raíz común: **se diseñó contra una fuente desactualizada o secundaria** (el Anexo 9 de la GPC,
que reproduce AJCC 7; láminas educativas previas a la errata *Critical* de 2018-02-02) en vez de
contra la normativa vigente (capítulo 48 corregido de AJCC 8). Contramedida ya aplicada: ADR-0006
fija la edición normativa y `docs/clinical/tnm.md` es la fuente clínica única del repo.

> **Qué NO es un defecto de esta tabla.** `docs/handoff-tnm-ajcc8.md` §3 marca con ⚠️ cuatro
> **trampas** —redondeo `T1mi` de la GPC (§3.2), tablas del modelo económico (§3.9), BI-RADS ≠ TNM
> (§3.10), `M0`/`N0` por defecto (§3.11)—. Son **riesgos documentados para quien implemente**, no
> defectos inyectados en este proceso: no se registran aquí. Si alguna llegara a materializarse en
> el código, **ahí** sí se abre su fila.

## Cómo agregar una fila

1. Asignar el siguiente `ID` consecutivo (`D-002`, `D-003`, …).
2. `Fase inyección` / `Fase detección`: usar los nombres de la tabla de
   [`psp-methodology.md`](psp-methodology.md) (`Planning|Design|Design Review|Coding|Code
   Review|Testing`).
3. `Tipo (PSP)`: categoría del defecto (p. ej. `10-Documentation`, `20-Environment/Config`,
   `40-Assignment`, `50-Interface`, `60-Checking`, `70-Data`, `80-Function`, `90-System`).
4. `Descripción`: qué pasó y por qué, **sin PHI**.
5. `Fix (commit)`: hash corto del commit que lo corrigió (o `—` si aún está abierto).
6. `Requisito`: `RF-NNN`/`RNF-NNN` afectado, si aplica, o `—`.

## Ver también

- [`post-mortem-template.md`](post-mortem-template.md) — el post-mortem de cada hito resume los
  defectos registrados aquí durante el período.
