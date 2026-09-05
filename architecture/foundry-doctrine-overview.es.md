---
schema: foundry-doc-v1
title: "PointSav arquitectura 2030 — Resumen planificado"
slug: foundry-doctrine-overview
category: architecture
index_group: platform-structure
type: topic
content_type: topic
quality: complete
short_description: El alcance planificado para la futura carta constitucional de PointSav — aún no ratificada ni redactada; descrita aquí solo en términos planificados/previstos.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
 - mcp-spec
 - olmo3-allenai
paired_with: foundry-doctrine-overview.md
---

La **arquitectura [[pointsav-overview|PointSav]] 2030** es una carta constitucional planificada para el entorno de desarrollo de software de PointSav — aún no redactada ni ratificada. Este artículo describe su alcance previsto: seis pilares planificados, un conjunto previsto de afirmaciones estructurales que constituirían sus compromisos, invenciones operativas entre industrias previstas, y el [[economic-model|modelo económico]] que se pretende que la sostenga. Una vez redactada, se prevé que la carta sea un artefacto público — versionada, firmada y publicada bajo CC BY 4.0 en cada versión MINOR. Véase [[foundry-doctrine-architecture|la visión arquitectónica]] para el conjunto de afirmaciones previsto.

Ninguna versión de esta carta ha sido ratificada. Lo que sigue describe la planificación actual, no un documento publicado.

## Los Seis Pilares

Los seis pilares siguientes son los invariantes previstos de la arquitectura, planificados para funcionar como restricciones aplicadas una vez ratificada la carta — aún no vigentes como documento firmado.

**1. Solo texto plano.** UTF-8 Markdown para prosa, YAML simple para el enrutamiento. Sin formatos binarios, sin bases de datos, sin daemons, sin índices activos a nivel del sustrato.

**2. Alcance geométrico.** El rol de una sesión está determinado por el directorio en el que comienza — no por configuración ni declaración. El coordinador del espacio de trabajo opera en la raíz; las sesiones de archivo operan dentro del archivo que les corresponde; las sesiones de tarea operan dentro de un directorio de clúster por proyecto.

**3. Flujo unidireccional.** El desarrollo de software siempre procede proveedor → cliente → despliegues. Sin escrituras directas inversas. Todas las solicitudes entre capas viajan a través de un buzón de archivos.

### Invariantes de coordinación y garantía

**4. Buzón en cada límite.** Cada rol tiene una bandeja de entrada y una bandeja de salida — archivos Markdown de texto plano, con control de versiones, duraderos.

**5. Artefactos autodescriptivos.** Cada directorio con el que vale la pena interactuar lleva un `MANIFEST.md` que declara su origen, propietario, linaje y estado actual.

**6. Sobre de garantía humana en el bucle.** El trabajo rutinario se ejecuta de forma autónoma. La atención humana se reserva para el conjunto definido de eventos de punto de control estricto: despliegues de nuevos modelos en producción, operaciones destructivas, cambios de gobernanza.

## Las Afirmaciones de Salto Adelante

La tesis central de la doctrina: una plataforma cuyo modelo cabe completamente en texto plano en una sola VM, funciona sin una API externa y sobrevive 100 años en un disco duro se vuelve más valiosa a medida que la conectividad global se fragmenta y los entornos regulatorios divergen.

Se prevé que un conjunto de afirmaciones estructurales constituya este compromiso arquitectónico soberano para PYMEs, entre ellas:

- **[[single-boundary-compute-discipline|Disciplina de Cómputo de Límite Único]]** — cada llamada de inferencia de IA pasa por un único límite de servicio, el [[doorman-protocol|Doorman]].
- **[[knowledge-graph-grounded-apprenticeship|Aprendizaje Fundamentado en Grafo de Conocimiento]]** — el servicio de inferencia consulta el grafo de conocimiento por inquilino antes de cada solicitud sustantiva.
- **[[tui-corpus-producer|TUI como Productor de Corpus]]** — cada interacción terminal con el servicio de inferencia es una contribución de corpus de entrenamiento curada.
- **[[mcp-substrate-protocol|MCP como Protocolo del Sustrato]]** — cada servicio de Ring 1 y Ring 2 expone una interfaz de servidor MCP como su contrato externo principal.
### Bootstrap del inquilino y propiedad del cliente

