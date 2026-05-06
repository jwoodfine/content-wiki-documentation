---
schema: foundry-doc-v1
title: "service-people — Libro Contable de Personal"
slug: service-people
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-people.md
cites: []
---

`service-people` es el servicio de ingestión perimetral del Anillo 1 que mantiene un libro contable de personal determinista en archivos planos, almacenando identificadores únicos de contacto, estados de comunicación e historiales de contacto como una base de datos de archivos planos JSON portátil y estable en cuanto al esquema.

## Línea de base arquitectónica

Cada comunicación que entra a través del Anillo 1 lleva identidad del remitente. `service-people` recibe registros de identidad del remitente de `service-extraction` y mantiene un libro contable persistente y consultable de contactos conocidos. Dado que el libro contable es una estructura JSON de archivos planos en lugar de una base de datos relacional o documental, puede copiarse, auditarse e inspeccionarse con herramientas estándar del sistema de archivos.

## El estándar de archivos planos

El diseño adopta el estándar de archivos planos DS-ADR-02, que rechaza los clústeres de bases de datos centralizados en favor de una máquina de estados JSON en archivos planos:

- **Portabilidad.** El libro contable completo es un directorio de archivos JSON que puede moverse a cualquier sistema.
- **Estabilidad del esquema.** Los archivos planos JSON no requieren migraciones de esquema cuando se añaden campos.
- **Auditabilidad.** El libro contable puede inspeccionarse, compararse y versionarse con herramientas estándar.
- **Compatibilidad con modelos.** El formato de archivos planos permite que el libro contable alimente directamente modelos de inteligencia local.

## Integración con el Verificador de Identidad

`service-people` se integra con el Verificador de Identidad, el punto de control humano en el bucle que previene que los errores de extracción automatizada se acumulen en el libro contable verificado.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
