---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-egress
short_description: "El servicio de soberanía de datos que transfiere físicamente cargas útiles almacenadas en la nube al almacenamiento en frío local, ejecutando protocolos de flujo que eliminan retención de datos del lado del proveedor y dependencia de almacenamiento en la nube."
title: "Servicio de egreso"
category: services
language: es
paired_with: service-egress.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

[[service-fs-architecture|`service-egress`]] es el motor de soberanía de datos que transfiere físicamente las cargas almacenadas en la nube al almacenamiento local en frío, ejecutando el protocolo de flujo que elimina la retención de datos del proveedor y la dependencia de la continuidad del almacenamiento en nube. Las cargas transferidas se escriben en el [[worm-ledger-design|libro mayor WORM]] por inquilino gestionado por [[service-fs-architecture]], donde se convierten en registros de solo adición. El servicio trabaja junto a [[service-email]] para garantizar que cada mensaje ingestado de un buzón en la nube tenga una copia local permanente antes de que se limpie la fuente en la nube. Consulte la [[sovereign-airlock-doctrine|exclusa soberana]] para conocer el principio arquitectónico que rige la dirección del flujo de datos.

## Puntos clave

- El protocolo de flujo tiene tres pasos en orden: descargar de la nube → escribir en el WORM local → limpiar la fuente en la nube. La copia original en la nube se elimina; el registro WORM local es la copia permanente.
- Las cargas transferidas se convierten en registros WORM de solo adición. La ruta de egreso no puede sobrescribir ni eliminar registros anteriores — la soberanía de datos se aplica estructuralmente, no por política.
- service-egress opera en el límite de soberanía. Una vez que una carga cruza de la nube al almacenamiento WORM local, ya no está sujeta a las políticas de retención de datos, divulgación compelida o terminación de servicio del proveedor de nube.
- El servicio depende de [[service-email]] para la ingestión de buzones y de [[service-fs-architecture]] para la interfaz de almacenamiento WORM. Estos tres servicios constituyen juntos la pila de soberanía de datos de entrada.

## Protocolo de flujo

El protocolo de flujo sigue la secuencia siguiente:

1. **Adquisición** — `service-egress` se conecta a la fuente en la nube (un buzón vía IMAP, un almacén de objetos o un sistema de archivos en la nube) y obtiene la carga.
2. **Escritura** — la carga se escribe en el libro mayor WORM por inquilino vía `service-fs`. La escritura solo se confirma cuando el libro mayor certifica que el registro es duradero en el almacenamiento local.
3. **Limpieza** — solo tras una escritura local durable confirmada emite `service-egress` el comando de eliminación o archivado a la fuente en la nube. El paso de limpieza es condicional: si la escritura falla, la copia en la nube se conserva.

Esta ordenación garantiza que la pérdida de carga sea imposible dentro del dominio de fallo del servicio. Un fallo entre los pasos 2 y 3 deja la carga en ambos lugares; la siguiente ejecución deduplica antes de reintentar la limpieza.

## Véase también

- [[sovereign-airlock-doctrine]] — el principio arquitectónico que rige el flujo de datos unidireccional hacia el libro mayor WORM
- [[service-email]] — el servicio de ingestión de correo que coordina con service-egress para la ingestión de buzones
- [[service-fs-architecture]] — el servicio de sistema de archivos que proporciona la interfaz del libro mayor WORM
- [[worm-ledger-design]] — la disciplina de almacenamiento de solo adición en la que entran los registros de egreso