- **[[seed-taxonomy-as-smb-bootstrap|Taxonomía Semilla como Bootstrap para PYMEs]]** — cada despliegue de inquilino se aprovisiona con una taxonomía semilla de cuatro partes como el bootstrap de su grafo de conocimiento.
- **[[customer-owned-graph-ip|IP del Grafo de Propiedad del Cliente]]** — el grafo de conocimiento por inquilino es propiedad intelectual del cliente.
- **[[tier-zero-customer-side-sovereign-specialist|Especialista Soberano del Lado del Cliente Nivel 0]]** — el despliegue de referencia Nivel 0 es un dispositivo de pequeño factor de forma que ejecuta el sustrato determinista completo más un modelo especialista de 1B, sin GPU requerida.
- **[[vertical-seed-packs-marketplace|Mercado de Paquetes Semilla Verticales]]** — paquetes semilla específicos de la industria distribuidos como taxonomías iniciales para nuevos despliegues de inquilinos.
### Contratos máquina-primero y flujos comerciales

- **[[code-for-machines-first|Código para Máquinas Primero]]** — cada contrato entre servicios, registro de auditoría, configuración y ontología es legible por máquinas como superficie primaria.
- **[[reverse-flow-substrate|Sustrato de Flujo Inverso]]** — la misma puerta de enlace [[doorman-protocol|Doorman]] y el mismo registro de auditoría que aplican la disciplina entrante también aplican los flujos comerciales salientes: un mercado de datos y un intercambio de publicidad.
- **[[service-wallet-settlement|Liquidación de Cartera de Servicios]]** — los ingresos del mercado y el intercambio de publicidad se acumulan en un libro de contabilidad interno por inquilino; [[pointsav-overview|PointSav]] nunca es un intermediario de custodia.
- **[[substrate-without-inference-base-case|Caso Base del Sustrato Sin Inferencia]]** — el [[totebox-archive|Archivo Totebox]] permanece completamente operativo y libremente transferible incluso cuando ningún nivel de inferencia está disponible.

### Afirmaciones fundacionales de versiones anteriores

Afirmaciones anteriores de importancia estructural, seleccionadas:

- **Vía de preentrenamiento continuo** hacia un modelo base propiedad del cliente. El sustrato se compone sin dependencia de proveedor a nivel del modelo.
- **El Sustrato Compuesto.** Cada interacción mejora el sustrato para las interacciones posteriores, dentro de la infraestructura del cliente.
- **Álgebra de Composición de Adaptadores.** El Doorman es un núcleo; los adaptadores son procesos; `service-content` es el sistema de archivos. Inteligencia componible.
- **Conocimiento Común / Comercio de Servicios.** Los artefactos de conocimiento son públicos y licenciados bajo CC. El umbral comercial es la agregación multi-Totebox.
- **Tenencia Diseñada para la Ruptura.** La salida del cliente es el final previsto por diseño, no una excepción de soporte.
- **Redacción Constitucional-Restringida.** El esquema de documentos del sustrato se compila en una gramática libre de contexto y se aplica en tiempo de decodificación de la IA. La IA no puede emitir contenido que no cumpla el esquema.
- **El Sustrato del Registro de Capacidades.** El estado de capacidad del sistema en ejecución ES el registro de solo-adición. La titularidad se transfiere mediante una única ceremonia de co-firma en la cúspide.
- **El Sustrato Soberano de Dos Bases.** seL4 para despliegues verificados; NetBSD para soberanía de arranque en cualquier lugar. Los mismos binarios en ambos.

## La Arquitectura de Tres Anillos

La plataforma organiza los servicios en tres anillos. Los Anillos 1 y 2 son deterministas y funcionan completamente sin el Anillo 3.

