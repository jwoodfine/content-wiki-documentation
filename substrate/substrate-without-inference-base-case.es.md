---
schema: foundry-doc-v1
title: "Substrato sin inferencia — El caso base"
slug: substrate-without-inference-base-case
category: substrate
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-customer-ownership
short_description: "El Archivo Totebox permanece completamente operativo y transferible libremente incluso cuando no hay ningún nivel de inferencia de IA disponible; el substrato determinístico es la base estructural."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Sigstore. 'Rekor: Software Supply Chain Transparency Log.' Sigstore.dev, 2024."
    url: "https://docs.sigstore.dev/logging/overview/"
paired_with: substrate-without-inference-base-case.md
---


El **Substrato sin Inferencia — El Caso Base** establece que el [[totebox-archive|Archivo Totebox]] debe permanecer completamente operativo y transferible libremente incluso cuando [[service-slm]] no puede ejecutar ninguna inferencia. La inferencia de IA es un valor añadido. El substrato determinístico — el registro de archivos, el [[knowledge-graph-grounded-apprenticeship|grafo de conocimiento]], el [[service-extraction|pipeline de extracción]] y los servicios editoriales — es la base estructural.

## Lo que requiere el caso base

Cuando los tres niveles de cómputo (especialista local, [[yoyo-compute-substrate|GPU en ráfaga]] y API externa) están simultáneamente no disponibles, todos los servicios determinísticos deben seguir siendo operativos: el registro de archivos WORM ([[service-fs|service-fs]]), el motor de conocimiento ([[service-content|`service-content`]]), el servicio de entrada, el [[service-extraction|servicio de extracción]] en su capa de análisis determinístico, el servicio de salida, y los servicios de personas, email y archivos. El [[compounding-doorman|Portero]] está vinculado y escuchando, devolviendo 503 a los endpoints de inferencia mientras mantiene los endpoints de salud y contrato siempre respondiendo. Las consultas y operaciones de la [[tui-corpus-producer|TUI]] del operador que no dependen de IA siguen funcionando; un modo "solo-determinístico" dedicado, con indicador visual propio, está previsto pero aún no construido como modo distinto.

Los [[reverse-flow-substrate|servicios de mercado y liquidación]] están previstos, no construidos todavía; cuando existan, el diseño prevé que se aplique la misma disciplina — las transacciones proceden sin fundamentación asistida por IA, con los registros de auditoría y consentimiento siempre aplicados.

## El flujo de transferencia de propiedad

La propiedad "transferible libremente" es el resultado comercial previsto por el diseño, no todavía un mecanismo entregado. Un único comando de exportación — que produciría un paquete autónomo y firmado criptográficamente con el instantáneo del grafo por inquilino, el [[worm-ledger-architecture|registro de auditoría]], los [[adapter-composition|pesos del adaptador]] entrenado, la [[seed-taxonomy-as-smb-bootstrap|taxonomía semilla]], el manifiesto del paquete y la configuración del inquilino — está previsto y aún no construido (véase [[customer-owned-graph-ip]]). Se prevé que el paquete sea firmado por la clave de identidad del operador con integridad anclada en un registro de transparencia público. [^1]

Una vez construido, se prevé que la parte receptora importe el paquete en un Totebox nuevo, con las operaciones determinísticas funcionando inmediatamente sobre el estado importado y las operaciones asistidas por IA disponibles cuando el nuevo operador configure un nivel de cómputo.

## Por qué esto importa comercialmente

La propiedad transferible libremente está prevista para distinguir un activo soberano de una suscripción a un servicio. Una vez construida la vía de exportación, el diseño prevé que, cuando se venda un negocio, el nuevo propietario importe el paquete del Totebox y tenga el historial operativo completo disponible inmediatamente — el grafo de conocimiento, el registro de auditoría y el vocabulario del flujo de trabajo — sin re-suscribirse a ninguna plataforma ni contratar consultores de migración.

El mismo mecanismo previsto cubre la disolución o división de un negocio (cada parte recibiendo su porción del grafo como un artefacto portátil firmado) y una adquisición corporativa (historial operativo con procedencia verificable disponible de inmediato para la parte adquirente).

Si la plataforma cesa sus operaciones, el cliente continúa operando su Totebox indefinidamente. El substrato determinístico funciona sin la plataforma. El cliente pierde la capacidad de recibir nuevos paquetes verticales y de transaccionar en el mercado de la plataforma, pero sus operaciones existentes no se detienen.

## Requisito de implementación

El caso base restringe cada implementación de servicio. Cada servicio debe tener una base determinística que funcione sin IA. Las operaciones mejoradas por IA se documentan como que requieren el nivel de IA y se degradan elegantemente cuando no está disponible. La regresión en la base determinística — cualquier servicio que falla cuando todos los niveles están inactivos — es una señal a nivel doctrinal de que una función de soporte de carga ha sido hecha dependiente de la IA.

## Véase También

- [[tier-zero-customer-side-sovereign-specialist]] — el despliegue del Nivel 0 que este caso base garantiza
- [[customer-owned-graph-ip]] — el derecho de propiedad que el flujo de transferencia ejercita
- [[single-boundary-compute-discipline]] — el comportamiento del Portero en el caso base (503 desde los endpoints de inferencia; los endpoints de salud siempre responden)
