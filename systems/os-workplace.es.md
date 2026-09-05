---
schema: foundry-doc-v1
title: "os-workplace — El escritorio soberano"
slug: os-workplace
category: systems
type: concept
content_type: topic
quality: complete
index_group: operator-surfaces
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: os-workplace.md
short_description: "os-workplace es el nivel de escritorio gratuito previsto en la familia PointSav — hoy, un conjunto creciente de aplicaciones independientes en Rust y Tauri que el operador ejecuta en su propio equipo, incorporándose a la red como un par WireGuard station-*; la puerta de entrada prevista a la línea comercial."
cites: []
references:
  - id: 1
    text: "ISO 19005-1:2005 — Gestión de documentos — Formato de archivo de documento electrónico para preservación a largo plazo — Parte 1: Uso de PDF 1.4 (PDF/A-1)."
    url: "https://www.iso.org/standard/38920.html"
---

`os-workplace` está previsto como el nivel de escritorio gratuito de la familia PointSav. Lo que
existe hoy es una familia de aplicaciones de escritorio independientes en Rust y Tauri — las
aplicaciones de Workplace — que el operador descarga y ejecuta directamente en su propio equipo.
El crate `os-workplace` que las uniría en un único entorno unificado y de marca sigue siendo un
marcador de posición de una sola línea, no infraestructura construida. La estrategia detrás del
nivel gratuito es deliberada: un operador instala las aplicaciones de Workplace porque son rápidas
y no cuestan nada; una vez que su trabajo diario ocurre dentro del ecosistema PointSav, el
agregador comercial [[os-orchestration|`os-orchestration`]] se convierte en el siguiente paso
lógico. Este artículo cubre las aplicaciones reales que existen hoy, el plan ratificado para que
un equipo de Workplace se incorpore a la red, y la justificación estratégica de un nivel de
escritorio gratuito.

## Las aplicaciones de Workplace

Las aplicaciones son aplicaciones de escritorio Tauri — un backend en Rust junto con una WebView
en HTML/JS/CSS, dirigidas a macOS 10.13 High Sierra en adelante. Dos de los nueve crates de abajo
son Rust puro, sin WebView. Cada aplicación es independiente: un operador puede instalar una sin
las demás, y ninguna requiere el shell unificado `os-workplace` para funcionar.

| Aplicación | Estado | Qué hace |
|---|---|---|
| `app-workplace-memo` | Activa | Editor de documentos; produce un archivo `.html` autocontenido con las fuentes incrustadas, que imprime a un PDF impecable mediante el diálogo de impresión del sistema [^1] |
| `app-workplace-presentation` | Activa | Editor de diapositivas, construido sobre el mismo diseño local-primero y sin nube que Memo |
| `app-workplace-workbench` | Activa | Una ventana WebView delgada sobre el servidor HTTP `app-privategit-workbench` que corre localmente; no inicia, detiene ni administra ese servidor por sí misma |
| `app-workplace-proforma` | Activa | Hoja de cálculo para análisis financiero institucional; produce un archivo `.json` autocontenido con fórmulas, formato y una cadena de auditoría |
| `app-workplace-pdf` | Con andamiaje de código | Visor de PDF y herramienta de impresión que usa el crate `pdfium-render` (Google PDFium, Apache-2.0) |
| `app-workplace-gis` | Con andamiaje de código | Visor de escritorio para datos de inteligencia de localización; carga un visor de teselas MapLibre GL contra `gis.woodfinegroup.com` o un servidor de teselas local sobre la PPN |
| `app-workplace-bim` | Carpeta reservada | Editor de autoría BIM previsto (memoria muscular de Revit/AutoCAD); hoy es solo un documento de investigación — todavía no existen `Cargo.toml` ni código fuente |
| `app-workplace-aibridge` | Construido, aún no registrado en el catálogo | El núcleo del puente de edición de secciones con IA — permite a un operador entregar solo una sección de un documento a una sesión de IA externa y aplicar únicamente el resultado de esa sección; aplica [[machine-based-auth|SYS-ADR-07]] rechazando esquemas estructurados (datos de proforma, GIS, BIM) en cada punto de entrada |
| `app-workplace-http-prototype` | Construido, aún no registrado en el catálogo | Un servidor axum que expone las aplicaciones de Workplace sobre la PPN WireGuard mientras las compilaciones nativas de Tauri esperan un equipo de compilación macOS; el editor Memo es la única superficie que sirve hoy, el resto figura como pendiente |

