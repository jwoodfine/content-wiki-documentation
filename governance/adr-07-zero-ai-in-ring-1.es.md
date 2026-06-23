---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: adr-07-zero-ai-in-ring-1
title: "SYS-ADR-07: Cero IA en el Ring 1"
short_description: "SYS-ADR-07 prohíbe la inferencia de IA en todos los servicios de ingestión del Ring 1, garantizando operaciones exclusivamente deterministas en la ruta de escritura WORM para asegurar auditabilidad y composabilidad."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: adr-07-zero-ai-in-ring-1.md
category: governance
status: active
quality: complete
last_edited: 2026-06-23
cites: []
---

# SYS-ADR-07: Cero IA en el Ring 1

SYS-ADR-07 es una decisión arquitectónica que prohíbe la inferencia de IA en los
servicios de ingestión del Ring 1. No es una preferencia ni una directriz — es una
restricción estricta que los cuatro servicios del Ring 1 implementan en código, sin
ninguna excepción. Este artículo explica la restricción, el razonamiento que la
sustenta y qué significa "cero IA" en la práctica para cada servicio.

---

## 1. Qué es el Ring 1

El Ring 1 es la frontera exterior del plano de datos. Es el conjunto de servicios que
aceptan entradas sin procesar desde el exterior del sistema y las escriben en
almacenamiento duradero e inmutable. En la implementación actual, el Ring 1 está
compuesto por cuatro servicios:

| Servicio | Función |
|---|---|
| `service-fs` | Libro mayor inmutable WORM — todas las escrituras del Ring 1 llegan aquí |
| `service-people` | Ingestión de identidades — registros de Person, Anchor y Claim |
| `service-email` | Ingestión de correo electrónico vía EWS (Exchange Web Services SOAP) |
| `service-input` | Ingestión de documentos — PDF, Markdown, DOCX, XLSX |

Estos servicios son el primer punto de contacto para los datos que entran al sistema.
Todo lo que escriben en `service-fs` pasa a formar parte del registro permanente y
auditable. Nada de lo que se escribe en el libro mayor WORM puede eliminarse ni
modificarse.

La consecuencia es que el estándar de corrección en el Ring 1 difiere del estándar de
corrección en el resto del sistema. Los errores en el Ring 1 son permanentes.

---

## 2. Por qué solo operaciones deterministas

Tres razones impulsan SYS-ADR-07.

**Pista de auditoría verificable.** La cadena de hashes de `service-fs` y la firma de
punto de control Ed25519 crean un registro verificable de todo lo que se escribe en el
Ring 1. Un tercero puede verificar la cadena desde el hash de origen hasta el extremo
actual sin necesidad de reproducir ningún estado de modelo. Si las operaciones del
Ring 1 fueran derivadas de IA, esta verificación quedaría incompleta: los auditores
necesitarían acceso a los pesos del modelo, la configuración de muestreo y el estado
de inferencia en el momento en que se escribió cada registro para entender qué decidió
el sistema y por qué. Las operaciones deterministas no tienen tal dependencia — el
algoritmo es la especificación completa.

**Garantía de composabilidad.** Los resultados del Ring 1 son consumidos por los
servicios del Ring 2 (`service-extraction`, `service-content`) y la inteligencia del
Ring 3 (`service-slm`). Para que el Ring 2 y el Ring 3 puedan componer de forma fiable
los datos del Ring 1, ambos deben ser capaces de razonar sobre lo que produjo el
Ring 1. Un resultado del Ring 1 derivado de IA conlleva una incertidumbre implícita que
se propaga a través de todos los cálculos posteriores. Un UUID derivado
deterministamente a partir de una dirección de correo electrónico en minúsculas no
lleva consigo esa incertidumbre — es el mismo valor en todo lugar y en todo momento.

**Postura regulatoria.** Los registros de auditoría inmutables en sectores regulados
(servicios financieros, sector legal, sanidad) requieren la capacidad de explicar
exactamente qué se registró y exactamente cómo se derivó. Los algoritmos deterministas
(SHA-256, UUIDv5, expresiones regulares, firma Ed25519) tienen especificaciones exactas
y auditables. La inferencia de IA no las tiene.

---

## 3. Qué significa "Cero IA" en la práctica

SYS-ADR-07 prohíbe lo siguiente en el Ring 1:

- Llamadas de inferencia a LLM (vía API o inferencia local)
- Cálculos de similitud basados en vectores de incrustación
- Pesos de modelo en la imagen del proceso
- Clasificación probabilística o extracción de entidades

Lo que sí está permitido:

- Expresiones regulares (correspondencia de patrones determinista)
- SHA-256 y otras funciones de hash criptográficas
- UUIDv5 (determinista a partir de un espacio de nombres fijo y una entrada dada)
- Firma y verificación Ed25519
- Análisis sintáctico de JSON, XML y OOXML (estructural, no semántico)
- Puntuaciones de confianza asignadas por regla, no por un modelo

La distinción es: cálculos cuyo resultado está completamente determinado por su entrada
y un algoritmo fijo (permitido) frente a cálculos cuyo resultado depende de pesos
aprendidos o muestreo estocástico (prohibido).

---

## 4. Instancias de implementación

### service-fs

Todas las operaciones en `service-fs` son criptografía pura y operaciones de entrada/salida
de ficheros:

- **Append** — escritura atómica D4 (`.tmp` → fsync → rename → chmod 0o444);
  hash de entrada SHA-256 encadenado desde el anterior
