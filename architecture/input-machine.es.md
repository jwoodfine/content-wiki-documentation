---
schema: foundry-doc-v1
title: "La Máquina de Ingesta"
slug: input-machine
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: input-machine.md
short_description: "La Máquina de Ingesta es la frontera de entrada obligatoria para todos los documentos que ingresan a los flujos de trabajo de os-console, asignada permanentemente a F12 e implementada por service-input en el Totebox Archive — todo el material fuente pasa por esta única puerta auditable."
cites: []
references: []
---

Todo sistema de gestión documental debe responder una pregunta fundamental: cuando un documento llega a un flujo de trabajo, ¿cómo llegó allí? En la mayoría de los sistemas, la respuesta es distribuida e implícita — los archivos aparecen en carpetas, se adjuntan a correos electrónicos, se cargan a través de formularios web, y el sistema reconstruye la cadena de ingesta a posteriori cuando el cumplimiento normativo lo exige.

La Máquina de Ingesta invierte este diseño. Una única puerta de entrada fija maneja toda la ingesta de documentos. Cada documento que entra en un flujo de trabajo de os-console pasa por ella. Cada paso queda registrado. La pregunta de cómo un documento entró al sistema tiene una sola respuesta: a través de F12, en un momento específico, con una confirmación explícita del operador.

## El Ancla: F12 como puerta de ingesta obligatoria

F12 está asignada permanentemente a la Máquina de Ingesta en os-console. Esta asignación es arquitectónica, no de configuración — no puede ser modificada por el operador ni anulada por otro cartucho. F12 ocupa la posición límite en la fila de teclas de función del teclado, físicamente separada de F1 a F11 por un espacio más amplio en la mayoría de los teclados. La posición es intencional: la puerta de ingesta debe ser localizable de forma inmediata e inequívoca en cualquier estado del flujo de trabajo, por cualquier operador, en cualquier momento.

La restricción de que F12 es inamovible queda registrada en [[sys-adr-10]]. Ningún flujo de trabajo puede eludir la Máquina de Ingesta para enviar un documento a un servicio de backend por otra ruta. Esta restricción se aplica en el despachador de eventos de `app-console-keys` a nivel del chasis, no por convención en cartuchos individuales.

## El flujo de ingesta

Presionar F12 en cualquier contexto de os-console — independientemente del cartucho activo en ese momento — activa el modal de la Máquina de Ingesta. El cartucho activo se suspende. El operador completa el flujo de ingesta:

1. Se abre el campo de entrada de ruta de archivo.
2. El operador proporciona la ruta y confirma explícitamente — no se acepta la presentación pasiva o accidental.
3. La Máquina de Ingesta valida que el archivo existe y es legible.
4. El archivo validado se transmite a `service-input` en el Totebox Archive.
5. `service-input` clasifica el documento mediante reglas deterministas, sin inferencia de IA.
6. `service-input` enruta el documento al servicio de backend apropiado.
7. Se escribe una entrada de auditoría inmutable: marca de tiempo, ruta de archivo, resultado de clasificación, destino de enrutamiento, identidad del operador.
8. El cartucho anteriormente activo se reanuda, con el documento ingestado disponible en su contexto.

El paso 5 aplica la restricción de [[sys-adr-07]]: ningún dato estructurado pasa por inferencia de IA en la frontera de ingesta. La clasificación es determinista — la extensión del archivo, el tipo MIME y las firmas estructurales determinan el tipo de documento. El resultado de clasificación en el registro de auditoría es reproducible: dado el mismo archivo, `service-input` produce la misma clasificación independientemente de la disponibilidad del modelo.

## La arquitectura Cero-Formulario

La Máquina de Ingesta implementa un principio de diseño llamado arquitectura Cero-Formulario. En los flujos de trabajo convencionales, los documentos ingresan a los sistemas a través de formularios: el operador completa campos de metadatos para contextualizar un documento antes de que entre en un proceso de procesamiento. El Cero-Formulario invierte esto. El operador proporciona un documento. El sistema lo clasifica, determina el destino de procesamiento y genera los metadatos contextualizadores automáticamente. El único aporte manual requerido es el documento en sí y una confirmación explícita de la intención de enviarlo.

Esto no es una función de conveniencia. El valor arquitectónico es la precisión en el cumplimiento normativo: el registro de auditoría refleja una decisión humana deliberada para cada documento. Ningún documento entra en un flujo de trabajo por hábito, automatización o accidente. La confirmación explícita del operador es el evento que registra el registro de auditoría.

## service-input: el servicio de ingesta en la frontera

`service-input` es la contraparte del servidor de la Máquina de Ingesta en el Totebox Archive. Es un servicio de ingesta en la frontera — un proceso distinto, por tenant, que maneja toda la ingesta de documentos para un archivo. Cada Totebox Archive ejecuta su propia instancia de `service-input`; no existe un servicio de ingesta compartido entre archivos.

`service-input` realiza tres funciones:

**Clasificación.** Identificación determinista del tipo de documento mediante extensión de archivo, tipo MIME y firmas estructurales. Sin inferencia de IA en esta etapa — la regla de clasificación está codificada en el servicio, no delegada a un modelo de lenguaje.

**Enrutamiento.** Despacho al servicio de backend apropiado según la clasificación: contenido editorial al servicio de corrección, material de archivo a `service-fs`, documentos de gobernanza al flujo de gobernanza. La decisión de enrutamiento pertenece a `service-input`; el operador no especifica el destino.

**Auditoría.** Una entrada de registro inmutable escrita en el momento de la ingesta, capturando el contexto completo del evento: qué se envió, cuándo, cómo se clasificó y hacia dónde se enrutó.

## El rastro de auditoría

Cada documento que pasa por la Máquina de Ingesta produce dos entradas de registro. Un registro local en la máquina del operador captura el evento de ingesta inmediatamente, persistiendo incluso si el Totebox Archive está temporalmente inaccesible. El libro mayor de `service-input` en el archivo es el registro canónico, escrito una vez que se completa la transmisión.

El registro dual es una propiedad de resiliencia: si ocurre una interrupción de red durante la ingesta, el registro local conserva evidencia del intento; el libro mayor canónico confirma la entrega.

## Enrutamiento por cartucho

Cada cartucho utiliza la Máquina de Ingesta para su material fuente, pero la decisión de enrutamiento pertenece a `service-input`, no al cartucho activo. Un operador en el cartucho editorial F4 y un operador en el cartucho de información de edificios F7 ambos presionan F12 para enviar material. `service-input` enruta al servicio de corrección o al servicio BIM según lo que se envió — no según qué cartucho estaba activo cuando se presionó F12. La Máquina de Ingesta es una puerta compartida; la clasificación determina el destino.

## Véase también

- [[os-console-platform]] — el contexto de plataforma y la arquitectura de cartuchos en los que opera la Máquina de Ingesta
- [[machine-based-auth]] — el mecanismo de autorización que conecta os-console con service-input en el Totebox Archive
- [[sys-adr-10]] — el registro de decisión arquitectónica que establece F12 como el punto de control de ingesta obligatorio
- [[sys-adr-07]] — el registro de decisión arquitectónica que prohíbe la inferencia de IA en datos estructurados en la frontera de ingesta
