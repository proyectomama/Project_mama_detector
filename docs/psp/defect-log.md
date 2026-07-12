# Registro de defectos (PSP)

Registro de defectos encontrados en cualquier fase del proceso (diseño, código, prueba), siguiendo
la práctica PSP de asentar **fase de inyección** (dónde se originó) y **fase de detección** (dónde
se encontró) por separado — la distancia entre ambas es la señal de proceso más importante a
mejorar. Ver [`psp-methodology.md`](psp-methodology.md) para las fases.

> **Nota:** las descripciones de esta tabla **no contienen PHI** — sin `case_ref` real, sin rutas
> de estudios DICOM/WSI reales, sin resultados de predicción reales (ver
> [`../architecture/phi-and-security.md`](../architecture/phi-and-security.md)). Los defectos de
> este proyecto académico, hasta ahora, son de infraestructura/andamiaje, no de datos clínicos.

## Tabla

| ID | Fecha | Fase inyección | Fase detección | Tipo (PSP) | Descripción | Fix (commit) | Requisito |
|----|-------|-----------------|-----------------|------------|--------------|---------------|-----------|
| D-001 | 2026-07-12 | Design | Test | 20-Environment/Config | Los servicios (`services/*`) importan `app` en sus tests (p. ej. `from app import model`), pero sin declarar `pythonpath = ["."]` en `[tool.pytest.ini_options]` de cada `pyproject.toml`, `uv run pytest` falla con `ModuleNotFoundError: app` al no resolver el paquete desde la raíz del servicio. | `40af3c5` | — |

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
