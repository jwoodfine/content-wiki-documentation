---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-orchestration-stateless-hub
title: "os-orchestration: La Capa de Agregación Sin Estado"
short_description: "os-orchestration coordina el trabajo entre los Archivos Totebox sin almacenar datos de clientes, claves ni registros de auditoría, actuando como superficie de enrutamiento e intermediación sin estado por encima de la capa de capacidades por archivo."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: os-orchestration-stateless-hub.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
---

# os-orchestration: La Capa de Agregación Sin Estado

La plataforma PointSav está construida alrededor de un límite arquitectónico deliberado: la capa de agregación que coordina el trabajo entre los Archivos Totebox no retiene datos de clientes, no almacena claves y no escribe nada en ningún libro de registro WORM. Esta capa es `os-orchestration`.

Comprender qué es `os-orchestration` requiere primero entender qué no es. No es una base de datos, no es un almacén de credenciales y no es un custodio. Cada archivo en la red PointSav mantiene su propio estado aislado: su propio registro de auditoría WORM, su propio material de claves, su propio segmento de DataGraph. `os-orchestration` se sitúa por encima de esa capa como coordinador: enruta solicitudes, aplica límites de capacidad y gestiona el trabajo entre archivos sin acceder nunca a los datos subyacentes.

## El Modelo de Federación

El acceso entre Archivos Totebox está gobernado por Dominios de Protección (PDs). Cada archivo ejecuta su propio PD de intermediación de capacidades, que posee la única autoridad para otorgar o denegar el acceso entre Totebox para ese archivo. La regla es estricta: ningún PD de capa de aplicación contacta directamente a un Totebox. Cada solicitud entre archivos pasa por el PD de intermediación de capacidades del archivo de destino, que aplica el límite de capacidad por organización definido para esa organización.

`os-orchestration` opera en la capa de federación, por encima de los PDs por archivo. Puede observar que existe una solicitud y enrutarla al intermediario de capacidades apropiado, pero no puede autorizar la solicitud por sí mismo. La autorización reside donde residen los datos: en el archivo.

Este diseño refleja la Geometría de Capacidades en la capa de federación. Los datos de cada organización están encerrados dentro de un límite de capacidad que `os-orchestration` no puede cruzar en nombre de otra organización. Una solicitud de una organización no puede enrutarse al archivo de otra organización explotando la capa de agregación. La geometría del sistema hace esto imposible por construcción, no por política.

## Lo Que Significa Sin Estado para la Confianza

La ausencia de estado es una propiedad de confianza, no simplemente un detalle de implementación. Dado que `os-orchestration` no escribe nada y no almacena nada, no puede ser obligado a producir datos de clientes que no posee. Una orden judicial dirigida a la capa de agregación no obtiene nada de sustancia. Una brecha en la capa de agregación expone la topología de enrutamiento, no el contenido.

Esto contrasta con arquitecturas de concentrador y radio donde el concentrador acumula estado de sesión, credenciales en caché o datos derivados. En esos diseños, el concentrador se convierte en un objetivo. En el modelo PointSav, la capa de agregación es estructuralmente inerte respecto a los datos de los clientes. Los archivos son los custodios; `os-orchestration` es la centralita.

En términos prácticos, esto significa que `os-orchestration` no tiene ninguna obligación bajo las regulaciones de residencia o custodia de datos. Las obligaciones regulatorias se adhieren a los archivos, que pueden ser aprovisionados en jurisdicciones específicas. La capa de agregación puede ejecutarse en cualquier lugar.

## El Modelo Comercial

La estructura comercial de la plataforma PointSav sigue el modelo de Anillos. Los dos primeros Anillos de capacidad — los servicios fundamentales que cada Totebox requiere para operar — se proporcionan sin cargo con cada aprovisionamiento de Totebox. Esto cubre el nivel de inferencia local (Nivel A), el acceso básico a DataGraph y la pila de servicios estándar.

