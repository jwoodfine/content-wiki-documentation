---
schema: foundry-doc-v1
title: "Protocolo Doorman"
slug: doorman-protocol
short_description: "Doorman es el único límite de solicitud de IA a través del cual se enruta toda llamada de inferencia — imponiendo la disciplina de sanitizar-y-rehidratar una sola vez, registrando cada llamada en un libro mayor de auditoría inmutable y capturando la señal de entrenamiento que compone la plataforma con el tiempo."
category: architecture
type: concept
status: active
bcsc_class: current-fact
forward_looking: true
last_edited: 2026-05-22
editor: pointsav-engineering
language: es
paired_with: doorman-protocol.md
cites: []
---

Cada servicio que puede llamar a un modelo de IA externo es su propio agujero en el muro. Diez servicios con diez rutas de salida significan diez superficies de auditoría, y diez lugares donde la disciplina de saneamiento puede olvidarse.

El Doorman reduce el muro a una sola puerta. <!--claim id=sole-boundary confidence=structural cites=[]-->[[service-slm|`service-slm`]] es el único límite de solicitud de IA de la plataforma; toda llamada de inferencia se enruta por una sola puerta de control de acceso, y ninguna llamada sale de la bóveda de datos del cliente sin atravesarla.<!--/claim-->

<!--claim id=doorman-functions confidence=structural cites=[]-->En ese único límite, el Doorman aplica la disciplina de sanitizar-y-rehidratar, enruta la llamada al nivel de cómputo apropiado, registra cada evento en un libro mayor de auditoría inmutable y captura la señal de entrenamiento que compone la plataforma con el tiempo.<!--/claim-->

Para un comprador regulado la consecuencia es concreta. Ninguna llamada de inferencia sale de la bóveda de datos sin registrar ni sanear, porque la disciplina es una garantía estructural y no una configuración por servicio. Este artículo define las reglas de enrutamiento, el esquema de auditoría, la disciplina de `moduleId` y la captura de señal de entrenamiento.

## Por qué un Doorman

La bóveda de datos del cliente contiene sus datos estructurados autorizados, y el cómputo externo — los grandes modelos de lenguaje — no puede recibir esos datos en bruto. <!--claim id=centralised-discipline confidence=structural cites=[]-->Sin un único límite, cada servicio del [[totebox-os|Totebox]] desarrolla su propia ruta de salida, cada ruta necesita su propia auditoría, y la disciplina de sanitizar-y-rehidratar (SYS-ADR-07) se convierte en disciplina por servicio en lugar de disciplina de sustrato.<!--/claim--> El Doorman centraliza el límite para que la disciplina se aplique una sola vez.

## Enrutamiento de cómputo en tres niveles

El Doorman enruta las llamadas de inferencia en tres niveles.

**Nivel A — local.** Se ejecuta en la VM del servidor usando CPU y RAM, para inferencia rápida, de baja latencia y bajo costo sobre un modelo alojado localmente. <!--claim id=tier-a-verified confidence=structural cites=[]-->El Nivel A gestiona la mayor parte del volumen de enrutamiento sin gasto en la nube, y está verificado operativamente.<!--/claim-->

**Nivel B — grupo de GPU por demanda.** <!--claim id=tier-b-planned confidence=projected cites=[] valid_at=2026-->El Nivel B está planificado para enrutar cargas de trabajo a instancias GPU efímeras ([[yoyo-compute-substrate|el sustrato de cómputo Yo-Yo]]), iniciadas bajo demanda y detenidas en reposo, con dos perfiles: una instancia de entrenamiento para ciclos continuos sobre tuplas acumuladas, y una instancia de extracción para la ingesta de corpus a gran escala.<!--/claim--> Ambos perfiles usan temporizadores de apagado por inactividad para que la facturación se detenga cuando la cola está vacía.

**Nivel C — proxy de API externa.** El Nivel C está planificado para enrutar tareas especializadas de refinamiento lingüístico y formato a modelos de frontera externos. El Doorman aplica límites de costo e inyecta ontologías de [[service-content|`service-content`]] predefinidas para restringir la salida al vocabulario canónico de la plataforma.

## El libro de auditoría

<!--claim id=audit-ledger confidence=structural cites=[]-->Cada llamada de inferencia produce una entrada JSONL anexada a un archivo diario. Los campos requeridos son marca de tiempo, ID de solicitud, ID de módulo, nivel, modelo, duración de inferencia, estimación de costo, indicador de saneamiento de salida y estado de finalización. El libro es de solo adición; ninguna entrada se modifica ni se borra tras la escritura.<!--/claim-->

## La disciplina de moduleId

<!--claim id=moduleid-five-roles confidence=structural cites=[]-->Un único campo `moduleId` cumple cinco funciones a la vez. Selecciona la unidad systemd que gestiona la solicitud, delimita los bloques de caché clave-valor y circunscribe los recorridos de la base de datos de grafo de propiedades al inquilino correcto. También selecciona la pila de adaptadores y etiqueta las entradas del libro de auditoría para la contabilidad de costos por proyecto. Una solicitud sin un `moduleId` válido se rechaza en el límite del Doorman.<!--/claim-->

## Enrutamiento de la tubería de aprendizaje

<!--claim id=learning-routing confidence=structural cites=[]-->El Doorman implementa la inversión de enrutamiento del [[apprenticeship-substrate]] para el trabajo con forma de código y editorial: `service-slm` intenta primero, y la sesión sénior revisa. Cada veredicto firmado — `Accept`, `Refine`, `Reject`, `DeferTierC` — se captura en el corpus de aprendizaje como una tupla de entrenamiento.<!--/claim-->

La lógica de enrutamiento del Doorman y el libro de promoción del sustrato de aprendizaje son dos superficies del mismo mecanismo.

## Véase también

- [[compounding-doorman]] — descripción conceptual del Doorman como patrón de sustrato de IA soberana
- [[apprenticeship-substrate]] — la inversión de enrutamiento y el protocolo de firma de veredictos
- [[three-ring-architecture]] — el Doorman es el único servicio del Anillo 3
- [[service-slm]] — el crate service-slm que implementa el Doorman
