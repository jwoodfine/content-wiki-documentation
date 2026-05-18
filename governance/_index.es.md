---
schema: foundry-doc-v1
title: "Gobernanza — Página de categoría"
slug: _index.es
short_description: "Registros formales de decisiones, postura de licenciamiento, modelo de contribuidor y requisitos de cumplimiento que rigen cómo se construye, licencia y modifica la plataforma PointSav — incluyendo las doce decisiones arquitectónicas vinculantes, la postura de divulgación continua BCSC y la matriz de licencias."
lang: es
paired_with: _index.md
category: governance
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
---

## Gobernanza

Esta categoría cubre los registros de decisiones formales, la postura de licencias, el modelo de colaboración y los requisitos de cumplimiento que rigen cómo se construye, licencia y modifica la plataforma PointSav a lo largo del tiempo. Los artículos de gobernanza son el registro escrito de decisiones tomadas y su justificación; no son declaraciones de intención.

Las doce [[architecture-decisions|decisiones de arquitectura vinculantes]] son las entradas más importantes de esta categoría para la diligencia debida técnica y la revisión regulatoria: definen dónde se detiene el procesamiento automatizado y dónde comienza la autoridad humana, cómo se separan los datos y dónde deben residir las claves criptográficas. La postura de divulgación continua de la BCSC documenta los requisitos de la normativa canadiense de valores tal como se aplican a la plataforma y su documentación pública.

## Artículos en esta categoría

### Debida diligencia institucional

Punto de entrada para la evaluación de adquisición, seguridad y cumplimiento.

- [[procurement-overview]] — Lo que adquiere un comprador regulado: despliegue en hardware propiedad del cliente, datos que el proveedor nunca posee, sin compromiso de gasto mínimo, y propiedades de cumplimiento aplicadas por arquitectura.
- [[security-overview]] — La postura de seguridad de la plataforma: aislamiento basado en capacidades, el estándar Diode de flujo de comandos unidireccional, el límite de IA Portero, el libro de auditoría WORM y cómo cada propiedad es aplicada por arquitectura.
- [[compliance-and-continuous-disclosure]] — Cómo la plataforma produce registros con calidad de divulgación continua y qué significa esto para los compradores regulados.
- [[bcsc-disclosure-posture]] — La postura de divulgación continua de la BCSC y cómo la plataforma la satisface por estructura.

### Registros de decisiones formales

- [[architecture-decisions]] — Las doce decisiones de arquitectura vinculantes que restringen toda la ingeniería futura; agrupadas por peso regulatorio, separación de datos, custodia del despliegue e integridad operativa.

### Licencias y contribución

- [[contributor-model]] — El modelo de colaboración de tres niveles: comunidad abierta, integradores de pago y el nivel de proveedor canónico.
- [[canadian-simple-copyright]] — La postura de derechos de autor conforme al derecho canadiense: selección de licencias y contexto jurídico.

## Véase también

- [Inicio del wiki](/)
- [Arquitectura](/architecture/)
- [Infraestructura](/infrastructure/)
- [Referencia](/reference/)
