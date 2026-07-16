# ADR-0006: Estadificación TNM con AJCC 8 y tabla pronóstica

## Estado

**Aceptada** — decidida y validada por el **equipo** el 2026-07-15. Sus requisitos derivados ya están
registrados en [`docs/requisitos.md`](../requisitos.md): **RF-009** (motor de estadificación, issue
[#6](https://github.com/proyectomama/Project_mama_detector/issues/6)) y **RF-010** (estimación de
`cT`, issue [#7](https://github.com/proyectomama/Project_mama_detector/issues/7)).

**Alcance de esta aceptación — leer antes de citarla:** la acepta el **equipo**. El **director aún no
ha respondido** el hilo del 2026-07-15, y esta entrada **no** registra su aprobación. Es una decisión
técnica que el equipo toma para poder avanzar, no una validación externa. Si la respuesta del
director contradice el alcance —por ejemplo, si esperaba que el sistema *infiriera* el TNM desde la
mamografía—, esta decisión se revisa.

Registrar esa respuesta sigue siendo **evidencia pendiente**, y es la **misma** que RNF-002 necesita
para la meta AUC-ROC ≥0.92 (ver [`docs/alcance-vigente.md`](../alcance-vigente.md)): un único correo
puede cerrar ambas. Esta aceptación **no** la da por cumplida.

## Contexto

El director solicitó (correo del 2026-07-15, sin reproducir datos personales) que el software
*"identifique y valide el TNM"*, e indicó analizar la Guía de Práctica Clínica del Minsalud
(Guía No. 19, 2013). El repositorio no tenía ninguna referencia a estadificación TNM.

Del análisis de las fuentes (detalle completo en [`docs/clinical/tnm.md`](../clinical/tnm.md))
salieron cuatro hechos que condicionan la decisión:

1. **El TNM no es inferible desde una mamografía.** `cT` es *estimable* del diámetro mayor de la
   lesión (con `PixelSpacing`); `cN` no —las proyecciones CC/MLO no cubren la axila de forma
   fiable—; `cM0` es una valoración clínica de signos y síntomas, no una salida de un modelo de
   imagen. Sin `N` ni `M` no hay estadio.
2. **CBIS-DDSM no tiene etiquetas TNM**, ni ganglionares, ni de metástasis, ni biomarcadores. No se
   puede entrenar ni validar estadificación contra el dataset de la rebanada vertical.
3. **El Anexo 9 de la GPC reproduce AJCC 7 (2010)**, no la 8.ª edición vigente desde 2018.
   Implementarlo literal codificaría dos errores: `Tis(CLIS)` (en AJCC 8 el LCIS ya no se
   estadifica) y el redondeo de 1.1 mm a `T1mi` (AJCC 8 obliga a 2 mm → `T1a`).
4. **AJCC 8 restringe la tabla anatómica** a *"global regions where biomarker tests unavailable"*, y
   es explícito en que no debe usarse aunque falten los factores pronósticos, porque sesga los
   datos. **Colombia sí dispone de biomarcadores**: el consenso CAC 2025 reporta indicadores de RH y
   HER2 como parte de la gestión mínima del riesgo.

La tensión: la tabla anatómica es la única computable sin biopsia, pero es justamente la que el
estándar desaconseja en el contexto colombiano.

## Decisión

**1. La edición normativa del repositorio es AJCC 8.ª ed.**, no el Anexo 9 de la GPC. La GPC sigue
siendo la fuente colombiana de tamizaje y contexto; para estadificar prevalece AJCC 8. La fuente
normativa es el **capítulo 48 corregido** (*Last updated 01/25/2018*), no el material educativo ni
la primera impresión del manual: la única errata *Critical* de mama (2018-02-02) reemplazó el
capítulo entero de la 1.ª impresión.

**2. Se implementa la tabla pronóstica, no solo la anatómica.** El motor acepta **grado Nottingham
+ RE + RP + HER2** como **entrada estructurada** del informe de patología y calcula el estadio
pronóstico (clínico o patológico según el contexto de tratamiento). Se descarta la alternativa de
emitir únicamente estadio anatómico.

**3. El motor es determinista y dirigido por tabla.** No hay ML en la estadificación. Recibe datos,
valida la tupla, rechaza combinaciones imposibles y calcula el grupo. Se valida por **cobertura
exhaustiva de la tabla de verdad**, no por muestreo estadístico.

**4. El sistema no infiere lo que no puede medir.** `cN`, `cM`, grado y biomarcadores **siempre**
entran como dato estructurado. La plataforma puede *proponer* `cT` desde la imagen, marcado como
estimación radiológica con incertidumbre y con prefijo `c` —nunca `pT`—. Ante cualquier entrada
obligatoria ausente, el resultado es **"estadio no determinable"**, nunca un valor por defecto.

## Alternativas consideradas

**Solo estadio anatómico (descartada).** Entradas `cT`/`cN`/`cM`, sin biomarcadores; tabla tomada de
la GPC, sin fricción de licencia. Se descartó porque AJCC 8 desaconseja explícitamente esa tabla
donde hay biomarcadores disponibles, que es el caso de Colombia: el sistema estaría emitiendo el
estadio que el propio estándar considera sesgado.

**No implementar TNM (descartada).** Ignora una solicitud explícita del director y desaprovecha el
único componente clínicamente relevante que es 100 % verificable con el alcance actual.

**Inferir biomarcadores desde WSI (descartada por ahora).** Es RF-006, trabajo futuro; además
BreakHis no tiene etiquetas de biomarcadores. No es prerrequisito: el estadio pronóstico no necesita
un modelo, necesita un campo en el contrato.

## Consecuencias

**Sobre el contrato** (`packages/contracts/schemas/models.json`): aparece un tipo de estadificación
con `cT`/`cN`/`cM`, grado, RE, RP, HER2 y **contexto de tratamiento** —este último es obligatorio,
porque decide si aplica la tabla clínica o la patológica, que dan resultados distintos para la misma
combinación—. Los datos ausentes se modelan como `null`/`unknown`: **`cNX` no significa "no
evaluado"** (AJCC 8 lo reserva para cuenca ganglionar extirpada) y **`cMX` no existe** (solo `cM0`,
`cM1`, `pM1`).

**Sobre el alcance:** la función queda **desacoplada** del modelo de mamografía y de la meta
AUC-ROC ≥0.92; no altera la Fase 1 del roadmap. El motor se dispara sobre un cáncer **confirmado por
biopsia**, no sobre la salida del modelo: la plataforma detecta *sospecha*, y estadificar porque el
modelo dijo "malignant" sería precisamente el error a evitar. La estimación de `cT`, en cambio, sí
toca el pipeline de mamografía (requiere segmentación de la lesión y `PixelSpacing`) y es separable
del motor.

**Sobre el perfil regulatorio:** emitir un **estadio** es una afirmación clínica de mayor riesgo que
un triaje. Sube el perfil ante **INVIMA** como SaMD (RNF-006) y refuerza las exigencias de
transparencia y responsabilidad de los principios OMS (RNF-007). El disclaimer de RNF-008 no
sustituye ese análisis.

**Sobre derechos de autor:** el capítulo AJCC prohíbe *"incorporated into any software, product, or
publication without a written license agreement with ACS"*. Para el uso **interno y académico del
TG** se asume como deuda consciente, citando la fuente. **Si el proyecto se aliara con clínicas** o
saliera de lo académico, la licencia debe evaluarse **antes** de ese paso. El PDF del capítulo **no
se versiona** en este repositorio: se cita por URL.

**Casos sin estadio asignable** que el motor debe representar en vez de forzar un valor: grado
nuclear en lugar de Nottingham; posneoadyuvancia (`ypT`/`ypN`); respuesta patológica completa.

**Pendiente:** validar el alcance con el director (respuesta al hilo del 2026-07-15), que es evidencia
compartida con RNF-002 y no queda cubierta por esta aceptación. Los requisitos derivados ya están
registrados: **RF-009** (#6) y **RF-010** (#7) en `docs/requisitos.md`, con sus issues creados antes
de tocar el catálogo, conforme al roadmap.
