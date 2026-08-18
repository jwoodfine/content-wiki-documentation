---
schema: foundry-doc-v1
title: "PointSav-LLM"
slug: pointsav-llm
category: ai
type: topic
content_type: topic
quality: complete
index_group: compute-tiers
short_description: "El modelo de IA especialista planificado para el Nivel 3 del sistema de cuatro niveles SLM de PointSav, construido mediante entrenamiento continuo de OLMo 3 32B sobre el corpus federado de aprendizaje de la plataforma."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: pointsav-llm.md

---

**PointSav-LLM** es el modelo de IA especialista planificado para el Nivel 3 del [[four-tier-slm-substrate|escalón SLM de cuatro niveles]] de [[pointsav-overview|PointSav]]. No es un producto activo en la fecha de este artículo. Se trata de una trayectoria planificada: el primer ciclo de entrenamiento continuo (CPT, por sus siglas en inglés) está actualmente previsto para v0.5.0 en el primer trimestre de 2027, con un despliegue productivo actualmente previsto para v1.0.0 en el cuarto trimestre de 2027.

*Todas las descripciones de capacidades, calendarios, estructuras de precios y objetivos de rendimiento de este artículo son de carácter prospectivo. Son planes o intenciones, no hechos operativos actuales. Los resultados reales dependen de la tasa de crecimiento del corpus, el rendimiento del modelo, la capacidad de ingeniería y las condiciones del mercado. [ni-51-102] [osc-sn-51-721]*

---

## Lo que es y lo que no es

PointSav-LLM está planificado como especialista en un dominio concreto, no como modelo de propósito general. Su corpus de entrenamiento previsto proviene del [[apprenticeship-substrate|sustrato de aprendizaje]] de la plataforma: los registros de trayectoria, los pares de decisiones editoriales y los historiales de commits alineados con el código que producen las sesiones de agente contribuyentes en toda la plataforma.

Sus áreas de especialización previstas incluyen la operación del [[totebox-archive|Archivo Totebox]], las convenciones de [[pointsav-overview|PointSav]], los patrones editoriales multiusuario, la generación de código alineada con las convenciones de la plataforma y los flujos de contribución de entrenamiento federado.

### Qué no está previsto que sea

PointSav-LLM no está planificado para competir con modelos de frontera de amplio alcance en conocimiento general, profundidad creativa o razonamiento multidisciplinar. Las consultas que requieran esa amplitud continuarán siendo enrutadas por el [[doorman-protocol|Doorman]] del cliente hacia las APIs externas del Nivel C (Nivel C externo). La base OLMo 3 (Apache 2.0; Open Data Commons) es abierta, y los adaptadores portátiles por cliente están planificados para preservar la soberanía del tenant: un cliente que abandone la plataforma conservaría el derecho a llevarse los datos que aportó y cualquier ajuste fino específico de su tenant que haya financiado.

---

## Cómo se prevé el acceso

El acceso de los clientes está previsto que se realice íntegramente a través del [[doorman-protocol|Doorman]] local de cada cliente. No se realizan llamadas directas al endpoint de PointSav-LLM desde el código de la aplicación del cliente.

La secuencia planificada es la siguiente: el Doorman recibe la consulta, clasifica su complejidad mediante el modelo local del Nivel A (OLMo 3 7B Q4), y enruta hacia el Nivel A para consultas sencillas o hacia el endpoint de PointSav-LLM para consultas que requieran profundidad especialista. La respuesta retorna a través del Doorman, se escribe una fila de auditoría tanto en el Doorman del cliente como en la pasarela de PointSav-LLM, y la facturación por token se computa en la pasarela. El código de la aplicación del cliente no cambia entre el enrutamiento local del Nivel A y el enrutamiento al Nivel C de PointSav-LLM.

---

## Diseño con intervención humana

Cuando la confianza del modelo cae por debajo de un umbral, la respuesta está planificada para incluir señales de confianza estructuradas: `confidence: low`, `escalate_to_human: true` y una etiqueta de motivo de escalado. El Doorman del cliente presenta entonces una opción de escalado al usuario, como "Consultar con un ingeniero de PointSav".

