---
schema: foundry-doc-v1
title: "El sustrato de cola de briefs"
slug: brief-queue-substrate
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "Una cola persistente respaldada en archivos que hace viable el apagado inactivo de Yo-Yo sin perder datos del corpus de aprendizaje — la capa de durabilidad del sustrato SLM de tres niveles."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-20
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: brief-queue-substrate.md
---

El **Sustrato de Cola de Briefs** es una cola persistente respaldada en archivos que conecta el flujo editorial de la plataforma PointSav con el sistema de captura del [[apprenticeship-substrate|corpus de aprendizaje]]. Su propósito central es recibir registros de ejecución de briefs — eventos en formato JSON Lines que describen una operación editorial — y conservarlos de forma confiable hasta que el proceso de vaciado pueda escribirlos en el corpus a largo plazo. Esta desvinculación es lo que hace viable el [[yoyo-compute-substrate|apagado inactivo de Yo-Yo]]: cuando la instancia GPU se apaga a mitad de sesión para evitar costos innecesarios, ningún evento del corpus en vuelo se pierde. La cola persiste en disco; el proceso de vaciado retoma donde lo dejó cuando comienza la siguiente sesión. El sustrato también absorbe los eventos de apropiación de instancias spot de proveedores de nube, simplifica el pipeline de captura-edición eliminando dependencias de escritura en línea, y posiciona la plataforma para el futuro camino de preentrenamiento continuo de PointSav-LLM.

## La cola

La cola es cuatro directorios organizados como una máquina de estados para archivos de eventos JSONL:

- **`queue/`** — los eventos entrantes llegan aquí. Cualquier proceso que genere un registro de ejecución de brief escribe un archivo atómico en este directorio. No se requiere bloqueo en el momento de escritura.
- **`queue-in-flight/`** — el proceso de vaciado renombra atómicamente un archivo desde `queue/` hacia este directorio al comenzar a procesarlo. El renombrado es la adquisición del arrendamiento. Si el proceso de vaciado falla a mitad de escritura, el archivo permanece en `queue-in-flight/` y es recuperable al reiniciar.
- **`queue-done/`** — después de que el proceso de vaciado añade exitosamente el evento al archivo JSONL del corpus, mueve el archivo aquí. Los archivos en `queue-done/` son seguros para archivar o eliminar periódicamente.
- **`queue-poison/`** — los archivos que no pueden parsearse, fallan en la validación del esquema o agotan un límite de reintentos configurable se mueven aquí para inspección manual. Los archivos venenosos no bloquean el resto de la cola.

Cada archivo en la cola es un único evento JSONL serializado en disco. Los nombres de archivo se construyen a partir de una marca de tiempo más un sufijo aleatorio para garantizar unicidad entre escritores concurrentes sin requerir coordinación. La estructura de cuatro directorios hace visible el estado de la cola de un vistazo usando herramientas estándar del sistema de archivos — no se requiere ningún daemon para inspeccionarla.

## Qué habilita la cola

El Sustrato de Cola de Briefs ofrece cinco propiedades operativas de las que depende la plataforma:

**Tolerancia al apagado inactivo de Yo-Yo.** El [[yoyo-compute-substrate|nivel de cómputo Yo-Yo]] (OLMo 3.1 32B Think en GPU en ráfaga) se apaga tras un período de inactividad configurable para evitar facturación innecesaria. Sin la cola, cualquier evento generado durante una sesión Yo-Yo tendría que escribirse sincrónicamente en el corpus antes del apagado — acoplando el bucle de inferencia del SLM a la E/S de disco y añadiendo latencia a cada llamada de inferencia. Con la cola, el bucle de inferencia escribe en `queue/` (una escritura local rápida) y el proceso de vaciado maneja la persistencia del corpus de forma independiente. El apagado puede proceder en cuanto se complete la inferencia; no hay escrituras del corpus en progreso.

