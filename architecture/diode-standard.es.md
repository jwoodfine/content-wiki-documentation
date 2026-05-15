---
schema: foundry-doc-v1
title: "El Estándar del Diodo — Flujo de Comandos Unidireccional"
slug: diode-standard
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: diode-standard.md
short_description: "El Estándar del Diodo es la topología de seguridad fundacional de la familia PointSav — una disciplina de flujo de comandos unidireccional donde el tráfico se mueve de la autoridad al sujeto y nunca al revés, eliminando estructuralmente los ataques de movimiento lateral al suprimir la lógica de enrutamiento que los haría posibles."
cites: []
---

En ingeniería eléctrica, un diodo conduce corriente en una dirección y la bloquea en la otra. El Estándar del Diodo aplica el mismo principio a los comandos en toda la familia de sistemas operativos PointSav: el tráfico fluye de la autoridad al sujeto, y nunca al revés. Es la topología de seguridad fundacional de toda la familia — no una característica de un solo sistema operativo, sino la ley que rige cómo todos los sistemas operativos se comunican entre sí. Este artículo cubre la jerarquía de autoridad, las tres categorías de tráfico, la eliminación estructural del movimiento lateral y el adaptador que hace cumplir el estándar.

## La jerarquía

| Posición | Sistema operativo | Privilegio |
|---|---|---|
| Autoridad | `os-console` y `os-orchestration` | Emite comandos; recibe telemetría |
| Sujeto | `os-totebox`, `os-mediakit`, `os-privategit`, `os-infrastructure`, `os-network-admin` | Ejecuta comandos; emite telemetría; nunca origina un comando |

Un Totebox no puede comandar a un MediaKit. Un MediaKit no puede acceder a un Totebox. Un Sujeto comprometido no puede moverse lateralmente a otro Sujeto porque la pila de protocolos no contiene lógica de enrutamiento para hacerlo.

## Las tres categorías de tráfico

| Tráfico | Dirección | Estado |
|---|---|---|
| Control descendente | Autoridad → Sujeto | Permitido: configuración, contenido, comandos, actualizaciones |
| Telemetría ascendente | Sujeto → Autoridad | Permitido pero estrictamente saneado: registros, latidos, estado |
| Control ascendente | Sujeto → Autoridad | Bloqueado estructuralmente: sin acceso shell, sin RPC, sin solicitudes de administración |

El control ascendente no está bloqueado por una regla de firewall. Está bloqueado porque el código para expresarlo no existe en el Sujeto. No hay cliente `ssh`. No hay tabla de enrutamiento entre pares. El Sujeto es estructuralmente incapaz de iniciar una relación de autoridad.

## Por qué esto importa

La categoría de ataques llamada movimiento lateral — donde un atacante compromete un nodo y lo usa para alcanzar nodos más valiosos — es el patrón dominante en los informes modernos de brechas de seguridad. El Estándar del Diodo lo elimina estructuralmente.

| Escenario | Sin el Diodo | Con el Diodo |
|---|---|---|
| Un plugin en `os-mediakit` es comprometido | El atacante usa el túnel de gestión para llegar al `os-totebox` corporativo | El adaptador no tiene ruta ascendente; el atacante queda contenido en el host público |
| Un kiosko Totebox es físicamente comprometido | El atacante escanea la red local y pivota al MediaKit | El Totebox del kiosko no puede enrutar a otros Sujetos; es un callejón sin salida |
| `os-orchestration` es comprometido | El atacante tiene las claves de cada Totebox en la flota | `os-orchestration` no tiene claves de Totebox; solicita capacidades firmadas por consulta; un compromiso completo de Orchestration no proporciona material de descifrado de Totebox |

## El adaptador

El Diodo es aplicado por un pequeño servicio conectable en caliente llamado `service-pointsav-link` (el paquete `pointsav-protocol`). Este adaptador es el único código que sabe cómo traducir comandos de autoridad en operaciones ejecutables por el Sujeto.

| Propiedad | Comportamiento |
|---|---|
| Estado predeterminado | No instalado; el Sujeto no tiene concepto de comunicarse con el exterior |
| Estado activado | Conectado en caliente por el operador con un solo comando; pone al Sujeto bajo gestión de flota |
| Modo de fallo | Si el adaptador falla, el enlace se corta limpiamente; el Sujeto continúa funcionando de forma autónoma; la superficie de gestión de flota queda oscura |
| Ruta del código | La política del Diodo vive dentro del adaptador, no en el kernel del SO — la política puede actualizarse sin tocar el resto del sistema |

## El Estándar Universal

El Diodo no es una característica del MediaKit ni del Totebox. Se aplica de forma idéntica a cada sistema operativo `os-*`. El mismo paquete `service-pointsav-link`, con diferentes enlaces de política, se sitúa entre cualquier par de nodos que necesiten comunicarse. Este único estándar uniforme es la razón por la que una flota compleja sigue siendo auditable: cada conexión tiene el mismo aspecto y obedece las mismas reglas.

## Véase también

- [[os-family-overview]] — los ocho sistemas operativos que gobierna la topología del Diodo
- [[machine-based-auth]] — el sistema de autorización basado en máquinas con el que trabaja el Diodo
- [[deployment-patterns]] — los patrones de implementación de flota que aplican la disciplina del Diodo
