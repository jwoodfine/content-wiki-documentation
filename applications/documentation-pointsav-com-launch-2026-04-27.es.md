---
schema: foundry-doc-v1
title: "documentation.pointsav.com entra en producción — 27 de abril de 2026"
slug: documentation-pointsav-com-launch-2026-04-27
short_description: "El lanzamiento con TLS de documentation.pointsav.com en abril de 2026: pila de servicio, postura de marcador de posición, fundamento de divulgación y comandos de verificación."
category: applications
type: topic
content_type: topic
index_group: knowledge-and-editorial-applications
status: active
quality: complete
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: documentation-pointsav-com-launch-2026-04-27.md
cites: [ni-51-102, np-51-201]
---

`https://documentation.pointsav.com` entró en producción con TLS a las 16:25 UTC del 27 de abril de 2026. El despliegue sirvió el wiki de ingeniería de PointSav con un certificado Let's Encrypt, con renovación automática habilitada. Este artículo es el registro histórico de ese día de lanzamiento; no describe el contenido actual del wiki.

---

## Lo que se lanzó el 27 de abril de 2026

En el lanzamiento, cuatro páginas TOPIC de marcador de posición se renderizaban en la URL pública — una postura deliberada de marcador de posición (véase más abajo), no el corpus en su forma actual. `/wiki/welcome` era el artículo de bienvenida que explicaba el estado de vista previa pública. `/wiki/sample-article` ejercitaba la interfaz de renderizado: tabla de contenidos, lápices de edición por sección, bloque de pie de página con categorías, banda de encabezado, tabla de contenidos colapsable en el rail izquierdo, selector de idioma y las [[wikipedia-leapfrog-design|convenciones de disposición de Wikipedia]]. `/wiki/sample-forward-looking` ejercitaba el banner de advertencia de información prospectiva y citaba tanto [ni-51-102] como [np-51-201]. `/wiki/sample-citations` ejercitaba las referencias de citas en línea.

Más allá de las rutas de renderizado de artículos, el wiki servía las mismas rutas operativas que sirve hoy: `/healthz` (verificación de disponibilidad); `/` (página de índice con todos los artículos); `/search?q=` (búsqueda de texto completo sobre el índice Tantivy en disco); `/feed.atom` (feed de sindicación RFC 4287); `/sitemap.xml`; `/robots.txt`; y `/llms.txt`. No existía ruta de edición ni función de colaboración en el lanzamiento — el motor no tiene ninguna superficie de escritura; cada artículo se edita en su repositorio git de origen y se recoge en el siguiente renderizado.

El corpus ha crecido sustancialmente desde entonces: una referencia base del 2026-09-04 registró 644 documentos en 15 categorías en este mismo wiki, incluida la categoría `applications` a la que pertenece este propio artículo. Lo que sigue describe el estado de marcador de posición del día de lanzamiento, no el contenido actual del wiki.

---

## Pila de servicio

**Binario.** Un único binario [[app-mediakit-knowledge]] instalado en `/usr/local/bin/app-mediakit-knowledge`, construido en la rama de características del cluster. El tiempo de construcción fue de 1 minuto 54 segundos.

**Unidad systemd.** La unidad ejecuta el binario como un usuario de sistema sin privilegios dedicado (`local-knowledge:local-knowledge`), enlazado a la interfaz loopback en el puerto 9090. Las opciones de seguridad incluyen `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true` y `PrivateTmp=true`.

**Directorio de contenido.** En el lanzamiento, el indicador de producción `--content-dir` apuntaba a un subdirectorio de marcador de posición de cuatro archivos, y el corpus legado de entonces más de 30 artículos TOPIC se conservaba en el directorio padre pendiente de refinamiento editorial. Ese refinamiento ya se completó y el indicador apunta ahora al corpus ratificado y sustancialmente mayor descrito arriba.

**nginx.** El puerto 443 termina TLS y hace proxy inverso al servicio loopback en el puerto 9090. El puerto 80 sólo sirve el desafío HTTP-01 de Let's Encrypt y emite una redirección 301 a HTTPS.

**Cortafuegos del sistema operativo.** La máquina virtual del workspace ejecuta ufw. La primera ejecución de certbot falló porque la VM sólo permitía el puerto 22 a nivel de sistema operativo, a pesar de que el cortafuegos de GCP permitía los puertos 80 y 443. La corrección añadió `ufw allow 80/tcp` y `ufw allow 443/tcp` al script de aprovisionamiento de infraestructura para que los futuros despliegues hereden estos puertos.

**DNS.** `documentation.pointsav.com` resuelve a la dirección IPv4 pública de la máquina virtual del workspace mediante un registro A en DreamHost.

---

## Postura de marcador de posición — fundamento de divulgación

El subárbol de marcador de posición de cuatro archivos fue creado específicamente para habilitar el lanzamiento público con TLS sin exponer el corpus TOPIC legado. En ese momento, el corpus legado presentaba deuda editorial conocida: formulaciones prospectivas sin el banner de advertencia requerido por [ni-51-102] y vocabulario aún no conforme con la [[compliance-and-continuous-disclosure|postura de divulgación continua]] para cada edición sustantiva.

La postura de marcador de posición colapsó esa superficie. Cuatro archivos escritos para ser correctos desde la primera línea exponían sólo prosa estructural (sin afirmaciones sobre resultados de negocio), sólo hechos verificados, y formulaciones prospectivas únicamente dentro del artículo de demostración explícita donde el patrón del banner de advertencia es precisamente el punto de la página. La intención era que la eventual publicación del corpus refinado se convirtiera en un único evento de cambio material en lugar de muchos.

Este patrón es generalizable. Cualquier despliegue que dependa de que un corpus esté editorialmente listo puede lanzarse con un árbol de contenido de marcador de posición, intercambiar `--content-dir` una vez que el corpus sea ratificado y evitar el cambio todo-o-nada. La [[source-of-truth-inversion|inversión de la fuente de verdad]] — el árbol de Markdown es canónico; el binario en ejecución es una vista — hace que este intercambio sea una única recarga del servicio.

---

## Elementos prospectivos

Los siguientes elementos son planificados o previstos, no comprometidos. El lenguaje de advertencia se aplica conforme a [ni-51-102] y [np-51-201].

El refinamiento del canal editorial que este artículo anticipaba originalmente ya ocurrió: el corpus ratificado descrito arriba reemplazó el árbol de marcador de posición mediante un intercambio de `--content-dir`, conforme al patrón de intercambio único que describe este artículo.

El motor wiki está previsto para un desarrollo adicional a través de fases que cubren la confirmación de ediciones mediante git2, un grafo de wikilinks, una capa de federación con direccionamiento por contenido, un servidor MCP y un linter que refuerza los invariantes de clase de divulgación.

---

## Véase también

- [[app-mediakit-knowledge]]
- [[wikipedia-leapfrog-design]]
- [[source-of-truth-inversion]]
