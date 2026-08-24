---
schema: foundry-doc-v1
title: "Aplicación de entrada de consola"
slug: app-console-input
category: applications
type: app
content_type: topic
quality: complete
index_group: input-and-developer-surfaces
short_description: "app-console-input es la superficie F12 en os-console — una ruta, una confirmación y un envío, a través de los cuales los archivos externos sin procesar ingresan a un Totebox antes de sellarse en el libro mayor verificado."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: app-console-input.md
cites:
 - ni-51-102
 - np-51-201
references:
  - id: 1
    text: "NIST, Marco de Gestión de Riesgos de Inteligencia Artificial (AI RMF 1.0), NIST AI 100-1, enero de 2023. Sección 5: Supervisión humana y responsabilidad en implementaciones de IA."
    url: "https://doi.org/10.6028/NIST.AI.100-1"
  - id: 2
    text: "Organización Internacional de Normalización, ISO/IEC 27001:2022 — Sistemas de gestión de la seguridad de la información, Anexo A.8.15: Registro."
    url: "https://www.iso.org/standard/82875.html"
---

`app-console-input` es la superficie F12 en [[os-console|os-console]] — el único camino a través del cual los archivos externos sin procesar ingresan a un [[totebox-os|Totebox]] antes de sellarse en el [[worm-ledger-design|libro mayor WORM]]. La superficie responsabiliza al operador por cada archivo que ingresa al libro mayor: nada se envía sin una decisión explícita del operador confirmada por teclado, de modo que cada acto fiduciario lleva la firma del operador en el [[worm-ledger-design|registro de auditoría]]. Al finalizar este artículo, el lector comprenderá el flujo de trabajo F12 y las propiedades de auditoría que protege esta puerta.

## Cómo se desarrolla una sesión F12

Una sesión recorre cuatro estados en orden: **Entrada**, donde el operador escribe la ruta del archivo; **Confirmar**, una única solicitud de sí/no que muestra la ruta exacta; **Enviando**, mientras el cartucho publica al endpoint de ingesta y espera; y **Listo** (o **Error** si falla). Cancelar desde Entrada o Confirmar regresa a Entrada sin que se envíe nada.

| Paso | Acción del operador | Respuesta del sistema |
|---|---|---|
| Entrada | Escribir una ruta de archivo | El cartucho acepta la entrada de ruta en texto libre |
| Confirmar | Presionar Y para enviar, N o Esc para cancelar | El cartucho muestra la ruta exacta para una decisión final de sí/no |
| Enviando | Esperar | El cartucho publica la ruta del archivo, la identidad del operador y el tenant al endpoint de ingesta por HTTP |
| Listo | — | El cartucho registra el resultado — éxito, advertencia o error — en un registro de auditoría local, y extiende un libro mayor local incremental con el envío |

### Cada envío queda firmado y encadenado

La interacción es solo con teclado y deliberadamente estrecha: una ruta, una confirmación, un envío. No hay modo de importación masiva ni formulario de metadatos — un documento se envía a través de esta secuencia exacta o nunca ingresa al libro mayor.

Dos registros de auditoría documentan cada envío, no uno. Localmente, el cartucho mantiene un hash incremental — cada entrada de envío exitoso se encadena a la anterior (`nueva_raíz = SHA256(raíz_previa ‖ id_de_carga)`), de modo que la secuencia local de envíos es verificable de forma independiente, entrada por entrada. El cartucho también escribe un registro de auditoría local — marca de tiempo, operador, tenant, ruta, referencia del libro mayor y resultado — visible en cualquier momento desde la pantalla de Entrada. Por separado, el archivo mismo se anexa al servicio de libro mayor de la plataforma, que devuelve su propia referencia al cartucho.

## Por qué el paso de confirmación es arquitectónicamente obligatorio

Si un archivo ingresara al libro mayor sin que el operador lo confirmara explícitamente, el libro mayor llevaría una entrada sin autor humano responsable a partir de ese punto. No existe un paso posterior que repare esto — la entrada ya lleva una marca de tiempo que afirma una decisión que ningún ser humano tomó.

### Decisiones arquitectónicas que refuerzan la puerta

[[architecture-decisions|SYS-ADR-10]] hace que F12 sea obligatorio precisamente porque este modo de fallo es estructural, no probabilístico: cualquier camino que permita que un archivo llegue al libro mayor sin una confirmación explícita del operador crea una entrada sin responsable. [[architecture-decisions|SYS-ADR-07]] extiende el principio a los datos estructurados de manera más amplia — ningún registro producido por IA ingresa a un libro mayor verificado sin un paso de confirmación humana. [[architecture-decisions|SYS-ADR-19]] cierra el camino restante — sin publicación automatizada en libros mayores verificados, independientemente de la puntuación de confianza.

Los fiduciarios institucionales — gestores de activos, abogados, entidades financieras reguladas — requieren un registro de auditoría que puedan defender bajo escrutinio. La puerta F12 es lo que hace posible esa defensa: cada envío se remonta a un operador específico, una confirmación específica y una marca de tiempo específica. [^2]

## Lo que la superficie F12 no es

F12 no es una interfaz de conversación. El operador no compone consultas ni conversa con [[service-slm|el modelo de lenguaje]] — no hay ningún modelo en este circuito. La superficie es una secuencia fija: una ruta, una confirmación de sí/no y un envío.

F12 no es una superficie de autoguardado. Un archivo ingresa al libro mayor solo cuando el operador presiona Y explícitamente en la solicitud de confirmación. Cancelar en cualquier punto antes de eso no deja nada registrado.

F12 no es una interfaz de importación masiva. El operador puede tener varios archivos que procesar, pero cada uno pasa por la secuencia completa de ruta→confirmar→enviar individualmente, produciendo su propio registro de auditoría. La restricción de un archivo a la vez no es una limitación de rendimiento — es una disciplina de auditoría. [[architecture-decisions|SYS-ADR-10]] es inequívoco en este punto: el límite F12 es obligatorio por archivo.

## Véase también

- [[architecture-decisions|SYS-ADR-07]] — la decisión arquitectónica que exige verificación humana antes de que los datos estructurados ingresen a un libro mayor verificado
- [[architecture-decisions|SYS-ADR-10]] — la decisión arquitectónica que establece F12 como la puerta de entrada obligatoria
- [[architecture-decisions|SYS-ADR-19]] — la decisión arquitectónica que prohíbe la publicación automatizada en libros mayores verificados
- [[os-console|os-console]] — el sistema operativo que aloja la superficie F12
- [[worm-ledger-design]] — los principios de diseño detrás del sustrato del libro mayor WORM
- [[machine-based-auth]] — la capa de autenticación que vincula las entradas del libro mayor con la identidad verificada del operador
