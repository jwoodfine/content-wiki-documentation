---
schema: foundry-doc-v1
title: "Consola del corrector"
slug: radical-proofreader-ui
category: applications
type: app
content_type: topic
quality: complete
index_group: knowledge-and-editorial-applications
short_description: "Cartucho de contenido de terminal para la canalización service-proofreader — el operador envía texto, revisa los hallazgos y registra un veredicto binario aceptar/rechazar que alimenta el corpus de aprendizaje."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
references: []
paired_with: radical-proofreader-ui.md
---

La **consola del corrector**, `app-console-content`, es el cartucho de contenido F4 de
[[os-console]] — una interfaz de terminal, no una aplicación web. Los operadores la usan para
enviar texto a la canalización `service-proofreader`, revisar los hallazgos estructurados y la
reescritura que esta devuelve, y registrar un veredicto que alimenta el
[[apprenticeship-substrate|corpus de aprendizaje]] de la plataforma.

## Registro de veredictos y el ciclo de aprendizaje

Después de que la canalización devuelve sus hallazgos y la reescritura, el operador los revisa
desde la terminal y registra un veredicto con una sola tecla: **aceptar** la reescritura, o
**rechazar** y conservar el original. Cada veredicto envía la solicitud, el inquilino y la
disposición a la canalización como un evento tipificado. No existe una tercera disposición de
"editar y reenviar" — la elección es binaria.

## La garantía de no entrenamiento con texto del inquilino

La consola expone el compromiso de manejo de datos de la plataforma en el punto de envío de
texto. La garantía de no entrenamiento con texto del inquilino es una propiedad estructural de
la ruta de escritura del corpus: el texto enviado por un operador y la reescritura resultante
se escriben en el directorio de instancia de despliegue de ese inquilino y no pueden mezclarse
con los registros de otros inquilinos.

La garantía se hace explícita en la interfaz de envío porque los operadores requieren confianza
antes de enviar material editorial sensible. La consola la muestra como un aviso de divulgación
— permanente, no descartable — adyacente al área de envío de texto.

## Véase también

- [[editorial-pipeline-three-stages]] — la canalización de tres etapas con la que interactúa
  la consola
- [[language-protocol-substrate]] — la clasificación de familia de género que refleja la
  visualización de hallazgos de la consola
- [[customer-tier-catalog-pattern]] — cómo se provisiona la instancia de despliegue del
  corrector
