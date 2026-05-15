---
schema: foundry-doc-v1
title: "service-email — La Ingesta WORM"
slug: service-email
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-email.md
short_description: "service-email es el servidor de correo del Totebox — ingesta tráfico SMTP e IMAP, saneea cada carga útil y escribe texto en bruto en un Maildir de solo adición en almacenamiento local. La interpretación del contenido se maneja en sentido ascendente por service-content."
cites: []
---

`service-email` es el servidor de correo del Totebox. Escucha el tráfico SMTP e IMAP, saneea cada carga útil — eliminando la lógica de renderizado HTML y los píxeles de rastreo — y escribe el texto en bruto en un Maildir de solo adición en almacenamiento de bloque local. El servicio no interpreta el contenido; ese trabajo ocurre en sentido ascendente en `service-content`. Este artículo cubre el pipeline de ingesta, las propiedades Soberanas que lo distinguen de un cliente de correo convencional y su relación con el camino de integración de Microsoft 365.

## El pipeline de ingesta

El servicio opera en seis etapas, cada una con una propiedad Soberana específica:

| Etapa | Acción | Propiedad Soberana |
|---|---|---|
| Arranque | El binario Rust escanea el almacén de auditoría local y recupera trabajos pendientes | Auto-reparable — no se pierde trabajo entre reinicios |
| Autenticación | Actualización de token OAuth2 a través de Microsoft Entra (flujo de credenciales de cliente) | Inmunidad — sin autenticación heredada de usuario/contraseña |
| Sincronización | El bucle espejo IMAP escribe el correo verificado en el Maildir usando operaciones atómicas del sistema de archivos | Resiliencia — las escrituras atómicas evitan registros parciales |
| Limpieza | El agente de higiene aplica reglas TTL en la fuente en la nube mientras la copia del Maildir permanece permanente | Soberanía — la nube del proveedor no puede borrar retroactivamente el registro del operador |
| Renderizado | Cuando el operador redacta un correo electrónico con plantilla, el motor renderiza la carga útil HTML y la prepara para reenvío manual | Disciplina de intervención humana |
| Auditoría | El registrador de auditoría escribe entradas JSONL no bloqueantes que consumen los servicios posteriores | Ingesta independiente por `service-people` y el Motor de Gravedad |

## Integración con Microsoft 365

La configuración OAuth2 usa un registro de Cliente Confidencial en Microsoft Entra. Se requieren tres permisos de Graph: `Mail.ReadWrite` (para sincronizar en el Maildir), `Mail.Send` (para preparar plantillas) y `User.Read.All` (para verificar identidades del remitente). El consentimiento de administrador se concede una vez para que el servicio se ejecute como daemon sin interacción humana por mensaje.

Este enfoque confina el límite de confianza en la nube a un único punto bien definido en el pipeline. Cada ciclo de sondeo es un intercambio HTTP discreto y autenticado — en lugar de una conexión IMAP persistente — haciendo que el límite de ingesta sea auditable y sin estado.

## La disciplina WORM

`service-email` escribe cargas útiles en el Maildir WORM — una estructura de solo adición en el almacenamiento de bloque local del Totebox. No hay operación de borrado. Una carga útil escrita en el Maildir no puede borrarse, incluso si la fuente en la nube (el buzón de Microsoft 365) es modificada, eliminada o la suscripción vence. El registro de correo del operador es soberano: pertenece al archivo, no al proveedor de nube.

## Lo que service-email no es

`service-email` es el límite de ingesta, no el cliente de correo. No renderiza correos HTML para que el operador los lea. No sintetiza contenido. No clasifica ni enruta mensajes. Entrega la carga útil en bruto saneada a `service-content` y `service-extraction` y cede la ejecución. Los servicios posteriores manejan todo desde la extracción de entidades hasta la superficie F3 CORREO que ve el operador en `os-console`.

## Véase también

- [[service-people]] — el libro mayor de identidades que recibe registros del remitente de service-email a través de service-extraction
- [[service-content]] — el Motor de Gravedad que sintetiza contenido del Maildir WORM
- [[app-console-input]] — la Máquina de Entrada F12; superficie de ingesta complementaria para cargas útiles que no son correo
- [[sys-adr-07]] — los datos estructurados nunca se enrutan a través de IA (rige el manejo posterior de la salida de service-email)
- [[totebox-os]] — el Totebox que aloja service-email y su almacenamiento WORM
