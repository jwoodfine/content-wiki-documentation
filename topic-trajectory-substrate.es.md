---
schema: foundry-doc-v1
title: "El Sustrato de Trayectoria"
slug: topic-trajectory-substrate
lang: es
paired_with: topic-trajectory-substrate.md
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - federated-lora-2502-05087
  - s-lora-2024
  - lorax-predibase
  - olmo3-allenai
---

Cada confirmación de código que realiza Foundry, cada sesión que
ejecuta un agente de trabajo, cada vez que un operador señala una
sugerencia incorrecta — todas estas interacciones se convierten en
señal de entrenamiento. El Sustrato de Trayectoria es el mecanismo
que convierte el trabajo operacional ordinario en tuples de
entrenamiento estructuradas, que se acumulan y mejoran el modelo
base de forma continua.

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
de Foundry. La base conceptual es la IA constitucional
`[constitutional-ai-2212-08073]`.

**Corpus de ingeniería (lado proveedor)** — trayectorias de sesiones
de trabajo en repositorios del proveedor. Alcance: sólo PointSav.
Produce el adaptador de ingeniería, que puede ofrecerse a los clientes
como "personalidad del constructor de plataforma."

**Corpus de tiempo de ejecución del inquilino (por cliente)** — datos
que fluyen a través del Anillo 1 dentro de cada despliegue del cliente.
Vive dentro del Totebox del cliente; nunca en el espacio de trabajo del
proveedor. Produce el adaptador del inquilino, que permanece en la
infraestructura del cliente.

Los adaptadores de los inquilinos no salen del despliegue del cliente
a menos que éste opte explícitamente por el mercado federado (función
planificada; ver sección sobre perspectivas futuras).

## Mecanismo de captura

Cinco scripts automatizan la captura: hooks de post-confirmación de
Git, scripts de fin de sesión, y rutinas de retroalimentación del
operador. Todos aplican disciplina de sanitización antes de escribir:
claves privadas, datos personales y detalles de identificación del
cliente se redactan en el script de captura, no en el consumidor
posterior.

La composición de adaptadores en tiempo de inferencia sigue el
álgebra de composición:

```
pesos_compuestos =
    modelo_base ⊕ constitucional ⊕ ingeniería? ⊕ inquilino? ⊕ rol ⊕ cluster?
```

La infraestructura de servicio multi-LoRA (`[s-lora-2024]`,
`[lorax-predibase]`) sirve miles de adaptadores concurrentes con
intercambio en caliente por solicitud.

## Por qué los grandes proveedores de nube no pueden replicarlo

Tres razones estructurales, cada una arraigada en incompatibilidad de
modelo de negocio:

**1. No pueden ofrecer fronteras de corpus por inquilino.** Los
productos de IA gestionada agrupan señales de entrenamiento de todos
los clientes. Esa agrupación es el fundamento de su escala. Aislar
el corpus por inquilino disuelve la señal agregada que justifica su
inversión.

**2. No pueden dejar los pesos del adaptador en el hardware del
cliente.** El modelo de negocio de un gran proveedor requiere que
el cómputo — y por tanto los pesos — permanezcan en su
infraestructura. Permitir que un inquilino produzca y retenga pesos
de adaptador elimina el alquiler de cómputo que es su línea de
ingresos.

**3. No pueden ofrecer una auditoría firmada y re-derivable.** Cada
adaptador de Foundry es una función determinista de sus registros
fuente. Un proveedor gestionado cuyo entrenamiento es opaco al cliente
no puede ofrecer trazabilidad equivalente sin exponer la naturaleza
agregada de su señal de entrenamiento.

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

- [El Sustrato de Composición](topic-compounding-substrate.es.md)
- [El Sustrato de Aprendizaje](topic-apprenticeship-substrate.es.md)
- [Restricciones en Tiempo de Decodificación](topic-decode-time-constraints.es.md)
- La convención que sustenta este artículo:
  `~/Foundry/conventions/trajectory-substrate.md`

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.