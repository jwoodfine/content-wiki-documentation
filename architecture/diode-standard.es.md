---
schema: foundry-doc-v1
title: "El estándar del diodo"
slug: diode-standard
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: diode-standard.md
short_description: "El Estándar del Diodo es la topología de seguridad fundacional de la familia de sistemas operativos PointSav — un flujo de comandos unidireccional donde el tráfico se mueve de la autoridad al sujeto y nunca al revés, suprimiendo los ataques de movimiento lateral al eliminar la lógica de enrutamiento que los haría posibles."
cites: []
references:
 - id: 1
 text: "Rose, S. et al. 'Arquitectura de Confianza Cero.' NIST SP 800-207, 2020."
 url: "https://doi.org/10.6028/NIST.SP.800-207"
 - id: 2
 text: "MITRE. 'ATT&CK Tactic: Movimiento Lateral (TA0008).' MITRE Corporation, 2023."
 url: "https://attack.mitre.org/tactics/TA0008/"
---

Un atacante que vulnera una máquina rara vez quiere esa máquina. Quiere la siguiente. El movimiento lateral — pivotar desde un primer nodo comprometido hacia nodos más valiosos — es el patrón dominante en los informes modernos de brechas de seguridad [^2].

El Estándar del Diodo elimina el pivote. <!--claim id=diode-principle confidence=structural cites=[]-->En ingeniería eléctrica un diodo conduce corriente en una dirección y la bloquea en la otra. El Estándar del Diodo aplica la misma regla a los comandos en toda la [[os-family-overview|familia de sistemas operativos]] de [[pointsav-overview|PointSav]]: el tráfico fluye de la autoridad al sujeto, y nunca al revés [^1].<!--/claim-->

<!--claim id=upstream-absent confidence=structural cites=[]-->Un sistema operativo Sujeto no tiene código para iniciar una relación de autoridad: ni cliente shell, ni tabla de enrutamiento entre pares. El control ascendente no lo bloquea una regla de firewall — el código para expresarlo no existe en el Sujeto.<!--/claim-->

Para un comprador regulado la consecuencia es concreta. Una categoría entera de brechas se elimina por estructura, y una flota compleja sigue siendo auditable porque cada conexión obedece una sola regla uniforme. Este artículo cubre la jerarquía de autoridad, las tres categorías de tráfico, la eliminación estructural del movimiento lateral y el adaptador que hace cumplir el estándar.

## La jerarquía

El Diodo es la topología fundacional de toda la familia de sistemas operativos — no una característica de un sistema, sino la ley que rige cómo todos se comunican.

| Posición | Sistema operativo | Privilegio |
|---|---|---|
| Autoridad | [[console-os|`os-console`]] y [[os-orchestration|`os-orchestration`]] | Emite comandos; recibe telemetría |
| Sujeto | [[totebox-os|`os-totebox`]], [[mediakit-os|`os-mediakit`]], [[os-privategit|`os-privategit`]], [[infrastructure-os|`os-infrastructure`]], [[os-network-admin|`os-network-admin`]] | Ejecuta comandos; emite telemetría; nunca origina un comando |

<!--claim id=no-lateral-route confidence=structural cites=[]-->Un Totebox no puede comandar a un MediaKit; un MediaKit no puede acceder a un Totebox. Un Sujeto comprometido no puede moverse lateralmente a otro Sujeto, porque la pila de protocolos no contiene lógica de enrutamiento para hacerlo.<!--/claim-->

## Las tres categorías de tráfico

| Tráfico | Dirección | Estado |
|---|---|---|
| Control descendente | Autoridad → Sujeto | Permitido: configuración, contenido, comandos, actualizaciones |
| Telemetría ascendente | Sujeto → Autoridad | Permitido pero estrictamente saneado: registros, latidos, estado |
| Control ascendente | Sujeto → Autoridad | Bloqueado estructuralmente: sin acceso shell, sin RPC, sin solicitudes de administración |

El control ascendente está bloqueado porque el Sujeto es estructuralmente incapaz de iniciar una relación de autoridad. La ausencia es el control.

## Por qué esto importa

El movimiento lateral — un atacante que compromete un nodo y lo usa para alcanzar nodos más valiosos — es el patrón dominante en los informes modernos de brechas [^2]. El Estándar del Diodo lo elimina estructuralmente.

| Escenario | Sin el Diodo | Con el Diodo |
|---|---|---|
| Un plugin en `os-mediakit` es comprometido | El atacante usa el túnel de gestión para llegar al `os-totebox` corporativo | El adaptador no tiene ruta ascendente; el atacante queda contenido en el host público |
| Un kiosko Totebox es físicamente comprometido | El atacante escanea la red local y pivota al MediaKit | El Totebox del kiosko no puede enrutar a otros Sujetos; es un callejón sin salida |
| `os-orchestration` es comprometido | El atacante tiene las claves de cada Totebox de la flota | `os-orchestration` no tiene claves de Totebox; solicita capacidades firmadas por consulta, así que un compromiso completo no proporciona material de descifrado |

## El adaptador

<!--claim id=hot-pluggable-adapter confidence=structural cites=[]-->El Diodo lo aplica un pequeño servicio conectable en caliente, [[service-pointsav-link|`service-pointsav-link`]] (el paquete `pointsav-protocol`). Es el único código que traduce comandos de autoridad en operaciones ejecutables por el Sujeto.<!--/claim-->

| Propiedad | Comportamiento |
|---|---|
| Estado predeterminado | No instalado; el Sujeto no tiene concepto de comunicarse con el exterior |
| Estado activado | Conectado en caliente por el operador con un solo comando; pone al Sujeto bajo gestión de flota |
| Modo de fallo | Si el adaptador falla, el enlace se corta limpiamente; el Sujeto continúa de forma autónoma; la superficie de gestión de flota queda oscura |
| Ruta del código | La política del Diodo vive dentro del adaptador, no en el kernel del SO — puede actualizarse sin tocar el resto del sistema |

## El estándar universal

<!--claim id=universal-standard confidence=structural cites=[]-->El Diodo no es una característica del [[mediakit-os|MediaKit]] ni del [[totebox-os|Totebox]]; se aplica de forma idéntica a cada sistema operativo `os-*`. El mismo paquete [[service-pointsav-link|`service-pointsav-link`]], con diferentes enlaces de política, se sitúa entre cualquier par de nodos que se comuniquen.<!--/claim-->

Este único estándar uniforme es la razón por la que una flota compleja sigue siendo auditable: cada conexión tiene el mismo aspecto y obedece las mismas reglas.

## Véase también

- [[os-family-overview]] — los ocho sistemas operativos que gobierna la topología del Diodo
- [[machine-based-auth]] — el sistema de autorización basado en hardware con el que trabaja el Diodo
- [[deployment-patterns]] — los patrones de implementación de flota que aplican la disciplina del Diodo
