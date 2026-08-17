---
schema: foundry-doc-v1
title: "Restricciones en tiempo de decodificación (resumen)"
slug: decode-time-constraints
short_description: "La técnica de decodificación restringida, descrita con precisión — y una línea clara entre esa técnica y lo que PointSav realmente ha construido: hoy, un linter asesor posterior a la generación; el mecanismo basado en gramática sigue siendo enteramente planificado, no implementado."
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
status: active
bcsc_class: public-disclosure-safe
forward_looking: true
last_edited: 2026-08-17
editor: pointsav-engineering
paired_with: decode-time-constraints.md
cites:
 - ni-51-102
 - llguidance
 - llm-structured-output-2026

---

Las **restricciones de tiempo de decodificación**, como técnica, son reglas estructurales
que un runtime aplica en el momento en que el modelo emite cada token, no después de que
la respuesta esté terminada. Cuando la regla dice "sin vocabulario prohibido" o "debe
producir JSON válido", el runtime hace que el token infractor sea matemáticamente
imposible — el modelo elige del conjunto de tokens válidos restantes. Esta técnica se
conoce como decodificación restringida, generación estructurada o generación guiada por
gramática, y está bien establecida en la literatura: la biblioteca `[llguidance]` de
Microsoft Research, `[xgrammar]` de Carnegie Mellon, las salidas estructuradas de vLLM, y
un cuerpo creciente de literatura sobre generación estructurada con modelos de lenguaje.

## Lo que realmente está en producción hoy

La aplicación del vocabulario editorial en esta plataforma no usa restricciones de tiempo
de decodificación. El mecanismo real y actual es una lista de palabras asesora,
`.agent/editorial-qa/banned-vocabulary.txt`, verificada por
`.agent/scripts/editorial-lint.py` — un linter que se ejecuta después de la generación,
no durante ella, y cuyo propio encabezado indica que ningún commit se bloquea jamás por
una coincidencia; las infracciones se registran como advertencias para revisión
editorial. Desde el 2026-08-01 el propio linter fue actualizado para leer
`tokens/linguistic/vocabulary-banned-*.yaml` de `pointsav-design-system` en lugar del
archivo de texto estático, así que incluso este mecanismo asesor ya cambió una vez.

No existe ningún archivo de gramática `.lark`, ningún directorio `service-content/
schemas/`, ningún `validate.py`, ni ningún directorio de plantillas por género
`service-disclosure/templates/` en ninguna parte del monorepo — confirmado por búsqueda
directa, no inferido. La inferencia de producción en el Nivel A (`slm-doorman/src/tier/
local.rs`) **rechaza** explícitamente las gramáticas Lark ("llama-server no incluye
llguidance") y escala al Nivel B en su lugar. `llguidance` es una dependencia real en el
código, pero valida la sintaxis de gramática arbitraria proporcionada por quien llama, en
el límite de la solicitud HTTP del Doorman — un paso de validación de entrada, sin
relación con la aplicación de vocabulario prohibido.

## La técnica que este artículo describía originalmente como construida

Todo lo que sigue describe el *diseño* — una arquitectura real, coherente y factible,
consistente con la técnica general anterior — no un sistema ya implementado. Cada verbo
en tiempo presente en esta sección debe leerse como `planificado`/`intencionado`, según
la postura estándar de esta plataforma sobre lenguaje prospectivo de la BCSC; nada de
esto debe leerse como una capacidad actual.

**El mecanismo previsto.** Una gramática declararía qué vocabulario está prohibido; el
runtime haría que el token infractor fuera inalcanzable en lugar de detectarlo después
del hecho. La gramática se compondría en tres capas. Una **gramática base** cubriría las reglas de
vocabulario prohibido universales para todo inquilino y género. Una **gramática de
inquilino** cubriría extensiones específicas por cliente — palabras propias de marca en
la lista de No-Usar, reglas de densidad de citas, patrones de afirmación prohibidos —
redactadas localmente por el propio inquilino. Una **gramática de género** cubriría
reglas estructurales por género: un TOPIC necesitaría un párrafo introductorio, una GUIDE
necesitaría pasos numerados, una divulgación regulatoria necesitaría campos de cita
específicos. En el momento de la solicitud, el [[doorman-protocol|Doorman]] compondría
las tres capas y ejecutaría la decodificación con la restricción compuesta activa.

**Por qué importaría si se construyera.** La ruta editorial se volvería estructuralmente
auditable en lugar de depender de revisión posterior: un TOPIC no podría contener un
término prohibido porque la gramática se negaría a emitirlo; los términos prohibidos de
un inquilino no podrían aparecer en la salida de ese inquilino; un patrón de cita
requerido no podría omitirse silenciosamente. Esta es la forma de aplicación de la que
eventualmente dependería la propiedad de composición federada del Sustrato Compuesto —
pero esa dependencia es en sí misma prospectiva, no una descripción de cómo funciona hoy
el entrenamiento federado.

## Por qué este diseño, si se construyera, sería estructuralmente difícil de igualar para la IA gestionada por hiperescaladores

Tres razones, cada una condicionada a que el diseño anterior realmente se construya — no
una afirmación sobre una capacidad vigente:

**1. La gramática necesitaría redactarse localmente.** Una restricción en tiempo de
decodificación se ejecuta dentro del bucle de inferencia; redactar una gramática
específica para los estándares editoriales de un inquilino requeriría acceso de
escritura al archivo de gramática que carga el runtime. Los productos de IA gestionados
por hiperescaladores tratan la gramática como parte del despliegue cerrado del modelo —
los inquilinos obtienen modos de salida estructurada, no una gramática propia cargada en
tiempo de inferencia.

**2. La restricción necesitaría componerse con el enrutamiento de adaptadores.** El
Doorman ya enruta entre tres niveles de cómputo (véase [[doorman-protocol]]); una
restricción de tiempo de decodificación necesitaría viajar con la composición de
adaptadores que sirve una solicitud dada. La IA gestionada por hiperescaladores no
expone primitivos de composición de adaptadores, y mucho menos de composición de
restricciones — esta razón se sostiene independientemente de si la capa de gramática ya
está construida.

**3. La restricción necesitaría ser auditable.** Por la postura de divulgación continua
de la BCSC (`[ni-51-102]`), toda salida editorial debería ser trazable a las reglas bajo
las cuales fue generada. El libro mayor de auditoría actual (véase [[doorman-protocol]])
no lleva un campo de versión de gramática ni de hash de respuesta — eso es
genuinamente prospectivo, no una omisión de esta descripción.

## Trabajo planificado

Por la postura de divulgación continua de la BCSC (`[ni-51-102]`), todo el mecanismo
basado en gramática descrito arriba es `planificado` e `intencionado`, no construido. En
orden aproximado de dependencia:

- Una gramática base real (reglas de vocabulario prohibido universales), que reemplace
  al linter asesor actual.
- Fragmentos de gramática por género — todavía no existe ningún directorio de
  plantillas de género al cual adjuntarlos.
- Extensiones de vocabulario prohibido por inquilino (palabras específicas de marca de
  un cliente que estén en su lista de No-Usar).
- Composición de adaptadores en vivo con composición de gramática a través del Doorman.
- Entradas en el libro mayor de auditoría que registren `grammar_version` +
  `adapter_composition` + `response_hash` por solicitud — el esquema actual del libro
  mayor no tiene ninguno de estos campos (véase [[doorman-protocol]]).

## Véase también

- [[compounding-substrate]]
- [[language-protocol-substrate]]
- [[apprenticeship-substrate]]
- [[sovereign-ai-routing]]
