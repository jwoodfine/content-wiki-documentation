---
schema: foundry-doc-v1
title: "OS Network Admin"
slug: os-network-admin
short_description: "os-network-admin es el plano de control de una Red Privada PointSav — proporciona enrutamiento de malla WireGuard, la superficie de ceremonia de unión de nodos y la aplicación del Diode Standard, sin poseer ninguna autoridad criptográfica del nivel de archivo."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: os-network-admin.md
last_edited: 2026-05-30
editor: editorial
---

`os-network-admin` es el plano de control de una Red Privada PointSav (PPN). Se ejecuta en la máquina del administrador de red — típicamente en hardware físico en el sitio principal del operador, o dentro de un contenedor LXC en el nodo de flota local — y proporciona dos funciones: un sustrato de enrutamiento e integridad de túnel para la malla WireGuard, y una superficie de aprobación del operador para la ceremonia de unión de nodos.

## Posición en la pila

`os-network-admin` lleva el prefijo `os-`, que lo marca como un componente de la capa Foundation — por debajo de la capa de aplicación, proporcionando servicios a nivel de sistema sin lógica orientada al usuario. Es un complemento de Capa 1 para `os-console`, no uno de los tres sistemas operativos de nivel de archivo (`os-totebox`, `os-console`, `os-orchestration`).

| Componente | Capa | Rol |
|---|---|---|
| `os-totebox` | Nivel de archivo | Bóveda soberana de datos por entidad |
| `os-console` | Nivel de archivo | Terminal del operador orientada al teclado |
| `os-orchestration` | Nivel de archivo | Agregador de datos de múltiples archivos |
| `os-network-admin` | **Foundation** | Plano de control PPN + superficie de ceremonia |

Esta distinción es importante: `os-network-admin` no almacena ni procesa datos de negocio. No contiene claves de archivo, credenciales MBA ni cartuchos F-key. Es una capa de transporte segura y ciega para la infraestructura PPN — la entidad que gestiona qué nodos físicos están autorizados en la malla, no lo que se ejecuta en ellos.

## Qué hace

### Enrutamiento e integridad de túnel

`os-network-admin` establece y mantiene la malla WireGuard en la interfaz `ppn0`. Gestiona la distribución del mapa de pares, supervisa la actividad del túnel y aplica las reglas del Diodo que restringen qué nodos pueden enviar comandos a qué destinos. No inspecciona el contenido del tráfico que fluye a través de los túneles.

### Ceremonia de unión de nodos

Cuando un nuevo nodo físico quiere unirse a la malla PPN, genera un código corto en base32 de Crockford (ocho caracteres, aproximadamente 40 bits de entropía). El operador ingresa este código en `os-network-admin`. Un intercambio CPace PAKE establece una clave de sesión compartida a través del canal de código corto; una comparación de Cadena Corta Autenticada (SAS) cierra la brecha de intermediario. Bajo esta clave, el nodo que se une envía su clave pública WireGuard, recibe un certificado firmado por la CA del clúster y el mapa de pares se distribuye automáticamente.

La implementación mínima actual consulta el backend `service-ppn-pairing` en busca de solicitudes pendientes y las imprime en la salida estándar. La aprobación del operador se emite mediante curl:

```bash
PAIRING_SERVER=http://10.8.0.9:9202 ./os-network-admin

# Aprobar una unión pendiente desde otra terminal:
curl -s -X POST http://10.8.0.9:9202/v1/node-join/approve \
     -H 'Content-Type: application/json' \
     -d '{"code":"XXXX-XXXX"}'
```

Se planea una TUI completa controlada por teclado — con teclas de aprobación/denegación (`a`/`d`), visualización de código QR mediante `system-pairing-codes::qr_unicode` y cuenta regresiva de vencimiento — como superficie del operador de producción.

## Relación con app-network-admin

`app-network-admin` es la interfaz del Terminal F8 que se ejecuta sobre `os-network-admin`. Proporciona dos superficies:

- **Superficie de comandos HTTP** en el puerto 8085 — acepta la intención del operador en lenguaje natural, la enruta a través de `service-slm` para producir un comando autorizado y lo despacha a la malla
- **Transmisión UDP a la malla** en el puerto 8090 — envía cargas útiles binarias firmadas de 16 bytes a las direcciones de pares PPN

La división `os-` / `app-` sigue la convención de nomenclatura estándar Foundation/Aplicación: `os-network-admin` es el sustrato del SO; `app-network-admin` es la aplicación orientada al operador que se ejecuta sobre él.

## Relación con route-network-admin

`route-network-admin` es el nombre de instancia de despliegue para el nodo de administración de red en la flota del cliente. No es una base de código separada. Una entrada `route-network-admin-1` en un manifiesto de flota significa que un nodo físico en esa ubicación está ejecutando `os-network-admin` como su carga de trabajo principal.

## Hardware de destino

El hardware de referencia canónico es un iMac 12,1 (mediados de 2011) con un Intel Sandy Bridge i5-2400S y una NIC Broadcom 14e4:16b4. Esta máquina es especialmente adecuada como nodo de autoridad de comando: tiene VT-x de hardware real (para ejecutar VMs en la misma máquina si es necesario), una NIC Broadcom para la que `system-substrate-broadcom` proporciona el sustrato de detección de silicio, y una ubicación física estable en el sitio del operador.

Para despliegues donde dedicar hardware físico no es práctico, `os-network-admin` puede ejecutarse dentro de un contenedor LXC en el nodo de flota local, con la interfaz WireGuard puenteada desde el host.

## Autoridad criptográfica nula

`os-network-admin` no contiene F-keys, credenciales MBA ni capacidades de carga útil. No puede leer el contenido del estado interno de las VMs. No puede aprobar el acceso a archivos. Su función es conocer qué nodos físicos están en la malla y hacer cumplir esa membresía — nada más. Esta restricción arquitectónica es intencional: mantener el plano de control de red separado del plano de datos significa que una brecha en la capa de enrutamiento no otorga acceso a los contenidos del archivo.

## Disciplina del Diodo

Los comandos fluyen hacia abajo: `os-network-admin` → `os-infrastructure` (capa hipervisor) → VMs. Ninguna VM puede emitir comandos de regreso a `os-network-admin`. Ningún archivo puede instruir a la malla para agregar o eliminar un nodo. Esta disciplina unidireccional es el mismo Diode standard que rige el nivel de archivo (`os-console` → `os-orchestration` → `os-totebox`).

## Véase también

- [[sovereign-mesh]] — la superposición WireGuard y el protocolo de comando binario de 16 bytes
- [[genesis-protocol]] — la secuencia de arranque autónomo que ejecuta `os-network-admin` en un nodo nuevo
- [[machine-based-auth]] — el modelo de emparejamiento MBA que gobierna el acceso al nivel de archivo
- [[infrastructure-os]] — la capa de hipervisor Tipo I que gestiona `os-network-admin`
- [[diode-standard]] — la jerarquía de autoridad y las reglas de tráfico que aplica el plano de control
