---
schema: foundry-doc-v1
title: "Álgebra de composición de adaptadores"
slug: adapter-composition
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
short_description: La metáfora del sistema operativo para la IA en PointSav — el Doorman como kernel, los adaptadores como procesos, service-content como sistema de archivos — y el álgebra que ensambla inteligencia por solicitud a partir de capas de adaptadores LoRA.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
editor: pointsav-engineering
cites:
 - lorax-predibase
 - s-lora-2024
paired_with: adapter-composition.md
---

El **Álgebra de Composición de Adaptadores** es el modelo diseñado para cómo se ensamblará la inteligencia de IA en tiempo de solicitud en un despliegue de PointSav. Su metáfora central se asigna con precisión a un sistema operativo: el Doorman ([[service-slm]]) es el kernel; los adaptadores LoRA son procesos; [[service-content]] es el sistema de archivos; el modelo base es el firmware. El mecanismo de composición aún no está construido — hoy existe un solo adaptador, entrenado pero aún no promovido a producción — pero la forma que sigue es el objetivo comprometido del sustrato, no una hipótesis.

## El álgebra

En tiempo de solicitud, el [[compounding-doorman|Doorman]] está diseñado para componer adaptadores apilándolos sobre el modelo base:

```
pesos_compuestos =
 modelo_base[OLMo-3-7B-Instruct]
 ⊕ adaptador_constitucional[doctrina_vM.m.p]
 ⊕ adaptador_ingeniería[pointsav_vN]?
 ⊕ adaptador_inquilino[<inquilino>_vK]?
 ⊕ adaptador_rol[master | root | task]
 ⊕ adaptador_clúster[<nombre-clúster>_vJ]?
```

Donde `?` denota un adaptador opcional cargado solo cuando aplica el contexto de la solicitud. La composición está diseñada para ser determinista dado el contexto de la solicitud — sin decisión en tiempo de ejecución sobre qué adaptadores usar, solo lo que determina el contexto.

Componer pesos en tiempo de ejecución depende de una capacidad de llama.cpp que aún no ha llegado. Hasta entonces, el paso de fusión devuelve un ID compuesto simbólico en lugar de pesos fusionados — esto conecta el resto del sustrato de extremo a extremo sin bloquearse en la pieza faltante. Solo un adaptador está registrado hoy, evaluado pero aún no promovido más allá de esa etapa; la tipología de cinco familias a continuación es la forma objetivo que el registro está construido para contener, no su población actual.

## Tipología y reglas de enrutamiento de adaptadores

| Adaptador | Se carga cuando | Propiedad |
|---|---|---|
| `constitutional` | Siempre — en cada despliegue de la plataforma | Adaptador constitucional; se publica con el conocimiento común (Apache 2.0) |
| `engineering` | El alcance de la solicitud es "construir o modificar la plataforma" | Curado por el proveedor; ofrecido a los Clientes mediante contrato de servicio |
| `tenant` | El alcance de la solicitud opera sobre datos del inquilino | Dentro del Totebox del Cliente; por inquilino; nunca sale del almacenamiento del cliente |
| `role` | La solicitud se origina desde una sesión Master/Root/Task | Universal en todos los despliegues; aprendido de la doctrina y de trayectorias etiquetadas por rol |
| `cluster` | El alcance de la solicitud es un clúster de proyecto específico | Por clúster; declarado en el manifiesto del clúster |

El adaptador constitucional es universal y lo carga cada despliegue de la plataforma. El adaptador de inquilino es estrictamente por inquilino, se produce y se mantiene dentro del [[totebox-archive|Totebox]] del Cliente, y nunca sale del almacenamiento del cliente. El adaptador de ingeniería se publica con el [[knowledge-commons|conocimiento común]] (Apache 2.0) y no es propiedad intelectual privada del proveedor.

## Implementación

El álgebra se ejecuta sobre la infraestructura de servicio multi-LoRA de producción de 2026:

- **LoRAX (Predibase)** — servidor de inferencia multi-LoRA; miles de adaptadores por GPU; intercambio en caliente por solicitud; adaptadores privados por inquilino
- **S-LoRA** — aislamiento de adaptadores por cómputo dinámico; columna vertebral estática compartida vía IPC seguro; reducción significativa del tiempo hasta el primer token
- **vLLM Multi-LoRA** — intercambio en caliente en tiempo de solicitud sin recargar el modelo base

La contribución de PointSav es el patrón de composición — qué adaptadores se componen, en qué orden, bajo qué restricción doctrinal — no la [[yoyo-compute-substrate|capa de servicio]] en sí misma.

