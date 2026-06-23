---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: worm-ledger-architecture
title: "Substrato WORM — arquitectura del ledger inmutable de cuatro capas y dos sobres de arranque"
short_description: "El ledger inmutable WORM por tenant al que escriben todos los servicios de ingestión del Anillo 1, construido sobre tiles C2SP con encadenamiento criptográfico de hashes, anclaje mensual a Sigstore Rekor y un diseño de doble sobre que abarca daemon Linux y unikernel seL4."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: worm-ledger-architecture.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---

`service-fs` es el ledger inmutable WORM (Write-Once-Read-Many) por tenant al que llegan primero todos los datos de cara al cliente. Todos los servicios de ingestión de frontera del [[three-ring-architecture|Anillo 1]] — el ledger de identidad (`service-people`), el ledger de comunicaciones (`service-email`), el servicio de ingestión de documentos (`service-input`) — escriben a través de él. Todos los servicios de extracción de conocimiento del Anillo 2 leen de él mediante consultas MCP paginadas por cursor. Existe exactamente un proceso `service-fs` por tenant `moduleId`; el acceso entre tenants es estructuralmente imposible.

Este artículo describe la arquitectura de cuatro capas, los dos sobres operativos (daemon Linux/BSD hoy; unikernel seL4 Microkit como objetivo previsto a largo plazo), la alineación con normas WORM externas nombradas, y cómo la Invención de Doctrina #7 — el anclaje mensual a Sigstore Rekor — cierra el ciclo de verificabilidad pública.

## Posición en el sistema

`service-fs` se sitúa en la frontera entre el plano de datos por tenant y el plano de conocimiento multitenant. La convención [[three-ring-architecture]] nombra esta posición explícitamente: los servicios del Anillo 1 son procesos MCP-server por tenant; el ledger WORM es el eje durable que comparten dentro de un tenant.

```
                    Anillo 2 (multitenant vía moduleId)
                    service-extraction (lector)
                              ▲
                              │ lectura MCP (paginada por cursor)
                              │
              ┌───────────────┴───────────────┐
              │     service-fs                 │
              │     Ledger inmutable WORM      │
              │     por tenant moduleId        │
              └───────────────▲───────────────┘
                              │ adición MCP
              ┌───────────────┼───────────────┐
              │               │               │
       service-people  service-input    service-email
       (Anillo 1)      (Anillo 1)       (Anillo 1)
```

**Frontera por tenant actual:** un proceso daemon por `moduleId` (espacios de direcciones de proceso separados); permisos de sistema de archivos que restringen el acceso por tenant a `FS_LEDGER_ROOT`; comprobación en tiempo de solicitud del encabezado `X-Foundry-Module-ID` que rechaza con 403 a los llamantes con discrepancia.

**Frontera prevista a largo plazo:** cumplimiento de capacidades a nivel del microkernel seL4, verificado formalmente según la trayectoria del sustrato moonshot kernel.

## La pila de cuatro capas

La arquitectura está diseñada en capas de forma intencionada para que cada capa sea intercambiable de forma independiente. La capa intermedia (L2) es el contrato durable del trait de Rust que sobrevive a los cambios por encima y por debajo de ella. El patrón de cuatro capas a nivel de sustrato está regido por la convención de diseño del ledger WORM del workspace (ratificada en workspace v0.1.7, commit `6c0b79a`); este artículo describe cómo `service-fs` lo aplica específicamente.

### L1 — Primitiva de almacenamiento de tiles (específica del sobre)

El formato en disco son los **tiles C2SP tlog-tiles** — el mismo formato usado por RFC 9162 v2 (Certificate Transparency v2), Trillian-Tessera y Sigstore Rekor v2. Los tiles son archivos de texto estáticos que contienen 256 entradas (o 256 hashes en niveles Merkle intermedios), codificados en base64 para inspección en texto plano según el principio DARP (directo, auditable, reproducible, texto plano).

Disposición concreta en disco por tenant:

```
$FS_LEDGER_ROOT/<moduleId>/
├── checkpoint            — cabeza de árbol firmada más reciente (formato signed-note)
├── tile/0/x000.b64       — tile de hoja 0, entradas 0–255
├── tile/0/x001.b64       — tile de hoja 1, entradas 256–511
├── tile/1/x000.b64       — tile de altura 1, hashes que cubren 256 hojas cada uno
├── tile/2/x000.b64       — tile de altura 2, hashes que cubren 65.536 hojas cada uno
└── audit-log/
    ├── checkpoint        — sub-ledger separado para eventos de lectura ADR-07
    └── tile/0/x000.b64
```

