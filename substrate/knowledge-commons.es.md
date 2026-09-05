---
schema: foundry-doc-v1
title: "Conocimiento común y comercio de servicios"
slug: knowledge-commons
category: substrate
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-customer-ownership
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

El modelo de **Conocimiento Común / Comercio de Servicios** es la [[economic-model|arquitectura económica]] de PointSav. Los artefactos de conocimiento — doctrina, convenciones, recetas de entrenamiento, [[adapter-composition|pesos de adaptadores]] y corpus de trayectoria depurado — se publican bajo licencias abiertas y son reutilizables libremente. [^1] El umbral comercial se supera precisamente cuando dos o más [[totebox-archive|Archivos Totebox]] deben operar como un sistema coordinado único. La operación de un solo Totebox es infraestructura soberana; la agregación de múltiples Totebox es un servicio de pago.

La línea entre ambos es clara y estructural. No es una decisión de precio — se deriva directamente de la arquitectura.

## El ecosistema de artefactos abiertos

Los siguientes artefactos se publican en cada versión MINOR bajo licencias abiertas:

| Artefacto | Licencia |
|---|---|
| Definiciones de arquitectura y sus enmiendas | CC BY 4.0 |
| Especificaciones de gobernanza publicadas | CC BY 4.0 |
| Registro de citas (`citations.yaml`) | CC0 |
| Fragmento de corpus de trayectoria depurado | CC BY 4.0 con redacción |
| Recetas de adaptadores (scripts de entrenamiento, hiperparámetros) | Apache 2.0 |
| Pesos del adaptador constitucional | Apache 2.0 |
| Pesos del adaptador de ingeniería | Apache 2.0 |
| Tokens, componentes y directrices del sistema de diseño | Apache 2.0 |

Cada versión MINOR produce un paquete firmado y versionado publicado en `pointsav/factory-release-engineering` con un identificador estable. El paquete es en sí mismo un [[citation-substrate|artefacto citable]]; los despliegues posteriores y los Clientes pueden fijar una versión específica y saber exactamente qué están ejecutando.

## El umbral de agregación comercial

Un solo Totebox con su propio despliegue de la plataforma es infraestructura soberana. El Cliente posee el sustrato, los datos, el adaptador y el entorno de ejecución. Nada de un solo Totebox supera el umbral comercial.

El umbral se supera cuando dos o más [[totebox-archive|Archivos Totebox]] — o un Archivo Totebox más un sistema externo en coordinación — deben operarse como uno. Algunos ejemplos:

- Consultar entre dos Toteboxes regionales para un informe consolidado
- Federar el Totebox de un Cliente con el Totebox de un socio para investigación conjunta
- Enrutar solicitudes de Nivel B hacia la capacidad LLM alojada por PointSav (véase [[four-tier-slm-substrate]])
- Participar en el [[sovereign-ai-commons|mercado de adaptadores]] para compartir adaptadores

La línea es estructural porque la agregación requiere cruzar límites de confianza, de identidad y de operación que un único Totebox soberano no tiene. Los clientes pagan por el sustrato que cruza esos límites, no por el acceso al conocimiento que no tiene límites.

## Documentación abierta estratégica

Publicar la receta no amenaza el negocio. El razonamiento:

**La economía de extracción es pobre para las PYME.** Un cliente pequeño que lee la documentación e intenta una implementación propia nunca fue el cliente objetivo. Los clientes de servicio pagan porque la implementación operativa, la integración, el cumplimiento y la agregación representan trabajo real, no porque el conocimiento esté restringido.

**El conocimiento público aumenta el valor del sustrato.** Cuando la documentación es pública y citable, los Clientes posteriores tienen una referencia estable para sus adaptadores, su postura de cumplimiento y la incorporación de sus contribuidores. Lo que pagan es la fiabilidad del sustrato.

**Los comunes son un embudo de reclutamiento.** Los contribuidores encuentran PointSav a través de artefactos públicos. Se unen porque el sustrato es algo sobre lo que pueden construir. El paquete de `factory-release-engineering` es el punto de entrada.

**Los artefactos arquitectónicos públicos resisten la captura.** Una arquitectura versionada, firmada y citable públicamente no puede adquirirse y alterarse silenciosamente. El versionado y la firma son el mecanismo de durabilidad.

## Modelo de contribuidores de tres niveles

El modelo de Conocimiento Común produce operativamente tres niveles de contribuidores:

**Núcleo (4–7 personas, empleados de PointSav)** — administración diaria del sustrato. Decisiones arquitectónicas, supervisión en modo aprendiz para nuevas versiones de modelos, operaciones de servicio al cliente. Pequeño por diseño; se prevé que las propiedades estructurales del sustrato permitan que este nivel permanezca pequeño a medida que crece la escala.

**Contribuidores de pago (50–100 personas, financiados por PointSav)** — trabajo de ingeniería por proyecto pagado por PointSav y ejecutado mediante pull requests contra los repositorios públicos del sustrato. Adaptadores de exportación por jurisdicción, autoría de adaptadores LoRA, aprovisionamiento de despliegues específicos del cliente, servicios de agregación multi-Totebox. Contratos basados en resultados vinculados a los ingresos por servicio al Cliente.

**Contribuidores abiertos (más de 10,000, licencias CC/Apache)** — contribuciones al sustrato público mediante pull requests a `pointsav/factory-release-engineering`, el sistema de diseño, el motor wiki, [[mcp-substrate-protocol|adaptadores de servidor MCP]] y contenido TOPIC en las wikis de contenido. Sin CLA requerido para contribuciones al núcleo abierto. [^2] La reputación se acumula mediante la atribución por contribuidor del [[trajectory-substrate|Sustrato de Trayectoria]]. Existe un camino hacia el nivel de pago para contribuidores cuyo trabajo demuestra calidad recurrente y fluidez operativa.

El valor estructural de este diseño es que el nivel Abierto sostiene características y cobertura que un Núcleo de 4–7 personas no podría mantener solo. Se prevé que la mayoría de las características del sustrato lleguen mediante contribución Abierta; el Núcleo revisa y acepta; los de Pago implementan las extensiones de nivel comercial.

## Movilidad operativa entre niveles

El modelo no es fijo. Un contribuidor Abierto cuyo trabajo recurrente demuestre calidad operativa puede recibir contratos de Pago. Un contribuidor de Pago puede, con el tiempo, avanzar hacia el Núcleo. Cualquier contribuidor puede bifurcar el proyecto, llevarse sus adaptadores y los datos de su inquilino, y operar de forma independiente — el sustrato está diseñado para que la salida ordenada sea el comportamiento por defecto, no el litigio.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que hacen que el sustrato se acumule con el tiempo
- [[disclosure-substrate]] — el patrón de sustitución de sustrato aplicado a las plataformas de divulgación continua
- [[apprenticeship-substrate]] — el mecanismo de entrenamiento que hace valiosa la contribución de corpus por inquilino
- [[adapter-composition]] — cómo se componen y versionan los adaptadores por inquilino

