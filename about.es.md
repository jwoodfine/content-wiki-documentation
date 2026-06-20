---
schema: foundry-doc-v1
title: "Acerca de PointSav Knowledge"
slug: about.es
category: governance
type: governance
content_type: page
quality: complete
short_description: "PointSav Knowledge es el wiki de documentación de ingeniería de la plataforma PointSav, al servicio de ingenieros, arquitectos y lectores institucionales."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: about.md
---

PointSav Knowledge es el wiki de documentación de ingeniería de la plataforma PointSav. Está al servicio de ingenieros, arquitectos, revisores de cumplimiento y lectores institucionales que necesitan material de referencia técnica preciso.

## Qué cubre este wiki

El wiki documenta la plataforma PointSav tal como está diseñada y construida:

- Arquitectura de la plataforma y las decisiones de diseño que la condicionan
- Conceptos de sustrato — los mecanismos fundamentales que componen la plataforma
- Patrones de diseño nombrados que se repiten en servicios, aplicaciones e instancias
- Sistemas operativos (`os-*`), servicios autónomos (`service-*`) y aplicaciones (`app-*`)
- Gobierno — registros de decisiones de arquitectura, licencias, modelo de contribuidores, postura de cumplimiento
- Infraestructura — topología de la flota, almacenamiento, red, telemetría
- Material de referencia — nomenclatura, guía de estilo, glosario

## Cómo está construido

PointSav Knowledge funciona sobre `app-mediakit-knowledge`, un motor wiki soberano escrito en Rust. El contenido se almacena como archivos Markdown planos en un repositorio Git. El motor ofrece búsqueda de texto completo BM25, enrutamiento bilingüe (inglés y español), verificación de citas por capa de afirmación e historial de revisiones nativo de Git.

El motor se ejecuta en hardware del cliente bajo MCorp. No tiene dependencia de infraestructura de nube de terceros para el almacenamiento o la recuperación de contenido.

## Licencia

Todo el contenido de este wiki está licenciado bajo [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Contribuir

Las contribuciones a este wiki son bienvenidas. Véase [[contribute.es]] para saber cómo proponer adiciones o correcciones.

## Contacto

[open.source@pointsav.com](mailto:open.source@pointsav.com)