La implementación L1 actual es `PosixTileLedger`: archivos POSIX bajo `FS_LEDGER_ROOT`, escritura atómica-luego-renombrado por tile, fsync tras cada tile y cada checkpoint, tiles finalizados marcados como solo lectura (modo `0o444`). El reemplazo previsto a largo plazo es `MoonshotDatabaseLedger` sobre IPC mediado por capacidades al sustrato `moonshot-database`. Los bytes son idénticos en ambas implementaciones — solo difiere el mecanismo de E/S.

### L2 — API del ledger WORM (trait de Rust, independiente del objetivo)

El trait de Rust `LedgerBackend` es el contrato durable de la API. Superficie actual: `open` / `append` / `read_since` / `root` / `checkpoint` / `verify_inclusion` / `verify_consistency`. El invariante de solo adición vive en la superficie de la API — ningún método público elimina ni modifica una entrada. Un sub-ledger de auditoría para el seguimiento de lecturas ADR-07 se ejecuta detrás del mismo trait (un trait, dos instancias por tenant).

Existen dos implementaciones hoy: `InMemoryLedger` (dispositivo de prueba) y `PosixTileLedger` (producción). Ambas pasan un conjunto idéntico de 18 pruebas sobre la superficie del trait. Las implementaciones futuras se incorporan detrás del mismo trait sin modificar la capa de cable ni el código de arranque.

### L3 — Protocolo de cable (por tenant, consciente de MCP)

Hoy: rutas HTTP axum 0.7 — `GET /healthz`, `GET /readyz`, `GET /v1/contract`, `POST /v1/append`, `GET /v1/entries?since=N`, `GET /v1/checkpoint`, `POST /mcp` para la interfaz MCP-server. La aplicación del encabezado `X-Foundry-Module-ID` se ejecuta antes de cualquier manejador de negocio; una discrepancia devuelve 403 con el moduleId esperado frente al recibido en el cuerpo de la respuesta. La misma forma de cable sirve a ambos sobres de arranque.

La evolución prevista a largo plazo añade una interfaz MCP-server más completa: recursos MCP para `/v1/checkpoint` y lecturas por tile; herramientas MCP para `/v1/append`. Está previsto que ambas superficies de cable (HTTP y MCP) coexistan, de modo que los clientes puedan usar la que mejor encaje en su patrón de integración.

### L4 — Anclaje (a nivel de workspace, mensual)

La Invención de Doctrina #7 especifica el anclaje a Sigstore Rekor v2 de los checkpoints por tenant. Un cron mensual agrupa el checkpoint firmado más reciente de cada tenant, lo envía al endpoint GA de Rekor v2 (fragmentado por año; la URL rota anualmente) y escribe la entrada tlog devuelta de vuelta en el ledger del tenant de origen como payload `anchor-rekor-<unix-ts>`. El flujo de anclaje es independiente del trabajo en tiempo de solicitud — el daemon no tiene estado respecto al anclaje; produce checkpoints firmados que consume la ejecución de anclaje del workspace.

La implementación (`service-fs/anchor-emitter/`) es un binario Rust autónomo (su propio `[workspace]` para evitar conflictos de openssl-sys en el monorepo principal). Usa `reqwest` bloqueante con rustls-tls (sin tokio en este binario), genera un par de claves Ed25519 efímero por anclaje y finaliza con códigos estructurados (0 éxito / 1 configuración / 2 obtención / 3 Rekor / 4 adición). La unidad systemd (`local-fs-anchor.{service,timer}`) está configurada con `OnCalendar=*-*-01 02:30:00`, `Persistent=true`, `RandomizedDelaySec=900`.

## Los dos sobres de arranque

`service-fs` está previsto para distribuirse en dos sobres que comparten el mismo protocolo de cable y el mismo formato de almacenamiento.

### Sobre A — daemon Linux/BSD bajo systemd (actual)

Runtime asíncrono Tokio, servidor HTTP axum 0.7, Rust std. Almacenamiento POSIX en `FS_LEDGER_ROOT/<moduleId>/`. Frontera por tenant mediante espacios de direcciones de proceso separados, permisos de sistema de archivos y la comprobación de encabezado en la capa de cable. Se despliega como unidad systemd (`infrastructure/local-fs/local-fs.service`). Funciona en cualquier kernel Linux o BSD — la VM del workspace de Foundry, hardware local del cliente, cómputo en la nube, o dentro de una VM Linux/BSD alojada por seL4 en hardware donde seL4 no puede arrancar de forma nativa.

