---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: zero-execution-routing
short_description: "Las capas de presentación en la plataforma cumplen un mandato de ejecución cero, eliminando JavaScript del lado del cliente para manipulación central de DOM mediante el uso de determinismo estructural para enrutamiento bilingüe y máquinas de estado CSS nativas para elementos interactivos."
title: Enrutamiento y presentación de ejecución cero
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: zero-execution-routing.md
category: patterns
last_edited: 2026-05-25
editor: pointsav-engineering
---



Las capas de presentación de la plataforma siguen un mandato de "Ejecución Cero", eliminando el uso de JavaScript en el cliente para la manipulación de la interfaz y el enrutamiento de idiomas. Esta arquitectura minimiza la superficie de ataque y garantiza un rendimiento instantáneo. El patrón complementa la capa de [[machine-based-auth|autenticación basada en máquinas]] y la arquitectura de [[sovereign-ai-routing|enrutamiento de IA soberana]].

## Enrutamiento Bilingüe Determinista

La plataforma no utiliza scripts de detección de IP. El cambio de idioma es estructural:
- **Directorio Raíz (`/`):** Contiene la versión por defecto en inglés.
- **Subdirectorio de Idioma (`/es/`):** Contiene el mismo archivo, pero con el estado de idioma español activado de forma nativa en el código HTML.

## Máquina de Estado de CSS Puro

Los elementos interactivos (como el cambio de idioma o botones dinámicos) funcionan mediante lógica de CSS puro:
- **Carga Simultánea:** El navegador carga todos los bloques de idioma a la vez.
- **Cambio Instantáneo:** Las reglas de CSS muestran u ocultan el contenido según el estado de un selector nativo del navegador.
- **Cero Latencia:** Se logra la fluidez de una aplicación moderna sin los riesgos de seguridad y retrasos asociados a la ejecución de scripts externos.

## Véase también

- [[sovereign-ai-routing]] — la arquitectura de enrutamiento de IA soberana que se combina con esta disciplina de ejecución cero
- [[machine-based-auth]] — capa de autenticación basada en máquinas que opera en el mismo contexto de presentación de confianza cero
- [[decode-time-constraints]] — restricciones en tiempo de decodificación que aplican los límites de ejecución deterministas
- [[sel4-microkernel-substrate]] — el sustrato de microkernel que fundamenta el modelo de aislamiento de ejecución