- **Checkpoint** — hash raíz SHA-256 sobre la cadena; firma Ed25519 con clave
  suministrada por el operador; formato de cable C2SP signed-note
- **Anchor-emitter** — par de claves Ed25519 efímero por ejecución; POST
  `hashedRekordRequestV002` de Sigstore; hash determinista del payload del punto
  de control

Sin modelo, sin inferencia, sin probabilidad. Cada operación produce un único resultado
determinista para una entrada y clave dadas.

### service-people

La extracción de identidades usa una única expresión regular compilada:

```
(?i)[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}
```

La derivación de UUID usa UUIDv5:

```
target_uuid = UUIDv5(NAMESPACE_DNS, lowercase(email))
```

Las puntuaciones de confianza se asignan por regla: `1.0` para una coincidencia con la
expresión regular. Ningún modelo produce una puntuación entre 0 y 1 basada en
representaciones aprendidas.

La detección de conflictos compara UUIDs por igualdad. Cuando dos operaciones de
ingestión vincularían la misma dirección de correo electrónico a UUIDs diferentes, el
sistema expone el conflicto al llamante — no invoca inferencia para resolverlo.

### service-email

`service-email` lee el correo electrónico de Microsoft Exchange vía el protocolo SOAP
de EWS (Exchange Web Services). Las operaciones son:

- Análisis sintáctico de cadenas XML de sobres SOAP (estructural, no semántico)
- Decodificación Base64 del contenido MIME
- Autenticación HTTP bearer usando un token pre-adquirido (`AZURE_ACCESS_TOKEN`)

Sin clasificación de contenido, sin extracción de entidades, sin puntuación de spam. El
servicio lee lo que proporciona Exchange y lo escribe en `service-fs`. Cualquier
inteligencia aplicada al contenido del correo ocurre en el nivel inferior, en el Ring 2
o Ring 3, leyendo desde el libro mayor WORM — nunca de forma integrada durante la
ingestión.

### service-input

`service-input` analiza documentos y extrae su contenido textual:

- **PDF** — análisis sintáctico estructural vía `oxidize-pdf`; extrae tramos de texto
- **Markdown** — análisis sintáctico por flujo de eventos vía `pulldown-cmark`; elimina
  etiquetas HTML
- **DOCX** — extracción de párrafos mediante ZIP + XML vía `docx-rust`
- **XLSX** — extracción de todas las hojas en formato delimitado por tabuladores vía
  `calamine`

En todos los casos, el analizador lee la estructura definida por el formato y emite
texto. Sin interpretación semántica, sin resumen, sin clasificación. El texto extraído
sin procesar es lo que llega a `service-fs`.

---

## 5. La frontera del Ring 2

La inteligencia entra al sistema en el Ring 2. `service-extraction` lee desde el Ring 1
vía MCP y aplica combinadores de análisis deterministas más, opcionalmente, llamadas de
inferencia del Ring 3. Sus resultados son artefactos del Ring 2 — no vuelven a escribir
en las entradas del libro mayor WORM del Ring 1; crean nuevas entradas etiquetadas con
procedencia del Ring 2.

Esta frontera es estructural, no basada en convención. Los servicios del Ring 2 acceden
al Ring 1 vía llamadas HTTP MCP. No existe ninguna ruta dentro del proceso que vaya
desde la inferencia del Ring 2 de vuelta al almacenamiento del Ring 1. Un servicio del
Ring 2 que desee anotar un registro del Ring 1 crea un nuevo registro del Ring 2 que
hace referencia a la entrada del Ring 1 — no modifica la entrada del Ring 1.

---

## 6. SYS-ADR-10 (F12): Exposición de la ambigüedad al operador

Cuando el procesamiento determinista encuentra una situación que no puede resolverse
algorítmicamente — por ejemplo, un conflicto en `service-people` donde la misma
dirección de correo electrónico se asignaría a dos UUIDs diferentes — el sistema
devuelve un error al llamante. No realiza ninguna de las siguientes acciones:

- Elegir silenciosamente uno de los registros en conflicto
- Aplicar un modelo para adivinar cuál es "más probable"
- Fusionar los registros en función de una similitud heurística

El requisito F12 (SYS-ADR-10) exige que la ambigüedad se exponga al operador. La
resolución de la ambigüedad es una acción explícita del operador, no un comportamiento
automático del sistema. Esto constituye una garantía de composabilidad: los operadores
pueden razonar sobre lo que decidió el sistema, porque toda decisión no trivial pasa
por el operador.

---

## 7. Ring 3: IA Compositiva

El Ring 3 (`service-slm`, el Doorman) es donde está previsto que se ejecute la
inferencia de IA. El Ring 3 es arquitectónicamente opcional — los Rings 1 y 2
funcionan completamente sin él. El diseño previsto es que el Ring 3 consulte al Ring 2,
que a su vez lee del Ring 1, formando una composición en capas.

Que el Ring 3 opere en la capa de sesión no constituye una excepción al Ring 1. Una
consulta del Ring 3 a los datos del Ring 1 (vía Ring 2) usa la misma interfaz MCP
determinista que cualquier otro cliente del Ring 2. El Ring 3 no puede eludir la
disciplina de escritura del Ring 1; lee los registros terminados del Ring 1 vía la
misma API que todo lo demás.

El modelo compositivo es: ingestión determinista (Ring 1) → procesamiento determinista
(Ring 2) → inteligencia opcional en tiempo de consulta (Ring 3). La inteligencia añade
valor, no es estructuralmente imprescindible, y nunca accede a la ruta de escritura
inmutable.
