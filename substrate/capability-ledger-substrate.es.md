---
schema: foundry-doc-v1
title: "Sustrato del libro de capacidades"
slug: capability-ledger-substrate
category: substrate
type: topic
content_type: topic
quality: complete
index_group: cryptographic-and-microkernel-primitives
short_description: "El Sustrato del Libro de Capacidades es el mecanismo por el cual cada decisión de control de acceso se convierte en un evento criptográficamente auditable, anclado en un registro controlado por el cliente."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Especificación C2SP signed-note"
    url: "https://github.com/C2SP/C2SP/blob/main/signed-note.md"
  - id: 2
    text: "RFC 9162 — Certificate Transparency Version 2.0"
    url: "https://datatracker.ietf.org/doc/html/rfc9162"
paired_with: capability-ledger-substrate.md
---

> El Sustrato del Libro de Capacidades es el mecanismo por el cual cada decisión de control de acceso en un despliegue de plataforma se convierte en un evento criptográficamente auditable, anclado en un registro que controla el cliente.

El Sustrato del Libro de Capacidades extiende el modelo de capacidades nativo del [[sel4-microkernel-substrate|microkernel seL4]] — correcto por prueba formal — con una capa de transparencia que hace que el registro de auditoría sea portátil, esté enraizado en el cliente y sea verificable por terceros sin ninguna relación de confianza con el operador.

## 1. Qué es el Sustrato del Libro de Capacidades

Un kernel de sistema operativo media el acceso a los recursos de hardware. Cuando un proceso quiere escribir en una región de memoria, abrir un archivo o enviar un paquete de red, el kernel decide si el proceso tiene permiso. Esta decisión es lo que "control de acceso" significa a nivel de sistema.

### Las capacidades de seL4 como fundamento

El [[sel4-microkernel-substrate|microkernel seL4]] toma decisiones de control de acceso usando *capacidades* — tokens infalsificables que codifican exactamente qué recurso posee un proceso y qué operaciones puede realizar sobre ese recurso. Un proceso que no posee una capacidad válida para un recurso no puede acceder a él; no hay anulación, no hay autoridad ambiental, no hay usuario root que se salte la comprobación. El modelo de capacidades de seL4 ha sido verificado formalmente: la implementación en C del kernel está probada correcta contra una especificación matemática. Este es el fundamento.

### La capa del libro sobre la prueba del kernel

El Sustrato del Libro de Capacidades no reemplaza este fundamento. Añade una propiedad nueva: cada decisión de invocación de capacidad puede vincularse, mediante una prueba de inclusión de Merkle, a un checkpoint en un registro de transparencia firmado. El cliente posee las claves de firma de ese registro. El cliente puede auditar el historial completo. Terceros pueden verificar entradas individuales contra checkpoints publicados sin acceder al registro completo.

El resultado es un sustrato de seguridad con dos capas verificables de forma independiente: la capa del kernel (prueba formal de seL4 — el kernel no puede ser engañado para honrar una capacidad que debería rechazar) y la capa del libro ([[worm-ledger-design|registro de auditoría]] — el historial de cambios de estado de capacidad no puede reescribirse sin las claves apex del cliente). La combinación es lo que el Sustrato del Libro de Capacidades nombra como el salto generacional: ninguna de las dos capas por sí sola ofrece ambas propiedades.

## 2. El tipo `Capability` — campos, enlace al kernel y el ancla del libro

En `system-core`, la estructura `Capability` es el token de autorización enlazado al libro:

```rust
pub struct Capability {
    pub cap_type: CapabilityType,       // Endpoint, Memory, Irq, Notification, CNode
    pub rights: Vec<Right>,             // Read, Write, Invoke, Grant, Revoke
    pub expiry_t: Option<u64>,          // Unix seconds; None = no built-in expiry
    pub witness_pubkey: Option<String>, // SSH public key for expiry extension
    pub ledger_anchor: LedgerAnchor,    // Points into the customer Merkle log
}
```

Los campos `cap_type` y `rights` se corresponden directamente con la semántica del CDT (Capability Derivation Tree) de seL4: una capacidad `Endpoint` con derechos `[Invoke]` es el objeto seL4 que permite que un dominio de protección envíe un mensaje a otro. Una capacidad `Memory` con `[Read, Write]` es una región de memoria compartida por IPC. Este es el vocabulario nativo del kernel; el Sustrato del Libro de Capacidades lo adopta sin modificación.

### El enlace del ancla del libro

El campo `ledger_anchor` es el enlace nuevo. Identifica el checkpoint de nota firmada C2SP en el registro de transparencia del cliente en el que se comprometió esta capacidad:

```rust
pub struct LedgerAnchor {
    pub origin: String,      // e.g. "foundry.<module-id>.capability-ledger"
    pub tree_size: u64,      // Log size at commitment time
    pub root_hash: Hash256,  // Merkle root at that size
}
```

Una capacidad que lleva un `ledger_anchor` que apunta a la posición de árbol 1.247 en un registro con una raíz conocida puede verificarse: producir una prueba de inclusión de que el hash SHA-256 de la capacidad está en la hoja 1.247 del árbol, y verificar esa prueba contra el checkpoint firmado en tree_size = 1.247. Si la prueba se verifica, la existencia de la capacidad en el registro queda establecida. Si el registro tiene un historial de checkpoints publicado, el ancla vincula la capacidad a un punto específico de ese historial auditable.

### Hash determinista de la capacidad

El método `Capability::hash()` calcula el SHA-256 de la estructura serializada en CBOR (vía `ciborium`). Este es el valor usado como hoja en el árbol de Merkle y como clave en el conjunto de revocación. El determinismo se comprueba: la misma estructura siempre produce el mismo hash; cambiar cualquier campo — incluidos `expiry_t` o el `tree_size` del ancla — produce un hash distinto.

## 3. Capacidades con límite de tiempo (Mecanismo A)

Una capacidad con un campo `expiry_t` distinto de None no puede invocarse después de la marca de tiempo Unix `t` sin una extensión. Este es el Mecanismo A, Capacidades con Límite de Tiempo, según la especificación operativa del sustrato §5.

El mecanismo de extensión requiere dos partes: la propia capacidad nombra una `witness_pubkey` (una clave pública SSH ed25519), y el poseedor de esa clave firma un `WitnessRecord`:

```rust
pub struct WitnessRecord {
    pub capability_hash: Hash256, // identifies which capability is extended
    pub new_expiry_t: u64,        // must be greater than the previous expiry_t
    pub signature: Vec<u8>,       // ssh-keygen -Y sign, namespace "capability-witness-v1"
}
```

La etiqueta de espacio de nombres `capability-witness-v1` impide la reutilización entre espacios de nombres. Una firma ed25519 producida por `ssh-keygen -Y sign` sobre un mensaje de commit o un veredicto de aprendizaje no puede reproducirse como una extensión de testigo de capacidad, porque las etiquetas de espacio de nombres difieren. El módulo `witness.rs` de `system-ledger` verifica las firmas invocando `ssh-keygen -Y verify` con el espacio de nombres correcto.

### Flujo de decisión del kernel al caducar

El flujo de decisión del kernel para una capacidad con límite de tiempo es:
1. Si `now < expiry_t`: se honra la invocación (no se necesita testigo)
2. Si `now >= expiry_t` y no se aporta testigo: `Refuse(Expired)`
3. Si `now >= expiry_t` y se aporta un testigo:
   - Verificar la firma del testigo contra la `witness_pubkey` de la capacidad
   - Verificar una prueba de inclusión de Merkle de que el hash del registro de testigo está en el registro actual
   - Si ambas pasan: `ExtendThenAllow { new_expiry_t }` — se honra la invocación y se actualiza el libro
   - Si alguna falla: `Refuse(WitnessSignatureInvalid)` o `Refuse(WitnessNotInLedger)`

El requisito de prueba de inclusión sobre el registro de testigo es la propiedad clave: una extensión de testigo no puede honrarse hasta que se haya comprometido en el registro de transparencia del cliente y un checkpoint firmado por el apex la cubra. La aprobación del apex del cliente es un requisito previo para la extensión de la vida de la capacidad. Esto no puede falsificarse sin las claves apex ed25519 del cliente.

## 4. La ceremonia de propiedad del apex (traspaso N+3+)

Las claves apex del cliente son la raíz de confianza de todo el libro de capacidades. Un registro de transparencia es tan digno de confianza como el proceso para establecer y rotar esas claves. El Sustrato del Libro de Capacidades especifica una ceremonia formal de transferencia de propiedad que produce un registro de traspaso auditable en el mismo libro que asegura.

La ceremonia procede en los checkpoints N, N+1, N+2, N+3+:

| Altura | Acción | Firmas requeridas |
|---|---|---|
| N | Último checkpoint bajo la autoridad de P-antiguo | Solo P-antiguo |
| N+1 | Entrada de revocación: P-antiguo queda revocado | P-antiguo (firmando su propia revocación) |
| N+2 | Checkpoint de traspaso — co-firmado por ambos apexes | P-antiguo Y P-nuevo (ambos requeridos) |
| N+3+ | Checkpoints posteriores al traspaso | Solo P-nuevo; P-antiguo rechazado con `StaleApex` |

