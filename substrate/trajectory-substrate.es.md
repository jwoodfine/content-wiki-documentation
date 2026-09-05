---
schema: foundry-doc-v1
content_type: topic
title: "Sustrato de trayectoria"
slug: trajectory-substrate
short_description: "El mecanismo de plataforma que convierte trabajo operativo — commits, sesiones, retroalimentación de operador — en tuplas de capacitación JSONL estructuradas, enrutándolas en un corpus de preentrenamiento continuado que mejora el modelo base OLMo a lo largo del tiempo."
lang: es
paired_with: trajectory-substrate.md
category: substrate
index_group: core-named-substrates
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
 - constitutional-ai-2212-08073
 - federated-lora-2502-05087
 - s-lora-2024
 - lorax-predibase
 - olmo3-allenai
---

Cada confirmación de código que realiza la plataforma, cada sesión que
ejecuta un agente de trabajo, cada vez que un operador señala una
sugerencia incorrecta — todas estas interacciones se convierten en
señal de entrenamiento. El Sustrato de Trayectoria es el mecanismo
que convierte el trabajo operacional ordinario en tuples de
entrenamiento estructuradas, que se acumulan y mejoran el modelo
base de forma continua — el motor del [[compounding-substrate|sustrato compuesto]].

## Qué es

El Sustrato de Trayectoria captura automáticamente las interacciones
del sistema — ediciones de código, registros de sesión, correcciones
del operador — y las almacena como registros JSONL con metadatos de
procedencia completos. Estos registros alimentan corridas periódicas
de preentrenamiento continuo sobre el modelo OLMo 3 `[olmo3-allenai]`,
mejorando el substrato base sin interrumpir el trabajo en curso.

Tres propiedades lo distinguen de un proceso genérico de
ajuste fino:

- **Captura automática**: no se requiere decisión del operador; el
 trabajo genera señal por el simple hecho de existir.
- **Procedencia estructural**: cada registro incluye la versión de
 doctrina bajo la que fue producido, el inquilino al que pertenece,
 el rol de la sesión y su clase de redacción.
- **Fronteras de corpus impuestas por infraestructura**: los datos del
 proveedor nunca se mezclan con los del cliente; los datos de un
 inquilino no cruzan hacia otro. La separación es a nivel de
 directorio y de pipeline, no de política.

## Los tres corpus

El sustrato organiza los datos en tres corpus ortogonales, cada uno
produciendo una familia de adaptadores distinta:

**Corpus constitucional** — cláusulas doctrinales cruzadas con roles
y alcances. Produce el adaptador constitucional; se retrae con cada
versión menor de la Doctrina. Universal: se carga en cada despliegue
de la plataforma. La base conceptual es la IA constitucional
`[constitutional-ai-2212-08073]`.

**Corpus de ingeniería (lado proveedor)** — trayectorias de sesiones
de trabajo en repositorios del proveedor. Alcance: sólo PointSav.
Produce el adaptador de ingeniería, que puede ofrecerse a los clientes
como "personalidad del constructor de plataforma."

**Corpus de tiempo de ejecución del inquilino (por cliente)** — datos
que fluyen a través del Anillo 1 dentro de cada despliegue del cliente.
Vive dentro del Totebox del [[totebox-archive|cliente]]; nunca en el espacio de trabajo del
proveedor. Produce el [[adapter-composition|adaptador del inquilino]], que permanece en la
infraestructura del cliente.

Los adaptadores de los inquilinos no salen del despliegue del cliente
a menos que éste opte explícitamente por el [[sovereign-ai-commons|mercado federado]] (función
planificada; ver sección sobre perspectivas futuras).

## Mecanismo de captura

Un único script de captura está en funcionamiento hoy: `capture-edit.sh`
(`service-slm/scripts/`), instalado como un hook `git post-commit`. No escribe un
archivo JSONL directamente — publica el diff del commit (encabezado de estadísticas más
contexto unificado de 3 líneas, truncado a 64 KiB) y el mensaje del commit al endpoint
de shadow-brief del Doorman (`POST /v1/shadow`), donde se convierte en el campo
`actual_diff` del brief pendiente. No hace nada cuando no hay ningún brief pendiente
para ese repositorio. No lleva ningún paso propio de redacción o depuración de PII —
esto coincide con el hallazgo ya establecido de que la sanitización de salida en otras
partes de la plataforma cubre solo la vía de escritura del corpus de aprendizaje que
alimenta este script, no una capa de redacción general y separada.

Los otros cuatro puntos de captura que menciona este artículo — captura de trayectoria
al final de sesión, captura de doctrina en versiones MINOR, captura de retroalimentación
rechazada y captura de tiempo de ejecución del inquilino — describen puntos de captura
futuros previstos, no scripts que existan hoy en el monorepo bajo ningún nombre
encontrado mediante una búsqueda en todo el repositorio. Si sus nombres eventuales
coincidirán con lo escrito aquí no está confirmado contra ningún plan de implementación.

Cada registro JSONL que produce la vía de captura en vivo lleva un encabezado de
procedencia con campos que incluyen `tuple_type`, `doctrine_version`, `tenant`,
`moduleId`, `cluster`, `role`, `scope`, `source_commit`, `session_id` y `created`. Se
prevé que el pipeline de entrenamiento filtre sobre estos campos para ensamblar cada
corpus una vez que el propio pipeline esté construido; se prevé que cualquier versión
de adaptador sea re-derivable a partir de sus registros fuente.

La composición de adaptadores en tiempo de inferencia — a través del [[compounding-doorman|Portero]] — sigue el
álgebra de composición:

```
pesos_compuestos =
 modelo_base ⊕ constitucional ⊕ ingeniería? ⊕ inquilino? ⊕ rol ⊕ cluster?
```

La infraestructura de servicio multi-LoRA (`[s-lora-2024]`,
`[lorax-predibase]`) sirve miles de adaptadores concurrentes con
intercambio en caliente por solicitud.

## Perspectivas futuras

Per `[ni-51-102]`, las siguientes afirmaciones describen desarrollo
planificado e intencionado. Los resultados reales pueden diferir.

El Sustrato de Trayectoria opera actualmente en Nivel 1 (captura de
corpus de edición, activo desde v0.1.1). Los niveles siguientes son:

- **Nivel 2 — Captura de trayectoria de sesión**: previsto para la
 ventana de lanzamiento v0.2.x.
- **Nivel 3 — Prototipo de ajuste fino**: previsto para el objetivo
 v0.5.0; el servicio `router-trainer` produce el primer adaptador
 entrenado sobre el corpus acumulado.
- **Nivel 4 — Mercado federado**: largo plazo; depende de la madurez
 operacional del Nivel 3 y del avance de la investigación en LoRA
 federado `[federated-lora-2502-05087]`.

La cadencia de preentrenamiento trimestral es intencionada una vez
que el Nivel 3 esté operativo. El mecanismo está en su lugar; la
señal se está acumulando.

## Véase también

- [[compounding-substrate]]
- [[apprenticeship-substrate]]
- [[decode-time-constraints]]
- [[language-protocol-substrate]]
- [[citation-substrate]]
