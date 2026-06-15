---
schema: foundry-doc-v1
title: "Cómo verificar una entrada del libro mayor WORM"
slug: verify-worm-ledger
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: verify-worm-ledger.md
---

El libro mayor WORM garantiza que los registros no pueden modificarse ni eliminarse después de ser escritos. La verificación confirma que esa garantía se mantiene para una entrada específica: que la cadena de hash está intacta y que no ocurrió ninguna alteración posterior a la escritura. Esta guía cubre la verificación usando la API de service-fs y la cadena de herramientas SHA-256 estándar — no se requieren herramientas propietarias.

Para lo que cubre la garantía WORM y lo que no cubre, véase [[worm-ledger-architecture]]. Para el formato de almacenamiento, véase [[worm-ledger-storage-architecture]].

## Requisitos previos

- Acceso a un libro mayor de Totebox (acceso local a archivos o API de service-fs)
- Una utilidad SHA-256 (`sha256sum` en Linux, `shasum -a 256` en macOS, o equivalente)
- La posición (índice de fila) o rango de tiempo de la entrada a verificar

## Paso 1: Exportar el tile que contiene su entrada

Usando la API de service-fs, llame a `read_since` con el punto de control inmediatamente anterior a la entrada objetivo:

```
read_since(checkpoint_id: "<checkpoint-id>", limit: 1)
```

Esto devuelve el archivo tile para ese segmento del libro mayor. En un despliegue local también puede leer los archivos C2SP tlog-tiles directamente desde el directorio del libro mayor.

## Paso 2: Localizar la entrada en el tile

El tile es texto plano en formato C2SP tlog-tiles. Cada línea es una entrada de registro codificada en base64 seguida de su hash. Encuentre la fila que corresponde a su entrada objetivo por marca de tiempo o número de secuencia.

## Paso 3: Verificar la cadena de hash

Para cada fila en el tile, el hash de esa fila se incluye en el cálculo de hash de la fila siguiente. Para verificar la entrada N:

1. Tome el hash de la fila N−1 (o el hash génesis para la primera entrada).
2. Concatenéelo con los bytes crudos de la entrada N.
3. Calcule SHA-256 de la concatenación.
4. Compare el resultado con el hash registrado en la fila N.

Una coincidencia confirma que la cadena está intacta desde el génesis hasta ese punto. Una discrepancia en la fila N significa que esa fila o alguna anterior fue alterada — inspeccione cada fila hacia atrás desde N para aislar el punto de manipulación.

## Paso 4: Verificar contra un punto de control firmado

Si un punto de control firmado cubre el rango que contiene su entrada, puede verificar la firma de ese punto de control para extender la garantía hasta el punto de anclaje:

1. Recupere el signed-note C2SP para el punto de control correspondiente.
2. Verifique la firma Ed25519 de la nota usando la clave pública publicada para el ancla Sigstore Rekor.
3. Confirme que el punto de control cubre un número de secuencia que incluye su entrada.

Una firma válida de Sigstore Rekor significa que el estado de la cadena fue marcado con tiempo externamente en ese punto, proporcionando verificabilidad independiente del servicio activo.

## Verificación automatizada

La CLI de `service-fs` proporciona un subcomando `verify` que ejecuta los pasos 2–4 automáticamente:

```
service-fs verify --from <checkpoint-id> --to <entry-id>
```

Use el procedimiento manual anterior cuando quiera inspeccionar la cadena sin confiar en la CLI.

## Puntos clave

- La verificación requiere solo una utilidad SHA-256 y los archivos tile crudos — no se necesita servicio activo
- Una discrepancia en la cadena de hash en la fila N significa alteración en N o antes; inspeccione hacia atrás para aislarla
- Los puntos de control firmados extienden la verificación a un ancla de tiempo público, permitiendo auditorías por terceros
- El formato C2SP tlog-tiles garantiza que estos pasos sean ejecutables con herramientas estándar durante décadas

## Véase también

- [[worm-ledger-architecture]] — qué cubre la garantía WORM y sus propiedades estructurales
- [[worm-ledger-storage-architecture]] — el formato de tiles, escrituras atómicas y estructura de puntos de control
- [[service-fs-architecture]] — el servicio que implementa y sirve el libro mayor
- [[read-the-command-ledger]] — leer entradas del libro mayor desde os-console
- [[worm-ledger-design]] — la filosofía de diseño y el fundamento de cumplimiento regulatorio
