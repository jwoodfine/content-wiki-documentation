---
schema: foundry-doc-v1
title: "documentation.pointsav.com — registro de lanzamiento (2026-04-27)"
slug: documentation-pointsav-com-launch-2026-04-27.es
category: applications
type: topic
quality: complete
short_description: "El registro operativo del lanzamiento de documentation.pointsav.com a las 16:25 UTC del 2026-04-27: la pila de servicio, la postura de marcador de posición compatible con BCSC, la brecha ufw identificada y corregida, y las superficies de verificación disponibles desde cualquier host externo."
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: documentation-pointsav-com-launch-2026-04-27.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

## Adaptación estratégica

`https://documentation.pointsav.com` entró en funcionamiento con TLS a las 16:25 UTC del 2026-04-27, bajo la versión de espacio de trabajo v0.1.29. El despliegue sirve el wiki de ingeniería de PointSav (`app-mediakit-knowledge`) a través de un certificado emitido por Let's Encrypt mediante ACME, válido hasta el 2026-07-26, con renovación automática programada mediante certbot.

## El lanzamiento

Se ejecutaron seis acciones de despliegue. La reconstrucción del binario tomó 1 minuto 54 segundos. El servicio systemd entró en estado `active` sin advertencias. El verificador de bucle en `127.0.0.1:9090` confirmó que todas las rutas devolvían 200. El verificador externo en `https://documentation.pointsav.com` confirmó todas las rutas devolviendo 200, incluida la redirección 301 HTTP→HTTPS instalada por la automatización nginx de certbot.

El lanzamiento puso en evidencia una brecha no detectada previamente. La VM del espacio de trabajo ejecutaba ufw con `default deny incoming` y solo `22/tcp` permitido en la capa del sistema operativo, a pesar de que el firewall de GCP ya permitía 80 y 443 a través de la regla `allow-https-documentation`. La primera ejecución de certbot falló con "Timeout during connect" antes de que se diagnosticara la brecha. La corrección aterrizó en v0.1.29: `infrastructure/configure/configure-ubuntu-foundry.sh` se extendió para agregar las reglas `ufw allow 80/tcp` y `ufw allow 443/tcp`, de modo que los futuros aprovisionamientos de VM hereden estos puertos.

## Qué sirve al lanzamiento

Cuatro páginas de artículos marcadores de posición se renderizan en la URL pública: `/wiki/welcome` (explicando el estado de vista previa pública), `/wiki/sample-article` (ejercitando el chrome de renderizado), `/wiki/sample-forward-looking` (ejercitando el banner cautelar de información prospectiva, citando `ni-51-102` y `osc-sn-51-721`), y `/wiki/sample-citations` (ejercitando las referencias `[citation-id]` en línea).

La superficie completa de rutas de las Fases 1, 1.1, 2 y 3 está operativa: `/healthz`, `/`, `/wiki/{slug}`, `/search?q=`, `/feed.atom`, `/feed.json`, `/sitemap.xml`, `/robots.txt`, `/llms.txt`, `/git/{slug}` y las rutas del editor de fase 2 (con el relé de colaboración desactivado por defecto).

## Sustrato operativo

La pila de servicio es Linux + nginx + systemd + Let's Encrypt convencionales:

**Distribución del binario.** `app-mediakit-knowledge` compila a un binario único instalado en `/usr/local/bin/app-mediakit-knowledge`. Duración de la compilación: 1 minuto 54 segundos para `cargo build --release` desde un directorio de destino templado.

**Unidad systemd.** `/etc/systemd/system/local-knowledge.service` ejecuta el binario como usuario de sistema sin privilegios (`local-knowledge:local-knowledge`), vinculado a la interfaz de loopback en el puerto 9090, con marcas de endurecimiento incluyendo `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true` y `PrivateTmp=true`.

**Directorio de estado.** `/var/lib/local-knowledge/state` contiene el índice de búsqueda Tantivy en disco. El índice se reconstruye en cada inicio del binario, por lo que una eliminación del directorio de estado no es destructiva.

**Árbol de contenido.** El `--content-dir` del lanzamiento apunta al subdirectorio de cuatro archivos marcadores de posición. El intercambio al corpus completo cuando esté editorialmente listo será una única recarga de systemd.

**Registro A de DreamHost.** `documentation.pointsav.com` resuelve a la dirección IPv4 pública de la VM del espacio de trabajo `34.53.65.203`.

**certbot.** El certificado fue provisionado mediante la integración nginx de certbot. La renovación automática está habilitada; vencimiento: 2026-07-26.

## La postura de marcador de posición — compatible con BCSC por construcción

Los cuatro archivos marcadores de posición fueron redactados específicamente para permitir el lanzamiento público con TLS sin exponer el corpus heredado de más de 30 artículos, que contiene deuda editorial conocida. Limpiar esos artículos en su lugar habría producido 23 ediciones más 6 elementos de decisión del operador, más un evento de divulgación de cambio material por cada edición sustantiva.

La postura de marcador de posición colapsa esa superficie. La eventual publicación del corpus refinado se convierte en UN evento de cambio material ("primera publicación del corpus") en lugar de 23 a 30 eventos separados.

El patrón es generalizable. Cualquier despliegue futuro que dependa de que un corpus esté editorialmente listo puede lanzarse con un árbol de contenido marcador de posición, intercambiar `--content-dir` una vez que el corpus esté ratificado, y evitar el cambio todo-o-nada.

## Lo que está planificado a continuación

Los encuadres prospectivos de esta sección son *planificados*, no *comprometidos*. Se aplica lenguaje cautelar conforme a [ni-51-102] y [osc-sn-51-721].

La canalización editorial *planifica* refinar el corpus heredado de más de 30 artículos en un pase editorial separado. El resultado esperado es un árbol de contenido ratificado al que se *podrá* cambiar `--content-dir`, produciendo un único evento de divulgación de cambio material.

El motor wiki *planifica* un desarrollo adicional a través de las Fases 4 a 8. Las Fases 4 a 8 son *planificadas*; se aplica lenguaje cautelar conforme a [ni-51-102] y [osc-sn-51-721]. Los cambios materiales en la trayectoria se divulgarán mediante commits firmados y entradas de registro de cambios en este dominio.

## Véase también

- [[app-mediakit-knowledge]] — la arquitectura del motor wiki, la superficie de rutas y las fases de construcción
- [[source-of-truth-inversion]] — el patrón canónico / vista / efímero que este despliegue encarna
- [[collab-via-passthrough-relay]] — la implementación del relé WebSocket (desactivada por defecto en el lanzamiento)
