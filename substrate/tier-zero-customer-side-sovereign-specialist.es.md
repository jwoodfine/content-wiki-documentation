---
schema: foundry-doc-v1
title: "Especialista soberano en el lado del cliente — Nivel 0"
slug: tier-zero-customer-side-sovereign-specialist
category: substrate
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-customer-ownership
short_description: "El Nivel 0 Totebox es un despliegue especialista soberano que funciona en el propio hardware del cliente sin ninguna dependencia de nube requerida y sin conectividad a internet requerida."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tier-zero-customer-side-sovereign-specialist.md
---


El **Especialista Soberano en el Lado del Cliente — Nivel 0** es el modelo de despliegue de referencia para la plataforma: la pila de plataforma completa funcionando en el propio hardware del cliente — la forma operativa de [[customer-hostability]] — sin dependencia de nube requerida y sin conectividad a internet requerida.

## La unidad de referencia

El despliegue de referencia del Nivel 0 es un Totebox — un dispositivo compacto de factor de forma pequeño (x86 o ARM). Los servicios determinísticos propios de la plataforma (el registro, el motor de conocimiento, los servicios de entrada/extracción/salida) suman unos pocos cientos de megabytes de binarios autónomos; el modelo especialista local, una compilación cuantizada de OLMo 3 de 7B parámetros, es con diferencia el componente individual más grande en disco, varios gigabytes con cuantización de 4 bits. No se requiere GPU.

La pila incluye el [[worm-ledger-architecture|registro de archivos WORM]] (`service-fs`), el motor de conocimiento ([[service-content|`service-content`]]), la [[compounding-doorman|frontera del Portero]] (`service-slm`), el modelo especialista local (OLMo 3 7B Instruct, cuantizado), la interfaz del operador ([[app-console-slm|app-console-slm]]), y los servicios de entrada, extracción y salida. Todos los componentes son binarios autónomos sin dependencias de tiempo de ejecución más allá del sistema operativo.

## Por qué un especialista en lugar de un generalista

El modelo local en el Totebox es un especialista en administración de sistemas con enrutamiento de propósito específico. Gestiona preguntas de administración de sistemas e infraestructura, ediciones mecánicas como mensajes de confirmación de Git y validación de esquemas, consultas de rutina contra el registro de auditoría y el grafo de conocimiento del cliente, y tareas de salida corta.

No está previsto para trabajo editorial, generación bilingüe o razonamiento de formato largo. Esas tareas se enrutan al Nivel B de [[yoyo-compute-substrate|GPU en ráfaga]] cuando está disponible, o devuelven una respuesta elegante de "nivel no disponible" cuando no lo está.

## Inferencia solo con CPU

El especialista del Nivel A es un modelo cuantizado de 7B parámetros, mayor que la clase de modelo que normalmente se esperaría ejecutar cómodamente en núcleos de CPU compartidos — pero la carga de trabajo enrutada al especialista (clasificación de salida corta, ediciones mecánicas, consultas al registro y al grafo de conocimiento) tolera una tasa de tokens por segundo más lenta de lo que exigiría la generación interactiva de formato largo. El operador escribe una pregunta; el especialista responde en pocos segundos para una respuesta corta típica, sin GPU.

No se requieren GPU, mantenimiento de controladores ni gestión térmica. El perfil del hardware es la misma clase que cualquier otro dispositivo interno que el cliente ya opera.

## Propiedades de soberanía

El Totebox opera sin los servidores de la plataforma, sin ninguna relación continua con los autores originales del modelo (los archivos GGUF existentes funcionan indefinidamente), sin claves de API externas (el Nivel C es opt-in y está desactivado por defecto), sin conectividad a internet y sin ninguna suscripción a la nube. El substrato funciona completamente sin conexión.

## Niveles opcionales

El Nivel B (capacidad de GPU en ráfaga) es opt-in por inquilino. El Nivel C (API externa) es opt-in por inquilino y está desactivado por defecto. Cuando se configura, las llamadas a API externas están limitadas a una lista de propósitos explícitamente permitidos, se registran en el registro de auditoría del cliente y se divulgan al operador. Se prevé que la mayoría de los clientes operen sin el Nivel C en absoluto.

## Véase También

- [[substrate-without-inference-base-case]] — operación determinística cuando todos los niveles de IA no están disponibles
- [[single-boundary-compute-discipline]] — toda la inferencia, incluido el especialista local, pasa por el Portero
- [[seed-taxonomy-as-smb-bootstrap]] — la taxonomía por inquilino con la que arranca el despliegue del Nivel 0

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-tier-zero-customer-side-sovereign-specialist.md` (refinado el 30 de abril de 2026). Las estimaciones de costos de hardware y el análisis de mercado se presentan como observaciones estructurales; las afirmaciones de enfoque comercial llevan encuadre BCSC prospectivo.

## Véase también

- [[substrate-without-inference-base-case]]
- [[single-boundary-compute-discipline]]
- [[seed-taxonomy-as-smb-bootstrap]]
