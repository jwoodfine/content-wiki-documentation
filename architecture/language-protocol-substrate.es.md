---
title: "El sustrato del protocolo de lenguaje"
slug: language-protocol-substrate
category: architecture
last_edited: 2026-06-29
editor: pointsav-engineering
status: stable
references:
  - id: 1
    text: "Padmakumar, V. et al. Does Writing with Language Models Reduce Content Diversity? arXiv:2310.06992, 2023."
    url: "https://arxiv.org/abs/2310.06992"
---

El **sustrato del protocolo de lenguaje** es una capa de clasificación de metadatos que rige
cómo el contenido editorial se categoriza, enruta y procesa en el espacio de trabajo de
Foundry. Cada artefacto borrador lleva una declaración `language_protocol:` en su cabecera.
Esa declaración es la instrucción legible por máquina que determina qué pasarela procesa el
artefacto, qué reglas de vocabulario aplican y qué destino recibe el artículo terminado.

## Fundamentación arquitectónica

El sustrato se apoya en tres mecanismos interconectados:

**Esquema `foundry-draft-v1`** — el sobre de cabecera que lleva cada artefacto borrador. El
esquema requiere un campo `language_protocol:`, un campo `destination:` y un campo `route_to:`.
Estos tres campos son las instrucciones de enrutamiento legibles por máquina; el esquema
impone su presencia en el momento de la puesta en escena.

**Tabla de enrutamiento** — el archivo de clasificación a nivel del espacio de trabajo que
mapea los valores de `language_protocol:` a proyectos pasarela y destinos. Un borrador que
declara `language_protocol: TOPIC-*` se resuelve a la pasarela `project-editorial` y al
destino wiki de documentación.

**Convención de notificación de archivo** — el protocolo mediante el cual los mensajes de
bandeja de salida llevan la intención de enrutamiento del borrador. Un borrador puesto en
escena en `.agent/drafts-outbound/` genera un mensaje de bandeja de salida dirigido a la
sesión pasarela apropiada.

## Por qué la selección explícita del protocolo

La elección de diseño fundamental del sustrato es requerir que el llamador declare un protocolo
de lenguaje en cada solicitud editorial, en lugar de autodetectarlo a partir de la entrada. Un
estudio de la Universidad de Cornell de 2023 encontró que la autodetección del estilo de
escritura estrecha el espacio de voces que produce un modelo — el paso de detección homogeneiza
las salidas hacia la expectativa del modelo del género, en lugar del registro propio del
autor.[^1] La selección explícita evita esto: el operador declara el registro previsto en el
límite de la solicitud.

## Las cuatro familias de género

Se definen cuatro familias de género, cada una con su propia lista de vocabulario prohibido,
objetivos de ajuste de registro y reglas de análisis de la Etapa 1:

- **PROSE** — editorial general: artículos, documentación técnica, TOPICs de arquitectura.
  Apunta al registro de artículo Bloomberg; prohíbe el vocabulario de marketing de productos
  de IA y las frases de cobertura vagas.
- **COMMS** — comunicaciones externas: cartas a inversores, comunicados de prensa, declaraciones
  públicas. Restricciones adicionales de formalidad; la postura de divulgación continua aplica
  donde corresponda.
- **LEGAL** — contratos e instrumentos legales. Precisión primero; paráfrasis mínima; lista
  específica de sinónimos no permitidos para evitar la deriva de significado no intencionada.
- **TRANSLATE** — producción bilingüe: el paso `.es.md` para artículos TOPIC y GUIDE.
  La política de señalar-sin-reescribir aplica estrictamente; el traductor humano es la
  autoridad.

## Composición de la canalización de tres etapas

`service-proofreader` compone tres etapas en cada llamada `/v1/proofread`:

1. **Análisis de vocabulario prohibido** — basado en reglas; determinista; submilisegundo;
   solo señala, nunca reescribe
2. **Paso mecánico de LanguageTool 6.6** — ortografía, gramática y estilo; se ejecuta como
   compañero Docker; hallazgos serializados a JSON para la Etapa 3
3. **Paso generativo del Doorman** — reescritura completa de texto de ajuste de registro a
   través del Doorman (service-slm)

Véase [[editorial-pipeline-three-stages]] para la especificación completa de la canalización.

## El valor predeterminado de señalar sin reescribir

La respuesta `/v1/proofread` lleva un array estructurado `findings`; el llamador decide qué
aplicar. El sustrato nunca reescribe silenciosamente el texto del operador. Una acción de
aplicar-todo es opcional por solicitud, no predeterminada.

## El veredicto del operador cierra el ciclo de aprendizaje

Después de revisar la reescritura de la Etapa 3, el operador registra una de tres
disposiciones: `accepted`, `rejected` o `edited`. El veredicto alimenta el par de eventos del
corpus de aprendizaje — `draft-created` → `draft-refined` → `creative-edited`. El sustrato es
tanto la herramienta editorial como la capa de recopilación de datos para el entrenamiento
continuo del modelo; estas dos funciones son inseparables por diseño.

## Separación de inquilinos en el corpus

La salida del corpus se enruta por inquilino según la ruta: los registros de la cuenta de
proveedor se escriben en la raíz del corpus del nivel del espacio de trabajo; los registros de
las cuentas de clientes se escriben en el directorio de instancia de despliegue del inquilino
cliente. La mezcla de inquilinos es estructuralmente imposible porque el componente de ruta es
el límite.

## Lo que el sustrato no hace

- No detecta automáticamente el protocolo — el operador lo declara en el límite de la solicitud
- No reescribe silenciosamente — el operador elige qué hallazgos aplicar
- No incorpora claves de API de Nivel C en el binario del corrector — las claves viven con el
  Doorman
- No entrena con texto de inquilinos por defecto — el contrato de no-entrenamiento se impone
  en la capa de escritura del corpus

## Véase también

- [[editorial-pipeline-three-stages]] — la canalización de tres etapas en detalle completo
- [[customer-tier-catalog-pattern]] — cómo se provisionan las instancias de despliegue para
  ejecutar la canalización
