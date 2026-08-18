---
schema: foundry-doc-v1
content_type: topic
index_group: compute-tiers
title: "Inferencia sin contenedores"
slug: zero-container-inference
short_description: "Patrón de implementación GPU de Nivel B con binarios Linux nativos bajo systemd sobre una GPU L4 (no la A100 que afirmaba texto anterior), con la detección de inactividad ejecutándose desde el proceso del servidor Doorman, no un temporizador en la propia VM de GPU."
category: ai
status: stub
bcsc_class: forward-looking
last_edited: 2026-08-17
editor: pointsav-engineering
language: es
paired_with: zero-container-inference.md
cites:
 - osc-sn-51-721

---

La inferencia sin contenedores es el patrón de despliegue para el [[yoyo-compute-substrate|cómputo GPU de Nivel B]] de la plataforma: binarios Linux nativos bajo systemd en instancias de máquina virtual de GCE, sin entorno de ejecución de contenedores ni orquestador. Esto está confirmado en la construcción real de Packer/OpenTofu (`service-slm/compute/`), que despliega unidades `.service` de systemd y ninguna herramienta Docker u OCI en todo el pipeline.

La economía funciona porque la detección de inactividad garantiza que la facturación de GPU se detiene cuando la inferencia no está en ejecución. Las afirmaciones específicas sobre la GPU y el precio en versiones anteriores de este artículo eran incorrectas, no solo imprecisas — corregidas más abajo en lugar de repetidas aquí, ya que ninguna cifra de coste se ha vuelto a calcular todavía contra la forma real de la instancia. El conjunto de inferencia de Nivel B que encarna este patrón tiene código de infraestructura real, desplegado; no es una construcción desde cero. Su estado de tráfico en producción no se confirmó de forma independiente aquí.

## Por qué sin contenedores

Las imágenes OCI implican un registro de contenedores: el registro se convierte en el artefacto duradero, y el operador debe mantener cadenas de construcción de imágenes, credenciales de registro y remediación de CVE para imágenes base. Para una VM de inferencia de uso puntual que arranca, opera un rato y se detiene, la capa de contenedores añade superficie operativa sin resolver ningún problema que el enfoque de máquina virtual no aborde más directamente.

## Qué se usa en su lugar

Un binario nativo en la familia de imágenes GCE `slm-yoyo` (`image_family = "slm-yoyo"` en la configuración real de Packer; `pointsav-public` es el id de proyecto GCP de ejemplo, no una familia de imágenes). Una unidad systemd con un `ExecStart` apuntando al binario — tanto `llama-server.service` como `vllm.service` se despliegan en la imagen, y el código base no concuerda consigo mismo sobre cuál es realmente el motor desplegado (véase Artefactos operativos, más abajo). OpenTofu para aprovisionamiento y gestión del ciclo de vida de la VM. Pesos del modelo en caché en GCS, confirmado en `vllm-weights-prep.sh`. nginx para terminación TLS, con el firewall restringido al puerto 9443. Controladores CUDA integrados en la imagen GCE en tiempo de construcción (`provision.sh` instala el toolkit CUDA 12 durante la construcción de Packer).

**No es Secret Manager para las claves de API** — no existe ningún uso de GCP Secret Manager en ninguna parte de `service-slm`. El mecanismo real es un token portador estático pasado a través de los metadatos de la instancia de GCE (`opentofu/variables.tf`).

## Economía SMB

La GPU es una `nvidia-l4` en una instancia `g2-standard-4`, confirmado en `opentofu/main.tf` — no una A100 de 80 GB como afirmaba texto anterior; las cifras específicas de coste por hora y por mes que se derivaban de la suposición de A100 son incorrectas junto con ella y no se reemplazan aquí con una nueva cifra hasta que se recalculen contra la forma real de la instancia. La instancia es interrumpible/spot, lo cual el texto anterior también acertó. La economía funciona porque la detección de inactividad es la primitiva que soporta el modelo: la instancia permanece activa solo mientras se ejecuta la inferencia, no por conveniencia del operador.