**Tolerancia a la apropiación de instancias spot.** Las instancias spot y apropiables en la nube pueden ser recuperadas con aviso mínimo. Los eventos que residen en `queue/` o `queue-in-flight/` sobreviven a la apropiación porque el directorio de la cola está en almacenamiento persistente, no en el almacenamiento efímero local de la instancia. Cuando una instancia de reemplazo arranca, el proceso de vaciado retoma desde la última posición comprometida.

**Simplificación del pipeline de captura-edición.** El patrón anterior requería que el pipeline de captura escribiera directamente en los archivos JSONL del corpus durante la sesión editorial, lo que creaba dependencias de ordenación entre la lógica de enrutamiento de auditoría del Doorman y la posición de adición del archivo del corpus. La cola elimina esa dependencia: el Doorman escribe un registro de evento en `queue/` y retorna inmediatamente; el proceso de vaciado serializa las adiciones al corpus en orden de llegada sin bloquear la ruta de inferencia.

**Alineación con el Nivel 1 del cliente.** La arquitectura de cola coincide con el patrón que los servicios de ingestión del Anillo 1 ([[service-people]], [[service-email]], [[service-extraction|service-input]]) ya utilizan para la captura durable de eventos en el límite del [[totebox-archive|inquilino]]. Un cliente que extienda la plataforma con un servidor MCP adicional puede usar el mismo patrón de cola de cuatro directorios para sus eventos de ingestión. La coherencia entre niveles reduce la superficie que un colaborador necesita comprender.

**Preparación para PointSav-LLM futuro.** El [[apprenticeship-substrate|corpus de aprendizaje]] — la acumulación de eventos JSONL creados-por-draft, refinados-por-draft y editados-creativamente — es la señal de entrenamiento prevista para una futura ejecución de preentrenamiento continuo de PointSav-LLM. El Sustrato de Cola de Briefs garantiza que el crecimiento del corpus no se interrumpa por transiciones de nivel de cómputo, apagados inactivos o eventos de apropiación. Cada sesión editorial contribuye al corpus independientemente del nivel de cómputo que haya manejado la inferencia.

## Mecánica de arrendamiento

La cola preserva la corrección bajo procesos de vaciado concurrentes y fallos de proceso mediante un patrón de arrendamiento por renombrado atómico. La secuencia es:

1. El proceso de vaciado escanea `queue/` en busca de archivos candidatos.
2. Para cada candidato, intenta `rename(queue/<archivo>, queue-in-flight/<archivo>)`. Esta es una operación atómica del sistema de archivos en sistemas de archivos conformes a POSIX: exactamente un proceso tiene éxito; todos los demás ven un error de "archivo no encontrado" y continúan.
3. El proceso ganador lee el evento, valida el esquema y añade al archivo JSONL del corpus.
4. En caso de éxito, renombra de `queue-in-flight/<archivo>` a `queue-done/<archivo>`.
5. En caso de fallo (error de parseo, fallo de validación del esquema o agotamiento de reintentos), renombra a `queue-poison/<archivo>`.

Al arrancar, el proceso de vaciado escanea `queue-in-flight/` en busca de archivos dejados por una instancia anterior que haya fallado. Reprocesa esos archivos antes de recoger nuevos de `queue/`. Esto garantiza la entrega al menos una vez: un evento puede añadirse al corpus más de una vez si el proceso de vaciado falla entre la adición al corpus y el renombrado a `queue-done/`. Los consumidores del corpus deduplickan por ID de evento cuando la idempotencia importa.

El patrón de arrendamiento no requiere un viaje de ida y vuelta por la red, un daemon de bloqueo ni un broker de mensajes. Solo requiere que los cuatro directorios compartan un sistema de archivos donde `rename()` sea atómico — una propiedad garantizada por todo sistema de archivos local conforme a POSIX y por la mayoría de los sistemas de archivos de red cuando el origen y el destino están en el mismo montaje.

## Archivos JSONL frente a brokers de mensajes

El Sustrato de Cola de Briefs almacena eventos como archivos JSONL en un sistema de archivos local en lugar de enrutarlos a través de un broker de mensajes alojado. Esta es una elección arquitectónica intencional fundamentada en la [[compounding-substrate|postura de soberanía]] de la plataforma y las restricciones operativas, no una limitación a remediar posteriormente.

