---
schema: foundry-doc-v1
title: "El sustrato compuesto"
slug: compounding-substrate.es
category: architecture
type: topic
quality: complete
short_description: "El sustrato compuesto es el patrón arquitectónico que PointSav construye y administra, combinando cinco propiedades estructurales para producir una plataforma donde cada interacción operativa genera señal de entrenamiento que se compone a través de todos los despliegues de inquilinos."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: compounding-substrate.md
---

> El sustrato compuesto es el patrón arquitectónico que PointSav construye y administra, combinando cinco propiedades estructurales para producir una plataforma donde cada interacción operativa genera señal de entrenamiento que se compone a través de todos los despliegues de inquilinos.

**El sustrato compuesto** es una arquitectura de sustrato de IA donde el código de la plataforma es abierto y bifurcable, la capa de datos determinista funciona independientemente de cualquier cómputo de IA, y la IA se agrega como una capa opcional que cualquier inquilino puede componer dentro o fuera. Cada interacción operativa genera una señal de entrenamiento que se compone a través de los despliegues del sustrato. Un curador — PointSav — periódicamente incorpora la señal acumulada en modelos base mejorados que regresan a todos los despliegues sin interrumpir la propiedad de los datos del cliente. El patrón aplica el modelo de fundación de código abierto (Apache Software Foundation) combinado con el modelo de distribución comercial (Red Hat) al sustrato de IA: el sustrato se convierte en bienes comunes abiertos y el valor migra hacia las operaciones, la integración y un mercado federado.

Este artículo describe el patrón, nombra las cinco propiedades y explica la inversión de la cadena de valor que hace que el modelo sea duradero.

## Definición

Un sustrato compuesto es una arquitectura de sustrato de IA donde:

1. El código del sustrato es abierto y bifurcable.
2. La capa de datos determinista funciona independientemente de cualquier cómputo de IA.
3. La IA se agrega como una **Capa de Inteligencia Opcional** que cualquier inquilino puede componer dentro o fuera.
4. Cada interacción operativa genera una señal de entrenamiento que se compone a través de los despliegues del sustrato.
5. Un curador (PointSav) periódicamente incorpora la señal acumulada en modelos base mejorados que regresan a todos los despliegues sin interrumpir la propiedad de los datos del cliente.

## Cinco propiedades estructurales

Cada propiedad es un reclamo estructural. Cada uno nombra una razón específica por la cual los hiperescaladores no pueden replicarlo sin desmantelar su propio modelo de negocio.

### Propiedad 1 — Propiedad del sustrato

Cada cliente posee su pila completa: datos, cómputo, adaptadores y composición de despliegue. El sustrato (código más modelo base) es abierto bajo una licencia permisiva. Los datos y los adaptadores son propiedad intelectual del cliente.

Brecha estructural del hiperescalador: su negocio es monetizar el sustrato como servicio alquilado. La propiedad del sustrato erosiona el bloqueo (lock-in), la base de su modelo de facturación.

### Propiedad 2 — Inteligencia opcional

Los anillos de datos y procesamiento determinista funcionan completamente sin el anillo de IA. Los clientes, miembros de la comunidad, compradores regulados y sitios aislados (air-gapped) pueden desplegar una plataforma de datos PointSav totalmente funcional con cero cómputo de IA. La IA es valor agregado, no lo básico.

Brecha estructural del hiperescalador: sus productos de IA acoplan estrechamente el cómputo de IA a los servicios de datos. Desacoplarlos elimina los ingresos por cómputo de IA de cualquier despliegue que opte por no participar.

### Propiedad 3 — Enrutamiento de cómputo multinivel

`service-slm` es el límite único de Doorman que enruta de manera transparente entre tres niveles de cómputo: OLMo 3 7B local en la máquina del cliente, ráfaga multi-nube (Cloud Run / RunPod / Modal / GPU del cliente) y API externa (Claude / Gemini / GPT). El cliente no elige el nivel; la forma de la solicitud y los topes presupuestarios lo hacen.

Brecha estructural del hiperescalador: cada nivel en su mundo es una relación de facturación separada; su ecosistema no abarca los modelos frontera de sus competidores. No pueden abstraer este enrutamiento.

### Propiedad 4 — Composición federada

Los clientes optan por un mercado federado de LoRA (agregación que preserva la privacidad según el linaje de investigación SDFLoRA / FedEx-LoRA / HeLoRA). Las mejoras de cada cliente elevan el sustrato. Los datos propios del cliente nunca salen; solo los pesos de los adaptadores y los bloques de caché KV (sin datos de origen) fluyen hacia la federación.

Brecha estructural del hiperescalador: la facturación por inquilino y la postura de cumplimiento hacen que el agrupamiento cruzado de inquilinos sea estructuralmente ilegal en su modelo. No pueden operar una verdadera federación.

### Propiedad 5 — Ruta de preentrenamiento continuo

