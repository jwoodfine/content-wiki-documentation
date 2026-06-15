---
schema: foundry-doc-v1
title: "app-console-email — cartucho de comunicaciones"
slug: app-console-email
category: applications
type: app
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: app-console-email.md
short_description: "app-console-email es el cartucho de comunicaciones F3 de os-console. Proporciona listado de bandeja de entrada, lectura de mensajes y redacción y envío, operando a través de service-email como el Diodo de Comunicaciones entre el operador y los corresponsales externos."
cites: []
---

`app-console-email` es el cartucho de comunicaciones F3 de [[console-os|os-console]]. Se conecta a [[service-email|service-email]] y proporciona una interfaz orientada al operador para tres tareas de comunicación: leer una bandeja de entrada, leer un mensaje y redactar y enviar un mensaje. El cartucho es completamente controlado por teclado; no se requiere interacción por puntero.

El cartucho implementa el rasgo `Cartridge` definido por [[app-console-keys|app-console-keys]], ocupando el slot F3 en la barra de navegación de la consola.

## El modelo del Diodo de Comunicaciones

`app-console-email` no es un cliente de correo electrónico de propósito general. Los mensajes salientes fluyen a través de `service-email` — un servicio que actúa como Diodo de Comunicaciones entre el [[totebox-os|Totebox]] del operador y los corresponsales externos. La analogía del diodo refleja una restricción de diseño: `service-email` controla la ruta de salida y aplica las políticas de comunicación del tenant antes de que cualquier mensaje cruce el límite de la plataforma.

Esto significa que el cartucho no habla directamente con un servidor de correo externo. Redacta un mensaje, lo envía a `service-email`, y el servicio gestiona el enrutamiento, la cola y la entrega. El cartucho recibe una confirmación de entrega o un error; no gestiona sesiones SMTP o IMAP por sí mismo.

## Vista de bandeja de entrada

La vista de bandeja de entrada lista los mensajes recibidos en orden cronológico inverso. Cada fila muestra el remitente, el asunto y la marca de tiempo de recepción. La lista se actualiza cuando el cartucho está enfocado y bajo demanda mediante atajo de teclado.

Los mensajes provienen del almacén de mensajes de `service-email`. El cartucho no mantiene su propia copia local; todo el estado reside en el servicio.

## Lectura de mensajes

Seleccionar un mensaje de la bandeja de entrada abre la vista de lectura. Esta vista muestra el cuerpo completo del mensaje, las cabeceras y los adjuntos listados por nombre. El contenido de los adjuntos está disponible para descarga a una ruta de preparación; los adjuntos no se abren automáticamente.

El modo de texto plano está disponible mediante el indicador `--plain` al iniciar la consola. En modo plano, los cuerpos de mensaje solo en HTML se renderizan como su alternativa de texto sin formato. Los terminales sin soporte Unicode reciben aproximaciones ASCII de los símbolos Unicode en las líneas de asunto y nombres de remitente.

## Redacción y envío

La vista de redacción proporciona campos para destinatario, asunto y cuerpo. La interfaz es estructurada: el operador completa cada campo en secuencia usando navegación por teclado. El envío entrega el mensaje redactado a `service-email` para su procesamiento de salida.

El guardado de borradores no está implementado. Una sesión de redacción abandonada se descarta; ningún mensaje parcial persiste en el almacén del servicio.

## Dependencia de autorización

La conexión del cartucho con `service-email` es mediada por el cliente de [[machine-based-auth|autorización basada en máquina]] gestionado por [[app-console-keys|app-console-keys]]. Si el enlace de autorización con el servicio de correo electrónico está inactivo, la vista de bandeja de entrada muestra el estado `MBA LINK INACTIVE` y la vista de redacción queda desactivada. El cartucho degrada con elegancia en lugar de hacer caer el chasis.

## Véase también

- [[service-email]] — el servicio de correo que gestiona el enrutamiento, la cola y la salida
- [[console-os]] — descripción general del producto os-console y la superficie de teclas de función
- [[os-console-platform]] — arquitectura de cartuchos y el mapa completo de teclas de función
- [[app-console-keys]] — el chasis que aloja este cartucho; define el rasgo Cartridge
- [[app-console-input]] — la puerta obligatoria F12 para la ingesta de archivos entrantes
- [[machine-based-auth]] — la capa de autorización a través de la que se conecta el cartucho
