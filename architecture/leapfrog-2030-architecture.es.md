---
schema: foundry-doc-v1
title: "La Arquitectura Leapfrog 2030"
slug: leapfrog-2030-architecture
language: es
paired_with: leapfrog-2030-architecture.md
category: architecture
type: concept
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
---

Tres fuerzas de mercado que convergen en 2026 — modelos de lenguaje ligeros viables en hardware de consumo, el Protocolo de Contexto de Modelos como estándar de composición de servicios de IA, y el despliegue en instalaciones propias como el segmento de mayor crecimiento en el mercado de software para pymes — abren un espacio estructural que los grandes proveedores de nube no pueden ocupar sin desmantelar su propio modelo de negocio. La Arquitectura Leapfrog 2030 es el compromiso de PointSav con ese espacio: código de plataforma soberano, servicios componibles e ingresos por transacción en lugar de cuotas de licencia recurrentes. El cliente posee su hardware, sus datos y sus pesos de adaptador; PointSav toma un porcentaje por transacción cuando el valor fluye.

## La apuesta estructural

En 2026, tres fuerzas convergen. Los modelos de lenguaje ligeros de código abierto han alcanzado un umbral de utilidad práctica para tareas especializadas. El Protocolo de Contexto de Modelos se ha convertido en el estándar de composición de servicios con inteligencia artificial [mcp-spec]. Y el despliegue en instalaciones propias es el segmento de mayor crecimiento dentro del mercado de software para pymes [idc-smb-2026].

Estas tres fuerzas abren un espacio que los grandes proveedores de nube no pueden ocupar por razones estructurales: su modelo de negocio requiere flujos continuos de datos hacia sus servidores y cobros recurrentes por acceso. PointSav propone una alternativa: el cliente posee su hardware, sus datos, sus pesos de adaptador y sus relaciones comerciales.

## Tres distinciones estructurales

**Soberanía sobre el servicio.** El sistema del cliente está diseñado para operar sin dependencia continua de PointSav. Si PointSav cesa operaciones, la plataforma del cliente está prevista para continuar funcionando.

**Especialización sobre generalización.** El nivel A —siempre activo, instalado en el sitio del cliente— es un especialista de mil millones de parámetros entrenado con los datos del propio cliente. Con el tiempo se torna útil de forma específica para el entorno de ese cliente. El nivel generalista (nivel B, modelos de 32 mil millones de parámetros en GPU) es opcional y por demanda.

**Composición en lugar de captura.** Los ingresos previstos de PointSav se acumulan junto con los ingresos del cliente, no a expensas de ellos. El sustrato de liquidación directa (doctrina, punto #53) está diseñado para que las transacciones de datos fluyan directamente del comprador al cliente.

## Para la pequeña empresa

Una empresa de cinco empleados instala un dispositivo Totebox —un mini-PC de entre trescientos y quinientos dólares— y opera el sustrato completo desde el primer día: libro de registros inmutable, grafo de conocimiento, ingesta de datos y el especialista de inteligencia artificial de nivel A. Un Paquete Semilla Vertical le ofrece un punto de partida personalizable en aproximadamente treinta minutos.

Cada interacción con el sistema es un posible ejemplo de entrenamiento para el adaptador propio del cliente. Con el tiempo, el especialista se prevé calibrado para ese entorno específico. La soberanía de datos no es una función adicional; es el modo operativo diseñado por defecto.

## Véase también

- [[compounding-substrate]] — El Sustrato Compuesto: fundamento económico y técnico
- [[service-slm-yoyo-operational]] — Estado operacional del nivel B (Yo-Yo) y Doorman
- [[source-of-truth-inversion]] — El patrón canónico/vista/efímero que sustenta el sustrato