El formato de nota firmada C2SP admite directamente la firma múltiple: el mismo cuerpo de checkpoint (origin + tree_size + root_hash) puede llevar varias líneas de firma, cada una de una clave nombrada distinta. La primitiva compuesta `SignedCheckpoint::verify_apex_handover` comprueba ambas firmas en un checkpoint de traspaso.

El invariante N+3+ es: cualquier invocación de capacidad que presente un checkpoint firmado únicamente por P-antiguo en la altura N+3 o posterior se rechaza con `Refuse(StaleApex)`. El módulo `ApexHistory` en `system-ledger` rastrea la vigencia efectiva de cada apex (alturas `effective_from` y `effective_until`) y aplica este invariante en el momento de la consulta.

### Atomicidad, auditabilidad, finalidad

La ceremonia tiene tres propiedades relevantes para un cliente:
1. **Atomicidad**: el traspaso es un único evento autocontenido en el registro. No hay migración de estado fuera de banda. El registro documenta la ceremonia completa.
2. **Auditabilidad**: cualquier tercero que examine el registro puede identificar el checkpoint exacto donde terminó la autoridad de P-antiguo y comenzó la de P-nuevo.
3. **Finalidad**: una vez publicado el checkpoint de traspaso N+2, P-antiguo no puede producir un checkpoint válido para N+3+ que el kernel acepte. La rotación de claves es permanente sin una nueva ceremonia.

Una prueba de extremo a extremo en `system-ledger` (`full_handover_ceremony_end_to_end`) verifica las cuatro etapas: antes del traspaso P-antiguo es aceptado; se aplica la revocación; el traspaso con ambas firmas se acepta; después del traspaso, P-antiguo por sí solo es rechazado con `StaleApex`.

## 5. La máquina de estados `LedgerConsumer` — flujo de consulta y tipos de veredicto

El rasgo `LedgerConsumer` en `system-ledger` es la interfaz orientada al kernel:

```rust
pub trait LedgerConsumer {
    fn consult_capability(
        &self, cap: &Capability, current_root: &SignedCheckpoint,
        now: u64, witness: Option<&WitnessRecord>
    ) -> Result<Verdict, ConsultError>;

    fn apply_revocation(&mut self, event: RevocationEvent) -> Result<(), LedgerError>;
    fn apply_apex_handover(&mut self, ...) -> Result<(), LedgerError>;
    fn apply_witness_record(&mut self, record: WitnessRecord, proof: InclusionProof)
        -> Result<(), LedgerError>;
}
```

`consult_capability` es la ruta caliente del lado de lectura. Devuelve uno de tres veredictos:

| Veredicto | Significado | Acción del kernel |
|---|---|---|
| `Allow` | La capacidad es vigente y no ha caducado | Honrar la invocación |
| `Refuse(reason)` | La capacidad no es válida; se aporta la razón | Denegar la invocación |
| `ExtendThenAllow { new_expiry_t }` | Extensión de testigo aceptada | Extender y honrar |

### Orden de comprobaciones en la consulta

El flujo de decisión de la consulta:
1. **Comprobación de validez del apex**: ¿está el current_root firmado por el apex reconocido? Si el checkpoint no está firmado por el apex, todo queda invalidado — `Refuse(ApexInvalid)`.
2. **Comprobación del invariante post-traspaso**: si ha ocurrido un traspaso de apex, ¿procede este checkpoint de un apex rechazado (obsoleto)? Si es así, `Refuse(StaleApex)`.
3. **Comprobación de revocación**: ¿está el hash de la capacidad en el conjunto de revocación? Si es así, `Refuse(Revoked)`.
4. **Comprobación de caducidad**: ¿es `now < expiry_t` (o `expiry_t` es None)? Si es así, `Allow`.
5. **Ruta de testigo**: si ha caducado, intentar el flujo de extensión de testigo (§3 arriba).

### Métodos del lado de escritura y su cadencia

Los tres métodos del lado de escritura (`apply_revocation`, `apply_apex_handover`, `apply_witness_record`) actualizan el estado del libro que las consultas posteriores leen. Están separados del lado de lectura precisamente porque los patrones de acceso de lectura/escritura del kernel difieren: `consult_capability` se llama en cada invocación; los métodos de escritura se llaman con mucha menos frecuencia (los eventos de revocación y los traspasos de apex son raros; las extensiones de testigo ocurren en los límites de caducidad de las capacidades, que pueden estar separados por horas o días).

