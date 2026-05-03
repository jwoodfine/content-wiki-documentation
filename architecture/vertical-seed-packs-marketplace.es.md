---
schema: foundry-doc-v1
title: "Mercado de Paquetes de Semilla Vertical"
slug: vertical-seed-packs-marketplace.es
category: architecture
type: topic
quality: published
short_description: "Foundry tiene previsto distribuir paquetes de semilla curados específicos de la industria como taxonomías de inicio, con un mercado planificado que permite a los inquilinos contribuir mejoras."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: vertical-seed-packs-marketplace.md
---

El **Mercado de Paquetes de Semilla Vertical** es un mecanismo de distribución planificado para taxonomías de inicio específicas de la industria que aprovisionan el grafo de conocimiento de un nuevo inquilino Foundry. Cada paquete agrupa Arquetipos, un Plan de Cuentas, Dominios, Temas, un glosario y extensiones de servidor MCP adecuadas para una vertical de negocio particular. Este patrón codifica la reclamación doctrinal #50.

## Contenido del paquete

Cada paquete es un conjunto curado en formatos abiertos: un archivo JSON de Arquetipos, un archivo JSON de Plan de Cuentas, un archivo JSON de Dominios, un archivo JSON de Temas (típicamente escaso; el cliente añade los suyos), un CSV de glosario y una configuración de extensiones de servidor MCP (por ejemplo, una integración de punto de venta para un restaurante o una integración de registro médico electrónico para un hospital), además de un manifiesto con metadatos, versión, licencia y contribuyentes.

## Paquetes de referencia planificados

Foundry tiene previsto desarrollar y mantener un conjunto de paquetes de referencia en el lanzamiento de la Fase 5. El conjunto planificado incluye un paquete para restaurantes pequeños y medianos, uno para firmas legales de treinta a trescientos abogados, uno para hospitales pequeños y rurales, uno para empresas medianas de desarrollo inmobiliario, y un paquete universal predeterminado para negocios que no encajan en una vertical específica.

El paquete inmobiliario de Woodfine es la implementación de referencia actual, derivada de la taxonomía semilla existente del despliegue de Woodfine y validada en operación en producción.

## Distribución y contribución del cliente

El mecanismo de distribución planificado enruta a través de la puerta de enlace del mercado. Se prevé que los operadores puedan explorar paquetes disponibles dentro de la TUI, instalar un paquete con un único comando y recibir una vista previa de las diferencias antes de aplicar actualizaciones futuras del paquete.

Cuando un cliente extiende su paquete con adiciones útiles para otros en la misma vertical, se tiene previsto que puedan contribuir esas adiciones de vuelta al mercado. Las contribuciones aceptadas están previstas para aterrizar en la próxima versión del paquete, beneficiando a otros inquilinos en la vertical sin requerir que Foundry cree todo el contenido del paquete.

## Licencia de los paquetes

Los paquetes de referencia están previstos para distribuirse bajo una licencia permisiva. Las adiciones contribuidas por el cliente retienen el copyright del cliente pero otorgan derechos de distribución para la inclusión en el mercado.

El principio [[customer-owned-graph-ip]] se aplica a nivel de instancia, no de paquete: el grafo de conocimiento en ejecución del cliente (su instancia personalizada de un paquete) es su propiedad intelectual; el paquete en sí es material con licencia permisiva del que el cliente se personalizó.

## Composición

Los Paquetes de Semilla Vertical son el mecanismo de distribución del patrón [[seed-taxonomy-as-smb-bootstrap]] — llevan la forma canónica de la taxonomía de cuatro partes para una industria específica. El mercado planificado [[reverse-flow-substrate]] tiene previsto incluir paquetes como inventario de primera clase junto a listados de datos y pesos de adaptadores.

## Véase También

- [[seed-taxonomy-as-smb-bootstrap]] — la estructura de taxonomía de cuatro partes que los paquetes instancian
- [[customer-owned-graph-ip]] — la instancia personalizada del cliente es su PI; el paquete en sí está licenciado
- [[reverse-flow-substrate]] — la puerta de enlace del mercado planificada que distribuiría los paquetes
- [[mcp-substrate-protocol]] — las extensiones del servidor MCP del paquete se conectan al descubrimiento de herramientas del Portero

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-vertical-seed-packs-marketplace.md` (refinado el 30 de abril de 2026). Todas las reclamaciones de distribución, contribución y gobernanza llevan encuadre "planificado," "previsto" y "puede" conforme a la postura de divulgación continua BCSC.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
