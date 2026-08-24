---
schema: foundry-doc-v1
title: "app-mediakit-marketing — servidor de páginas de marketing autoría por agente"
slug: app-mediakit-marketing
category: applications
type: concept
content_type: topic
quality: complete
index_group: knowledge-and-editorial-applications
short_description: "app-mediakit-marketing es un servidor web en Rust que entrega sitios de marketing a partir de manifiestos de página tipados — la IA redacta vía MCP, un humano aprueba antes de que algo se publique. Sirve home.woodfinegroup.com y home.pointsav.com."
status: active
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: app-mediakit-marketing.md
cites: []
---

`app-mediakit-marketing` es un servidor web en Rust que entrega páginas de inicio de marketing — renderizadas en el servidor, con la IA como autora principal. Una página es un manifiesto tipado, no HTML ni Markdown libre: compone un título, una descripción, un idioma y una lista ordenada de secciones tipadas (una "hero", por ejemplo) tomadas del vocabulario de secciones compartido de `app-mediakit-shell`. El binario valida cada manifiesto contra ese vocabulario antes de poder renderizarlo, de modo que un manifiesto se ajusta o se rechaza — no existe una página parcial o malformada.

## Redacción por agente, publicación con aprobación humana

El contenido de esta plataforma está pensado para que lo redacte un agente de IA y lo apruebe un humano antes de publicarse, el mismo patrón de punto de control humano [[architecture-decisions|SYS-ADR-10]]/SYS-ADR-19 aplicado en el resto de la plataforma. Un servidor MCP, montado en `POST /api/mcp` cuando se habilita explícitamente, expone herramientas que un autor de IA invoca directamente: listar los tipos de sección disponibles, leer una página existente, validar un borrador contra el contrato de secciones, proponer una página y listar lo pendiente.

Un autor de IA nunca escribe directamente al árbol de contenido en producción. `propose_page` valida el manifiesto y lo deja en cola como un elemento pendiente; nada se publica hasta que un humano revisa el manifiesto propuesto frente a lo que está actualmente en vivo y lo aprueba. No existe una ruta de publicación automatizada.

## Arquitectura

### Binario

Un único binario de Rust compilado estáticamente (`app-mediakit-marketing`) ejecuta el servidor, construido sobre Axum. Sin dependencias de tiempo de ejecución más allá del kernel del sistema operativo y una libc.

### Multi-inquilino mediante variables de entorno

Un único binario admite múltiples inquilinos. La identidad del inquilino se establece al inicio mediante `SERVICE_MARKETING_MODULE_ID` (por ejemplo, `woodfine`, `pointsav`); el directorio de contenido, el puerto de escucha y el título del sitio se resuelven a partir de ese valor.

Dos instancias que ejecutan el mismo binario en el mismo host lo demuestran:

| Instancia | Inquilino | Dominio | Puerto |
|---|---|---|---|
| media-marketing-landing-1 | woodfine | home.woodfinegroup.com | 9102 |
| media-marketing-landing-2 | pointsav | home.pointsav.com | 9101 |

Cada instancia es un servicio systemd con su propio archivo de unidad y bloque de entorno. Ninguna instancia conoce a la otra.

## Soberanía y alineación con Nivel 0

La disciplina del [[compounding-substrate|Sustrato Compuesto]] define el Nivel 0 como un sistema propiedad del operador que funciona sin ninguna dependencia de nube de terceros. `app-mediakit-marketing` cumple este estándar:

- Binario único sin dependencias externas de tiempo de ejecución
- Almacenamiento de contenido basado en archivos — manifiestos de página en disco, sin base de datos
- El proxy inverso nginx gestiona TLS; no se requiere balanceador de carga administrado
- Se ejecuta en el VPS comercial más pequeño disponible ($7/mes)

Un operador PYME puede ejecutar su propio sitio de marketing en hardware que posee, con software construido a partir de fuente auditable, sin ninguna relación continua con un proveedor.

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
                              └→ CONTENT_DIR/ (manifiestos de página)
```

## Despliegues de referencia en vivo

Dos despliegues están activos desde el 2026-05-07 en `foundry-workspace`:

- **home.woodfinegroup.com** — sitio de marketing de nivel cliente de MCorp. Demuestra el patrón cliente: con marca propia, operado bajo la identidad del cliente.
- **home.pointsav.com** — despliegue de referencia abierto de nivel proveedor de PointSav. Demuestra el patrón proveedor: una referencia pública que los clientes potenciales pueden inspeccionar antes de desplegar su propia instancia.

Ambos sitios ejecutan el mismo binario `app-mediakit-marketing`. La diferencia es el contenido y los tokens de tema.

## Véase también

- [[app-mediakit-knowledge]] — servidor Rust hermano para contenido de base de conocimiento (mismo patrón arquitectónico)
- `app-mediakit-shell` — el vocabulario de secciones tipadas compartido del que este crate compone páginas (todavía sin artículo en la wiki de documentación)
- [[compounding-substrate]] — la disciplina arquitectónica soberana
- [[totebox-archive]] — el Archivo Totebox que contiene el contenido canónico de cada inquilino
