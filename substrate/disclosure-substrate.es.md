---
schema: foundry-doc-v1
content_type: topic
title: "El sustrato de divulgación"
slug: disclosure-substrate
short_description: "El mecanismo que convierte una wiki Markdown con control de versiones en el registro de divulgación continua principal — cadenas de autoría criptográfica, hashes de contenido y adaptadores de exportación por jurisdicción planificados que producen salidas conformes a reguladores desde una única fuente mantenida en la propia infraestructura del emisor."
lang: es
language_protocol: TRANSLATE-ES
paired_with: disclosure-substrate.md
category: substrate
type: topic
status: active
last_edited: 2026-06-20
editor: pointsav-engineering
audience: vendor-public
bcsc_class: public-disclosure-safe
cites:
 - ni-51-102
 - osc-sn-51-721
 - bcsc-continuous-disclosure
 - sec-17a-4-f
 - eidas-qualified-preservation
 - ixbrl-esef
 - esap-eu-2027
 - opentimestamps
 - rfc-3161
 - sigstore-rekor-v2
 - cloud-act-us
 - w3c-verifiable-credentials
---

Una wiki de documentación puede diseñarse de modo que no sea una descripción de las divulgaciones de una empresa — sino el registro de divulgación en sí mismo. Cada artículo comprometido lleva una cadena de autoría firmada, un hash criptográfico de contenido y una marca de tiempo anclada a un [[worm-ledger-architecture|libro]] externo. Los reguladores y analistas leen el mismo corpus que escriben los colaboradores internos. La presentación regulatoria y el documento de trabajo son el mismo artefacto.

La consecuencia práctica para los compradores regulados: un emisor de reportes que sirva su wiki de divulgación desde infraestructura propia y firmada puede atender una solicitud de registros de un regulador sin coordinarse con una plataforma de terceros, sin depender de la continuidad operativa de un proveedor, y sin riesgo de que el registro de divulgación y la documentación interna hayan divergido — porque son el mismo archivo.

El sustrato colapsa tres cuerpos de texto convencionalmente separados — documentación interna, un sitio de relaciones con inversores y presentaciones regulatorias periódicas — en un único corpus Markdown bajo infraestructura del emisor, que se renderiza en páginas wiki orientadas al lector, paquetes de exportación conformes a reguladores y artefactos de prueba de estado criptográficos, todo desde la misma fuente.

Para los emisores regulados bajo `[ni-51-102]` y `[osc-sn-51-721]`, los adaptadores de exportación y el anclaje criptográfico descritos en este artículo son infraestructura planificada; la cadena de autoría firmada y el anclaje por hash de contenido son operativos en la actualidad.

## Descripción general

El Sustrato de Divulgación es un motor wiki, un corpus Markdown con control de versiones y un conjunto de adaptadores criptográficos y de exportación diseñados conjuntamente para que la wiki sea el registro de divulgación continua principal — no un complemento de una presentación regulatoria, y no un espejo de una plataforma de relaciones con inversores mantenida por separado.

Bajo `[ni-51-102]` (NI 51-102 Obligaciones de Divulgación Continua), un emisor de reportes debe mantener a los inversores y al público continuamente informados sobre cambios materiales, información prospectiva e informes anuales e intermedios. La implementación convencional separa esto en tres cuerpos de texto en tres pilas de proveedores: documentación interna, un sitio de relaciones con inversores y presentaciones regulatorias en SEDAR+ o EDGAR. Esos tres cuerpos se redactan por separado, suelen ser inconsistentes y son difíciles de auditar conjuntamente.

El sustrato colapsa los tres en uno: un único corpus Markdown bajo infraestructura del emisor, renderizado en páginas wiki orientadas al lector, paquetes de exportación conformes a reguladores y artefactos de prueba de estado criptográficos — todo desde la misma fuente.

## Anillo y función

El Sustrato de Divulgación abarca los tres anillos y la capa de documentación. El Anillo 1 proporciona el flujo de contenido entrante (artículos redactados y comprometidos por los colaboradores). El Anillo 2 proporciona la capa de búsqueda y grafo de conocimiento que indexa el corpus. El Anillo 3 proporciona la capa de fundamentación por IA (planificada) que valida las citas antes de la publicación. El anclaje criptográfico, los adaptadores de exportación y el registro que valida cada cita son infraestructura de la capa de espacio de trabajo. El sustrato se activa en cada compromiso a los repositorios wiki de contenido.

## Arquitectura

### Cómo opera el sustrato