## Despliegue: incorporación a la red

**Ratificado el 2026-05-23** (`DOCTRINE.md §IV.f`); implementación pendiente. `os-workplace` se
ejecuta en el propio equipo personal del operador — hoy, una MacBook — y está previsto que entregue
`app-workplace-desktop`, la superficie de escritorio unificada del operador que uniría las
aplicaciones anteriores en un solo entorno. Aloja [[os-console|`os-console`]] como aplicación
co-residente, no mediante virtualización de Tipo 2 — son dos capas independientes que comparten la
misma máquina. El equipo se incorpora a la [[ppn-architecture-overview|Red Privada PointSav]] como
par WireGuard directo dentro del rango `10.42.20.0/24`; la instancia `node-*` de `os-console` que
aloja hereda esa membresía en lugar de recibir una dirección propia. Las instancias de despliegue
usan el prefijo `station-*`, siguiendo la misma convención de numeración `<nombre>-N` que otras
instancias de despliegue de la PPN (véase, por ejemplo,
[[os-network-admin|`route-network-admin-1`]]). Las dos primeras previstas son `station-workplace-1`
y `station-workplace-2`, ambas a la espera del despliegue de la red WireGuard y de la
construcción de `app-workplace-desktop`. `os-workplace` no se conecta directamente con
[[totebox-orchestration|la puerta de enlace de orquestación]] — solo indirectamente, a través de
la instancia de `os-console` que aloja.

## Emparejamiento con el Totebox

`os-workplace` es el entorno local del operador. Los datos viven en el
[[totebox-os|os-totebox]] del operador. El emparejamiento basado en la máquina establece
confianza vinculada al hardware entre la estación de trabajo y el archivo — véase
[[machine-based-auth]] para el mecanismo. No hay nombres de usuario ni contraseñas; el
emparejamiento es el permiso.

## Por qué un escritorio gratuito es estratégico

Tres razones hacen de `os-workplace` un compromiso estructural en lugar de un gesto de marketing:

1. **Embudo de adopción.** Un conjunto de aplicaciones de escritorio gratuito y rápido está
   pensado para introducir al operador en la disciplina de teclas de función de
   [[os-console|`os-console`]] y el modelo de seguridad del [[diode-standard|Diodo]]. Así, los
   productos comerciales se sienten familiares desde el primer día.
2. **Implementación de referencia.** Cada línea de código escrita para las aplicaciones de
   Workplace es revisable en el monorepo público. Los clientes pueden auditar el
   [[compounding-substrate|sustrato]] antes de adquirir la agregación comercial.
3. **Gravedad del ecosistema.** Se prevé que una comunidad creciente de usuarios de las
   aplicaciones de Workplace cree una circunscripción independiente de contribuidores,
   empaquetadores y traductores que ningún producto exclusivamente comercial puede replicar. El
   [[contributor-model|modelo de contribuidores]] describe los roles y derechos para la
   participación comunitaria.

## Véase también

- [[os-family-overview]] — la familia de ocho SO y dónde encaja os-workplace
- [[totebox-os]] — el socio de datos; el archivo con el que os-workplace se empareja
- [[os-console]] — la superficie co-residente TUI-primero que transporta la conexión de red de
  os-workplace
- [[machine-based-auth]] — el modelo de emparejamiento que reemplaza los nombres de usuario y
  contraseñas
- [[ppn-architecture-overview]] — la red WireGuard a la que se incorporan los despliegues
  station-*