El modelo base OLMo 3 fluye hacia una variante de preentrenamiento continuo de PointSav, lanzada como el sustrato para despliegues posteriores. Los bienes comunes curados de cada año alimentan el modelo base del año siguiente. Para 2030, se pretende que el modelo base entrenado por la federación sea competitivo con los modelos propietarios de frontera en los dominios de la federación.

Brecha estructural del hiperescalador: no pueden permitir que los datos de los clientes entrenen un modelo base que el cliente posea posteriormente. Eso destruye el bloqueo que justifica sus márgenes.

## La inversión de la cadena de valor

La cadena de valor de los hiperescaladores depende de que el cliente permanezca en el sustrato del proveedor. La cadena de valor del sustrato compuesto depende de que el cliente se componga *fuera* del sustrato del proveedor. Los dos modelos de negocio son matemáticamente opuestos; uno no puede adoptar el otro sin desmantelarse.

Esta es la asimetría que hace que el patrón sea duradero. Un hiperescalador que copiara la propiedad del sustrato erosionaría su propio bloqueo. Un hiperescalador que copiara la propiedad de inteligencia opcional perdería ingresos por cómputo de IA en cada despliegue que optara por no participar. Un hiperescalador que copiara la propiedad de composición federada violaría sus propios contratos de cumplimiento por inquilino.

## Qué es PointSav en este patrón

No es un proveedor. No es un portero. **Administrador.**

- Administrador del protocolo (gobierna la especificación de Doorman, ejecuta el proceso de la Convención Constitucional según la Doctrina §III).
- Administrador del modelo base (publica la variante de preentrenamiento continuo, contribuye a OLMo cuando es relevante).
- Administrador del mercado (opera el grupo federado de LoRA, toma un porcentaje de los LoRA con participación en los ingresos).
- Operador de registro (vende dispositivos más integración más soporte).
- Cliente de referencia (Foundry mismo más Woodfine — prueba de que el patrón funciona).

El sustrato es un bien común abierto; el valor migra hacia las operaciones, la integración y el mercado de bibliotecas LoRA.

## El bucle compuesto

Cada acción produce datos; cada dato produce conocimiento; cada conocimiento mejora las acciones futuras. El bucle se ejecuta continuamente, en cada despliegue de inquilino, federado a través de los bienes comunes.

```
operador + asistente hace el trabajo
    ↓ produce
commits de git + ediciones de archivos + registros de sesión + turnos de conversación
    ↓ ingerido por
service-fs[inquilino]   ← registro WORM
    ↓ analizado por
service-extraction[inquilino]   ← determinista
    ↓ escribe estructurado en
service-content[inquilino]   ← grafo de conocimiento
    ↓ indexado por
service-search[inquilino]   ← índice de texto completo
    ↓ consultado por (cuando la IA está activa)
service-slm   ← Doorman; enruta entre 3 niveles de cómputo
    ↓ entrena (periódicamente)
adaptadores LoRA   ← paquetes de habilidades por inquilino
    ↓ contribuye (con opción de participar, federado)
grupo federado de LoRA   ← beneficio común
    ↓ se incorpora a (anualmente)
preentrenamiento continuo del modelo base   ← curado por PointSav
    ↓ se envía en
actualización del dispositivo   ← cada cliente se beneficia
    ↓ usado por
operador + asistente en la siguiente sesión   ← el bucle se cierra, compuesto
```

## Prospectiva — la trayectoria hacia 2030

Según el lenguaje de divulgación continua de `[ni-51-102]` y la disciplina prospectiva de `[osc-sn-51-721]`, la trayectoria descrita a continuación es `planeada` e `intencionada`, no un futuro declarativo. La forma está establecida; la capacidad operativa madura con el tiempo.

Para 2030, el sustrato compuesto apunta a producir:

- Un modelo base competitivo con la frontera de los hiperescaladores en tareas reguladas de PyME.
- Una federación de más de cien clientes, cada uno poseyendo su pila completa, cada uno contribuyendo y beneficiándose de los bienes comunes.
- Una pila de protocolos versionada dos veces a través de la Convención Constitucional y validada en producción.
- Una posición de mercado donde las industrias PyME reguladas — pequeñas clínicas, firmas de abogados medianas, asesores financieros regionales, operadores de bienes raíces — se han estandarizado en este patrón porque su postura de cumplimiento lo requiere y el diseño del sustrato lo cumple.

El patrón no desplaza a los hiperescaladores en volumen; ellos conservan la larga cola no regulada de la IA en la nube. La trayectoria captura el mercado PyME regulado que los hiperescaladores no pueden alcanzar económicamente.

## Ver también

- [[apprenticeship-substrate]]
- [[3-layer-stack]]
- [[worm-ledger-architecture]]
- [[sovereign-ai-routing]]
- [[language-protocol-substrate]]

## Referencias

- `conventions/compounding-substrate.md` — especificación canónica
- `DOCTRINE.md §XIV` — contexto de la doctrina
- `conventions/three-ring-architecture.md` — columna vertebral arquitectónica
- `conventions/customer-first-ordering.md` — justificación del orden de despliegue


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