Cada artículo (denominado TOPIC) en la wiki lleva frontmatter YAML que declara su título, slug, categoría, estado y — cuando el contenido está fundamentado en material externo — sus dependencias de citas. Las citas se resuelven contra un registro a nivel de espacio de trabajo; las referencias en línea utilizan IDs estables (`[ni-51-102]`); el registro asigna a cada ID un título, URL y referencia opcional a una cláusula. Esta es la capa [[citation-substrate]]. El sustrato es servido por [[substrate-native-compatibility|el motor wiki]] como la superficie orientada al lector.

Cada TOPIC comprometido adquiere una identidad criptográfica estable: un SHA del compromiso Git más la ruta del archivo, y un hash de contenido. Ambos se exponen en el HTML renderizado para que un indexador externo o un recuperador de reguladores pueda fijar un estado de contenido específico.

Dos mecanismos de marca de tiempo están planificados para la Fase 7 del motor wiki (previsto; la entrega real está sujeta a la capacidad de ingeniería y la secuenciación de hitos):

- **Anclaje OpenTimestamps** `[opentimestamps]` — anclaje criptográfico planificado de cada compromiso a la blockchain de Bitcoin. El anclaje en Bitcoin es gratuito, de código abierto y externo a la infraestructura del emisor; produce prueba de que un estado de contenido específico existía en una altura de bloque específica, sin requerir confianza en ningún intermediario único.
- **Marca de tiempo RFC 3161** `[rfc-3161]` — tokens de marca de tiempo formales planificados de una Autoridad de Sellado de Tiempo reconocida. Los tokens RFC 3161 tienen reconocimiento legal en la UE y en la mayoría de las jurisdicciones de derecho consuetudinario. El uso planificado de ambos mecanismos proporciona redundancia criptográfica: uno se ancla a un libro descentralizado; el otro proporciona el token formalmente reconocido que un regulador o tribunal puede verificar.

Los compromisos de cambio material — aquellos cuyas ediciones de TOPIC constituyen cambios materiales bajo la postura `[bcsc-continuous-disclosure]` — están previstos para emitir un artefacto de Diff-de-Divulgación firmado junto al TOPIC actualizado. El Diff-de-Divulgación es un diff criptográficamente firmado del cambio, no un derivado del TOPIC; está planificado para comprometerse como una Credencial Verificable W3C `[w3c-verifiable-credentials]` junto al artículo afectado. Esto es prospectivo y está sujeto a los factores de precaución en `[ni-51-102]` y `[osc-sn-51-721]`.

### Adaptadores de exportación por jurisdicción (planificados)

Está planificada una capa de adaptadores conectables (previsto; la entrega real sujeta a la activación del clúster y la secuenciación de ingeniería) para transformar el corpus Markdown en el formato de presentación que requiere cada superficie regulatoria:

| Adaptador | Superficie objetivo |
|---|---|
| `export-sedar` | SEDAR+ — presentaciones de divulgación continua canadienses bajo `[ni-51-102]` |
| `export-edgar` | SEC EDGAR — presentaciones en EE.UU.; etiquetadas con XBRL bajo las normas de la Ley de Valores |
| `export-esef` | Mandato ESEF de la UE — informes anuales iXBRL `[ixbrl-esef]`; objetivo de la Fase 1 de ESAP julio 2027 `[esap-eu-2027]` |
| `export-edinet` | Japón EDINET — presentaciones XBRL de la FSA |
| `export-dart` | Korea DART — presentaciones XBRL de la FSS |
| `export-magna` | Israel MAGNA — presentaciones iXBRL |

Para las jurisdicciones que requieren preservación electrónica cualificada — por ejemplo, `[eidas-qualified-preservation]` de la UE o los estándares de preservación a largo plazo ETSI — los adaptadores planificados están diseñados para producir salidas que satisfagan esos requisitos de preservación incluyendo la cadena de certificados de firma del emisor y el token de marca de tiempo RFC 3161 en el paquete de presentación.

Cada adaptador está planificado como un crate de Rust separable. Se prevé que las nuevas jurisdicciones sean aditivas sin modificar el núcleo del sustrato. Las declaraciones prospectivas en esta sección dependen del supuesto material de que el clúster de divulgación se active y de que el trabajo de mapeo de la taxonomía XBRL se complete antes de que los adaptadores sean necesarios en producción.

### Sustitución de sustrato aplicada a plataformas de divulgación

La práctica convencional de relaciones con inversores posiciona una plataforma de RI separada entre la documentación interna del emisor y la divulgación pública. Dichas plataformas suelen operar en infraestructura de nube de terceros y sirven la divulgación a los inversores desde esa infraestructura, con el registro legalmente material viviendo en el proveedor en lugar de bajo la propia infraestructura del emisor.