El nivel de pago se activa cuando las cargas de trabajo superan la capacidad local o cuando los operadores eligen acceder al mercado de datos más amplio. La inferencia de Nivel B se enruta a través de `os-orchestration` hacia el centro de inferencia, donde la capacidad se agrupa en toda la red. El mercado de datos permite a los archivos publicar conjuntos de datos estructurados y consumir conjuntos de datos publicados por otros archivos dentro del límite de capacidad.

Los ingresos se acumulan en la capa de agregación para las transacciones de Nivel B y del mercado. La capa de agregación es la puerta de enlace comercial aunque no sea un custodio de datos. Este es el diseño previsto: la monetización fluye a través del enrutamiento y el control de acceso, no a través de la acumulación de datos.

## El Intermediario de GPU Yo-Yo

`app-orchestration-slm` es el intermediario comercial de GPU Yo-Yo, que implementa el mecanismo de asignación de GPU bajo demanda. Cuando un Archivo Totebox envía una solicitud de inferencia que supera la capacidad local de Nivel A — ya sea porque el modelo es demasiado grande para el hardware local o porque la carga concurrente ha agotado el cómputo disponible — la solicitud se enruta a `app-orchestration-slm`.

El intermediario mantiene un grupo de capacidad de GPU extraído de la Red Privada PointSav y de proveedores externos contratados. Asigna capacidad bajo demanda, enruta la solicitud de inferencia y devuelve el resultado al archivo de origen. El archivo nunca requiere su propio hardware de GPU para cargas de trabajo de Nivel B; el intermediario proporciona elasticidad.

El nombre refleja la metáfora de diseño: la capacidad de cómputo se extiende hacia afuera desde el archivo bajo demanda y se retrae cuando la solicitud se completa. El archivo no mantiene ninguna asignación de GPU persistente entre solicitudes.

## Lo Que Esto Significa en el Despliegue

Cuando un operador aprovisiona una instancia de `os-orchestration`, está desplegando una superficie de enrutamiento e intermediación, no un sistema de almacenamiento. La lista de verificación de aprovisionamiento es por tanto más corta que para un Archivo Totebox: sin configuración de almacenamiento WORM, sin aprovisionamiento de claves más allá de los certificados TLS requeridos para la autenticación mutua con los archivos que servirá, sin migración de datos.

Una instancia de `os-orchestration` puede reemplazarse, escalarse o reubicarse sin pérdida de datos, porque no contiene datos. Esta propiedad hace que la capa de agregación sea sencilla de operar: sus modos de fallo se limitan a la disponibilidad (es inaccesible) en lugar de a la integridad (su estado ha derivado o sido corrompido).

Por la misma razón, `os-orchestration` nunca es el sistema de registro para ningún proceso de negocio. Los operadores que necesitan auditar lo ocurrido — qué archivo procesó qué solicitud, cuándo, bajo la autorización de quién — leen el libro de registro WORM del Archivo Totebox correspondiente. La capa de agregación está ausente de ese registro de auditoría excepto como nodo de enrutamiento.

## Anclajes de Doctrina

El diseño de `os-orchestration` está fundamentado en cuatro posiciones doctrinales. La estructura comercial, que incluye el modelo de Anillos y el intermediario Yo-Yo, establece el mecanismo de asignación de GPU bajo demanda. Las disposiciones del mercado de datos gobiernan los límites de capacidad por organización que previenen la fuga de datos entre organizaciones. La obligación de auditoría WORM se aplica a los archivos y excluye deliberadamente la capa de agregación. Las superficies de orquestación orientadas al navegador (`app-orchestration-exchange`, `app-orchestration-market`) operan como la cara visible para el cliente de la capa de agregación.

En conjunto, estas posiciones definen una plataforma donde la coordinación está separada de la custodia. La capa de agregación es eficaz precisamente porque no retiene lo que enruta.
