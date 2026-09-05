---
schema: foundry-doc-v1
title: "Las pruebas de Merkle como primitiva del sustrato"
slug: merkle-proofs-as-substrate-primitive
category: substrate
type: topic
content_type: topic
quality: complete
index_group: cryptographic-and-microkernel-primitives
short_description: "Las pruebas de Merkle son el mecanismo criptográfico que permite a la plataforma demostrar a cualquier tercero que un registro forma parte de un libro de solo adición que no ha sido reescrito."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "RFC 9162 — Certificate Transparency Version 2.0"
    url: "https://datatracker.ietf.org/doc/html/rfc9162"
  - id: 2
    text: "Especificación C2SP signed-note"
    url: "https://github.com/C2SP/C2SP/blob/main/signed-note.md"
paired_with: merkle-proofs-as-substrate-primitive.md
---

> Las pruebas de Merkle son el mecanismo criptográfico que permite al sustrato de la plataforma garantizar — a cualquier tercero, sin confianza previa — que un registro específico forma parte de un libro de solo adición, y que el libro no ha sido reescrito entre dos puntos observados en el tiempo.

Estas dos garantías juntas forman el lado de lectura y el lado de seguridad de replicación del [[capability-ledger-substrate|Sustrato del Libro de Capacidades]]. Este artículo explica qué son las pruebas de Merkle, por qué existen dos variantes distintas, cómo el crate `system-core` implementa ambas según RFC 9162 Certificate Transparency 2.0, y cómo el crate `system-ledger` las usa para controlar la validez del lado de escritura sin degradar la ruta caliente del lado de lectura.

## 1. Qué son las pruebas de Merkle

Una función hash SHA-256 toma una secuencia arbitraria de bytes y produce una huella de longitud fija de 32 bytes. Cualquier cambio de un solo bit en la entrada produce una huella completamente distinta. Dada solo la huella, recuperar la entrada es computacionalmente inviable — esta es la propiedad de resistencia a colisiones sobre la que descansa todo el razonamiento posterior.

Un árbol de Merkle se construye sobre esta propiedad organizando una secuencia de registros en un árbol binario de hashes. Cada nodo hoja guarda el hash de un registro. Cada nodo interno guarda el hash de la concatenación de sus dos hijos. La raíz — un único valor de 32 bytes — es un compromiso con toda la secuencia: cualquier cambio en cualquier registro cambia todos los hashes en la ruta de esa hoja hasta la raíz, y por tanto cambia la raíz.

### Separación de dominio según RFC 9162

RFC 9162 §2.1 especifica un requisito adicional: la separación de dominio. Los hashes de hoja se calculan como SHA-256 del byte `0x00` seguido de los datos del registro. Los hashes de nodo interno se calculan como SHA-256 del byte `0x01` seguido del hash del hijo izquierdo seguido del hash del hijo derecho. Sin esta distinción, el hash de un nodo interno podría hacerse pasar por el hash de una hoja que ocupa una posición distinta en el árbol, habilitando ataques de segunda preimagen. El crate `system-core` implementa esto exactamente:

```rust
// Leaf hash: SHA-256(0x00 || leaf_data)
pub fn rfc9162_leaf_hash(leaf_data: &[u8]) -> Hash256 { ... }

// Internal hash: SHA-256(0x01 || left || right)
pub fn rfc9162_internal_hash(left: &Hash256, right: &Hash256) -> Hash256 { ... }
```

### Rutas de hermanos y tamaño logarítmico de la prueba

Una prueba de inclusión de Merkle para una hoja específica es una lista de hashes hermanos a lo largo de la ruta desde esa hoja hasta la raíz. Un verificador que posee el hash de la hoja y la lista de hermanos puede reconstruir la raíz aplicando hashes hacia arriba. Si la raíz reconstruida coincide con la raíz reclamada, la hoja está en el árbol. Si no, o bien la hoja o bien la raíz han sido manipuladas.

