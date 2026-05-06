---
schema: foundry-doc-v1
title: "Especialista Soberano en el Lado del Cliente — Nivel 0"
slug: tier-zero-customer-side-sovereign-specialist.es
category: architecture
type: topic
quality: published
short_description: "El Nivel 0 Totebox es un despliegue especialista soberano que funciona en el propio hardware del cliente sin ninguna dependencia de nube requerida y con una huella total de 1 GB."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tier-zero-customer-side-sovereign-specialist.md
---

El **Especialista Soberano en el Lado del Cliente — Nivel 0** es el modelo de despliegue de referencia para Foundry: la pila de plataforma completa funcionando en el propio hardware del cliente, sin dependencia de nube requerida, sin conectividad a internet requerida, y con una huella de disco total de aproximadamente un gigabyte. Este patrón codifica la reclamación doctrinal #49.

## La unidad de referencia

El despliegue de referencia del Nivel 0 es un Totebox — un dispositivo compacto de factor de forma pequeño (x86 o ARM). La pila completa ocupa aproximadamente un gigabyte de disco y un conjunto de trabajo de dos a cuatro gigabytes de memoria en dos a cuatro núcleos de CPU. No se requiere GPU.

La pila incluye el registro de archivos WORM (`service-fs`), el motor de conocimiento (`service-content`), la frontera del Portero (`service-slm`), el modelo especialista local (OLMo 2 1B a aproximadamente 600 MB en disco), la TUI del operador (`slm-cli`), y los servicios de entrada, extracción y salida. Todos los componentes son binarios autónomos sin dependencias de tiempo de ejecución más allá del sistema operativo.

## Por qué un especialista en lugar de un generalista

El modelo local en el Totebox es un especialista en administración de sistemas con enrutamiento de propósito específico. Gestiona preguntas de administración de sistemas e infraestructura, ediciones mecánicas como mensajes de confirmación de Git y validación de esquemas, consultas de rutina contra el registro de auditoría y el grafo de conocimiento del cliente, y tareas de salida corta.

No está previsto para trabajo editorial, generación bilingüe o razonamiento de formato largo. Esas tareas se enrutan al Nivel B de GPU en ráfaga cuando está disponible, o devuelven una respuesta elegante de "nivel no disponible" cuando no lo está.

## Base empírica para la inferencia solo con CPU

La afirmación del Nivel A se basa en rendimiento medido, no en capacidad teórica: en un despliegue de solo cuatro vCPU, el modelo de 1B parámetros con cuantización de cuatro bits produce aproximadamente siete tokens por segundo, generando respuestas completas en el rango de seis segundos para respuestas típicas de 40 tokens. Esto es suficientemente rápido para uso conversacional humano.

No se requieren GPU, mantenimiento de controladores ni gestión térmica. El perfil del hardware es la misma clase que cualquier otro dispositivo interno que el cliente ya opera.

## Propiedades de soberanía

El Totebox opera sin los servidores de Foundry, sin ninguna relación continua con los autores originales del modelo (los archivos GGUF existentes funcionan indefinidamente), sin claves de API externas (el Nivel C es opt-in y está desactivado por defecto), sin conectividad a internet y sin ninguna suscripción a la nube. El substrato funciona completamente sin conexión.

## Niveles opcionales

El Nivel B (capacidad de GPU en ráfaga) es opt-in por inquilino. El Nivel C (API externa) es opt-in por inquilino y está desactivado por defecto. Cuando se configura, las llamadas a API externas están limitadas a una lista de propósitos explícitamente permitidos, se registran en el registro de auditoría del cliente y se divulgan al operador. Se prevé que la mayoría de los clientes operen sin el Nivel C en absoluto.

## Véase También

- [[substrate-without-inference-base-case]] — operación determinística cuando todos los niveles de IA no están disponibles
- [[single-boundary-compute-discipline]] — toda la inferencia, incluido el especialista local, pasa por el Portero
- [[seed-taxonomy-as-smb-bootstrap]] — la taxonomía por inquilino con la que arranca el despliegue del Nivel 0

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-tier-zero-customer-side-sovereign-specialist.md` (refinado el 30 de abril de 2026). Las estimaciones de costos de hardware y el análisis de mercado se presentan como observaciones estructurales; las afirmaciones de enfoque comercial llevan encuadre BCSC prospectivo.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
