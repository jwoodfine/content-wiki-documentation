---
schema: foundry-doc-v1
title: "Pasarela de inferencia por niveles — enrutamiento de IA local-primero"
slug: soft-slm-tiered-gateway
category: substrate
type: topic
content_type: topic
quality: complete
index_group: small-language-model-stack
short_description: "Una pasarela de inferencia por niveles que enruta las solicitudes de IA primero al modelo local, escalando a nodos GPU remotos y APIs externas solo cuando el nivel local no puede responder — minimizando la latencia, el coste y la exposición de datos mientras se mantiene la capacidad completa bajo demanda."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-09
editor: pointsav-engineering
cites: []
references: []
paired_with: soft-slm-tiered-gateway.md
supersedes: slm-tiered-substrate.es.md
---

Una pasarela de inferencia por niveles enruta cada solicitud de IA a través de una
jerarquía de niveles de cómputo, seleccionando el nivel más económico y capaz para
cada solicitud. El trabajo rutinario se ejecuta en hardware propiedad de la
organización. La capacidad adicional en GPU arrendada gestiona el trabajo que supera
la capacidad local. Una API comercial externa proporciona el respaldo final. Cada nivel
se degrada de forma controlada hacia el nivel inferior; ningún nivel es un único punto
de fallo.

## Por qué importa el enfoque local-primero

Enrutar toda la inferencia a un servicio externo es operacionalmente simple, pero
conlleva costes estructurales. Cada solicitud cruza una frontera organizativa,
exponiendo el contenido de las solicitudes y respuestas a un proveedor tercero. El
coste es proporcional al uso sin amortización. La organización no tiene forma de
adaptar el modelo a su propio vocabulario, procesos o conocimiento acumulado.

Una pasarela local-primero elimina estos costes para la mayoría del trabajo. El modelo
local gestiona las solicitudes dentro de su capacidad. Los recursos externos gestionan
lo que no puede. Con el tiempo, el modelo local mejora a través del entrenamiento
derivado del uso, reduciendo el conjunto de solicitudes que requieren cómputo externo.

## Los tres niveles

### Nivel A — inferencia local

El Nivel A es un servidor de inferencia que se ejecuta en el hardware propio de la
organización. Siempre está en funcionamiento, produce respuestas en segundos y no tiene
coste por solicitud más allá del hardware amortizado. Es el destino predeterminado para
todas las solicitudes.

El modelo local está entrenado o ajustado específicamente para el dominio de la
organización. Es más pequeño y rápido que los modelos de niveles superiores. Responde
de forma competente la mayoría de las solicitudes rutinarias: resúmenes, clasificación,
extracción de entidades de tipos de documentos conocidos, generación de código en
patrones conocidos.

El Nivel A no maneja bien la salida estructurada restringida por gramática en modelos
de tamaño pequeño. Las solicitudes que requieren cumplimiento estricto de un esquema
JSON se enrutan al Nivel B.

### Nivel B — nodo GPU de expansión

El Nivel B son uno o más nodos de inferencia remotos que ejecutan un modelo más grande
y capaz en hardware GPU dedicado. Los nodos arrancan bajo demanda y se detienen cuando
están inactivos, por lo que el coste es proporcional al uso real y no a la
disponibilidad.

La pasarela mantiene un disyuntor por nodo y una máquina de estados del ciclo de vida
de la VM. Cuando llega una solicitud al Nivel B y el nodo objetivo está detenido, la
pasarela lo inicia automáticamente. El llamante recibe una respuesta 202 Accepted con
un punto de consulta mientras arranca el nodo.

Cuando el nodo está en funcionamiento, las solicitudes se despachan de inmediato.
Cuando el disyuntor se abre — tras fallos consecutivos de sondeo de salud — las
solicitudes caen al Nivel A o se ponen en cola hasta que el nodo se recupera.

Los nodos del Nivel B se organizan por etiqueta. Una etiqueta `batch` gestiona trabajo
en segundo plano: extracción de corpus, procesamiento de datos de entrenamiento y
mantenimiento programado. Una etiqueta `express` gestiona trabajo sensible al tiempo
que no puede esperar un arranque en frío.

### Nivel C — proveedor de inferencia externo

El Nivel C es una conexión opcional a una API de modelo de lenguaje comercial. Sirve
como respaldo final cuando tanto el Nivel A como el Nivel B no están disponibles, y
como ruta directa para tareas que la organización ha designado explícitamente como
externas.