Para un árbol de `n` hojas, la prueba contiene como máximo ⌈log₂ n⌉ hashes hermanos — unos 10 hashes para un árbol de 1.000 registros, 20 hashes para uno de un millón de registros. El costo de almacenamiento y verificación de la prueba crece logarítmicamente, no linealmente, con el tamaño del libro. Esta es la propiedad que hace que las pruebas de Merkle sean prácticas como primitiva de sustrato a la escala de un libro contable.

La diferencia entre *comprometerse* con un libro (producir la raíz) y *demostrar pertenencia* a un libro (producir una ruta de hermanos) es estructural: el operador del libro mantiene el árbol completo y puede producir pruebas bajo demanda; un verificador solo necesita el hash de la raíz, el hash de la hoja y la ruta de la prueba. El operador del libro no puede falsificar una prueba válida para una hoja que no está en el árbol sin romper la resistencia a colisiones de SHA-256.

## 2. Dos variantes: inclusión y consistencia

El mismo árbol de Merkle admite dos tipos de prueba distintos que responden preguntas diferentes.

Las **pruebas de inclusión** (RFC 9162 §2.1.3) responden: "¿está el hash de este registro específico presente en el árbol en esta raíz?" El consumidor posee un hash de registro, la posición reclamada en el libro, y la raíz actual. La prueba aporta los hashes hermanos necesarios para reconstruir la raíz desde esa hoja. Esta es la comprobación de validez del lado de escritura: antes de registrar un testigo en el libro de capacidades, verificar que el hash del testigo aparece en el árbol de Merkle cubierto por el checkpoint firmado actual.

Las **pruebas de consistencia** (RFC 9162 §2.1.4) responden: "¿es este estado de árbol más nuevo una extensión válida del anterior, o se ha reescrito la historia?" El consumidor posee dos pares `(raíz, tamaño de árbol)` — el antiguo y el nuevo. La prueba demuestra que la raíz antigua está incrustada en la estructura del árbol nuevo, lo que significa que cada hoja de 0 a `old_size - 1` es idéntica en ambos árboles. Un verificador que compara dos checkpoints de distintos puntos en el tiempo puede usar una prueba de consistencia para confirmar que el libro solo añadió registros entre esas dos instantáneas — no eliminó, reordenó ni modificó ningún registro anterior.

Las dos variantes son complementarias. Las pruebas de inclusión controlan cada escritura individual (cada llegada de testigo debe demostrar su lugar en el estado actual del libro antes de ser aceptada). Las pruebas de consistencia controlan la puesta al día de las réplicas del libro (una réplica que avanza del checkpoint A al checkpoint B puede verificar que la extensión es limpia antes de confiar en el estado del checkpoint B). Juntas hacen que el libro de capacidades sea auditable sin requerir que ninguna parte mantenga localmente el historial completo del libro.

## 3. Pruebas de inclusión en `system-core`

La estructura `InclusionProof` en `system-core/src/inclusion_proof.rs` lleva tres campos:

```rust
pub struct InclusionProof {
    pub leaf_index: u64,    // 0-indexed position of the proven leaf
    pub tree_size: u64,     // log size at proof generation time
    pub sibling_hashes: Vec<Hash256>,  // path from leaf to root
}
```

### Algoritmo de verificación de RFC 9162

La verificación sigue textualmente RFC 9162 §2.1.3. El algoritmo mantiene dos contadores llamados `fn_` (la posición del nodo actual, que se desplaza a la derecha al ascender por el árbol) y `sn` (el tamaño de la capa actual, que también se desplaza a la derecha). En cada paso:

- Si el nodo actual es un hijo derecho (`fn_ & 1 == 1`) o ha alcanzado la frontera del árbol para esta capa (`fn_ == sn`), el hermano está a la izquierda: se aplica hash como `internal_hash(sibling, accumulator)`, y luego se eliminan los bits pares finales de ambos contadores (el "recorte interno" — alinea los contadores cuando el árbol no tiene un tamaño potencia de dos).
- En caso contrario, el hermano está a la derecha: se aplica hash como `internal_hash(accumulator, sibling)`.

