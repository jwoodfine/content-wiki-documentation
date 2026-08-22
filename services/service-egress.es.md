---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-egress
short_description: "service-egress comprime y fragmenta datos de correo locales para transferencia saliente, y solo elimina la fuente local una vez que una contraparte externa confirma la recepción con una prueba criptográfica — una válvula de liberación saliente, no una importación de la nube a local."
title: "Servicio de egreso"
category: services
index_group: ring-2-knowledge-and-processing
language: es
paired_with: service-egress.md
status: stub
last_edited: 2026-08-22
editor: pointsav-engineering
---

`service-egress` mueve datos de correo locales hacia afuera — lo contrario de lo que su nombre podría sugerir a primera vista. No trae nada desde la nube; prepara datos locales para transferencia saliente y solo elimina la copia local una vez que tiene la prueba de que la transferencia tuvo éxito.

## El ciclo

Ejecutándose continuamente, el servicio repite dos pasos:

1. **Preparar.** Cualquier archivo de correo local aún no preparado se comprime y divide en fragmentos de tamaño fijo dentro de una cola de salida, listos para que un proceso externo homólogo los recoja.
2. **Eliminar al recibir confirmación.** Cuando ese proceso externo confirma que ha recibido una transferencia — un recibo criptográfico, no un simple acuse de recibo — `service-egress` elimina tanto el archivo local original como sus fragmentos preparados. Nada se elimina hasta que existe ese recibo.

## Por qué importa el orden

Este orden hace que la pérdida de datos durante una transferencia sea imposible del lado de este servicio: el original local permanece en su lugar durante la preparación y la transferencia, y desaparece solo después de la confirmación independiente de que la copia saliente llegó. Un fallo a mitad de la transferencia simplemente deja tanto el original local como sus fragmentos preparados presentes para que el siguiente ciclo los retome.

Este servicio no tiene cliente IMAP ni de almacenamiento de objetos, y nunca llama a la interfaz del [[worm-ledger-design|libro mayor WORM]] — las garantías de solo adición del libro mayor WORM son reales en otra parte de la plataforma, simplemente no forman parte de este servicio en particular.

## Véase también

- [[service-email]] — el servicio de ingesta de correo cuyo Maildir local este servicio prepara para transferencia saliente
