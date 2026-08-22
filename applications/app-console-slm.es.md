---
schema: foundry-doc-v1
title: "app-console-slm — consola de monitorización de infraestructura de inferencia"
slug: app-console-slm
category: applications
type: app
content_type: topic
quality: complete
index_group: input-and-developer-surfaces
short_description: "Cartucho de consola en terminal que muestra el estado en vivo de la infraestructura de inferencia — salud del modelo, la flota GPU de ráfaga, profundidad de cola y gasto diario — de solo lectura, sin controles propios."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
references: []
paired_with: app-console-slm.md
---

app-console-slm es un cartucho TUI para la consola del operador que muestra el
estado en vivo de la infraestructura de inferencia de IA: la salud del modelo
local, la flota de cómputo de ráfaga, el grafo de entidades, la profundidad de
cola y el gasto del día. Es un panel de solo lectura. Toda operación de escritura que muestra — política de
enrutamiento, [[spot-vm-lifecycle-kill-switch|el interruptor de emergencia]] — ocurre a través de una superficie de API
separada, no desde esta consola.

La consola se ejecuta en una ventana de terminal en el mismo nodo que la [[service-slm|pasarela de
inferencia]]. No requiere navegador, conexión de red a un servicio externo ni
autenticación más allá del acceso local al shell.

## Paneles de visualización

La consola organiza la información en cinco paneles que se actualizan automáticamente
cada diez segundos. El operador puede activar una actualización inmediata en cualquier
momento con la tecla R.

### Panel de pasarela

Muestra si el enrutador está en funcionamiento, la disponibilidad del modelo local y
su rendimiento en tokens por segundo, el estado del disyuntor del nivel de ráfaga, y
la clase de nodo que atiende las solicitudes actualmente.

### Panel de flota YoYo

Lista cada nodo de cómputo de ráfaga configurado por nombre junto con su estado de
ciclo de vida: uno de desconocido, detenido, en preparación, ejecutándose,
disponible, fallo al iniciar o zombie (en ejecución pero sin responder ya a las
sondas de salud). El panel destaca solo los nodos disponibles como saludables; los
detenidos, fallidos y zombie comparten un mismo estilo atenuado.

### Panel de DataGraph

Muestra el recuento total de entidades en el grafo de conocimiento y el estado del
disyuntor del nivel de ráfaga (el mismo disyuntor que muestra el panel de pasarela,
ya que ambos reflejan el mismo nivel).

### Panel de cola

Muestra la profundidad de la cola de extracción: cuántas tareas están pendientes,
cuántas en curso, cuántas pausadas, cuántas completadas, cuántas en cuarentena y —
resaltado cuando es distinto de cero — cuántas han agotado los reintentos y quedan
marcadas como poison, requiriendo revisión del operador.

### Panel de costes de hoy

Muestra el gasto total del día en curso, desglosado en la porción de cómputo de
ráfaga y la porción de horas de VM, junto con el recuento de solicitudes del día.

## Controles de teclado

| Tecla | Acción |
|---|---|
| R | Actualización inmediata — vuelve a consultar todos los endpoints de estado |
| ? | Ayuda — muestra todos los atajos de teclado |
| Esc | Cierra la ayuda |
| Q | Salir |

El cambio de política de enrutamiento y el interruptor de emergencia son mecanismos
reales, controlados por el operador. El interruptor detiene por completo, sin que
ninguna solicitud pueda evitarlo; la política de enrutamiento (balanced, drain-batch,
drain-express o local-only) es cambiable en tiempo de ejecución. Ambos residen tras
la API propia de la pasarela, no en esta consola — que solo muestra sus efectos.

## Características técnicas

La consola es un crate de biblioteca que implementa el rasgo Cartridge para el chasis
de la consola del operador. Se carga en el [[use-f-key-model|slot F9]]. La comunicación con la pasarela
de inferencia usa HTTP estándar contra los endpoints de monitorización de la pasarela.

La consola usa una tarea de sondeo en segundo plano que obtiene datos de estado cada
diez segundos y los envía a la tarea de renderizado por un canal. La tarea de
renderizado no bloquea en las solicitudes de red; muestra los datos más recientes que
haya recibido, por lo que la consola permanece receptiva incluso cuando la pasarela
responde con lentitud.

El modo de texto plano está disponible mediante la bandera `--plain` para entornos de
terminal sin soporte unicode. Los símbolos de estado unicode se reemplazan por
equivalentes ASCII.

## Relación con la pasarela de inferencia

La consola es un observador puro: no realiza ninguna llamada de escritura a la
pasarela de inferencia. Se despliega junto a la pasarela en el mismo nodo y no
requiere conectividad de red a servicios externos. Si la pasarela no está disponible,
la consola sigue ejecutándose y muestra cada panel como no disponible en lugar de
fallar.
