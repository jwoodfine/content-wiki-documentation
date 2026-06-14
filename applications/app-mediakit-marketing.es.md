---
schema: foundry-doc-v1
title: "Aplicación de marketing MediaKit"
slug: app-mediakit-marketing
category: applications
type: concept
content_type: topic
quality: needs-update
short_description: "app-mediakit-marketing es un servidor web en Rust que entrega sitios de marketing usando el vocabulario de WordPress sobre una arquitectura soberana de archivos planos. Dos despliegues activos sirven home.woodfinegroup.com y home.pointsav.com."
status: active
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: app-mediakit-marketing.md
update_note: "EN sibling updated 2026-06-01 with expanded content (Background, WORM-ledger, Roadmap, Deployment pattern). ES adaptation refresh pending."
---

`app-mediakit-marketing` sirve páginas de inicio de marketing multi-inquilino desde un único binario Rust compilado estáticamente — sin PHP, sin MySQL, sin infraestructura de plugins — preservando al mismo tiempo la memoria muscular de WordPress.org en la superficie de URL y navegación orientada al operador. La aplicación entró en servicio en la versión v0.0.1 en mayo de 2026 y ejecuta dos inquilinos simultáneos en producción — Woodfine en `home.woodfinegroup.com` y PointSav en `home.pointsav.com` — desde el mismo binario en una única máquina virtual de bajo coste, separados únicamente por configuración de variables de entorno. Forma parte de la familia de superficies [[os-orchestration|`os-orchestration`]] y sigue el patrón [[leapfrog-2030-architecture|leapfrog-2030]] de contenido en archivos planos sin dependencia de base de datos.

## Función y arquitectura

El servidor presenta la presencia de marketing pública de cada inquilino en un dominio
configurable. La memoria muscular de WordPress se conserva en la capa UX: la interfaz
de administración expone el vocabulario Dashboard, Pages, Media y Themes familiar para
cualquier operador de WordPress, pero internamente la aplicación no utiliza PHP, MySQL
ni infraestructura de plugins.

Cada instancia por inquilino lee contenido desde un directorio de archivos planos
configurable. Un único binario compilado sirve tanto al inquilino Woodfine como al
inquilino PointSav mediante variables de entorno. El contenido almacenado en el [[totebox-archive|Archivo Totebox]] del inquilino es la fuente canónica; el binario en ejecución es una vista derivada sobre ese árbol de archivos planos. La compatibilidad de rutas
(`/wp-admin/`, `/wp-admin/post.php`, `/wp-admin/upload.php`) se mantiene en la capa
HTTP, garantizando la integración con herramientas que esperan el vocabulario WordPress.

## Despliegues

Dos despliegues de producción simultáneos operan en una única máquina virtual de bajo coste:

| Despliegue | Inquilino | Dominio |
|---|---|---|
| `media-marketing-landing-1` | Woodfine | home.woodfinegroup.com |
| `media-marketing-landing-2` | PointSav | home.pointsav.com |

## Estado actual

v0.0.1 entrega el servidor multi-inquilino central, la navegación compatible con
WordPress y el servicio básico de contenido en archivos planos. La integración de
entidades DataGraph, la gestión de carga de medios y el panel de administración
completo equivalente a WordPress están previstos para hitos posteriores.

## Véase también

- [[app-mediakit-knowledge]] — el motor wiki compañero en la familia MediaKit
- [[leapfrog-2030-architecture]] — el patrón arquitectónico que rige el sustrato de archivos planos sin base de datos
- [[totebox-archive]] — el Archivo Totebox que contiene el contenido canónico de cada inquilino
- [[os-orchestration]] — el SO de orquestación que aloja la familia MediaKit
