---
schema: foundry-doc-v1
title: "Ciclo diario de enriquecimiento Yo-Yo"
slug: yoyo-daily-enrichment-cycle
short_description: "La ventana nocturna de dos fases en GPU que reconstruye el DataGraph y, una vez habilitada por completo, entrena pesos de adaptador para el modelo de lenguaje local — actualmente ejecutándose solo en modo DataGraph."
category: services
index_group: ring-3-ai-gateway
type: topic
content_type: topic
quality: complete
status: stable
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: yoyo-daily-enrichment-cycle.md
---

El ciclo diario de enriquecimiento Yo-Yo es la ventana de lote nocturna en el
[[yoyo-compute-substrate|nodo GPU de ráfaga]] que reconstruye el
[[ontological-datagraph|DataGraph]] y, una vez habilitada por completo, entrena pesos de
adaptador actualizados para el modelo de lenguaje del espacio de trabajo. El ciclo se
ejecuta en un horario fijo y siempre libera la GPU al final, complete o no ambas fases.

## Dos fases, no ocho

El ciclo es un solo script que ejecuta dos fases secuenciales, cada una
con su propio presupuesto de tiempo configurable, por defecto de dos horas — aproximadamente
cuatro horas en total, no una ventana de cuarenta y cinco minutos. Las dos fases no pueden
superponerse: necesitan acceso exclusivo a la misma GPU, y el script detiene el servidor de
inferencia antes de que comience la fase de entrenamiento.

**Fase 1 — Reconstrucción del DataGraph.** La VM de lote arranca, espera a que su servidor de
inferencia esté saludable, y luego procesa los documentos acumulados del día a través del
Doorman, escribiendo las entidades extraídas directamente en el DataGraph. Detalle completo:
[[service-slm-graph-store-migration]].

**Fase 2 — Entrenamiento de adaptador.** Una verificación de umbral cuenta las tuplas de
entrenamiento acumuladas en dos depósitos de corpus. Una vez que un depósito cruza su piso de
pares limpios, se escribe un marcador de entrenamiento pendiente y, si está configurado, el
corpus correspondiente se sincroniza al almacenamiento en la nube. En la VM de lote, un
script de entrenamiento sondea ese marcador y ejecuta un ajuste fino eficiente en parámetros
(QLoRA) contra el modelo base cuando aparece uno.

## Estado actual: el entrenamiento aún no está activo

Al momento de escribir esto, la mitad de entrenamiento del ciclo se ejecuta en modo
solo-marcador: la verificación de umbral escribe y despacha el marcador, pero el propio
script de entrenamiento aún no está habilitado en la imagen en ejecución de la VM de lote —
una reconstrucción de imagen pendiente es el siguiente paso antes de que entre en vivo. Cada
ciclo nocturno hoy realiza un enriquecimiento real del DataGraph; ningún adaptador ha sido
producido aún por esta canalización ejecutándose de principio a fin en su propio horario.

## Costo y la detención garantizada

La VM se detiene incondicionalmente al final del ciclo sin importar hasta dónde llegaron las
fases, y un archivo de interruptor de apagado puede suprimir todo el ciclo de inmediato si se
establece. Un monitor de inactividad ofrece un respaldo: si el ciclo alguna vez falla en
detener la VM por sí mismo, el monitor la detiene tras un período sostenido de inactividad,
acotando el peor de los casos. Al largo real del ciclo de varias horas, el costo por ciclo es
significativamente mayor de lo que sugeriría una ventana mucho más corta; no se republica aquí
una cifra exacta actual, ya que necesitaría remedirse contra los presupuestos reales de la
Fase 1/Fase 2 y los precios actuales de la nube.

## Véase también

- [[service-slm-graph-store-migration]] — la reconstrucción del DataGraph que es la Fase 1 de este ciclo
- [[elastic-compute-lora-training-pipeline]] — la descripción más completa de la canalización de dos fases, incluida la configuración QLoRA real de la fase de entrenamiento
- [[service-slm]] — el servicio que orquesta la canalización
