# mama-detector — Contexto para Claude Code

Plataforma académica multimodal de apoyo a la detección temprana de cáncer de mama
(mamografía + histopatología + genómica). No es un dispositivo médico certificado.

## Convenciones de commit
Mensajes en español: `tipo: descripción breve` (`feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `test`).

## Datos sensibles (PHI)
Nunca loguear identificadores de paciente/caso, rutas/nombres de archivos (DICOM/WSI),
resultados de predicción ni URLs de Storage. Nunca exponer URLs de Storage al cliente
sin signed URL generada server-side.

## Contratos
`packages/contracts/schemas/*.json` es la fuente de verdad. El código pydantic/TS es
generado con `just gen-contracts` — nunca se edita a mano.

## Arquitectura
Solo el `gateway` se expone al exterior. Los servicios de modalidad y fusión son internos.
