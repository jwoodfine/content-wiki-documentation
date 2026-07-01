---
schema: foundry-doc-v1
title: "Guía de estilo editorial"
slug: style-guide.es
lang: es
category: internal
type: reference
content_type: reference
quality: complete
short_description: "Referencia interna consolidada para cada tipo de contenido editorial redactado en la plataforma — TOPIC, GUIDE, ARCHITECTURE y los géneros de comunicación interna y documentos legales (correo electrónico, chat, notas de reunión, contrato, CLA, política, README, términos de uso, comentario de ticket, memo, explicador de licencia, inventario, changelog). No se publica en el wiki público; es material solo para colaboradores."
status: active
audience: contributor-internal
bcsc_class: internal-only
last_edited: 2026-07-01
editor: pointsav-engineering
paired_with: style-guide.md
---

> Este documento vive en `.internal/` y no es renderizado por `app-mediakit-knowledge` — el cargador de contenido omite cualquier directorio con nombre punteado. Consolida los dieciséis artículos que antes vivían en `reference/style-guide-*.md` en un único estándar dirigido a colaboradores. El contenido de este documento está dirigido a quienes redactan contenido de la plataforma, no a los lectores del wiki.

## Tema

Un archivo TOPIC explica *qué es* algo — arquitectura, contexto o antecedentes de la plataforma que un lector nuevo necesita para orientarse. No describe cómo operar algo; eso corresponde a un archivo GUIDE.

Este artículo es en sí mismo un TOPIC y sigue la estructura que documenta.

### El estándar editorial

Estas cinco reglas son el estándar editorial ratificado para cada TOPIC. Fueron reconciliadas y ratificadas por el operador el 2026-05-21. Donde cualquier otra guía de este documento — o de [[editorial-language-registers]] — entre en conflicto con una regla siguiente, prevalece la regla.

1. **La longitud de la oración se presupuesta según su función.** Una oración de desarrollo — la que desarrolla un mecanismo o un argumento dentro de una sección del cuerpo — llega a unas 45 palabras como máximo. Una oración de divulgación — el encabezado, una afirmación de cumplimiento, una declaración regulatoria — llega a 25 palabras como máximo. Varíe el ritmo: cada párrafo incluye al menos una oración corta y declarativa.
2. **Los verbos activos describen el mecanismo como hecho presente.** Use la voz activa para describir cómo funciona algo ahora. No la use para afirmar como hecho consumado una afirmación prospectiva — la capacidad, el cronograma o el resultado aún no real conserva `planificado`, `previsto`, `puede` u `objetivo`. No atribuya intención ni emoción humana a un sistema. No hay prohibición de `es`, `son` o `era`.
3. **La analogía es un techo, no una cuota.** Una analogía es opcional. Donde se use, manténgase en una como máximo por cada 300 palabras.
4. **El encabezado es el núcleo informativo; el arco Franklin ordena el cuerpo.** El encabezado adelantado de cuatro párrafos lleva la noticia en aproximadamente el primer 10% del artículo. El arco Franklin — Crisis, luego Búsqueda, luego Avance — rige solo el orden de las secciones del cuerpo.
5. **Se rechaza el registro de marketing SaaS.** El contenido público no adopta la voz promocional de una página de producto de software. Los nombres en clave internos se mantienen internos y no aparecen en el texto público de un TOPIC.

### Dónde viven los TOPICs

| Wiki | Materia | Licencia |
|---|---|---|
| `content-wiki-documentation` | Documentación de la plataforma del proveedor | CC BY 4.0 (pública) |
| `content-wiki-corporate` | Principios corporativos del cliente | CC BY-ND 4.0 |
| `content-wiki-projects` | Narrativas de proyectos del cliente | CC BY-ND 4.0 |

Un TOPIC vive en la wiki cuya materia cubre. Cruzar estos límites en silencio es deriva; plantee la pregunta en lugar de elegir arbitrariamente.

### Pareja bilingüe obligatoria

Cada TOPIC se entrega como pareja: el archivo en inglés y una adaptación estratégica en español (`.es.md`). El archivo en español es adaptación estratégica, no traducción 1:1 — traduzca la orientación que necesita un lector hispanohablante; omita el detalle de implementación más profundo.

### Frontmatter requerido

Cada TOPIC declara sus metadatos en frontmatter YAML. La lista `cites` es obligatoria cuando el artículo hace afirmaciones que se resuelven en instrumentos regulatorios externos, documentos de investigación o especificaciones técnicas.

### Estructura del encabezado adelantado

Un TOPIC abre con un encabezado adelantado de cuatro párrafos. El modelo: el primer párrafo enuncia la propiedad estructural en una oración que satisfaría a un lector institucional con conocimientos financieros leyendo en su teléfono. El segundo párrafo aporta un dato concreto o número que hace verificable el primero. El tercero explica el mecanismo. El cuarto declara por qué importa a un comprador regulado, un auditor o un gestor de riesgos.

