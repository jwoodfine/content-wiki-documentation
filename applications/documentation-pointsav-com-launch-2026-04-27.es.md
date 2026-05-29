---
schema: foundry-doc-v1
title: "documentation.pointsav.com entra en producción — 27 de abril de 2026"
slug: documentation-pointsav-com-launch-2026-04-27
short_description: "El lanzamiento con TLS de documentation.pointsav.com en abril de 2026: pila de servicio, postura de marcador de posición, fundamento de divulgación y comandos de verificación."
category: applications
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: documentation-pointsav-com-launch-2026-04-27.md
cites: [ni-51-102, osc-sn-51-721]
---

# documentation.pointsav.com entra en producción — 27 de abril de 2026

`https://documentation.pointsav.com` entró en producción con TLS a las 16:25 UTC del 27 de abril de 2026. El despliegue sirve el wiki de ingeniería de PointSav con un certificado Let's Encrypt válido hasta el 26 de julio de 2026, con renovación automática habilitada.

---

## Lo que se sirve hoy

Cuatro páginas TOPIC de marcador de posición se renderizan en la URL pública. `/wiki/welcome` es el artículo de bienvenida que explica el estado de vista previa pública. `/wiki/sample-article` ejercita la interfaz de renderizado: tabla de contenidos, lápices de edición por sección, bloque de pie de página con categorías, banda de encabezado, tabla de contenidos colapsable en el rail izquierdo, selector de idioma y las [[wikipedia-leapfrog-design|convenciones de disposición de Wikipedia]]. `/wiki/sample-forward-looking` ejercita el banner de advertencia de información prospectiva y cita tanto [ni-51-102] como [osc-sn-51-721]. `/wiki/sample-citations` ejercita las referencias de citas en línea.

Más allá de las rutas de renderizado de artículos, el wiki sirve: `/healthz` (verificación de disponibilidad); `/` (página de índice con todos los artículos); `/search?q=` (búsqueda de texto completo sobre el índice Tantivy en disco); `/feed.atom` (feed de sindicación RFC 4287); `/feed.json` (JSON Feed 1.1); `/sitemap.xml`; `/robots.txt`; `/llms.txt`; y `/git/{slug}` (fuente Markdown sin procesar).

---

## Pila de servicio

**Binario.** Un único binario [[app-mediakit-knowledge]] instalado en `/usr/local/bin/app-mediakit-knowledge`, construido en la rama de características del cluster. El tiempo de construcción fue de 1 minuto 54 segundos.

**Unidad systemd.** La unidad ejecuta el binario como un usuario de sistema sin privilegios dedicado (`local-knowledge:local-knowledge`), enlazado a la interfaz loopback en el puerto 9090. Las opciones de seguridad incluyen `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true` y `PrivateTmp=true`.

**Directorio de contenido.** El indicador de producción `--content-dir` apunta a un subdirectorio de marcador de posición de cuatro archivos. El corpus legado de más de 30 artículos TOPIC se conserva en el directorio padre pendiente de refinamiento editorial.

**nginx.** El puerto 443 termina TLS y hace proxy inverso al servicio loopback en el puerto 9090. El puerto 80 sólo sirve el desafío HTTP-01 de Let's Encrypt y emite una redirección 301 a HTTPS.

**Cortafuegos del sistema operativo.** La máquina virtual del workspace ejecuta ufw. La primera ejecución de certbot falló porque la VM sólo permitía el puerto 22 a nivel de sistema operativo, a pesar de que el cortafuegos de GCP permitía los puertos 80 y 443. La corrección añadió `ufw allow 80/tcp` y `ufw allow 443/tcp` al script de aprovisionamiento de infraestructura para que los futuros despliegues hereden estos puertos.

**DNS.** `documentation.pointsav.com` resuelve a la dirección IPv4 pública de la máquina virtual del workspace mediante un registro A en DreamHost.

---

## Postura de marcador de posición — fundamento de divulgación

El subárbol de marcador de posición de cuatro archivos fue creado específicamente para habilitar el lanzamiento público con TLS sin exponer el corpus TOPIC legado. El corpus legado presenta deuda editorial conocida: formulaciones prospectivas sin el banner de advertencia requerido por [ni-51-102] y vocabulario no conforme con la política de lenguaje del workspace.

La postura de marcador de posición colapsa esa superficie. Cuatro archivos escritos para ser correctos desde la primera línea exponen sólo prosa estructural (sin afirmaciones sobre resultados de negocio), sólo hechos verificados, y formulaciones prospectivas únicamente dentro del artículo de demostración explícita donde el patrón del banner de advertencia es precisamente el punto de la página. La eventual publicación del corpus refinado se convierte en un único evento de cambio material en lugar de muchos.

Este patrón es generalizable. Cualquier despliegue que dependa de que un corpus esté editorialmente listo puede lanzarse con un árbol de contenido de marcador de posición, intercambiar `--content-dir` una vez que el corpus sea ratificado y evitar el cambio todo-o-nada. La [[source-of-truth-inversion|inversión de la fuente de verdad]] — el árbol de Markdown es canónico; el binario en ejecución es una vista — hace que este intercambio sea una única recarga del servicio.

---

## Elementos prospectivos

Los siguientes elementos son planificados o previstos, no comprometidos. El lenguaje de advertencia se aplica conforme a [ni-51-102] y [osc-sn-51-721].

El canal editorial está previsto para refinar el corpus TOPIC legado en un pase separado. El resultado esperado es un árbol de contenido ratificado al que se puede intercambiar `--content-dir`, produciendo un único evento de cambio material.

El motor wiki está previsto para un desarrollo adicional a través de fases que cubren la confirmación de ediciones mediante git2, un grafo de wikilinks, una capa de federación con direccionamiento por contenido, un servidor MCP y un linter que refuerza los invariantes de clase de divulgación.

---

## Véase también

- [[app-mediakit-knowledge]]
- [[wikipedia-leapfrog-design]]
- [[source-of-truth-inversion]]