## 6. Disciplina de caché — por qué la aceleración de 358.000× es arquitectónicamente crítica

El flujo de decisión de `consult_capability` requiere verificar que el checkpoint actual está firmado por el apex. Una verificación de firma ed25519 tarda aproximadamente 4 milisegundos en el hardware Intel Xeon a 2,20 GHz donde se desarrolla el sustrato. Cualquier carga de trabajo que llame a `consult_capability` cientos de veces por segundo pasaría la mayor parte de su tiempo verificando firmas — una sobrecarga inaceptable para un control de acceso mediado por el kernel.

### Ruta de acierto de `CheckpointCache`

El `CheckpointCache` en `system-ledger` resuelve esto. Guarda los N checkpoints verificados más recientes (64 por defecto), indexados por tree_size. Un acierto de caché — buscar un checkpoint que el libro ya ha verificado — cuesta 11,2 nanosegundos. La caché almacena los objetos `SignedCheckpoint` ya verificados; una búsqueda confirma que el checkpoint está presente y lo devuelve sin volver a ejecutar ed25519.

| Operación | Tiempo | Proporción |
|---|---|---|
| Acierto de caché (búsqueda más reciente) | 11,2 ns | 1× (referencia) |
| Fallo de caché (escaneo completo de 64 entradas) | 362 ns | ~32× |
| `verify_signer` (ed25519, 1 apex) | 4,01 ms | ~358.000× |
| `consult_capability` (ruta completa, fallo de caché) | 3,74 ms | ~334.000× |

En operación estable, el kernel publica checkpoints con poca frecuencia (cada checkpoint compromete un lote de cambios de estado de capacidad). Entre publicaciones de checkpoint, cada invocación de capacidad acierta en la caché. La tasa de aciertos de caché se aproxima al 100% para cualquier carga de trabajo sostenida. El verificador ed25519 se ejecuta solo cuando se publica un nuevo checkpoint — lo cual ocurre en la ruta de escritura, no en la de lectura.

### Límite de la caché y la separación lectura/escritura

El límite de 64 entradas cubre: la ventana de traspaso de apex (durante la cual coexisten checkpoints de P-antiguo y P-nuevo en las alturas N+1 y N+2), el período de solapamiento en que varios componentes del sistema mantienen referencias a checkpoints recientes ligeramente distintos, y tasas razonables de publicación de checkpoints sin exceder las restricciones del conjunto de trabajo del kernel. El límite es una decisión de configuración, no un requisito de protocolo.

La lección arquitectónica es que la caché y las pruebas de inclusión de Merkle no son alternativas — responden a preguntas distintas en rutas de acceso distintas. La caché hace rápida la ruta de lectura. Las pruebas de inclusión hacen fiable la ruta de escritura. Ambas son necesarias para un sustrato de producción.

## 7. Revocación e invariantes post-traspaso

La **revocación** es el mecanismo para revocar permanentemente la autoridad de una capacidad. Un `RevocationEvent` lleva el hash SHA-256 de la capacidad y un registro de revocación. Tras invocar `apply_revocation`, `consult_capability` devuelve `Refuse(Revoked)` para ese hash de capacidad independientemente de la caducidad o el estado del testigo. El conjunto de revocación es un `HashSet<Hash256>` en la implementación en memoria — comprobación de pertenencia O(1).

Los eventos de revocación son a su vez entradas del registro, ancladas al mismo registro de transparencia firmado por el cliente que las confirmaciones de capacidad. Un auditor que examine el registro ve la secuencia completa: capacidad comprometida en la altura N₁, revocada en la altura N₂, y ninguna extensión de testigo posterior es válida después de N₂ porque cualquier extensión así necesitaría referenciar un checkpoint en N₂ o posterior, donde la entrada de revocación es visible.

### El corte del apex tras el traspaso

El **invariante post-traspaso** es una propiedad distinta: gobierna qué clave de firma de apex es autoritativa en un checkpoint dado, independientemente de la revocación de capacidades individuales. Una vez que la ceremonia de traspaso de apex se completa en la altura N+2, cualquier invocación que presente un checkpoint firmado únicamente por P-antiguo en la altura N+3 o posterior se rechaza. Esto impide que P-antiguo reafirme su autoridad después de transferirla — el registro documenta la transferencia, y el kernel aplica la altura de corte.

Las dos propiedades operan en niveles distintos del sustrato:
- La revocación es por capacidad (un token específico es inválido)
- El post-traspaso es por época (la clave de apex antigua es inválida para todo un período de tiempo)

