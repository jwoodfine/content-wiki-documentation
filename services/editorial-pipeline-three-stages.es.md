---
schema: foundry-doc-v1
title: "El contrato de la canalización de corrección"
slug: editorial-pipeline-three-stages
aliases:
  - editorial-pipeline-three-stages
short_description: "El contrato real, confirmado del lado cliente, de la canalización de corrección de la plataforma: un conjunto fijo de protocolos de idioma, una respuesta que informa qué nivel de cómputo se ejecutó y qué se degradó, y un veredicto humano binario que alimenta el corpus de entrenamiento."
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: editorial-pipeline-three-stages.md
---

La [[radical-proofreader-ui|consola de corrección]] — el cartucho de contenido F4 en `app-console-content` — envía texto para revisión editorial y recibe de vuelta una reescritura. Lo que sigue describe solo lo confirmado por los tipos de solicitud y respuesta del propio cliente: el vocabulario de protocolos de idioma, la forma de una respuesta de corrección y el paso de veredicto que cierra el ciclo.

## La selección de protocolo es una lista fija y real

Cada envío nombra un `protocol` de un conjunto fijo de nueve, con `prose-topic` como valor predeterminado:

| Protocolo | Género |
|---|---|
| `prose-architecture` | Documentación de arquitectura |
| `prose-guide` | Manual operativo |
| `prose-memo` | Memorando |
| `prose-readme` | README |
| `prose-topic` | TOPIC de wiki de contenido (predeterminado) |
| `comms-chat` | Mensaje de chat |
| `comms-email` | Correo electrónico |
| `comms-ticket-comment` | Comentario de ticket |
| `translate-en-es` | Traducción de inglés a español |

La solicitud también lleva un `tenant`, que limita el envío a la propia organización del emisor.

## La respuesta informa qué se ejecutó realmente

Una respuesta exitosa lleva `improved_text` (la reescritura) junto con campos que describen cómo se produjo. `tier_used` nombra qué nivel de cómputo atendió la solicitud. `degraded` lista cualquier cosa que no se ejecutó a plena capacidad — evidencia real de que la canalización tiene más de un componente interno capaz de fallar de forma independiente, aunque este contrato no nombra esos componentes ni su orden. `audit_ledger_id` referencia el rastro de auditoría, y `request_id` se usa para registrar el veredicto después. Un llamador puede saber, solo con la respuesta, si la canalización completa se ejecutó o si algo se degradó en el camino, sin necesitar llamadas de estado separadas.

## El veredicto es binario, y entrena al modelo

Tras revisar la reescritura, el operador envía un veredicto vinculado al `request_id` original. El veredicto es binario — aceptar o rechazar — y se firma con SSH de la misma forma que los demás puntos de control de revisión humana de la plataforma: la firma de un revisor se verifica contra el archivo `allowed_signers` del espacio de trabajo antes de registrar el veredicto. Un veredicto aceptado marca la reescritura como ejemplo positivo de entrenamiento; uno rechazado conserva el original. Es el mismo mecanismo de veredicto de tipo aprendizaje supervisado que se usa en otras partes de la plataforma — una decisión humana convertida directamente en señal de entrenamiento, nunca una aceptación automática.

## Véase también

- [[radical-proofreader-ui]] — la consola de terminal que envía texto a través de esta canalización
- [[language-protocol-substrate]] — las definiciones de familias de género de las que proviene la lista de protocolos
- [[customer-tier-catalog-pattern]] — el modelo de implementación para una instancia de la canalización de corrección
