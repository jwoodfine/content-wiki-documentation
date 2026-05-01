---
schema: foundry-topic-v1
title: "Registro de Plantillas (service-email-template)"
slug: topic-template-ledger
category: services
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

El Registro de Plantillas es el mecanismo de distribución dentro de `service-email-template` que garantiza que todas las comunicaciones corporativas salientes utilicen la versión actual y aprobada de cada plantilla. Elimina la deriva de versiones entre el diseño de la plantilla y su ejecución por parte del operador, manteniendo una única copia autoritativa por identificador de plantilla y sincronizándola automáticamente con el entorno de correo del operador.

## Intención de diseño

Los operadores de Woodfine Management Corp. no redactan correos corporativos de rutina desde cero. Cada tipo de plantilla —avisos de cumplimiento, divulgaciones financieras, correspondencia con clientes— existe como un registro versionado en el Registro de Plantillas. Los operadores recuperan la versión actual mediante una clave y la envían directamente. La distinción entre redactar y desplegar es estructural, no meramente procedimental.

## Flujo de trabajo del operador

El operador abre su carpeta `Template Ledger` en Microsoft 365, accede al catálogo `.html` adjunto al correo `[TMPL-000]`, filtra por categoría (por ejemplo, *Compliance* o *Finance*) y copia la clave de la plantilla deseada. A continuación, pega la clave en la barra de búsqueda de M365 para obtener la versión actual, hace clic en **Reenviar**, actualiza el destinatario, elimina el bloque de metadatos de enrutamiento y envía.

## Sincronización silenciosa

Cuando un ingeniero de PointSav actualiza una plantilla, el servicio de sincronización utiliza la API de Microsoft Graph para reemplazar la versión anterior en la subcarpeta del operador por la nueva, sin enviar ninguna notificación. La ausencia de notificaciones es deliberada: la plantilla actual siempre está disponible en la carpeta y no se requiere ninguna acción por parte del operador para recibirla.

## Véase también

- [[topic-service-email]] — el servicio de ingesta de correo del Anillo 1
- [[topic-disclosure-substrate]] — la arquitectura de divulgación que rige las comunicaciones salientes

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
