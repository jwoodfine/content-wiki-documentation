---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-input
title: "service-input — Ingesta de Documentos"
short_description: "service-input es el servicio de ingesta de documentos del Anillo 1 que acepta archivos en el límite por inquilino, los enruta a través de analizadores específicos por formato y escribe la salida normalizada en el registro inmutable WORM por inquilino mediante service-fs."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: service-input.md
category: services
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---

`service-input` es el servicio de ingesta de documentos del [[three-ring-architecture|Anillo 1]] en la arquitectura del sistema PointSav. Acepta archivos en el límite por inquilino, los enruta a través de analizadores específicos por formato y escribe la salida normalizada en el [[worm-ledger-design|registro inmutable WORM]] por inquilino mediante [[service-fs-architecture|`service-fs`]].

## La posición Ancla (F12 / SYS-ADR-10)

El límite del Anillo 1 es el perímetro de confianza del sistema. Todo artefacto que cruce este límite debe pasar por un paso de procesamiento determinista y auditable antes de ser confirmado en el registro WORM. `service-input` ocupa esa posición para los documentos estructurados.

[[sys-adr-10|SYS-ADR-10]] designa esta posición como **el Ancla** (función F12): el único punto de entrada obligatorio donde los bytes del documento ingresan al Anillo 1, se someten a análisis determinista y se transfieren a `service-fs` para su almacenamiento permanente de solo adición. Ningún aspecto del análisis se delega a un modelo de inteligencia artificial; ningún aspecto del esquema de salida varía de forma no determinista. Los mismos bytes de entrada, con la misma versión del analizador, producen siempre el mismo `ParsedDocument`.

Esta es la propiedad Ancla: la presencia del documento en el registro WORM queda anclada a una transformación determinista reproducible, no a una inferencia probabilística de un modelo de IA.

## Arquitectura

```
Llamador (Anillo 2 u operador)
        │
        │  POST /mcp  (JSON-RPC 2.0, cabecera X-Foundry-Module-ID)
        ▼
   Manejador MCP  (src/mcp.rs)
        │
        │  filename, source_id, bytes_base64
        ▼
   Despachador  (src/lib.rs)
        │
        │  detect_format → enruta al Analizador por formato
        ▼
   Analizador  (src/pdf.rs | markdown.rs | docx.rs | xlsx.rs)
        │
        │  ParsedDocument { format, source_id, text, metadata }
        ▼
   FsClient  (src/fs_client.rs)
        │
        │  POST /v1/append  (X-Foundry-Module-ID, cuerpo JSON)
        ▼
   service-fs  (Anillo 1, registro inmutable WORM)
```

El límite HTTP expone tres puntos de acceso: `GET /healthz`, `GET /readyz` y `POST /mcp`. El punto MCP es la única superficie de escritura. Este servicio no dispone de superficie de lectura; las lecturas se realizan en `service-fs` a través de su propia interfaz de recursos MCP.

## Detección de formato

La detección de formato se ejecuta antes del despacho al analizador. La función `detect_format` (en `src/lib.rs`) aplica dos estrategias en orden.

**Extensión primero**: la extensión del nombre de archivo se compara con el conjunto conocido (`.pdf`, `.md` / `.markdown`, `.docx`, `.xlsx`). La comparación de extensiones no distingue entre mayúsculas y minúsculas.

**Bytes mágicos como alternativa**: cuando la extensión está ausente o no se reconoce, se inspeccionan los primeros cuatro bytes del documento en busca de secuencias mágicas conocidas. Los documentos PDF comienzan con `%PDF` (hex `25 50 44 46`). Los archivos DOCX y XLSX son archivos ZIP y comparten la cabecera `PK` (`50 4B 03 04`); en este nivel alternativo, ambos formatos son ambiguos, por lo que la detección de formato se remite a la comparación de extensión. Un archivo cuya extensión no sea ni `.docx` ni `.xlsx`, pero cuyo contenido sea un archivo ZIP, se reporta como `FormatUndetected`.

La detección de formato devuelve un `Option<Format>`. Un resultado `None` provoca que el manejador MCP devuelva un error `-32602 Invalid params` al llamador; el archivo no se escribe en el registro. Este algoritmo de detección es completamente determinista, sin inferencia de IA, conforme a [[sys-adr-07|SYS-ADR-07]].

## Analizadores

### PDF — oxidize-pdf 2.x

El `PdfParser` (en `src/pdf.rs`) usa oxidize-pdf 2.x para extraer texto de documentos PDF. La biblioteca expone una API de ruta de archivo en lugar de un lector en memoria; para gestionar esto, `PdfParser` escribe los bytes de entrada en un archivo temporal con nombre único en el directorio temporal del sistema, lo abre mediante oxidize-pdf, extrae el texto y elimina el archivo temporal a través de un guardia de liberación RAII. El archivo temporal nunca permanece en disco después de que el método retorna, incluso si el análisis falla.

