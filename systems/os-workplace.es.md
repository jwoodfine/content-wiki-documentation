---
schema: foundry-doc-v1
title: "os-workplace — El Escritorio Soberano"
slug: os-workplace
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-workplace.md
short_description: "os-workplace es el sistema operativo de escritorio gratuito de la familia PointSav — un escritorio soberano nativo en Rust que se empareja con un archivo Totebox, funciona en hardware de referencia deliberado y sirve como puerta de entrada a la línea de productos comerciales de PointSav."
cites: []
---

`os-workplace` es el sistema operativo de escritorio gratuito de la familia PointSav. Proporciona un entorno de escritorio limpio, seguro y nativo en Rust que se empareja naturalmente con un archivo Totebox y lleva la disciplina de teclas de función y el modelo de seguridad de la plataforma a un usuario comunitario que lo instala por primera vez. La estrategia es deliberada: `os-workplace` es la puerta de entrada a la adopción. Un nuevo usuario lo instala porque es gratuito y rápido; una vez que su trabajo diario ocurre dentro del ecosistema PointSav, el agregador comercial `os-orchestration` se convierte en el siguiente paso lógico. Este artículo cubre el hardware de referencia, la suite de aplicaciones, el modelo de emparejamiento y la justificación estratégica de un escritorio gratuito.

## Hardware de referencia

`os-workplace` apunta a un conjunto pequeño y deliberado de dispositivos. La fragmentación de hardware es el enemigo de la estabilidad; los perfiles de referencia oficiales se eligen por su compatibilidad de primer nivel con una base FreeBSD reforzada o seL4:

| Nivel | Dispositivo |
|---|---|
| Insignia | Dell XPS 13 / 14 (Developer Edition) |
| Flota | HP ProBook serie 400 (445/450) |

La evolución del núcleo refleja al resto de la familia: la Fase 1 funciona con un perfil de escritorio FreeBSD reforzado; la Fase 2 (prevista) migra a una compilación nativa del micronúcleo seL4.

## La suite de aplicaciones

Todas las aplicaciones son binarios nativos en Rust. La elección es razonada: un cliente PYME en 2030 valora el rendimiento local-primero y la fiabilidad sin conexión por encima de las herramientas de suscripción basadas en el navegador. Cada aplicación es pequeña, de propósito único y arranca en menos de 100 milisegundos.

| Aplicación | Enfoque del código fuente |
|---|---|
| `app-workplace-pdfs` | Bifurcación de `pdf-rs`; solo fidelidad ISO PDF/A |
| `app-workplace-wordprocessor` | Motor Typst para maquetación de documentos |
| `app-workplace-spreadsheet` | IronCalc — motor Rust con matemáticas deterministas |
| `app-workplace-email` | Bifurcación de Himalaya; TUI-primero, local-primero |
| `app-workplace-browser` | Bifurcación de Servo; telemetría eliminada |
| `app-workplace-communications` | Cliente Rust punto a punto basado en WebRTC |
| `app-workplace-chat` | Mensajería segura en tiempo real |
| `app-workplace-file-manager` | Bifurcación de Broot; búsqueda difusa, activado por acciones |
| `app-workplace-wiki` | Visor de documentación local-primero |
| `app-workplace-gis` (previsto) | Bifurcación de Whitebox-tools; geoespacial puro en Rust |
| `app-workplace-bim` (previsto) | ifc-rs y núcleo B-rep truck |

## Emparejamiento con el Totebox

`os-workplace` es el entorno local del usuario. Los datos viven en el [[totebox-os|os-totebox]] del usuario. Un apretón de manos de emparejamiento entre la estación de trabajo y el archivo establece confianza vinculada al hardware a través de `service-pairing`. No hay nombres de usuario ni contraseñas — el emparejamiento es el permiso.

Un usuario puede llevar `os-workplace` en una memoria USB, arrancarlo en una máquina prestada y tener el mismo entorno seguro sin dejar rastros en el anfitrión. Al cerrar la sesión, la memoria segura se borra. El Totebox permanece intacto en la nube.

## Por qué un escritorio gratuito es estratégico

Tres razones hacen de `os-workplace` un compromiso estructural en lugar de un gesto de marketing:

1. **Embudo de adopción.** Un escritorio gratuito y rápido introduce al operador en la disciplina de teclas de función de `os-console` y el modelo de seguridad del Diodo. Los productos comerciales se sienten familiares desde el primer día.
2. **Implementación de referencia.** Cada línea de código escrita para `os-workplace` es revisable en el monorepo público. Los clientes pueden auditar el sustrato antes de adquirir la agregación comercial.
3. **Gravedad del ecosistema.** Una comunidad creciente de usuarios de `os-workplace` crea una circunscripción independiente de contribuidores, empaquetadores y traductores que ningún producto exclusivamente comercial puede replicar.

## Véase también

- [[os-family-overview]] — la familia de ocho SO y dónde encaja os-workplace
- [[totebox-os]] — el socio de datos; el archivo con el que os-workplace se empareja
- [[console-os]] — la superficie alternativa TUI-primero para operadores que quieren control solo por teclado
- [[machine-based-auth]] — el modelo de emparejamiento que reemplaza los nombres de usuario y contraseñas
- [[hardware-reference]] — requisitos completos de CPU y hardware para la familia PointSav
