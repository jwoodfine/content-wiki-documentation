---
schema: foundry-doc-v1
content_type: topic
title: "Cómo app-orchestration-command publica los cambios de un archivo"
slug: app-orchestration-command-publication-flow
short_description: "app-orchestration-command es el coordinador que transfiere código validado desde los Totebox Archives hacia los repositorios canónicos, aplicando un único límite de auditoría e impidiendo que el estado operativo contamine el historial canónico."
category: architecture
type: reference
quality: complete
status: stable
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: app-orchestration-command-publication-flow.md
cites: []
---

`app-orchestration-command` es el servicio coordinador que transfiere código validado desde los Totebox Archives individuales hacia los repositorios canónicos `pointsav/*` y `woodfine/*`. Este artículo explica qué significa la publicación, quién puede iniciarla y cómo se comporta el sistema cuando el coordinador no está disponible.

## Qué significa publicar

La publicación es el acto de confirmar código revisado y probado de un Totebox Archive en el repositorio de referencia aguas arriba. El resultado es una entrada firmada y permanente en el historial canónico, que no puede modificarse ni retirarse sin una acción de gobernanza explícita.

La publicación mueve únicamente código. Los archivos de estado operativo —memoria de sesión, documentos en borrador, notas operativas— quedan excluidos en la capa de filtrado y nunca aparecen en el historial canónico. Esta separación es deliberada: el historial canónico es un registro de auditoría, no un diario operativo.

## Por qué existe un coordinador central

`app-orchestration-command`, que se ejecuta en `os-orchestration`, posee la credencial SSH de administrador necesaria para escribir en los repositorios canónicos. Concentrar la autoridad de publicación en un único punto sirve a tres propósitos:

1. **Límite de auditoría único.** El coordinador registra cada evento de publicación. No existe ninguna ruta secundaria que pueda producir una confirmación no registrada en el historial canónico.
2. **Prevención de conflictos.** Dos archivos que publiquen simultáneamente podrían generar estados canónicos en conflicto. El coordinador serializa las solicitudes de publicación para garantizar que cada una sea una integración limpia de avance rápido (*fast-forward*).
3. **Integridad del historial.** El coordinador exige que solo los commits que superen el filtro de publicación lleguen a `origin/main`. Ningún contenido de estado operativo entra en el historial canónico, independientemente del archivo que haya enviado la solicitud.

## Criterios de publicación

Antes de iniciar la publicación, el coordinador verifica:

- La rama local del archivo está actualizada con `origin/main` (rebasada, sin conflictos).
- El árbol de trabajo está limpio (sin modificaciones sin confirmar).
- La suite de compilación y pruebas pasa (verificado por la puerta de pre-publicación).
- El conjunto de commits contiene al menos un cambio de código (la publicación con solo archivos de estado operativo no produce ningún efecto y termina de forma limpia).

Los commits que únicamente afectan archivos de estado operativo se detectan y omiten automáticamente. Permanecen en la rama aislada del archivo y se envían al espejo de preparación para garantizar su durabilidad.

## Modelo de elegibilidad

Cada Totebox Archive declara un nivel de capacidad de autoservicio que el coordinador lee antes de decidir cómo gestionar una solicitud de publicación:

| Nivel de capacidad | Quién ejecuta la publicación |
|---|---|
| Coordinador requerido | El coordinador debe ejecutar la publicación en nombre del archivo. El archivo envía la solicitud y espera. |
| Autoservicio *(previsto/en desarrollo)* | El archivo puede iniciar la publicación directamente, siempre que la clave de administrador sea accesible desde el entorno del archivo. El coordinador valida la solicitud a posteriori. |
| No elegible | El archivo está en estado de planificación o inactivo. Las solicitudes de publicación se rechazan hasta que el archivo transite a un estado activo. |

El nivel de capacidad lo establece el operador del archivo y se revisa durante el aprovisionamiento. Aumentar el nivel requiere la aprobación del coordinador.

## Comportamiento sin conexión

Si `app-orchestration-command` no está disponible —mantenimiento programado, un evento de hardware o una partición de red— los archivos con solicitudes de publicación pendientes escriben dichas solicitudes en una cola duradera. El coordinador vacía la cola en el próximo arranque, procesando cada entrada en orden de envío.

Los archivos en modo de autoservicio *(previsto/en desarrollo)* también pueden escribir en esta cola como alternativa cuando la clave de administrador no está temporalmente disponible. Ningún intento de publicación se descarta silenciosamente.

## Temas relacionados

- [[app-orchestration-command-branch-model]] — cómo el aislamiento de archivos evita la contaminación del historial canónico con estado operativo
- [[scaling-coordinated-development-totebox-archives]] — el desafío de coordinación a medida que crece el número de archivos

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