Ambas son aplicadas por `InMemoryLedger` en `system-ledger`. Ambas se comprueban en la prueba de integración `full_handover_ceremony_end_to_end`.

## 8. Relación con el libro WORM

El libro [[worm-ledger-architecture|WORM]] (de solo escritura, lectura múltiple) es la capa fundamental de almacenamiento de registros de la arquitectura Foundry. Implementa un registro de transparencia compatible con C2SP tlog-tiles: de solo adición, direccionado por contenido, firmado criptográficamente por un apex. Los consumidores a nivel de servicio interactúan con él en el nivel de aplicación.

El Sustrato del Libro de Capacidades es el consumidor a nivel de sustrato del mismo formato de registro. Los tipos de primitiva de datos (`Capability`, `WitnessRecord`, `LedgerAnchor`, `SignedCheckpoint`, `InclusionProof`, `ConsistencyProof`) definidos en `system-core` son la capa de esquema L0. La máquina de estados en `system-ledger` es el consumidor L1+L2.

### Consumidores a nivel de sustrato y a nivel de aplicación

El paralelismo con `service-fs` es estructural y deliberado:
- `service-fs` es el consumidor WORM a nivel de aplicación: Ring 1, espacio de usuario, accesible por red, con rendimiento de registros a escala humana
- `system-ledger` es el consumidor WORM a nivel de sustrato: adyacente al kernel, de un solo hilo, con latencia de lectura requerida en microsegundos

Ambos usan el mismo formato de nota firmada C2SP para los checkpoints. Ambos verifican firmas ed25519 del apex. Ambos aceptan cambios de estado de capacidad (revocaciones, registros de testigo) que necesitan pruebas de inclusión de Merkle para ser de confianza. La diferencia es el patrón de acceso y la consecuencia de un fallo: en `service-fs`, una verificación lenta retrasa una operación de archivo; en `system-ledger`, una verificación lenta retrasa una invocación de capacidad mediada por el kernel, lo cual es una restricción de rendimiento a nivel de sistema.

Esta separación de capas — las mismas primitivas criptográficas, distintos niveles de despliegue, distintos presupuestos de rendimiento — es el patrón arquitectónico que el Sustrato del Libro de Capacidades formaliza. Un futuro sistema que reemplace a `service-fs` o añada un segundo consumidor WORM no necesita reimplementar la mecánica de pruebas; comparte `system-core` y compone las mismas primitivas en su propio nivel.

## 9. Referencias cruzadas

- **El Sustrato del Libro de Capacidades** — el ancla constitucional para el enlace de registro Merkle enraizado en el cliente en los despliegues de plataforma. Cada autorización de capacidad se ancla a un registro de transparencia que mantiene el cliente.

- **El Sustrato Soberano de Dos Bases** — la [[system-substrate-doctrine|composición de Dos Bases]] (base nativa seL4 + base de compatibilidad NetBSD) comparte el mismo sustrato de libro de capacidades. El registro de auditoría viaja con la capacidad independientemente de sobre qué base se ejecute.

- **Especificación operativa del sustrato**
  La especificación de 12 secciones que cubre: §3.1 (esquema del tipo Capability), §4
  (ceremonia de traspaso de apex N+3+), §5.1 (esquema de WitnessRecord y Mecanismo A),
  §6.1 (formato de artefacto de verificación reproducible), §8 (hoja de puntuación).

- **[[worm-ledger-design|Diseño del libro WORM]]**
  La capa fundamental de almacenamiento de registros. §3 D1 (formato de cable C2SP tlog-tiles),
  §3 D3 (línea base SHA-256). El Libro de Capacidades es un consumidor a nivel de sustrato
  del mismo diseño.

- **[[merkle-proofs-as-substrate-primitive]]**
  Artículo técnico complementario que cubre las pruebas de inclusión y consistencia de RFC 9162, las estructuras `InclusionProof` y `ConsistencyProof`, los algoritmos de verificación y las pruebas de rendimiento. Léase junto a este artículo para la fundamentación criptográfica.

- **Estado de implementación**
  - `system-core` v1.0.0: `Capability`, `WitnessRecord`, `LedgerAnchor`,
    `Checkpoint`, `NoteSignature`, `SignedCheckpoint`, `InclusionProof`,
    `ConsistencyProof`. 62 pruebas.
  - `system-ledger` v1.0.0: rasgo `LedgerConsumer`, `InMemoryLedger`,
    `CheckpointCache`, `RevocationSet`, `ApexHistory`,
    `verify_witness_signature`. 47 pruebas + 12 benchmarks de criterion.
