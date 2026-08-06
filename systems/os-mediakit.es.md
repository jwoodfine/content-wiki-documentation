---
schema: foundry-doc-v1
content_type: topic
title: "OS Mediakit"
slug: os-mediakit
short_description: "El nivel web público de la familia de SO PointSav — os-mediakit posee TLS, el ciclo de vida systemd y el acceso a datos mediado por la puerta de enlace; app-mediakit-knowledge/marketing/distribution poseen la lógica de dominio. Ubuntu 24.04 hoy; el estado final previsto es una VM seL4 por instancia de despliegue, no un dispositivo combinado único."
category: systems
index_group: publishing-and-media
last_edited: 2026-08-06
editor: pointsav-engineering
status: stable
bcsc_class: no-disclosure-implication
---

**os-mediakit** es la imagen del sistema operativo invitado para el nivel de VM
`vm-mediakit` en la capa del hipervisor de la Red Privada PointSav. Aísla la superficie
de servicio MediaKit — wikis de conocimiento, sitios de marketing y flujos de
cumplimiento/distribución — del almacén de fuentes y los niveles de orquestación.

## Frontera entre SO y aplicaciones

`os-mediakit` (el sistema operativo) y `app-mediakit-*` (las aplicaciones que aloja)
tienen una división fija de responsabilidades, ratificada como parte de las
definiciones de nivel de la familia de SO.

`os-mediakit` proporciona: terminación TLS (nginx y certbot), ciclo de vida de
unidades systemd, el diseño de sistema de archivos por inquilino, la rotación de
registros con reenvío al libro mayor WORM, el emparejamiento MBA con la puerta de
enlace de la flota, el arranque TLS del cliente Doorman, la limitación de tasa y el
servicio de activos estáticos.

`app-mediakit-*` proporciona: lógica de dominio — renderizado de páginas, búsqueda,
verificación de pagos, consultas de taxonomía, la interfaz editorial, la resolución
de wikilinks y la emisión de licencias. Cada binario `app-mediakit-*` es un inquilino
del SO, no parte de él.

## Despliegues y flujo de datos

Cada instancia `app-mediakit-*` alcanza los datos de Totebox únicamente a través de la
puerta de enlace de la flota — `media-* → MBA saliente → gateway-orchestration-command-1
→ auditoría Doorman → cluster-totebox-*`. **Ningún proceso `app-mediakit-*` lee el
almacenamiento de Totebox directamente**; la puerta de enlace es el único punto de
cruce, y cada lectura queda registrada en el libro de auditoría a su paso.

| Instancia | Binario | Superficie | Estado |
|---|---|---|---|
| `media-knowledge-documentation-1` | app-mediakit-knowledge | documentation.pointsav.com | Activo |
| `media-knowledge-projects-1` | app-mediakit-knowledge | projects.woodfinegroup.com | Activo |
| `media-marketing-landing-1` | app-mediakit-marketing | home.woodfinegroup.com | Activo |
| `media-marketing-landing-2` | app-mediakit-marketing | home.pointsav.com | Activo |
| `media-intranet-1` | nginx (sin binario de aplicación) | Vista previa interna solo por VPN de lo anterior | Activo, restringido a WireGuard |
| `media-knowledge-corporate-1` | app-mediakit-knowledge | corporate.woodfinegroup.com | Aún no desplegado |
| `media-distribution-*` | app-mediakit-distribution | Flujo de comunicados/cumplimiento | Aún no desplegado |

Dos cosas que conviene decir con claridad en lugar de suavizar. Primero, el
emparejamiento MBA con la puerta de enlace de la flota del que depende este modelo de
flujo de datos no está aún conectado para ninguna instancia `media-*` hoy — cada una
accede a su contenido localmente en lugar de a través de la puerta de enlace, una
brecha conocida y registrada. Segundo, `software.pointsav.com` — asociado a veces con
`app-mediakit-distribution` en la planificación temprana — en la práctica es servido
por los binarios independientes `app-privategit-marketplace`/`app-privategit-source`;
ninguna instancia de `app-mediakit-distribution` está desplegada allí hoy.

## Posición en la arquitectura

Las cuatro capas del stack Totebox ubican os-mediakit en la **capa del hipervisor**:

```
Operador
  ↓
PPN (malla WireGuard, plano de control os-network-admin)
  ↓
Capa del hipervisor  ←— el SO invitado os-mediakit se ejecuta aquí
  ↓
Orquestación Totebox (app-mediakit-*, service-fs, system-core)
```

os-mediakit es uno de los tres invitados en el esquema de tres VMs:

| VM | SO invitado | Nivel |
|---|---|---|
| vm-workspace | SO anfitrión (Linux) | os-privategit (anfitrión permanente) |
| vm-intelligence | os-intelligence (previsto) | os-totebox + inferencia |
| vm-mediakit | **os-mediakit** | os-mediakit |

---

## Fase 1: Ubuntu 24.04 provisional (presente)

El primer despliegue de vm-mediakit utiliza una imagen **Ubuntu 24.04 server cloud x86_64 QCOW2**
como SO invitado. Esta es la implementación provisional de producción mientras se desarrollan
las VMs seL4 por instancia.

Ubuntu 24.04 es obligatorio — no Debian 12 — porque todos los binarios de servicio compilados
en el anfitrión GCP (Ubuntu 24.04, glibc 2.39) dependen de los símbolos `GLIBC_2.39`. Debian 12
solo proporciona glibc 2.36 y no puede ejecutar los binarios.

