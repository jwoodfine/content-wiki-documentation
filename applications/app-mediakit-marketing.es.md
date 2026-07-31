---
schema: foundry-doc-v1
title: "Aplicación de marketing MediaKit"
slug: app-mediakit-marketing
category: applications
type: concept
content_type: topic
quality: complete
short_description: "app-mediakit-marketing es un servidor web en Rust que entrega sitios de marketing usando el vocabulario de WordPress sobre una arquitectura soberana de archivos planos. Dos despliegues activos sirven home.woodfinegroup.com y home.pointsav.com."
status: active
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: app-mediakit-marketing.md
---

`app-mediakit-marketing` sirve páginas de inicio de marketing multi-inquilino desde un único binario Rust compilado estáticamente — sin PHP, sin MySQL, sin infraestructura de plugins — preservando al mismo tiempo la memoria muscular de WordPress.org en la superficie de URL y navegación orientada al operador. La aplicación entró en servicio en la versión v0.0.1 en mayo de 2026 y ejecuta dos inquilinos simultáneos en producción — Woodfine en `home.woodfinegroup.com` y PointSav en `home.pointsav.com` — desde el mismo binario en una única máquina virtual de bajo coste, separados únicamente por configuración de variables de entorno. Forma parte de la familia de superficies [[os-orchestration|`os-orchestration`]] y sigue el patrón [[leapfrog-2030-architecture|leapfrog-2030]] de contenido en archivos planos sin dependencia de base de datos.

## Antecedentes

WordPress impulsa aproximadamente el 40 por ciento de los sitios web rastreados por los motores de búsqueda. Su prevalencia refleja un logro de producto genuino: la interfaz de administración estandarizó la gestión de contenido para toda una generación de operadores. Un operador que aprendió WordPress en 2010 puede navegar una instalación nueva de WordPress en 2026 sin necesidad de reentrenamiento.

El pasivo es el sustrato. Los entornos de ejecución PHP, la administración de MySQL, la proliferación de plugins y el almacenamiento de contenido a nivel de base de datos crean una sobrecarga operativa desproporcionada para operadores pequeños y medianos. Las rutas de actualización rompen plugins. La corrupción de la base de datos requiere recuperación especializada. Los costos de alojamiento escalan con la capacidad del servidor, no con el volumen de contenido. La multi-tenencia requiere aislamiento de base de datos por inquilino o esquemas complejos de tablas compartidas.

`app-mediakit-marketing` resuelve esto conservando el contrato de interfaz mientras descarta el sustrato.

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

## Historial de contenido en el libro contable WORM

Previsto para v0.0.3: cada edición de contenido capturada a través del endpoint de auditoría (`/v1/audit/capture` mediante Doorman) está pensada para formar un historial de versiones de solo anexado. Esto se alinea con la convención [[worm-ledger-design|de diseño del libro contable WORM]]: el historial de contenido nunca se elimina, solo se anexa. El registro de auditoría cumple dos propósitos — reversión por parte del operador, y corpus de entrenamiento para el nivel de IA.

## Patrón de despliegue

`app-mediakit-marketing` se despliega detrás de nginx. nginx se encarga de:
- Terminación TLS (Let's Encrypt vía certbot)
- Servicio de archivos estáticos para `robots.txt` y `sitemap.xml`
- Redirección HTTP→HTTPS
- Proxy inverso hacia el puerto de loopback del binario

El binario nunca escucha en un puerto público. Todo el tráfico público pasa a través de nginx.

```
Internet → nginx :443 (TLS) → 127.0.0.1:PUERTO → app-mediakit-marketing
                              │
                              └→ CONTENT_DIR/ (lecturas de archivos planos)
                              └→ Doorman :9081 (DataGraph, opcional)
```

## Despliegues

Dos despliegues de producción simultáneos operan en una única máquina virtual de bajo coste:

| Despliegue | Inquilino | Dominio |
|---|---|---|
| `media-marketing-landing-1` | Woodfine | home.woodfinegroup.com |
| `media-marketing-landing-2` | PointSav | home.pointsav.com |

## Hoja de ruta

| Versión | Adiciones clave |
|---|---|
| v0.0.1 | Binario Rust, navegación con vocabulario WordPress, entorno multi-inquilino, DataGraph opcional, Nivel 0 |
| v0.0.2 | Sistema de temas (tokens CSS desde pointsav-design-system), marca por inquilino, ediciones auditadas (previsto) |
| v0.0.3 | Historial de versiones de edición de páginas en el libro contable WORM, fundamentos SEO (meta, sitemap, RSS) (previsto) |
| v0.1.0 | Superficie de plugins (app-orchestration-* compuestos vía iframe/API), formularios de contacto/leads que alimentan DataGraph (previsto) |

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
