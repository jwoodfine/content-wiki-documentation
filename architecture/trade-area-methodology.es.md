---
schema: foundry-doc-v1
title: "Metodología de área de atracción"
slug: trade-area-methodology
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: es
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: trade-area-methodology.md
cites: []
---

La metodología de área de atracción establece cómo el mapa de inteligencia de ubicación de Woodfine (gis.woodfinegroup.com) define, representa y etiqueta el área alrededor de cada clúster de co-ubicación desde la cual se estima que viajan los clientes. Un área de atracción no es simplemente la extensión geográfica de las tiendas en un clúster; es una representación de dónde se origina la demanda. La metodología especifica, con claridad y con sus limitaciones declaradas, cómo se construye esa representación en cada etapa del desarrollo del producto.

## Lo que muestra el mapa hoy

El mapa en vivo muestra una banda de distancia alrededor del centroide de cada clúster. **Hasta que la canalización de áreas de atracción observadas esté integrada, esa banda es un radio de línea recta, no una cuenca hidrográfica medida.** La regla de etiquetado es inequívoca: cualquier geometría derivada de una fórmula de línea recta se lee como "banda de distancia (línea recta)" en la cara del mapa y en el panel de detalles — nunca "cuenca hidrográfica" y nunca "área de atracción."

El modal de Metodología incluye una declaración clara: *"Las bandas de distancia son radios de línea recta alrededor del centroide del clúster; aproximan, pero no miden, de dónde provienen los clientes."*

Las distancias se calculan geodésicamente en lugar de en pantalla. Una banda etiquetada como 35 km representa 35 km de distancia real sobre el terreno independientemente de la latitud, porque se utilizan distancias haversine y búferes geodésicos métricos en todo el sistema.

## El modelo previsto: orígenes observados y tiempo de conducción

Dos métodos — isócronas de tiempo de conducción y polígonos de origen-destino empíricos — están planeados como mejoras sucesivas a las bandas de distancia actuales.

### Isócronas de tiempo de conducción

Una isócrona reemplaza el radio de línea recta con el área accesible dentro de un tiempo de conducción declarado (por ejemplo, 10, 20 o 30 minutos) a lo largo de la red vial. Las isócronas respetan barreras que los círculos ignoran — ríos, acceso a autopistas, puertos de montaña, rutas costeras de un solo sentido — por lo que dos clústeres con radios de línea recta idénticos pueden tener áreas de alcance sustancialmente diferentes. Las isócronas de tiempo de conducción son el estándar de la geografía minorista que esperan los revisores de selección de sitios.

La implementación prevista utiliza un motor de enrutamiento auto-alojado sobre los extractos de OSM ya incorporados en el archivo. La dependencia de una API de isócronas de terceros con tarificación por uso no es el camino previsto para un producto construido sobre infraestructura de datos soberana y autocontenida. El motor de enrutamiento específico es una cuestión abierta en el registro de trabajo de ingeniería.

### Polígonos de origen-destino observados

En lugar de modelar de dónde podrían venir los clientes, un polígono de O-D dibuja de dónde vienen realmente, utilizando datos de movilidad ya almacenados en disco:

- **Estados Unidos — US LEHD LODES.** Flujos de origen-destino de trabajadores agregados a celdas H3, 49 estados, aproximadamente 684,000 celdas H3. Admite un área de atracción de origen laboral para clústeres estadounidenses.
- **España — MITMA.** Las matrices de movilidad del Ministerio de Transporte de España están incorporadas para 58 clústeres ES, proporcionando una distribución de origen observada en lugar de un anillo modelado.
- **`layer6-mobility-work.pmtiles`.** La superficie de origen laboral combinada de US LODES y MITMA está construida y servida como capa de mosaicos de mapa. Los datos necesarios para representar polígonos de origen observados para clústeres de EE. UU. y España están presentes; la integración que convierte un clic en un clúster en un polígono de origen observado, en lugar de un anillo, está planeada pero aún no conectada.

La cobertura es desigual (EE. UU. y España hoy; Reino Unido, Francia y Alemania investigados como fuentes viables siguientes), por lo que el despliegue planeado es por país. Los clústeres sin cobertura de O-D mantienen la banda de distancia claramente etiquetada como medida provisional explícita.

## Cálculo geodésico y la advertencia de Web Mercator

El mapa se representa en Web Mercator (EPSG:3857). Web Mercator preserva la forma localmente pero distorsiona el área y la distancia en pantalla con la latitud. La metodología calcula distancias y áreas geodésicamente:

- Las pruebas de distancia utilizan la distancia haversine (gran círculo) entre coordenadas geográficas.
- La construcción de polígonos utiliza búferes geodésicos métricos — el búfer métrico de turf construye geometría en distancia real sobre el terreno y la proyecta a Web Mercator solo para su visualización.
- Las cifras de área — área de captación, densidad por kilómetro cuadrado — se calculan sobre el polígono geodésico, no a partir de píxeles de pantalla.

## Marco espacial

La población y el gasto se agregan en la cuadrícula hexagonal global H3 a resolución 7 (aproximadamente 5,16 km² por celda). La cuadrícula es mundial y consistente, lo que permite la comparación entre clústeres de los 13 países.

## Plan de migración (planeado)

La migración prevista desde los anillos de línea recta es por fases:

1. **Edición de honestidad.** Reetiquetado de cada anillo de línea recta como "banda de distancia (línea recta)"; exposición de la fórmula del radio, el factor 1,15, el piso de 1,0 km y la advertencia de Web Mercator en el modal de Metodología.
2. **O-D observado donde existen datos.** Conexión de los datos de movilidad LODES y MITMA ya incorporados para que los clústeres de EE. UU. y España muestren un polígono de origen laboral observado.
3. **Isócronas de tiempo de conducción.** Configuración de un motor de enrutamiento auto-alojado y oferta de una banda de tiempo de conducción fijo como la vista de área alcanzable predeterminada.
4. **Calibración de decaimiento de distancia.** Ajuste de curvas de decaimiento a los flujos de O-D para establecer límites de percentil de demanda publicados.

## Véase también

- [[co-location-tiering-scoring]] — cómo se asignan los niveles de composición a los clústeres y el puntaje de fortaleza planeado
- [[spend-population-provenance]] — la cadena de estimación para población y gasto dentro del área de atracción
- [[regional-market-definition]] — el resumen a nivel de asentamiento construido sobre clústeres de co-ubicación
- [[app-orchestration-gis]] — la capa de orquestación que ejecuta la canalización de análisis espacial
