---
schema: foundry-doc-v1
content_type: topic
index_group: compute-tiers
title: "Inferencia sin contenedores"
slug: zero-container-inference
short_description: "Patrón de implementación GPU de Nivel B con binarios Linux nativos bajo systemd sobre una GPU L4, con la detección de inactividad ejecutándose desde el proceso del servidor Doorman en lugar de un temporizador en la propia VM de GPU."
category: ai
status: stub
bcsc_class: forward-looking
last_edited: 2026-08-24
editor: pointsav-engineering
language: es
paired_with: zero-container-inference.md
cites:
 - np-51-201

---

La inferencia sin contenedores es el patrón de despliegue para el [[yoyo-compute-substrate|cómputo GPU de Nivel B]] de la plataforma: binarios Linux nativos bajo systemd en instancias de máquina virtual de GCE, sin entorno de ejecución de contenedores ni orquestador.

La economía funciona porque la detección de inactividad garantiza que la facturación de GPU se detiene cuando la inferencia no está en ejecución. El conjunto de inferencia de Nivel B que encarna este patrón tiene código de infraestructura real, desplegado; no es una construcción desde cero.

## Por qué sin contenedores

Las imágenes OCI implican un registro de contenedores: el registro se convierte en el artefacto duradero, y el operador debe mantener cadenas de construcción de imágenes, credenciales de registro y remediación de CVE para imágenes base. Para una VM de inferencia de uso puntual que arranca, opera un rato y se detiene, la capa de contenedores añade superficie operativa sin resolver ningún problema que el enfoque de máquina virtual no aborde más directamente.

## Qué se usa en su lugar

Un binario nativo en la familia de imágenes GCE `slm-yoyo`. Una unidad systemd supervisa el binario; tanto un servicio llama.cpp como un servicio vLLM se despliegan en la imagen, y cuál de los dos atiende el tráfico real de Nivel B todavía no está resuelto (véase Artefactos operativos, más abajo). OpenTofu gestiona el aprovisionamiento y el ciclo de vida de la VM. Los pesos del modelo se guardan en caché en Cloud Storage, de modo que el arranque en frío los obtiene localmente en lugar de descargarlos del registro de origen en cada arranque. nginx gestiona la terminación TLS, con el firewall restringido al puerto 9443. Los controladores CUDA se integran en la imagen GCE en tiempo de construcción.

La autenticación no usa Secret Manager. El mecanismo es un token portador estático pasado a través de los metadatos de la instancia de GCE.

## Economía SMB

La GPU es una `nvidia-l4` en una instancia `g2-standard-4`, que se ejecuta como instancia interrumpible/spot. La economía funciona porque la detección de inactividad es la primitiva que soporta el modelo: la instancia permanece activa solo mientras se ejecuta la inferencia, no por conveniencia del operador.

**Cómo funciona la detección de inactividad.** Una tarea en segundo plano dentro del proceso del servidor Doorman consulta las métricas de salud de la instancia cada 5 minutos y elimina la instancia — una eliminación real, no una simple "parada" — una vez que ha estado inactiva más allá de `SLM_YOYO_IDLE_MINUTES` (30 por defecto). Una unidad systemd separada, local a la VM, es un interruptor de hombre muerto que apaga la instancia al alcanzar una vida máxima fijada en los metadatos — un mecanismo distinto, para un modo de fallo distinto (una instancia descontrolada o huérfana), no la ruta rutinaria de apagado por inactividad.

## Arranque en frío

Los presupuestos de arranque configurados en las unidades systemd son del orden de minutos, no menos de dos — el arranque en frío desde una instancia detenida hasta quedar lista para inferencia toma varios minutos, no segundos. Para cargas de trabajo sensibles a la latencia que requieren una respuesta rápida, el despliegue debería extender `SLM_YOYO_IDLE_MINUTES` para mantener la instancia caliente en lugar de asumir un arranque en frío rápido. Para cargas de trabajo en lote nocturnas — el caso de uso principal para el preentrenamiento continuo y la extracción de corpus a gran escala — el coste del arranque en frío es el precio del cero coste en reposo y es una compensación razonable.

## Artefactos operativos

La pila de despliegue para una instancia de inferencia de Nivel B tiene cuatro piezas. Un módulo de OpenTofu gestiona el ciclo de vida de la instancia. La imagen GCE incluye controladores CUDA, nginx, unidades systemd, y tanto un servicio llama.cpp como un servicio vLLM — cuál de los dos atiende el tráfico real todavía no está resuelto a nivel de plataforma. Un token portador en los metadatos de la instancia de GCE gestiona la autenticación. Cloud Logging apunta al propio proyecto GCP del cliente.

La defensa en profundidad contra gasto descontrolado — un presupuesto de Cloud Billing con un interruptor de apagado — todavía no está construida. El operador nunca interactúa directamente con la instancia durante la inferencia; las unidades systemd y el monitor de inactividad del lado del Doorman gestionan el ciclo de vida de forma autónoma.

## Lo que se descarta

Plataformas de orquestación de contenedores gestionadas, entornos de ejecución de contenedores, marcos de abstracción multinube, registros de imágenes OCI y cadenas de construcción de contenedores en capas. No se excluyen por ser inferiores en general; se excluyen porque introducen superficie operativa incompatible con el compromiso estructural [[zero-container-runtime]] y el caso económico SMB descrito anteriormente.

## Véase también

- [[zero-container-runtime]] — el compromiso estructural que subyace a este patrón de despliegue
- [[doorman-protocol]] — la ruta de enrutamiento de Nivel B que distribuye al conjunto de inferencia
- [[substrate-without-inference-base-case]] — el sustrato funciona completamente sin Nivel B; la inferencia es aditiva

## Referencias

- [[zero-container-runtime]] — especificación del compromiso de despliegue sin contenedores.
- **Política Nacional 51-201 de la CSA** — Divulgación de información prospectiva. El conjunto de inferencia de Nivel B y los plazos de despliegue en este artículo son declaraciones prospectivas sujetas a cambios.
