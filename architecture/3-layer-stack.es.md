---
schema: foundry-doc-v1
title: "La Pila de Tres Capas"
slug: 3-layer-stack
category: architecture
type: topic
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

La Pila de Tres Capas es el patrón de descomposición de infraestructura utilizado en los despliegues de PointSav. El patrón separa la capacidad de cómputo bruto, la ejecución de la plataforma aislada y el acceso seguro del operador en tres capas distintas.

## Las tres capas

**Capa de infraestructura** — el sustrato de cómputo físico o virtual: servidores bare-metal, instancias en la nube, hardware del cliente o cualquier combinación. Esta capa suministra tiempo de CPU y memoria. No realiza garantías de seguridad más allá de las que ofrece el hardware.

**Capa de plataforma** — el entorno de ejecución del sistema operativo y los servicios: ToteboxOS, gestores de capacidades y los procesos de servicio de los Anillos 1 y 2. El aislamiento entre componentes se aplica en esta capa. Ningún componente de la capa de plataforma puede superar las capacidades que se le han concedido explícitamente.

**Capa de entrega** — las interfaces de terminal y consola que utilizan los operadores: terminales ConsoleOS, la interfaz del corrector y cualquier superficie de acceso basada en navegador. La capa de entrega es la única capa con la que los operadores interactúan directamente; reenvía las solicitudes hacia la plataforma y devuelve los resultados hacia arriba.

## Por qué importa la separación

Cada capa es reemplazable de forma independiente. Un cliente puede migrar de una capa de infraestructura en la nube a hardware local sin cambiar cómo opera la capa de plataforma. La lógica operativa no está acoplada al sustrato físico que la ejecuta.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