`ParsedDocument` producido: `text` es el texto concatenado de todas las páginas; `metadata` es `{ "page_count": N, "parser": "oxidize-pdf" }`.

### Markdown — pulldown-cmark 0.12

El `MarkdownParser` (en `src/markdown.rs`) usa pulldown-cmark 0.12. A diferencia del analizador PDF, el análisis de Markdown opera directamente sobre el fragmento de bytes en memoria; no se necesita archivo temporal. El analizador recopila todos los eventos `Text` y `Code`, elimina las etiquetas HTML de la secuencia de eventos y concatena los resultados. El texto de los encabezados se recopila por separado y se devuelve en los metadatos.

`ParsedDocument` producido: `text` contiene todo el contenido textual visible; `metadata` es `{ "headings": ["Encabezado 1", "Encabezado 2", ...], "parser": "pulldown-cmark" }`.

### DOCX — docx-rust 0.1.x

El `DocxParser` (en `src/docx.rs`) usa docx-rust 0.1.x para extraer texto de párrafos de documentos Word Open XML (DOCX). Los archivos DOCX son archivos ZIP; el analizador confirma primero la firma de bytes mágicos (`PK\x03\x04`) antes de intentar la extracción. Si los bytes no coinciden, se devuelve `FormatMismatch` de inmediato sin intentar la extracción del ZIP, lo que protege contra el despacho erróneo de archivos ZIP que no son DOCX.

`ParsedDocument` producido: `text` es el texto de los párrafos concatenados con separadores de nueva línea; `metadata` es `{ "paragraph_count": N, "parser": "docx-rust" }`.

### XLSX — calamine 0.34

El `XlsxParser` (en `src/xlsx.rs`) usa calamine 0.34. Al igual que DOCX, los archivos XLSX son archivos ZIP y reciben la misma verificación de bytes mágicos. El analizador abre el libro desde un `Cursor` en memoria (sin archivo temporal), itera todas las hojas y serializa todas las filas como columnas separadas por tabuladores. Los límites entre hojas se separan con saltos de línea en el texto de salida.

`ParsedDocument` producido: `text` contiene los valores de las celdas separados por tabuladores, una fila por línea, todas las hojas concatenadas; `metadata` es `{ "sheet_count": N, "sheets": ["Sheet1", ...], "parser": "calamine" }`.

## Despachador

El `Dispatcher` (en `src/lib.rs`) es un registro por formato de instancias `Box<dyn Parser + Send + Sync>`. Se construye al inicio del daemon con los cuatro analizadores compatibles registrados mediante una API de construcción:

```
Dispatcher::new()
    .with_pdf(Box::new(PdfParser))
    .with_markdown(Box::new(MarkdownParser))
    .with_docx(Box::new(DocxParser))
    .with_xlsx(Box::new(XlsxParser))
```

Hay dos métodos de despacho disponibles:

- `dispatch(format, source_id, bytes)` — el llamador ya ha identificado el formato. Devuelve `ParseError::UnsupportedFormat` si no hay ningún analizador registrado para el formato dado.
- `dispatch_with_detection(filename, bytes)` — ejecuta la detección de formato internamente y luego despacha. Envoltura de conveniencia para llamadores que aún no han ejecutado la detección.

El trait `Parser` es compatible con objetos:

```rust
pub trait Parser: Send + Sync {
    fn parse(&self, source_id: &str, bytes: &[u8]) -> Result<ParsedDocument, ParseError>;
}
```

## ParsedDocument

Los cuatro analizadores devuelven un `ParsedDocument` normalizado:

```rust
pub struct ParsedDocument {
    pub format: Format,
    pub source_id: String,
    pub text: String,
    pub metadata: serde_json::Value,
}
```

- `format`: uno de `Format::{Pdf, Markdown, Docx, Xlsx}`
- `source_id`: transferido desde el llamador (el `payload_id` del registro)
- `text`: contenido textual extraído; codificación específica por formato (véanse las secciones de analizadores anteriores)
- `metadata`: objeto JSON con campos específicos del analizador; siempre incluye la clave `"parser"`

El tipo `ParsedDocument` implementa `Serialize`. `FsClient` lo envuelve como campo `payload` en la solicitud de adición a service-fs.

## FsClient

`FsClient` (en `src/fs_client.rs`) envía registros `ParsedDocument` al punto de acceso `/v1/append` de `service-fs`.

Formato de red:

```json
POST /v1/append
X-Foundry-Module-ID: <module_id>
Content-Type: application/json

{
  "payload_id": "<doc.source_id>",
  "payload": { ...ParsedDocument... }
}
```

La cabecera `X-Foundry-Module-ID` identifica al llamador por inquilino. El servidor service-fs valida esta cabecera frente a su propia configuración `FS_MODULE_ID` y devuelve HTTP 403 si los valores no coinciden. Este es el mecanismo de aplicación del límite por inquilino en la capa del registro WORM.

