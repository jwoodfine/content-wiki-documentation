---
schema: foundry-doc-v1
title: "Iniciativa de Reemplazo Soberano"
slug: sovereign-replacement-initiative
short_description: "La Iniciativa de Reemplazo Soberano es el programa de gobernanza de ingeniería que rastrea dependencias de terceros, las aísla en directorios de componentes en cuarentena, y coordina los programas moonshot activos que construyen reemplazos nativos."
category: governance
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: sovereign-replacement-initiative.md
cites: []
---


La Iniciativa de Reemplazo Soberano es el programa formal que registra cada dependencia foránea en un libro contable estructurado, aplica aislamiento de cuarentena hasta que un reemplazo nativo esté listo, y retira la dependencia una vez que el reemplazo alcanza paridad estructural.

## El problema estructural

Cualquier plataforma que haya pasado por una fase de transformación digital hereda componentes arquitectónicos de terceros que no diseñó. La dependencia de esos componentes — proveedores de autenticación en la nube propietarios, controladores de GPU foráneos, APIs de grafos comerciales — crea un riesgo estructural: si un proveedor de terceros cambia sus condiciones de servicio o depreca una API, la plataforma dependiente debe adaptarse bajo presión o detenerse.

## El libro contable de dependencias

La Iniciativa mantiene un libro contable físico de dependencias de terceros pendientes. Cada entrada registra la dependencia, el riesgo estructural que representa, y el estado de la iniciativa moonshot que construye el reemplazo.

El libro contable hace la deuda visible. La visibilidad evita que se acumule silenciosamente — una dependencia no registrada es una dependencia que no recibe priorización de ingeniería.

## Criterios de finalización

Una entrada del libro contable se cierra cuando la iniciativa moonshot asociada alcanza **paridad estructural** con el componente en cuarentena que reemplaza. La paridad estructural tiene tres condiciones:

1. **Cobertura funcional.** La implementación nativa cubre todos los casos de uso de la plataforma que actualmente sirve el componente en cuarentena.
2. **Supersesión física.** El directorio `vendor-*` en cuarentena se elimina del repositorio. No quedan referencias en el código fuente al componente reemplazado.
3. **Objetivo de verificación formal.** Para componentes en la capa de kernel, la implementación nativa satisface el requisito de verificación formal de la plataforma (compatible con seL4, memoria segura, sin desbordamiento de búfer). Para componentes en la capa de aplicación, se cumplen los requisitos de cobertura de pruebas y la integración con el libro contable de auditoría.

Hasta que se cumplan las tres condiciones, la cuarentena permanece activa y la entrada del libro contable sigue abierta.

## Relación con ADR-08

La [[architecture-decisions|Decisión de Arquitectura 8]] registra formalmente el sistema de inicio systemd como una dependencia en cuarentena — la dependencia que la plataforma acepta mientras la iniciativa `moonshot-kernel` avanza hacia el reemplazo con el micronúcleo seL4. La Iniciativa de Reemplazo Soberano es el mecanismo de gobernanza que da fuerza operativa a ADR-08: sin el libro contable, la cuarentena es una declaración de intención; con el libro contable, es un compromiso rastreado con una trayectoria de finalización definida.

## Véase también

- [[moonshot-initiatives]]
- [[ontological-governance]]
- [[verification-surveyor]]
- [[customer-hostability]]