Bajo el modelo de sustitución de sustrato, el posicionamiento es diferente: la wiki es el registro de divulgación, servida directamente bajo el dominio propio del emisor, firmada bajo su propia clave, y anclada a libros externos que el emisor controla. No hay una plataforma de distribución de divulgación separada entre la fuente Markdown y el lector.

Los servicios que las plataformas de RI de proveedores ofrecen y que el sustrato no replica — segmentación de inversores, agregación de consenso del lado vendedor, analítica de vigilancia — son componibles a través de [[mcp-substrate-protocol|adaptadores MCP]] del Anillo 1 a medida que el sustrato madura. El sustrato reemplaza la función de sustrato de registro; compone con servicios adyacentes que dependen de datos de panel multi-emisor que el sustrato no puede replicar desde un único despliegue.

Las plataformas SaaS de divulgación de proveedores que operan en infraestructura con sede en Estados Unidos tienen una propiedad estructural relevante: la Ley CLOUD `[cloud-act-us]` extiende la autoridad extraterritorial de acceso a datos de EE.UU. sobre los proveedores con sede en ese país independientemente de dónde se almacenen los datos del cliente. Para un emisor en una jurisdicción donde la jurisdicción del proveedor importa — RGPD de la UE bajo la postura Schrems II, mandatos de residencia de Salud Canadá, PDPL de Arabia Saudita — el valor del sustrato de divulgación es que el registro vive bajo la propia infraestructura del emisor, en la jurisdicción propia del emisor, con el emisor en posesión de la clave de firma. Esta es portabilidad jurisdiccional por construcción, no por acuerdo de política con un proveedor.

### Fundamentación por IA aplicada al sustrato (planificado)

Un sustrato de divulgación que permita que texto generado por IA llegue a la publicación sin verificación produce una responsabilidad estructural: si la IA alució un hecho, ese hecho queda en el registro de divulgación. El HHEM de Vectara `[vectara-hhem]` es un enfoque de solo detección — identificar alucinaciones después de la generación. El mecanismo planificado del sustrato es la negativa de renderización: un TOPIC cuya cadena de prueba de fundamentación no verifica no llega al lector.

El mecanismo planificado (Fase 9 del motor wiki; previsto sujeto a que el clúster `project-disclosure` alcance este hito; sujeto a los factores de precaución en `[ni-51-102]` y `[osc-sn-51-721]`):

1. Cada afirmación en un TOPIC redactado por IA debe estar emparejada con un ID de cita resolvible en el registro de citas.
2. El hash de contenido de cada cita debe verificarse contra el hash almacenado del registro.
3. Un paso de veredicto de IA adversaria (una evaluación por un modelo separado) confirma que la afirmación está fundamentada en el contenido real de la fuente citada.
4. El veredicto se firma como una Credencial Verificable W3C `[w3c-verifiable-credentials]` y se compromete en el mismo compromiso Git que el TOPIC.
5. El renderizador wiki se niega a servir cualquier TOPIC cuya cadena de prueba de fundamentación no verifique.

Este mecanismo no depende de que el modelo que redactó el TOPIC sea fiable. Depende únicamente de que el registro de citas sea preciso y de que el veredicto de la IA adversaria sea más conservador que el modelo de redacción.

## Configuración

Conforme al lenguaje de divulgación continua de `[ni-51-102]`, los siguientes elementos de este artículo son prospectivos:

- Los adaptadores de exportación por jurisdicción planificados dependen de la activación del clúster `project-disclosure` y del trabajo de mapeo de la taxonomía XBRL. La entrega real está sujeta a la secuenciación de ingeniería y a la priorización por parte del operador.
- El anclaje mensual planificado con Sigstore Rekor v2 y el sellado de tiempo RFC 3161 dependen de que el binario `fs-anchor-emitter` se complete y de que la infraestructura de anclaje se active.
- La fundamentación por IA aplicada al sustrato planificada (Fase 9) depende del adaptador de la capa constitucional del clúster de inferencia y de que el clúster de divulgación alcance esa fase.
- Los artefactos de Diff-de-Divulgación firmados planificados y las Credenciales Verificables W3C de Prueba de Recepción del Suscriptor dependen de que la Fase 8 se complete antes de la Fase 9.

Los resultados reales pueden diferir de la trayectoria planificada descrita anteriormente. Todas las declaraciones prospectivas dependen de los supuestos materiales nombrados en cada sección y están sujetas a la realidad operativa, la capacidad de ingeniería y las decisiones del operador sobre la priorización de clústeres.

## Véase también

- [[compounding-substrate]]
- [[substrate-native-compatibility]]
- [[citation-substrate]]
- [[worm-ledger-architecture]]
