# Anteproyecto — Material fuente (TG)

Documentos originales del Trabajo de Grado, copiados aquí para que el repo sea autosuficiente.

- `anteproyecto.docx` — anteproyecto formal (USC). Contexto epidemiológico CO, problema, objetivos.
- `resumen-requisitos-profesor.md` — requisitos del profesor Jair Sanclemente (capacidades IA, multiagente, métricas, interoperabilidad, legal).
- `propuesta-alcance-tg.md` — alcance acordado: arquitectura completa diseñada; rebanada vertical implementada.
- `referencias-apa.md` — referencias APA 7 de las fuentes de estadificación TNM y contexto colombiano (GPC Minsalud, consenso CAC 2025, AJCC 8), con datos colombianos citables. **No es fuente**: es material de apoyo para redactar el anteproyecto, y marca qué referencias siguen pendientes de verificar.

Estos son la **fuente**; los requisitos operativos viven en [`../requisitos.md`](../requisitos.md).

## Convención de versionado del anteproyecto

El anteproyecto se descarga del navegador con nombres como `AnteProyecto Cancer de mama (3).docx`.
**Ese nombre no se versiona.** Al traer una versión nueva se **sobrescribe `anteproyecto.docx`**:

```sh
cp "/ruta/descargas/AnteProyecto Cancer de mama (N).docx" docs/anteproyecto/anteproyecto.docx
```

**Por qué:** el sufijo `(N)` es un artefacto de descarga, no una versión del documento. Si cada
descarga entrara con su propio nombre, git la vería como archivo nuevo sin relación con la anterior
y **se perdería la historia** del documento. Con el nombre normalizado, cada versión queda como un
commit más sobre el mismo archivo y `git log --follow docs/anteproyecto/anteproyecto.docx` muestra
la evolución completa. El historial de versiones vive en git, no en el nombre.
