---
schema: foundry-doc-v1
title: "app-console-keys — chasis de la consola y marco de teclas de función"
slug: app-console-keys
category: applications
type: app
content_type: topic
quality: complete
index_group: input-and-developer-surfaces
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: app-console-keys.md
short_description: "app-console-keys es el chasis base siempre instalado de os-console. Proporciona el rasgo Cartridge que implementan todos los módulos de la consola, la barra de navegación de teclas de función, la barra de estado y el cliente de autorización basada en máquina."
cites: []
---

`app-console-keys` es el chasis base siempre instalado de [[console-os|os-console]]. Todos los demás módulos de la consola — correo electrónico, contenido, monitorización de modelos de inferencia y el resto — son cartuchos opcionales que se conectan al marco que define `app-console-keys`. El módulo es obligatorio: un binario de `os-console` construido sin él no compilará.

**Nota de nomenclatura:** "keys" en `app-console-keys` hace referencia a las teclas de función del teclado — la barra F1 a F12 que navega entre los slots de cartuchos. No hace referencia a claves criptográficas. El emparejamiento criptográfico y la autorización basada en máquina son implementados por `system-gateway-mba`, un crate separado.

## El rasgo Cartridge

`app-console-keys` define el rasgo `Cartridge` — la interfaz que debe implementar cada módulo `app-console-*`. El rasgo es mínimo: un módulo declara qué slot de tecla de función ocupa, qué renderizar cuando ese slot está activo y cómo manejar la entrada del teclado mientras está activo. El chasis gestiona todo lo demás: registro de slots, despacho de entrada, gestión del foco y la barra de estado.

Dado que los cartuchos se compilan directamente en el binario de `os-console` en lugar de cargarse en tiempo de ejecución, el rasgo es un contrato en tiempo de compilación. Un módulo que no lo implementa produce un error de compilación, no un fallo en tiempo de ejecución.

## La barra de navegación de teclas de función

El elemento de interfaz principal gestionado por `app-console-keys` es la barra horizontal de pestañas de teclas de función en la parte superior de la consola. La barra muestra un slot por cartucho registrado. El slot activo está resaltado; los slots inactivos aparecen en gris cuando no están instalados.

La barra no reordena los slots en tiempo de ejecución. La posición de cada cartucho está fijada en el número de tecla de función que reclama. [[app-console-input]] está permanentemente fijado en F12 según [[architecture-decisions|SYS-ADR-10]].

## La barra de estado

La barra de estado de `app-console-keys` se ejecuta a lo largo de la parte inferior de la consola y es siempre visible, independientemente del slot de cartucho activo. Muestra:

| Componente | Contenido |
|---|---|
| Identidad | Nombre de usuario y tenant establecidos durante la ceremonia de emparejamiento |
| Estado de autorización | `MBA LINK ACTIVE`, `MBA LINK INACTIVE <razón>` o `MBA LINK PENDING` |
| Slot activo | Nombre del cartucho enfocado actualmente |
| Emparejamientos pendientes | Cantidad de solicitudes de emparejamiento a la espera de aprobación del operador |
| Duración de la sesión | Tiempo transcurrido desde el inicio de la consola |

## Cliente de autorización

`app-console-keys` mantiene un único enlace saliente de [[machine-based-auth|autorización basada en máquina]] hacia el host Totebox. A diferencia de los slots por cartucho de la barra F, este enlace es de todo el chasis, no por servicio: hay un único estado de autorización, no uno por backend emparejado.

Cuando el enlace se vuelve inactivo, el chasis reemplaza toda su área de contenido con una pantalla de emparejamiento a pantalla completa — todos los cartuchos, sin importar con qué backend hablen, dejan de renderizarse hasta que el enlace se restablece. Ningún cartucho hace caer el chasis; el chasis simplemente muestra la pantalla de emparejamiento en lugar de cualquier contenido de cartucho.

## Configuración

La configuración basada en perfiles se almacena en `~/.config/os-console/config.toml`. El archivo de configuración controla a qué servicios de backend intenta emparejarse la consola al inicio, las preferencias de visualización y el puerto del servidor SSH (si la función de servidor SSH está compilada).

## Renderización de PDF y soporte gráfico

`app-console-keys` proporciona la infraestructura gráfica utilizada por los cartuchos que renderizan imágenes: la ruta de visualización usa el protocolo de gráficos Kitty como camino principal, con la codificación Sixel como alternativa y un mensaje de error para entornos de terminal que no admiten ninguno de los dos. La renderización de PDF es un asunto aparte — los cartuchos que renderizan páginas PDF como mapas de bits dependen de `app-console-content`, que incorpora `pdfium-render` directamente en lugar de pasar por este chasis.

## Véase también

- [[console-os]] — descripción general del producto os-console, incluida la superficie de teclas de función y los modos de operación
- [[os-console-platform]] — la arquitectura completa de cartuchos y el mapa de teclas de función
- [[app-console-input]] — la puerta de entrada obligatoria F12; siempre compilada junto a app-console-keys
- [[machine-based-auth]] — el mecanismo de autorización que gestiona el cliente del chasis
- [[three-ring-architecture]] — la arquitectura Ring 1/2/3 a la que se conecta el cliente de autorización
