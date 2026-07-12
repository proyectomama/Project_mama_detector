# PHI, seguridad y marco legal

## 1. Qué es PHI en `mama-detector`

Se trata como **Información de Salud Protegida (PHI)** cualquiera de los siguientes elementos,
en cualquier servicio (`gateway`, `mammography`, `histopathology`, `genomics`, `fusion`):

- `case_ref` — identificador de caso clínico. Aparece en `PredictRequest` y `ClinicalAlert`
  (ver [`contracts.md`](contracts.md)). Es PHI aunque parezca un identificador opaco: permite
  correlacionar un paciente con sus resultados.
- Rutas y nombres de archivo de estudios **DICOM** (mamografía) y **WSI** (histopatología, whole
  slide images).
- `result_json` — la predicción de IA en sí (score, label, mapas de explicabilidad): revela
  información clínica sensible aunque no incluya nombre del paciente.
- URLs de almacenamiento (Storage) donde viven los estudios o resultados.

## 2. Reglas de logging

- **Nunca** loguear PHI en `stdout`/`stderr`, en logs de FastAPI/uvicorn, ni en trazas de error
  (excepciones que incluyan el payload de la petición).
- Los logs de aplicación referencian el caso, cuando sea imprescindible, por un identificador
  técnico no correlacionable (p. ej. `request_id`), nunca por `case_ref` directo.
- **Nunca** exponer una URL de Storage al cliente sin que sea una signed URL generada
  server-side, de vida corta y con alcance mínimo (solo el objeto necesario).
- Los mensajes de error devueltos al cliente no deben filtrar rutas de archivo, stack traces
  internos ni el contenido de `result_json` de otros casos.
- Los defectos y ejemplos documentados en `docs/psp/defect-log.md` y en cualquier reporte de PSP
  se redactan **sin PHI** (sin `case_ref` real, sin rutas de estudio reales).

Este proyecto es académico y no maneja pacientes reales todavía, pero el andamiaje se construye
desde ya bajo estas reglas para que la evolución hacia datos reales no requiera rediseño.

## 3. Marco legal colombiano

- **Ley 1581 de 2012** — Régimen general de protección de datos personales en Colombia. Los datos
  de salud son datos sensibles: requieren tratamiento con consentimiento explícito, finalidad
  definida y medidas de seguridad reforzadas. Aplica a `case_ref`, estudios y resultados.
- **Resolución 1995 de 1999** (Ministerio de Salud) — Reserva de la historia clínica: establece
  que la historia clínica es un documento reservado, solo accesible a las personas autorizadas.
  El sistema debe garantizar acceso controlado a cualquier dato clínico que persista.
- **Resolución 2654 de 2019** (Ministerio de Salud) — Regula la telesalud y las plataformas
  tecnológicas en salud (telemedicina, tele-experticia); aplica en la medida en que
  `mama-detector` se plantea como plataforma de apoyo diagnóstico remoto.
- **INVIMA** — El Instituto Nacional de Vigilancia de Medicamentos y Alimentos es la autoridad
  colombiana que regula el software con inteligencia artificial como **dispositivo médico**
  (Software as a Medical Device, SaMD). Un sistema que emite alertas de riesgo clínico como
  `mama-detector` requeriría **registro sanitario ante INVIMA antes de cualquier uso asistencial
  real** (fuera del alcance académico del TG).

## 4. Ética — 6 principios OMS de IA en salud

El diseño y la operación del sistema se alinean con los seis principios de la OMS para la ética y
gobernanza de la inteligencia artificial en salud:

1. **Autonomía** — proteger la autonomía humana: el sistema apoya la decisión clínica, no la
   sustituye; el profesional de salud mantiene el control final.
2. **Bienestar y seguridad** — promover el bienestar humano, la seguridad del paciente y el
   interés público por encima de cualquier otra consideración.
3. **Transparencia y explicabilidad** — las predicciones deben ser explicables (Grad-CAM/XAI en
   mamografía; ver RF-003), no cajas negras.
4. **Responsabilidad (accountability)** — trazabilidad clara de quién es responsable de cada
   decisión asistida por el sistema; corresponde al Agente Auditor regulatorio.
5. **Equidad (inclusividad)** — que el sistema sea accesible y funcione con la misma calidad para
   distintas poblaciones (ver sección 6).
6. **IA ambientalmente responsable y sostenible** — uso proporcionado de cómputo; coherente con
   la restricción de alcance del TG a una rebanada vertical por presupuesto de hardware (ver
   `docs/anteproyecto/propuesta-alcance-tg.md`).

## 5. Disclaimer obligatorio

Toda salida clínica visible (reporte, alerta, score, nivel de riesgo) debe mostrar, sin
excepción, el siguiente disclaimer:

> **"No es un dispositivo médico certificado."**

Este es un requisito no funcional (RNF-008) y aplica hoy al diseño del `ClinicalAlert` que
devuelve el gateway; el mock actual todavía no lo incluye en el payload (ver
`docs/requisitos.md`, estado `Propuesto`).

## 6. Sesgo poblacional y equidad

Los datasets públicos de referencia para mamografía (CBIS-DDSM), histopatología (BreakHis,
TCGA-BRCA) y genómica (TCGA-BRCA, METABRIC) están mayoritariamente compuestos por población
norteamericana/europea. Un riesgo explícito del proyecto es que un modelo entrenado solo sobre
esos datos generalice mal a mujeres latinoamericanas (contexto colombiano del TG). Mitigación
prevista (RNF-005): evaluar y reportar métricas desagregadas por subgrupo cuando se disponga de
datos representativos, y documentar explícitamente esta limitación en cualquier resultado o
informe mientras no se cuente con datos locales. Corresponde al Agente Gobernanza IA vigilar este
principio (ver `.claude/agents/mama-gobernanza-ia.md`).
