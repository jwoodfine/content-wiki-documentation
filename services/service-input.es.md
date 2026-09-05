---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-input
title: "service-input — migración de archivo de referencia y calibración"
short_description: "service-input migra por lotes material de referencia en markdown desde un archivo fuente hacia la canalización de ingesta de la plataforma, deduplicando por hash de contenido y validando contra el registro de libro mayor propio de cada archivo — con una herramienta complementaria que puntúa qué tan bien coincide la extracción posterior con ese libro mayor."
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
paired_with: service-input.md
category: services
index_group: ring-1-boundary-ingest
status: active
quality: complete
last_edited: 2026-09-05
editor: pointsav-engineering
---

`service-input` es el backend detrás de una tarea específica y nombrada: migrar el material en markdown de un archivo de referencia hacia la plataforma en lotes controlados, y evaluar qué tan bien la extracción propia de la plataforma coincide después con lo que el libro mayor de ese archivo ya decía sobre cada archivo. No es un analizador de documentos multi-formato de propósito general — su propia descripción de paquete lo llama "ingesta de archivos, migración por lotes y evaluación de calibración."

## Qué hace

**Ingesta de archivo único.** `POST /v1/append` lee un archivo del disco, lo aplica hash con SHA-256, y lo omite si ese hash ya se procesó en esta ejecución — una compuerta de deduplicación simple y directa antes de reenviar nada.

**Migración por lotes.** `POST /v1/migrate` recorre los activos en markdown de un archivo de referencia fuente en cortes ordenados por desplazamiento y tamaño de lote (con un tope de 50 archivos por llamada), verificando cada archivo contra un registro de libro mayor en YAML antes de incluirlo. Existen dos modos de entrega: la ruta predeterminada enruta los archivos hacia adelante a través de la cadena de ingesta normal de la plataforma, mientras que un modo directo opcional — cuando hay configurado un directorio de emisión de corpus — escribe un archivo puente `CORPUS_<stem>.json` directamente a un directorio que vigila [[service-content]], el mismo patrón de puente que usa [[service-extraction]]. En modo directo, la validación del libro mayor se relaja y se incluye todo archivo markdown del lote, no solo los que coinciden con el libro mayor.

**Evaluación de calibración.** `GET /v1/eval/:stem` y `GET /v1/calibration-report` comparan lo que la extracción realmente produjo para un archivo dado contra una forma canónica y normalizada de la entrada del libro mayor de referencia propio de ese archivo — entidades, métricas y temas — para medir qué tan de cerca la extracción automatizada sigue un registro ya conocido como correcto.

## Configuración

El servicio lee su alcance de inquilino desde `SERVICE_INPUT_MODULE_ID` (con `jennifer` como valor predeterminado), y el resto de su configuración — la ruta raíz del archivo de referencia fuente, el archivo de destino, los límites de tasa de solicitudes y tamaño de lote, y los endpoints posteriores de `service-fs`/contenido a los que reenvía — se establece al inicio en lugar de negociarse por solicitud.

## Véase también

- [[service-content]] — uno de los dos consumidores de la salida de este servicio, ya sea vía la cadena de ingesta normal o el puente CORPUS directo
- [[service-extraction]] — usa el mismo patrón de entrega por puente CORPUS para su propia salida
- [[service-fs]] — el libro mayor en el que escribe la ruta de entrega normal (no directa) de este servicio
