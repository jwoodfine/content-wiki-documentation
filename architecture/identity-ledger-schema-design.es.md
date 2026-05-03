---
schema: foundry-doc-v1
type: topic
slug: identity-ledger-schema-design
title: Diseño del Esquema del Ledger de Identidad
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: identity-ledger-schema-design.md
---

# Diseño del Esquema del Ledger de Identidad

El Ledger de Identidad es el registro canónico y permanente de las personas dentro del ecosistema Foundry. Utiliza un formato de "solo anexar" (append-only) para asegurar que la historia de cada identidad sea inmutable y auditable.

## Principios de Identidad Determinista

- **ID Inmutable (UUIDv5):** La identificación de cada persona se deriva matemáticamente de su correo electrónico principal. Esto garantiza que la misma persona siempre tenga el mismo ID en cualquier sistema, sin necesidad de recurrir a procesos de IA probabilística.
- **Sin IA en la Capa Base (ADR-07):** Siguiendo las normas de seguridad de Foundry, la resolución de identidades es puramente determinista. En caso de ambigüedad, el sistema solicita intervención humana en lugar de realizar fusiones automáticas inciertas.
- **Historial Completo:** Los cambios (como un ascenso o un cambio de teléfono) se guardan añadiendo un nuevo registro. El sistema siempre utiliza la versión más reciente, pero mantiene el rastro de todas las versiones anteriores.

## Roles y Atributos

El esquema permite seguir la evolución de los roles de una persona (empleado, contratista, cliente) mediante "instantáneas temporales". Cada rol especifica su vigencia y atributos específicos del departamento o cargo, permitiendo auditorías precisas sobre quién tenía acceso a qué información en un momento dado.

## Integración MCP

El sistema publica estas identidades mediante el protocolo MCP, permitiendo que otros servicios de Foundry consulten datos de personas de forma segura y estandarizada, sirviendo como la base de confianza para toda la plataforma.
