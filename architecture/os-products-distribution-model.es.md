---
schema: foundry-doc-v1
title: "os-infrastructure y os-network-admin: Modelo de Distribución"
slug: os-products-distribution-model
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: os-products-distribution-model.md
short_description: "Dos productos están previstos para software.pointsav.com: os-infrastructure ($19 USDC, metal desnudo o VM en la nube) y os-network-admin ($1 USDC, plano de control de la malla que incluye modo demonio Linux). Cada uno se distribuye como tres artefactos firmados por versión."
cites: []
---

Dos productos están previstos para distribución en `software.pointsav.com`:

| Producto | Precio | Qué proporciona |
|---|---|---|
| `os-infrastructure` | 19 USD en USDC | SO soberano para nodos de infraestructura PPN — funciona en metal desnudo, VM en la nube o QEMU |
| `os-network-admin` | 1 USD en USDC | Plano de control de la malla; también disponible como demonio Linux para sistemas existentes |

El precio está denominado en USDC en Polygon PoS. Sin facturación por suscripción. Sin necesidad de cuenta de cliente. La transacción en cadena es el recibo.

## Tres artefactos por producto

Cada producto distribuye tres artefactos firmados por versión. La misma clave Ed25519 firma los tres, por lo que la autenticidad del artefacto es verificable independientemente del servidor de distribución.

### `.iso` — Metal desnudo

Imagen ISO 9660 con cargador de arranque El Torito y GRUB2 multiboot. Se escribe en USB con herramientas estándar. Arranca en cualquier máquina x86-64 con soporte de virtualización por hardware (Intel VT-x o AMD-V), o AArch64 cuando se publique el objetivo AArch64.

Hardware objetivo: portátiles y equipos de escritorio retirados, servidores arrendados, equipos empresariales descomisionados — cualquier máquina x86-64 desde aproximadamente 2011 en adelante.

### `.qcow2` — Importación en VM en la nube

Imagen QCOW2 (formato nativo de QEMU). Se puede importar a los principales proveedores de nube como imagen personalizada y, a continuación, lanzar como instancia de nube estándar. Un único argumento de arranque `platform=` selecciona el comportamiento en tiempo de ejecución — el metal desnudo y la VM en la nube utilizan la misma imagen de núcleo.

### AppImage de demonio / `.deb` — Demonio Linux (solo os-network-admin)

Un binario Linux independiente para `os-network-admin`. No requiere arranque seL4. Se instala en cualquier sistema Linux x86-64 con WireGuard disponible, uniéndose a la malla PPN sin necesidad de reimaginar el host. Este es el camino principal para estaciones de trabajo Linux existentes — incluidas las máquinas que gestionan la custodia física de claves de la malla.

## Modelo de licencia

Flujo de pago:

1. El operador selecciona un producto en `software.pointsav.com` e inicia una transacción USDC en Polygon PoS.
2. El monitor de pagos detecta la transferencia confirmada en cadena y escribe un recibo.
3. El operador proporciona el hash de la transacción; la tienda emite un token de descarga firmado con Ed25519.
4. El token de descarga desbloquea los tres formatos de artefacto para la versión adquirida.
5. En usos posteriores, el binario instalado puede reverificar su token contra la clave pública de la tienda sin contactar de nuevo con la tienda.

El código fuente está disponible en GitHub. El pago de $19 / $1 cubre el binario precompilado, la firma Ed25519 de la clave de firma de PointSav y el token de licencia comercial.

## Principio de instalación en dos clics

El mercado objetivo son pequeñas y medianas empresas con personal de TI limitado. La complejidad de la instalación está limitada a tres decisiones del operador o menos.

Para `os-infrastructure` en metal desnudo: descargar el `.iso`, grabarlo en USB, arrancar la máquina y responder tres preguntas de configuración (nombre del nodo, punto de acceso de génesis, código de emparejamiento). El nodo aparece en la flota en treinta segundos tras completar la secuencia de emparejamiento.

Para `os-network-admin` en modo demonio: descargar el AppImage, hacerlo ejecutable, ejecutarlo y configurar el punto de acceso WireGuard a través de la interfaz de terminal guiada. El demonio se une a la malla y se registra en la flota sin necesidad de reimaginar ningún sistema.

Cualquier paso de instalación que añada complejidad más allá de este modelo es trabajo de reducción de alcance del producto, no una adición de funcionalidades.

## Véase también

- [[software-distribution-substrate]] — la arquitectura técnica del sistema de pago, emisión de licencias y entrega de binarios
- [[ppn-three-path-architecture]] — las tres opciones de arquitectura seL4 para nodos os-infrastructure
- [[sovereign-mesh]] — la malla WireGuard a la que se unen el demonio y el nodo en el primer arranque
- [[genesis-protocol]] — la secuencia de primer arranque autónomo para nodos os-infrastructure en metal desnudo