**Anillo 1 — Ingesta en el Límite (por inquilino, servidores MCP).** Servicios para la ingesta de documentos, datos de personas, correo electrónico y entrada directa.

**Anillo 2 — Conocimiento y Procesamiento (multi-inquilino mediante moduleId).** Servicios de extracción, grafo de contenido, búsqueda y egreso. El núcleo determinista de la plataforma, funcional sin IA.

**Anillo 3 — Inteligencia Opcional (instancia única, multi-inquilino).** El [[doorman-protocol|Doorman]] ([[service-slm]]) es la totalidad del Anillo 3. Enruta entre tres niveles de cómputo: Nivel A local (OLMo 1B en hardware del cliente, costo marginal cero), Nivel B de ráfaga de GPU ([[yoyo-compute-substrate|Yo-Yo]] OLMo 32B Think en una instancia de GPU de corta duración, controlada por el cliente), y Nivel C de API externa (API de proveedor externo con lista de permitidos explícita por solicitud). El Anillo 3 es estructuralmente opcional.

## Las Ocho Invenciones Entre Industrias

Se prevé que la arquitectura extraiga patrones operativos de dominios fuera del software, entre ellos: Pasaporte del Espacio de Trabajo (marítimo), NOTAM (aviación), Procedimiento de Retiro (farmacéutico), Conocimiento de Embarque (transporte marítimo), Operación Diferida en el Tiempo (bancario/fiduciario), Modo Aprendiz (habilitación tipo aviación / residencia médica), Ancla de Integridad (notaría / sellado de tiempo público), y Convención Constitucional (IETF RFC / enmienda constitucional, prevista para ejecutarse a través del proceso de gobernanza ya existente de `factory-release-engineering` una vez que exista la carta).

## El Modelo Económico

Los artefactos de conocimiento son la capa pública — publicados bajo licencias abiertas en cada versión MINOR de la Doctrina, libremente reutilizables. El umbral comercial es la agregación multi-Totebox. Un solo Totebox es infraestructura soberana; las operaciones que cruzan los límites del Totebox son un servicio de pago.

El modelo de contribuidores que sostiene esto: 4–7 empleados del Núcleo, 50–100 contribuidores de pago bajo contratos basados en resultados, y más de 10,000 contribuidores abiertos previstos construyendo sobre el sustrato público.

## Disciplina de Versionado

Se prevé que el texto se versione de forma independiente de cualquier repositorio individual una vez redactado: incrementos PATCH por cada commit aceptado; MINOR por cada hito de funcionalidad enviado; MAJOR por cada cambio disruptivo, con v1.0.0 planificada como la primera versión declarada estable. Actualmente no existe ninguna versión.

Se prevé que los incrementos MAJOR requieran un período de comentario público de 30 días. Se prevé que los incrementos MINOR produzcan un paquete firmado, versionado y citable públicamente. Se prevé que los commits a la eventual carta se firmen mediante firma basada en SSH y se anclen a un registro público de transparencia a través del Ancla de Integridad.

Las declaraciones prospectivas en este documento usan lenguaje de "planificado," "previsto" o "puede" con una base declarada y un marco de cautela. El texto no describe capacidades futuras como hechos actuales.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales del Sustrato Compuesto
- [[compounding-doorman]] — la disciplina de cómputo de límite único
- [[adapter-composition]] — el Álgebra de Composición de Adaptadores
- [[knowledge-commons]] — el modelo de Conocimiento Común / Comercio de Servicios
- [[system-substrate-doctrine]] — el Registro de Capacidades y el Sustrato Soberano de Dos Bases
- [[disclosure-substrate]] — el Sustrato de Divulgación Continua aplicado a la capa de la wiki

## Referencias

1. NI 51-102 Obligaciones de Divulgación Continua — Administradores de Valores de Canadá.
2. Política Nacional 51-201 de la CSA Divulgación de Información Prospectiva.
3. Especificación MCP — Protocolo de Contexto de Modelo, Anthropic, 2024.
4. OLMo 3 — Allen Institute for AI, Apache 2.0.
