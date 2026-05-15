---
schema: foundry-doc-v1
title: "El Sustrato del Micronúcleo seL4"
slug: sel4-microkernel-substrate
category: substrate
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: sel4-microkernel-substrate.md
references:
  - id: 1
    text: "Klein, G., et al. 'seL4: Formal Verification of an OS Kernel.' ACM SOSP, 2009."
    url: "https://dl.acm.org/doi/10.1145/1629575.1629596"
  - id: 2
    text: "seL4 Foundation. 'Manual de Referencia seL4.' seL4 Foundation, 2023."
    url: "https://sel4.systems/Info/Docs/seL4-manual-latest.pdf"
---

El micronúcleo seL4 es el núcleo de L1, verificado formalmente por demostración matemática, sobre el que se ejecutan todos los sistemas operativos PointSav — sus propiedades de seguridad están demostradas, no aseveradas mediante pruebas. [^1] PointSav adopta seL4 como materia prima en lugar de construir un núcleo propio, y construye su capa Rust propietaria por encima de él. El aislamiento de memoria, los desbordamientos de búfer nulos, los permisos basados en capacidades y la ejecución determinista están garantizados estructuralmente — la base para afirmaciones de seguridad que pueden razonarse formalmente y presentarse a reguladores. Este artículo cubre la justificación arquitectónica, la pila de capas, las restricciones de la cadena de herramientas y la disciplina de lenguaje aplicada por encima del núcleo.

## Por qué adoptar en lugar de construir

Una alternativa razonable sería escribir un núcleo propio. PointSav rechaza explícitamente ese camino:

| Opción | Costo | Resultado |
|---|---|---|
| Construir un núcleo propio | Decenas de millones de dólares; cinco o más años de trabajo de verificación formal | Alcanzar un estándar de 2009 en la década de 2030 |
| Adoptar seL4 | Cero | Ya demostrado; listo para construir sobre él |

El principio es usar seL4 como materia prima — como el acero estructural — y construir el valor propietario por encima. El trabajo técnico competitivo de PointSav ocurre en la capa Rust por encima de seL4, no en el núcleo mismo.

## La pila de capas

| Capa | Componente | Propietario |
|---|---|---|
| L0 — Hardware | CPU x86_64 Haswell+ (véase [[hardware-reference\|referencia de hardware]]) | Proveedor de hardware |
| L1 — Micronúcleo | seL4 [^2] | Proyecto seL4 (adoptado upstream; parches menores) |
| L2 — Marco de controladores | sDDF (Marco de Controladores de Dispositivos seL4) con VirtIO | Ecosistema seL4 |
| L3 — Paquetes del sistema | Crates Rust `system-*` — controladores, red, sistema de archivos | PointSav |
| L4 — Servicios | Crates Rust `service-*` — lógica de aplicación | PointSav |
| L5 — Sistemas operativos | Composiciones `os-*` | PointSav |
| L6 — Aplicaciones | Superficies de usuario `app-*` | PointSav |

El límite entre L2 (adyacente al núcleo) y L3 (propiedad de PointSav) es la línea que PointSav traza alrededor de su valor propietario. Todo lo que está por debajo es una materia prima adoptada; todo lo que está por encima es propiedad.

Cuando el hardware de destino no admite el arranque nativo de seL4, una máquina virtual invitada Linux o BSD dentro de un hipervisor basado en seL4 proporciona un aislamiento estructural equivalente alrededor del SO invitado. La capa del hipervisor ofrece contención formalmente verificada incluso cuando el invitado en sí es un sistema operativo convencional.

## Qué proporciona seL4

| Propiedad | Qué significa en la práctica |
|---|---|
| Aislamiento matemático | Si `service-email` falla, `service-people` no puede sentirlo; el núcleo garantiza el límite |
| Ejecución determinista | Garantías en tiempo real sobre la temporización de instrucciones — importante para los protocolos de sincronización |
| Seguridad basada en capacidades | Los permisos se pasan como tokens de capacidad criptográfica, no como entradas en una tabla de permisos central |
| Cero desbordamientos de búfer en el núcleo | La clase de vulnerabilidad que produce la mayoría de los CVEs de sistemas operativos está matemáticamente excluida del núcleo |

