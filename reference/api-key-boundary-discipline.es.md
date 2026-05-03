---
schema: foundry-doc-v1
title: "Disciplina de límite para claves de API"
slug: api-key-boundary-discipline.es
category: reference
type: topic
quality: published
short_description: La regla que establece que todas las credenciales externas de LLM pertenecen exclusivamente al servicio de pasarela y nunca a los motores de inferencia.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: api-key-boundary-discipline.md
---

## Resumen estratégico

La disciplina de límite para claves de API establece una regla fundamental en el diseño de plataformas de inteligencia artificial: las credenciales de proveedores externos pertenecen exclusivamente al servicio de pasarela (Doorman), nunca a los motores de inferencia. Esta disciplina aplica a todos los niveles de implementación, desde appliances autohospedados hasta trabajadores de cómputo en la nube.

## Principio central

Cualquier proceso que ejecute inferencia de modelos — sea local en hardware del cliente, en trabajadores de ráfaga en nube, o en cualquier nodo de cómputo futuro — no debe leer ni almacenar credenciales de proveedores externos de LLM. Las credenciales fluyen únicamente entre el Doorman y el endpoint del proveedor. No existen excepciones.

## Por qué importa

Tres propiedades estructurales justifican la regla:

**Completitud de auditoría.** Toda llamada a la API pasa por el punto límite de la pasarela. Un ledger de auditoría por tenant puede capturar proveedor, propósito, volumen de tokens y costo en un único punto de control. Las rutas alternativas que evitan la pasarela generan gasto que no puede atribuirse ni auditarse.

**Aplicación de listas de permitidos.** Restringir las llamadas de inferencia a un conjunto definido de propósitos requiere un único punto de aplicación. Una pasarela que recibe todas las solicitudes puede aplicar la lista de permitidos; los motores de inferencia distribuidos entre múltiples nodos de cómputo no pueden.

**Escalado sin estado.** Los procesos de inferencia que no almacenan secretos pueden iniciarse, detenerse y reemplazarse sin rotación de credenciales.

## Patrones prohibidos

- Un proceso de inferencia que lee claves desde variables de entorno, aunque no realice llamadas externas en ese momento.
- Un proceso de inferencia que obtiene claves de un gestor de secretos al arrancar.
- Scripts ad hoc que leen claves de API desde cualquier fuente distinta a la pasarela.
- Almacenamiento del lado del proveedor de claves externas de LLM propiedad del cliente.

## Cumplimiento

La combinación de límite de pasarela, ledger de auditoría por tenant y lista de propósitos permitidos produce un rastro de auditoría criptográfico sobre cada llamada de inferencia externa. Esta estructura satisface los requisitos de integridad de procesamiento de SOC 2 y los principios de cadena de custodia de ISAE 3402 por construcción.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
