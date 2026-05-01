---
schema: foundry-doc-v1
title: "El Sustrato de Aprendizaje Asistido"
slug: topic-apprenticeship-substrate.es
category: architecture
type: topic
quality: published
short_description: "Un protocolo de enrutamiento en producción que invierte el flujo habitual de trabajo asistido por IA: el modelo local intenta la tarea primero, un revisor senior firma un veredicto, y el desacuerdo entre ambos — capturado como tuplas de entrenamiento firmadas — genera la señal de preentrenamiento continuo de mayor calidad que la plataforma puede producir."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: topic-apprenticeship-substrate.md
---

El Sustrato de Aprendizaje Asistido invierte el orden habitual del trabajo asistido por IA. En lugar de que una sesión senior redacte un resultado y opcionalmente pida a la IA que lo verifique, el modelo local — el aprendiz — intenta la tarea en primer lugar. El revisor senior revisa el intento y firma un veredicto. El desacuerdo entre intento y veredicto se captura como una tupla de entrenamiento firmada y se incorpora al pipeline de preentrenamiento continuo de la plataforma.

## Por qué los datos de interacción son la señal de entrenamiento más valiosa

Entrenar un modelo de lenguaje con observaciones de lo que escribió un revisor senior produce un tipo de mejora. Entrenar con la interacción entre el intento del aprendiz y la corrección del senior produce una mejora un orden de magnitud más eficiente por ejemplo de entrenamiento. Esta es la conclusión central de la investigación sobre optimización por preferencias directas (DPO) y entrenamiento de alineación relacionado.

Esta señal de entrenamiento es estructuralmente inaccesible para plataformas cuya señal de preferencia se promedia entre todos los usuarios — no pueden producir datos de interacción por cliente, por tipo de tarea y por colaborador con la granularidad que genera el Sustrato de Aprendizaje Asistido.

## Los tres estadios de progresión

Cada tipo de tarea registrado progresa a través de tres estadios según el historial de veredictos acumulados.

**Revisión.** El aprendiz intenta la tarea; el senior revisa cada resultado antes de que se confirme. Los nuevos tipos de tareas comienzan aquí.

**Verificación muestral.** Los resultados del aprendiz se confirman sin revisión por resultado individual; el senior revisa una fracción muestreada y cualquier resultado marcado por un detector de anomalías.

**Autónomo.** El aprendiz opera sin revisión activa. Las reversiones post-confirmación trazadas a resultados del aprendiz desencadenan una regresión automática al estadio anterior.

## El formato de encargo, intento y veredicto

Un **encargo** nombra el tipo de tarea, los archivos en alcance, el test de aceptación y las citas doctrinales que acotan el trabajo. Un **intento** es el resultado propuesto por el aprendiz: razonamiento, diferencia de cambios, nivel de confianza autoevaluado y bandera de escalación. Un **veredicto** es la evaluación del senior — aceptar, refinar, rechazar o derivar a un nivel de cómputo superior — firmado con la misma primitiva criptográfica usada para los commits de la plataforma.

## Enrutamiento en sombra y crecimiento continuo del corpus

Para los tipos de tarea no registrados para enrutamiento en producción, la plataforma opera un camino en sombra: tras cada confirmación, el aprendiz produce lo que habría hecho. La tripleta de encargo, intento del aprendiz y resultado real se captura como tupla de entrenamiento sin veredicto senior. Las tuplas capturadas en sombra no esperan un veredicto para ingresar al corpus — aterrizan inmediatamente, con el campo de veredicto en nulo hasta que un senior lo firme.

## El tipo de tarea editorial

El pipeline editorial de la plataforma genera su propio corpus de aprendizaje asistido. Cada borrador que entra al pipeline produce un evento de creación; cada refinamiento produce un evento de refinamiento. Los borradores que reciben posteriormente una edición creativa producen un tercer evento que captura la transformación antes y después del paso creativo. El tipo de tarea editorial genera más tuplas por unidad de tiempo que los tipos orientados a código, y es la principal fuente de señal de entrenamiento de voz de dominio para el sustrato de IA de la plataforma.

## Ver también

- [[topic-trajectory-substrate]] — la tipología de corpus más amplia de la que el corpus de aprendizaje asistido es un componente
- [[compounding-doorman]] — el Doorman que enruta los encargos al modelo local
- [[topic-llm-substrate-decision]] — por qué la estructura completamente abierta de OLMo 3 hace posible el preentrenamiento continuo previsto

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
