---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: identity-ledger-schema-design
short_description: "El Identity Ledger proporciona un registro de solo anexión basado en JSONL de identidades de personas canónicas utilizando derivación UUIDv5 determinista de direcciones de correo electrónico y disciplina WORM. Sirve como la fuente unificada para todos los puntos finales de comunicación y copias instantáneas de roles temporales, permitiendo resolución de entidades determinista sin inferencia probabilística."
title: Diseño del esquema del ledger de identidad
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: identity-ledger-schema-design.md
category: architecture
---



El Ledger de Identidad es el registro canónico y permanente de las personas dentro de la plataforma. Utiliza un formato de "solo anexar" (append-only) basado en la disciplina [[worm-ledger-architecture|WORM]] para asegurar que la historia de cada identidad sea inmutable y auditable. Servido por [[service-people]] y consultado mediante [[mcp-substrate-protocol|MCP]].

## Puntos clave

- La resolución de identidades es completamente determinista. El identificador principal (`identity_id`) es un UUIDv5 derivado del correo electrónico principal del usuario — el mismo correo siempre produce el mismo UUID en cualquier nodo, sin IA ni coincidencia probabilística. Esto satisface el requisito del ADR-07 de que la extracción en el Anillo 1 no utilice inferencia.
- Los registros de identidad siguen la [[worm-ledger-architecture|disciplina WORM]]. Los cambios de rol, nuevos puntos de contacto y otras actualizaciones se añaden como nuevos registros; los lectores obtienen el registro más reciente por `identity_id`. El historial de adiciones completo se preserva como un registro de auditoría inmutable de la progresión de la identidad en el tiempo.
- Un único registro de identidad es la fuente autorizada de todos los puntos de contacto: correo electrónico (RFC 5322), teléfono (E.164) y gestores tipados de plataforma (Slack, Teams, Signal). Los servicios posteriores resuelven los puntos de contacto desde este registro — no derivan ni cachean los suyos propios.
- Las identidades ambiguas o en conflicto se presentan a un operador humano en lugar de fusionarse silenciosamente. Extracción determinista en el Anillo 1; resolución humana para las excepciones. Ningún modelo probabilístico realiza fusiones silenciosas en la ingesta.

## Principios de Identidad Determinista

- **ID Inmutable (UUIDv5):** La identificación de cada persona se deriva matemáticamente de su correo electrónico principal. Esto garantiza que la misma persona siempre tenga el mismo ID en cualquier sistema, sin necesidad de recurrir a procesos de IA probabilística.
- **Sin IA en la Capa Base (ADR-07):** Siguiendo las normas de seguridad de la plataforma, la resolución de identidades es puramente determinista. En caso de ambigüedad, el sistema solicita intervención humana en lugar de realizar fusiones automáticas inciertas.
- **Historial Completo:** Los cambios (como un ascenso o un cambio de teléfono) se guardan añadiendo un nuevo registro. El sistema siempre utiliza la versión más reciente, pero mantiene el rastro de todas las versiones anteriores.

## Roles y Atributos

El esquema permite seguir la evolución de los roles de una persona (empleado, contratista, cliente) mediante "instantáneas temporales". Cada rol especifica su vigencia y atributos específicos del departamento o cargo, permitiendo auditorías precisas sobre quién tenía acceso a qué información en un momento dado.

## Integración MCP

El sistema publica estas identidades mediante el [[mcp-substrate-protocol|protocolo MCP]], permitiendo que otros servicios de la plataforma consulten datos de personas de forma segura y estandarizada, sirviendo como la base de confianza para toda la plataforma.

## Véase también

- [[machine-based-auth]]
- [[capability-based-security]]
- [[worm-ledger-design]]
- [[cryptographic-ledgers]]
