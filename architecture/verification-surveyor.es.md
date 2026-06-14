---
schema: foundry-doc-v1
title: "Verificador de identidad"
slug: verification-surveyor
short_description: "El Verification Surveyor es el componente de bucle humano de service-people que presenta fragmentos de identidad extraídos a un operador para verificación manual antes de que se comprometan permanentemente en el libro mayor verificado."
category: architecture
type: topic
content_type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: verification-surveyor.md
cites: []
---


El Verificador de Identidad es el punto de control arquitectónico en [[service-people|`service-people`]] que impide que los errores de extracción automatizada se acumulen. Requiere que un operador humano confirme cada fragmento de identidad contra una fuente externa antes de que se comprometa permanentemente en el libro contable verificado.

## Filosofía del humano en el bucle

Los algoritmos de extracción sin supervisión acumulan errores. Un pipeline de ingestión totalmente automatizado que procese grandes volúmenes de correo electrónico inevitablemente producirá falsos positivos. El Verificador de Identidad es el cuello de botella arquitectónico deliberado que fuerza todos los fragmentos de identidad extraídos a través de un filtro cognitivo humano antes de que se escriban permanentemente en el libro contable verificado.

## Procedimiento de verificación

El Verificador presenta el fragmento — el texto extraído, el tipo de entidad inferido, el contexto de origen — al operador. El operador busca al individuo usando su propio navegador personal y su propia cuenta personal en un directorio externo, confirma la entidad, y pega la URL verificada de vuelta en el terminal. La plataforma nunca inicia la búsqueda externa por sí misma.

Este diseño es deliberado. Las búsquedas basadas en API contra directorios externos requerirían tokens foráneos persistentes, incurrirían en costos por consulta y expondrían la plataforma a riesgos de limitación de velocidad. El enfoque con separación de redes evita los tres problemas.

## Límite diario de verificaciones

El Verificador aplica un límite estricto de diez verificaciones por operador por día. El límite no es una restricción de capacidad; es una disciplina de calidad de datos. Los datos verificados a una tasa controlada mantienen una fidelidad a largo plazo que los datos verificados en masa no pueden igualar.

## Véase también

- [[ontological-governance]]
- [[message-courier]]
- [[sovereign-telemetry]]
- [[moonshot-initiatives]]