| Párrafo | Contenido | Prueba |
|---|---|---|
| 1 — Qué + consecuencia | La propiedad estructural y su consecuencia de cumplimiento o riesgo | ¿Puede un analista leerlo en su teléfono y entender el punto? |
| 2 — Dato concreto | Un dato específico: métrica, fecha, decisión binaria | ¿Es verificable? ¿Hace falsificable el párrafo 1? |
| 3 — Mecanismo | Cómo funciona | ¿Es esta la descripción más simple y precisa del mecanismo? |
| 4 — Por qué importa | Consecuencia para el cumplimiento, la custodia o el riesgo | ¿Sabe un comprador regulado qué acción tomar? |

**Prueba del PDF independiente.** Imprima los párrafos 1–4 de forma aislada y entréguelos a un lector que no verá nada más. El mensaje esencial de cumplimiento o riesgo debe sobrevivir. Si no lo hace, revise el encabezado antes de cualquier otra edición.

### Voz — institucional, no marketing

El estándar es prosa precisa y profesional comprensible para un lector financieramente competente sin formación técnica. Voz activa salvo que la voz pasiva aporte un significado técnico específico. La longitud de la oración sigue el estándar presupuestado arriba — oraciones de desarrollo hasta unas 45 palabras, prosa de divulgación hasta 25 — y cada párrafo incluye al menos una oración corta y declarativa.

La lista de vocabulario prohibido se aplica en su totalidad: `aprovechar`, `empoderar`, `próxima generación`, `líder del sector`, `sin fricciones`, `robusto`, `de vanguardia`.

**Actores y consecuencias nombrados.** Cada oración activa nombra quién hace qué y cuál es la consecuencia si no lo hace. "El Portero centraliza todas las claves API" nombra al actor. "Las claves API se gestionan centralmente" lo oculta. La voz pasiva es útil solo cuando el actor genuinamente no importa; en la mayoría de las oraciones de gobernanza, el actor es el punto.

**Prueba de la oración del director financiero.** Cada oración debe ser útil para un director financiero — alguien que entiende contratos, riesgo y regulación pero no lee código fuente. El detalle de ingeniería puro sin consecuencia empresarial pertenece más adelante en el artículo o en una nota al pie.

**Disciplina "¿y qué?"** Cada párrafo del cuerpo responde a la pregunta: *¿y qué significa esto para un comprador regulado o un ingeniero consciente del riesgo?*

### Registro institucional y de desarrollo: 75/25

Un TOPIC en `content-wiki-documentation` se dirige a dos audiencias simultáneamente: lectores institucionales (comunidad financiera, compradores regulados, responsables de cumplimiento, auditores) y lectores de desarrollo (ingenieros, arquitectos, integradores). El registro objetivo es 75% institucional, 25% de desarrollo.

En la práctica: escriba la afirmación estructural y su consecuencia de cumplimiento antes del detalle de implementación.

### Vocabulario de gobernanza interna

Las palabras **Doctrina** y **Convención** como vocabulario de gobernanza interna nunca aparecen en el cuerpo del texto de un TOPIC ni en los encabezados de sección. Un lector institucional con conocimientos financieros leyendo este wiki debe encontrar la idea subyacente en prosa institucional, no el nombre interno del mecanismo de gobernanza.

Escriba el principio, no la etiqueta:
- En lugar de "según la Doctrina, ninguna IA puede escribir en el grafo de conocimiento" → "ningún componente de IA escribe en el grafo de conocimiento; esa ruta es exclusivamente determinista"

### Lenguaje prospectivo con advertencia

Un TOPIC que describe capacidad, cronograma, resultado para el cliente o acuerdo de gobernanza futuros usa `planificado`, `previsto`, `puede` o `objetivo` — nunca futuro declarativo. Este es el requisito de divulgación continua de la BCSC por `[ni-51-102]` y la disciplina de información prospectiva de `[osc-sn-51-721]`.

### Citar cada afirmación no obvia

La disciplina es auditabilidad, no exhaustividad académica. Un revisor que lea el TOPIC dentro de cinco años debe poder rastrear cada afirmación no obvia hasta su fuente.

### Editar en el mismo archivo

Sin sufijos `_V2` / `_V3` — el historial de Git es el registro de versiones. Esta regla se aplica con todo su peso a los archivos TOPIC porque el renderizador del wiki sirve la versión más reciente confirmada.

### Qué no es un TOPIC

- No es un manual operativo. Las instrucciones operativas viven en archivos GUIDE dentro de la subcarpeta de despliegue que operan.
- No es material de marketing. La audiencia es colaboradores, clientes, reguladores e ingenieros — no compradores que necesitan ser persuadidos.
- No es material solo para uso interno. Lo interno vive en los directorios `.agent/` del espacio de trabajo o en instancias de despliegue, no en una wiki de contenido.

### Véase también

- **Guía** (más abajo)
- [[language-protocol-substrate|Sustrato de protocolo de lenguaje]]
- [[citation-substrate|Sustrato de citación]]
- [[anti-homogenization-discipline|Disciplina anti-homogenización]]