## Versionado de adaptadores

Cada adaptador lleva un nombre, una versión semver, la versión de doctrina contra la que fue entrenado, un campo de procedencia que nombra los fragmentos de corpus de los que fue destilado, y una firma del trainer que lo produjo. Una solicitud compuesta debe reconciliar las versiones de los adaptadores. La política por defecto carga adaptadores cuya `doctrine_version` coincide con la `doctrine_version` actual del despliegue. Un desajuste de versión se manifiesta como una señal operativa — el MANIFEST del despliegue registra la versión de doctrina activa y la discrepancia se vuelve visible.

Esto resuelve la deriva de IA a nivel del [[compounding-substrate|sustrato]]: el modelo está verificablemente alineado con una versión de doctrina específica, y cualquier desajuste es observable de primera clase, no una degradación silenciosa.

## La metáfora del SO de la IA

| Concepto del SO | Concepto de IA | Artefacto de la plataforma |
|---|---|---|
| Firmware | Modelo base preentrenado | OLMo 3 7B / 32B GGUF |
| Kernel | Enrutador de solicitudes | Doorman (`service-slm`) |
| Proceso | Unidad de comportamiento componible | Adaptador LoRA |
| Sistema de archivos | Conocimiento estructurado | `service-content` (grafo LadybugDB) |
| Llamada al sistema | Invocación de herramienta | Interfaz del servidor MCP |
| Memoria virtual | Aislamiento por inquilino | Particiones codificadas por `moduleId` |
| Módulo del kernel | Capacidad con alcance de clúster | Adaptador de clúster |
| Perfil de usuario | Límite de rol | Adaptador de rol |
| Constitución / carta | Licencia de SO + principios | Adaptador constitucional |
| Gestor de paquetes | Biblioteca de adaptadores + firma | `data/adapters/` + manifiestos firmados |

Los clientes instalan y desinstalan adaptadores como paquetes. Las firmas de los adaptadores se verifican antes de la composición. El aislamiento por inquilino se aplica en la capa de servicio de la misma manera que el aislamiento de memoria virtual se aplica en la capa del kernel.

Esto enmarca el [[compounding-substrate|sustrato]] para pequeñas y medianas empresas como **el sistema operativo de la IA** — inteligencia componible con una arquitectura plana en lugar de un único producto cerrado. Los adaptadores entrenados en el corpus del cliente son propiedad del cliente. La doctrina es el alma; el corpus es la mente; los adaptadores son la personalidad.

## Techo de composición práctico

La investigación de producción de multi-LoRA demuestra que componer 2–3 adaptadores por solicitud funciona limpiamente. Componer 5 o más adaptadores cruza hacia la interferencia de múltiples tareas. El álgebra se mantiene en un máximo de tres adaptadores en tiempo de ejecución por solicitud por diseño. Los parámetros de registro, voz de marca y tipo de documento viven en el andamiaje de instrucciones (la [[language-protocol-substrate|capa de plantilla de género]]), no como adaptadores adicionales.

## El nivel de LLM del Proveedor

Cuando el corpus de ingeniería del Proveedor acumule escala suficiente — planificado para el Año 2 o después, a partir de la versión 0.5.0 — el preentrenamiento continuado podría producir un modelo cuya capacidad cruce una inflexión de SLM a un modelo de mayor tamaño. Este modelo más grande podría ofrecerse como un nivel de [[compounding-doorman|Doorman]] en los despliegues de Cliente junto a las API externas de Nivel C, bajo contrato de servicio. Los Doormans de Cliente podrían entonces enrutar hacia el LLM del Proveedor para consultas que excedan la capacidad local del [[four-tier-slm-substrate|Nivel A]] y donde el Nivel C no sea deseable.

Se pretende que este nivel sea un subproducto del trabajo del [[trajectory-substrate|sustrato]] a medida que el corpus madura, no un producto desarrollado por separado.

## Véase también

- [[compounding-doorman]] — el Doorman que implementa el rol de kernel en este álgebra
- [[apprenticeship-substrate]] — el mecanismo que produce el corpus de adaptadores por inquilino
- [[language-protocol-substrate]] — la taxonomía de adaptadores de familia de lenguaje que extiende este álgebra para el trabajo editorial

## Referencias

1. LoRAX — servidor de inferencia multi-LoRA de Predibase, código abierto.
2. S-LoRA — servicio escalable de miles de adaptadores LoRA concurrentes, MLSys 2024.