### Sobre B — unikernel seL4 Microkit Protection Domain (previsto)

Crate de runtime Rust `sel4-microkit` (según Microkit 1.3.0, reescrito de Python a Rust). Almacenamiento: IPC mediado por capacidades a `moonshot-database`. Los tokens de capacidad se conceden por tenant; el acceso entre tenants requiere una transferencia explícita de capacidades — verificación formal, no una comprobación de encabezado. Un System Description File declara las asignaciones de capacidades del Protection Domain y los canales IPC por tenant.

El caso de envoltura Linux/BSD es un patrón de infraestructura de producción real, no una alternativa degradada: `libsel4vm` + `libsel4vmmplatsupport` + CAmkES VMM aloja una VM Linux/BSD invitada donde el código del Sobre A se ejecuta sin cambios, mientras el hipervisor seL4 proporciona aislamiento verificado alrededor de la VM invitada.

### Portabilidad entre sobres

El protocolo de cable es idéntico entre sobres. El formato de almacenamiento es idéntico. Solo difieren el sobre de runtime y el mecanismo de E/S de almacenamiento. La migración del Sobre A al Sobre B es un intercambio de runtime, no una migración de formato de datos — cada tile creado bajo almacenamiento POSIX es bit a bit idéntico a uno creado bajo IPC mediado por capacidades de `moonshot-database`.

## Formato de checkpoint — signed-note C2SP

El formato signed-note C2SP se adopta textualmente — el mismo formato usado por Sigstore Rekor v2. Un checkpoint es un pequeño artefacto de texto:

```
service-fs.foundry.example
17                                                <-- tamaño del árbol
HQC1ZP2bbV3Hr1cI4aXxFQ8vQwG4sQYwR0uW4cEAhvA=     <-- hash raíz (base64 SHA-256)

— foundry-tenant-foundry signed-note-key-id Wm8s...   <-- firma
```

Firmado por la clave del tenant (hoy: clave del administrador del workspace; previsto a largo plazo: clave de identidad por Totebox vinculada al hardware del cliente). Los testigos co-firman añadiendo líneas de firma adicionales — el workspace de Foundry co-firma de forma predeterminada cada checkpoint del Totebox del cliente; un tercero elegido por el cliente puede co-firmar adicionalmente.

El formato signed-note es texto plano y orientado a líneas. La verificación de la firma solo requiere Ed25519 (o un equivalente post-cuántico futuro) — sin cadena de herramientas propietaria.

## Flujo de escritura

1. El cliente hace `POST /v1/append` con el payload y el encabezado `X-Foundry-Module-ID` (y opcionalmente `X-Foundry-Request-ID`).
2. El servidor valida el moduleId contra la variable de entorno `FS_MODULE_ID`; rechaza con 403 en caso de discrepancia.
3. El servidor genera un número de secuencia monótono (cursor) y lo añade al búfer pendiente en memoria.
4. El secuenciador agrupa las entradas pendientes (cada N ms o M entradas — ajustable por perfil de carga del tenant).
5. Al finalizar el lote: escribe los bytes del tile de hoja (escritura atómica-luego-renombrado y `fsync`); si se cruza un límite de tile, calcula y escribe los tiles intermedios recién completados; firma y escribe atómicamente un nuevo checkpoint.
6. Devuelve el cursor y la firma del checkpoint al cliente.

El invariante de solo adición se aplica en tres niveles:

- **Superficie de la API de Rust** — ningún método público de `LedgerBackend` elimina ni modifica una entrada.
- **Nivel de sistema de archivos** — los tiles finalizados se marcan como solo lectura (`0o444`); hardening futuro mediante `chattr +i` cuando la unidad systemd esté instalada y el operador pueda conceder `CAP_LINUX_IMMUTABLE`.
- **Nivel criptográfico** — la cadena de hashes Merkle detecta cualquier modificación retroactiva; las pruebas de consistencia contra un checkpoint anclado en Rekor fallan públicamente si se altera el historial.

## Flujo de lectura (llamantes del Anillo 2)

1. El cliente hace `GET /v1/checkpoint` — obtiene la cabeza de árbol firmada más reciente.
2. El cliente hace `GET /v1/tile/0/xNNN.b64` — obtiene los tiles de hoja específicos para el rango de cursores de interés.
3. El cliente calcula la prueba de inclusión localmente a partir de los tiles intermedios. Sin búsqueda en base de datos en el servidor; los tiles son almacenables en caché por CDN; la verificación es independiente del daemon.
4. El servidor registra el intento de lectura en el sub-ledger `audit-log/`.

