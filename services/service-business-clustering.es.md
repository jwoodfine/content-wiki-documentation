---
schema: foundry-doc-v1
title: "Agrupación comercial"
slug: service-business-clustering
short_description: "Un patrón espacial padre-hijo que convierte puntos minoristas en bruto en una entidad comercial por sitio físico, para que la canalización GIS razone sobre una ubicación una sola vez en lugar de una vez por cada inquilino colocalizado."
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-business-clustering.md
cites: []
---

Los datos minoristas son inherentemente desordenados — un solo sitio comercial suele contener múltiples puntos distintos, como un ancla de gran formato, una farmacia anidada y una estación de servicio que comparten el mismo estacionamiento. El paso de agrupación comercial de la plataforma convierte esos puntos en bruto en clústeres comerciales mediante un patrón padre-hijo, de modo que el análisis GIS posterior razone sobre una entidad comercial unificada por sitio físico en lugar de varios registros superpuestos.

## El patrón padre-hijo

Los puntos que plausiblemente pertenecen al mismo sitio físico se fusionan en un pequeño número de pasadas basadas en proximidad, usando distintos umbrales de distancia según si los puntos comparten una señal identificadora (la misma cadena minorista, por ejemplo) o solo coinciden a nivel de marca. El punto con mayor peso en un sitio fusionado se convierte en el registro padre; el resto pasa a ser hijo. Sin este paso, varios inquilinos colocalizados en un sitio contarían cada uno como una señal independiente en la puntuación posterior, sobrestimando el peso comercial de esa ubicación.

## Dónde encaja esto en la canalización

La agrupación se ejecuta como parte de la misma canalización GIS basada en Python documentada en [[app-orchestration-gis]] — el código que convierte datos geográficos y comerciales en bruto en el índice regional de co-localización — en lugar de como un servicio desplegado por separado. Este artículo no reproduce los umbrales de distancia específicos de la canalización ni los nombres internos de los scripts; el patrón general (fusionar puntos colocalizados, promover al ancla más fuerte a padre) es la parte estable y de cara pública del diseño.

## Véase también

- [[app-orchestration-gis]] — la canalización de la que este paso de agrupación forma parte
- [[service-fs-data-lake]] — los datos en bruto que consume este paso
