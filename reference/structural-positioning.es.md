---
schema: foundry-doc-v1
title: "structural-positioning"
slug: structural-positioning
category: reference
type: concept
content_type: topic
quality: complete
short_description: "El posicionamiento estructural es el enfoque de PointSav para la diferenciación de mercado: articular compromisos arquitectónicos visibles en el código y la topología, en lugar de hacer comparaciones con competidores nombrados o referencias de rendimiento."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: structural-positioning.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
  - id: 1
    text: "NIST, Open Security Controls Assessment Language (OSCAL) — un conjunto de formatos en XML, JSON y YAML que proporcionan representaciones legibles por máquina de catálogos de controles, líneas base de controles, planes de seguridad del sistema y planes y resultados de evaluaciones."
    url: "https://pages.nist.gov/OSCAL/"
  - id: 2
    text: "Committee of Sponsoring Organizations of the Treadway Commission (COSO), Control Interno — Marco Integrado, 2013. Parte II: Marco — Principios y Puntos de Enfoque."
    url: "https://www.coso.org/guidance-on-ic"
---

El posicionamiento estructural es el enfoque que PointSav utiliza para describir la arquitectura al mercado: articular compromisos visibles a nivel del sistema de archivos, el protocolo o el kernel, en lugar de hacer comparaciones con competidores nombrados o afirmaciones de rendimiento relativo. La arquitectura está construida para fiduciarios institucionales — Consejeros Generales de empresas públicas, gestores de activos regulados, profesionales médicos y legales — que evalúan el software por su defensibilidad arquitectónica bajo auditoría, no por material de marketing. Los ocho compromisos descritos en este artículo son verificables por un auditor directamente en el sustrato desplegado. Al finalizar este artículo, el lector comprenderá los ocho compromisos estructurales, los patrones heredados que reemplazan y los segmentos de clientes a los que se dirigen.

## Por qué PointSav se posiciona estructuralmente en lugar de comparativamente

La base de clientes a la que sirve la plataforma no compra software basándose en comparaciones entre proveedores. Los gestores de activos, los profesionales regulados y las instituciones fiduciarias compran basándose en la defensibilidad: ¿puede el sistema responder las preguntas de un auditor directamente desde su propia estructura, sin una carta de atestación del proveedor?

El posicionamiento estructural aborda esto directamente. Cada compromiso en la tabla siguiente está presente en el sustrato desplegado o no lo está — ningún argumento de marketing interviene. Un auditor independiente puede verificar la propiedad de solo-adición del libro mayor, la ausencia del verbo de eliminación en la ruta de código, o la restricción unidireccional en el [[diode-standard|adaptador Diodo]], sin depender del resumen de controles autoreportado por el proveedor. [^2]

Las comparaciones con competidores nombrados se evitan específicamente. Los segmentos de clientes que atiende la plataforma toman decisiones de compra institucional que sobreviven cualquier tabla de comparación entre dos proveedores; los compromisos descritos aquí se mantienen independientemente del panorama competitivo cuando se revisa la decisión.

## Ocho compromisos estructurales que definen la arquitectura

Ocho propiedades distinguen el sustrato PointSav de los patrones que está diseñado para reemplazar. Cada una es estructural — visible a nivel del sistema de archivos, el protocolo o el kernel — y se mantiene en cada despliegue independientemente del cliente o la escala.

| Compromiso | Cómo se aplica |
|---|---|
| Propiedad del sistema operativo | El cliente posee una imagen de disco transferible, no una licencia de suscripción |
| Libro mayor de solo adición | El verbo de eliminación está ausente de la ruta de código del [[worm-ledger-design|libro mayor WORM]] |
| Flujo de comandos unidireccional | El [[diode-standard|adaptador Diodo]] es el único componente de enrutamiento entre la autoridad y el sujeto |
| Emparejamiento como permiso | No existen bases de datos de nombres de usuario y contraseñas en ningún lugar del sustrato; el acceso se rige por [[machine-based-auth|emparejamiento basado en máquina]] |
| Auditoría continua | El registro de auditoría se ejecuta a nivel del sistema; un administrador no puede deshabilitarlo |
| Resolución de activos en caso de fallo del proveedor | El Paquete de Resolución de Activos Digitales separa los datos limpiamente y los devuelve al propietario en caso de fallo del proveedor |
| Sustrato soberano | El cómputo y el almacenamiento se desacoplan entre sustratos — en las instalaciones, arrendado, nube — sin trampa de salida |
| Cumplimiento legible por máquina | Los manifiestos OSCAL[^1], el inventario de software y el inventario de hardware se exponen continuamente en lugar de solo durante los ciclos de auditoría anuales |

