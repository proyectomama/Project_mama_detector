# Estadificación TNM del cáncer de mama — referencia clínica

**Fecha:** 2026-07-15
**Estado:** referencia clínica vigente. Fuente única de la nomenclatura TNM en este repo.
**Origen:** solicitud del director (correo del 2026-07-15): *"Tener en cuenta la clasificación TNM
del cáncer de mama. El software diagnosticará de manera temprana el cáncer de mama y eso requiere
identificar y validar el TNM"*, con instrucción de analizar la GPC del Minsalud.

> Este documento **no** convierte al sistema en una herramienta de estadificación clínica. Define
> qué es el TNM, qué parte de él el sistema puede tocar honestamente, y qué parte **no es
> inferible** desde una mamografía. mama-detector no es un dispositivo médico certificado.

---

## 1. Qué es el TNM

Sistema que determina el grado de diseminación del cáncer: **T** = tamaño del tumor y su extensión
local; **N** = afectación de ganglios linfáticos locorregionales; **M** = presencia de metástasis
(definición literal del glosario del [consenso CAC 2025](#5-fuentes)).

El TNM es **ortogonal a BI-RADS**. BI-RADS gradúa la *sospecha* de un estudio de imagen (0–6) y
guía la conducta diagnóstica; TNM describe la *extensión anatómica de un cáncer ya diagnosticado*.
Un BI-RADS 5 no es un estadio, y no existe función que convierta BI-RADS en TNM. Confundirlos es
un error clínico, no una imprecisión de nomenclatura.

## 2. Edición normativa: AJCC 8 (no AJCC 7)

**Para este repo, la edición normativa es AJCC 8.ª (vigente desde 2018-01-01).**

El **Anexo 9 de la GPC del Minsalud (Guía No. 19, 2013)** reproduce la **AJCC 7.ª ed. (2010)**. Es
la fuente colombiana que pidió el director, pero está **desactualizada** en puntos que cambian el
resultado. Divergencias que importan:

| Punto | AJCC 7 (GPC 2013, Anexo 9) | AJCC 8 (vigente) |
|-------|----------------------------|------------------|
| CLIS / LCIS | `Tis (CLIS)` es categoría válida | **Eliminado**. LCIS es entidad benigna, no se estadifica. In situ solo `Tis (CDIS)` o `Tis (Paget)` |
| Redondeo de tamaño | "un tumor de 1,1 mm se notifica como 1 mm" → caería en `T1mi` | **>1.0–1.4 mm redondea a 2 mm** → `T1a`. `T1mi` solo puede representar **≤1 mm** |
| Estadio pronóstico | No existe | Añadido: anatómico **+ grado Nottingham + RE + RP + HER2** (+ Oncotype DX) |
| Tabla anatómica | Es la única tabla | Se conserva, pero **solo para regiones sin acceso a biomarcadores** |

**Consecuencia de la última fila —y es la más importante de este documento:** AJCC 8 es explícita
en que la tabla de estadio **anatómico** *"ONLY for global regions where biomarker tests
unavailable"*, y que no debe usarse aunque falten los factores pronósticos, porque sesga los datos.
Colombia **sí** tiene tamizaje de biomarcadores (el consenso CAC 2025 reporta indicadores de RH y
HER2). Por lo tanto, en el contexto colombiano el estadio válido es el **pronóstico**, que exige
grado histológico y RE/RP/HER2 — es decir, **exige biopsia**, no imagen.

> **Verificado (2026-07-15):** la tabla de estadio **anatómico** de la §3.5 es **idéntica** en AJCC
> 7 y AJCC 8 — se cotejaron las 19 filas del Anexo 9 de la GPC contra las *Anatomic Staging
> Groupings* del material oficial AJCC/ACS ([Physician to Physician, Breast, 8th
> ed.](https://www.facs.org/media/u4djjc4v/breast-8th-ed.pdf), láminas 23–24). Lo que cambió no es
> la tabla anatómica: es **qué tabla se debe usar**. Las tablas **pronósticas** (clínica y
> patológica) están en ese mismo material, láminas 39–49.
>
> ⚠️ **Aviso de derechos — más restrictivo de lo que parece.** El capítulo oficial de AJCC 8 lleva
> esta nota: *"Content is available for user's personal use. It cannot be sold, distributed,
> published, or **incorporated into any software, product, or publication** without a written
> license agreement with ACS."* Dice **explícitamente "software"**: codificar las tablas
> **pronósticas** en el motor de estadificación cae dentro de esa frase, y "citar la fuente" no
> alcanza — apuntaría a una licencia escrita con ACS (hay proceso de permisos en `cancerstaging.org`).
>
> Postura vigente del proyecto (decisión del equipo, 2026-07-15):
> - **Uso interno y académico del TG:** no es bloqueante. Se codifican las tablas necesarias
>   citando la fuente. **Si el proyecto llegara a aliarse con clínicas** o a cualquier uso fuera de
>   lo académico, la cláusula de *"incorporated into any software"* se evalúa a fondo **antes** de
>   ese paso — queda registrado como deuda consciente, no como descuido.
> - **Tabla anatómica → se toma de la GPC del Minsalud**, documento público del Estado colombiano
>   que ya obtuvo permiso (*"Reproducido con permiso del AJCC"*). Procedencia más limpia.
> - **No se versiona el PDF del capítulo AJCC en este repo**: publicarlo en un repositorio sería
>   *distribuir*. Se cita por URL.

> **Versión del capítulo — resuelto, pero conviene entenderlo.** El capítulo 48 (*Breast*) de AJCC 8
> **se reemplazó entero** después de la primera impresión del manual. Según la hoja oficial de
> erratas, la única entrada *Critical* de mama es:
>
> | Print Run | Tipo | Publicada | Antes | Después |
> |---|---|---|---|---|
> | **1** | **Critical** | **2018-02-02** | Sistema de grado único para in situ e invasivo; **grupos de estadio pronóstico con combinaciones faltantes** | Grados distintos para in situ e invasivo; **nuevos grupos pronósticos clínico y patológico** con datos adicionales del NCDB |
>
> (La otra entrada de mama es un typo de la Tabla 48.1 en la 3.ª impresión, `cPR y pCR` → `cPR y
> pPR`, 2018-03-29. La entrada de 2021 de la hoja es de *Soft Tissue Sarcoma*, no de mama.)
>
> Consecuencias prácticas:
> - **No existe una "versión 2021" de AJCC 8.** Lo que varía es la **impresión** del manual (1.ª,
>   2.ª, 3.ª). 2021 es solo la última fecha de revisión de la *hoja* de erratas.
> - La errata *Critical* de mama afecta a la **1.ª impresión** y ya está resuelta: el capítulo
>   corregido (*Last updated 01/25/2018*, páginas **589–636** = rango de la 3.ª impresión) es la
>   fuente normativa.
> - Las **láminas educativas** citadas abajo **no son normativas** y son anteriores a esa
>   corrección: no se codifican tablas pronósticas desde ellas.
> - La tabla **anatómica no está afectada** por ninguna errata de mama, y aquí se toma de la GPC.

## 3. Categorías

### 3.1 Tumor primario (T)

La clasificación T es la misma sea clínica o patológica; se mide **al milímetro más cercano** y se
prefija con `c` (clínico: examen físico o radiológico) o `p` (patológico). **La determinación
patológica prevalece sobre la clínica.**

| Categoría | Definición |
|-----------|------------|
| `TX` | No se puede evaluar el tumor primario |
| `T0` | No hay prueba de tumor primario |
| `Tis (CDIS)` | Carcinoma ductal in situ |
| `Tis (Paget)` | Enfermedad de Paget del pezón **sin** carcinoma invasivo ni in situ subyacente. Si hay carcinoma parenquimatoso asociado, se clasifica por ese tumor |
| `T1` | ≤20 mm |
| `T1mi` | ≤1 mm (microinvasión) |
| `T1a` | >1 mm y ≤5 mm |
| `T1b` | >5 mm y ≤10 mm |
| `T1c` | >10 mm y ≤20 mm |
| `T2` | >20 mm y ≤50 mm |
| `T3` | >50 mm |
| `T4` | Cualquier tamaño con extensión directa a pared torácica o piel (ulceración o nódulos cutáneos) |
| `T4a` | Extensión a pared torácica (no basta adherencia/invasión de músculos pectorales) |
| `T4b` | Ulceración, nódulos satélites ipsilaterales o edema (piel de naranja) que no cumple criterio de carcinoma inflamatorio |
| `T4c` | T4a **y** T4b |
| `T4d` | Carcinoma inflamatorio |

Reglas que un validador debe hacer cumplir:
- La invasión de la dermis **por sí sola no** califica como T4.
- Redondeo AJCC 8: un tumor **>1.0 mm nunca se redondea hacia abajo a `T1mi`** (1.1–1.4 mm → 2 mm →
  `T1a`). En general se redondea hacia abajo entre 1–4 y hacia arriba entre 5–9. `T1mi` **solo**
  para ≤1 mm.
- **Tumores múltiples:** sufijo `(m)`; se usa la dimensión del **mayor**, no la suma.
- **`T4b`:** los nódulos satélites deben estar **separados** del primario e identificarse
  **macroscópicamente**. Los vistos solo al microscopio **no** califican como `T4b`.
- `T1` incluye `T1mi` a efectos de agrupación por estadio.

### 3.2 Ganglios regionales — clínico (cN)

`cN` se determina por examen físico o **imagen** (excluyendo linfocentellografía). "Detectado
clínicamente" exige características altamente sospechosas o macrometástasis presunta por BACAF con
citología. Confirmación por BACAF sin biopsia escisional → sufijo `(f)`, p. ej. `cN3a(f)`.

**Reglas AJCC 8 sobre `cN0`/`cNX` — críticas para este sistema:**
- **`cN0` se asigna cuando la evaluación ganglionar *es posible*** (examen físico o imagen) **y sale
  negativa**. No es un valor por defecto.
- **`cNX` solo es válido si la cuenca ganglionar fue extirpada** y por eso no puede examinarse.
  **`cNX` NO significa "no lo evaluamos"**: si los ganglios son evaluables y nadie los evaluó, la
  categoría es **desconocida/ausente**, no `cNX`.

| Categoría | Definición |
|-----------|------------|
| `NX` | No evaluable **por extirpación previa de la cuenca ganglionar** (no aplica a "no se examinó") |
| `N0` | Evaluación posible y negativa: sin metástasis ganglionar regional |
| `N1` | Metástasis en ganglios axilares ipsilaterales niveles I–II, **móviles** |
| `N2` | Axilares I–II **fijos o apelmazados**; **o** mamarios internos detectados clínicamente sin metástasis axilar manifiesta |
| `N2a` | Axilares I–II fijos entre sí o a otras estructuras |
| `N2b` | Solo mamarios internos detectados clínicamente, sin metástasis axilar I–II manifiesta |
| `N3` | Infraclaviculares (nivel III); **o** mamarios internos detectados clínicamente **con** metástasis axilar I–II manifiesta; **o** supraclaviculares |
| `N3a` | Infraclaviculares ipsilaterales |
| `N3b` | Mamarios internos **y** axilares ipsilaterales |
| `N3c` | Supraclaviculares ipsilaterales |

### 3.3 Ganglios regionales — patológico (pN)

Requiere disección axilar y/o biopsia de ganglio centinela. Sufijo `(sn)` si la clasificación se
basa solo en centinela (p. ej. `pN0(sn)`). Umbrales de depósito tumoral:

- **Macrometástasis:** >2 mm
- **Micrometástasis:** >0.2 mm y ≤2 mm (o >200 células)
- **Células tumorales aisladas (ITC):** ≤0.2 mm o <200 células en un corte histológico

Los ganglios con solo ITC **se excluyen** del recuento de nódulos positivos, pero **se incluyen** en
el total de nódulos evaluados.

| Categoría | Definición |
|-----------|------------|
| `pNX` | No evaluables |
| `pN0` | Sin metástasis regional por histología |
| `pN0(i-)` | Sin metástasis, IHQ negativa |
| `pN0(i+)` | Células malignas ≤0.2 mm (H&E o IHQ, incluye ITC) |
| `pN0(mol-)` | Sin metástasis, RT-PCR negativa |
| `pN0(mol+)` | RT-PCR positiva, sin metástasis por histología ni IHQ |
| `pN1mi` | Micrometástasis (>0.2 mm o >200 células, ninguna >2.0 mm) |
| `pN1a` | 1–3 axilares, al menos una >2.0 mm |
| `pN1b` | Mamarios internos por centinela (micro o macro), sin detección clínica |
| `pN1c` | `pN1a` + `pN1b` |
| `pN2a` | 4–9 axilares (al menos un depósito >2 mm) |
| `pN2b` | Mamarios internos detectados clínicamente, sin metástasis axilar |
| `pN3a` | ≥10 axilares (al menos uno >2.0 mm); **o** infraclaviculares (nivel III) |
| `pN3b` | >3 axilares + mamarios internos (detectados clínicamente, o por centinela sin detección clínica) |
| `pN3c` | Supraclaviculares ipsilaterales |

### 3.4 Metástasis a distancia (M)

**Las únicas categorías M válidas son `cM0`, `cM1` y `pM1`. No existe `MX`/`cMX`** — no se debe
emitir ni aceptar en contratos.

| Categoría | Definición |
|-----------|------------|
| `cM0` | **Sin signos ni síntomas** de metástasis a distancia (juicio clínico; no exige TC/PET) |
| `cM0(i+)` | Sin prueba clínica/radiográfica, pero con depósitos moleculares o microscópicos ≤0.2 mm en sangre circulante, médula ósea u otros tejidos no regionales, en paciente **sin** signos ni síntomas |
| `cM1` | Signos, síntomas o evidencia imagenológica de metástasis a distancia |
| `pM1` | Confirmación **microscópica** de metástasis a distancia (>0.2 mm) |

**`pM0` no es válido: todo `M0` es clínico.** Si la paciente es `M1` antes de terapia neoadyuvante,
permanece estadio IV independientemente de la respuesta.

> Matiz importante: `cM0` es "sin signos ni síntomas", una **valoración clínica** — no requiere
> estadificación sistémica completa. Eso **no** lo hace inferible por el sistema: sigue siendo el
> juicio de un clínico sobre historia y examen físico, no una salida de un modelo de imagen.

### 3.5 Grupos de estadio anatómico

Reproducido de la GPC, Anexo 9, Cuadro 5. **Verificado idéntico en AJCC 7 y AJCC 8** (ver §2): las
19 filas coinciden con las *Anatomic Staging Groupings* del material oficial AJCC/ACS. Es
implementable tal cual; lo que hay que decidir con cuidado es **cuándo se puede usar esta tabla**.

| Estadio | T | N | M |
|---------|---|---|---|
| 0 | Tis | N0 | M0 |
| IA | T1 | N0 | M0 |
| IB | T0 | N1mi | M0 |
| IB | T1 | N1mi | M0 |
| IIA | T0 | N1 | M0 |
| IIA | T1 | N1 | M0 |
| IIA | T2 | N0 | M0 |
| IIB | T2 | N1 | M0 |
| IIB | T3 | N0 | M0 |
| IIIA | T0 | N2 | M0 |
| IIIA | T1 | N2 | M0 |
| IIIA | T2 | N2 | M0 |
| IIIA | T3 | N1 | M0 |
| IIIA | T3 | N2 | M0 |
| IIIB | T4 | N0 | M0 |
| IIIB | T4 | N1 | M0 |
| IIIB | T4 | N2 | M0 |
| IIIC | Cualquier T | N3 | M0 |
| IV | Cualquier T | Cualquier N | M1 |

Notas normativas:
- `T1` incluye `T1mi`.
- **T0 y T1 con solo micrometástasis nodal (`N1mi`) se excluyen de IIA y se clasifican IB.**
- `M0` incluye `cM0(i+)`.
- Terapia posneoadyuvante se prefija `yc`/`yp`. **No se asigna grupo de estadio** a la respuesta
  patológica completa (`ypT0 ypN0 cM0`) ni, en AJCC 8, a ninguna estadificación posterapia.

### 3.6 Estadio pronóstico (AJCC 8) — el cambio de fondo

Entradas: TNM anatómico **+ grado Nottingham (G1–G3) + RE + RP + HER2** (+ perfil genómico en la
tabla patológica). Reglas:

- El grado **debe ser Nottingham/SBR modificado** (túbulos + pleomorfismo nuclear + mitosis), **no**
  grado nuclear. Con solo grado nuclear **no se asigna grupo de estadio**.
- **RE/RP:** positivos con **>1 %** de células teñidas por IHQ. Si hay resultados múltiples (biopsia
  y resección) y uno es positivo, **prevalece el positivo**.
- **HER2:** por IHQ o ISH según estándar ASCO/CAP 2013. IHQ 0/1+ negativo · 2+ equívoco · 3+
  positivo. **HER2 "equívoco" por ISH se categoriza como HER2 negativo** para asignar estadio.
- **Clinical prognostic stage:** historia, examen físico, imagen, biopsias y biomarcadores. Se
  determina **antes de cualquier tratamiento** y aplica a *todos* los pacientes, incluidos los que
  recibirán tratamiento preoperatorio.
- **Pathological prognostic stage:** hallazgos de la cirugía definitiva + biomarcadores. Solo si la
  cirugía es el tratamiento inicial; **no aplica** tras neoadyuvancia. Es el sistema **recomendado
  para todos los registros de tumores en EE. UU.**
- Las tablas clínica y patológica **difieren** para la misma combinación (ver §3.7).
- **Perfil genómico:** con evidencia Nivel 1 (ensayo de 21 genes), un **Oncotype DX <11** en
  **T1–2 N0 M0, RE+, HER2−, cualquier grado, cualquier RP** → estadio patológico **IA**. Los demás
  paneles (MammaPrint, ProSigna, EndoPredict, Breast Cancer Index, IHC4) aportan información
  pronóstica similar pero **no se usan para asignar estadio**, por falta de datos de ese nivel.
- **Posneoadyuvancia:** los grupos pronósticos posneoadyuvantes estaban **en preparación** en la
  publicación de AJCC 8; se asignan `ypT`/`ypN` pero **no hay grupo de estadio**.

Las tablas completas (clínica y patológica) están en el material oficial AJCC/ACS ya citado,
láminas 39–49 — ver el aviso de derechos de la §2 antes de codificarlas.

### 3.7 Por qué el estadio pronóstico cambia el resultado

Ejemplos oficiales del AJCC (mismo TNM anatómico, biología distinta):

| Caso | TNM | Anatómico | Clínico pronóstico | Patológico pronóstico |
|------|-----|-----------|-----------|--------------------|
| G3, RE− RP− HER2− (triple negativo) | pT1 N1 M0 | **IIA** | **IB** | **IIA** |
| G1, RE+ RP+ HER2+ | pT1 N1 M0 | **IIA** | **IA** | **IA** |
| G1, RE+ RP+ HER2+ | pT3 N1 M0 | **IIIA** | **IIA** | **IB** |
| G2, RE+ RP− HER2−, Oncotype 9 | pT2 N0 M0 | **IIA** | IIA | IIA → **IA** (modificador genómico) |

El tercer caso salta de **IIIA anatómico a IB patológico**: dos grupos completos, por biología. Y un
mismo `T3 N2 M0` (IIIA anatómico) puede caer en cualquier grupo entre **IA y IIIA** según grado y
biomarcadores. Ese es exactamente el problema que AJCC 8 vino a resolver: la anatomía sola no
predice el pronóstico. Por eso la tabla anatómica no cambió y aun así "todo cambió".

## 4. Qué puede y qué no puede hacer este sistema

Esta sección es la que gobierna el diseño. La rebanada vertical del TG es **mamografía 2D sobre
CBIS-DDSM** (ver [`alcance-vigente.md`](../alcance-vigente.md)).

| Componente | ¿Inferible desde mamografía 2D? | Justificación |
|------------|----------------------------------|---------------|
| **cT** | **Parcial — estimable** | El diámetro mayor de la lesión es medible sobre la imagen si hay `PixelSpacing`/`ImagerPixelSpacing` en el DICOM. Es una **estimación radiológica con incertidumbre**, se emite como `cT` y **nunca** como `pT` |
| **cN** | **No** | Las proyecciones CC/MLO de tamizaje no cubren la axila de forma fiable. La evaluación ganglionar exige ecografía axilar, RM, BACAF o ganglio centinela. Y `cN0` exige que la evaluación *se haya hecho* y sea negativa |
| **cM** | **No** | `cM0` es "sin signos ni síntomas": una valoración clínica sobre historia y examen físico, no una salida de un modelo de imagen. `cM1` exige evidencia clínica o radiográfica |
| **Grado Nottingham** | **No** | Requiere histología. **Se recibe** del informe de patología como dato estructurado |
| **RE / RP / HER2** | **No** | Requieren inmunohistoquímica sobre biopsia. **Se reciben** del informe de patología |
| **Grupo de estadio** | **No se infiere — se calcula** | El motor lo computa a partir de las entradas anteriores. Sin `N`, `M`, grado y biomarcadores completos, no hay estadio |

**Conclusión operativa: el sistema no puede emitir un estadio TNM a partir de una mamografía.**
Cualquier salida que lo afirme es un defecto clínico bloqueante.

> **Inferir ≠ recibir.** Esta distinción gobierna todo el diseño y es fácil de colapsar. Que el
> sistema no pueda *inferir* un biomarcador desde una imagen **no** significa que no pueda *usarlo*:
> RE/RP/HER2 y el grado llegan como **entrada estructurada del informe de patología**, igual que
> `cN`/`cM` llegan del clínico. Así opera cualquier sistema clínico real — el laboratorio mide, el
> informe reporta, el software recibe. No hay inferencia en el medio, y el motor sigue siendo
> determinista y sin ML.
>
> Corolario: **RF-006 no es prerrequisito del estadio pronóstico.** RF-006 es *inferir* desde WSI
> (BreakHis/TCGA-BRCA) y es trabajo futuro — además, BreakHis no tiene etiquetas de biomarcadores.
> Para el estadio pronóstico no hace falta un modelo: hace falta un **campo en el contrato**.

### 4.1 CBIS-DDSM no tiene etiquetas TNM

CBIS-DDSM aporta: densidad, tipo de anormalidad (masa/calcificación), **evaluación BI-RADS**,
patología (`BENIGN` / `BENIGN_WITHOUT_CALLBACK` / `MALIGNANT`), sutileza y máscaras de ROI. **No
contiene** estadio TNM, estado ganglionar, metástasis ni biomarcadores.

Por lo tanto **no se puede entrenar ni validar estadificación TNM contra CBIS-DDSM**. Afirmar
"validamos el TNM" con este dataset sería una afirmación sin evidencia posible. Validar TNM de
verdad exigiría una cohorte con estadificación patológica confirmada — otro dataset y otro alcance.

### 4.2 Lo que sí es implementable y verificable

Lo que responde con rigor a *"identificar y validar el TNM"* sin prometer lo imposible:

1. **Motor de estadificación determinista** (función pura, dirigida por tabla): valida que una
   tupla `(T, N, M)` esté bien formada, rechaza combinaciones imposibles, y calcula el grupo de
   estadio. Sin ML, 100 % testeable contra la tabla de verdad — encaja con PSP.
2. **Estimación de `cT`** desde la lesión detectada (diámetro mayor en mm + incertidumbre), como
   *propuesta* al radiólogo, marcada como estimación radiológica.
3. **`cN`/`cM`, grado y biomarcadores como entrada estructurada** del clínico o del informe de
   patología — nunca inventados, nunca inferidos desde imagen.
4. **Negativa explícita a estadificar** cuando falte cualquier entrada obligatoria: el resultado
   correcto es *"estadio no determinable — dato ausente"*.

**Decisión vigente (2026-07-15): se implementan las tablas pronósticas (Opción B).** Dado que
AJCC 8 restringe la tabla anatómica a regiones sin acceso a biomarcadores y Colombia sí los tiene,
emitir solo estadio anatómico sería usar la tabla que el estándar desaconseja. El motor acepta
grado + RE/RP/HER2 como entrada estructurada y calcula el **estadio pronóstico**. Ver ADR-0006.

Lo que esa decisión obliga a resolver, y conviene tener presente antes de codificar:

- **Son dos tablas, no una.** Clínica y patológica dan resultados distintos para la misma
  combinación (§3.7). El motor necesita saber **cuál aplica**, y eso depende del **contexto de
  tratamiento**: la clínica aplica a todo paciente antes de cualquier tratamiento; la patológica
  solo si la cirugía fue el tratamiento inicial. Eso es una entrada más del contrato, no un detalle.
- **Hay casos sin estadio asignable**, y el motor debe representarlos en vez de forzar un valor:
  grado nuclear en lugar de Nottingham → sin grupo; posneoadyuvancia (`ypT`/`ypN`) → sin grupo;
  respuesta patológica completa → sin grupo.
- **Reglas de normalización previas a la tabla:** HER2 equívoco por ISH → negativo; RE/RP positivos
  con >1 %; si biopsia y resección discrepan, prevalece el positivo.
- **La validación no necesita cohorte clínica.** Al ser determinista, se prueba por **cobertura
  exhaustiva de la tabla de verdad**: todas las combinaciones de TNM × grado × HER2 × RE × RP. Es
  verificación completa, no muestreo estadístico — un artefacto PSP excepcionalmente fuerte, y una
  diferencia de fondo con la evaluación del modelo de mamografía (que sí es estadística).
- **El límite de la afirmación no se mueve:** el motor *calcula* el estadio a partir de datos que
  recibe; no los mide ni los verifica. La plataforma no determina el estadio de una mamografía.

Sobre cómo representar ese dato ausente, cuidado con dos trampas de nomenclatura:

- **`cNX` no es "no evaluado".** AJCC 8 lo reserva para cuando la cuenca ganglionar fue extirpada.
  Si nadie evaluó la axila, la categoría es **ausente/desconocida**, y así debe modelarse el
  contrato (`null` / `"unknown"`), **no** `cNX`.
- **`cMX` no existe.** Las únicas categorías M válidas son `cM0`, `cM1` y `pM1`. Un contrato que
  acepte `cMX` está mal formado.

Un `cM0` (o `cN0`) asumido por silencio es el modo de fallo más peligroso de este diseño: convierte
"no sabemos" en "no hay enfermedad". Y como `cN0`/`cM0` son afirmaciones **positivas** de que la
evaluación se hizo y salió negativa, ponerlas por defecto no es un atajo: es fabricar un hallazgo
clínico.

## 5. Contexto colombiano

- **Tamizaje (GPC 2013, recomendación fuerte):** mamografía de **dos proyecciones cada dos años en
  mujeres de 50 a 69 años**, dentro de un programa organizado. **No** se recomienda tamizaje de
  rutina en 40–49 años (decisión individual). Un sistema de triaje que opere fuera de esa ventana
  debe declararlo.
- **Falsos positivos esperados (GPC, Tabla 9.15/9.22):** mamografía **5 %** (rango 3–11 %); examen
  clínico 10 % (3–16 %).
- **Perfil al diagnóstico (GPC, Tabla 9.21):** RH+ 66 %, HER2+ 20 %; sin ganglios 65 %, 1–3
  ganglios 20 %, ≥4 ganglios 15 %. Útil como *prior* poblacional y para detectar distribuciones
  implausibles; no es una regla de decisión.
- **Consenso CAC 2025:** define los indicadores mínimos de gestión del riesgo, incluido el
  **estadio al diagnóstico**. Es el marco de reporte al que tendría que alinearse cualquier salida
  con pretensión de uso real en Colombia.

### 5.1 Aviso: las tablas del modelo económico no son reglas de estadificación

La GPC contiene, en su capítulo de **evaluación económica**, un modelo de simulación de
costo-efectividad del tamizaje. Sus tablas **parametrizan una simulación**, no clasifican
pacientes:

- **Tabla 9.16/9.23 "Estadio según diámetro tumoral"** (in situ 0.50 cm, local 1.00 cm, regional
  2.00 cm): son **estados de un modelo de Markov**, no umbrales TNM. Usarlas para asignar estadio
  sería un error de categoría.
- **Figura 9.7** agrupa: in situ = **0**; local = **I–IIA**; regional = **IIA, IIIA–IIIC**;
  metastásico = **IV**. Es una simplificación para simular historia natural.
- Tabla 9.17/9.24 (probabilidad de síntomas por diámetro) y las distribuciones de crecimiento
  tumoral (lognormal, Weibull) pertenecen al mismo modelo.

Si alguna vez el repo modela historia natural o costo-efectividad, estas tablas son la fuente
correcta. Para estadificar, no.

## 6. Fuentes

- **GPC Minsalud/Colciencias, Guía No. 19 (2013)** — *Guía de Práctica Clínica para la detección
  temprana, tratamiento integral, seguimiento y rehabilitación del cáncer de mama*. Anexo 9
  (Clasificación TNM, reproduce AJCC 7.ª ed.); §2.2 (tamización); cap. 9 (evaluación económica).
  [PDF](https://www.minsalud.gov.co/sites/rid/1/Gu%C3%ADa%20de%20Pr%C3%A1ctica%20Cl%C3%ADnica%20%20de%20Cancer%20de%20Mama%20versi%C3%B3n%20completa.pdf)
- **Cuenta de Alto Costo (2025)** — *Actualización del consenso basado en la evidencia: indicadores
  mínimos para la medición, evaluación y monitoreo de la gestión del riesgo de las mujeres con
  cáncer de mama en Colombia*. Bogotá, abril 2025.
  [PDF](https://cuentadealtocosto.org/wp-content/uploads/2025/04/actualizacion-del-consenso-de-cancer-de-mama-2025.pdf)
- **AJCC 8.ª ed. (2018)** — jerarquía de fuentes, de normativa a didáctica:
  1. **Capítulo 48 *Breast* corregido** (*Last updated 01/25/2018*, pp. 589–636) — **la fuente
     normativa**. El AJCC lo distribuye tras registro por correo; la American Society of Breast
     Surgeons lo espeja:
     [PDF](http://www.breastsurgeonsweb.com/wp-content/uploads/downloads/2020/10/AJCC-Breast-Cancer-Staging-System.pdf).
     No versionar en este repo (ver §2).
  2. **Hoja oficial de erratas** (*Updates & Errata*, rev. 2021-05-13) — descarga libre:
     [errata.xlsx](https://www.facs.org/media/g0wdye45/errata.xlsx) ·
     [página Updates and Corrections](https://www.facs.org/quality-programs/cancer-programs/american-joint-committee-on-cancer/updates-and-corrections/).
     Niveles: *Critical* (afecta categorías TNM o grupos pronósticos), *Histo/Topo*,
     *Clarification*, *Omission*.
  3. **Material educativo** (no normativo, anterior a la corrección de 2018-02-02):
     Hortobagyi GN, *Physician to Physician — AJCC 8th Edition: Breast*
     ([PDF](https://www.facs.org/media/u4djjc4v/breast-8th-ed.pdf), tablas en láminas 23–24 y
     39–49, casos de ejemplo de la §3.7); Gress DM, *AJCC 8th Edition — Breast Staging*
     ([PDF](https://www.facs.org/media/ws2fjubi/8th-edition-breast-staging.pdf), reglas de uso,
     redondeo y grado); Giuliano et al., *Breast Cancer — Major changes in the AJCC eighth edition
     cancer staging manual*, CA Cancer J Clin 2017.
- **NCI — TNM staging system (mama):**
  [cancer.gov](https://www.cancer.gov/types/breast/stages/tnm-staging-system)
- **Medwave — curso de estadificación TNM:**
  [medwave.cl](https://www.medwave.cl/puestadia/cursos/3486.html)

## 7. Documentos relacionados

- [`../adr/0006-estadificacion-tnm-ajcc8-pronostica.md`](../adr/0006-estadificacion-tnm-ajcc8-pronostica.md)
  — decisión: AJCC 8 como edición normativa y tabla pronóstica alimentada por entrada estructurada.
- [`../requisitos.md`](../requisitos.md) — catálogo RF/RNF.
- [`../alcance-vigente.md`](../alcance-vigente.md) — alcance vigente del TG.
- [`../architecture/contracts.md`](../architecture/contracts.md) — contratos de datos.
- [`../architecture/phi-and-security.md`](../architecture/phi-and-security.md) — PHI y marco legal.
