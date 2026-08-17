---
schema: foundry-doc-v1
title: "Protocolo Doorman"
slug: doorman-protocol
short_description: "Doorman es el único límite de solicitud de IA a través del cual se enruta toda llamada de inferencia — imponiendo la disciplina de sanitizar-y-rehidratar una sola vez, registrando cada llamada en un libro mayor de auditoría inmutable y capturando la señal de entrenamiento que compone la plataforma con el tiempo."
category: ai
type: concept
content_type: topic
index_group: the-doorman-boundary
status: active
bcsc_class: current-fact
forward_looking: true
last_edited: 2026-08-17
editor: pointsav-engineering
language: es
paired_with: doorman-protocol.md
cites: []

---

Cada servicio que puede llamar a un modelo de IA externo es su propio agujero en el muro. Diez servicios con diez rutas de salida significan diez superficies de auditoría, y diez lugares donde la disciplina de saneamiento puede olvidarse.

El Doorman reduce el muro a una sola puerta. [[service-slm|`service-slm`]] es el único límite de solicitud de IA de la plataforma; toda llamada de inferencia se enruta por una sola puerta de control de acceso, y ninguna llamada sale de la bóveda de datos del cliente sin atravesarla.

En ese único límite, el Doorman aplica la disciplina de sanitizar-y-rehidratar, enruta la llamada al nivel de cómputo apropiado, registra cada evento en un libro mayor de auditoría inmutable y captura la señal de entrenamiento que compone la plataforma con el tiempo.

Para un comprador regulado la consecuencia es concreta. Ninguna llamada de inferencia sale de la bóveda de datos sin registrar ni sanear, porque la disciplina es una garantía estructural y no una configuración por servicio. Este artículo define las reglas de enrutamiento, el esquema de auditoría, la disciplina de `moduleId` y la captura de señal de entrenamiento.

## Por qué un Doorman

La bóveda de datos del cliente contiene sus datos estructurados autorizados, y el cómputo externo — los grandes modelos de lenguaje — no puede recibir esos datos en bruto. Sin un único límite, cada servicio del [[totebox-os|Totebox]] desarrolla su propia ruta de salida, cada ruta necesita su propia auditoría, y la disciplina de sanitizar-y-rehidratar (SYS-ADR-07) se convierte en disciplina por servicio en lugar de disciplina de sustrato. El Doorman centraliza el límite para que la disciplina se aplique una sola vez.

## Enrutamiento de cómputo en tres niveles

El Doorman enruta las llamadas de inferencia en tres niveles. Los tres están implementados en el código de enrutamiento — "planificado" describe el estado de activación, no código que aún no existe.

**Nivel A — local.** Se ejecuta en la VM del servidor usando CPU y RAM, para inferencia rápida, de baja latencia y bajo costo sobre un modelo alojado localmente. El Nivel A gestiona la mayor parte del volumen de enrutamiento sin gasto en la nube, y está verificado operativamente.

**Nivel B — grupo de GPU por demanda.** El Nivel B enruta cargas de trabajo a instancias GPU efímeras ([[yoyo-compute-substrate|el sustrato de cómputo Yo-Yo]]), iniciadas bajo demanda y detenidas en reposo (un monitor de apagado por inactividad, con un valor predeterminado de 30 minutos, emite la llamada real de desaprovisionamiento), con dos perfiles: una instancia de **entrenamiento** para ciclos continuos sobre tuplas acumuladas, y una instancia de **grafo** para cargas de trabajo del grafo de propiedades — no una instancia de "extracción" como describía la documentación anterior. La lógica de enrutamiento y el monitor de apagado por inactividad están completamente implementados; que un perfil determinado esté accesible en un momento dado depende de su propia verificación de salud y del estado de su interruptor de circuito, que el punto de conexión `/readyz` del Doorman reporta por perfil.

**Nivel C — proxy de API externa.** La lista de permitidos y el andamiaje de límites de costo del Nivel C están implementados para tareas de precisión limitada — fundamentación de citas, asistencia en la construcción del grafo, desambiguación de entidades — pero los comentarios del propio código fuente indican que las llamadas en vivo a API externas aún no están habilitadas en esta versión; activarlas es una decisión operativa separada, no una función faltante. La documentación anterior afirmaba que el Nivel C "inyecta ontologías de `service-content` predefinidas para restringir la salida al vocabulario canónico de la plataforma" — no existe tal mecanismo en la ruta de código del Nivel C; esa afirmación se retracta aquí, no simplemente se suaviza.

## El libro de auditoría

Cada llamada de inferencia produce una entrada JSONL anexada a un archivo diario. Campos: marca de tiempo, ID de solicitud, ID de módulo, nivel, modelo, duración de inferencia, estimación de costo, indicador de saneamiento de salida, estado de finalización, tipo de entrada y, cuando corresponde, un mensaje de error y un nombre de archivo. Cada entrada también lleva un hash calculado al momento de la escritura para la detección de manipulaciones. El libro es de solo adición; ninguna entrada se modifica ni se borra tras la escritura.

## La disciplina de moduleId

Se confirma que `moduleId` cumple dos funciones, no cinco. Etiqueta las entradas del libro de auditoría para la contabilidad de costos por proyecto y — desde que se implementó la corrección de aislamiento de inquilinos — circunscribe estrictamente las lecturas y escrituras del grafo de propiedades al módulo del solicitante, sin fusión entre inquilinos.

La documentación anterior afirmaba además que `moduleId` selecciona la unidad systemd que gestiona la solicitud, delimita la caché clave-valor y selecciona la pila de adaptadores. Ninguna de esas tres funciones tiene respaldo en el código actual de enrutamiento, caché o centro de adaptadores, así que la afirmación se retracta aquí en lugar de mantenerse sin verificar.

La aplicación es real pero más limitada que "toda solicitud necesita un `moduleId` válido": los puntos de conexión del grafo (`graph_query`, `graph_mutate`) rechazan un `moduleId` ausente o mal formado directamente. El punto de conexión de inferencia principal (`chat_completions`) rechaza un `moduleId` mal formado, pero recurre silenciosamente a un valor predeterminado cuando el encabezado simplemente está ausente, registrando solo una advertencia — una brecha real entre las dos familias de puntos de conexión, no un límite uniforme.

## Enrutamiento de la tubería de aprendizaje

El Doorman implementa la inversión de enrutamiento del [[apprenticeship-substrate]] para el trabajo con forma de código y editorial: `service-slm` intenta primero, y la sesión sénior revisa. Cada veredicto firmado — `Accept`, `Refine`, `Reject`, `DeferTierC` — se captura en el corpus de aprendizaje como una tupla de entrenamiento.

La lógica de enrutamiento del Doorman y el libro de promoción del sustrato de aprendizaje son dos superficies del mismo mecanismo.

## Véase también

- [[compounding-doorman]] — descripción conceptual del Doorman como patrón de sustrato de IA soberana
- [[apprenticeship-substrate]] — la inversión de enrutamiento y el protocolo de firma de veredictos
- [[three-ring-architecture]] — el Doorman es el único servicio del Anillo 3
- [[service-slm]] — el crate service-slm que implementa el Doorman
- [[configure-doorman]] — guía paso a paso: configurar las direcciones de nivel, los umbrales del interruptor de circuito y verificar el punto de conexión de salud
- [[run-first-slm-query]] — guía paso a paso: enviar un prompt de inferencia y leer el panel de salud del Doorman
