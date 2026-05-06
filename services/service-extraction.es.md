---
schema: foundry-doc-v1
title: "service-extraction — Analizador Determinista"
slug: service-extraction
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-extraction.md
cites: []
## Véase también

- [[service-email]]
- [[service-people]]
- [[service-slm]]
- [[service-search]]

---

`service-extraction` es el controlador de tráfico central del Anillo 2 que elimina el formato propietario de las cargas útiles en bruto, construye Paquetes de Entidades estructurados, asigna IDs de transacción, y enruta los datos a servicios deterministas o a `service-slm` para extracción asistida por IA.

## Línea de base arquitectónica

Cada mensaje que pasa a través del Anillo 1 llega a `service-extraction` como una carga útil sin procesar con formato del proveedor. El servicio tiene una responsabilidad: transformar esa carga útil en un Paquete de Entidades limpio y trazable, y enrutarlo al servicio descendente correcto. Asigna un ID de transacción a cada paquete, proporcionando una referencia de cadena de custodia que persiste a través de cada paso de procesamiento posterior.

## Anillo y función

`service-extraction` ocupa el **Anillo 2 — Conocimiento y Procesamiento** en la arquitectura de tres anillos. El Anillo 2 es multiinquilino (a través del espacio de nombres `moduleId`) y determinista: procesa datos sin invocar inferencia de IA a menos que la forma de los datos lo requiera. Cuando una carga útil contiene texto no estructurado que no puede clasificarse por reglas deterministas, `service-extraction` enruta ese texto al Anillo 3 (`service-slm`) para extracción asistida por IA.

## El Paquete de Entidades

Cada carga útil se aísla en un directorio Unix nombrado por su marca de tiempo e ID de enrutamiento. El paquete contiene `payload.txt` — el registro legible permanente — más adjuntos binarios almacenados de forma nativa junto al texto.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