**Cómo funciona realmente la detección de inactividad — no es un temporizador en la propia VM de GPU.** Es una tarea en segundo plano dentro del proceso del servidor Doorman (`idle_monitor.rs`) que consulta el `/metrics` de la instancia cada 5 minutos y emite una llamada real `instances.delete` — eliminación, no una simple "parada" — una vez que la instancia ha estado inactiva más allá de `SLM_YOYO_IDLE_MINUTES` (30 por defecto). Una unidad systemd separada, verdaderamente local a la VM, `yoyo-deadman.service`, es un interruptor de hombre muerto real que apaga la instancia al alcanzar una vida máxima fijada en los metadatos — un mecanismo distinto, para un modo de fallo distinto (una instancia descontrolada o huérfana), no la ruta rutinaria de apagado por inactividad.

## El único inconveniente honesto: el arranque en frío

El texto anterior estimaba 60–120 segundos desde el estado detenido hasta listo para inferencia. Los propios presupuestos de arranque configurados en las unidades systemd sugieren que esto era optimista: `llama-server.service` fija `TimeoutStartSec=300`, `vllm.service` fija `TimeoutStartSec=600` — presupuestos reales de arranque en frío del orden de minutos, no menos de dos. Para cargas de trabajo sensibles a la latencia que requieren una respuesta rápida, el despliegue debería extender `SLM_YOYO_IDLE_MINUTES` para mantener la instancia caliente en lugar de asumir un arranque en frío de menos de dos minutos. Para cargas de trabajo en lote nocturnas — el caso de uso principal para el preentrenamiento continuo y la extracción de corpus a gran escala — el coste del arranque en frío es el precio del cero coste en reposo y es una compensación razonable independientemente de la cifra exacta.

## Artefactos operativos

La pila de despliegue para una instancia de inferencia de Nivel B tiene cuatro piezas reales. Un módulo de OpenTofu gestiona el ciclo de vida de la instancia. La imagen GCE incluye controladores CUDA, nginx, unidades systemd y — aquí es donde el código base se contradice a sí mismo — **ambos** servicios `llama-server` y `vllm`: `slm-doorman/src/tier/yoyo.rs` afirma que el servidor de Nivel B desplegado es llama.cpp, "NOT vLLM", mientras que `tier/local.rs` afirma por separado que el Nivel B es "vLLM ≥0.12". Esa contradicción no se resuelve aquí — se señala en lugar de elegir un lado en silencio. Un token portador en los metadatos de la instancia de GCE gestiona la autenticación (no Secret Manager, véase arriba). Cloud Logging apunta al propio proyecto GCP del cliente.

**No confirmado, a pesar de lo que afirmaba texto anterior**: un presupuesto de Cloud Billing con un interruptor de apagado vía Pub/Sub como defensa adicional contra gasto descontrolado. No existe código de Pub/Sub ni de presupuesto de Cloud Billing en `opentofu/` ni en `slm-doorman` — el único rastro es una mención no implementada de `monthly_cap_usd` en documentación de prosa. El operador nunca interactúa directamente con la instancia durante la inferencia; las unidades systemd y el monitor de inactividad del lado del Doorman gestionan el ciclo de vida de forma autónoma.

## Lo que se descarta

Plataformas de orquestación de contenedores gestionadas, entornos de ejecución de contenedores, marcos de abstracción multinube, registros de imágenes OCI y cadenas de construcción de contenedores en capas. No se excluyen por ser inferiores en general; se excluyen porque introducen superficie operativa incompatible con el compromiso estructural [[zero-container-runtime]] y el caso económico SMB descrito anteriormente.

## Véase también

- [[zero-container-runtime]] — el compromiso estructural que subyace a este patrón de despliegue
- [[doorman-protocol]] — la ruta de enrutamiento de Nivel B que distribuye al conjunto de inferencia
- [[substrate-without-inference-base-case]] — el sustrato funciona completamente sin Nivel B; la inferencia es aditiva

## Referencias

- [[zero-container-runtime]] — especificación del compromiso de despliegue sin contenedores.
- **Aviso de personal OSC 51-721** — Divulgación de información prospectiva. El conjunto de inferencia de Nivel B y los plazos de despliegue en este artículo son declaraciones prospectivas sujetas a cambios.