## Guía

Un archivo GUIDE es un manual operativo: cómo ejecutar, configurar o recuperarse de una falla. Le indica al operador qué hacer, en orden, con los comandos exactos que copiará y pegará. No explica el razonamiento detrás del procedimiento; eso corresponde a un archivo TOPIC, cubierto en la sección **Tema** de arriba.

### Ubicación

Los GUIDEs viven dentro de la subcarpeta de despliegue que operan. Hay dos niveles:

| Nivel | Ruta | Propósito |
|---|---|---|
| Catálogo | `customer/woodfine-fleet-deployment/<nombre-despliegue>/guide-*.md` | Define cómo se opera este despliegue. |
| Instancia | `deployments/<instancia>/guide-*.md` | Solo cuando una instancia tiene desviaciones operativas significativas frente a su GUIDE de catálogo. |

Un GUIDE en la raíz de un catálogo de flota, sin subcarpeta de despliegue contenedora, está mal ubicado. Trasládelo a la subcarpeta correspondiente.

### Solo en inglés

Los archivos GUIDE son solo en inglés. Son operativos, no de cara al público — las parejas bilingües añaden costo de mantenimiento sin beneficio para una audiencia de operadores con competencia de trabajo en inglés.

### Estructura obligatoria de seis secciones

Cada GUIDE tiene seis secciones en este orden:

1. **Requisitos previos** — todo lo que el operador debe tener antes de comenzar.
2. **Propósito** — una oración que indica qué logra este GUIDE.
3. **Procedimiento** — pasos numerados en voz imperativa.
4. **Resultado esperado** — la post-condición que este GUIDE pretende establecer; enunciada como un hecho verificable.
5. **Verificación** — la secuencia de comandos que el operador ejecuta para confirmar que el resultado esperado se cumple.
6. **Recuperación** — cómo deshacer el procedimiento si la verificación falla. Nombre el modo de falla, el comando de diagnóstico y los pasos correctivos.

Las secciones que no se aplican no se omiten — explican por qué no se aplican. Una sección de Requisitos previos que no lista nada dice explícitamente: "Sin requisitos previos; el procedimiento es autocontenido."

### Voz imperativa terse

Los GUIDEs usan oraciones más cortas que los TOPICs. Presupuesto de longitud de oración: promedio de catorce palabras, máximo de veinticuatro. Voz imperativa — `ejecute`, `confirme`, `reinicie`, `verifique`. Voz activa siempre; la voz pasiva en un manual operativo oculta quién o qué realiza la acción, lo que importa cuando algo falla.

**Actores nombrados.** Cada paso nombra al agente y al objeto: "el operador ejecuta el siguiente comando", no "el siguiente comando se ejecuta". Cuando un paso cambia el estado de un servicio o sistema, diga qué cambia. Un paso que el operador no puede verificar no ocurrió.

La [[editorial-language-registers|lista de vocabulario prohibido]] se aplica. No tiene lugar en un manual operativo ninguna palabra que no describa algo que el operador pueda verificar.

### Comandos copiables y pegables

Cada comando en un GUIDE está en un bloque de código cercado, solo en su línea, listo para copiar y pegar. El código entre comillas en línea es para referirse a un comando, no para ejecutarlo.

Los marcadores de posición son obvios — `<id-inquilino>`, `<nombre-instancia>`, `<sha-commit>` — nunca `xxx`, `SU_VALOR` ni `[insertar aquí]`.

### Verificación concreta

Cada paso tiene una comprobación que el operador puede ejecutar para confirmar que el paso funcionó. La comprobación es un comando con una salida esperada, no una narración. "Verifique que el servicio esté activo" no es una comprobación. "`systemctl is-active local-doorman.service` devuelve `active`" sí lo es.

### Recuperación concreta

Las instrucciones de recuperación nombran el modo de falla que abordan, el comando de diagnóstico que lo confirma y los pasos correctivos. Mejor escribir "no hay recuperación automática; escale al equipo de guardia" que sugerir al operador que tiene opciones cuando el procedimiento no ha sido pensado hasta el final.

Dos casos especiales se manejan explícitamente:

- **Procedimiento idempotente**: "Este procedimiento es idempotente. Si se interrumpe, reinícielo desde el paso 1 — no hay estado parcial que limpiar."
- **Procedimiento irreversible**: "Esta operación no se puede deshacer. Verifique los requisitos previos y el resultado esperado antes de ejecutar el paso N."

### Qué no es un GUIDE

- No es un TOPIC. El razonamiento o la intención de diseño que motiva un procedimiento vive en un TOPIC.
- No es un script. Un script que el GUIDE invoca vive en el directorio `scripts/` del proyecto; el GUIDE lo referencia por ruta.
- No es un artefacto de cara al público. El detalle operativo pertenece a GUIDEs leídos por operadores con acceso al despliegue.

### Véase también