## Patrones heredados que la arquitectura reemplaza estructuralmente

Sin referencia a proveedores nombrados, los patrones arquitectónicos que el sustrato está diseñado para reemplazar son:

| Patrón heredado | Por qué falla la prueba de auditoría institucional |
|---|---|
| Interfaz SaaS arrendada | El cliente pierde el archivo cuando vence la suscripción |
| Base de datos en nube del proveedor centralizada | El cliente no puede tomar custodia física de sus propios registros |
| Control de Acceso Basado en Roles | Una credencial de administrador comprometida expone todo el patrimonio del cliente |
| Fuente única de verdad | Una brecha exitosa compromete la integridad de todos los consumidores posteriores |
| Lista de verificación de auditoría anual | El certificado del auditor puede estar desactualizado en el momento de su emisión |
| Suites de oficina de suscripción | No pueden operar sin conexión; no pueden garantizar la fidelidad de impresión a pantalla para registros regulados |
| Intermediarios de mensajes centralizados | Punto único de fallo para la malla de mensajes operativos |
| Interfaces de IA estilo chat | Requieren que los operadores fiduciarios conversen con el modelo; no producen un registro auditable de la intención del operador |

## Afirmaciones que la plataforma específicamente no hace

Tres afirmaciones que la plataforma no hace en material público, con las razones aquí declaradas:

1. **Sin comparaciones de "más rápido que".** Las características de rendimiento varían según el hardware del cliente; las afirmaciones comparativas no representarían los resultados en ninguna configuración que no sea la probada.
2. **Sin afirmaciones de precios de "más barato que".** La propuesta de valor comercial es la propiedad del sustrato, no el precio por licencia; las comparaciones de precios cambian más rápido que la arquitectura.
3. **Sin vocabulario de marketing de "IA Soberana".** Los términos operativos del producto son "Orquestación Totebox" y "Red Privada." El término "IA Soberana" estaba suficientemente saturado en múltiples productos no relacionados a principios de 2026 que ya no transmitía los compromisos arquitectónicos específicos aquí descritos.

## Cómo la arquitectura se adapta a cada segmento de clientes

La misma configuración de sustrato sirve a cada uno de los siguientes segmentos de clientes. Los compromisos estructurales anteriores se aplican de manera idéntica en todos los segmentos; lo que cambia es la configuración del [[archetypes-and-chart-of-accounts|Plan de Cuentas]] y la superficie de cumplimiento.

| Segmento de clientes | Registros en archivos [[totebox-os|Totebox]] |
|---|---|
| Gestor de activos inmobiliarios | Documentos de arrendamiento, modelos de información de construcción, comunicaciones con inquilinos |
| Emisor de información pública [ni-51-102] [osc-sn-51-721] | Comunicados de prensa, presentaciones regulatorias, actas de la junta |
| Práctica médica o quirúrgica | Registros de pacientes, archivos de diagnóstico, facturación clínica |
| Bufete de abogados | Expedientes de casos, materiales de descubrimiento, escritos judiciales firmados |
| Family office | Registros fiscales, documentos de sucesión, contratos del hogar |
| Hogar | Recibos, garantías, correspondencia personal |

Cada segmento utiliza los mismos cinco primitivos — Personas, Comunicaciones, Borradores, Registros, Dinero — bajo la misma superficie de [[console-os|Libro Mayor de Comandos]]. El sustrato no cambia. El Plan de Cuentas cambia.

## Véase también

- [[diode-standard]] — flujo de comandos unidireccional, el adaptador Diodo
- [[worm-ledger-design]] — principios de diseño del libro mayor WORM de solo adición
- [[machine-based-auth]] — emparejamiento como permiso, la alternativa al Control de Acceso Basado en Roles
- [[deployment-patterns]] — las seis formas canónicas de despliegue y sus contrapartes en el catálogo de flota
- [[archetypes-and-chart-of-accounts]] — la taxonomía del Plan de Cuentas que se adapta por segmento de cliente
- [[compliance-and-continuous-disclosure]] — los marcos de cumplimiento que aborda la arquitectura
