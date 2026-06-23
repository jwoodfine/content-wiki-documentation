---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: doctrine-invention-7-rekor-anchoring
title: "Doctrina Invención #7 — El Ancla de Integridad"
short_description: "Cómo el binario emisor-de-ancla de Foundry publica un punto de control firmado en Sigstore Rekor cada mes, proporcionando evidencia independiente y verificable del estado del espacio de trabajo."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: doctrine-invention-7-rekor-anchoring.md
category: governance
status: active
quality: complete
last_edited: 2026-06-23
---

# Doctrina Invención #7 — El Ancla de Integridad

La Doctrina §III.7 define el patrón Ancla de Integridad: una operación mensual que agrupa el hash del estado del espacio de trabajo, los hashes de manifiestos y el hash del registro, y publica el resultado en Sigstore Rekor — un registro de transparencia público y de solo anexado. El resultado es verificable de forma independiente: cualquier parte puede confirmar que este estado existió en este momento, bajo esta identidad, sin confiar en la infraestructura de Foundry.

El patrón se modela sobre la notarización combinada con el sellado de tiempo público. La notarización prueba que un documento existió; el sellado de tiempo público prueba que existió en un momento determinado o antes. El registro de transparencia de Rekor proporciona ambas garantías: la prueba de inclusión en el registro constituye evidencia independiente de terceros.

---

## 1. Por Qué un Registro de Transparencia

Un punto de control firmado y almacenado dentro del mismo registro que describe presenta un problema de circularidad: si el registro se ve comprometido, la firma también queda bajo el control del atacante. Una segunda copia en el propio almacén de respaldo del operador traslada la custodia, pero no la confianza — la misma entidad controla ambas.

Un registro de transparencia público rompe este ciclo. El registro de Sigstore Rekor es operado por el proyecto Sigstore (una colaboración entre Google, Red Hat y la Universidad de Purdue, lanzado en 2021) y es de solo anexado por construcción. Una vez publicada una entrada, ninguna parte — incluido Sigstore — puede eliminarla sin romper las pruebas de consistencia criptográfica del registro. Un auditor con acceso al registro de Rekor y al punto de control original puede verificar el ancla de forma independiente a Foundry.

Esta es la misma propiedad estructural que Certificate Transparency (RFC 9162) proporciona para los certificados TLS: la autoridad de certificación no puede mostrar u ocultar certificados de forma selectiva a distintos verificadores, porque las pruebas de inclusión del registro no coincidirían. Sigstore Rekor extiende este modelo a artefactos arbitrarios.

---

## 2. Qué se Publica

Cada operación de anclaje publica una entrada `hashedRekordRequestV002` en Rekor. El artefacto que se ancla es el punto de control en formato JSON serializado, obtenido de `service-fs/v1/checkpoint`:

```json
{
  "origin": "<module_id>",
  "tree_size": <número de entradas en el momento del anclaje>,
  "root_hash": "<SHA-256 hexadecimal del extremo de la cadena>",
  "algorithm": "sha256",
  "timestamp": <segundos en época Unix>,
  "signature": "<firma Ed25519 de nota firmada, en base64>",
  "public_key": "<clave de verificación Ed25519, en base64>"
}
```

El campo `root_hash` es el extremo de cadena SHA-256 de la cadena de hashes de `service-fs` en el momento del anclaje. El campo `signature` es la firma de nota firmada Ed25519 producida por la clave de firma del operador (`FS_SIGNING_KEY`). En conjunto, estos campos constituyen una declaración firmada del estado del registro en un `tree_size` específico.

La entrada de Rekor envuelve este artefacto con los siguientes campos:

- **digest** — SHA-256 del JSON del punto de control (bytes en crudo, codificados en base64)
- **signature.content** — firma Ed25519 de los bytes del punto de control, producida por un par de claves efímeras generadas por ejecución
- **signature.verifier.publicKey.rawBytes** — 44 bytes de DER SPKI de la clave de verificación efímera (codificados en base64)
- **signature.verifier.keyDetails** — `PKIX_ED25519` (firma bytes arbitrarios, no un mensaje con hash previo)

El par de claves efímeras se descarta después de cada ejecución. Su propósito es satisfacer el formato de transmisión Rekor v0.0.2, que requiere un artefacto firmado. La identidad duradera es la marca de tiempo asignada por Rekor y la prueba de inclusión — no la clave efímera.

---

## 3. El Ciclo de Escritura de Vuelta al Registro de Transparencia

Después de que Rekor acepta la entrada, el emisor-de-ancla publica la respuesta completa de Rekor de vuelta en `service-fs/v1/append`, con un identificador de carga útil `anchor-rekor-<unix-timestamp>`.

Esto significa que el registro contiene un historial de su propio anclaje externo. Un auditor que lea el registro puede encontrar la entrada del registro de transparencia de Rekor directamente en el historial del propio registro — no necesita consultar Rekor por separado para confirmar que ocurrió el anclaje. El `tree_size` en el punto de control anclado proporciona el cursor con el que buscar el registro de anclaje: dicho registro aparece en un cursor mayor que `tree_size`, dado que el anclaje ocurre después de que se calcula el punto de control.

El ciclo cerrado significa que la evidencia del anclaje es tan duradera como el propio registro, al tiempo que permanece verificable de forma independiente a través de Rekor.