Lo que está en funcionamiento actualmente:
- Ubuntu 24.04 arrancado mediante `provision-vm-mediakit.sh` bajo QEMU/TCG
- 6 GiB de RAM, disco QCOW2 de 20 GB
- Red NAT de modo usuario: reenvíos de puerto anfitrión `1xxxx → :xxxx` por cada servicio
- Dispositivo `virtio-balloon`: ajuste dinámico de RAM sin reinicio del invitado
- Primer arranque cloud-init: nombre de host `vm-mediakit`, usuario `foundry`, systemd nativo
- nginx/1.24.0 y build-essential instalados tras el arranque

Servicios dentro del invitado Ubuntu 24.04 (estado Fase 1, 2026-05-29):

| Servicio | Puerto | Propósito | Estado Fase 1 |
|---|---|---|---|
| local-proofreader | 9092 | Servicio de corrección de pruebas | ✓ activo |
| local-knowledge-documentation | 9090 | Wiki de documentación | ✓ activo |
| local-knowledge-corporate | 9095 | Wiki corporativa | ✓ activo |
| local-knowledge-projects | 9093 | Wiki de proyectos | ✓ activo |
| local-marketing-pointsav | 9101 | Sitio de marketing PointSav | ✓ activo |
| local-marketing | 9102 | Sitio de marketing Woodfine | ✓ activo |
| service-fs | 9100 | Registro WORM — columna vertebral de datos | pendiente (build project-data) |
| local-bim-orchestration | 9096 | Puerta de enlace BIM | pendiente (depende de service-fs) |
| system-core | — | Substrato del Registro de Capacidades | pendiente (project-system) |
| system-ledger | — | Máquina de estado del registro | pendiente (project-system) |

---

## Fase 3: una VM seL4 por instancia de despliegue (prevista)

La topología moonshot ratificada para la familia de SO no empaqueta `os-mediakit`
como un único dispositivo seL4 combinado, a diferencia de cómo `os-orchestration`
consolidó Command y SLM en un solo invitado. En cambio, cada **instancia de
despliegue** `app-mediakit-*` — no cada tipo de servicio — obtiene su propia VM
seL4/Microkit dedicada, usando el mismo patrón de invitado Linux Microkit-más-
`vendor-libvmm` ya probado para `os-totebox`.

| VM prevista | Aloja |
|---|---|
| `mediakit-knowledge-vm-1` | `media-knowledge-documentation-1` (documentation.pointsav.com) |
| `mediakit-knowledge-vm-2` | `media-knowledge-projects-1` (projects.woodfinegroup.com) |
| `mediakit-knowledge-vm-3` | `media-knowledge-corporate-1` (corporate.woodfinegroup.com, aún no desplegado) |
| `mediakit-marketing-vm` | las instancias de páginas de aterrizaje de marketing |
| `mediakit-dist-vm` | la instancia de distribución/flujo de cumplimiento, una vez construida |

La justificación es la misma que las tres instancias independientes de
`os-privategit` (bóveda de fuentes, distribución de software, activos de diseño):
distintas superficies públicas conllevan distintos perfiles de ataque, y el
compromiso de una instancia de wiki no debería poner en riesgo el espacio de
proceso de una instancia hermana. Se trata de un hito planificado, aún no iniciado
— ninguna VM `os-mediakit`, combinada o por instancia, se ejecuta bajo seL4 hoy.

---

## Qué cambia respecto a la Fase 1 y qué permanece igual

| Propiedad | Ubuntu 24.04 (Fase 1, hoy) | VMs seL4 por instancia (Fase 3, prevista) |
|---|---|---|
| SO invitado | Ubuntu 24.04 Linux 6.x (glibc 2.39), un invitado para todas las instancias co-inquilinas | Micronúcleo seL4, un invitado por instancia de despliegue |
| Anfitrión | QEMU/TCG (x86_64) | QEMU/KVM o bare metal AArch64 |
| Binarios de servicio | Los mismos (compilación cruzada) | Los mismos, recompilados para el invitado seL4 objetivo |
| Frontera de aislamiento | Separación de proceso/sistema de archivos dentro de un invitado compartido | Una frontera de VM completa por instancia |
| Números de puerto | Los mismos (9090, 9093, 9095, ...) | Los mismos, accesibles a través de la malla PPN |
| virtio-balloon | Presente | Presente (capa del hipervisor sin cambios) |
| Custodia de claves | Permisos de archivos del SO | Material de clave por VM, sin invitado compartido que comprometer |

---

## Relación con os-infrastructure y el Genesis Protocol

`os-infrastructure` es la capa de arranque del hipervisor — ejecuta el Genesis Protocol
en el anfitrión físico para establecer la identidad WireGuard del nodo PPN. os-mediakit
es un *invitado* que se ejecuta sobre os-infrastructure. Son capas y binarios diferentes.

La secuencia de primer arranque del Genesis Protocol se aplica al **nodo anfitrión**
(os-infrastructure), no al invitado (os-mediakit). Un nuevo invitado vm-mediakit se une
a la malla mediante la ceremonia de emparejamiento MBA después de que el nodo anfitrión
ya es miembro del PPN.

---

## Véase también

- [[ppn-hypervisor-resource-pool]] — cómo virtio-balloon gestiona la RAM para vm-mediakit
- [[totebox-archive]] — qué hace el nivel Totebox Archive sobre el SO invitado
- [[os-network-admin]] — el plano de control PPN; vm-mediakit se une a la malla a través de él
- [[os-family-overview|Visión general de la familia de SO]] — la familia completa de SO PointSav