El Nivel C nunca se utiliza como fuente de datos de entrenamiento. Requiere una clave
API explícita para activarse.

## Enrutamiento de solicitudes

Cada solicitud lleva una indicación de complejidad y, opcionalmente, una etiqueta de
nivel. La pasarela selecciona el nivel usando esta secuencia de decisión:

1. Si hay un [[spot-vm-lifecycle-kill-switch|interruptor de emergencia]] cerrado para el nivel solicitado, la solicitud
   se rechaza o cae al siguiente nivel.
2. Si hay una etiqueta de nivel explícita, la solicitud se enruta a ese nivel.
3. Si no hay etiqueta, se aplica la política de enrutamiento:
   - `balanced`: complejidad baja y media → Nivel A; alta → Nivel B.
   - `drain-batch`: todo el trabajo no-express va al nodo batch.
   - `drain-express`: todo el trabajo va al nodo express para vaciar el backlog.
   - `local-only`: todo el trabajo va al Nivel A independientemente de la complejidad.
4. Si el nivel seleccionado no está disponible, la solicitud cae al siguiente nivel a
   menos que se requiera afinidad de nivel (por ejemplo, la extracción estructurada
   requiere el Nivel B y no cae de vuelta al Nivel A).

La política de enrutamiento es configurable en tiempo de ejecución sin reiniciar la
pasarela:

```
POST /v1/flow/policy  { "policy": "balanced" }
```

## El interruptor de emergencia

Cada nivel tiene un interruptor de emergencia independiente. Cerrar un interruptor
detiene inmediatamente todo nuevo despacho a ese nivel. Las solicitudes en vuelo se
completan; ninguna nueva comienza. El trabajo en cola se acumula y se vacía cuando se
reabre el interruptor.

El interruptor de emergencia es el control de facturación del operador. Cerrar el
interruptor del nodo express detiene el arranque de la GPU L4; el coste cae a cero.
Cerrar el interruptor global detiene todo el gasto de los Niveles B y C mientras
permite que el Nivel A continúe funcionando.

El carril express — que evita la cola respaldada en archivos para trabajo sensible al
tiempo — sigue verificando el interruptor de emergencia. Nada evita el interruptor de
emergencia.

## La cola de prioridad

El trabajo en segundo plano — briefs de aprendizaje, extracción de corpus, generación
de corpus de entrenamiento — se procesa mediante una cola de prioridad respaldada en
archivos con tres niveles:

- **P0** se enruta exclusivamente al modelo local para clasificación ligera.
- **P1** se enruta al nodo GPU batch para trabajo de extracción que requiere salida
  estructurada.
- **P2** se enruta al nodo GPU batch para generación de corpus de entrenamiento y
  tareas similares de larga duración en segundo plano.

El proceso de vaciado de la cola procesa un elemento de cada nivel por ciclo, en orden
P0 → P1 → P2, y luego repite. Esto evita que un lote grande de trabajo P2 bloquee las
tareas de extracción P1 durante un período prolongado.

## La memoria organizativa

Antes de despachar cualquier solicitud a cualquier nivel, la pasarela consulta el [[ontological-datagraph|grafo de conocimiento
organizativo]] para obtener entidades relevantes. Las entidades coincidentes se inyectan
en el prompt del sistema como contexto estructurado. El modelo ve las relaciones,
decisiones y políticas conocidas de la organización sin necesidad de derivarlas de
nuevo mediante inferencia.

Esta inyección de contexto no es fatal: si el servicio de grafo no está disponible, la
solicitud continúa sin contexto. Un disyuntor en la ruta de consulta del grafo evita
que un servicio de grafo lento bloquee la inferencia.

## El servidor MCP

Un proceso complementario expone la memoria organizativa de la pasarela como
herramientas [[mcp-substrate-protocol|Protocolo de Contexto de Modelo]] — no un
segundo puerto de red en la propia pasarela, sino un programa separado que habla
MCP por entrada y salida estándar con quien lo invoque, y habla HTTP normal con la
pasarela como su propio cliente. Cualquier cliente de IA compatible con MCP puede
invocar este proceso usando su suscripción integrada, sin necesidad de una clave
API adicional. La capacidad de razonamiento del cliente se combina con el
[[ontological-datagraph|grafo de conocimiento organizativo]] de la pasarela para
producir respuestas fundamentadas en los datos reales de la organización.

Esta es la vía principal de uso interactivo para operadores que ya tienen una
suscripción a un cliente compatible con MCP. La pasarela gestiona la memoria; el
cliente gestiona el razonamiento.