El esqueleto actual también implementa `GET /v1/entries?since=N` como un envoltorio de conveniencia que devuelve las entradas directamente sin cálculo de prueba a nivel de tile en el cliente. Esta forma es transitoria, adecuada para el backend de marcador de posición en memoria; la implementación post-ratificación añade endpoints de nivel de tile junto a este.

## Sub-ledger de auditoría ADR-07

Cada lectura produce una adición a `audit-log/` (su propio sub-árbol de tiles, separado del ledger de datos). Cada entrada de auditoría es JSON: moduleId, request-id, cursor since, entradas devueltas, marca de tiempo.

El sub-ledger es en sí mismo WORM — los auditores pueden verificar retroactivamente que el registro de auditoría no ha sido manipulado. El checkpoint del sub-ledger se ancla junto con el checkpoint del ledger de datos en el paquete mensual de Rekor. Esto satisface SOC 2 PI4 (Integridad del procesamiento — Salidas) y el requisito de que las lecturas de material sean externamente demostrables.

## Agilidad criptográfica

La función hash y el esquema de firma son ágiles en cuanto a algoritmos para admitir migración futura sin reformatear los tiles:

- **Hoy:** hashes SHA-256, firmas Ed25519.
- **Ruta de migración de hash:** familia SHA-3 o BLAKE3 — el formato de checkpoint incluye un identificador de algoritmo; los nuevos tiles usan el nuevo hash; los checkpoints registran ambos algoritmos durante el periodo de transición.
- **Ruta de migración de firma:** candidatos post-cuánticos (NIST PQC Dilithium o SPHINCS+) — mismo formato signed-note con firmas etiquetadas por algoritmo.

Este diseño aborda el requisito de preservación cualificada de eIDAS de que la prueba de existencia sobreviva independientemente de los cambios tecnológicos futuros (Artículo 4(3), Reglamento de Ejecución de la Comisión (UE) 2025/1946) y el objetivo de la plataforma de legibilidad durante 100 años para cada artefacto del ledger.

## Arranque de un nuevo tenant

El directorio por tenant `FS_LEDGER_ROOT/<moduleId>/` se crea en el primer `open()`:

1. Verificar que el directorio está vacío o contiene un estado previo válido.
2. Inicializar un tile de hoja vacío y un checkpoint en tamaño de árbol 0, firmado por la clave del tenant.
3. Al recargar (llamadas `open()` posteriores): leer el checkpoint más reciente, validar la firma, recorrer los tiles hacia atrás para recomputar la raíz y negarse a iniciar si la raíz recomputada no coincide con la raíz firmada.

La detección de cadena manipulada es un modo de fallo severo. El daemon se niega a iniciar, expone la discrepancia al operador y espera intervención manual. Reinicializar silenciosamente un ledger manipulado anularía la propiedad WORM; este modo de fallo es intencional.

## Alineación con normas WORM externas

`service-fs` está estructuralmente alineado con dos normas WORM externas nombradas, además de la postura interna SOC 2 y DARP:

- **SEC Rule 17a-4(f)** (registro electrónico de corredores-agentes estadounidenses; 17 CFR §240.17a-4(f); la enmienda de 2022 en vigor desde el 03-05-2023 añadió una alternativa de Pista de Auditoría al WORM). La plataforma apunta a la vía WORM. El cumplimiento es estructural: el sustrato de almacenamiento deniega la modificación mediante la inmutabilidad de la cadena de hashes criptográficos y la aplicación de escritura única a nivel de sistema de archivos, no mediante política ni proceso.

- **Servicio cualificado de preservación de eIDAS** (Reglamento de Ejecución de la Comisión (UE) 2025/1946 en vigor desde el 06-01-2026; ETSI TS 119 511; ETSI EN 319 401 v3.2.1; CEN TS 18170:2025). El formato de texto plano de tiles C2SP tlog-tiles y el diseño de agilidad de algoritmos abordan el requisito del Artículo 4(3) de que la prueba de existencia sobreviva independientemente de los cambios tecnológicos futuros.

Ninguna norma requiere certificación formal hoy. El diseño está listo para alineación; una auditoría futura o una designación como proveedor de servicios cualificados es un elemento de la trayectoria v1.0.0+ prevista, condicionada a la demanda de los clientes y la postura corporativa.

