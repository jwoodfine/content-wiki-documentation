---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-orchestration-stateless-hub
title: "os-orchestration: La Capa de Agregación Sin Estado"
short_description: "os-orchestration coordina el trabajo entre los Archivos Totebox sin almacenar datos de clientes, claves ni registros de auditoría, actuando como superficie de enrutamiento e intermediación sin estado por encima de la capa de capacidades por archivo."
audience: vendor-public
bcsc_class: forward-looking
language: es
paired_with: os-orchestration-stateless-hub.md
category: infrastructure
index_group: fleet-and-edge-deployment
status: active
quality: complete
last_edited: 2026-08-03
---

La plataforma PointSav está diseñada alrededor de un límite arquitectónico deliberado: una capa de agregación pensada para coordinar el trabajo entre los [[totebox-archive|Archivos Totebox]] sin retener datos de clientes, sin almacenar claves y sin escribir nada en ningún [[worm-ledger-architecture|libro de registro WORM]]. Esta capa está planeada como `os-orchestration` — hoy un crate de scaffold registrado pero sin implementar, no un sistema en funcionamiento.

Comprender qué está previsto que sea `os-orchestration` requiere primero entender qué está diseñado para no ser. No está pensado como una base de datos, ni como un almacén de credenciales, ni como un custodio. Cada archivo en la red PointSav está diseñado para mantener su propio estado aislado: su propio registro de auditoría WORM, su propio material de claves, su propio segmento de DataGraph. `os-orchestration` está planeado para situarse por encima de esa capa como coordinador: enrutando solicitudes, aplicando límites de capacidad y gestionando el trabajo entre archivos sin acceder nunca a los datos subyacentes.

## El Modelo de Federación (previsto)

El acceso entre Archivos Totebox está diseñado para ser gobernado por Dominios de Protección (PDs). Cada archivo ejecutaría su propio PD de intermediación de capacidades, con la única autoridad para otorgar o denegar el acceso entre Totebox para ese archivo. La regla prevista es estricta: ningún PD de capa de aplicación contactaría directamente a un Totebox. Cada solicitud entre archivos pasaría por el PD de intermediación de capacidades del archivo de destino, que aplicaría el límite de capacidad por organización definido para esa organización.

`os-orchestration` está planeado para operar en la capa de federación, por encima de los PDs por archivo — pudiendo observar que existe una solicitud y enrutarla al intermediario de capacidades apropiado, pero sin poder autorizar la solicitud por sí mismo. La autorización está diseñada para residir donde residen los datos: en el archivo.

Este diseño busca reflejar la [[capability-geometry|Geometría de Capacidades]] en la capa de federación. Los datos de cada organización estarían encerrados dentro de un límite de capacidad que `os-orchestration` no podría cruzar en nombre de otra organización. Una solicitud de una organización no podría enrutarse al archivo de otra organización explotando la capa de agregación — por diseño, no solo por política, una vez construido.

## Lo Que Se Prevé que Signifique la Ausencia de Estado para la Confianza

La ausencia de estado está diseñada como una propiedad de confianza, no simplemente un detalle de implementación. Dado que `os-orchestration` está pensado para no escribir ni almacenar nada, no podría ser obligado a producir datos de clientes que no posee. Bajo este diseño, una orden judicial dirigida a la capa de agregación no obtendría nada de sustancia, y una brecha en la capa de agregación expondría la topología de enrutamiento, no el contenido.

Esto busca contrastar con arquitecturas de concentrador y radio donde el concentrador acumula estado de sesión, credenciales en caché o datos derivados — diseños en los que el concentrador se convierte en un objetivo. En el modelo previsto de PointSav, la capa de agregación sería estructuralmente inerte respecto a los datos de los clientes: los archivos son los custodios; `os-orchestration` está pensada como la centralita.

En términos prácticos, este diseño busca que `os-orchestration` no tenga ninguna obligación bajo las regulaciones de residencia o custodia de datos, con las obligaciones regulatorias adhiriéndose en cambio a los archivos, que pueden aprovisionarse en jurisdicciones específicas. La capa de agregación, una vez construida, está pensada para poder ejecutarse en cualquier lugar.

## El Modelo Comercial

Se prevé que la estructura comercial de la plataforma PointSav siga un modelo de Anillos. Los dos primeros Anillos de capacidad previstos — los servicios fundamentales que cada Totebox necesitaría para operar — están pensados para proporcionarse sin cargo con cada aprovisionamiento de Totebox. Esto cubriría el nivel de inferencia local (Nivel A), el acceso básico a DataGraph y la pila de servicios estándar.

