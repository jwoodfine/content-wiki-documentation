---
schema: foundry-doc-v1
title: "Filtrado de lugares"
slug: service-places-filtering
short_description: "Un paso de filtrado que conserva solo instituciones de nivel regional de los datos cívicos en bruto, para que los rankings de nivel GIS reflejen concentración institucional en lugar de cada clínica e instalación comunitaria."
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-places-filtering.md
cites: []
references:
  - id: 1
    text: "Point of interest. Wikipedia, consultado el 2026-06-14."
    url: "https://es.wikipedia.org/wiki/Punto_de_inter%C3%A9s"
---

Los [[retail-co-location-tier-methodology|rankings de nivel GIS]] dependen de saber dónde se
ubican las instituciones regionales, no dónde se ubica cada clínica o instalación comunitaria
local. El paso de filtrado de lugares de la plataforma conserva solo las instalaciones
cívicas e institucionales que alcanzan una escala regional — hospitales, universidades y
centros de transporte importantes validados por encima de umbrales de tamaño fijos — y
consolida los registros de campus multipunto en un solo ancla regional. La densidad de
servicios locales se elimina en esta etapa, de modo que los rankings posteriores reflejan
concentración institucional en lugar del recuento bruto de instalaciones.[^1]

## Lo que conserva el filtro

El filtro aplica umbrales fijos y estructurales en lugar de parámetros configurables: un
hospital debe alcanzar un recuento mínimo de camas con personal, una universidad una
matrícula mínima equivalente a tiempo completo, y un aeropuerto debe ser un centro regional
validado en lugar de una instalación de aviación general. Las instituciones por debajo de
estos umbrales se descartan antes de que se ejecute cualquier puntuación posterior.

## Consolidación de registros de campus

Un campus institucional grande suele aparecer en los datos geoespaciales abiertos en bruto
como muchos puntos separados. El filtro fusiona los puntos que plausiblemente pertenecen al
mismo campus físico en un solo ancla regional con un centroide unificado, evitando que una
sola institución grande se cuente muchas veces.

## Dónde encaja esto en la canalización

El filtrado se ejecuta como parte de la misma canalización GIS basada en Python documentada
en [[app-orchestration-gis]] — el código que convierte datos geográficos y comerciales en
bruto en el índice regional de co-localización — en lugar de como un servicio desplegado por
separado. Su salida alimenta a [[app-orchestration-gis]] junto con el paso de agrupación
minorista de [[service-business-clustering]] cuando la canalización asigna los niveles
finales de co-localización. Este artículo no reproduce los umbrales específicos de la
canalización, las distancias de buffer, ni los nombres de archivos internos; el patrón
general (descartar instalaciones subregionales, consolidar campus multipunto en un solo
ancla) es la parte estable y de cara pública del diseño.

## Véase también

- [[app-orchestration-gis]] — la canalización de la que este paso de filtrado forma parte
- [[service-business-clustering]] — el paso de agrupación minorista que se ejecuta junto a él
- [[service-fs-data-lake]] — los datos cívicos y minoristas en bruto que consume este paso
- [[retail-co-location-tier-methodology]] — la metodología de niveles que alimentan los datos filtrados
