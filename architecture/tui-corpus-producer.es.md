---
schema: foundry-doc-v1
title: "La TUI como Productora de Corpus"
slug: tui-corpus-producer.es
category: architecture
type: topic
quality: published
short_description: "Cada interacción del operador con service-slm a través de la interfaz de terminal es una contribución curada al corpus de entrenamiento del adaptador por inquilino."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tui-corpus-producer.md
---

El patrón **TUI como Productora de Corpus** designa la interfaz de terminal del operador (`slm-cli`) como fuente primaria de datos de entrenamiento de alta calidad para el adaptador del modelo por inquilino. Cada interacción con el Portero a través de esta interfaz es una contribución curada al corpus. Este patrón codifica la reclamación doctrinal #45.

## Por qué las interacciones de terminal producen datos de alta calidad

Las interacciones de administración de sistemas e infraestructura tienen tres propiedades que las distinguen de los datos de entrenamiento generales:

**Verdad fundamental verificable.** Cuando un operador sigue el consejo de la IA — ejecutando un comando sugerido, aplicando un cambio de configuración propuesto — el sistema se recupera o no lo hace. No existe ninguna demora para saber si la respuesta fue correcta. Esta propiedad de retroalimentación inmediata es exclusiva de los dominios operacionales.

**Dominio acotado.** Las operaciones de archivo, las convenciones del sistema y el vocabulario de flujo de trabajo específico del cliente forman un conjunto acotado de comandos y modos de fallo. Los modelos se entrenan más eficientemente sobre dominios acotados que sobre corpus generales.

**Retroalimentación de expertos en el dominio.** El operador que emite un veredicto es la persona que sabe si la respuesta fue correcta, no un anotador distante del trabajo real. La literatura publicada sobre aprendizaje por refuerzo a partir de retroalimentación humana reporta consistentemente que las tuplas de interacción firmadas con veredicto entrenan un orden de magnitud más eficientemente que las tuplas sin veredicto.

## El mecanismo de /feedback

Después de cada respuesta del asistente en la TUI, el operador recibe tres opciones de veredicto explícito: Buena (la respuesta fue correcta — tupla marcada como ejemplo positivo de optimización de preferencia directa), Refinar (la respuesta era aproximada pero necesitaba ajuste — el operador proporciona una corrección inline) o Mala (la respuesta fue incorrecta — tupla marcada como ejemplo negativo). Si el operador descarta sin veredicto, la tupla contribuye al ajuste fino supervisado pero no a la optimización de preferencia directa.

## Propiedad del adaptador por inquilino

El corpus producido por los operadores de un cliente entrena el adaptador de ese cliente, no un adaptador general. Por la convención [[customer-owned-graph-ip]], los pesos del adaptador entrenado son propiedad del cliente. Foundry distribuye la arquitectura del modelo y el pipeline de entrenamiento; el cliente retiene el adaptador resultante.

## Disciplina de captura de veredicto

Ciertas sesiones de terminal no deben contribuir al corpus de entrenamiento: las sesiones de prueba iniciadas con una bandera de no-corpus, las sesiones interrumpidas por niveles no disponibles antes de completarse, y las sesiones en modo de depuración de nivel forzado se registran en el registro de auditoría pero se excluyen de los datos de entrenamiento normales.

## Véase También

- [[single-boundary-compute-discipline]] — la TUI nunca llama a los niveles de inferencia directamente
- [[customer-owned-graph-ip]] — los pesos del adaptador por inquilino son propiedad del cliente
- [[knowledge-graph-grounded-apprenticeship]] — las tuplas de entrenamiento llevan contexto de grafo cuando el Portero fundamenta la solicitud

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-tui-corpus-producer.md` (refinado el 30 de abril de 2026).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