El resultado es un sustrato donde las propiedades de seguridad pueden razonarse formalmente en lugar de aseverarse mediante pruebas de penetración. Esto cambia el tipo de afirmaciones de seguridad que pueden presentarse defensiblemente a un regulador.

## El Microkit y las restricciones de la cadena de herramientas

seL4 es intencionalmente mínimo: proporciona capacidades y comunicación entre procesos y muy poco más. Para hacerlo prácticamente utilizable, PointSav se apoya en el seL4 Microkit, un marco que traduce descripciones de sistema de alto nivel (manifiestos XML, binarios ELF) en las operaciones de capacidad de bajo nivel que el núcleo espera.

El Microkit tiene restricciones. Una está documentada en detalle en el archivo de ingeniería: el constructor x86_64 del Microkit mapea ávidamente Huge Pages de 1 GB para el código del núcleo, y luego no puede "fragmentar" esas páginas en sub-páginas de 4 KB cuando las asignaciones pequeñas posteriores colisionan. La resolución pragmática — colocar el búfer IPC en la parte inferior de la memoria y el núcleo justo por encima — es el tipo de disciplina detallada que exige trabajar en este nivel.

Este es un problema de calidad de vida del Microkit, no un error del núcleo. seL4 funciona según lo diseñado para un sistema de alta seguridad que prioriza el diseño de memoria determinista sobre la conveniencia del desarrollador.

## Disciplina de lenguaje

El sustrato aplica un único lenguaje por encima del núcleo: Rust.

| Lenguaje | Estado | Justificación |
|---|---|---|
| Rust | Obligatorio para todo el código `system-*`, `service-*` y `os-*` | Seguridad de memoria sin recolección de basura; se alinea con la verificación formal de seL4 |
| C / C++ | Prohibido en L3 y superior | Un solo desbordamiento de búfer en C anula el valor de las demostraciones de seL4 |
| Python / JavaScript | Prohibido en L3 y superior | Requiere tiempos de ejecución pesados; no puede ejecutarse como un Dominio de Protección seL4 sin violar las garantías de aislamiento |
| WebAssembly | Permitido solo para extensiones de usuario invitado | Un formato futuro de plugins de usuario; se ejecuta dentro de un tiempo de ejecución Wasm hospedado en Rust, nunca como servicio principal |

Permitir un servicio que no sea Rust en un Dominio de Protección reintroduciría la sobrecarga del tiempo de ejecución y la ejecución impredecible que el sustrato del micronúcleo está diseñado para eliminar.

## La arquitectura del estado final

La forma a largo plazo del sustrato es un Sistema Operativo de Micronúcleo Multi-Servidor: cada servicio — red, sistema de archivos, lógica de aplicación — se ejecuta como un unikernel aislado que pasa mensajes a través de IPC de seL4. El único trabajo del núcleo es el enrutamiento de hardware y la aplicación de capacidades.

Este es uno de los patrones más difíciles de la informática para implementar correctamente. El sustrato es ahora lo suficientemente maduro — a través de marcos como Genode y compiladores de unikernel basados en Rust — para que un proveedor institucional construya productos sobre él.

## Véase también

- [[machine-based-auth]] — autorización basada en capacidades construida sobre el modelo de capacidades seL4
- [[diode-standard]] — el protocolo de flujo de comandos unidireccional aplicado por encima del núcleo
- [[os-family-overview]] — las cinco superficies de SO que se componen sobre este sustrato
- [[hardware-reference]] — los requisitos arquitectónicos de CPU (Haswell+, fsgsbase, 1 GB Huge Pages)
- [[compliance-and-continuous-disclosure]] — cómo la verificación formal del núcleo apoya el cumplimiento de prueba continua
