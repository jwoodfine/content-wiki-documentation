---
schema: foundry-doc-v1
title: "El Álgebra de Composición de Adaptadores"
slug: adapter-composition.es
category: architecture
type: topic
quality: published
short_description: La metáfora del sistema operativo para la IA en PointSav — el Doorman como kernel, los adaptadores como procesos, service-content como sistema de archivos — y el álgebra que ensambla inteligencia por solicitud a partir de capas de adaptadores LoRA.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - lorax-predibase
  - s-lora-2024
paired_with: adapter-composition.md
---

El **Álgebra de Composición de Adaptadores** es el modelo que rige cómo se ensambla la inteligencia de IA en tiempo de solicitud en un despliegue de PointSav. Su metáfora central se asigna con precisión a un sistema operativo: el Doorman (`service-slm`) es el kernel; los adaptadores LoRA son procesos; `service-content` es el sistema de archivos; el modelo base es el firmware. La analogía no es ilustrativa — es operativa.

## El álgebra

En tiempo de solicitud, el Doorman compone adaptadores apilándolos sobre el modelo base:

```
pesos_compuestos =
    modelo_base[OLMo-3-1125-7B-Q4]
    ⊕ adaptador_constitucional[doctrina_vM.m.p]
    ⊕ adaptador_ingeniería[pointsav_vN]?
    ⊕ adaptador_inquilino[<inquilino>_vK]?
    ⊕ adaptador_rol[master | root | task]
    ⊕ adaptador_clúster[<nombre-clúster>_vJ]?
```

Donde `?` denota un adaptador opcional cargado solo cuando aplica el contexto de la solicitud. La composición es determinista dado el contexto de la solicitud; no hay una decisión en tiempo de ejecución sobre qué adaptadores usar.

## Tipología de adaptadores

El adaptador constitucional es universal y lo carga cada despliegue de Foundry. El adaptador de inquilino es estrictamente por inquilino, se produce y se mantiene dentro del Totebox del Cliente, y nunca sale del almacenamiento del cliente. El adaptador de ingeniería se publica con el conocimiento común (Apache 2.0) y no es propiedad intelectual privada del proveedor.

## La metáfora del SO de la IA

| Concepto del SO | Concepto de IA | Artefacto de Foundry |
|---|---|---|
| Firmware | Modelo base preentrenado | OLMo 3 7B / 32B GGUF |
| Kernel | Enrutador de solicitudes | Doorman (`service-slm`) |
| Proceso | Unidad de comportamiento componible | Adaptador LoRA |
| Sistema de archivos | Conocimiento estructurado | `service-content` (grafo LadybugDB) |
| Llamada al sistema | Invocación de herramienta | Interfaz del servidor MCP |
| Memoria virtual | Aislamiento por inquilino | Particiones codificadas por `moduleId` |
| Módulo del kernel | Capacidad con alcance de clúster | Adaptador de clúster |
| Perfil de usuario | Límite de rol | Adaptador de rol |

Esto enmarca el sustrato para pequeñas y medianas empresas como **el sistema operativo de la IA** — inteligencia componible con una arquitectura plana en lugar de un único producto cerrado. Los adaptadores entrenados en el corpus del cliente son propiedad del cliente. La doctrina es el alma; el corpus es la mente; los adaptadores son la personalidad.

## Techo de composición práctico

La investigación de producción de multi-LoRA demuestra que componer 2–3 adaptadores por solicitud funciona limpiamente. Componer 5 o más adaptadores cruza hacia la interferencia de múltiples tareas. El álgebra se mantiene en un máximo de tres adaptadores en tiempo de ejecución por solicitud por diseño.

## Véase también

- [[compounding-doorman]] — el Doorman que implementa el rol de kernel en este álgebra
- [[apprenticeship-substrate]] — el mecanismo que produce el corpus de adaptadores por inquilino
- [[language-protocol-substrate]] — la taxonomía de adaptadores de familia de lenguaje que extiende este álgebra para el trabajo editorial

## Referencias

1. LoRAX — servidor de inferencia multi-LoRA de Predibase, código abierto.
2. S-LoRA — servicio escalable de miles de adaptadores LoRA concurrentes, MLSys 2024.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
