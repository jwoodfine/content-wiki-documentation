---
schema: foundry-doc-v1
title: "app-console-input"
slug: app-console-input
category: applications
type: app
quality: complete
short_description: "app-console-input es la superficie F12 en os-console — la puerta de entrada estructurada a través de la cual los archivos externos sin procesar ingresan a un Totebox antes de sellarse en el libro mayor verificado."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: app-console-input.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
 - id: 1
 text: "NIST, Marco de Gestión de Riesgos de Inteligencia Artificial (AI RMF 1.0), NIST AI 100-1, enero de 2023. Sección 5: Supervisión humana y responsabilidad en implementaciones de IA."
 url: "https://doi.org/10.6028/NIST.AI.100-1"
 - id: 2
 text: "Organización Internacional de Normalización, ISO/IEC 27001:2022 — Sistemas de gestión de la seguridad de la información, Anexo A.8.15: Registro."
 url: "https://www.iso.org/standard/82875.html"
---

`app-console-input` es la superficie F12 en [[console-os|os-console]] — el único camino a través del cual los archivos externos sin procesar ingresan a un [[totebox-os|Totebox]] antes de sellarse en el [[worm-ledger-design|libro mayor WORM]]. La superficie conduce cada documento entrante a través de un paso de verificación humana estructurado, responsabilizando al operador por cada afirmación [[service-extraction|extraída]] antes de que avance al estado verificado. A diferencia de una interfaz de [[service-slm|modelo de lenguaje]] o una canalización de autoguardado, presenta opciones binarias — el sistema propone, el operador confirma o rechaza — de modo que cada decisión fiduciaria lleva la firma del operador en el [[worm-ledger-design|registro de auditoría]]. Al finalizar este artículo, el lector comprenderá el flujo de trabajo F12, el patrón Agrimensor de Verificación y las propiedades de auditoría que protege esta puerta.

## Cómo se desarrolla una sesión F12

Una sesión F12 típica tiene una forma determinista de cinco pasos. Cada paso tiene un límite claro; el operador no salta hacia adelante ni agrupa decisiones.

| Paso | Acción del operador | Respuesta del sistema |
|---|---|---|
| 1 | Arrastrar un archivo desde el escritorio a la ventana F12 | El sistema calcula un hash del contenido y elimina los permisos de ejecución |
| 2 | Seleccionar una categoría del [[archetypes-and-chart-of-accounts|Plan de Cuentas]] (Perfil → Dominio → Subdominio) | El sistema prepara un destino de enrutamiento |
| 3 | Revisar las entidades y temas que el sistema preextrajo mediante [[service-extraction]] y [[service-content]] | El sistema muestra una solicitud de verificación Sí / No para cada afirmación |
| 4 | Aprobar o rechazar cada afirmación con teclas individuales | Las afirmaciones aprobadas avanzan al estado L5 verificado; las rechazadas quedan en cuarentena |
| 5 | Confirmar el destino de enrutamiento | El archivo se sella en service-minutebook o service-bookkeeper; se escribe una entrada en el libro mayor; el [[worm-ledger-design|registro de auditoría]] captura la identidad del operador, la marca de tiempo y la decisión de enrutamiento |

La interacción es solo con teclado y deliberadamente rápida. El operador no escribe nombres de archivo, completa formularios de metadatos ni compone consultas de base de datos. [[service-extraction]] y [[service-content]] ya realizaron el trabajo computacional; el papel del operador es verificar o rechazar cada afirmación en secuencia y luego confirmar el destino.

Esta estructura secuencial es deliberada. Agrupar varios pasos en una única confirmación reduciría la resolución del [[worm-ledger-design|registro de auditoría]] — cada afirmación heredaría la misma marca de tiempo en lugar de llevar su propio registro de decisión. La puerta de cinco pasos preserva la granularidad de auditoría por afirmación.

## El patrón Agrimensor de Verificación — opciones binarias frente a formularios abiertos

El modelo de interacción F12 se describe a veces como el Agrimensor de Verificación: en lugar de presentar al operador un formulario en blanco, el sistema presenta una opción binaria — "Extraje este dato; ¿es correcto? Sí o No." [^1]

El patrón tiene tres propiedades:

| Propiedad | Efecto |
|---|---|
| Baja carga cognitiva | El operador procesa una secuencia de decisiones de Sí/No en lugar de crear datos estructurados |
| Claridad fiduciaria | Cada afirmación que ingresa al libro mayor verificado lleva una decisión explícita del operador, no un valor predeterminado del sistema |
| Integridad del registro de auditoría | El [[worm-ledger-design|registro de auditoría]] captura la decisión exacta sobre cada afirmación, no solo el destino final de enrutamiento |