El algoritmo termina correctamente cuando `sn` llega a cero (la raíz) y el hash acumulado coincide con `expected_root`. La taxonomía de errores distingue cuatro condiciones estructurales: `LeafIndexOutOfBounds`, `PathTooLong`, `PathTooShort` y `RootMismatch`.

### Cobertura de pruebas en distintas formas de árbol

La suite de pruebas cubre 11 casos: sanidad del prefijo de separación de dominio para hashes de hoja e internos; árbol de una sola hoja (la prueba está vacía, la raíz es igual al hash de la hoja); árboles de dos, cuatro y ocho hojas con cada índice de hoja verificado; árboles de tamaño impar (5 hojas, que ejercita la ruta de promoción del borde derecho); hash hermano manipulado; hash de hoja incorrecto; raíz incorrecta; índice de hoja fuera de rango; ruta demasiado larga; ruta demasiado corta; y rechazo de prueba para hoja incorrecta.

### Tiempos de verificación medidos

Rendimiento de la ejecución limpia del benchmark de la Fase 1A.4 en un Intel Xeon a 2,20 GHz:

| Tamaño del árbol | Longitud de ruta de hermanos | Tiempo de verificación |
|---|---|---|
| 8 hojas | 3 hashes | 5,37 µs |
| 1024 hojas | 10 hashes | 17,74 µs |

Se confirma el costo logarítmico: triplicar la longitud de la ruta (3 → 10 hashes) aumenta el tiempo de verificación en 3,3×, siguiendo directamente las operaciones SHA-256 adicionales. Para cualquier tamaño de árbol que un libro de capacidades alcanzaría en la práctica, la verificación bruta de una prueba de inclusión se mantiene muy por debajo de 100 µs.

## 4. Pruebas de consistencia en `system-core`

La estructura `ConsistencyProof` en `system-core/src/consistency_proof.rs` lleva un único campo:

```rust
pub struct ConsistencyProof {
    pub hashes: Vec<Hash256>,
}
```

La aparente simplicidad es engañosa. El algoritmo opera con dos acumuladores en ejecución — `old_hash` y `new_hash` — que rastrean las rutas de hash hacia la raíz antigua y la nueva respectivamente. Ambos se inicializan desde `hashes[0]`, que es la hoja frontera derecha del árbol antiguo (la última hoja en el índice `old_size - 1`). Los `hashes[1..]` restantes se consumen uno a uno.

En cada paso, el verificador rastrea `node` (la posición de frontera actual del árbol antiguo) y `last_node` (la posición de frontera del árbol nuevo). La decisión en cada hash:

- Si `node` es un hijo derecho (`node & 1 == 1`) o ambas fronteras han convergido (`node == last_node`): combinar ambos acumuladores hacia la izquierda — este hash está en el prefijo compartido de los árboles antiguo y nuevo. Se aplica el recorte interno a ambos contadores.
- En caso contrario: combinar solo `new_hash` hacia la derecha — este hash está en la extensión que existe solo en el árbol nuevo; el árbol antiguo aún no ha crecido para cubrirlo.

Una vez consumidos todos los hashes, `last_node` debe ser cero (el algoritmo alcanzó la raíz de ambos árboles), y los dos acumuladores deben ser iguales a `old_root` y `new_root` respectivamente.

### Taxonomía de nueve variantes de error

Las nueve variantes de error distinguen:

| Error | Condición |
|---|---|
| `OldSizeIsZero` | Un árbol vacío es una entrada degenerada; el llamante debe gestionarla por separado |
| `OldSizeExceedsNewSize` | Los árboles solo crecen; este orden es estructuralmente inválido |
| `EqualSizesNonEmptyProof` | Si los tamaños son iguales, la prueba de identidad debe estar vacía |
| `EqualSizesRootMismatch` | Tamaños iguales, prueba vacía, pero las raíces difieren — las raíces son inconsistentes |
| `EmptyProofForNonZeroOldSize` | Una extensión no trivial requiere al menos un hash |
| `PathTooLong` | La prueba consumió `last_node` antes de usar todos los hashes |
| `PathTooShort` | Los hashes se agotaron antes de que `last_node` llegara a cero |
| `OldRootMismatch` | El hash antiguo acumulado no coincide con la raíz antigua reclamada |
| `NewRootMismatch` | El hash nuevo acumulado no coincide con la raíz nueva reclamada |

