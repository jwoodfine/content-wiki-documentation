---
schema: foundry-doc-v1
title: "Ciclo de Vida de VM Spot — Controlador Único e Interruptor de Emergencia"
slug: spot-vm-lifecycle-kill-switch
short_description: "Ciclo de vida de controlador único para la VM spot Yo-Yo — un solo temporizador posee arranque y parada, con interruptor centinela de archivo para control inmediato."
category: infrastructure
index_group: compute-and-vm-fabric
type: topic
content_type: topic
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-07-18
editor: pointsav-engineering
paired_with: spot-vm-lifecycle-kill-switch.md
---

Cuando un pipeline automatizado depende de una VM interrumpible o spot, el ciclo de vida
de esa VM debe estar controlado por un único responsable. Dos temporizadores independientes
que tienen autoridad para arrancar la VM terminarán disparándose al mismo tiempo,
dejando la VM en ejecución entre ciclos con el costo completo y sin ninguna ruta
automatizada para detenerla. Este documento describe la arquitectura de controlador único
utilizada para el [[yoyo-compute-substrate|nodo de lotes Yo-Yo]] y el interruptor de emergencia basado en archivo
centinela que proporciona control inmediato al operador.


## El problema de los dos temporizadores

El pipeline de lotes Yo-Yo tenía inicialmente dos temporizadores funcionando de forma
independiente:

- un **temporizador de ciclo diario**, que ejecutaba el [[yoyo-daily-enrichment-cycle|ciclo de enriquecimiento diario]] y tanto arrancaba como detenía la VM
- un **temporizador de umbral de corpus**, que comprobaba el corpus de entrenamiento en su propio calendario y arrancaba la VM si se superaba un umbral

Ambos temporizadores podían arrancar la VM. Solo el temporizador de ciclo diario la
detenía. Cuando el temporizador de umbral de corpus se disparaba por sí solo, podía
arrancar la VM pero no tenía ruta para detenerla. Si el ciclo diario no se disparaba
poco después, la VM permanecería en ejecución indefinidamente.

Un evento de arranque sin control del temporizador de umbral suponía una acumulación real
y no presupuestada de costo por cada hora que la VM se ejecutara más allá de su ventana
prevista — y si el propio ciclo diario se omitía (un día festivo, o un interruptor de
emergencia dejado activo), la VM podía ejecutarse durante un día completo o más antes de
que algo la detuviera.

## La solución de controlador único

La solución es arquitectónica: exactamente una unidad programada controla el ciclo de vida
completo de cada VM. Todas las operaciones del ciclo de vida de la VM — arrancar,
extracción de datos, comprobación de umbral del corpus, entrenamiento, detener — se
realizan ahora dentro de una única invocación de un script orquestador, disparado una vez
al día. Un disparador semanal independiente para el paso de entrenamiento todavía existe
como unidad instalable en el repositorio, pero su propia cadencia queda sustituida por la
propia fase de entrenamiento del orquestador, que ya se ejecuta cada noche — se lee como
documentación remanente del esquema que este diseño de controlador único reemplazó, no
como una segunda vía de arranque en producción.

El orquestador diario ejecuta dos fases obligatorias cada noche: una fase de extracción de
datos y luego una fase de entrenamiento ejecutada contra la comprobación de umbral del
corpus. Ambas se ejecutan mientras la VM ya está en marcha, sin ningún costo adicional de
arranque más allá del único arranque nocturno.

La regla se generaliza: para cualquier VM spot que realice múltiples tareas automatizadas,
consolidar todas las tareas en un único script orquestador invocado por un único temporizador.
No dar a múltiples temporizadores autoridad de arranque sobre la misma VM.

## El interruptor de emergencia con archivo centinela

Un interruptor de emergencia es un archivo cuya presencia o ausencia controla si se
ejecuta un proceso automatizado. El patrón es:

```
presencia de /ruta/al/archivo-bandera  →  suprimir la operación
ausencia de /ruta/al/archivo-bandera   →  operación normal
```

Para el nodo de lotes Yo-Yo, el interruptor de emergencia es un único archivo centinela
en una ruta fija que sobrevive a los reinicios.

El script del ciclo diario comprueba este archivo como su primera acción (Fase 0),
antes de emitir cualquier comando del ciclo de vida de la VM:

