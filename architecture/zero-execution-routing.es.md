---
schema: foundry-doc-v1
type: topic
slug: zero-execution-routing
title: Enrutamiento y Presentación de Ejecución Cero
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: zero-execution-routing.md
---

# Enrutamiento y Presentación de Ejecución Cero

La capa de presentación de Foundry sigue un mandato de "Ejecución Cero", eliminando el uso de JavaScript en el cliente para la manipulación de la interfaz y el enrutamiento de idiomas. Esta arquitectura minimiza la superficie de ataque y garantiza un rendimiento instantáneo.

## Enrutamiento Bilingüe Determinista

Evitamos el uso de scripts de detección de IP. El cambio de idioma es estructural:
- **Directorio Raíz (`/`):** Contiene la versión por defecto en inglés.
- **Subdirectorio de Idioma (`/es/`):** Contiene el mismo archivo, pero con el estado de idioma español activado de forma nativa en el código HTML.

## Máquina de Estado de CSS Puro

Los elementos interactivos (como el cambio de idioma o botones dinámicos) funcionan mediante lógica de CSS puro:
- **Carga Simultánea:** El navegador carga todos los bloques de idioma a la vez.
- **Cambio Instantáneo:** Las reglas de CSS muestran u ocultan el contenido según el estado de un selector nativo del navegador.
- **Cero Latencia:** Se logra la fluidez de una aplicación moderna sin los riesgos de seguridad y retrasos asociados a la ejecución de scripts externos.
