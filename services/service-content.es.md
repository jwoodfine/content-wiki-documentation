---
schema: foundry-doc-v1
title: "service-content — El Motor de Gravedad"
slug: service-content
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-content.md
short_description: "service-content es el motor de síntesis de la familia PointSav — el Motor de Gravedad que lee cargas útiles en bruto de un Totebox, las procesa contra una taxonomía institucional y genera los documentos estructurados que publica una organización."
cites: []
references:
  - id: 1
    text: "Aho, A. V. & Corasick, M. J. 'Efficient String Matching: An Aid to Bibliographic Search.' Communications of the ACM, 18(6):333–340, 1975."
    url: "https://dl.acm.org/doi/10.1145/360825.360855"
  - id: 2
    text: "OIT. 'CIUO-08: Clasificación Internacional Uniforme de Ocupaciones.' Organización Internacional del Trabajo, 2012."
    url: "https://www.ilo.org/public/english/bureau/stat/isco/isco08/"
---

`service-content` es el motor de síntesis de la familia PointSav. Lee cargas útiles en bruto desde el interior de un Totebox, las procesa contra una taxonomía institucional, produce densos Vectores de Gravedad y, en última instancia, genera los documentos que publica una organización — wikis, comunicados de prensa, libros mayores de debida diligencia, memorandos internos. Es la diferencia entre un almacén de archivos y un motor de inteligencia activo. Este artículo cubre la Bóveda de Semillas de Cuatro Pilares, el pipeline del Motor de Gravedad, la Ontología Estratificada y el límite de intervención humana que rige lo que el motor puede escribir de forma autónoma.

## La Bóveda de Semillas de Cuatro Pilares

Cada Totebox se aprovisiona con cuatro libros mayores JSON que forman la gramática institucional del sistema — la Bóveda de Semillas. La Bóveda de Semillas se construye una vez, se bloquea y solo la ajustan los operadores, no la IA:

| Pilar | Qué captura | Ejemplo |
|---|---|---|
| Entidades | El "quién" — cada individuo, organización, correo electrónico y número de teléfono extraídos de las cargas útiles | Un Sovereign-ID asociado al hash de correo de un contacto específico |
| Arquetipos | El "logos" — once personas funcionales (Ejecutivo, Guardián, Fiduciario, Arquitecto, Ingeniero, Artesano, Constructor, Catalizador, Embajador, Administrador, Sabio) | Un consultor de fachadas se mapea a "El Ingeniero" |
| Plan de Cuentas | El "dónde" — la estructura jerárquica rígida de la organización (Perfil → Dominio → Sub-Dominio) | Construcción → Colaboradores → Consultores de Fachadas |
| Dominios | El "qué" — el vocabulario localizado y los términos del glosario en uso | "Solución de Tenencia Directa" |

Un quinto pilar, Temas, captura las corrientes multidimensionales que emergen del corpus — temas recurrentes y preocupaciones institucionales que se señalan y proponen a los operadores para su aprobación.

## El pipeline del Motor de Gravedad

Cuando llega una carga útil (un correo electrónico, un PDF, un DOCX), el motor realiza una secuencia determinista ajustada:

1. **Ingesta.** `service-email` (o la [[app-console-input|Máquina de Entrada]]) escribe la carga útil en bruto en la bóveda WORM del Totebox. Nada se muta todavía.
2. **Extracción de entidades.** `service-extraction` ejecuta Aho-Corasick sobre el texto en bruto y extrae cada nombre, correo electrónico, número de teléfono y organización. [^1] Cada uno recibe un Sovereign-ID determinista y comienza en estado `Discovery`.
3. **Cálculo de gravedad.** `service-content` carga los cuatro pilares, los fusiona en un único autómata de búsqueda y extrae solo las oraciones que contienen palabras clave estructurales. Una carga útil de 5 MB se convierte en un Vector de Gravedad de 50 palabras.
4. **Verificación.** El vector y el paquete de entidades pasan a `service-slm`, que evalúa si la carga útil se alinea con la taxonomía de la institución. La salida es un único token — `VALID` o `REJECT`.
5. **Enrutamiento.** Las cargas útiles verificadas van al almacenamiento profundo; las rechazadas van a cuarentena. Las entidades verificadas tienen su estado `Discovery` actualizado y son conectadas al Plan de Cuentas.

## La Ontología Estratificada

`service-content` organiza la información en una pila de cinco capas, con tres motores derivados encima:

| Capa | Qué contiene |
|---|---|
| L0 — Geometría Base | Archivos en bruto (`/source`, `/assets`, `/ledger`) — inmutables, locales |
| L1/L2 — Grafo en Bruto | Extracción ciega al 100% en un grafo de conocimiento JSONL |
| L3 — Anclas Globales | Estándares universales (IFRS/GAAP para finanzas, O*NET/ISCO para personal) [^2] |
| L4 — Taxonomía Soberana | La realidad operativa propia de la institución — Dominios, Glosarios, Temas |
| L5 — Corteza de Verificación | El libro mayor de verdad con intervención humana; solo salidas de contenido verificado por el operador |

| Derivado | Qué produce |
|---|---|
| D1 — Cuantificación Temática | Previsión: monitorea la entrada al grafo y señala temas emergentes para revisión del operador |
| D2 — Protocolos Lingüísticos | Restricciones de comportamiento — protocolos TRANSLATE, MEMO, COMMS, TEXT, LEGAL |
| D3 — Creación de Contenido | Artefactos finales: wikis HTML, libros mayores PDF, comunicados de prensa — generados desde la verdad L5 |

## Auto-reparación

El Motor de Gravedad es auto-reparable en un sentido específico y limitado: sus propias salidas retroalimentan sus entradas. Un memorando sintetizado con éxito se convierte en contenido nuevo que el motor indexa la próxima vez que se ejecuta. Con el tiempo, los glosarios de Dominios crecen, los Temas rastrean preocupaciones institucionales reales y las síntesis del motor convergen en la voz real de la institución. Esto no es ajuste fino autónomo del modelo — la mejora es a nivel de corpus: el motor tiene más material verificado del que extraer.

## El límite de intervención humana

`service-content` no publica en libros mayores verificados de forma autónoma. Cada entrada L5 debe transitar un paso de verificación con intervención humana — ya sea a través de la [[app-console-input|Máquina de Entrada]] (F12) o a través de la superficie de revisión de contenido — antes de que pueda escribirse en un libro mayor verificado. Esto satisface [[sys-adr-07]] (sin datos estructurados a través de IA) y [[sys-adr-19]] (sin publicación automatizada de IA en libros mayores verificados).

## Véase también

- [[service-slm]] — el modelo de lenguaje pequeño local que produce las decisiones `VALID`/`REJECT`
- [[service-people]] — el libro mayor de identidades que recibe entidades conectadas del Motor de Gravedad
- [[archetypes-and-chart-of-accounts]] — la taxonomía institucional que forma la estructura de la Bóveda de Semillas
- [[app-console-input]] — la Máquina de Entrada F12; la superficie de ingesta con compuerta humana
- [[totebox-os]] — el Totebox que aloja service-content y su almacenamiento WORM