Los eventos de escalado resueltos por ingenieros humanos están planificados para convertirse en pares de datos de entrenamiento DPO para el siguiente ciclo CPT, a través del sustrato de aprendizaje. La distribución prevista es: aproximadamente el 80–90% de las consultas gestionadas de forma autónoma en el Nivel L1, las restantes con intervención humana en L2, y los casos límite no resueltos escalados al Nivel L3 de ingeniería. Todos los porcentajes son objetivos planificados, ilustrativos y no estimaciones con fuente.

Este sobre de respuesta no existe en el código hoy, algo consistente con un producto de Nivel 3 sin estado operativo. Un mecanismo relacionado, distinto, ya funciona en otra parte de la plataforma: las trayectorias internas de aprendizaje de los agentes de IA se condicionan con una puntuación de confianza y un umbral de escalado, que determinan si el propio intento de una sesión de IA se escala a un revisor sénior dentro del espacio de trabajo. Ese mecanismo no es un sobre de respuesta de PointSav-LLM orientado al cliente, pero es un precedente funcional del mismo patrón: puntuación de confianza, umbral, escalado.

Infraestructura relacionada ya funciona hoy para un nivel distinto de la escalera comercial: infraestructura funcional de LoRA/adaptadores que sirve a adaptadores por inquilino-cliente y por grafo de commits (Nivel 1/2 de la escalera comercial), no al modelo CPT de Nivel 3 que describe este artículo.

---

## Posicionamiento en el mercado

El mercado de IA para atención al cliente y conocimiento empresarial en 2026 está servido principalmente por productos de código cerrado y totalmente gestionados, estructurados para grandes compradores empresariales. Los compromisos contractuales mínimos, los precios por puesto y las condiciones de residencia de datos pensadas para organizaciones de miles de personas hacen que estos productos sean estructuralmente inaccesibles para la mayoría de las pequeñas y medianas empresas.

Las PYME de 10 a 200 empleados que necesitan asistencia de IA en sus operaciones de archivo, sus flujos editoriales o su función de atención al cliente se enfrentan a dos opciones bajo la estructura de mercado actual: asumir precios pensados para organizaciones un orden de magnitud mayores, u operar sin asistencia de IA. Una tercera opción — alojar por cuenta propia modelos de propósito general de código abierto — exige experiencia en infraestructura de aprendizaje automático que la mayoría de las PYME no tiene.

### Cubrir el vacío de las PYME

PointSav-LLM está pensado para cubrir precisamente este vacío. La arquitectura planificada enruta las consultas especialistas a través de un modelo mantenido por el proveedor, sin exigir a los clientes que aprovisionen infraestructura GPU, gestionen actualizaciones del modelo o negocien contratos de nivel empresarial. Los clientes que contribuyen datos de trayectoria al corpus bajo el nivel contribuyente están previstos para recibir tarifas por token preferenciales, ya que sus datos aumentan la profundidad especialista del modelo para cada suscriptor posterior.

---

## Estructura de precios (trayectoria planificada)

Tres niveles de suscripción planificados; los detalles y las tarifas específicas por token aún no se han publicado:

**Nivel Abierto (gratuito, contribuidor comunitario)**
- Acceso previsto: acceso de lectura al common de conocimiento, foro comunitario, documentación pública.
- Acceso al modelo: solo el modelo local del Nivel A (alojado por el cliente).
- Contribución al corpus: no incluida.
- Punto de entrada objetivo: individuos y organizaciones que contribuyen al common de conocimiento, con un objetivo de 10,000 o más usuarios registrados a nivel de plataforma.

**Nivel C de pago (por token, suscripción)**
- Acceso previsto: API de PointSav-LLM mediante enrutamiento del Doorman.
- Precio por token: previsto para ser accesible al tamaño de contrato típico de una PYME; tarifas específicas aún no publicadas.
- Contribución al corpus: solo lectura; contribuye telemetría de consultas anonimizada.
- SLA: compromisos estándar de tiempo de respuesta.

