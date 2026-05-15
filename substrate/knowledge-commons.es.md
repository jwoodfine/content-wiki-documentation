---
schema: foundry-doc-v1
title: "Conocimiento Común y Comercio de Servicios"
slug: knowledge-commons.es
category: substrate
type: topic
quality: complete
short_description: El modelo económico que separa lo que PointSav publica libremente de lo que vende — artefactos de conocimiento bajo licencias abiertas, servicio de pago en el punto de agregación multi-Totebox.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
 - id: 1
 text: "Creative Commons. 'About the Licenses.' Creative Commons, 2024."
 url: "https://creativecommons.org/licenses/"
 - id: 2
 text: "GitHub. 'Open Source Guides.' GitHub, Inc., 2024."
 url: "https://opensource.guide/"
paired_with: knowledge-commons.md
---

El modelo de **Conocimiento Común / Comercio de Servicios** es la arquitectura económica de PointSav. Los artefactos de conocimiento — doctrina, convenciones, recetas de entrenamiento, pesos de adaptadores y corpus de trayectoria depurado — se publican bajo licencias abiertas y son reutilizables libremente. [^1] El umbral comercial se supera precisamente cuando dos o más Archivos Totebox deben operar como un sistema coordinado único. La operación de un solo Totebox es infraestructura soberana; la agregación de múltiples Totebox es un servicio de pago.

La línea entre ambos es clara y estructural. No es una decisión de precio — se deriva directamente de la arquitectura.

## La parte pública

Los siguientes artefactos se publican en cada versión MINOR de la Doctrina bajo licencias abiertas: DOCTRINE.md y enmiendas (CC BY 4.0), convenciones (CC BY 4.0), registro de citas (CC0), fragmento de corpus de trayectoria depurado (CC BY 4.0 con redacción), recetas de adaptadores (Apache 2.0), pesos de adaptadores constitucionales y de ingeniería (Apache 2.0), y tokens, componentes y directrices del sistema de diseño (MIT + CC BY 4.0).

Cada versión MINOR produce un paquete firmado y versionado publicado en `pointsav/factory-release-engineering` con un identificador estable. El paquete es en sí mismo un artefacto citable; los despliegues posteriores pueden fijar una versión específica y saber exactamente qué están ejecutando.

## El umbral comercial

Un solo Totebox con su propio despliegue de la plataforma es infraestructura soberana. El Cliente posee el sustrato, los datos, el adaptador y el entorno de ejecución. Nada de un solo Totebox supera el umbral comercial. El umbral se supera cuando dos o más Archivos Totebox deben operar como uno: consultas consolidadas entre instancias regionales, federación con sistemas de socios, enrutamiento a capacidad LLM alojada, o participación en el mercado de adaptadores.

La línea es estructural porque la agregación requiere cruzar límites de confianza, identidad y operación que un único Totebox soberano no tiene. Los clientes pagan por el sustrato que cruza esos límites, no por el acceso al conocimiento que no tiene límites.

## Modelo de contribuidores de tres niveles

El modelo de Conocimiento Común produce operativamente tres niveles de contribuidores:

**Núcleo (4–7 personas, empleados de PointSav)** — administración diaria del sustrato, decisiones arquitectónicas, supervisión en modo aprendiz para nuevas versiones de modelos, operaciones de servicio al cliente.

**Contribuidores de pago (50–100 personas, financiados por PointSav)** — trabajo de ingeniería por proyecto ejecutado mediante pull requests contra los repositorios públicos del sustrato: adaptadores de exportación por jurisdicción, autoría de adaptadores LoRA, aprovisionamiento de despliegues específicos del cliente, servicios de agregación multi-Totebox.

**Contribuidores abiertos (más de 10,000, licencias CC/Apache)** — contribuciones al sustrato público mediante pull requests. Sin CLA requerido para contribuciones al núcleo abierto. [^2] La reputación se acumula mediante la atribución por contribuidor del Sustrato de Trayectoria. Existe un camino hacia el nivel de pago para contribuidores cuyo trabajo demuestra calidad recurrente.

La ventaja de esta estructura es que el nivel abierto mantiene características y cobertura que un Núcleo de 4–7 personas no podría sostener solo. La mayoría de las características del sustrato están previstas para llegar mediante contribuciones abiertas; el Núcleo revisa y acepta; los de pago implementan las extensiones del nivel comercial.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que hacen que el sustrato se acumule con el tiempo
- [[disclosure-substrate]] — el patrón de sustitución de sustrato aplicado a las plataformas de divulgación continua
- [[apprenticeship-substrate]] — el mecanismo de entrenamiento que hace valiosa la contribución de corpus por inquilino

