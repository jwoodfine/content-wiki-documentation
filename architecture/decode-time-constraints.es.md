---
title: "Restricciones en tiempo de decodificación (resumen)"
slug: decode-time-constraints.es
category: architecture
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
  - llguidance
  - llm-structured-output-2026
---

El sustrato impone reglas estructurales en el momento en que el modelo
emite cada token, no después de que la respuesta esté terminada.
Cuando la regla dice "sin vocabulario prohibido" o "debe producir JSON
válido", el runtime hace que el token infractor sea matemáticamente
imposible — el modelo elige del conjunto de tokens válidos restantes.
Es la diferencia entre un humano calificando trabajo después de la
entrega y una barandilla que evita la violación antes de que suceda.

## Cómo lo usa Foundry

El sustrato envía `service-content/schemas/banned-vocab.lark` — una
gramática Lark EBNF que declara ocho términos editoriales prohibidos
más una regla de escape entre comillas inversas. La inferencia de
producción en el Nivel A (OLMo 3 7B local) y el Nivel B (Yo-Yo en la
nube) carga la gramática vía `[llguidance]` y la aplica en tiempo de
decodificación. La validación editorial en el espacio de trabajo
(`validate.py`) ejecuta la misma gramática en modo Lark para
verificación offline antes de que el contenido se publique.

El patrón se compone con el sustrato de protocolo de lenguaje: cada
plantilla de género (TOPIC, GUIDE, README, contrato, política,
etcétera) envía un fragmento de gramática por género. En tiempo de
inferencia, la gramática activa es
`gramática-base ⊕ gramática-inquilino ⊕ gramática-género`.

## Por qué los hiperescaladores no pueden replicarlo

Tres razones estructurales:

- **La gramática debe escribirse localmente.** Una restricción en
  tiempo de decodificación ejecuta dentro del bucle de inferencia.
  El inquilino necesita acceso de escritura al archivo de gramática
  que el runtime carga. Los productos de IA gestionados por
  hiperescaladores tratan la gramática como parte del despliegue
  cerrado del modelo.
- **La restricción debe componerse con el enrutamiento de
  adaptadores.** El Doorman de Foundry (`service-slm`) compone
  adaptadores por solicitud; las restricciones de decodificación
  viajan con esa composición. La IA gestionada por hiperescaladores
  no expone primitivos de composición de adaptadores.
- **La restricción debe ser auditable.** Por la postura de
  divulgación continua de la BCSC (`[ni-51-102]`), cada salida
  editorial debe ser trazable a las reglas bajo las cuales fue
  generada. El libro mayor de auditoría por inquilino de Foundry
  captura la versión de la gramática, la composición de adaptadores
  y la respuesta — juntas.

## Qué habilita esto

La ruta editorial del Sustrato Compuesto se vuelve matemáticamente
auditable. Un TOPIC comprometido a un repositorio de wiki de
contenido no puede contener un término del vocabulario prohibido. Una
GUIDE renderizada para un Cliente no puede contener términos
prohibidos específicos del inquilino. Un borrador de divulgación
regulatoria no puede omitir un patrón de citas requerido.

La disciplina cambia de calificación-humana-después-de-la-entrega a
imposibilidad-en-tiempo-de-emisión. Esta es la capa de aplicación de
sustrato de la que depende la propiedad de composición federada del
Sustrato Compuesto.

## Trabajo planificado

Por la postura de divulgación continua de la BCSC (`[ni-51-102]`), la
trayectoria descrita a continuación es `planificada` e `intencionada`:

- Gramáticas por género para las 16 plantillas en
  `service-disclosure/templates/`.
- Extensiones de vocabulario prohibido por inquilino (palabras
  específicas de marca de un Cliente que estén en su lista de
  No-Usar).
- Composición de adaptadores con composición de gramática a través
  del Doorman de `service-slm`.
- Entradas en el libro mayor de auditoría que registren
  `grammar_version + adapter_composition + response_hash` por
  solicitud.

## Véase también

- [El Sustrato Compuesto](topic-compounding-substrate.es.md)
- [El sustrato de protocolo de lenguaje](topic-language-protocol-substrate.es.md)
- [El sustrato de aprendizaje](topic-apprenticeship-substrate.es.md)
- La convención que refleja este artículo:
  `~/Foundry/conventions/language-protocol-substrate.md` §3