Esta taxonomía importa para un consumidor del sustrato: `OldRootMismatch` significa que el checkpoint antiguo está siendo tergiversado; `NewRootMismatch` significa que el checkpoint nuevo está siendo tergiversado; `PathTooLong` o `PathTooShort` significa que la propia prueba se construyó incorrectamente o ha sido manipulada. Cada clase de fallo tiene una respuesta operativa distinta.

### Pruebas de conformidad de rejilla completa

La suite de pruebas incluye 11 casos que cubren el caso identidad, `OldSizeIsZero`, `OldSizeExceedsNewSize`, tamaños iguales con prueba no vacía, extensión de una sola hoja (1 → 2), extensiones potencia de dos (2 → 4, 4 → 8), tamaños que no son potencia de dos (3→5, 4→7, 5→7, 6→8, 3→8), raíz antigua incorrecta, raíz nueva incorrecta, hash de prueba corrupto, y la rejilla completa 1..=8 — cada par `(antiguo, nuevo)` con `0 < antiguo ≤ nuevo ≤ 8` verificándose correctamente contra raíces calculadas de forma independiente.

La prueba de rejilla completa es la comprobación de conformidad crítica: un oráculo genera pruebas de forma independiente del verificador (a partir de la estructura del árbol, no de la función recursiva PROOF de la RFC), y el verificador debe aceptar los 36 pares. Este enfoque de verificación cruzada detecta divergencias de algoritmo que pasarían pruebas de ida y vuelta dentro de una sola implementación.

## 5. Primitivas compuestas sobre `SignedCheckpoint`

Un hash de raíz de Merkle es tan digno de confianza como la autoridad que lo firma. El formato de nota firmada C2SP, implementado en `system-core/src/checkpoint.rs`, vincula una raíz de Merkle a un apex nombrado que firma con ed25519. El formato de cable es:

```
<origin>
<tree-size>
<base64(root-hash)>
[<extension-line>...]

— <signer-name> <base64(4-byte-key-hash || 64-byte-ed25519-sig)>
[— <signer-name-2> ...]
```

El cuerpo — origen, tamaño de árbol, hash de raíz, y líneas de extensión opcionales, cada una terminada por un salto de línea — es lo que firma el apex. Varias líneas de firma sobre el mismo cuerpo realizan la ceremonia de transferencia de propiedad multi-apex: en el checkpoint de traspaso, tanto el apex saliente (P-antiguo) como el entrante (P-nuevo) firman el mismo cuerpo, produciendo dos líneas de firma. El verificador del kernel confirma que la transferencia está completa exigiendo ambas firmas en la altura del traspaso.

### API de verificación orientada al kernel

La API compuesta orientada al kernel reside en `SignedCheckpoint`:

```rust
impl SignedCheckpoint {
    // Chain: tree-size invariants → signature verify → inclusion proof verify
    pub fn verify_inclusion_proof(
        &self,
        proof: &InclusionProof,
        leaf_hash: &Hash256,
        signer_name: &str,
        signer_pubkey: &VerifyingKey,
    ) -> Result<(), CheckpointInclusionError> { ... }

    // Chain: tree-size invariants → both-signature verify → consistency proof verify
    pub fn verify_consistency_proof(
        &self,
        proof: &ConsistencyProof,
        old_checkpoint: &SignedCheckpoint,
        signer_name: &str,
        signer_pubkey: &VerifyingKey,
    ) -> Result<(), CheckpointConsistencyError> { ... }
}
```