---

## 4. El Protocolo de Rotación de Fragmento

Sigstore despliega Rekor sobre fragmentos de registro anuales. Cada fragmento tiene su propia clave de firma e identidad de registro. El fragmento de 2025 es:

```
https://log2025-1.rekor.sigstore.dev/api/v2/log/entries
```

Cuando el fragmento de 2026 entre en servicio, el fragmento de 2025 será dado de baja. La API Rekor v2 (`/api/v2/`) no está disponible en el nombre de host heredado (`rekor.sigstore.dev`) — solo en los nombres de host explícitos de cada fragmento.

El emisor-de-ancla utiliza el fragmento de 2025 por defecto. La variable de entorno `REKOR_URL` permite al operador fijar un fragmento diferente sin necesidad de recompilar el binario. La rotación anual de fragmento requiere actualizar esta variable y reiniciar el temporizador de systemd — el manual operativo documenta este procedimiento.

Las entradas de fragmentos antiguos siguen siendo legibles durante un período prolongado tras la rotación. Los anclajes históricos del fragmento de 2025 permanecen verificables frente al registro del fragmento de 2025 durante el tiempo que Sigstore opere ese fragmento en modo de solo lectura. El registro de anclaje en el libro mayor (la escritura de vuelta del registro de transparencia) conserva la respuesta completa de Rekor, por lo que la evidencia de anclaje queda retenida en el registro incluso si el fragmento es dado de baja más adelante.

---

## 5. El Flujo Operativo en Cuatro Pasos

El binario emisor-de-ancla (`fs-anchor-emitter`) ejecuta cuatro pasos en secuencia:

1. **Obtención del punto de control** — `GET /v1/checkpoint` a service-fs, con la cabecera `X-Foundry-Module-ID` configurada con el valor de `FS_MODULE_ID`. Devuelve el JSON del punto de control firmado. Salida con código 2 en caso de fallo.

2. **Construcción del hashedrekord** — se calcula el resumen SHA-256 del JSON del punto de control en el propio proceso; se genera un par de claves Ed25519 efímeras mediante el generador de números aleatorios del sistema operativo; se firman los bytes del punto de control; se codifica el DER SPKI de la clave de verificación. Se ensambla el cuerpo JSON `hashedRekordRequestV002`.

3. **POST a Rekor** — `POST` a `REKOR_URL` (por defecto: fragmento de 2025). En caso de éxito, Rekor devuelve una respuesta JSON con la entrada del registro de transparencia (incluida la marca de tiempo asignada por Rekor y la prueba de inclusión). Salida con código 3 en caso de fallo.

4. **Escritura de vuelta del registro de transparencia** — `POST /v1/append` a service-fs con la respuesta JSON completa de Rekor como carga útil y `payload_id: anchor-rekor-<ts>`. Salida con código 4 en caso de fallo.

Salida con código 0 en caso de éxito completo. El binario termina con un código distinto de cero en el primer paso fallido; una unidad systemd `OnFailure=` puede alertar al operador.

---

## 6. Verificación Independiente

Un tercero que verifique un anclaje necesita:

1. El registro de anclaje del libro mayor (la escritura de vuelta del registro de transparencia — legible en `service-fs/v1/entries` con el rango de cursor adecuado)
2. Acceso al registro de Sigstore Rekor para el fragmento activo

A partir del registro de anclaje, el verificador extrae la entrada del registro de transparencia de Rekor (que contiene el índice de registro asignado por Rekor y la prueba de inclusión). Desde el registro de Rekor, el verificador recupera la misma entrada por índice de registro y confirma:

- El resumen del artefacto en la entrada de Rekor coincide con `SHA-256(JSON del punto de control)`
- La marca de tiempo de Rekor es coherente con la fecha de anclaje declarada
- La prueba de inclusión es válida frente al hash raíz del registro de Rekor en ese tamaño de árbol

A partir del propio JSON del punto de control, el verificador confirma:

- El `root_hash` del punto de control coincide con el extremo de cadena SHA-256 esperado, recalculando la cadena desde las entradas del registro
- La `signature` del punto de control es una firma de nota firmada Ed25519 válida bajo la clave de verificación pública del operador

Esta verificación es independiente del operador de extremo a extremo: utiliza el registro de Rekor (no la infraestructura de Foundry) y la propia cadena de hashes del registro (no la atestación de Foundry sobre dicha cadena).

---

## 7. Descubrimiento de Claves con TUF

La implementación actual fija la URL del fragmento de Rekor mediante una variable de entorno. El camino a largo plazo para el descubrimiento de claves es TUF (The Update Framework) — Sigstore publica una raíz TUF que permite a los clientes descubrir las claves y el punto de acceso del fragmento activo sin codificar una URL de forma fija. Este enfoque está previsto para sobrevivir a la rotación de fragmento sin necesidad de ningún cambio de configuración por parte del operador.

El descubrimiento de SigningConfig basado en TUF está previsto para una versión futura de `fs-anchor-emitter`. Hasta entonces, la variable de entorno `REKOR_URL` proporciona un mecanismo funcionalmente equivalente para las transiciones de fragmento, a costa de requerir una actualización anual de configuración por parte del operador.
