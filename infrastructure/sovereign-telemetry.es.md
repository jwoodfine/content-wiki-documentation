---
schema: foundry-doc-v1
title: "Arquitectura de telemetría de estado cero"
slug: sovereign-telemetry
short_description: "Telemetría de estado cero: una única baliza al cierre de página con URI y marca temporal, emparejada del lado del servidor con la IP y el user agent del solicitante, escrita sin enmascarar en un registro CSV de solo anexado."
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: sovereign-telemetry.md
cites: []
---

La arquitectura de telemetría de estado cero es el enfoque de la plataforma para entender el tráfico del sitio sin cookies, identificadores de sesión ni un proveedor de análisis de terceros. Una página envía una pequeña baliza cuando el visitante se va; el servidor la captura junto con la dirección IP del solicitante y escribe una línea en un registro de solo anexado. No hay acumulación de estado del lado del cliente entre visitas — "estado cero" describe al cliente, no el registro del lado del servidor.

## Carga útil

En el evento `unload`, la página envía mediante `navigator.sendBeacon` un cuerpo JSON con dos campos: `uri` (la ruta de la página) y `timestamp` (el reloj del cliente, en milisegundos). No intervienen cookies, píxeles de seguimiento ni scripts de análisis de terceros — la baliza es un único POST del mismo origen.

El servidor empareja esa carga con dos valores que lee de la propia solicitud: la dirección IP del solicitante (de una cabecera de reenvío, la primera entrada si la cabecera contiene una cadena) y la cadena `User-Agent`. Los cuatro valores — IP, marca temporal, URI y user agent — se anexan como una línea a un registro CSV en texto plano. **Ninguno de los cuatro campos está enmascarado o truncado.** Véase [[data-sovereignty-telemetry|el artículo de la categoría de seguridad sobre este mismo demonio]] para las implicaciones de cumplimiento de la IP sin enmascarar específicamente, ya escaladas por separado — este artículo no vuelve a plantear ese hallazgo, solo describe la misma carga real desde el lado de la infraestructura.

## Véase también

- [[telemetry-architecture]] — cómo se enruta y procesa la carga de la baliza una vez que llega al servidor
- [[ontological-governance]] — gobernanza que rige el uso de señales de comportamiento
- [[verification-surveyor]] — el servicio que consume las señales de telemetría
- [[message-courier]] — enrutamiento de mensajes dentro de la plataforma
- [[customer-hostability]] — principios de custodia de datos del cliente que informan este diseño