`verify_inclusion_proof` realiza tres comprobaciones en secuencia. Primero, el campo `tree_size` del `InclusionProof` debe ser igual al `tree_size` del checkpoint; una prueba generada contra un estado de árbol distinto no es válida para este checkpoint. Segundo, el cuerpo del checkpoint debe llevar una firma ed25519 válida del firmante nombrado usando la clave pública proporcionada. Tercero, el `InclusionProof::verify` en bruto debe confirmar que el hash de hoja reconstruye la raíz. Las tres deben pasar.

### Por qué la verificación de prueba en bruto no se expone

La composición sirve un propósito específico: los consumidores no deberían llamar directamente a `InclusionProof::verify` en bruto. Una verificación de prueba en bruto contra un hash de raíz que el llamante obtuvo por otros medios (una variable local, una deserialización sin verificar) no aporta ninguna autenticación — solo la composición con la verificación de firma hace que el hash de raíz sea digno de confianza. La taxonomía `CheckpointInclusionError` mantiene distintas las dos clases de fallo: `SignatureError` significa que el apex no puede autenticarse; `ProofError(InclusionVerifyError)` significa que la ruta de Merkle no reconstruye la raíz autenticada.

`verify_consistency_proof` sigue el mismo patrón con un paso adicional: verifica la firma tanto en el checkpoint *antiguo* como en el nuevo, asegurando que ambos extremos de la cadena de consistencia estén autenticados por el apex antes de evaluar la prueba de consistencia en bruto.

## 6. Integración del consumidor en `system-ledger`

El crate `system-ledger` posee la máquina de estados del lado del kernel que decide si honrar una invocación de capacidad. El rasgo `LedgerConsumer` define el contrato público:

```rust
pub trait LedgerConsumer {
    fn consult_capability(
        &self,
        cap: &Capability,
        current_root: &SignedCheckpoint,
        now: u64,
        witness: Option<&WitnessRecord>,
    ) -> Result<Verdict, ConsultError>;

    fn apply_witness_record(
        &mut self,
        record: WitnessRecord,
        proof: InclusionProof,
    ) -> Result<(), LedgerError>;

    // ... revocation and apex methods
}
```

### Control del lado de escritura mediante pruebas de inclusión

Antes de la Fase 1A.4, `apply_witness_record` aceptaba un `WitnessRecord` sin ninguna verificación criptográfica de su posición en el libro. Se confiaba en que el llamante aportara solo registros que pertenecieran al checkpoint actual. Esto creaba una brecha: un llamante mal configurado o comprometido podía extender el libro con registros que nunca aparecieron en el registro de transparencia firmado.

La Fase 1A.4 cerró esta brecha promoviendo `apply_witness_record` para exigir una `InclusionProof` junto con el registro. El checkpoint actual contra el que se verifica la prueba proviene del propio estado retenido por el consumidor (`InMemoryLedger` mantiene un `CheckpointCache`), no de un parámetro en cada llamada. El método ahora delega en `verify_inclusion_proof` antes de registrar el testigo. Un registro se acepta solo si la prueba de Merkle confirma que el hash del registro está en el árbol cubierto por el checkpoint actual firmado por el apex. Este es el cambio disruptivo v0.1.x → v0.2.0: cambió la firma del rasgo, no solo la implementación.

### Costo del lado de lectura y la caché de checkpoints

El lado de lectura opera en una curva de costo distinta. `consult_capability` debe responder rápido — se sitúa en la ruta de invocación mediada por el kernel. La verificación de firma a ~4 ms por llamada sería prohibitiva para cualquier carga de trabajo intensiva en capacidades. El `CheckpointCache` resuelve esto:

| Operación | Tiempo medido | Notas |
|---|---|---|
| Acierto de caché (entrada más reciente) | 11,2 ns | Búsqueda O(1) por tree_size |
| Fallo de caché (escaneo completo de 64 entradas) | 362 ns | Escaneo secuencial; acotado |
| `verify_signer` (verificación de apex de 1 firma) | 4,01 ms | Ed25519, limitado por hardware |
| `consult_capability` (ruta Allow) | 3,74 ms | Ruta de fallo de caché; dominada por la verificación |

