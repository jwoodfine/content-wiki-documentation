---
schema: foundry-doc-v1
title: "PointSav-LLM"
slug: pointsav-llm.es
category: architecture
type: topic
quality: core
short_description: "El modelo de IA especialista planificado para el Nivel 3 del sistema de cuatro niveles SLM de PointSav, construido mediante entrenamiento continuo de OLMo 3 32B sobre el corpus federated de aprendizaje de Foundry."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: pointsav-llm.md
---

**PointSav-LLM** es el modelo de IA especialista planificado para el Nivel 3 del escalón SLM de cuatro niveles de PointSav. No es un producto activo en la fecha de este artículo. Se trata de una trayectoria planificada: el primer ciclo de entrenamiento continuo (CPT, por sus siglas en inglés) está actualmente previsto para v0.5.0 en el primer trimestre de 2027, con un despliegue productivo actualmente previsto para v1.0.0 en el cuarto trimestre de 2027.

*Todas las descripciones de capacidades, calendarios, estructuras de precios y objetivos de rendimiento de este artículo son de carácter prospectivo. Son planes o intenciones, no hechos operativos actuales. Los resultados reales dependen de la tasa de crecimiento del corpus, el rendimiento del modelo, la capacidad de ingeniería y las condiciones del mercado. [ni-51-102] [osc-sn-51-721]*

---

## Lo que es y lo que no es

PointSav-LLM está planificado como especialista en un dominio concreto, no como modelo de propósito general. Su corpus de entrenamiento previsto proviene del sustrato de aprendizaje de Foundry: los registros de trayectoria, los pares de decisiones editoriales y los historiales de commits alineados con el código que producen las sesiones de Task Claude contribuyentes en toda la plataforma.

Sus áreas de especialización previstas incluyen la operación del Archivo Totebox, las convenciones de PointSav, los patrones editoriales multiusuario, la generación de código alineada con las convenciones de Foundry y los flujos de contribución de entrenamiento federado.

PointSav-LLM no está planificado para competir con modelos de frontera de amplio alcance en conocimiento general, profundidad creativa o razonamiento multidisciplinar. Las consultas que requieran esa amplitud continuarán siendo enrutadas por el Doorman del cliente hacia las APIs externas del Nivel C (Nivel C externo). La base OLMo 3 (Apache 2.0; Open Data Commons) es abierta, y los adaptadores portátiles por cliente están planificados para preservar la soberanía del tenant conforme a la claim #28 de la Doctrina (Tenancy Diseñada para la Desvinculación).

---

## Cómo se prevé el acceso

El acceso de los clientes está previsto que se realice íntegramente a través del Doorman local de cada cliente. No se realizan llamadas directas al endpoint de PointSav-LLM desde el código de la aplicación del cliente.

La secuencia planificada es la siguiente: el Doorman recibe la consulta, clasifica su complejidad mediante el modelo local del Nivel A (OLMo 3 7B Q4), y enruta hacia el Nivel A para consultas sencillas o hacia el endpoint de PointSav-LLM para consultas que requieran profundidad especialista. La respuesta retorna a través del Doorman, se escribe una fila de auditoría tanto en el Doorman del cliente como en la pasarela de PointSav-LLM, y la facturación por token se computa en la pasarela. El código de la aplicación del cliente no cambia entre el enrutamiento local del Nivel A y el enrutamiento al Nivel C de PointSav-LLM.

---

## Diseño con intervención humana

Cuando la confianza del modelo cae por debajo de un umbral, la respuesta está planificada para incluir señales de confianza estructuradas: `confidence: low`, `escalate_to_human: true` y una etiqueta de motivo de escalado. El Doorman del cliente presenta entonces una opción de escalado al usuario, como "Consultar con un ingeniero de PointSav".

Los eventos de escalado resueltos por ingenieros humanos están planificados para convertirse en pares de datos de entrenamiento DPO para el siguiente ciclo CPT, a través del sustrato de aprendizaje (claim #32 de la Doctrina). La distribución prevista es: aproximadamente el 80–90% de las consultas gestionadas de forma autónoma en el Nivel L1, las restantes con intervención humana en L2, y los casos límite no resueltos escalados al Nivel L3 de ingeniería. Todos los porcentajes son objetivos planificados, no datos operativos actuales.

---

## Fundamento de código abierto

La base técnica de PointSav-LLM es OLMo 3 32B Think, publicado por AllenAI bajo licencia Apache 2.0, con datos de entrenamiento base bajo Open Data Commons. Esta elección es estructural: una base completamente abierta permite el entrenamiento continuo propio (CPT), la auditoría independiente de los pesos y la portabilidad para el cliente. Los pesos base son abiertos; el valor comercial de PointSav reside en el CPT especialista sobre el corpus agregado de Foundry, la infraestructura de escalado con intervención humana, el sustrato de auditoría por tenant y el SLA.

---

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que hacen posible la trayectoria de CPT federado
- [[service-slm-yoyo-operational]] — el estado operativo actual de los Niveles A/B del que este artículo describe el Nivel 3
- [[apprenticeship-substrate]] — el bucle DPO que alimenta el corpus CPT
- [[contributor-model]] — el Modelo de Contribuidor de Tres Niveles alineado con los niveles de precios

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
