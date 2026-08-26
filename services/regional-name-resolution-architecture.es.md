---
schema: foundry-doc-v1
title: "Arquitectura de resolución de nombres regionales"
slug: regional-name-resolution-architecture
language: es
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "El motor de geocodificación inversa por capas y sin conexión que convierte las coordenadas de una agrupación en un nombre regional legible: sus conjuntos de límites, su orden de enrutamiento por país y el posprocesado que hace legibles los nombres en lengua de origen, sin ninguna llamada a API externa."
cites: [overture-maps]
paired_with: regional-name-resolution-architecture.md
---

Cada agrupación de coubicación se etiqueta con un nombre regional legible: un área metropolitana norteamericana, una región NUTS-3 europea, un municipio mexicano, una subdivisión censal canadiense. Ese nombre no es un campo de los datos de origen: es la salida de un motor de geocodificación inversa por capas que funciona sin conexión.

**Por qué importa:** toda la resolución se ejecuta desde archivos de límites locales, sin ninguna API de geocodificación externa en el circuito, de modo que el [[location-intelligence-substrate|sustrato]] conserva su capacidad de funcionar sin red y sin coste por solicitud incluso en el paso que más obviamente invitaría a contratar un servicio alojado.

## Las capas de límites

Las coordenadas del ancla de cada agrupación se comprueban contra un conjunto de capas de límites en un orden específico por país. Capas principales de enrutamiento:

| Capa | Fuente | Cobertura | Granularidad |
|---|---|---|---|
| `us_cbsa.geojson` | US Census Bureau TIGER GENZ2023 | Estados Unidos | Áreas estadísticas basadas en núcleo (metro y micropolitanas) |
| `ca_cma.geojson` | Statistics Canada, Censo 2021 | Canadá | Áreas metropolitanas censales |
| `ca_csd.geojson` | GADM 4.1 admin-3 | Canadá | Aproximaciones a subdivisiones censales (municipios) |
| `mx_municipio.geojson` | GADM 4.1 admin-2 | México | Municipios |
| `mx_metro.geojson` | INEGI 2018, Zonas Metropolitanas | México | Zonas metropolitanas (reserva intermedia) |
| `eu_nuts3.geojson` | Eurostat GISCO 2021 | UE, Reino Unido, AELC y Balcanes occidentales | Regiones NUTS-3 |
| `fallback_ne_admin1.geojson` | Natural Earth 10m | Global | Admin-1 (estados y provincias) |

Además de este conjunto principal, el motor carga una capa de archivos de límites a escala de asentamiento — límites más finos de ciudad, población y municipio para Estados Unidos, la Unión Europea y Canadá — que resuelven un nombre más específico allí donde esos datos existen. Todos los archivos se cargan una sola vez al inicializar el motor, y los índices espaciales reducen las búsquedas de punto en polígono a coste logarítmico por consulta.

**Por qué importa:** cargarlo todo una vez al arranque es lo que abarata lo suficiente la resolución por agrupación como para ejecutarla sobre el manifiesto completo en cada reconstrucción.

## Enrutamiento por país

- **Estados Unidos** — búsqueda en CBSA. Al encontrar coincidencia, se formatea el nombre: se elimina el sufijo estatal y se añade «Metro Area» si falta.
- **Canadá** — primero la subdivisión censal (admin-3). Cuando coinciden y difieren tanto la subdivisión como el área metropolitana circundante, el resultado se compone: «Strathcona County, Edmonton». Cuando solo coincide una, se devuelve ese nombre solo.
- **México** — búsqueda de municipio (admin-2), con posprocesado del texto en español al coincidir. Si falla, el motor recurre a la capa de zonas metropolitanas y, si esta también falla, a la reserva estatal de Natural Earth.
- **Unión Europea, Reino Unido, AELC y Balcanes occidentales** — búsqueda NUTS-3.
- **Reserva** — admin-1 de Natural Earth para cualquier país no cubierto por las capas, devolviendo nombres de estado o provincia.

Cada capa incorpora una tolerancia en su consulta espacial: cuando un punto cae justo fuera de todos los polígonos — una tienda costera al borde de un fiordo, por ejemplo — el motor acepta el polígono más cercano dentro de unos 15 km.

**Por qué importa:** sin esa tolerancia, tiendas costeras e insulares legítimas atraviesan todas las capas específicas hasta la reserva estatal, y el mapa etiqueta una localidad noruega con el nombre de su condado.

## Posprocesado de los nombres brutos

Los archivos de límites traen nombres en lengua de origen con afijos concatenados que no son legibles. Tres transformaciones los limpian.

**Separador de CamelCase.** Los nombres GADM admin-2 y admin-3 se almacenan sin separadores de palabra: «StrathconaCounty» pasa a «Strathcona County».

**Separador de preposiciones en español.** Los nombres de municipios mexicanos arrastran a veces preposiciones concatenadas — «Bocadel Río», «Apetatitlánde Antonio Carvajal». Una expresión regular detecta *de*, *del*, *la*, *las*, *el* y *los* pegadas a un carácter minúsculo precedente e inserta un espacio antes.

**Normalizador de puntos.** «Gustavo A.Madero» se normaliza a «Gustavo A. Madero».

Un diccionario aparte de anulaciones explícitas resuelve los casos fuera del alcance de las expresiones regulares: nombres griegos transliterados al inglés, simplificaciones de sufijos finlandeses, eliminación de prefijos polacos, normalización de nombres bilingües belgas. Ese diccionario contenía unas 200 entradas a mediados de 2026.

**Por qué importa:** el nombre es la única parte de esta tubería que una persona lee directamente, así que un artefacto mecánico en él socava la confianza en cada cifra que aparece a su lado.

## Anulaciones de presentación

Algunos nombres de municipio son técnicamente correctos pero no la forma que un lector hispanohablante espera ver en un mapa. Un pequeño diccionario de anulaciones asigna los nombres de zona metropolitana del INEGI a sus formas breves habituales: «Zona Metropolitana del Valle de México» pasa a «Ciudad de México» y «Zona Metropolitana de Guadalajara» a «Guadalajara».

## Escala

Tras el enrutamiento por capas y el posprocesado, el motor produce unos 1.200 nombres de región únicos en el ámbito operativo a mayo de 2026: 671 áreas metropolitanas estadounidenses distintas, 245 regiones canadienses (subdivisiones censales y áreas metropolitanas combinadas), 104 municipios mexicanos y varios cientos de regiones NUTS-3 europeas. Cada uno aparece en las ventanas emergentes de agrupación y en el panel del inspector.

## Véase también

- [[location-intelligence-substrate]] — la arquitectura SIG de archivos planos en la que se ejecuta este motor
- [[poi-data-schema]] — las estructuras de registro cuyas coordenadas alimentan el motor
- [[service-business-clustering]] — el servicio de agrupación que consume los nombres resueltos
- [[gis-as-bim-substrate]] — cómo usa después una tubería BIM un nombre regional resuelto
