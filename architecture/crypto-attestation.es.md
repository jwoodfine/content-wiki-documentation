---
schema: foundry-doc-v1
title: "Attestación Criptográfica de Cargas"
slug: crypto-attestation
category: architecture
type: topic
quality: core
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: crypto-attestation.md
cites: []
---

La attestación criptográfica de cargas es el mecanismo por el cual los nodos perimetrales de PointSav demuestran dinámicamente la integridad de su contenido textual publicado a cualquier espectador. Utiliza hashing SHA-256 del lado del cliente, de modo que cualquier auditor puede verificar independientemente que una divulgación no ha sido alterada en tránsito.

## Cómo funciona

Todos los nodos perimetrales públicos calculan y muestran dinámicamente un hash SHA-256 de su contenido de idioma visible. Cualquier inversor institucional, auditor o contraparte puede copiar el texto de forma independiente, calcular el hash localmente con cualquier herramienta SHA-256, y confirmar que el hash mostrado coincide — lo que prueba que el contenido no ha sido alterado entre la publicación y la pantalla del espectador.

La operación se ejecuta completamente en el navegador, sin participación del servidor en el propio cálculo del hash. Esto significa que la attestación es independiente de si la infraestructura de servicio es confiable.

## Postura de seguridad

La attestación es de cero ejecución en el servidor para el cálculo del hash: el servidor entrega el JavaScript y el contenido, pero el hash lo calcula el navegador usando solo datos locales. Un atacante intermediario que modificara el contenido en tránsito produciría una discrepancia de hash que cualquier espectador podría detectar.

## Aplicaciones

- Divulgaciones regulatorias públicas en nodos perimetrales operados por PointSav.
- Artículos del wiki de contenido donde la verificación de integridad importa a lectores institucionales.
- Cualquier superficie de contenido donde un lector necesite confirmar que está leyendo la versión publicada.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
