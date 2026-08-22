---
schema: foundry-doc-v1
title: "service-content"
slug: service-content
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-content.md
short_description: "service-content extrae entidades nombradas de cargas útiles en bruto mediante una canalización de modelos escalonada, las escribe en el grafo de conocimiento bajo un punto de control de revisión humana, y aloja las taxonomías de referencia de la plataforma."
cites: []
references:
  - id: 1
    text: "OIT. 'CIUO-08: Clasificación Internacional Uniforme de Ocupaciones.' Organización Internacional del Trabajo, 2012."
    url: "https://www.ilo.org/public/english/bureau/stat/isco/isco08/"
---

Los archivos de una organización contienen su conocimiento pero no lo hacen aflorar. Un archivo de correo, una carpeta de contratos, un almacén de PDF — cada uno es consultable, y ninguno sabe quién se relaciona con quién ni qué significan los términos propios de la organización. `service-content` es el servicio de extracción de entidades y escritura al grafo de conocimiento de la plataforma: convierte cargas útiles de documentos en bruto en entidades nombradas y relaciones, y aloja las taxonomías de referencia contra las que se clasifican esas entidades.

## La extracción pasa por tres niveles, del más económico al más costoso

Cuando llega una carga útil, `service-content` intenta primero el método de extracción más rápido y solo escala cuando es necesario:

1. **Nivel 0 — GLiNER.** Una llamada HTTP directa a un modelo GLiNER local (puerto 9085), sin pasar por el enrutador de solicitudes de IA (el Doorman). La mayoría de los documentos se procesan aquí.
2. **Respaldo de Nivel A — OLMo, vía el Doorman.** Se activa cuando GLiNER no responde, cuando GLiNER no encuentra nada (para detectar sus puntos ciegos), o cuando la carga útil es un CSV estructurado que el modelo de lenguaje natural de GLiNER no puede analizar. Cada pasada del Nivel 0 también encola una ejecución asíncrona del Nivel A en segundo plano. Los dos resultados forman un par de entrenamiento — la salida extractiva de GLiNER como respuesta preferida, la de OLMo como comparación — usado para seguir mejorando la calidad de extracción del Nivel A con el tiempo. Este es el verdadero mecanismo de automejora de esta canalización: un mecanismo concreto de datos de entrenamiento, no un glosario que crece orgánicamente.
3. **Nivel B — OLMo 32B, vía el endpoint `/v1/extract` del Doorman.** El nivel más pesado, usado cuando los niveles más rápidos no están disponibles o resultan insuficientes.

Un control de contrapresión contra la profundidad de la cola del Doorman puede aplazar un documento en lugar de acumularse sobre una canalización ya cargada.

## Toda escritura automática al grafo se retiene para un veredicto humano

`service-content` nunca escribe entidades extraídas directamente en el grafo de conocimiento. Toda escritura — de cualquiera de los dos niveles — pasa por el mismo punto de control. Primero captura la escritura, y solo la promueve tras la aprobación de un humano:

1. **Captura.** La escritura se registra en un archivo JSONL duradero en disco, en lugar de tocar el grafo. Sobrevive a un reinicio del proceso, y un humano puede revisar la cola completa pendiente en cualquier momento.
2. **Verificación.** Un revisor envía un veredicto firmado con SSH. La firma se verifica contra el archivo `allowed_signers` del espacio de trabajo, bajo un espacio de nombres dedicado, de modo que una firma de veredicto de este sistema nunca pueda reutilizarse contra uno no relacionado.
3. **Promoción al aceptar.** Solo después de firmarse un veredicto, la escritura llega realmente al grafo.
4. **Descarte al rechazar.** El registro pendiente se conserva — nunca se elimina — con el veredicto de rechazo adjunto, para auditoría.

Esto satisface directamente los compromisos SYS-ADR-07 (sin datos estructurados a través de IA) y SYS-ADR-19 (sin publicación automática de IA en libros verificados) de la plataforma: la canalización de extracción puede ejecutarse sin supervisión continua, pero nada de lo que produce pasa a formar parte del grafo de registro sin una decisión humana explícita y firmada.

## Las taxonomías de referencia que aloja

Por separado de la extracción, `service-content` posee un conjunto de archivos CSV de taxonomía — el [[archetypes-and-chart-of-accounts|Plan de Cuentas y los once arquetipos]] entre ellos, además de vocabularios de dominio, glosarios e índices de temas y guías para cada wiki. Estos se cargan en el grafo como entidades de referencia estáticas mediante una pequeña API administrativa, distintas de las entidades que la canalización de extracción produce a partir de documentos reales.

## Véase también

- [[archetypes-and-chart-of-accounts]] — las dos taxonomías de referencia que `service-content` carga en el grafo de conocimiento
- [[verification-surveyor]] — donde un humano aplica la etiqueta de arquetipo que la taxonomía de `service-content` pone a disposición
- [[service-extraction]] — la capa de identidad determinista que reciben las entidades una vez extraídas
- [[app-console-input]] — la puerta F12 donde un operador revisa una escritura automática pendiente
- [[query-the-datagraph]] — guía paso a paso: buscar entidades nombradas, navegar relaciones y gestionar interrupciones del Nivel A
- [[export-structured-data]] — guía paso a paso: cuatro rutas de exportación, incluidas las consultas al DataGraph y Markdown de wiki