- **Tema** (más arriba)
- [[language-protocol-substrate|Sustrato de protocolo de lenguaje]]
- [[customer-hostability|Hospedaje por el cliente]]

## Arquitectura

Un archivo `ARCHITECTURE.md` en la raíz de un proyecto explica la posición del proyecto dentro del sistema más amplio, la interfaz que expone, la organización interna de sus módulos y, con igual importancia, lo que el proyecto no hace. La [[root-files-discipline|disciplina de archivos en la raíz]] rige qué archivos compañeros pueden aparecer junto a ARCHITECTURE.md en la raíz del proyecto.

### Cuándo usar esta plantilla

Se utiliza cuando el diseño del proyecto es suficientemente complejo como para que un colaborador nuevo no pueda reconstruir su estructura leyendo únicamente el código fuente. Los proyectos con más de dos módulos significativos, una decisión de capas no obvia, o un contrato de consumidor relevante con otras partes del sistema, requieren un `ARCHITECTURE.md`.

Las utilidades de un solo archivo y los adaptadores delgados generalmente no lo requieren.

### Estructura requerida

La plantilla exige cuatro secciones en este orden:

1. **Position** — dónde se ubica este proyecto en el sistema más amplio, con referencias a sus pares por nombre canónico.
2. **Public surface** — la API, interfaz o contrato que el proyecto expone al resto del sistema.
3. **Module layout** — árbol de directorios anotado de la organización interna del proyecto.
4. **What this is not** — objetivos explícitamente excluidos, para limitar la interpretación del lector.

### Registro

Técnico. Se asume familiaridad con el dominio. Las oraciones son concisas — promedio de dieciocho palabras, máximo treinta. Se aplica la lista de vocabulario prohibido. Los nombres canónicos del Nomenclature Matrix se usan con exactitud.

### Véase también

- **Tema** (más arriba)
- **Guía** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Correo electrónico

Todo correo electrónico externo tiene un único punto. El destinatario comprende qué se le pide al terminar de leer el primer párrafo.

### Cuándo usar esta plantilla

Se usa para cualquier comunicación que salga del espacio de trabajo Foundry, que requiera registro escrito, o que esté dirigida a un destinatario específico externo al equipo. Los mensajes internos a la bandeja de entrada o salida usan el formato de mensaje interno del espacio de trabajo §12. Los mensajes de chat usan la plantilla **Chat**.

### Estructura requerida

**Encabezado** (antes del cuerpo):

```
To:      <nombre y correo del destinatario, o rol>
Subject: <asunto específico — qué trata este correo, no "Actualización">
```

Tres secciones del cuerpo:

1. **Opening** — una oración: contexto y solicitud juntos. El destinatario comprende qué se le pide sin leer más.
2. **Body** — el detalle necesario para responder o actuar. Un punto por párrafo; máximo tres párrafos.
3. **Close** — el siguiente paso concreto y quién lo asume, con fecha donde sea posible. Seguido inmediatamente del cierre.

### Registro

Profesional y llano. El asunto debe ser específico: "Solicitud de NDA — MCorp" en lugar de "Conversación de asociación". Promedio de veinte palabras por oración; máximo treinta y cinco. Voz activa. Se aplica la [[editorial-language-registers|lista de vocabulario prohibido]]. Cuando el destinatario puede ser un inversor actual o potencial, las declaraciones prospectivas sobre la plataforma, los productos o la hoja de ruta llevan lenguaje de "planificado / previsto / puede / objetivo".

### Véase también

- **Chat** (más abajo)
- **Memo** (más abajo)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Chat

Un mensaje de chat lleva un único punto. Si se necesita un segundo punto, se envía un segundo mensaje.

### Cuándo usar esta plantilla

Se usa para comunicaciones cortas, oportunas y de bajo impacto dirigidas a destinatarios presentes o que estarán presentes próximamente en la misma plataforma. Si el contenido debe ser rastreable, recuperable o procesado por alguien que no está presente, se usa un **comentario de ticket**, un **correo electrónico** o un mensaje de bandeja de entrada.

### Estructura requerida

**Encabezado opcional:**

```
Channel: #<nombre-del-canal>   [o]   To: <@destinatario>
```

Cuerpo: un punto, máximo tres oraciones. Si incluye una solicitud, va en la última oración como pregunta directa. Sin despedida. Sin párrafos. Sin múltiples temas en un solo mensaje.

### Registro

Conversacional pero profesional. Las contracciones son aceptables. Los emojis son aceptables cuando reemplazan una palabra o expresan un tono genuino, no como decoración. Las respuestas de una línea son preferibles. Si se necesita un párrafo, la respuesta pertenece a un comentario de ticket o correo electrónico.

### Véase también

- **Correo electrónico** (más arriba)
- **Comentario de ticket** (más abajo)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Notas de reunión

Las notas de reunión existen para los elementos de acción y las decisiones. Todo lo demás es material de archivo.

### Cuándo usar esta plantilla

