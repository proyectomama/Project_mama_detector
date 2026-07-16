# Handoff — TNM / AJCC 8: hallazgos, correcciones y trabajo pendiente

**Fecha:** 2026-07-15
**Origen:** solicitud del director (correo del 2026-07-15) de *identificar y validar el TNM*.
**Propósito:** que otra sesión pueda continuar sin repetir la investigación **ni volver a caer en
los errores que ya se cometieron y corrigieron aquí** (§3).
**Rama:** `fix/fase-0-saneamiento`.

> Documento de continuidad, no fuente de verdad. La fuente clínica es
> [`clinical/tnm.md`](clinical/tnm.md); la decisión es
> [`adr/0006-estadificacion-tnm-ajcc8-pronostica.md`](adr/0006-estadificacion-tnm-ajcc8-pronostica.md).
> Si algo aquí los contradice, mandan ellos.

> ## ⚠️ Actualización del 2026-07-15 (sesión siguiente) — leer antes que §6 y §8
>
> Se ejecutó **§8.1–§8.4**. Dos decisiones **cambiaron respecto de lo que dice este documento más
> abajo**; el texto original de §6.2/§6.3/§8 se conserva como registro de lo que se pensó entonces,
> pero **manda esta nota**:
>
> 1. **Convención del `.docx`: se normalizó a `docs/anteproyecto/anteproyecto.docx`** — **no** la
>    ruta con `(3)` que §6.2 daba por canónica. Se tomó la opción que §6.2 dejaba abierta ("si el
>    equipo quisiera volver a esa convención, este es el momento"), para no perder la historia del
>    archivo cuando baje el `(4)`. La convención quedó escrita en
>    [`anteproyecto/README.md`](anteproyecto/README.md).
>    - **Hallazgo que §6.2 no registraba:** el blob de `(2).docx` en staging era **idéntico** al de
>      `anteproyecto.docx` en HEAD (`c9e2e85`), o sea que el viejo `anteproyecto.docx` **era** la
>      versión (2). Por eso la resolución limpia no fue un rename sino una **modificación de
>      contenido** de `anteproyecto.docx` (v2 → v3, blob `87b116a`): git conserva la historia
>      completa y **no se commitea ningún borrado** del material del TG.
>    - **Efecto colateral: §6.3 quedó sin trabajo.** Las 4 referencias a `anteproyecto.docx` **ya no
>      son obsoletas** —el archivo vuelve a llamarse así—, así que no se tocó ninguna. **B-008 sigue
>      vigente** y no se cerró (§6.3 ya advertía de no confundir un cambio de ruta con su cierre).
> 2. **ADR-0006 pasó a `Aceptada`**, pero **por el equipo, no por el director**: él **aún no ha
>    respondido** el hilo del 2026-07-15. El ADR lo dice explícitamente. **No citar esa aceptación
>    como aprobación del director.**
>
> **Hecho:** issues **#6** (RF-009) y **#7** (RF-010) creados · `requisitos.md` con RF-009/RF-010 en
> estado `Aprobado` y notas en RNF-006/RNF-007 · `traceability.md` · ADR-0006 `Aceptada` ·
> `contracts.md` (tipo de estadificación, diseñado) · `overview.md` §4.1 · `alcance-vigente.md` §5 ·
> `roadmap-tg.md` (frente paralelo) · `anteproyecto/referencias-apa.md` (nuevo).
>
> **Sigue pendiente:** **§8.2** (schema + `just gen-contracts`), **§8.5** (responder al director) y
> **§8.6** (implementar el motor). Las secciones §1–§5, §7 y §9 **no cambiaron** y siguen vigentes —
> en particular **§3, las trampas, que es la razón de ser de este handoff**.

---

## 1. Qué pidió el director y qué era el PDF

`D:\Descargas\TNM.pdf` **no es un documento sobre TNM**: es un correo de Outlook impreso a PDF
(5 páginas, **imagen pura, sin capa de texto** — hubo que renderizar a PNG para leerlo; `pdftoppm`
no está instalado, se usó PyMuPDF).

Contenido del correo:
- **La petición:** *"Tener en cuenta la clasificación TNM del cáncer de mama. El software
  diagnosticará de manera temprana el cáncer de mama y eso requiere identificar y validar el TNM"*.
- **La instrucción:** *"Leer y analizar muy bien este documento"* → la GPC del Minsalud.
- **Cuatro enlaces**, todos analizados (§7).
- Las figuras pegadas (9.6, 9.7, 9.10, 9.11) y tablas (9.14–9.25) son del capítulo de **evaluación
  económica** de la GPC — ver la trampa de §3.9.
- La definición de TNM del correo es **literal del glosario del consenso CAC 2025**.

> **PHI / datos personales:** el hilo contiene nombres y direcciones de correo del director y de los
> estudiantes. **No reproducirlos** en commits, issues, docs ni código (Ley 1581/2012). Citar por
> **fecha y asunto**, como ya hace `alcance-vigente.md`.

## 2. Los cuatro hallazgos que gobiernan todo

1. **El TNM no es inferible desde una mamografía.** `cT` es *estimable* (diámetro mayor, requiere
   `PixelSpacing`/`ImagerPixelSpacing` del DICOM); `cN` **no** (CC/MLO no cubren la axila de forma
   fiable → exige ecografía axilar, RM, BACAF o centinela); `cM0` es **juicio clínico** sobre signos
   y síntomas, no salida de un modelo. Sin `N` ni `M` no hay estadio.
2. **CBIS-DDSM no tiene etiquetas TNM**, ni ganglionares, ni de metástasis, ni biomarcadores. Tiene
   densidad, tipo de anormalidad, BI-RADS, patología (`BENIGN`/`BENIGN_WITHOUT_CALLBACK`/
   `MALIGNANT`), sutileza y máscaras de ROI. **No se puede entrenar ni validar TNM con él.**
   Afirmar "validamos el TNM" con CBIS-DDSM es del mismo tipo de defecto que afirmar una métrica no
   medida.
3. **El Anexo 9 de la GPC reproduce AJCC 7 (2010)**, no la 8.ª vigente. Implementarlo literal
   codifica dos errores concretos: `Tis(CLIS)` y el redondeo de 1.1 mm (§3.2).
4. **AJCC 8 restringe la tabla anatómica** a *"global regions where biomarker tests unavailable"* —
   y **Colombia sí tiene biomarcadores** (el consenso CAC 2025 reporta indicadores de RH y HER2).
   De aquí sale la decisión de §5.

**Consecuencia transversal:** el sistema **no puede emitir un estadio TNM desde una mamografía**.
Cualquier salida que lo afirme es defecto clínico **bloqueante**. El motor se dispara sobre un
cáncer **confirmado por biopsia**, no sobre la salida del modelo — la plataforma detecta *sospecha*,
y estadificar porque el modelo dijo `malignant` sería precisamente el error a evitar.

## 3. Trampas: errores ya cometidos y corregidos en esta sesión

**Esta sección es la razón de ser del handoff.** Cada punto es un error que ya se cometió y se
corrigió. Si otra sesión lee solo el resultado final, los repite.

### 3.1 `cNX` no significa "no evaluado" ❌→✅

- **Se escribió:** ante datos faltantes, emitir *"estadio indeterminado (`cNX`/`cMX`)"*.
- **Por qué está mal:** AJCC 8 reserva `cNX` para cuando **la cuenca ganglionar fue extirpada** y por
  eso no puede examinarse. Y `cN0` **se asigna cuando la evaluación es posible y sale negativa** —
  es una afirmación *positiva*, no un default.
- **Correcto:** si nadie evaluó la axila, la categoría es **ausente/desconocida** (`null` /
  `"unknown"` en el contrato), **no** `cNX`.

### 3.2 `T1mi` y el redondeo: la GPC contradice a AJCC 8 ⚠️

- **La GPC (AJCC 7) dice:** *"un tumor con tamaño 1,1 mm se notifica como 1 mm"* → caería en `T1mi`.
- **AJCC 8 dice:** un tumor **>1.0 mm nunca se redondea hacia abajo a `T1mi`**. 1.1–1.4 mm → **2 mm**
  → `T1a`. `T1mi` **solo** para ≤1 mm. Regla general: redondear abajo entre 1–4, arriba entre 5–9.
- **Impacto:** cambia la categoría T. No copiar la regla de redondeo de la GPC.

### 3.3 `cMX` no existe ❌→✅

- **Se escribió:** `cMX` como categoría para dato faltante.
- **Correcto:** las **únicas** categorías M válidas son **`cM0`, `cM1`, `pM1`**. No hay `MX`/`cMX`.
  Un contrato que los acepte está mal formado. Y **`pM0` no es válido**: todo `M0` es clínico.

### 3.4 El motivo por el que `cM` no es inferible ❌→✅

- **Se escribió:** *"`cM` exige estadificación sistémica (TC, gammagrafía ósea, PET)"*.
- **Matiz correcto:** `cM0` significa **"sin signos ni síntomas"** — es una **valoración clínica**
  sobre historia y examen físico, y **no exige** TC/PET. Sigue sin ser inferible por el sistema,
  pero **por otra razón**: es juicio clínico, no salida de un modelo de imagen. (`cM1` sí exige
  evidencia clínica o radiográfica.)

### 3.5 La tabla anatómica sí está verificada ❌→✅

- **Se escribió:** *"el manual AJCC 8 es de pago, la tabla no se verificó celda por celda; cotejar
  antes de implementar"*.
- **Correcto:** se cotejaron **las 19 filas** del Anexo 9 de la GPC contra las *Anatomic Staging
  Groupings* oficiales de AJCC 8: son **idénticas**. **La tabla anatómica no cambió entre AJCC 7 y
  8.** Lo que cambió es **qué tabla se debe usar**. Está verificada y es implementable tal cual.

### 3.6 "Encontré las tablas gratis, problema resuelto" — a medias ❌→✅

- **Se escribió:** que las láminas educativas del ACS resolvían el acceso a las tablas.
- **Correcto:** las láminas (Hortobagyi P2P, webinar de Gress) son **material educativo, NO
  normativo**, y son **anteriores a la corrección de 2018-02-02**. La fuente normativa es el
  **capítulo 48 corregido** (§4). No codificar tablas pronósticas desde las láminas.

### 3.7 "Copyright: citá y listo" — demasiado suelto ❌→✅

- **Se escribió:** que bastaba citar la fuente.
- **Correcto:** el capítulo oficial dice: *"Content is available for user's personal use. It cannot
  be sold, distributed, published, or **incorporated into any software**, product, or publication
  without a written license agreement with ACS."* Dice **software** explícitamente. Ver la postura
  vigente en §5.

### 3.8 "Sin biomarcadores no podés calcular las pronósticas" ❌→✅ (el error de fondo)

- **Se escribió:** *"Las pronósticas no las necesitás. Sin biomarcadores no podés calcularlas. No
  codifiques lo que no podés computar — y la pregunta de licencia se vuelve irrelevante."*
- **Por qué está mal:** confunde **inferir** con **recibir**. El motor es una función: no le importa
  de dónde vienen los datos. Si grado y RE/RP/HER2 entran como **dato estructurado del informe de
  patología**, el estadio pronóstico **se calcula perfectamente**, sin ML y sin inferencia. Así
  opera cualquier sistema clínico real: el laboratorio mide, el informe reporta, el software recibe.
- **Corolarios:**
  - **RF-006 NO es prerrequisito del estadio pronóstico.** RF-006 es *inferir* desde WSI
    (BreakHis/TCGA-BRCA) y es trabajo futuro — además **BreakHis no tiene etiquetas de
    biomarcadores**. Para el estadio pronóstico no hace falta un modelo: hace falta **un campo en el
    contrato**.
  - La pregunta de licencia **no era irrelevante**: era *contingente* a una decisión de alcance que
    se había tomado sin declararla. Ver §5.

### 3.9 Las tablas del modelo económico de la GPC no son reglas de estadificación ⚠️

Las tablas y figuras que el director pegó en el correo vienen del capítulo de **evaluación
económica** (modelo de Markov de costo-efectividad del tamizaje). **Parametrizan una simulación, no
clasifican pacientes.** Usarlas para estadificar es un **error de categoría**:

- **Tabla 9.16 / 9.23** "Estadio según diámetro tumoral" (in situ 0.50 cm · local 1.00 cm · regional
  2.00 cm) → **estados de un modelo**, no umbrales TNM.
- **Figura 9.7** agrupa: in situ = 0 · local = I–IIA · regional = IIA, IIIA–IIIC · metastásico = IV.
  Simplificación para simular historia natural.
- **Tabla 9.17 / 9.24** (probabilidad de síntomas por diámetro) y las distribuciones de crecimiento
  (lognormal, Weibull) son del mismo modelo.

Si algún día el repo modela historia natural o costo-efectividad, **esas son las tablas correctas**.
Para estadificar, no.

### 3.10 BI-RADS no es TNM ⚠️

BI-RADS gradúa la **sospecha** de un estudio de imagen y guía la conducta diagnóstica. TNM describe
la **extensión anatómica de un cáncer ya diagnosticado**. **No existe función BI-RADS → estadio.**
Confundirlos es error clínico, no imprecisión de nomenclatura.

### 3.11 `M0` / `N0` por defecto: el modo de fallo más peligroso ⚠️

Un `cM0` o `cN0` asumido por silencio convierte **"no sabemos"** en **"no hay enfermedad"**. Como
ambas son afirmaciones *positivas* (la evaluación se hizo y salió negativa), ponerlas por defecto no
es un atajo: **es fabricar un hallazgo clínico**. Ante entrada obligatoria ausente → *"estadio no
determinable"*.

## 4. AJCC 8: versiones, erratas y fuentes

### 4.1 No existe una "versión 2021"

Solo hay **AJCC 8** (vigente desde **2018-01-01**; **no hay 9.ª edición para mama**). Lo que varía
es la **impresión** del manual (1.ª, 2.ª, 3.ª). El "2021" es solo la última fecha de revisión de la
*hoja de erratas*.

### 4.2 Erratas de mama: solo dos, ninguna te afecta hoy

| Impresión | Tipo | Publicada | Cambio |
|---|---|---|---|
| **1.ª** | **Critical** | **2018-02-02** | **Capítulo entero reemplazado.** Antes: sistema de grado único para in situ e invasivo, *"prognostic stage group with missing combinations"*. Después: grados distintos para in situ vs invasivo + **nuevos grupos pronósticos clínico y patológico** con datos adicionales del NCDB. pp. 589–628 (1.ª/2.ª) → **589–636** (3.ª) |
| 3.ª | Typo | 2018-03-29 | Tabla 48.1: `Partial Response (cPR y pCR)` → `(cPR y pPR)` |

La entrada de **2021-01-13** de la hoja es de *Soft Tissue Sarcoma*, **no de mama**.
Niveles de errata: **Critical** (afecta categorías TNM o grupos pronósticos) · Histo/Topo ·
Clarification · Omission.

### 4.3 Jerarquía de fuentes (de normativa a didáctica)

1. **Capítulo 48 *Breast* corregido — NORMATIVO.** *"Last updated 01/25/2018"*, pp. **589–636**
   (= rango de la 3.ª impresión → **es el corregido**), 50 pp., ambas tablas pronósticas.
   El AJCC lo entrega tras registro por correo; la American Society of Breast Surgeons lo espeja:
   `http://www.breastsurgeonsweb.com/wp-content/uploads/downloads/2020/10/AJCC-Breast-Cancer-Staging-System.pdf`
   **No versionar el PDF en el repo** (sería *distribuir*) — citar por URL.
2. **Hoja de erratas — libre:** `https://www.facs.org/media/g0wdye45/errata.xlsx` ·
   [página Updates and Corrections](https://www.facs.org/quality-programs/cancer-programs/american-joint-committee-on-cancer/updates-and-corrections/)
3. **Material educativo — NO normativo:** Hortobagyi, *Physician to Physician: Breast*
   (`https://www.facs.org/media/u4djjc4v/breast-8th-ed.pdf`, tablas en láminas 23–24 y 39–49) ·
   Gress, *8th Edition Breast Staging* (`https://www.facs.org/media/ws2fjubi/8th-edition-breast-staging.pdf`) ·
   Giuliano et al., CA Cancer J Clin 2017.

> Nota técnica: el `.xlsx` se leyó como ZIP + XML (`sharedStrings.xml`), porque `openpyxl` provoca
> segfault en este entorno al importar numpy. Las fechas vienen como serial de Excel (epoch
> 1899-12-30): 43133 → 2018-02-02 · 43188 → 2018-03-29 · 44209 → 2021-01-13.

### 4.4 Qué cambia AJCC 8 respecto de AJCC 7

**Lo contraintuitivo: la tabla anatómica NO cambió.** Cambió *cuál tabla se usa*. Tres tablas:

| Tabla | Cuándo |
|---|---|
| **Anatómica** | **Solo** en regiones sin acceso a biomarcadores. Palabras del AJCC: *"May never use anatomic stage group table — even if prognostic factor categories are missing, even if stage group will be unknown — will skew stage group data."* |
| **Clínica pronóstica** | **Todos** los pacientes, **antes de cualquier tratamiento** |
| **Patológica pronóstica** | Solo si la **cirugía es el tratamiento inicial**; **no aplica tras neoadyuvancia**. Recomendada para todos los registros de tumores en EE. UU. |

Cambios concretos:
- **LCIS eliminado de `Tis`** (entidad benigna). In situ solo `Tis (CDIS)` o `Tis (Paget)`.
- **Redondeo:** >1.0 mm nunca baja a `T1mi` (§3.2).
- **Tumores múltiples `(m)`:** dimensión del **mayor**, no la suma.
- **`T4b`:** nódulos satélite **separados** del primario e identificados **macroscópicamente**; los
  vistos solo al microscopio **no** califican.
- **`cN0`/`cNX`:** ver §3.1. **M:** solo `cM0`/`cM1`/`pM1`; `pM0` inválido.
- **Grado:** debe ser **Nottingham/SBR modificado** (túbulos + pleomorfismo + mitosis), **no**
  nuclear. Con grado nuclear solo → **no se asigna grupo de estadio**.
- **RE/RP:** positivos con **>1 %** de células teñidas (IHQ). Si biopsia y resección discrepan,
  **prevalece el positivo**.
- **HER2:** ASCO/CAP 2013. IHQ 0/1+ negativo · 2+ equívoco · 3+ positivo. **Equívoco por ISH →
  se categoriza NEGATIVO** para asignar estadio.
- **Perfil genómico:** **solo Oncotype DX <11** en **T1–2 N0 M0 / RE+ / HER2− / cualquier grado /
  cualquier RP** → patológico **IA**. MammaPrint, ProSigna, EndoPredict, Breast Cancer Index e IHC4
  **no** asignan estadio.
- **Posneoadyuvancia:** se asignan `ypT`/`ypN` pero **no hay grupo de estadio**. Los grupos
  pronósticos posneoadyuvantes estaban *"under preparation"*. Respuesta patológica completa
  (`ypT0 ypN0 cM0`) → sin grupo.
- **Ki-67:** recomendado como marcador de proliferación, pero **no** entra en el estadio pronóstico.

**Por qué importa** (ejemplos oficiales del AJCC — mismo TNM, biología distinta):

| Caso | TNM | Anatómico | Clínico | Patológico |
|---|---|---|---|---|
| G3, triple negativo | pT1 N1 M0 | IIA | **IB** | IIA |
| G1, RE+ RP+ HER2+ | pT1 N1 M0 | IIA | **IA** | **IA** |
| G1, RE+ RP+ HER2+ | pT3 N1 M0 | **IIIA** | IIA | **IB** |
| G2, RE+ RP− HER2−, Oncotype 9 | pT2 N0 M0 | IIA | IIA | IIA → **IA** (genómico) |

El tercero baja **dos grupos completos** (IIIA → IB). Un `T3 N2 M0` puede caer entre **IA y IIIA**
según grado y biomarcadores.

## 5. Decisión tomada: Opción B (ADR-0006)

**Decidido por el equipo el 2026-07-15.** Razonamiento del equipo: *si AJCC 8 es la norma y su uso
correcto implica biomarcadores, la única opción coherente es la B.*

- **Edición normativa: AJCC 8**, no el Anexo 9 de la GPC. Fuente: capítulo 48 corregido.
- **Se implementa la tabla pronóstica, no solo la anatómica.** El motor acepta **grado Nottingham +
  RE + RP + HER2** como **entrada estructurada** y calcula el estadio pronóstico.
- **Motor determinista, dirigido por tabla.** Sin ML. Valida la tupla, rechaza combinaciones
  imposibles, calcula el grupo.
- **El sistema no infiere lo que no puede medir.** `cN`, `cM`, grado y biomarcadores **siempre**
  entran como dato estructurado. `cT` puede *proponerse* desde imagen, marcado como estimación
  radiológica con incertidumbre y prefijo `c` — **nunca `pT`**.

**Alternativa descartada (Opción A — solo anatómico):** sin fricción de licencia, pero emite
justamente la tabla que AJCC 8 desaconseja donde hay biomarcadores, que es el caso de Colombia.

**Postura de licencia (decisión del equipo):** para el **TG interno/académico no bloquea** — se
codifica citando la fuente. **Si el proyecto se aliara con clínicas** o saliera de lo académico, la
cláusula de *"incorporated into any software"* se evalúa **a fondo antes de ese paso**. Queda como
**deuda consciente**, no como descuido. Precedente útil: la GPC del Minsalud reproduce las tablas
con nota *"Reproducido con permiso del AJCC"* — el Estado colombiano **pidió permiso**.

### 5.1 Lo que la Opción B obliga a resolver

- **Son dos tablas, no una.** Clínica y patológica dan resultados **distintos** para la misma
  combinación → el motor necesita el **contexto de tratamiento** como entrada obligatoria (¿fue la
  cirugía el tratamiento inicial? ¿hubo neoadyuvancia?). No es un detalle.
- **Casos sin estadio asignable**, a representar en vez de forzar un valor: grado nuclear en lugar
  de Nottingham · posneoadyuvancia (`ypT`/`ypN`) · respuesta patológica completa.
- **Normalización previa a la tabla:** HER2 equívoco por ISH → negativo · RE/RP >1 % · si biopsia y
  resección discrepan, prevalece el positivo.
- **Validación por cobertura exhaustiva de la tabla de verdad** (todas las combinaciones TNM × grado
  × HER2 × RE × RP). Es verificación **completa**, no muestreo estadístico → artefacto **PSP**
  excepcionalmente fuerte, y contrasta a propósito con la evaluación estadística del modelo de
  mamografía.
- **El límite de la afirmación no se mueve:** el motor **calcula** el estadio con datos que
  **recibe**; no los mide ni los verifica. La plataforma no determina el estadio de una mamografía.

## 6. Estado del repo al cerrar esta sesión

**Rama:** `fix/fase-0-saneamiento`. **Nada de esto está commiteado.**

### 6.1 Trabajo ya hecho (no rehacer)

| Archivo | Estado |
|---|---|
| `docs/clinical/tnm.md` | **Nuevo** (444 líneas). Fuente única de TNM del repo: categorías T/cN/pN/M, tabla anatómica, estadio pronóstico, divergencias AJCC 7 vs 8, límites de inferencia, contexto CO, fuentes |
| `docs/adr/0006-estadificacion-tnm-ajcc8-pronostica.md` | **Nuevo** (102 líneas). Estado: **Propuesta** |
| `.claude/agents/mama-radiologo.md` | Modificado: cT, límites de cN/cM, BI-RADS≠TNM, tamizaje CO |
| `.claude/agents/mama-patologo.md` | Modificado: pT/pN, umbrales de depósito, `(sn)`, `pM0` inválido, AJCC 8 vs 7, estadio pronóstico, biomarcadores, erratas |
| `.claude/agents/mama-gobernanza-ia.md` | Modificado: validez de afirmaciones de estadio, edición declarada, dato ausente ≠ negativo |
| `.claude/agents/mama-auditor.md` | Modificado: trazabilidad del requisito TNM, fuentes normativas CO, impacto INVIMA |
| `CLAUDE.md` | Modificado: `docs/clinical/` agregado al mapa de docs |

### 6.2 El `.docx` del anteproyecto: ruta canónica y rename roto

**NO es trabajo de esta sesión, pero bloquea el commit de la rama.**

**Ruta canónica — decidida por el equipo (2026-07-15):**

```
W:\mama-detector\docs\anteproyecto\AnteProyecto Cancer de mama (3).docx
```

En POSIX/git: `docs/anteproyecto/AnteProyecto Cancer de mama (3).docx`. **El `(3)` es el documento
actual del TG.** El archivo **ya está en esa ruta** (verificado 2026-07-15 19:10); antes estaba
suelto en `docs/` raíz.

**Lo que sigue roto en git:**

```
RD docs/anteproyecto/anteproyecto.docx -> "docs/anteproyecto/AnteProyecto Cancer de mama (2).docx"
?? "docs/anteproyecto/AnteProyecto Cancer de mama (3).docx"
```

- `RD` = rename **en staging** cuyo destino (`…(2).docx`) **no existe en el working tree**.
  **Commitear así commitea el borrado** del material fuente del TG.
- El `(3)` está **sin trackear**: git aún no lo conoce.
- **Hay que resolver ambas cosas a la vez**: deshacer/rehacer el rename para que apunte al `(3)`
  real y quede `git add`-eado. Idealmente que git lo registre como **rename** de
  `anteproyecto.docx` → `(3)`, para no perder la historia del archivo.

> Nota de convención (no bloqueante, decisión del equipo ya tomada): el `(3)` es un artefacto de
> descarga del navegador, y la próxima versión bajará como `(4)` — que git verá como archivo nuevo
> sin relación con el anterior, perdiendo historia. El precedente del repo era **normalizar** el
> nombre (`docs/superpowers/plans/2026-07-12-gobernanza-docs-claude.md` copiaba
> `AnteProyecto Cancer de mama (1).docx` → `anteproyecto.docx`). Si el equipo quisiera volver a esa
> convención, este es el momento; si no, **la ruta canónica es la de arriba** y así debe quedar en
> toda la documentación.

### 6.3 Referencias obsoletas al nombre viejo (`anteproyecto.docx`) — **a corregir**

El archivo se llamaba `anteproyecto.docx`. **Cuatro documentos siguen citando ese nombre**, que ya
no existe. Actualizar a la ruta canónica de §6.2:

| Archivo | Línea | Qué dice |
|---|---|---|
| `docs/anteproyecto/README.md` | 5 | *"`anteproyecto.docx` — anteproyecto formal (USC)…"* — **describe el contenido de la carpeta**: es el más importante de corregir |
| `docs/auditoria-alineacion-profesor.md` | 23 | lista `docs/anteproyecto/anteproyecto.docx` entre los documentos revisados |
| `docs/auditoria-alineacion-profesor.md` | 235 | evidencia de **B-008**: *"el documento `anteproyecto.docx` conserva objetivos de entrenar modelos multimodales…"* |
| `docs/handoff-estado-y-roadmap.md` | 96 | **B-008**: *"`anteproyecto.docx` aún promete modelos multimodales…"* |

**No tocar** `docs/superpowers/plans/2026-07-12-gobernanza-docs-claude.md` (líneas 176, 190, 203):
es un **plan histórico**, registro de lo que se hizo en su momento. El repo no reescribe documentos
históricos (misma regla que aplica a `docs/anteproyecto/*` en `alcance-vigente.md`).

> Ojo al corregir las de **B-008**: el hallazgo sigue vigente y no depende del nombre del archivo —
> solo cambia el nombre con que se lo cita. **No convertir un cambio de ruta en un cierre de B-008.**

## 7. Fuentes analizadas

- **GPC Minsalud/Colciencias, Guía No. 19 (2013)** — *Detección temprana, tratamiento integral,
  seguimiento y rehabilitación del cáncer de mama*. 930 pp. **Anexo 9 = Clasificación TNM (AJCC 7,
  pp. 923–929 del PDF)**; §2.2 tamización; cap. 9 evaluación económica.
  `https://www.minsalud.gov.co/sites/rid/1/Gu%C3%ADa%20de%20Pr%C3%A1ctica%20Cl%C3%ADnica%20%20de%20Cancer%20de%20Mama%20versi%C3%B3n%20completa.pdf`
- **Cuenta de Alto Costo (2025)** — *Actualización del consenso basado en la evidencia: indicadores
  mínimos… cáncer de mama en Colombia*, abril 2025, 90 pp. Glosario TNM (origen literal de la
  definición del correo); indicadores mínimos incl. **estadio al diagnóstico**.
  `https://cuentadealtocosto.org/wp-content/uploads/2025/04/actualizacion-del-consenso-de-cancer-de-mama-2025.pdf`
- **NCI** — `https://www.cancer.gov/types/breast/stages/tnm-staging-system` (T y pN; **no** trae
  grupos de estadio ni pronóstico).
- **Medwave, curso 3486** — `https://www.medwave.cl/puestadia/cursos/3486.html` (TNM en cm, AJCC
  antiguo; útil como material docente, no como norma).
- **AJCC 8** — ver §4.3.

### 7.1 Datos colombianos útiles (de la GPC / CAC)

- **Tamizaje (GPC, recomendación fuerte):** mamografía de **dos proyecciones cada 2 años en mujeres
  de 50–69**, dentro de programa organizado. **No** rutina en 40–49 (decisión individual).
- **Falsos positivos esperados (GPC Tabla 9.15/9.22):** mamografía **5 %** (3–11 %); examen clínico
  10 % (3–16 %).
- **Perfil al diagnóstico (GPC Tabla 9.21/9.14):** RH+ **66 %**, HER2+ **20 %**; sin ganglios
  **65 %**, 1–3 ganglios **20 %**, ≥4 ganglios **15 %**. *Priors* poblacionales para detectar
  distribuciones implausibles — **no** son reglas de decisión.

## 8. Trabajo pendiente

Ordenado por dependencia. **Regla de gobernanza que aplica a casi todo:** el roadmap exige **crear
el issue antes de tocar `docs/requisitos.md`**; el catálogo se actualiza solo con issue y
evidencia/aprobación.

### 8.1 Trazabilidad (bloquea al resto)

- [ ] **Crear los issues** de los frentes TNM. Sin issue, `requisitos.md` no se toca.
- [ ] **Agregar los requisitos** a `docs/requisitos.md` (IDs siguientes libres: **RF-009**, **RF-010**;
      no reciclar IDs). Propuesta:
      - **RF-009** — *Motor de estadificación TNM (AJCC 8)*: valida la tupla `(T,N,M)`, rechaza
        combinaciones imposibles y calcula el grupo pronóstico (clínico/patológico según contexto de
        tratamiento). Determinista, sin ML. Módulo sugerido: nuevo (p. ej. `services/staging`) o
        `packages/`.
      - **RF-010** — *Estimación de `cT` desde mamografía*: diámetro mayor en mm + incertidumbre,
        requiere `PixelSpacing`; sale como **propuesta** marcada, prefijo `c`, nunca `pT`.
- [ ] **Actualizar `docs/psp/traceability.md`** (es **vista derivada** de `requisitos.md`, nunca la
      contradice, se actualiza en el mismo commit/PR).
- [x] ~~**ADR-0006 pasa de `Propuesta` a `Aceptada`** cuando el director valide el alcance.~~
      **Superado por la nota del encabezado — el criterio cambió, leerlo con cuidado.** El ADR **ya
      está `Aceptada`**, pero **el director no validó**: la aceptó el **equipo** el 2026-07-15 para
      desbloquear el trabajo, y el ADR lo declara explícitamente. **No leer esta casilla marcada como
      "el director validó".** La validación del director **sigue pendiente** y se rastrea en §8.5 y
      en `roadmap-tg.md` ("Única evidencia pendiente"), donde es la **misma** evidencia que RNF-002.

### 8.2 Contrato

- [ ] Extender `packages/contracts/schemas/models.json` (**fuente de verdad**) con el tipo de
      estadificación: `cT`/`cN`/`cM`, grado (Nottingham), RE, RP, HER2, y **contexto de tratamiento**
      (obligatorio: decide tabla clínica vs patológica).
- [ ] **Dato ausente = `null`/`"unknown"`**, nunca `X`. **No** aceptar `cMX` (no existe). **No** usar
      `cNX` como "no evaluado" (§3.1, §3.3).
- [ ] Regenerar pydantic con `just gen-contracts` — **nunca editar el generado a mano** (RNF-003).

### 8.3 Documentación

- [ ] `docs/architecture/contracts.md` — documentar el tipo de estadificación.
- [ ] `docs/architecture/overview.md` — ubicar el motor en el mapa diseño↔hoy↔futuro; dejar claro que
      **se dispara sobre cáncer confirmado por biopsia**, no sobre la salida del modelo.
- [ ] `docs/alcance-vigente.md` — reconciliar: el TNM **no altera** la rebanada vertical ni la meta
      AUC-ROC ≥0.92; es función desacoplada. (La estimación de `cT` **sí** toca el pipeline de
      mamografía.)
- [ ] `docs/roadmap-tg.md` — ubicar el frente TNM sin desplazar Fase 1.
- [ ] `docs/requisitos.md` — ver §8.1.
- [ ] Evaluar si `RNF-006` (INVIMA) necesita nota: **emitir un estadio es afirmación clínica de mayor
      riesgo que un triaje** → sube el perfil SaMD y refuerza transparencia/responsabilidad OMS
      (RNF-007). El disclaimer RNF-008 **no** sustituye ese análisis.

### 8.4 Anteproyecto (frente inmediato del roadmap, <15 días desde 2026-07-12 → ~2026-07-27)

- [ ] **El material de esta sesión alimenta directo el marco legal / estado del arte**: GPC Minsalud,
      consenso CAC 2025 y AJCC 8, ya con cita y con las divergencias mapeadas. Es el uso de mayor
      palanca de esta investigación.
- [ ] Referencias APA de las fuentes de §7.
- [ ] **Ruta canónica del anteproyecto:** `docs/anteproyecto/AnteProyecto Cancer de mama (3).docx`
      (§6.2). El archivo ya está ahí; falta **resolver el rename roto en staging y trackearlo**.
- [ ] **Actualizar las 4 referencias obsoletas** a `anteproyecto.docx` (§6.3) — empezando por
      `docs/anteproyecto/README.md`, que describe el contenido de la carpeta.

### 8.5 Comunicación con el director

- [ ] **Responder el hilo del 2026-07-15.** Contenido mínimo: (a) el sistema **puede** proponer `cT`
      y **validar/calcular** el estadio como motor de reglas alimentado por datos clínicos; (b) **no
      puede** inferir `cN`/`cM` desde mamografía ni validar TNM contra CBIS-DDSM; (c) se adopta
      **AJCC 8** (su Anexo 9 es AJCC 7).
- [ ] **Oportunidad de doble propósito:** el roadmap dice que la **única evidencia pendiente** del
      proyecto es registrar la aprobación del director del alcance y de **AUC-ROC ≥0.92**, y sugiere
      *"enviar un correo de recapitulación"*. **Ya hay un hilo vivo con él.** Responder ese hilo con
      la delimitación del TNM **más** la recapitulación del alcance **cierra ambas cosas de una vez**.
- [ ] Sin reproducir datos personales en el repo (§1).

### 8.6 Implementación (después de §8.1–8.2)

- [ ] Motor determinista dirigido por tabla + tests de **cobertura exhaustiva** de la tabla de verdad.
- [ ] Manejo explícito de los casos **sin grupo de estadio** (§5.1).
- [ ] Reglas de normalización previas a la tabla (§5.1).
- [ ] Cotejar las tablas pronósticas contra el **capítulo 48 corregido** (§4.3), **no** contra las
      láminas educativas.

## 9. Convenciones que aplican a este trabajo

- **Commits en español:** `tipo(#N): descripción` (hook `.githooks/commit-msg`).
- **Sin atribución a IA** en ningún artefacto — regla firme (`CLAUDE.md`, `docs/psp/conventions.md`).
- **Contratos:** `packages/contracts/schemas/*.json` es la fuente; el pydantic se genera.
- **PHI:** nunca loguear `case_ref`, rutas DICOM/WSI, `result_json` ni URLs de Storage.
- **DoR/DoD:** `docs/psp/definition-of-ready.md` · `docs/psp/definition-of-done.md`.

## 10. Documentos relacionados

- [`clinical/tnm.md`](clinical/tnm.md) — **fuente clínica única** de TNM.
- [`adr/0006-estadificacion-tnm-ajcc8-pronostica.md`](adr/0006-estadificacion-tnm-ajcc8-pronostica.md) — la decisión.
- [`requisitos.md`](requisitos.md) · [`alcance-vigente.md`](alcance-vigente.md) ·
  [`roadmap-tg.md`](roadmap-tg.md) · [`handoff-estado-y-roadmap.md`](handoff-estado-y-roadmap.md) —
  contexto de continuidad anterior.
