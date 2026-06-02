---
schema: foundry-doc-v1
title: "El sustrato SLM por niveles — enrutamiento de IA con prioridad local"
slug: slm-tiered-substrate
short_description: "Cómo la plataforma enruta las solicitudes de modelos de lenguaje a través de tres niveles de cómputo — CPU local, GPU en ráfaga y API externa — manteniendo el trabajo rutinario en hardware bajo control del operador y los registros estructurados dentro del perímetro del operador."
category: substrate
type: topic
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: slm-tiered-substrate.md
---

# El sustrato SLM por niveles — enrutamiento de IA con prioridad local

La plataforma enruta el trabajo con modelos de lenguaje a través de una única puerta de enlace que decide, por solicitud, qué nivel de cómputo debe responder. El objetivo de diseño es mantener el trabajo rutinario en hardware que el operador ya posee, recurrir a GPU arrendada sólo cuando una tarea realmente lo requiere, y nunca dejar que los datos estructurados del negocio crucen el perímetro de la IA. Este artículo describe los niveles, cómo se enruta una solicitud y cómo la puerta de enlace restringe la salida del modelo a la forma requerida.

## Los niveles

El sustrato distingue tres niveles de inferencia, cada uno adaptado a una clase de trabajo diferente.

*Nivel A — el modelo local.* Un modelo pequeño (actualmente OLMo 2 7B, cuantizado a 4 bits) se ejecuta en la propia máquina del operador y responde de inmediato para trabajo interactivo: navegación de código, redacción breve, preguntas rápidas. Siempre está disponible y no tiene coste por solicitud. Es el *estudiante* del bucle de aprendizaje, no el generador de datos de entrenamiento — una distinción importante porque un modelo pequeño al que se le pide que evalúe su propio trabajo produce señal útil limitada.

*Nivel B — el modelo GPU en ráfaga.* Un modelo de razonamiento mayor (OLMo 3 32B-Think) se ejecuta en una GPU en la nube con capacidad apropiable, iniciada bajo demanda y detenida cuando está inactiva. Gestiona el trabajo pesado y estructurado — extracción de entidades para el grafo de conocimiento y la generación de datos de entrenamiento que mejora el Nivel A. Dado que la GPU se arrienda por minuto, la puerta de enlace la activa sólo cuando hay trabajo por lotes pendiente y un interruptor automático la detiene al finalizar.

*Nivel C — la API externa.* Un modelo comercial, deliberadamente no configurado. Existe en el diseño como opción de resiliencia pero no está habilitado, porque el valor del sustrato reside en que el trabajo permanece en cómputo bajo control del operador.

## Cómo se enruta una solicitud

Cada solicitud lleva un indicador de complejidad y una preferencia de nivel opcional. La postura predeterminada de la puerta de enlace es *prioridad local*: el modelo local principal responde con confianza a menos que el caller solicite explícitamente el nivel de ráfaga y el chequeo de salud de ese nivel esté pasando. Un disyuntor de circuito rastrea la disponibilidad del nivel de ráfaga — cuando la GPU está caída, el disyuntor se abre y el trabajo dependiente *aplaza* en lugar de fallar, de modo que una escasez de capacidad o una VM detenida nunca produce un error, sólo un "inténtelo más tarde" que el caller reintenta con retroceso exponencial.

Una regla de enrutamiento es absoluta: la extracción de entidades va sólo al nivel de ráfaga. El modelo local pequeño no puede producir de forma fiable arrays JSON estructurados, por lo que nunca se usa como alternativa para la extracción. Cuando la GPU no está disponible, la extracción simplemente espera.

## El perímetro de datos estructurados

Una regla arquitectónica estricta ([[sys-adr-07|SYS-ADR-07]]) rige lo que puede cruzar el perímetro de la IA: la prosa puede salir como indicación; los registros estructurados del negocio no pueden. La extracción de entidades ilustra la disciplina. El texto a analizar es prosa. El *esquema* que describe la salida deseada se envía como restricción, no como dato. El modelo devuelve un array estructurado que la puerta de enlace analiza y escribe en el grafo — pero ningún registro estructurado existente fue expuesto al modelo. El perímetro es unidireccional por diseño.

## Restricción de la salida a una forma requerida

Para que la extracción sea utilizable, la salida del modelo debe coincidir exactamente con una forma JSON conocida. La puerta de enlace consigue esto enviando el esquema de salida como una *restricción de gramática* junto con la indicación, de modo que el servidor de inferencia se ve obligado a emitir sólo tokens conformes. En pruebas en vivo esto convierte una solicitud que de otro modo se explayaría en prosa en un resultado compacto y analizable: una breve frase comercial devolvió cuatro entidades correctamente clasificadas — empresa, ubicación, ubicación, persona — en aproximadamente siete segundos.

