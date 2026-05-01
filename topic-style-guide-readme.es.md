# Guía de estilo — README (resumen)

El archivo README es el más leído de cualquier repositorio. Es
el primer artefacto que ve un lector frío, un colaborador o un
evaluador, y marca el tono de todo lo que leerán a continuación.
Foundry tiene tres subtipos de README — *workspace*, repositorio
y proyecto — cada uno con su propio alcance, pero con una
disciplina editorial compartida.

Esta guía de estilo es el documento operativo público para
colaboradores. Es el complemento humano de las plantillas
estructuradas en `service-disclosure/templates/readme-*.toml`,
que llevan las mismas reglas en forma legible por máquina para
el canal de adaptadores por inquilino.

## Subtipos de README

| Subtipo | Ubicación | Función |
|---|---|---|
| *Workspace* | `~/Foundry/README.md` | Identifica el espacio de trabajo y orienta al lector hacia `DOCTRINE.md`, `CLAUDE.md`, `NEXT.md`, `MANIFEST.md`. |
| Repositorio | `<repo>/README.md` | Estructura *Standard Readme*: contexto, instalación, uso, contribución, licencia. |
| Proyecto | `<repo>/<project>/README.md` | Más estrecho: qué hace el proyecto, cómo se compila y prueba, nota de licencia. |

## Reglas centrales

- **Las primeras 30 líneas funcionan en editores planos.** Sin
  bloques HTML centrados, sin Mermaid, sin grupos de insignias
  al inicio.
- **Pareja bilingüe obligatoria.** Cada `README.md` se acompaña
  de `README.es.md`. La versión en español es adaptación
  estratégica, no traducción 1:1.
- **Voz Bloomberg, no marketing.** Voz activa por defecto.
  Promedio de oraciones cerca de dieciocho palabras; máximo
  cerca de treinta. La lista de vocabulario prohibido aplica.
- **Lenguaje a futuro con cautela.** Capacidad futura,
  cronograma o resultado para el cliente se describen como
  "planeado", "previsto", "puede", "objetivo" — nunca como
  futuro declarativo. Es la postura BCSC de divulgación
  continua.
- **Nombres canónicos.** Los nombres del *Nomenclature Matrix*
  no se sustituyen con sinónimos.

## Véase también

- [Documento canónico en inglés](topic-style-guide-readme.md)
- [Guía de estilo — TOPIC](topic-style-guide-topic.md)
- [Guía de estilo — GUIDE](topic-style-guide-guide.md)

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.