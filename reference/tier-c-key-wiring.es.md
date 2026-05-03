---
schema: foundry-doc-v1
title: "Conexión de Claves del Nivel C"
slug: tier-c-key-wiring.es
category: reference
type: topic
quality: published
short_description: El procedimiento operativo para gestionar las claves de API externas en el servicio Doorman — dónde viven las claves, cómo se aprovisionan, cómo rotan y cómo se contiene una brecha.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tier-c-key-wiring.md
---

El Nivel C de la arquitectura de enrutamiento de cómputo de PointSav enruta las solicitudes asistidas por inteligencia artificial a proveedores externos de modelos de lenguaje a través de HTTPS. El servicio Doorman es el único componente del marco que conserva las claves de API de los proveedores. Este artículo describe el procedimiento operativo para gestionar las claves del Nivel C: dónde se almacenan, cómo se aprovisionan y rotan, cómo se auditan el costo y el uso, y cómo se contiene un compromiso sospechado.

## Principio rector

Las claves de API viven en el portal únicamente — nunca en el código de aplicación, nunca en archivos rastreados por control de versiones y nunca en registros o registros de auditoría. El binario del Doorman lee las claves de su entorno en el momento de inicio y las conserva en la memoria del proceso. Las claves nunca se escriben en disco por el Doorman, nunca se ecos en los cuerpos de respuesta y nunca se incluyen en ningún nivel de registro de salida.

## Dónde viven las claves

Las claves se conservan en archivos de extensión de unidad systemd en la máquina virtual de trabajo. Cada proveedor puede tener su propio archivo de extensión, lo que hace que la rotación por proveedor sea atómica. Los archivos de extensión son propiedad de root y legibles por el usuario del servicio que ejecuta el Doorman. No están rastreados en ningún repositorio de control de versiones.

## Aprovisionamiento y rotación

Activar una nueva clave requiere la presencia del operador para los pasos que tocan el valor de la clave. La secuencia de ocho pasos comienza con la obtención de la clave desde la consola del proveedor, crea un archivo temporal con permisos restringidos para la clave, escribe la extensión systemd del Doorman, recarga el servicio, verifica el funcionamiento con una llamada de prueba de bajo costo, y finaliza con la eliminación segura del archivo temporal y una entrada en el registro de cambios.

La rotación trimestral por proveedor es el ritmo predeterminado. La rotación acelerada es apropiada cuando se sospecha un compromiso, cuando el proveedor exige rotación en su propio calendario, o cuando el operador elige un ritmo más frecuente.

## Postura de auditoría y respuesta a brechas

Cada llamada al Nivel C produce una entrada en el registro de auditoría por inquilino con: nombre del proveedor, nombre del modelo, conteos de tokens, costo en USD calculado, latencia de extremo a extremo, identificador del inquilino, propósito de la llamada y estado de éxito. Una brecha — cualquier evento que exponga el valor de una clave más allá del límite del Doorman — requiere revocación inmediata en la consola del proveedor antes de limpiar la fuente de la filtración.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
