---
schema: foundry-doc-v1
title: "Disciplina de límite para claves de API"
slug: api-key-boundary-discipline
category: governance
type: topic
content_type: topic
quality: complete
index_group: platform-disciplines
short_description: La regla que establece que todas las credenciales externas de LLM pertenecen exclusivamente al servicio de pasarela y nunca a los motores de inferencia.
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: api-key-boundary-discipline.md
---

La disciplina de límite para claves de API establece una regla fundamental en el diseño de plataformas de inteligencia artificial: las credenciales de proveedores externos pertenecen exclusivamente al servicio de pasarela ([[doorman-protocol|Doorman]]), nunca a los motores de inferencia. Esta disciplina aplica a todos los niveles de implementación, desde appliances autohospedados hasta trabajadores de cómputo en la nube.

## Principio central

Cualquier proceso que ejecute inferencia de modelos — sea local en hardware del cliente, en trabajadores de ráfaga en nube, o en cualquier nodo de cómputo futuro — no debe leer ni almacenar credenciales de proveedores externos de LLM. Las credenciales fluyen únicamente entre el Doorman y el endpoint del proveedor. No existen excepciones.

## Por qué importa

Tres propiedades estructurales justifican la regla:

**Completitud de auditoría.** Toda llamada a la API pasa por el punto límite de la pasarela. Un [[worm-ledger-design|ledger de auditoría]] por tenant puede capturar proveedor, propósito, volumen de tokens y costo en un único punto de control. Las rutas alternativas que evitan la pasarela generan gasto que no puede atribuirse ni auditarse.

**Aplicación de listas de permitidos.** Restringir las llamadas de inferencia a un conjunto definido de propósitos requiere un único punto de aplicación. Una pasarela que recibe todas las solicitudes puede aplicar la lista de permitidos; los motores de inferencia distribuidos entre múltiples nodos de cómputo no pueden.

**Escalado sin estado.** Los procesos de inferencia que no almacenan secretos pueden iniciarse, detenerse y reemplazarse sin rotación de credenciales.

## Ubicación de las claves por nivel

La disciplina se aplica de manera consistente en cada forma de despliegue:

**[[totebox-os|Totebox]] autohospedado (despliegue del cliente).** El [[doorman-protocol|Portero]] local del cliente conserva las claves externas de LLM y, opcionalmente, una clave de suscripción para los niveles de modelo alojados en la nube. El motor de inferencia local no conserva nada. Las claves del cliente nunca viajan hacia el proveedor.

**Trabajadores de ráfaga en la nube.** Cuando una solicitud se enruta hacia un trabajador de GPU en la infraestructura de un proveedor de nube, ese trabajador no conserva credenciales externas de API. La autenticación entre el nivel de ráfaga en la nube y cualquier proveedor externo la gestiona la pasarela que despachó la solicitud.

**Pasarela del proveedor (despliegues del lado del proveedor).** El Portero del proveedor conserva las credenciales del lado del proveedor. El proveedor nunca conserva, almacena ni accede a las claves externas de LLM propiedad del cliente. Las contribuciones federadas al mercado intercambian adaptadores, no credenciales.

## Patrones prohibidos

- Un proceso de inferencia que lee claves desde variables de entorno, aunque no realice llamadas externas en ese momento.
- Un proceso de inferencia que obtiene claves de un gestor de secretos al arrancar.
- Scripts ad hoc que leen claves de API desde cualquier fuente distinta a la pasarela.
- Almacenamiento del lado del proveedor de claves externas de LLM propiedad del cliente.

## Relación con las credenciales de identidad

Las claves de API para proveedores de LLM son credenciales de tiempo de ejecución — cambian con la rotación, pertenecen al Portero, y nunca se incrustan en el código. Son distintas de las claves de firma de identidad, que son credenciales de autoría usadas en el momento del commit. Las dos clases de credencial tienen ubicaciones de almacenamiento y reglas de ciclo de vida separadas; ninguna cruza el límite de la otra.

## Cumplimiento

La combinación de límite de pasarela, ledger de auditoría por tenant y lista de propósitos permitidos produce un rastro de auditoría criptográfico sobre cada llamada de inferencia externa por construcción, no mediante un proceso de cumplimiento aparte. Esta estructura está diseñada para respaldar los requisitos de integridad de procesamiento de SOC 2 y los principios de cadena de custodia de ISAE 3402; ninguna certificación SOC 2 ni ISAE 3402 existe todavía — véase [[compliance-and-continuous-disclosure]] para el estado actual de certificación.

## Véase también

- [[compounding-substrate]]
- [[design-system-substrate]]
