---
schema: foundry-doc-v1
title: "Protocolo Doorman"
slug: doorman-protocol
short_description: "Doorman es el único límite de solicitud de IA a través del cual se enruta toda llamada de inferencia — conserva cada credencial de modelo externo y registra cada llamada en un libro mayor de auditoría inmutable."
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

Cada servicio que puede llamar a un modelo de IA externo es su propio agujero en el muro. Diez servicios con diez rutas de salida significan diez superficies de auditoría, y diez lugares donde el manejo de credenciales y el registro pueden desincronizarse.

El Doorman reduce el muro a una sola puerta. [[service-slm|`service-slm`]] es el único límite de solicitud de IA de la plataforma; toda llamada de inferencia se enruta por una sola puerta de control de acceso, y ninguna llamada sale de la bóveda de datos del cliente sin atravesarla.

En ese único límite, el Doorman conserva cada credencial de modelo externo, enruta la llamada al nivel de cómputo apropiado, registra cada evento en un libro mayor de auditoría inmutable y captura la señal de entrenamiento que mejora la plataforma con el tiempo.

Para un comprador regulado la consecuencia es concreta. Ninguna llamada de inferencia sale de la bóveda de datos sin registrar ni con una credencial que el Doorman no controle, porque el límite es una garantía estructural y no una configuración por servicio. Este artículo define las reglas de enrutamiento, el esquema de auditoría, la disciplina de `moduleId` y la captura de señal de entrenamiento.

## Por qué un Doorman

La bóveda de datos del cliente contiene sus datos estructurados autorizados. Sin un único límite, cada servicio del [[totebox-os|Totebox]] desarrolla su propia ruta de salida, cada ruta necesita su propia auditoría, y la disciplina de credenciales y auditoría se vuelve por servicio en lugar de vigente en toda la plataforma. El Doorman centraliza el límite para que la disciplina se aplique una sola vez.

**Lo que el Doorman todavía no hace**: no depura información personal identificable ni datos de ubicación de un prompt antes de una llamada externa. El único código de saneamiento de la plataforma hoy redacta credenciales — claves de API, tokens, claves privadas — y se ejecuta únicamente en la ruta que escribe ejemplos de entrenamiento en el corpus de aprendizaje, nunca en la ruta hacia un modelo externo. Véase [[sovereign-ai-routing]] para el panorama completo de qué llega hoy al Nivel C y qué no.

## Enrutamiento de cómputo en tres niveles

El Doorman enruta las llamadas de inferencia en tres niveles.

**Nivel A — local.** Se ejecuta en la VM del servidor usando CPU y RAM, para inferencia rápida, de baja latencia y bajo costo sobre un modelo alojado localmente. El Nivel A gestiona la mayor parte del volumen de enrutamiento sin gasto en la nube.

**Nivel B — grupo de GPU por demanda.** El Nivel B enruta cargas de trabajo a instancias GPU efímeras ([[yoyo-compute-substrate|el sustrato de cómputo Yo-Yo]]), iniciadas bajo demanda y detenidas en reposo — una ventana de inactividad predeterminada de 30 minutos antes del desaprovisionamiento — con dos perfiles: una instancia de **entrenamiento** para ciclos continuos sobre tuplas acumuladas, y una instancia de **grafo** para cargas de trabajo del grafo de propiedades. Que un perfil determinado esté accesible en un momento dado depende de su propia verificación de salud y del estado de su interruptor de circuito, que el punto de estado del Doorman reporta por perfil.

**Nivel C — proxy de API externa.** La lista de permitidos y el andamiaje de límites de costo del Nivel C cubren tareas de precisión limitada — fundamentación de citas, asistencia en la construcción del grafo, desambiguación de entidades. Activar llamadas externas en vivo es una decisión operativa deliberada y separada, no una construcción en curso.

## El libro de auditoría

Cada llamada de inferencia produce una entrada JSONL anexada a un archivo diario. Campos: marca de tiempo, ID de solicitud, ID de módulo, nivel, modelo, duración de inferencia, estimación de costo, indicador de saneamiento de salida, estado de finalización, tipo de entrada y, cuando corresponde, un mensaje de error y un nombre de archivo. Cada entrada también lleva un hash calculado al momento de la escritura para la detección de manipulaciones. El libro es de solo adición; ninguna entrada se modifica ni se borra tras la escritura.

## La disciplina de moduleId

`moduleId` cumple dos funciones. Etiqueta las entradas del libro de auditoría para la contabilidad de costos por proyecto, y circunscribe estrictamente las lecturas y escrituras del grafo de propiedades al módulo del solicitante, sin fusión entre inquilinos.

La aplicación varía según el punto de conexión. Los puntos de conexión del grafo rechazan un `moduleId` ausente o mal formado directamente. El punto de conexión de inferencia principal rechaza un `moduleId` mal formado, pero recurre a un valor predeterminado cuando el encabezado simplemente está ausente, registrando solo una advertencia — una garantía más limitada en esa ruta que en los puntos de conexión del grafo.

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
