---
schema: foundry-doc-v1
title: "app-mediakit-marketing"
slug: app-mediakit-marketing
language: es
category: applications
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
paired_with: app-mediakit-marketing.md
---

`app-mediakit-marketing` es el servidor de páginas de inicio de marketing de PointSav.
Entrega superficies web de marketing multi-inquilino desde un binario Rust compilado
estáticamente, respaldado por contenido en archivos planos, aplicando el vocabulario de
URL y navegación compatible con WordPress.org sobre la arquitectura interna leapfrog-2030
de PointSav. La aplicación alcanzó el estado MVP v0.0.1 en mayo de 2026, sirviendo dos
despliegues de producción simultáneos en la VM foundry-workspace.

## Función y arquitectura

El servidor presenta la presencia de marketing pública de cada inquilino en un dominio
configurable. La memoria muscular de WordPress se conserva en la capa UX: la interfaz
de administración expone el vocabulario Dashboard, Pages, Media y Themes familiar para
cualquier operador de WordPress, pero internamente la aplicación no utiliza PHP, MySQL
ni infraestructura de plugins.

Cada instancia por inquilino lee contenido desde un directorio de archivos planos
configurable. Un único binario compilado sirve tanto al inquilino Woodfine como al
inquilino PointSav mediante variables de entorno. La compatibilidad de rutas
(`/wp-admin/`, `/wp-admin/post.php`, `/wp-admin/upload.php`) se mantiene en la capa
HTTP, garantizando la integración con herramientas que esperan el vocabulario WordPress.

## Despliegues

Dos despliegues de producción simultáneos operan en la VM foundry-workspace:

| Despliegue | Inquilino | Dominio | Puerto |
|---|---|---|---|
| `media-marketing-landing-1` | Woodfine | home.woodfinegroup.com | 9102 |
| `media-marketing-landing-2` | PointSav | home.pointsav.com | 9101 |

## Estado actual

v0.0.1 entrega el servidor multi-inquilino central, la navegación compatible con
WordPress y el servicio básico de contenido en archivos planos. La integración de
entidades DataGraph, la gestión de carga de medios y el panel de administración
completo equivalente a WordPress están previstos para hitos posteriores.

## Véase también

- [[app-mediakit-knowledge]]
- [[app-orchestration-bim]]
- [[leapfrog-2030-architecture]]