El acierto de caché de 11,2 ns frente a la verificación de firma de 4,01 ms es una diferencia de ~358.000×. Cualquier checkpoint que la caché ya mantenga puede consultarse sin tocar el verificador ed25519. En un kernel en estado estable que ve el mismo checkpoint a través de miles de invocaciones de capacidad por segundo, la tasa de aciertos de caché es efectivamente del 100%; el verificador de firma se ejecuta solo cuando se publica un nuevo checkpoint.

La caché mantiene los 64 checkpoints más recientes por tree_size, indexados para búsqueda O(1). El desalojo LRU mantiene la memoria acotada. El límite de 64 entradas se eligió para cubrir la ventana de traspaso de apex (durante la cual coexisten checkpoints de P-antiguo y P-nuevo) más tasas razonables de publicación de checkpoints sin exceder las restricciones del conjunto de trabajo del kernel.

### Interacción con el traspaso de apex

Una interacción de diseño merece atención explícita: en la altura de traspaso N+2, el checkpoint de traspaso de apex lleva las firmas tanto de P-antiguo como de P-nuevo. La prueba de inclusión de un registro de testigo en la altura N+2 puede verificarse contra la clave pública de cualquiera de los dos firmantes — la pregunta que se responde es "¿está este registro en el árbol?", no "¿quién firmó el árbol?". Los consumidores que requieren una semántica estricta de "ambos apexes firmaron" para los checkpoints de traspaso llaman a `verify_apex_handover` por separado, una comprobación compuesta sobre las verificaciones de firma individuales. La estratificación es deliberada: la verificación de prueba de inclusión responde su propia pregunta acotada; la política sobre quién debe firmar se compone por encima.

## 7. Por qué esto importa como primitiva del sustrato

El Sustrato del Libro de Capacidades requiere que cada autorización de capacidad esté anclada a un registro de transparencia enraizado en el cliente. El cliente — no ningún intermediario — posee las claves de firma del apex. El cliente puede auditar el libro completo. Terceros pueden verificar registros individuales contra checkpoints publicados sin poseer el libro completo. Esta estructura tiene tres propiedades que las alternativas no tienen:

**Auditabilidad sin custodia.** Cualquier parte que posea un checkpoint firmado y un registro de testigo puede verificar de forma independiente la presencia del registro. El cliente no necesita conceder al auditor acceso al libro; el checkpoint y la prueba son suficientes. La revocación de una capacidad es en sí misma una entrada del libro; un auditor que inspeccione un checkpoint posterior a la revocación no encontrará una prueba válida para el registro de testigo de la capacidad revocada contra esa raíz.

**Inmutabilidad de la historia.** La combinación de pruebas de inclusión y pruebas de consistencia hace detectable la reescritura del libro. Si el operador del libro publicó el checkpoint A en el tiempo T₁ y el checkpoint B en el tiempo T₂, cualquier parte que haya registrado ambos checkpoints puede exigir una prueba de consistencia de A a B. Si el operador no puede producir una prueba válida — o si la prueba falla al verificarse — el operador ha reescrito la historia entre T₁ y T₂. La prueba de consistencia es el mecanismo estructural que convierte "de solo adición" en una afirmación verificable en lugar de una declaración de política.

**Replicación sin confianza.** Una réplica que avanza de un checkpoint antiguo a uno nuevo verifica la extensión mediante una prueba de consistencia antes de aceptar el nuevo estado. Un espejo que no puede producir una prueba de consistencia válida desde el último estado confirmado hasta el nuevo estado reclamado, o bien está retrasado (se perdió checkpoints intermedios) o bien presenta un libro bifurcado. Esto importa para el Sustrato Soberano de Dos Bases: un binario del sistema operativo que corre sobre la base de compatibilidad NetBSD debe poder verificar su propio estado de capacidades contra el mismo registro de transparencia que la instancia de base nativa seL4, sin ninguna relación de confianza en tiempo de ejecución entre ambas.

