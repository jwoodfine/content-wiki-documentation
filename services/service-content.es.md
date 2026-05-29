---
schema: foundry-doc-v1
title: "Motor de gravedad"
slug: service-content
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: service-content.md
short_description: "service-content es el motor de síntesis de la familia PointSav — el Motor de Gravedad que lee cargas útiles en bruto de un Totebox, las procesa contra una taxonomía institucional y genera los documentos estructurados que publica una organización, con un límite de intervención humana en cada libro mayor verificado."
cites: []
references:
 - id: 1
 text: "Aho, A. V. & Corasick, M. J. 'Efficient String Matching: An Aid to Bibliographic Search.' Communications of the ACM, 18(6):333–340, 1975."
 url: "https://dl.acm.org/doi/10.1145/360825.360855"
 - id: 2
 text: "OIT. 'CIUO-08: Clasificación Internacional Uniforme de Ocupaciones.' Organización Internacional del Trabajo, 2012."
 url: "https://www.ilo.org/public/english/bureau/stat/isco/isco08/"
---

Los archivos de una organización contienen su conocimiento pero no lo hacen aflorar. Un archivo de correo, una carpeta de contratos, un almacén de PDF — cada uno es consultable, y ninguno sabe quién se relaciona con quién, qué preocupaciones se repiten ni qué significan los términos propios de la organización.

<!--claim id=gravity-engine confidence=structural cites=[]-->`service-content` — el Motor de Gravedad — es el motor de síntesis de la familia PointSav. Lee cargas útiles en bruto desde el interior de un Totebox, las procesa contra una taxonomía institucional, produce densos Vectores de Gravedad y genera los documentos que publica una organización: wikis, comunicados de prensa, libros mayores de debida diligencia, memorandos internos.<!--/claim-->

El motor se construye sobre una Bóveda de Semillas de Cuatro Pilares — la gramática institucional — un pipeline determinista de ingesta a enrutamiento, y una Ontología Estratificada de cinco capas. Es la diferencia entre un almacén de archivos y un motor de inteligencia activo. El [[archetypes-and-chart-of-accounts|Plan de Cuentas y los once arquetipos]] forman dos de los cuatro pilares de la Bóveda de Semillas.

Para un comprador regulado, un solo límite gobierna todo. <!--claim id=human-loop-boundary confidence=structural cites=[]-->`service-content` no publica en un libro mayor verificado de forma autónoma; cada entrada verificada transita primero un paso de verificación con intervención humana.<!--/claim--> Este artículo cubre la Bóveda de Semillas, el pipeline del Motor de Gravedad, la Ontología Estratificada y ese límite.

## La Bóveda de Semillas de Cuatro Pilares

<!--claim id=seed-vault confidence=structural cites=[]-->Cada Totebox se aprovisiona con cuatro libros mayores JSON que forman la gramática institucional del sistema — la Bóveda de Semillas. La Bóveda de Semillas se construye una vez, se bloquea y solo la ajustan los operadores, nunca la IA.<!--/claim-->

| Pilar | Qué captura | Ejemplo |
|---|---|---|
| Entidades | El "quién" — cada individuo, organización, correo y teléfono extraídos de las cargas útiles | Un Sovereign-ID asociado al hash de correo de un contacto |
| Arquetipos | El "logos" — once personas funcionales (Ejecutivo, Guardián, Fiduciario, Arquitecto, Ingeniero, Artesano, Constructor, Catalizador, Embajador, Administrador, Sabio) | Un consultor de fachadas se mapea a "El Ingeniero" |
| Plan de Cuentas | El "dónde" — la estructura jerárquica rígida de la organización (Perfil → Dominio → Sub-Dominio) | Construcción → Colaboradores → Consultores de Fachadas |
| Dominios | El "qué" — el vocabulario localizado y los términos del glosario en uso | "Solución de Tenencia Directa" |

Un quinto pilar, Temas, captura los temas recurrentes y las preocupaciones institucionales que emergen del corpus — señalados y propuestos a los operadores para su aprobación.

## El pipeline del Motor de Gravedad

Cuando llega una carga útil — un correo, un PDF, un DOCX — el motor ejecuta una secuencia determinista ajustada.