Se usan notas para toda reunión que produzca decisiones o elementos de acción. Las verificaciones informales breves que no producen ninguno no requieren notas: un mensaje de **chat** al canal es suficiente. Son obligatorias cuando se toma una decisión que afecta el alcance, el cronograma o la propiedad del trabajo, o cuando se asigna un elemento de acción a una persona nombrada.

### Estructura requerida

**Bloque de encabezado** (antes de cualquier sección):

```
Meeting:   <título descriptivo — no "Sync" ni "Check-in">
Date:      <YYYY-MM-DD>
Attendees: <nombres o roles, separados por coma>
```

Cuatro secciones:

1. **Agenda** — temas listados antes de la reunión. Un ítem por línea. Marcados con ✓ si se trataron, — si se aplazaron.
2. **Decisions** — lista con viñetas de decisiones discretas tomadas. Cada viñeta es autónoma y legible sin el contexto de las notas.
3. **Action items** — tabla: `Owner` \| `Action` \| `Due`. Una fila por ítem. `Due` es `TBD` si no se fijó fecha; nunca en blanco. "Alguien" no es un responsable aceptable.
4. **Notes** — opcional. Contexto que apoya las decisiones o elementos de acción. Comprimir agresivamente: tres oraciones suele ser suficiente.

### Registro

Las decisiones se expresan como hechos consumados. Los elementos de acción usan forma imperativa con un responsable específico. Las notas son mínimas en [[editorial-language-registers|prosa]]: contexto, no transcripción.

### Véase también

- **Comentario de ticket** (más abajo)
- **Memo** (más abajo)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Contrato

Un contrato nombra a sus partes, define sus términos y establece a qué está obligada cada parte. Cada cláusula es un compromiso o una condición; nada más.

### Cuándo usar esta plantilla

Se usa cuando se requiere un acuerdo formal vinculante entre partes nombradas, cuando las obligaciones, la vigencia y las condiciones de terminación deben ser explícitas y rastreables. Los acuerdos operativos informales entre miembros del equipo no requieren un contrato — un **memo** o un **comentario de ticket** los registra. Los acuerdos que obligan a una entidad legal requieren revisión de gobernanza antes de cualquier firma.

### Estructura requerida

Seis secciones en orden:

1. **Parties** — nombres legales completos, direcciones registradas y nombres abreviados definidos de cada parte.
2. **Effective date** — la fecha en que entra en vigor el acuerdo. Si está condicionada a una firma, indicar "la fecha de la última firma."
3. **Recitals** — cláusulas "Considerando que": contexto e intención. Dos a cinco. No son obligaciones.
4. **Definitions** — cada término definido, establecido una sola vez. Los términos definidos se escriben en mayúscula en todo el contrato.
5. **Terms** — las obligaciones sustantivas: qué debe hacer cada parte, cuándo y bajo qué condiciones. Cláusulas numeradas.
6. **Term and termination** — duración del acuerdo, cómo puede terminarse y qué ocurre al terminarse.

### Registro

Legal-llano. Voz activa donde sea posible. Sin "en este documento" ni "sin perjuicio de lo anterior" cuando existen alternativas llanas. Todo acuerdo que obligue a una entidad legal es revisado por el administrador del sistema antes de cualquier firma.

### Véase también

- **CLA** (más abajo)
- **Política** (más abajo)
- **Términos de uso** (más abajo)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## CLA

Un CLA transfiere derechos específicos de propiedad intelectual de un contribuidor al proyecto. El texto canónico está gobernado por `factory-release-engineering`; esta plantilla es para redactar o explicar uno, no para ejecutarlo.

### Cuándo usar esta plantilla

Se usa cuando un proyecto de código abierto en `pointsav-monorepo` acepta contribuciones externas y necesita un marco de contribución, cuando los derechos de un contribuidor deben ser explícitos para satisfacer un requisito de licencia, o cuando se necesita una revisión de gobernanza de un CLA existente. El texto canónico del CLA es mantenido por `factory-release-engineering`: no redactar un CLA para ejecución sin revisión de gobernanza de **Política**.

### Estructura requerida

**Bloque de encabezado:**

```
Agreement:   Contributor License Agreement — <nombre del proyecto>
Contributor: <nombre legal completo o nombre de entidad>
```

Cinco secciones:

1. **Definitions** — tres términos definidos: Contribution (lo que el contribuidor envía), Project (a lo que contribuye), Contributor (quién acuerda). Definidos exactamente una vez.
2. **Grant of copyright license** — los derechos de autor específicos que el Contribuidor otorga al Proyecto. Mínimo: reproducir, preparar obras derivadas, exhibir públicamente, ejecutar públicamente, distribuir.
3. **Grant of patent license** — cualquier derecho de patente necesariamente infringido por la Contribución, con cláusula de terminación defensiva incluida.
4. **Representations** — las declaraciones del Contribuidor de que tiene derecho a realizar la Contribución. Deben ser concretas, no vagas.
5. **Scope** — qué cubre el acuerdo y qué no cubre explícitamente.