El modelo real de ingresos y medición por uso de Nivel B pertenece a un crate en funcionamiento, `app-orchestration-slm` — no a `os-orchestration`, que es un scaffold sin implementar y no tiene lógica de ingresos propia. `app-orchestration-slm` es un "chasis intermediario Yo-Yo" en funcionamiento (puerto `:9180`) que conecta las instancias Doorman de `service-slm` de los Archivos Totebox con una flota de GPU Yo-Yo compartida. Implementa una medición real de costos por inquilino: el costo de cada solicitud de inferencia se calcula a partir del tiempo de inferencia medido y una tarifa horaria en USD configurada, y se registra en un libro de contabilidad por inquilino contra el cual se factura a un cliente de Nivel B. El Nivel A — el nivel de inferencia local y gratuito — no se ve afectado por esto y no requiere medición. Si `os-orchestration` llega a construirse como capa de agregación/federación, podría en principio enrutar solicitudes hacia el servicio de Nivel B de `app-orchestration-slm`, pero la lógica de medición, facturación y acumulación de ingresos reside en `app-orchestration-slm`.

## El Intermediario de GPU Yo-Yo

`app-orchestration-slm` es el chasis [[yoyo-compute-substrate|intermediario de GPU Yo-Yo]] real y en funcionamiento, que implementa hoy la asignación de GPU bajo demanda y la medición por inquilino. Cuando el Doorman de `service-slm` de un Archivo Totebox envía una solicitud de inferencia que supera la capacidad local de Nivel A — ya sea porque el modelo es demasiado grande para el hardware local o porque la carga concurrente ha agotado el cómputo disponible — la solicitud se enruta al chasis de `app-orchestration-slm`.

El chasis se conecta a una flota de GPU Yo-Yo y enruta la solicitud de inferencia, devolviendo el resultado al archivo de origen. El archivo no necesita su propio hardware de GPU para cargas de trabajo de Nivel B; el chasis proporciona elasticidad y registra el costo de cada solicitud contra el inquilino solicitante.

El nombre refleja la metáfora de diseño: la capacidad de cómputo se extiende hacia afuera desde el archivo bajo demanda y se retrae cuando la solicitud se completa. El archivo no mantiene ninguna asignación de GPU persistente entre solicitudes.

## Lo Que Se Prevé que Esto Signifique en el Despliegue

Cuando un operador eventualmente aprovisione una instancia de `os-orchestration`, la intención es que esté desplegando una superficie de enrutamiento e intermediación, no un sistema de almacenamiento. La lista de verificación de aprovisionamiento está diseñada para ser más corta que para un Archivo Totebox: sin configuración de almacenamiento WORM, sin aprovisionamiento de claves más allá de los certificados TLS que se requerirían para la autenticación mutua con los archivos a los que serviría, sin migración de datos.

Se prevé que una instancia de `os-orchestration` pueda reemplazarse, escalarse o reubicarse sin pérdida de datos, porque está diseñada para no contener datos. Se busca que esta propiedad haga que la capa de agregación sea sencilla de operar: sus modos de fallo estarían limitados a la disponibilidad (es inaccesible) en lugar de a la integridad (su estado ha derivado o sido corrompido).

Por la misma razón, `os-orchestration` está diseñada para no ser nunca el sistema de registro de ningún proceso de negocio. Los operadores que necesiten auditar lo ocurrido — qué archivo procesó qué solicitud, cuándo, bajo la autorización de quién — leerían el libro de registro WORM del Archivo Totebox correspondiente. Se prevé que la capa de agregación esté ausente de ese registro de auditoría excepto como nodo de enrutamiento.

## Anclajes de Diseño

El diseño previsto de `os-orchestration` se apoya en varias posiciones arquitectónicas. La estructura comercial planeada, que incluye el modelo de Anillos, establece el marco dentro del cual opera hoy el mecanismo real de asignación de GPU y medición de `app-orchestration-slm`, descrito arriba. Las disposiciones del mercado de datos, si se construyen, están pensadas para gobernar los límites de capacidad por organización que evitarían la fuga de datos entre organizaciones. Se prevé que una obligación de auditoría WORM se aplique a los archivos y excluya deliberadamente la capa de agregación. Las superficies de orquestación orientadas al navegador (`app-orchestration-exchange`, `app-orchestration-market`) están pensadas para operar como la cara visible para el cliente de la capa de agregación, una vez construidas.

En conjunto, estas posiciones describen una plataforma donde se busca que la coordinación esté separada de la custodia. El objetivo de diseño es que la capa de agregación sea eficaz precisamente porque no retiene lo que enruta — aunque hoy, solo la parte de `app-orchestration-slm` de este panorama es real.