**Nivel C+ de pago (premium)**
- Acceso previsto: API de PointSav-LLM con reserva de SLA de escalado.
- Precio: por token más horas de escalado reservadas.
- Contribución al corpus: datos de trayectoria completos del nivel contribuyente, previstos para generar tarifas por token preferenciales en ciclos de facturación posteriores como crédito acumulativo.
- SLA: compromisos de tiempo de respuesta mejorados más ventana de respuesta de escalado L2/L3.

Las tarifas específicas por token y las ventanas de SLA de escalado se publicarán cuando estén disponibles los datos de evaluación del primer ciclo CPT. Todos los precios son planificados y están sujetos a revisión según los costos de infraestructura, el rendimiento del modelo y las condiciones del mercado. [ni-51-102] [osc-sn-51-721]

---

## Relación con la Escalera de Cuatro Niveles del Sustrato SLM

PointSav-LLM ocupa el Nivel 3 de la Escalera de Cuatro Niveles del Sustrato SLM planificada. Los cuatro niveles, tal como están diseñados actualmente:

| Nivel | Nombre | Base | Estado |
|------|------|------|--------|
| 0 | Núcleo determinista | Reglas, regex, búsqueda estructurada | Operativo |
| A | Modelo local pequeño | OLMo 3 7B Q4 (CPU) | Operativo (llama-server local) |
| B | Cómputo de ráfaga | `Olmo-3-1125-32B-Think` (GPU vía Yo-Yo) | Operativo |
| C | Especialista del proveedor | PointSav-LLM (CPT planificado del modelo base OLMo 3 32B) | Planificado — primer trimestre de 2027 |

Los niveles 0, A y B son operativos hoy. El Nivel C (PointSav-LLM) está planificado, sin estado operativo en la fecha de este artículo. La lógica de enrutamiento del Doorman para el Nivel C es infraestructura planificada; su estado actual es únicamente enrutamiento a los Niveles A/B.

Los niveles técnicos A/B/C de enrutamiento de cómputo de esta tabla y la escalera comercial 0/1/2/3 orientada al cliente (los niveles de precios Abierto/C de pago/C+ de pago descritos más adelante) son dos esquemas de numeración separados que comparten dígitos por coincidencia — no la misma escalera, aunque la columna única "0/A/B/C" de esta tabla los fusiona visualmente.

---

## Fundamento de código abierto

La base técnica de PointSav-LLM es el modelo base OLMo 3 32B, publicado por AllenAI bajo licencia Apache 2.0, con datos de entrenamiento base bajo Open Data Commons — no la variante "Think", que AllenAI no ha publicado en el tamaño de 32B. Esta elección es estructural: una base completamente abierta permite el entrenamiento continuo propio (CPT), la auditoría independiente de los pesos y la portabilidad para el cliente. Los pesos base son abiertos; el valor comercial de PointSav reside en el CPT especialista sobre el corpus agregado de la plataforma, la infraestructura de escalado con intervención humana, el sustrato de auditoría por tenant y el SLA.

---

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que hacen posible la trayectoria de CPT federado
- [[service-slm-yoyo-operational]] — el estado operativo actual de los Niveles A/B del que este artículo describe el Nivel 3
- [[apprenticeship-substrate]] — el bucle DPO que alimenta el corpus CPT
- [[brief-queue-substrate]] — cola durable para la acumulación de briefs
- [[contributor-model]] — el Modelo de Contribuidor de Tres Niveles alineado con los niveles de precios
- [[service-slm|Servicio SLM]] — el servicio de modelo local que PointSav-LLM está previsto para extender en el Nivel C
- [[slm-stack-architecture|Arquitectura del Stack SLM]] — la Escalera de Cuatro Niveles del Sustrato SLM de la que este artículo describe el Nivel 3

---

## Referencias

1. AllenAI. *Familia de modelos OLMo 3*. Licencia Apache 2.0; datos de entrenamiento bajo licencia Open Data Commons. https://allenai.org/olmo
2. *National Instrument 51-102 Continuous Disclosure Obligations.* British Columbia Securities Commission. [ni-51-102]
3. *OSC Staff Notice 51-721: Forward-Looking Information Disclosure.* Ontario Securities Commission. [osc-sn-51-721]
