---
schema: foundry-doc-v1
title: "os-infrastructure — El sustrato de cómputo"
slug: infrastructure-os
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: infrastructure-os.md
short_description: "os-infrastructure es el sustrato de cómputo que aloja los sistemas operativos PointSav en hardware propio, arrendado y en la nube. Crea la Red Privada PointSav y arranca flotas aisladas mediante el Protocolo Génesis."
cites: []
---

`os-infrastructure` es el sustrato de cómputo que aloja los demás sistemas operativos de PointSav. Una instancia se ejecuta en una pieza de hardware — un servidor bare-metal en una oficina, un rack colocado o una máquina virtual en la nube. Tomado en conjunto, una flota de nodos `os-infrastructure` forma la Red Privada PointSav (PPN): una malla cifrada WireGuard que conecta Toteboxes, Consolas, MediaKits e instancias PrivateGit sin exponer ningún nodo a internet público. Este artículo cubre los tres modos de despliegue, el Protocolo Génesis que arranca una flota y la brecha estructural en las ofertas convencionales de nube que el diseño explota.

## Los tres modos de despliegue

`os-infrastructure` es el mismo SO en tres configuraciones. El operador elige dónde vive su cómputo — y puede combinar cualquier combinación en una sola flota:

| Superficie de aplicación | Hardware | Perfil de confianza |
|---|---|---|
| `app-infrastructure-onprem` | Servidores en las instalaciones propias del operador | Mayor confianza; el operador posee y puede verificar físicamente el hardware |
| `app-infrastructure-leased` | Bare-metal colocado en un centro de datos externo | Confianza híbrida; el operador controla el SO pero no puede verificar físicamente cada arranque |
| `app-infrastructure-cloud` | VMs de hiperscaler (GCP, AWS, Azure) | Menor confianza; se usa para retransmisión perimetral sin estado, no para almacenamiento persistente |

La misma malla WireGuard se ejecuta en las tres configuraciones. Un operador puede comenzar con un único nodo de retransmisión en la nube y agregar nodos propios más adelante sin reestructurar el software.

## El Protocolo Génesis

La gestión de flotas convencional requiere que exista un plano de control antes de que cualquier nodo de cómputo pueda unirse. `os-infrastructure` invierte esto. Cuando un nodo arranca y no encuentra un beacon de PPN, no falla — se declara a sí mismo una Red Privada de uno.

1. **Arranque ciego.** El nodo ignora las convenciones de DHCP y DNS. El núcleo seL4 genera un par de claves fiduciarias de Nivel 1 en el primer arranque.
2. **Exploración.** El nodo busca un beacon de `os-network-admin` en la malla local.
3. **Bifurcación génesis.** Si nada responde, el nodo crea su propia PPN de un nodo y sella todos los puertos externos excepto uno.
4. **Patrón de espera.** Un único endpoint WebSocket reforzado espera una solicitud de reclamación administrativa.
5. **Reclamación.** Cuando un administrador arranca `os-network-admin` y presenta la clave fiduciaria administrativa, el nodo verifica la reclamación, se vincula a la flota y se une a la malla.

Un cliente puede enviar cincuenta servidores a cincuenta ubicaciones remotas. Cada uno arranca, forma una PPN de un nodo y espera. Cuando el administrador está listo, el `os-network-admin` central los reclama a todos, fusionándolos en una sola flota global. Los nodos no necesitan saber de antemano cuántos hermanos tendrán eventualmente.

## La Red Privada PointSav

Cada nodo `os-infrastructure` es miembro de la PPN — la superposición WireGuard que conecta todos los dispositivos PointSav en una flota:

- Transferencia de datos cifrada: Las imágenes de archivo Totebox se mueven entre ubicaciones sin tocar internet público.
- Señalización lingüística: `os-network-admin` transmite comandos binarios de 16 bytes a través de la malla; cada nodo recibe simultáneamente, solo el nodo destinatario actúa.
- Administración remota: `os-console` se empareja con instancias de `os-totebox` a través de la PPN sin requerir un cliente VPN en la máquina anfitriona del operador.

## La Brecha del Hiperscaler

La arquitectura explota deliberadamente una brecha estructural en las ofertas convencionales de nube:

| Nube convencional | os-infrastructure |
|---|---|
| Acopla el cómputo a almacenamiento propietario; cobra por la salida de datos | Trata la nube como retransmisión sin estado; el almacenamiento persistente permanece en el hardware del operador |
| Provee acceso de alquiler; niega la propiedad custodial | El operador puede desconectar físicamente y mover el sustrato |
| Requiere ingeniería de red antes de agregar cómputo | Los nodos se auto-arrancan mediante el Protocolo Génesis |
| Plano de control de un único proveedor como punto único de fallo | Cada nodo `os-infrastructure` puede iniciar una flota de forma independiente |

Un operador con `os-infrastructure` en un servidor en su oficina, un nodo de retransmisión en la nube para conectividad pública y `os-network-admin` en una estación de trabajo administrativa ha construido una flota que no está bloqueada a ningún hiperscaler y es inaccesible para atacantes externos sin una clave fiduciaria válida.

## Véase también

- [[os-network-admin]] — el plano de control que comanda las flotas `os-infrastructure`
- [[os-family-overview]] — la familia completa de ocho SO y cómo encaja cada miembro
- [[totebox-os]] — el SO de archivo alojado en los nodos `os-infrastructure`
- [[diode-standard]] — el protocolo que rige el flujo de comandos entre nodos
- [[machine-based-auth]] — cómo los pares de claves fiduciarias aseguran la membresía en la flota
- [[deployment-patterns]] — las seis configuraciones de flota canónicas