Este modelo refleja un límite deliberado entre la plataforma y el operador. [[service-extraction]] y [[service-content]] gestionan la detección de entidades, la clasificación temática y la sugerencia de enrutamiento. El operador gestiona la puerta binaria. Las instituciones sujetas a obligaciones de divulgación continua [ni-51-102] [osc-sn-51-721] y estándares de registros electrónicos [^2] pueden señalar una decisión específica del operador con marca de tiempo para cada documento que ingresa al libro mayor verificado.

El patrón difiere del autocompletado asistido por IA, donde un modelo completa los campos y el operador acepta por omisión. En F12, el silencio nunca es aceptación. Cada afirmación que avanza al estado verificado requiere una pulsación de tecla afirmativa explícita del operador.

## Por qué el paso de verificación es arquitectónicamente obligatorio

Si [[service-extraction]] o [[service-content]] enrutaran un documento fuente a la cuenta incorrecta sin confirmación humana, el libro mayor verificado llevaría una entrada matemáticamente comprometida desde ese punto en adelante. Reclasificar el documento más tarde no repara el registro de auditoría — la entrada original ya lleva una marca de tiempo de verificación que registra una decisión que ningún ser humano tomó.

[[architecture-decisions|SYS-ADR-10]] hace que F12 sea obligatorio precisamente porque este modo de fallo es estructural, no probabilístico: cualquier arquitectura que delegue la decisión final de enrutamiento a un sistema automatizado crea una entrada en el libro mayor sin un autor humano responsable. [[architecture-decisions|SYS-ADR-07]] extiende el principio a los datos estructurados de manera más amplia — ningún registro producido por IA ingresa a un libro mayor verificado sin un paso de confirmación humana. [[architecture-decisions|SYS-ADR-19]] cierra el camino restante — sin publicación automatizada en libros mayores verificados, independientemente de la puntuación de confianza.

Los fiduciarios institucionales — gestores de activos, abogados, entidades financieras reguladas — requieren un registro de auditoría que puedan defender bajo escrutinio. La puerta F12 es lo que hace posible esa defensa: cada entrada en service-minutebook y service-bookkeeper se remonta a un operador específico, una decisión específica y una marca de tiempo específica. [^2]

## Lo que la superficie F12 no es

F12 no es una interfaz de conversación. El operador no compone consultas ni conversa con [[service-slm|el modelo de lenguaje]]. La superficie es estructurada: un archivo, una selección del [[archetypes-and-chart-of-accounts|Plan de Cuentas]], una secuencia de solicitudes binarias y una confirmación. Todo el trabajo del modelo de lenguaje ocurre en sentido ascendente en [[service-extraction]] y [[service-content]] antes de que comience la sesión F12; el operador nunca ve la salida bruta del modelo.

F12 no es una superficie de autoguardado. Un documento ingresa al [[worm-ledger-design|libro mayor WORM]] solo cuando el operador confirma explícitamente el destino de enrutamiento. Esto protege el registro de auditoría de escrituras parciales y sesiones abandonadas. Los borradores en progreso no se acumulan en el libro mayor; un documento solo se registra cuando el operador llega al paso cinco y confirma.

F12 no es una interfaz de importación masiva. El operador puede tener una cola de documentos para procesar, pero cada uno pasa por la puerta de cinco pasos individualmente, produciendo un registro de auditoría distinto por documento. La restricción secuencial no es una limitación de rendimiento — es una disciplina de auditoría. [[architecture-decisions|SYS-ADR-10]] es inequívoco en este punto: el límite F12 es obligatorio por documento.

## Véase también

- [[architecture-decisions|SYS-ADR-07]] — la decisión arquitectónica que exige verificación humana antes de que los datos estructurados ingresen a un libro mayor verificado
- [[architecture-decisions|SYS-ADR-10]] — la decisión arquitectónica que establece F12 como la puerta de entrada obligatoria
- [[architecture-decisions|SYS-ADR-19]] — la decisión arquitectónica que prohíbe la publicación automatizada en libros mayores verificados
- [[console-os|os-console]] — el sistema operativo que aloja la superficie F12
- [[service-extraction]] — el motor de extracción de entidades y temas en sentido ascendente
- [[service-content]] — el motor de clasificación y enrutamiento en sentido ascendente
- [[worm-ledger-design]] — los principios de diseño detrás del sustrato del libro mayor WORM
- [[machine-based-auth]] — la capa de autenticación que vincula las entradas del libro mayor con la identidad verificada del operador
