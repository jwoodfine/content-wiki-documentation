---
schema: foundry-doc-v1
title: "Registro de plantillas (service-email-template)"
slug: template-ledger.es
category: services
type: topic
quality: complete
short_description: "El Registro de Plantillas es el mecanismo de distribución dentro de service-email-template que sincroniza una única copia autoritativa de cada plantilla aprobada con el entorno de correo del operador — eliminando la deriva de versiones entre el diseño de la plantilla y la ejecución del operador, y eliminando cada paso de redacción de la correspondencia corporativa rutinaria."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: template-ledger.md
cites: []
---

El Registro de Plantillas es el mecanismo de distribución dentro de `service-email-template` que sincroniza automáticamente una única copia autoritativa de cada plantilla aprobada con el entorno de correo del operador. Elimina la deriva de versiones entre el diseño de la plantilla y la ejecución del operador manteniendo una sola copia canónica por identificador de plantilla; el operador recupera la versión actual mediante una clave y la envía directamente. La distinción entre redactar y desplegar se vuelve estructural en lugar de procedimental — el operador no está redactando correspondencia corporativa rutinaria, solo seleccionando qué plantilla aprobada despachar.

## Intención de diseño

Los operadores de Woodfine Management Corp. no redactan correos corporativos de rutina desde cero. Cada tipo de plantilla —avisos de cumplimiento, divulgaciones financieras, correspondencia con clientes— existe como un registro versionado en el Registro de Plantillas. Los operadores recuperan la versión actual mediante una clave y la envían directamente. La distinción entre redactar y desplegar es estructural, no meramente procedimental.

## Flujo de trabajo del operador

El operador abre su carpeta `Template Ledger` en Microsoft 365, accede al catálogo `.html` adjunto al correo `[TMPL-000]`, filtra por categoría (por ejemplo, *Compliance* o *Finance*) y copia la clave de la plantilla deseada. A continuación, pega la clave en la barra de búsqueda de M365 para obtener la versión actual, hace clic en **Reenviar**, actualiza el destinatario, elimina el bloque de metadatos de enrutamiento y envía.

## Sincronización silenciosa

Cuando un ingeniero de PointSav actualiza una plantilla, el servicio de sincronización utiliza la API de Microsoft Graph para reemplazar la versión anterior en la subcarpeta del operador por la nueva, sin enviar ninguna notificación. La ausencia de notificaciones es deliberada: la plantilla actual siempre está disponible en la carpeta y no se requiere ninguna acción por parte del operador para recibirla.

## Véase también

- [[service-email]] — el servicio de ingesta de correo del Anillo 1
- [[disclosure-substrate]] — la arquitectura de divulgación que rige las comunicaciones salientes