*Nota de ingeniería — la restricción es específica del motor, y eso es un riesgo de mantenimiento.* El mecanismo para solicitar una restricción de gramática difiere entre motores de inferencia. Una familia de servidores lee la restricción de un sobre de solicitud anidado; otra la lee de campos de solicitud de nivel superior e ignora silenciosamente el sobre. Cuando el nivel de ráfaga del sustrato migró del primer motor al segundo, una ruta de cliente se actualizó y otra no — de modo que durante un período el esquema se enviaba de una forma que el servidor en ejecución ignoraba, y el modelo generaba prosa sin restricciones que no podía analizarse. La lección es duradera: cuando una restricción de salida estructurada "no funciona", confirme empíricamente qué campo de solicitud honra realmente el motor *desplegado* antes de cambiar cualquier otra cosa, porque el fallo es silencioso — el servidor devuelve una respuesta válida que simplemente ignora la restricción.

## El perímetro entre interactivo y por lotes

Una segunda lección duradera: un modelo de razonamiento es la herramienta equivocada para una tarea estructurada y mecánica. El modelo de razonamiento de 32B gasta un gran presupuesto de tokens "pensando" antes de responder, lo cual es valioso para trabajo generativo difícil pero sobrecarga pura para extraer entidades nombradas según un esquema fijo. La intención de diseño del sustrato es, por tanto, reservar el razonamiento para la ruta generativa y ejecutar la ruta de extracción con el razonamiento suprimido — rápido, barato y determinista. El control del razonamiento por solicitud en la puerta de enlace es una capacidad planificada; hoy el presupuesto de razonamiento es una configuración a nivel del servidor para el servidor de inferencia del nivel de ráfaga.

## Supervivencia a una ráfaga interrumpida

La GPU en ráfaga funciona con capacidad apropiable: el proveedor de la nube puede reclamar la máquina en cualquier momento, a menudo con poco o ningún aviso previo. Un sustrato que perdiera o corrompiera trabajo cada vez que esto ocurriera sería inservible, por lo que el diseño trata la interrupción como un evento normal y no como un fallo.

Dos rutas transportan trabajo en curso, y ambas están construidas para fallar de forma cerrada. En el lado por lotes, cada unidad de trabajo se arrienda desde una cola duradera antes de enviarse a la GPU; si la máquina desaparece a mitad de una solicitud, el arrendamiento simplemente expira y un reparador devuelve la unidad a la cola, donde el siguiente trabajador la recoge. Nada se marca como completado hasta que el resultado está realmente disponible. En el lado de la extracción, el servicio que alimenta documentos a la puerta de enlace distingue una interrupción transitoria de un fallo genuino y permanente. Una solicitud cortada porque la GPU desapareció se trata como reintentable, no como documento procesado — por lo que nunca se descarta silenciosamente. Mientras la GPU no está disponible, los documentos pendientes se mantienen en estado durmiente en lugar de reintentarse en un bucle cerrado, lo que agotaría innecesariamente la puerta de enlace. Un único sondeo ligero se ejecuta en un intervalo fijo; en el momento en que tiene éxito, toda la cartera de trabajos durmientes se promueve de vuelta a la cola activa y la extracción se reanuda por sí sola, sin ninguna acción del operador ni reinicio del servicio.

El resultado es un flujo que se degrada con gracia: una ráfaga interrumpida cuesta algo de latencia mientras el sistema reacciona y cae hacia atrás, pero ningún documento se pierde, ningún registro queda a medio escribir, y la recuperación es automática cuando la capacidad vuelve.

## Por qué importa

El sustrato por niveles es lo que permite a un despliegue bajo control del operador comportarse como un servicio de IA gestionado sin ceder el control de sus datos ni de su cómputo. El trabajo rutinario es instantáneo y gratuito en hardware local; el trabajo pesado usa la GPU sólo cuando es necesario y se detiene solo; los registros estructurados nunca salen del perímetro del operador; y la salida del modelo está restringida a una forma en que el sistema puede confiar. La arquitectura es deliberadamente poco llamativa en operación — que es exactamente el objetivo para una infraestructura que se sitúa entre una bóveda de datos privada y un modelo externo.

## Véase también

- [[sys-adr-07]] — el registro de decisión arquitectónica que codifica el perímetro de datos estructurados
- [[service-slm]] — el servicio que implementa la puerta de enlace y la lógica del disyuntor de circuito
- [[service-content]] — el cliente de extracción que alimenta documentos a través de la puerta de enlace