1. **Ingesta.** `service-email`, o la [[app-console-input|Máquina de Entrada]], escribe la carga útil en bruto en la bóveda WORM del Totebox. Nada se muta todavía.
2. **Extracción de entidades.** `service-extraction` ejecuta la concordancia de cadenas Aho-Corasick [^1] sobre el texto en bruto y extrae cada nombre, correo, teléfono y organización. Cada uno recibe un Sovereign-ID determinista y comienza en estado `Discovery`.
3. **Cálculo de gravedad.** `service-content` carga los cuatro pilares, los fusiona en un único autómata de búsqueda y extrae solo las oraciones con palabras clave estructurales. <!--claim id=gravity-vector confidence=structural cites=[]-->Una carga útil de 5 MB se convierte en un Vector de Gravedad de 50 palabras.<!--/claim-->
4. **Verificación.** El vector y el paquete de entidades pasan a `service-slm`, que evalúa si la carga útil se alinea con la taxonomía de la institución. La salida es un único token — `VALID` o `REJECT`.
5. **Enrutamiento.** Las cargas verificadas van al almacenamiento profundo; las rechazadas van a cuarentena. Las entidades verificadas tienen su estado `Discovery` actualizado y se conectan al Plan de Cuentas.

## La Ontología Estratificada

`service-content` organiza la información en una pila de cinco capas, con tres motores derivados encima. La capa base L0 alimenta directamente la [[service-fs-architecture|arquitectura del libro mayor WORM]] proporcionada por `service-fs`.

| Capa | Qué contiene |
|---|---|
| L0 — Geometría Base | Archivos en bruto (`/source`, `/assets`, `/ledger`) — inmutables, locales |
| L1/L2 — Grafo en Bruto | Extracción ciega completa en un grafo de conocimiento JSONL |
| L3 — Anclas Globales | Estándares universales (IFRS/GAAP para finanzas, O*NET/ISCO para personal) [^2] |
| L4 — Taxonomía Soberana | La realidad operativa propia de la institución — Dominios, Glosarios, Temas |
| L5 — Corteza de Verificación | El libro mayor de verdad con intervención humana; solo salidas verificadas por el operador |

| Derivado | Qué produce |
|---|---|
| D1 — Cuantificación Temática | Previsión: monitorea la entrada al grafo y señala temas emergentes para revisión del operador |
| D2 — Protocolos Lingüísticos | Restricciones de comportamiento — protocolos TRANSLATE, MEMO, COMMS, TEXT, LEGAL |
| D3 — Creación de Contenido | Artefactos finales: wikis HTML, libros mayores PDF, comunicados de prensa — generados desde la verdad L5 |

## Auto-reparación

El Motor de Gravedad es auto-reparable en un sentido específico y limitado: sus propias salidas retroalimentan sus entradas. Un memorando sintetizado con éxito se convierte en contenido nuevo que el motor indexa en su siguiente ejecución. Con el tiempo, los glosarios de Dominios crecen, los Temas rastrean preocupaciones institucionales reales y las síntesis del motor convergen en la voz real de la institución. Esto no es ajuste fino autónomo del modelo — la mejora es a nivel de corpus: el motor tiene más material verificado del que extraer. El patrón del [[compounding-substrate|sustrato de composición]] describe la lógica arquitectónica detrás de este ciclo de retroalimentación.

## El límite de intervención humana

<!--claim id=adr-compliance confidence=structural cites=[]-->Cada entrada L5 debe transitar un paso de verificación con intervención humana — a través de la [[app-console-input|Máquina de Entrada]] (F12) o la superficie de revisión de contenido — antes de poder escribirse en un libro mayor verificado. Esto satisface SYS-ADR-07 (sin datos estructurados a través de IA) y SYS-ADR-19 (sin publicación automatizada de IA en libros mayores verificados).<!--/claim-->

El límite es lo que hace al motor utilizable en un entorno regulado. El motor acelera la síntesis; un humano, no el motor, confirma el resultado en un libro mayor de registro.

## Véase también

- [[service-slm]] — el modelo de lenguaje pequeño local que produce las decisiones `VALID`/`REJECT`
- [[service-people]] — el libro mayor de identidades que recibe entidades conectadas del Motor de Gravedad
- [[archetypes-and-chart-of-accounts]] — la taxonomía institucional que forma la estructura de la Bóveda de Semillas
- [[app-console-input]] — la Máquina de Entrada F12; la superficie de ingesta con compuerta humana
- [[totebox-os]] — el Totebox que aloja service-content y su almacenamiento WORM