La distinción estructural-frente-a-política es importante. Una propiedad WORM mantenida por política es rebatible. Una propiedad WORM mantenida por estructura — donde los bytes no pueden modificarse sin romper una firma de checkpoint publicada — es verificable por cualquier tercero. El enfoque estructural se compone: cada cliente que ejecuta el mismo sustrato hereda la misma propiedad sin tener que confiar en ninguna promesa hecha por el operador de la plataforma.

## Lo que WORM garantiza — y lo que no garantiza

**La garantía WORM cubre (actual):**
- **Inmutabilidad tras la escritura.** Un registro escrito en el ledger no puede ser modificado ni eliminado por ningún actor, incluida la propia plataforma. Esto es estructural, no de política.
- **Evidencia de manipulación a nivel de registro.** Cada registro añadido lleva un resumen SHA-256 por payload. La modificación de cualquier registro almacenado es detectable recomputando el resumen.

**La garantía WORM está diseñada para cubrir (implementación actual del formato de tiles):**
- **Evidencia de manipulación a nivel de cadena.** Un auditor con los archivos de tiles C2SP y una implementación de SHA-256 puede verificar la cadena de hashes completa sin un servicio activo.
- **Verificabilidad externa.** El anclaje mensual a Sigstore Rekor crea una cadena de marcas de tiempo pública que persiste independientemente de la instancia de la plataforma.
- **Legibilidad a lo largo de décadas.** El formato de texto plano de tiles C2SP tlog-tiles solo requiere utilidades Unix básicas para decodificarse. No se necesita ninguna herramienta propietaria.

**La garantía WORM no cubre:**
- **La corrección de lo que se escribió.** WORM no puede detectar ni evitar que un registro incorrecto entre en el ledger. La corrección es responsabilidad del proceso de verificación con intervención humana en F12, no de la capa de almacenamiento.
- **La disponibilidad.** WORM garantiza la durabilidad; no garantiza que el ledger sea accesible en un momento dado. El tiempo de actividad es una preocupación de infraestructura.
- **El acceso por búsqueda o consulta.** El ledger almacena registros; no los indexa. La búsqueda de texto completo y las consultas de entidades las proporcionan [[service-search]] y [[service-content]].
- **El aislamiento entre tenants por encima de la capa de almacenamiento.** El invariante WORM es por tenant. El control de acceso entre tenants lo aplica el protocolo de cable (límites `X-Module-ID`) y está previsto que lo aplique la mediación de capacidades de seL4 en el Sobre B.

## Trayectoria a largo plazo

El sobre de unikernel seL4 (Sobre B) y la capa de persistencia consciente de capacidades `moonshot-database` son elementos de trayectoria v1.0.0+ previstos. La ruta de migración es intencionada: el backend POSIX del Sobre A está previsto para permanecer como alternativa indefinida incluso después de que se distribuya el Sobre B, porque los bytes de los tiles C2SP se serializan de forma idéntica en ambos backends. Los clientes que ejecutan el Sobre A reciben la misma propiedad WORM y el mismo anclaje a Rekor; el aislamiento formalmente verificado está disponible migrando al Sobre B cuando el hardware admite el arranque nativo de seL4.

Supuestos materiales para la transición a seL4: el ecosistema rust-sel4 y sel4-microkit continúa madurando (Microkit 1.3.0 fue reescrito en Rust durante 2025–2026, señalando soporte de primera clase para Rust); el trabajo de la Fase 2 del Sustrato Soberano para `moonshot-database` se materializa según la hoja de ruta de Reemplazos Soberanos Activos; la demanda de los clientes de aislamiento formalmente verificado justifica el coste de desarrollo. Ninguno de estos puntos es una garantía.

## Véase también

- [[worm-ledger-design]] — mapeo de cumplimiento normativo y el argumento de inmutabilidad estructural
- [[worm-ledger-storage-architecture]] — detalle de la capa de almacenamiento: formato de tiles, durabilidad atómica y sobres de doble objetivo
- [[service-fs-architecture]] — el servicio que implementa esta arquitectura como ledger desplegado por tenant
- [[app-console-input]] — la puerta F12 de verificación con intervención humana que es el control de calidad aguas arriba del ledger
- [[sel4-microkernel-substrate]] — la trayectoria prevista de cumplimiento de capacidades seL4 para el aislamiento entre tenants
- [[verify-worm-ledger]] — guía paso a paso: exportar un tile, verificar la cadena de hashes y validar el checkpoint firmado
- [[read-the-command-ledger]] — guía paso a paso: leer entradas del ledger WORM desde la pestaña LEDGER de F12
