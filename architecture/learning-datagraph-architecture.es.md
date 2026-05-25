---
schema: foundry-doc-v1
title: "Grafo de aprendizaje — Cola de aprendizaje, pares DPO y captura de trayectorias"
slug: learning-datagraph-architecture
language: es
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: learning-datagraph-architecture.md
---

La plataforma construye un sustrato acumulativo: cada interacción del operador con una sesión de IA se convierte en una tupla de entrenamiento estructurada, enrutada a través de un único límite auditable (Doorman), capturada en un ledger de solo adición y reincorporada al SLM local mediante ajuste fino periódico. El resultado es un entorno de desarrollo que aprende de cómo se usa — las sugerencias de código se acercan a los patrones que escribe este operador, las propuestas de borrador se alinean más con la voz editorial de esta casa, las extracciones de entidades se afinan a medida que el grafo se enriquece.

El sustrato tiene cuatro patas.

**Captura de trayectorias.** Un hook de cierre de sesión se activa al final de cada sesión, escribiendo una entrada JSONL estructurada en el ledger de auditoría: estado de la rama, recuento de archivos sin confirmar, SHA de la cabeza y un indicador de promoción pendiente. Una cosecha nocturna de transcripciones copia las transcripciones del día en el mismo ledger, etiquetadas por operador y archivo.

**Cola de aprendizaje.** Un hook post-commit emite un brief para cada confirmación del espacio de trabajo. Un drenador de 15 minutos llama al SLM local (OLMo-2 7B Q4) contra cada brief, captura el intento del modelo y escribe la tupla `(brief, intento, diff_real)` en el corpus de aprendizaje. A 2026-05-18 se habían acumulado 502 tuplas.

**Pares DPO editoriales.** Cada borrador que pasa por el patrón editorial de embudo inverso — de crudo a refinado a editado creativamente — emite dos pares de preferencia directa (DPO, del inglés direct preference optimisation) en el corpus de edición de prosa. El par captura los deltas de mejora editorial. A esa fecha se habían acumulado 34 pares.

**Destilación de trayectorias negativas.** Un script de análisis de buzones lee las correcciones del operador de los mensajes archivados y emite señales de trayectoria negativa en el corpus de retroalimentación. Esta cuarta pata captura lo que el modelo no debe hacer.

Lo que queda por conectar — trabajo de ingeniería en Rust de varias semanas: el bucle de entidades estructuradas. [[service-content]] (grafo respaldado por LadybugDB) necesita un endpoint `POST /v1/draft/generate` que consulte el grafo para obtener entidades relevantes, ensamble un prompt fundamentado de 2K tokens, llame al Doorman y escriba la respuesta como tupla de corpus fundamentado en el grafo. Un planificador LoRA deberá activar el cómputo GPU de nivel B para el entrenamiento nocturno de adaptadores.

El sustrato se acumula en dos direcciones: estructuralmente (la densidad de citas y las cadenas de supersedencia se enriquecen con cada borrador) y generativamente (cada adaptador eleva el nivel del "crudo" para que cada ciclo de refinamiento comience más cerca de lo publicable).

## Véase también

- [[compounding-substrate]] — la disciplina de sustrato que esta arquitectura instancia
- [[service-slm]] — el servicio SLM local que ejecuta la inferencia del modelo en el bucle
- [[totebox-session]] — el modelo de sesión que la captura de trayectorias instrumenta al final de cada sesión
- [[mailbox-atomicity]] — la disciplina de escritura atómica que protege el ledger de auditoría de condiciones de carrera