### Registro

Legal-llano. Los términos definidos se escriben en mayúscula. Las declaraciones en Representations deben ser precisas: las declaraciones vagas reducen la [[disclosure-substrate|aplicabilidad]] y crean ambigüedad.

### Véase también

- **Contrato** (más arriba)
- **Explicador de licencia** (más abajo)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Política

Una política establece qué se requiere, quién está obligado y qué ocurre cuando se viola la regla. Cada oración de una política es una regla o el soporte de una regla. Se diferencia de un ADR (que registra una decisión arquitectónica puntual) — véase [[architecture-decisions|Decisiones de Arquitectura]].

### Cuándo usar esta plantilla

Se usa una política cuando el comportamiento debe ser uniforme en un equipo, proyecto u organización, cuando la desviación tiene consecuencias reales que deben establecerse, y cuando la regla necesita una cadencia de revisión para no quedar obsoleta en silencio. No se escribe una política para una preferencia o guía; una guía lleva "preferido" o "recomendado" y no implica aplicación.

### Estructura requerida

Cinco secciones en orden:

1. **Scope** — a quién y qué aplica esta política. Roles, sistemas o contextos nombrados. Explícito sobre lo que no aplica.
2. **Policy** — las reglas, numeradas. Cada regla es una declaración completa y autónoma. La primera palabra es una obligación: "Todo X debe…", "Ningún Y puede…", "Todo Z está obligado a…".
3. **Enforcement** — qué ocurre cuando se viola una regla. Debe nombrar una consecuencia o un proceso, no un vago "será abordado."
4. **Review** — con qué frecuencia y por quién se revisa esta política. Mínimo anual.
5. **See also** — vínculos a los ADR, convenciones o leyes que esta política implementa o requiere.

### Registro

Legal-llano. Voz activa. Sin conjeturas: "debe" y "no puede" para requisitos. "Debería" y "se recomienda" no son lenguaje de política. Máximo veinticinco palabras por regla.

### Véase también

- [[architecture-decisions|SYS-ADR-07 — Sin IA en datos estructurados]]
- **Arquitectura** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## README

Un archivo `README.md` es lo primero que lee un colaborador o sistema automatizado al ingresar a un repositorio. Responde tres preguntas en orden: qué es esto, qué necesito saber para usarlo y dónde busco más información. La [[root-files-discipline|disciplina de archivos en la raíz]] rige qué archivos compañeros pueden aparecer junto al README en la raíz de un repositorio.

### Cuándo usar esta plantilla

Toda raíz de repositorio debe incluir un `README.md`. Los proyectos dentro de un monorepo (`pointsav-monorepo/<prefijo>-<nombre>/`) incluyen su propio `README.md` en la raíz cuando son lo suficientemente significativos para ser abordados de forma independiente. Los repositorios con contenido bilingüe (conforme al §6 del espacio de trabajo) también incluyen un `README.es.md` al mismo nivel.

### Estructura requerida

La plantilla exige cinco secciones en este orden:

1. **Opening** — un párrafo: qué es este repositorio o proyecto y para quién está dirigido. Sin encabezados antes de este párrafo.
2. **What this is** — alcance, no características. De dos a cuatro oraciones.
3. **Layout** — árbol de directorios anotado. Una frase por entrada. Describe estructura, no comportamiento.
4. **Using it** — la secuencia mínima para leer, ejecutar o construir el contenido. Requisitos previos, luego comandos, luego resultado esperado.
5. **Where to look next** — lista de apuntadores a documentación más detallada.

### Registro

Inglés llano, dirigido directamente al lector. Promedio de veinte palabras por oración; ninguna supera las cuarenta. Se aplica la lista de vocabulario prohibido. Los pares bilingües son adaptaciones estratégicas, no traducciones literales: la versión en español puede reestructurarse y reformularse para un contexto diferente mientras mantiene el mismo contenido factual.

### Véase también

- **Tema** (más arriba)
- **Guía** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Términos de uso

Los términos de uso establecen qué puede hacer un usuario con un servicio, qué no puede hacer y qué le debe el servicio a cambio. El uso del servicio constituye aceptación.

### Cuándo usar esta plantilla

Se usan términos de uso cuando un servicio o sitio se pone a disposición de usuarios fuera del espacio de trabajo Foundry, cuando los usos permitidos y prohibidos del servicio deben quedar registrados, y cuando las limitaciones de responsabilidad y las exenciones de garantías deben ser declaradas formalmente. Las herramientas internas no requieren términos de uso públicos: una **política** cubre las obligaciones de uso interno. Todo documento de términos de uso ejecutado en esta plataforma es revisado por `factory-release-engineering` antes de su publicación.

### Estructura requerida

**Cláusula de apertura** (antes de cualquier sección): una oración que establece qué servicio rigen estos términos y que el uso del servicio constituye aceptación de estos términos.

Cinco secciones en orden:

1. **Definitions** — cada término definido, establecido una sola vez. En mayúscula tras su primera definición.
2. **Acceptance** — cómo acepta el usuario los términos y qué obliga esa aceptación.
3. **Use of the service** — usos permitidos, usos prohibidos y obligaciones del usuario. Numerados para rastreabilidad.
4. **Liability and disclaimers** — la exención de garantías y la limitación de responsabilidad. En lenguaje llano; la jerga legal excesiva reduce la aplicabilidad. Las formulaciones estándar pueden usarse pero deben ir seguidas de un equivalente en lenguaje llano.
5. **Changes to these terms** — cómo pueden cambiar los términos, qué constituye notificación y cuándo entran en vigor los cambios.

### Registro

Legal-llano. Los términos definidos en mayúscula en cada uso posterior. Donde el servicio toca material de inversión o [[disclosure-substrate|divulgación]], las declaraciones prospectivas sobre funciones del servicio o hoja de ruta llevan lenguaje de "planificado / previsto / puede / objetivo", conforme a las obligaciones canadienses de divulgación continua en materia de valores.

### Véase también

- **Política** (más arriba)
- **Contrato** (más arriba)
- **CLA** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Comentario de ticket

Un comentario de ticket registra un cambio de estado o una decisión, no un pensamiento. Todo comentario hace avanzar el ticket.

### Cuándo usar esta plantilla

Se escribe un comentario cuando el estado del trabajo cambió y los interesados necesitan saberlo, cuando se tomó una decisión que afecta al ticket, cuando se identificó o resolvió un bloqueo, o cuando se completó una acción y la finalización debe quedar registrada. No se comenta para decir que se está trabajando en el ítem: se actualiza el campo de estado.

### Estructura requerida

**Bloque de encabezado** (antes del cuerpo):

```
Ticket: <id o título del ticket>
Status: <nuevo estado — Open | In progress | Blocked | Review | Done>
```

Dos secciones:

1. **What changed** — uno a tres oraciones: el cambio específico en el estado, la decisión tomada o el hecho establecido. Nombra el artefacto, SHA de commit o decisión explícitamente.
2. **Next** — el siguiente paso concreto con responsable. Si el ticket está Done, "Next" es "Closed."

### Registro

Factual y breve. Tiempo pasado para lo que cambió; tiempo presente o futuro para los pasos siguientes. Sin conjeturas. Los valores del campo Status son un conjunto cerrado: `Open`, `In progress`, `Blocked`, `Review`, `Done`. Si "What changed" requiere más de tres oraciones, el cambio es suficientemente complejo para un brief o un **memo**; referenciar desde el comentario.

### Véase también

- **Chat** (más arriba)
- **Notas de reunión** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Memo

Un memo registra una decisión, análisis o recomendación dirigida a una audiencia nombrada. Es completo cuando el lector sabe qué se decidió y qué ocurre a continuación, sin necesidad de consultar ningún otro documento. Para la disciplina de registro y tono aplicada a todos los artefactos en prosa, véase [[editorial-language-registers|registros de lenguaje editorial]].

### Cuándo usar esta plantilla

Se usa un memo cuando una decisión ha sido tomada y debe comunicarse con el análisis que la respaldó, cuando una recomendación está lista para un tomador de decisiones nombrado y no puede entregarse en un solo párrafo, o cuando una pregunta compleja ha sido resuelta y la resolución debe quedar registrada. No se usa para debate en curso, estado de proyectos ni preguntas sin resolver.

### Estructura requerida

**Bloque de encabezado** (antes de cualquier sección):

```
To:   <destinatario>
From: <autor>
Date: <YYYY-MM-DD>
Re:   <asunto en una línea — específico y accionable>
```

Cinco secciones en orden:

1. **Summary** — la conclusión, expresada primero. Uno a tres oraciones. El lector que solo lea esta sección debe poder actuar sobre ella.
2. **Context** — los hechos necesarios para evaluar la recomendación. Solo lo que es relevante, no la historia completa.
3. **Analysis** — el razonamiento, estructurado en puntos numerados o párrafos cortos. Reconoce el contraargumento más sólido y explica por qué no fue decisivo.
4. **Recommendation** — la acción específica solicitada, con responsable y plazo. Un memo sin recomendación es un brief; reestructurar en consecuencia.
5. **Next steps** — acciones concretas de seguimiento con responsables y fechas.

### Registro

Prosa profesional, no legalismo. La recomendación va antes del análisis. El campo `Re:` debe ser específico y accionable. Promedio de veintidós palabras por oración; máximo cuarenta. Voz activa. Se aplica la lista de vocabulario prohibido.

### Véase también

- **Tema** (más arriba)
- **Guía** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Explicador de licencia

Un explicador de [[disclosure-substrate|licencia]] traduce un instrumento legal a términos llanos. No es la licencia. Si el explicador y la licencia entran en conflicto, la licencia prevalece.

### Cuándo usar esta plantilla

