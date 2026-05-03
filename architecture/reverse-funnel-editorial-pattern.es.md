---
schema: foundry-doc-v1
title: "El Patrón Editorial de Embudo Invertido"
slug: reverse-funnel-editorial-pattern.es
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
lang: es
paired_with: reverse-funnel-editorial-pattern.md
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - olmo3-allenai
  - llguidance
  - knowledge-commons-wiki
---

El substrato invierte el ciclo editorial convencional. En la
mayoría de los flujos de publicación, el colaborador creativo
inicia el proceso — redacta el manuscrito, lo pasa a corrección,
lo envía al lector. En el substrato de Foundry, el Colaborador
Creativo entra al **final** del ciclo. Los clústeres de trabajo
generan borradores técnicos; la pasarela editorial los refina
hasta el registro de producción; la versión refinada se publica;
los Colaboradores Creativos editan el archivo publicado; y sus
ediciones alimentan el siguiente ciclo de entrenamiento como datos
de preferencia. Esta inversión es lo que permite que un equipo
creativo pequeño escale a un substrato del tamaño de Wikipedia.

## Definición

El Patrón Editorial de Embudo Invertido es una disciplina de
publicación en la que:

1. Múltiples clústeres de origen producen **borradores en bloque**
   — técnicamente precisos, con referencias libres, en registro
   informal.
2. Una única pasarela editorial (`service-language`, el clúster
   project-language) refina cada borrador al registro de
   producción: aplicación del vocabulario prohibido, postura de
   divulgación continua BCSC, generación de pares bilingües y
   resolución del registro de citas.
3. La versión refinada se publica de inmediato en el repositorio
   de destino.
4. Los Colaboradores Creativos entran al **final** — editan el
   archivo publicado. Sus ediciones constituyen la segunda parte
   de un par de preferencia.
5. El preentrenamiento continuo trimestral sobre el corpus de
   tuplas (borrador → refinado → edición creativa) produce una
   línea base del substrato que converge hacia (refinado ⊕
   Creativo) con el tiempo.

## Por qué los proveedores de infraestructura no pueden replicar esto

Tres razones estructurales.

Primero: el preentrenamiento continuo por inquilino está
estructuralmente ausente en los SaaS multiinquilino. Un modelo
compartido no puede personalizar su voz en función de las ediciones
de un único cliente. El bucle de compounding del Embudo Invertido
solo se cierra cuando el modelo de lenguaje cuenta con adaptadores
privados por inquilino y un corpus de entrenamiento igualmente
privado.

Segundo: los adaptadores de piso editorial por inquilino no
existen en los productos de los grandes proveedores. Las gramáticas
de vocabulario prohibido, las plantillas de postura BCSC y los
adaptadores de protocolo de lenguaje son específicos de cada
inquilino en Foundry. Los proveedores de infraestructura exponen
modos de salida estructurada genéricos, no "esta es la gramática
de su inquilino que se carga en tiempo de inferencia."

Tercero: el bucle cerrado exige soberanía sobre los datos de
entrenamiento `[constitutional-ai-2212-08073]`. Aunque un
proveedor de infraestructura capturara las ediciones creativas, los
datos resultantes alimentarían un modelo neutro para el proveedor.
El inquilino no puede poseer un modelo que aprenda su voz
particular.

## Lo que esto habilita en Foundry

El substrato cierra un bucle de preentrenamiento continuo sobre el
oficio editorial, no solo sobre la estructura. La etapa de
aprendizaje por aprendiz (Doctrina, afirmación #32) cierra el
bucle sobre la corrección estructural mediante pares DPO de
Etapa 1. El Patrón de Embudo Invertido cierra el bucle sobre el
**oficio editorial** mediante pares DPO de Etapa 2. Ambas etapas
alimentan el mismo corpus de preentrenamiento continuo de OLMo
`[olmo3-allenai]`.

Tras suficientes ciclos, el substrato produce borradores que
alcanzan el 80% → 90% → 95% del nivel creativo humano. La carga
sobre los Colaboradores Creativos disminuye de forma monótona; su
alcance se amplía hacia estrategia de marca, enmarcado
arquitectónico y formas de autoría que el substrato aún no puede
alcanzar.

## Implicaciones operativas

El perfil de contratación cambia. Dado que el borrador generado
por el substrato ya contiene contenido técnico preciso, los
colaboradores de nivel Pagado no necesitan formación técnica
profunda. El perfil se orienta hacia especialistas en narrativa,
editores de voz de marca y colaboradores de ilustración.

El control de calidad se simplifica. El piso del substrato es
verificable de forma mecánica; el trabajo creativo es principalmente
mejora. El control humano se enfoca en coherencia narrativa y
alineación de marca, no en precisión técnica.

La voz creativa por inquilino se destila en adaptadores por
inquilino. A medida que se acumulan pares de preferencia editados
creativamente en el espacio de nombres de un inquilino, el
adaptador aprende la voz de ese inquilino. Los borradores
posteriores en ese espacio de nombres llegan más cerca de la línea
base establecida por el cliente. Esto es la Álgebra de Composición
de Adaptadores (afirmación #22 de Doctrina) aplicada a la capa
editorial.

## Perspectivas — trabajo pendiente en el substrato

Conforme a las obligaciones de divulgación continua bajo
`[ni-51-102]` y `[osc-sn-51-721]`, la trayectoria que se describe
a continuación es `planificada` e `intencionada`. Los resultados
reales pueden diferir según la disponibilidad de modelos OLMo bajo
licencia Apache 2.0, el volumen de corpus editado creativamente y
la operación ininterrumpida de la pasarela editorial.

- Se prevé integrar `[llguidance]` en el Portero para que el Tier B
  de vLLM acepte gramáticas estructuradas. service-language es el
  consumidor principal planificado.
- Se prevé que los adaptadores de voz creativa por inquilino se
  destilen a partir de los pares DPO acumulados de Etapa 2 durante
  el primer año de operación.
- El ciclo de preentrenamiento continuo de OLMo apunta a una
  cadencia trimestral.
- La contratación del nivel Creativo está planificada para comenzar
  tras la publicación del primer lote de TOPICs refinados.

## Véase también

- [El Substrato de Compounding](topic-compounding-substrate.es.md)
- [El Substrato de Aprendizaje](topic-apprenticeship-substrate.es.md)
- [El Modelo de Contribuidor en Tres Niveles](topic-contributor-model.es.md)
- Convenciones del espacio de trabajo:
  `~/Foundry/conventions/reverse-funnel-editorial-pattern.md`
  `~/Foundry/conventions/cluster-wiki-draft-pipeline.md`
