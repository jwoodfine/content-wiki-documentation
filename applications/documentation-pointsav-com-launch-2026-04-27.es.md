---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
language: es
companion: topic-documentation-pointsav-com-launch-2026-04-27.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

`https://documentation.pointsav.com` entró en servicio con TLS a las 16:25 UTC del 2026-04-27 bajo la versión v0.1.29 del espacio de trabajo. El despliegue sirve el wiki de ingeniería de PointSav (`app-mediakit-knowledge`) con un certificado Let's Encrypt válido hasta el 2026-07-26, con renovación automática programada mediante certbot.

El lanzamiento cierra un camino que comenzó en la sesión 1 del cluster project-knowledge (Fase 1 del motor wiki), continuó a través de la sesión 2 (Fase 1.1 cromo de memoria muscular Wikipedia) y la sesión 3 (Fase 2 todos los 7 pasos, más Fase 3), y concluyó con una sesión Master en v0.1.29 que reconstruyó el binario, lo instaló en `/usr/local/bin/app-mediakit-knowledge`, creó el directorio de estado en `/var/lib/local-knowledge/state`, y ejecutó la integración nginx de certbot para obtener el certificado TLS.

## La brecha que el lanzamiento detectó

El lanzamiento detectó una brecha previamente no identificada. La VM del espacio de trabajo ejecutaba ufw con `default deny incoming` y sólo `22/tcp` permitido en la capa del sistema operativo, a pesar de que el firewall de GCP ya permitía 80 y 443. La primera ejecución de certbot falló con "Timeout during connect". La corrección se aplicó en v0.1.29: `infrastructure/configure/configure-ubuntu-foundry.sh` se extendió para añadir reglas `ufw allow 80/tcp` y `ufw allow 443/tcp`.

## Lo que sirve hoy

Cuatro páginas TOPIC de marcador de posición se renderizan en la URL pública. El árbol de contenido de marcador de posición de cuatro archivos fue elaborado deliberadamente para estar limpio desde la perspectiva BCSC desde el primer carácter. Esto evita exponer el corpus heredado de 30+ TOPICs que tiene deuda editorial conocida.

La superficie de rutas completa de las Fases 1, 1.1, 2 y 3 está operativa: renderizado de artículos, editor CodeMirror 6, búsqueda Tantivy, feeds de sindicación, mapa del sitio, y endpoint `/git/{slug}` para ingesta de markdown crudo.

## Sustrato operacional

La pila de servicio es Linux + nginx + systemd + Let's Encrypt convencional. El binario está instalado en `/usr/local/bin/app-mediakit-knowledge` y se ejecuta como un usuario de sistema dedicado sin privilegios (`local-knowledge:local-knowledge`), vinculado a la interfaz de bucle invertido en el puerto 9090. La configuración de la unidad systemd está controlada por versiones como infraestructura como código en `~/Foundry/infrastructure/local-knowledge/local-knowledge.service`.

## La postura de marcador de posición — disciplina de divulgación por construcción

El cluster elaboró el subárbol `launch-placeholder/` de cuatro archivos para habilitar el lanzamiento TLS público sin exponer el corpus heredado con deuda editorial. La publicación eventual del corpus refinado se convierte en un único evento de cambio material ("primera publicación del corpus") en lugar de 23 a 30 eventos separados. El patrón es generalizable: cualquier despliegue futuro que dependa de un corpus listo editorialmente puede lanzar con un árbol de contenido de marcador de posición, y cambiar `--content-dir` una vez que el corpus esté ratificado.

## Verificación

Las siguientes comprobaciones son reproducibles desde cualquier host externo con conectividad TCP/443:

```
$ curl https://documentation.pointsav.com/healthz
ok

$ curl -I http://documentation.pointsav.com/
HTTP/1.1 301 Moved Permanently
```

El certificado indica `notAfter=Jul 26 16:24:00 2026 GMT` según la salida de `openssl x509`.

## Véase también

- [[app-mediakit-knowledge]] — la arquitectura del motor wiki
- [[source-of-truth-inversion]] — el patrón canónico / vista / efímero

## Procedencia

Narrativa de hechos actuales, redactada el 2026-04-27 inmediatamente después del lanzamiento v0.1.29. Las declaraciones prospectivas sobre las Fases 4–8 siguen [ni-51-102] y [osc-sn-51-721]. Refinado por project-language 2026-04-30.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