Se escribe un explicador de licencia cuando un repositorio lleva una licencia que afecta a colaboradores o consumidores de maneras no obvias, o cuando la audiencia no está compuesta por profesionales legales. No es sustituto de una revisión legal: los acuerdos que obligan a personas u organizaciones deben revisarse a través de `factory-release-engineering` o el administrador del sistema antes de su publicación.

### Estructura requerida

Cinco secciones en orden:

1. **Lede** — uno a dos oraciones: qué licencia es esta y qué pretende lograr. Sin jerga legal.
2. **What it permits** — lista con viñetas de lo que esta licencia permite explícitamente. Verbos llanos: "Usar comercialmente", "Modificar el código fuente".
3. **What it requires** — lista con viñetas de condiciones. Verbos llanos: "Incluir el aviso de derechos de autor", "Declarar los cambios realizados".
4. **What it forbids** — lista con viñetas de restricciones. Verbos llanos. Puede omitirse si la licencia no prohíbe nada.
5. **Where binding text lives** — vínculo directo al documento de licencia formal y declaración de que el texto formal prevalece ante cualquier discrepancia.

### Registro

Inglés llano. Sin "aforementioned" ni "notwithstanding." Promedio de dieciocho palabras por oración; máximo treinta. Las viñetas son frases imperativas que comienzan con un verbo, no oraciones completas.

### Véase también

- **Política** (más arriba)
- **CLA** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Inventario

Un inventario es un conteo fechado de lo que existe, en qué estado se encuentra y de qué tipo es. No es un plan ni un registro de cambios. Para la disciplina de [[citation-substrate|citas]] que rige cómo los inventarios referencian otros documentos, consulte el sustrato de citas.

### Cuándo usar esta plantilla

Se usa un inventario cuando se necesita un recuento para comprender el tamaño de una tarea de migración, limpieza o auditoría, o cuando la clasificación en sí misma es el entregable, o cuando se necesita una instantánea antes de un cambio estructural para registrar el estado anterior. Los inventarios son instantáneas: llevan fecha, envejecen y son reemplazados por uno nuevo cuando el alcance cambia significativamente.

### Estructura requerida

Tres secciones en orden:

1. **Opening** — un párrafo: qué alcance fue inventariado, a qué fecha y qué revela el recuento a alto nivel.
2. **Inventory table** — la enumeración. Columnas: `Item` (nombre canónico), `State` (enumeración cerrada), `Type` (enumeración cerrada), `Notes` (máximo una cláusula).
3. **Summary** — recuentos por estado y tipo. Totales. Puede incluir un apuntador de "acción siguiente" si el inventario es la entrada para una migración o auditoría.

Sección opcional **Classification vocabulary** cuando los valores de State y Type no son evidentes por sí mismos.

### Disciplina de la tabla

Una fila por ítem. Sin celdas combinadas. Los valores de `State` y `Type` provienen de enumeraciones cerradas. La columna Notes admite máximo una cláusula.

### Registro

Factual. Sin interpretación en la tabla: las filas son observaciones, no recomendaciones. Fechas en ISO 8601. Nombres canónicos del Nomenclature Matrix.

### Véase también

- **README** (más arriba)
- **Memo** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]

## Changelog

Un changelog responde una pregunta para cada versión: qué cambió, expresado en una línea, desde el punto de vista del lector. La [[root-files-discipline|disciplina de archivos en la raíz]] rige cuándo es obligatorio un `CHANGELOG.md`.

### Cuándo usar esta plantilla

Todo repositorio que lleva números de versión usa un `CHANGELOG.md`. El archivo se crea cuando existe la primera entrada significativa, no como marcador de posición. Los repositorios que no versionan pueden omitirlo y rastrear los cambios significativos en `NEXT.md` o `cleanup-log.md`.

### Estructura requerida

Lista plana de bloques de versión, el más reciente al inicio:

```markdown
## M.m.P — YYYY-MM-DD

- <entrada en una línea, dirigida al lector>
```

Cada bloque lleva encabezado `##` con número de versión y fecha en ISO 8601 en la misma línea. Una viñeta por cambio significativo, orientada al lector: describe el efecto, no el mecanismo. Se pueden agregar etiquetas de agrupación (`### Added`, `### Fixed`, `### Changed`) cuando un bloque tiene más de cinco entradas; se omiten para cinco o menos.

### Qué incluir y qué excluir

**Incluir:** nuevas capacidades disponibles para los consumidores, cambios que rompen la compatibilidad, correcciones con impacto visible, cambios estructurales importantes.

**Excluir:** refactorizaciones internas sin efecto visible para el consumidor, cambios en pruebas o CI, commits solo de documentación, commits de actualización de versión.

### Registro

Llano, activo, tiempo presente: "Agrega soporte para X", "Corrige el error de análisis Y." Máximo veinte palabras por entrada. ISO 8601 para fechas. No "hemos agregado" ni "esta versión incluye."

### Véase también

- **README** (más arriba)
- **Arquitectura** (más arriba)
- [[language-protocol-substrate|Sustrato del Protocolo de Lenguaje]]
