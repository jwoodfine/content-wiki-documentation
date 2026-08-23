---
schema: foundry-doc-v1
title: "Máquina de entrada"
slug: input-machine
aliases:
  - input-machine
short_description: "La Máquina de Entrada es la puerta obligatoria de incorporación de documentos en os-console, asignada permanentemente a F12 y respaldada por service-input en el Archivo Totebox."
category: systems
type: topic
content_type: topic
index_group: operator-surfaces
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: input-machine.md
language: es
---

La Máquina de Entrada es la puerta obligatoria de incorporación a través de la cual todos los documentos y textos ingresan a los flujos de trabajo de [[console-os|os-console]]. Ocupa permanentemente la tecla F12 en todas las configuraciones de teclado. Cada [[os-console-platform|cartucho]] en os-console depende de la Máquina de Entrada para su material de origen. Ningún flujo de trabajo la evita.

## Por qué la posición es permanente

La tecla F12 ocupa la posición límite en la fila de teclas de función, separada físicamente de F1–F11 por un espacio más amplio en la mayoría de los teclados. Esta posición es deliberada. La Máquina de Entrada no es una función de flujo de trabajo; es un control de frontera. Debe ser localizable inmediata e inequívocamente sin importar qué cartucho esté activo.

La decisión de arquitectura de sistema SYS-ADR-10 establece F12 como el punto de control humano obligatorio para todas las operaciones de ingesta. La asignación no puede ser evitada por otro panel ni reasignada. Estas restricciones se aplican en el despachador de eventos de `app-console-keys`, no por convención.

## Qué ocurre al presionar F12

Al presionar F12 en cualquier punto de os-console se suspende el cartucho activo y se abre el modal de la Máquina de Entrada. El operador completa el flujo de ingesta. Luego el cartucho se reanuda.

El flujo de ingesta opera así. Un modal presenta el campo de ruta del archivo; el operador ingresa y confirma la ruta (no se acepta envío pasivo). `app-console-input` envía la ruta, el nombre de usuario y el arrendatario al endpoint `/v1/append` de `service-input` en el Archivo Totebox. `service-input` lee el archivo, lo verifica por hash y lo omite si ya fue procesado; a los archivos nuevos les asigna una marca de destino aproximada — `service-research` o `service-minutebook` si la ruta contiene esa cadena, `service-content` en cualquier otro caso — y los reenvía a `service-fs`. `service-input` escribe su propia entrada de ledger (ID de carga, ruta, hash, marca de tiempo, marca de destino) y `app-console-input` escribe un registro local (marca de tiempo, operador, arrendatario, ruta, estado). Por último, el cartucho activo se reanuda con el documento incorporado disponible en su contexto.

## service-input: el servicio frontera de ingesta

`service-input` es la contraparte del lado servidor del cartucho de la [[app-console-input|Máquina de Entrada]], ejecutándose en el Archivo Totebox. Lee un documento una vez, lo deduplica por hash de contenido y lo reenvía a [[service-fs|service-fs]] bajo una etiqueta aproximada. No clasifica el tipo de documento ni lo enruta a distintos servicios según su contenido — todo archivo no duplicado termina en `service-fs`, distinguido solo por su etiqueta, sin una ruta separada hacia `service-proofreader`, un manejador específico para BIM, ni ningún otro destino sensible al contenido.

`service-input` no realiza inferencia de inteligencia artificial — la asignación de etiqueta es una simple comprobación de subcadena sobre la ruta del archivo, no un clasificador por tipo MIME o firma estructural. Esto mantiene el paso de ingesta reproducible e independiente de la disponibilidad del modelo, conforme a SYS-ADR-07.

## La pista de auditoría

Cada documento que pasa por la Máquina de Entrada genera dos registros.

Un registro local en SQLite en la máquina de os-console guarda la marca de tiempo, el operador, el arrendatario, la ruta del archivo y un campo de estado. Este registro local persiste incluso si el [[totebox-archive|Archivo Totebox]] no está disponible.

Una entrada de ledger independiente en el propio `service-input` registra el ID de carga, la ruta del archivo, el hash de contenido, la marca de tiempo y la etiqueta de destino asignada. Juntos, estos dos registros establecen cuándo llegó un documento, quién lo envió y adónde se reenvió — pero ninguno registra una clasificación de contenido, porque no se realiza ninguna.

## El cartucho app-console-input

`app-console-input` es el crate del cartucho F12 en `pointsav-monorepo`. Implementa el
flujo de trabajo de la Máquina de Entrada en el lado cliente de os-console: renderiza el
modal de entrada de ruta de archivo, envía la solicitud POST a `service-input` con un
tiempo de espera de 30 segundos, y escribe la entrada de auditoría local en SQLite.
Cuando termina la ingesta, devuelve el control al cartucho previamente activo.

`app-console-input` siempre está instalado y el modal siempre es accesible mediante F12.
Esto no es configurable.

## Cumplimiento de ADR-07

SYS-ADR-07 establece que ningún dato estructurado pasa por inferencia de IA. La Máquina
de Entrada aplica esta regla en la frontera de ingesta — la asignación de etiqueta de
`service-input` es una comprobación de subcadena determinista sobre la ruta del archivo,
no una llamada a un modelo. Dado el mismo archivo, `service-input` siempre produce la
misma etiqueta, y el registro de auditoría nunca depende de versiones del modelo ni de
la disponibilidad de la inferencia.

## La arquitectura sin formularios

La Máquina de Entrada es el fundamento de lo que la documentación operativa describe como la arquitectura sin formularios. Los flujos de trabajo tradicionales requieren que el operador rellene campos para contextualizar un documento antes de que ingrese al sistema. La Máquina de Entrada invierte esto: el operador proporciona un documento y confirma la intención, y el sistema lo registra, etiqueta y reenvía sin más captura de datos. La única entrada requerida es el documento en sí y una confirmación explícita de la intención de enviarlo.

## Reanudación tras la ingesta

Cada cartucho utiliza la misma Máquina de Entrada para su material de origen, y F12
siempre devuelve el control al cartucho que estaba activo cuando se presionó. Es el
cartucho activo, no la etiqueta de destino asignada, lo que determina qué ocurre con el
documento dentro del flujo propio de ese cartucho. La etiqueta que asigna
`service-input` es independiente de qué tecla de función abrió el modal — refleja solo
dónde coincidió el texto de la ruta, no qué cartucho envió el archivo.

## Véase también

- [[console-os]] — la plataforma de os-console
- [[machine-based-auth]] — el mecanismo de autorización de os-console
- [[three-ring-architecture]] — la arquitectura de tres anillos
- [[os-console-platform]] — la arquitectura de cartuchos y el mapa de teclas de función
- [[worm-ledger-design]] — la disciplina del ledger de solo adición para los registros de auditoría
