---
schema: foundry-doc-v1
title: "Servicio de inferencia de IA"
slug: service-slm
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-3-ai-gateway
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-slm.md
short_description: "service-slm es la puerta de enlace de inferencia de IA de la plataforma — cada solicitud, local o remota, transita el límite de auditoría del Doorman y uno de tres niveles de cómputo antes de que se devuelva una respuesta."
cites:
 - olmo3-allenai
references:
  - id: 1
    text: "ISO/IEC 42001:2023 — Tecnología de la información — Inteligencia artificial — Sistema de gestión."
    url: "https://www.iso.org/standard/81230.html"
  - id: 2
    text: "Groeneveld, D. et al. 'OLMo: Accelerating the Science of Language Models.' arXiv:2402.00838, 2024."
    url: "https://arxiv.org/abs/2402.00838"
---

Una solicitud de IA que sale del edificio no puede auditarse ni recuperarse. `service-slm` es
la puerta de enlace de inferencia de IA de la plataforma — el espacio de trabajo que aloja el
enrutador [[doorman-protocol|Doorman]] y sus crates de soporte. Su propiedad central es que
cada llamada de inferencia, sea cual sea el nivel que finalmente la sirva, cruza primero el
límite de auditoría del Doorman.

## El Doorman enruta, quien llama solo sugiere

`service-slm` implementa [[model-tier-discipline|la disciplina de enrutamiento por niveles
de la plataforma]]: quien llama envía una sugerencia de complejidad, no una elección de nivel,
y el Doorman elige una de tres rutas según esa sugerencia más el estado de presupuesto en
tiempo real.

| Ruta | Dónde se ejecuta | Modelo |
|---|---|---|
| Local | En el mismo host que el Doorman | OLMo 3 7B cuantizado, servido por HTTP |
| Yoyo | Una instancia GPU multi-nube prescindible de ráfaga | Un modelo OLMo 3 más grande ajustado para razonamiento más profundo |
| External | Una API de terceros con licencia, controlada por lista blanca | Un modelo de frontera, solo para tareas de precisión crítica y estrechas |

Estos tres niveles de enrutamiento interno son un sistema distinto de la escala de
suscripción comercial de cara al cliente descrita en [[pointsav-llm]] — el propio código
fuente nombra el enum de enrutamiento deliberadamente para evitar que ambos se confundan.

## El límite de auditoría del Doorman

Cada mensaje y cada finalización capturados por el Doorman se escriben en una ruta de
auditoría antes de que la respuesta regrese a quien llamó, formando el registro institucional
de cada decisión de IA. El Doorman existe por tres razones:

1. **Regulatoria.** ISO/IEC 42001, el estándar de sistema de gestión de IA [^1], exige un
   registro inmutable de las decisiones asistidas por IA.
2. **Operativa.** Un sistema autocurativo necesita un corpus de su propio comportamiento
   pasado para mejorar; la captura de auditoría lo proporciona.
3. **Soberana.** Ninguna solicitud llega a una API de terceros sin antes pasar por un límite
   que controla el operador.

Detalle completo sobre el enrutamiento y los mecanismos de auditoría propios del Doorman:
[[doorman-protocol]].

## Selección de modelo

El modelo local canónico proviene de la familia OLMo, que se distribuye con pesos
completamente abiertos y documentación de datos de entrenamiento [^2]. Esto es un requisito
previo para el pre-entrenamiento continuo sobre el propio corpus de un operador, la ruta a
largo plazo hacia un modelo especializado por dominio.

## Por qué un modelo pequeño, por defecto

Un modelo de escala de frontera impone costos que el nivel Local está diseñado para evitar:
egreso a la nube, decenas de gigabytes de RAM, y una solicitud que no puede auditarse de
manera significativa. Un modelo cuantizado de 7B es suficiente para la mayoría de las
solicitudes y cabe dentro del presupuesto de costo de un nodo de bajo costo que se ejecuta
junto al resto de la plataforma. La especialización y la segmentación por niveles, no la escala por defecto,
es el principio de diseño — los niveles Yoyo y External existen precisamente para las
solicitudes donde genuinamente se necesita más capacidad.

## Véase también

- [[doorman-protocol]] — los mecanismos de enrutamiento y auditoría del Doorman en detalle
- [[model-tier-discipline]] — la disciplina de enrutamiento por niveles que implementa este servicio
- [[pointsav-llm]] — la escala comercial distinta, de cara al cliente
- [[architecture-decisions|SYS-ADR-07]] — los datos estructurados nunca se enrutan a través de IA; el Doorman implementa este límite
- [[run-local-slm-inference]] — guía paso a paso: iniciar el servicio SLM y enviar solicitudes de inferencia desde la consola o la API
- [[run-first-slm-query]] — guía paso a paso: leer el panel de salud del Doorman y enviar tu primera consulta
