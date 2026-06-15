---
schema: foundry-doc-v1
title: "La pila de tres capas"
slug: 3-layer-stack
short_description: "El Three-Layer Stack es el patrón de descomposición de infraestructura utilizado en todas las implementaciones de PointSav, separando la capacidad de cómputo puro, la ejecución de plataforma aislada y el acceso seguro del operador en tres capas distintas."
category: architecture
type: topic
content_type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: 3-layer-stack.md
cites: []
---


La Pila de Tres Capas es el patrón de descomposición de infraestructura utilizado en los despliegues de [[pointsav-overview|PointSav]]. El patrón separa la capacidad de cómputo bruto, la ejecución de la plataforma aislada y el acceso seguro del operador en tres capas distintas.

## Puntos clave

- Tres capas distintas: Infraestructura (cómputo bruto — bare-metal, nube o hardware del cliente), Plataforma (microkernel aislado y ejecución de servicios con límites de seguridad basada en capacidades), Entrega (interfaces de terminal y consola con las que interactúan directamente los operadores).
- Reemplazabilidad independiente en cada capa. Migrar de una infraestructura en la nube a hardware local no requiere cambios en la capa de plataforma. Las capas están desacopladas por diseño, no por convención.
- Ningún componente en la capa de plataforma puede superar las capacidades explícitamente otorgadas. El aislamiento se aplica en la capa del [[sel4-microkernel-substrate|microkernel]], no por política — un servicio comprometido no puede elevar su propio acceso.
- La capa de entrega es la única capa con la que los operadores interactúan directamente. Reenvía solicitudes hacia la plataforma y devuelve resultados hacia arriba; los operadores nunca tienen acceso directo a las primitivas de la capa de infraestructura como disco en bruto o interfaces de red.

## Las tres capas

**Capa de infraestructura** — el sustrato de cómputo físico o virtual: servidores bare-metal, instancias en la nube, hardware del cliente o cualquier combinación. Esta capa suministra tiempo de CPU y memoria. No realiza garantías de seguridad más allá de las que ofrece el hardware.

**Capa de plataforma** — el entorno de ejecución del sistema operativo y los servicios: [[totebox-os|ToteboxOS]], gestores de [[capability-based-security|capacidades]] y los procesos de servicio de los [[three-ring-architecture|Anillos 1 y 2]]. El aislamiento entre componentes se aplica en esta capa. Ningún componente de la capa de plataforma puede superar las capacidades que se le han concedido explícitamente.

**Capa de entrega** — las interfaces de terminal y consola que utilizan los operadores: terminales [[console-os|ConsoleOS]], la interfaz del corrector y cualquier superficie de acceso basada en navegador. La capa de entrega es la única capa con la que los operadores interactúan directamente; reenvía las solicitudes hacia la plataforma y devuelve los resultados hacia arriba.

## Por qué importa la separación

Cada capa es reemplazable de forma independiente. Un cliente puede migrar de una capa de infraestructura en la nube a hardware local sin cambiar cómo opera la capa de plataforma. La lógica operativa no está acoplada al sustrato físico que la ejecuta.

## Véase también

- [[compounding-substrate]]
- [[capability-based-security]]
- [[sel4-microkernel-substrate]]
- [[sovereign-ai-routing]]
- [[worm-ledger-architecture]]