```bash
if [[ -e "$KILL_SWITCH" ]]; then
    log "INTERRUPTOR ACTIVO — $KILL_SWITCH presente; abortando ciclo de vida de VM"
    exit 0
fi
```

Crear el archivo es una acción de un solo comando que tiene efecto en el siguiente disparo
del temporizador:

```bash
touch "$KILL_SWITCH"
```

Eliminar el archivo reanuda el funcionamiento normal:

```bash
rm "$KILL_SWITCH"
```

El patrón es apropiado para cualquier proceso automatizado donde:
- El operador necesita un freno instantáneo que sobreviva a un reinicio
- La supresión debe persistir a través de múltiples disparos del temporizador hasta
  que se revierta explícitamente
- No se debe requerir ningún reinicio de servicio ni cambio de configuración para
  activar o desactivar el control

Una variable de entorno (`export SUPRIMIR=true`) no sobreviviría a un reinicio ni a
un reinicio del servicio. Enmascarar una unidad systemd requiere permisos de root y
un `daemon-reload`. El enfoque del archivo centinela es reversible, auditable (su
presencia o ausencia es visible con `ls`) y no requiere privilegios elevados para
activarlo.

## Defensa en profundidad: el monitor de inactividad

El interruptor de emergencia evita los arranques. Una capa de seguridad independiente
detiene una VM que está en ejecución cuando no debería estarlo. Esto no es un
temporizador independiente — es una tarea en segundo plano dentro del propio Doorman,
que sondea cada cinco minutos si la VM de lotes Yo-Yo ha estado en ejecución más de 30
minutos sin una solicitud de inferencia activa. Si se cumple esa condición, el monitor
elimina la instancia directamente (su disco de arranque sobrevive, ya que la eliminación
automática está deshabilitada en él — la VM se vuelve a crear, no se reanuda, en la
siguiente ejecución nocturna).

El monitor de inactividad es una medida de seguridad, no el controlador principal. Su
función es limitar la exposición al costo si el ciclo diario no completa su secuencia
de parada — por ejemplo, si el host de control pierde conectividad durante la ejecución,
o si el ciclo es interrumpido por una señal de proceso antes de que se emita el comando
de parada.

La combinación de ciclo diario de controlador único, interruptor de emergencia con
archivo centinela y monitor de inactividad proporciona tres capas independientes:

1. El ciclo diario detiene la VM como su fase final (ruta prevista)
2. El monitor de inactividad detiene la VM si el ciclo falla (primera medida de seguridad)
3. El interruptor de emergencia evita que la VM arranque si el operador necesita pausar
   toda la actividad (anulación del operador en la Fase 0)

## El guardia de comprobación de umbral

El script de umbral de corpus contiene una función de arranque de entrenador que
originalmente era llamada directamente por el temporizador de umbral del corpus. Tras
enmascarar ese temporizador, esta función fue modificada para comprobar el archivo del
interruptor de emergencia antes de emitir cualquier comando de arranque de VM. Esta es
una medida de defensa en profundidad: si la función alguna vez es llamada desde una ruta
de código que omite el ciclo diario, el interruptor de emergencia sigue teniendo efecto.

El patrón del guardia:

```python
if os.path.exists(KILL_SWITCH_PATH):
    print(f"[interruptor] {KILL_SWITCH_PATH} presente — arranque de VM suprimido")
    return
```

Cualquier script que tenga autoridad para arrancar una VM spot debe implementar esta
comprobación.

## Aplicación del patrón

Para aplicar controlador único + interruptor de emergencia a cualquier pipeline de VM spot:

1. Identificar todos los temporizadores y scripts que tienen autoridad para arrancar la VM.
2. Consolidar todo el trabajo en un único script orquestador. El script arranca la VM,
   realiza todas las tareas en secuencia y detiene la VM como paso final.
3. Deshabilitar todas las demás rutas de arranque (enmascarar los temporizadores;
   modificar cualquier script que tuviera autoridad de arranque para que compruebe
   el archivo del interruptor de emergencia en su lugar).
4. Crear la ruta del archivo del interruptor de emergencia en un directorio que
   sobreviva a los reinicios.
5. Añadir la comprobación del interruptor de emergencia como primera instrucción del
   script orquestador.
6. Añadir un monitor de inactividad como medida de seguridad de costo, apuntando al
   nombre y zona específicos de la VM.
