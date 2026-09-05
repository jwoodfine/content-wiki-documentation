---
schema: foundry-doc-v1
type: topic
content_type: topic
index_group: sovereignty-and-infrastructure-patterns
slug: zero-execution-routing
short_description: "Las plantillas públicas de la página de inicio de la plataforma usan un patrón de casilla CSS nativa para el cambio de idioma y elementos interactivos, junto con una pequeña cantidad de JavaScript del lado del cliente para la integridad de página y analítica."
title: "Enrutamiento y script del lado del cliente en la capa de presentación"
audience: vendor-public
bcsc_class: current-fact
language: es
language_protocol: PROSE-TOPIC
quality: complete
cites: []
paired_with: zero-execution-routing.md
category: patterns
last_edited: 2026-08-22
editor: pointsav-engineering
---

Las plantillas públicas de la página de inicio usan estado de casilla CSS nativa — no JavaScript — para sus elementos interactivos. Los selectores de idioma y los botones de descarga cambian el contenido visible mediante selectores `:checked`, no mediante un script que escucha clics. **Un lector que cambia de idioma en la página de inicio no ejecuta ningún script para hacerlo** — esa interacción funciona incluso con JavaScript completamente desactivado. Las mismas plantillas sí llevan una pequeña cantidad de JavaScript del lado del cliente con otro propósito: calcular y mostrar una suma de verificación de integridad de página, y reportar analítica básica de vista de página al salir de ella.

## El patrón de casilla CSS

Los elementos interactivos — selectores de idioma, variantes de botón de descarga — operan sobre el estado de una casilla CSS nativa, no sobre estado controlado por script. El DOM carga todos los bloques de idioma y variantes de botón a la vez; reglas CSS de `display` ligadas al estado `:checked` de una casilla oculta muestran u ocultan el bloque correspondiente. Cambiar de idioma no implica ejecución de script ni recarga de página — es un cambio de estado puramente CSS. Los dos bloques de idioma viven hoy en un único archivo de plantilla, alternados por una sola casilla, no como documentos separados en rutas distintas.

## Qué script del lado del cliente sí ejecutan las páginas

Las plantillas de la página de inicio cargan un pequeño script en línea con dos propósitos ajenos al enrutamiento o al cambio de idioma. Calcula una suma de verificación SHA-256 del contenido para mostrarla en el bloque de metadatos, y emite una señal de vista de página (`navigator.sendBeacon`) cuando el lector navega fuera de ella. **Esto significa que la capa de presentación no está completamente libre de scripts** — un lector que audite el comportamiento real de la página encontrará este script ejecutándose hoy tanto en `pointsav.com` como en `woodfinegroup.com`. El enrutamiento y los cambios de estado basados en casillas descritos arriba sí funcionan sin script; la suma de verificación y la señal de analítica son una funcionalidad separada, más pequeña, superpuesta a esa página basada en CSS.

## Véase también

- [[sovereign-ai-routing]] — la arquitectura de enrutamiento de IA soberana que se combina con esta capa de presentación
- [[machine-based-auth]] — capa de autenticación basada en máquinas que opera en el mismo contexto de presentación
- [[decode-time-constraints]] — restricciones en tiempo de decodificación que aplican los límites de ejecución deterministas
- [[sel4-microkernel-substrate]] — el sustrato de microkernel que fundamenta el modelo de aislamiento de ejecución
