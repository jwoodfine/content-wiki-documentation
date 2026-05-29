---
schema: foundry-doc-v1
title: "La Máquina de Entrada"
slug: input-machine
short_description: "La Máquina de Entrada es la puerta obligatoria de incorporación de documentos en os-console, asignada permanentemente a F12 y respaldada por service-input en el Archivo Totebox."
category: systems
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
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

El flujo de ingesta opera de la siguiente manera: un modal presenta el campo de ruta del archivo; el operador ingresa y confirma la ruta (no se acepta envío pasivo); la Máquina de Entrada valida que el archivo exista y sea legible; el archivo validado se envía a `service-input` en el Archivo Totebox; `service-input` clasifica el documento y determina el destino de enrutamiento; `service-input` enruta el documento al servicio apropiado; se escribe una entrada de auditoría inmutable con marca de tiempo, ruta del archivo, clasificación, destino y identidad del operador; finalmente el cartucho activo se reanuda con el documento incorporado disponible en su contexto.

## service-input: el servicio frontera del Anillo 1

`service-input` es un servicio del Anillo 1 en la [[three-ring-architecture|Arquitectura de Tres Anillos]] — un servicio frontera de ingesta de documentos por arrendatario que maneja la incorporación genérica de documentos. Es la contraparte del lado servidor del cartucho de la [[app-console-input|Máquina de Entrada]].

`service-input` realiza tres funciones: clasifica el tipo de documento y la canalización de procesamiento apropiada; enruta el documento al servicio correcto del Anillo 2 o Anillo 1; y escribe un registro inmutable del evento de ingesta en el [[worm-ledger-design|ledger]].

`service-input` no realiza inferencia de inteligencia artificial. La clasificación utiliza reglas deterministas conforme a SYS-ADR-07, lo que garantiza que el rastro de auditoría sea reproducible y no dependa de la disponibilidad del modelo.

## La pista de auditoría

Cada documento que pasa por la Máquina de Entrada genera dos entradas de auditoría: un registro local en SQLite en la máquina de os-console, y un registro canónico e inmutable en el ledger de `service-input` en el [[totebox-archive|Archivo Totebox]].

## La arquitectura sin formularios

La Máquina de Entrada es el fundamento de lo que la documentación operativa describe como la arquitectura sin formularios. Los flujos de trabajo tradicionales requieren que el operador rellene campos para contextualizar un documento antes de que ingrese al sistema. La Máquina de Entrada invierte esto: el operador proporciona un documento y el sistema lo clasifica, enruta y contextualiza automáticamente. La única entrada requerida es el documento en sí y una confirmación explícita de la intención de enviarlo.

## Véase también

- [[console-os]] — la plataforma de os-console
- [[machine-based-auth]] — el mecanismo de autorización de os-console
- [[three-ring-architecture]] — la arquitectura de tres anillos
- [[os-console-platform]] — la arquitectura de cartuchos y el mapa de teclas de función
- [[worm-ledger-design]] — la disciplina del ledger de solo adición para los registros de auditoría