`FsClient::submit` devuelve el `cursor: u64` asignado por service-fs, un entero monotónicamente creciente que sirve como referencia estable para esta entrada del registro. El cursor se devuelve al llamador MCP en la respuesta de la herramienta. `FsClient` usa ureq 3.x para E/S HTTP bloqueante; la llamada bloqueante es aceptable para el rendimiento de ingesta en el límite del Anillo 1, donde se procesa un documento por llamada MCP.

## Interfaz MCP

**Punto de acceso:**

```
POST /mcp
Content-Type: application/json
X-Foundry-Module-ID: <module_id>
```

**Protocolo:** JSON-RPC 2.0 (transporte HTTP con flujo — una respuesta JSON por solicitud).

### document.ingest

Detecta el formato del documento, analiza los bytes y escribe el documento analizado en el registro WORM de service-fs.

**Esquema de entrada:**

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `filename` | string | Sí | Nombre de archivo original; se usa para la detección de formato (extensión primero, bytes mágicos como alternativa) |
| `source_id` | string | Sí | Identificador del documento en el lado del llamador; se reenvía como `payload_id` del registro |
| `bytes_base64` | string | Sí | Bytes del documento codificados en Base64 (codificación estándar) |

**Respuesta en caso de éxito:**

```json
{
  "content": [{"type": "text", "text": "{\"cursor\": 42, \"source_id\": \"doc-001\", \"format\": \"Pdf\"}"}],
  "isError": false
}
```

**Respuestas de error:**

- `-32602 Invalid params`: formato no detectado, fallo en la decodificación Base64 o argumentos faltantes
- `-32603 Internal error`: fallo del analizador o error de transporte en service-fs

### Límite por inquilino

Todas las solicitudes MCP requieren la cabecera `X-Foundry-Module-ID`. El valor de la cabecera debe coincidir con el ID de módulo con el que se inició el daemon (`INPUT_MODULE_ID`). Una discrepancia o la ausencia de la cabecera devuelve un error JSON-RPC `-32600 Invalid request`. Esta verificación se realiza en la capa del manejador MCP, antes de cualquier análisis o escritura en el registro.

## Cumplimiento de ADR-07

[[sys-adr-07|SYS-ADR-07]] prohíbe la inferencia de IA en el Anillo 1. `service-input` mantiene esta restricción en todo momento:

- **La detección de formato** es determinista: comparación de extensión seguida de inspección de bytes mágicos. No se utiliza ningún clasificador entrenado.
- **El análisis** lo realizan bibliotecas de propósito específico (oxidize-pdf, pulldown-cmark, docx-rust, calamine) que aplican algoritmos deterministas a secuencias de bytes estructurados. No interviene ningún modelo generativo en ninguna etapa.
- **La normalización de texto** es puramente estructural: unión de espacios en blanco, extracción de texto de flujo de eventos, serialización de celdas. No hay procesamiento semántico.

Como consecuencia de esta restricción, `service-input` no intenta extraer significado del texto analizado. El campo `text` de `ParsedDocument` es una extracción fiel y determinista del contenido textual del documento. La interpretación semántica es responsabilidad del [[service-extraction|Anillo 2]] (`service-extraction`).

## Configuración de despliegue

| Variable | Obligatoria | Valor por defecto | Descripción |
|---|---|---|---|
| `INPUT_MODULE_ID` | Sí | — | Identificador de módulo por inquilino; debe coincidir con `FS_MODULE_ID` en la instancia de service-fs |
| `INPUT_FS_URL` | Sí | — | URL base de service-fs (p. ej., `http://127.0.0.1:9100`) |
| `INPUT_BIND_ADDR` | No | `0.0.0.0:9200` | Dirección y puerto al que se enlaza el servidor HTTP MCP |

El binario es un daemon Tokio de proceso único. Inicia el servidor HTTP axum y atiende las solicitudes MCP entrantes hasta que se termina el proceso.

## Relaciones con otros servicios del Anillo 1

`service-input` es uno de cuatro servicios de ingesta en el límite del Anillo 1. Cada uno atiende un canal de entrada de documentos distinto:

| Servicio | Canal de entrada | Salida |
|---|---|---|
| `service-input` | Documentos genéricos (PDF, DOCX, XLSX, Markdown) | `ParsedDocument` → registro WORM |
| [[service-email]] | Buzones de Microsoft Exchange (EWS SOAP) | MIME sin procesar → registro WORM |
| [[service-people]] | Registros de identidad | Registro `Person` → registro WORM |
| `service-fs` | El propio registro WORM | Proporciona `/v1/append` y `/v1/entries` |

Los cuatro escriben a través de `service-fs`. [[service-extraction]] (Anillo 2) lee desde `service-fs` y aplica análisis asistido por IA aguas abajo, fuera del límite del Anillo 1.

## Véase también

- [[fs-anchor-emitter]] — el servicio de anclaje del registro WORM
- [[three-ring-architecture]] — posición del límite del Anillo 1 y el papel de service-input
- [[worm-ledger-design]] — arquitectura del registro WORM y semántica de adición
- [[service-fs-architecture]] — interfaz de recursos MCP de service-fs