Los brokers de mensajes como NATS JetStream o Redis Streams ofrecen sólidas garantías de durabilidad y una semántica rica de grupos de consumidores. También introducen una dependencia de red persistente: el productor no puede escribir si el broker no es alcanzable, y el consumidor no puede leer si el broker ha perdido su estado. Para un espacio de trabajo de un solo inquilino donde el productor de la cola, el consumidor de la cola y el almacenamiento del corpus están todos en la misma máquina o en el mismo volumen persistente en la nube, el viaje de ida y vuelta por la red añade latencia y un modo de fallo sin añadir una capacidad que la plataforma necesite a esta escala.

Los archivos JSONL tienen además una ventaja para este caso de uso: son directamente inspeccionables. Un operador que investigue una anomalía en el corpus puede leer un archivo en `queue-poison/` con cualquier editor de texto. Una entrada de un broker de mensajes requiere la propia interfaz de consulta del broker. La distribución de cuatro directorios hace observable la profundidad de la cola, el recuento en vuelo y el recuento de archivos venenosos con una única invocación de `find` o `ls -l` — no se requiere ningún panel de control del broker.

La elección de archivos JSONL también se alinea con el principio de diseño de solo-texto-plano de la plataforma. El corpus en sí mismo es JSONL; el formato de carga útil de la cola coincide con el formato del corpus; el único trabajo del proceso de vaciado es mover eventos de un contexto JSONL (archivo de cola) a otro (archivo de corpus). Toda la ruta es auditable como texto plano sin estado binario.

Cuando la plataforma escale a productores de corpus de múltiples nodos — un estado futuro planificado — el directorio de la cola puede colocarse en un sistema de archivos de red compartido (NFS, Cloud Filestore o equivalente) y la mecánica de arrendamiento sigue siendo válida en montajes conformes a POSIX. Alternativamente, ese estado futuro puede introducir un broker de mensajes como una capa de velocidad mientras se retiene el formato de corpus JSONL. La elección permanece abierta y no está descartada por el diseño actual.

## Estado de implementación

La convención del Sustrato de Cola de Briefs fue ratificada en la versión v0.1.78 del espacio de trabajo. La implementación está en curso dentro del ámbito de ingeniería del servicio SLM.

Los componentes funcionales en construcción son:

- **API de cola** — cuatro operaciones expuestas a los productores: `enqueue` (escribir un archivo de evento en `queue/`), `dequeue` (arrendar atómicamente un archivo desde `queue/`), `release` (mover de `queue-in-flight/` de vuelta a `queue/` en caso de error no fatal) y `poison` (mover a `queue-poison/` en caso de error fatal).
- **Proceso de vaciado en segundo plano** — un proceso de larga ejecución dentro del Doorman que sondea `queue/` a intervalos configurables, procesa los archivos arrendados y añade al JSONL del corpus. El proceso de vaciado también realiza la recuperación al arrancar de cualquier archivo varado en `queue-in-flight/`.
- **Graduación del hook post-commit** — el pipeline de captura actual escribe eventos del corpus en línea durante la sesión editorial. Una vez disponible la API de cola, el hook post-commit se actualiza para escribir en `queue/` en lugar de directamente en el archivo del corpus. La ruta de escritura del corpus pasa a ser exclusivamente responsabilidad del proceso de vaciado.

La implementación no cambia el esquema JSONL del corpus. Los consumidores del corpus de aprendizaje — incluido el futuro pipeline de preentrenamiento de PointSav-LLM — no observan ningún cambio en el formato del corpus; solo cambia la ruta de escritura.

## Véase también

- [[service-slm-yoyo-operational]] — el estado operativo Yo-Yo que motivó el requisito de tolerancia al apagado inactivo de la cola
- [[service-slm]] — el servicio Doorman que aloja el proceso de vaciado y aplica la disciplina de enrutamiento de auditoría