### Camino hacia el consumo por el kernel en `no_std`

La implementación de `system-core` es apta para compilación `no_std`. El crate usa `std` para `Vec` y serialización JSON en v0.2.x; ni `inclusion_proof.rs` ni `consistency_proof.rs` usan ninguna primitiva exclusiva de `std`. Una futura versión MINOR trazará la ruta `no_std`, habilitando el consumo directo desde el kernel por `moonshot-kernel` (el reemplazo Rust `no_std` previsto para la [[sel4-microkernel-substrate|maquinaria de capacidades de seL4]]) sin una frontera de función externa. La primitiva de sustrato que controla cada invocación de capacidad en espacio de usuario puede controlarla también a nivel de kernel usando el mismo código.

### Composición de estándares maduros

Las primitivas criptográficas de `system-core` no son invenciones novedosas. RFC 9162 Certificate Transparency 2.0 es un estándar IETF maduro con múltiples implementaciones independientes. SHA-256 es FIPS 180-4. Ed25519 es RFC 8032. La biblioteca `ed25519-dalek` está ampliamente auditada en el ecosistema Rust. Lo que es nuevo es la composición: conectar un tipo de capacidad de kernel (`seL4_CNode_derivation → Capability`) a un libro RFC 9162 enraizado en el cliente mediante checkpoints de nota firmada C2SP, con control de validez del lado de escritura por prueba de inclusión y control de seguridad de replicación por prueba de consistencia. La composición crea garantías estructurales que ni el kernel ni el libro ofrecen de forma aislada.

## 8. Referencias cruzadas

- **RFC 9162 — Certificate Transparency 2.0** [^1]
  §2.1 (construcción del árbol de hash), §2.1.3 (pruebas de inclusión), §2.1.4
  (pruebas de consistencia). La implementación de `system-core` sigue RFC 9162
  textualmente; los nombres de variables del algoritmo en el código fuente (`fn_`, `sn`, `node`,
  `last_node`) coinciden con el pseudocódigo de la RFC.

- **Especificación C2SP signed-note** [^2]
  El formato de cable para `Checkpoint` y `NoteSignature`. El prefijo de hash de clave de 4 bytes
  en cada línea de firma es `SHA-256("<name>\nED25519\n<32-byte-pubkey>")[..4]`.

- **[[worm-ledger-design|Diseño del libro WORM]]**
  El patrón fundamental de almacenamiento de libros que extiende el Sustrato del Libro de Capacidades.
  Compatibilidad con C2SP tlog-tiles y SHA-256 como función hash de referencia.
  `system-core` es la capa de esquema L0; `system-ledger` es el
  consumidor L1+L2 a nivel de sustrato.

- **[[capability-ledger-substrate]]**
  El artículo complementario que cubre la máquina de estados completa: la estructura `Capability`,
  las Capacidades con Límite de Tiempo, la ceremonia de traspaso de apex, y los veredictos de `LedgerConsumer`.

- **El Sustrato Soberano de Dos Bases**
  El ancla constitucional para la verificación de capacidades que arranca en cualquier lugar. La
  base nativa seL4 y la base de compatibilidad NetBSD comparten el mismo sustrato de libro de
  capacidades; las pruebas de Merkle son el mecanismo de verificación que funciona
  idénticamente en ambas.

- **Commits de implementación (Fase 1A)**
  - `9b5e4fd` — system-core: inclusion_proof.rs + SignedCheckpoint::verify_inclusion_proof (v0.1.3)
  - `82b659f` — system-core: consistency_proof.rs + SignedCheckpoint::verify_consistency_proof (v0.2.0)
  - `2b9ca9c` — system-ledger: apply_witness_record controlado por prueba de inclusión (cambio disruptivo v0.1.x → v0.2.0)
  - `0d6da97` — benchmarks de criterion para las rutas de verificación compuestas
