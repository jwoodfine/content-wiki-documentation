---
schema: foundry-doc-v1
title: "Ciclo de Vida de VM Spot — Controlador Único e Interruptor de Emergencia"
slug: spot-vm-lifecycle-kill-switch
short_description: "Ciclo de vida de controlador único para la VM spot Yo-Yo — un solo temporizador posee arranque y parada, con interruptor centinela de archivo para control inmediato."
category: infrastructure
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

**Corrección (2026-07-18):** varios nombres específicos de este artículo no coinciden con
la fuente real de `service-slm`, aunque el mecanismo del interruptor de emergencia en sí
se verifica correctamente. Hechos verificados:

- **El script orquestador es `nightly-run.sh`** (`service-slm/scripts/nightly-run.sh`, con
  las banderas `--no-yoyo` y `--test-mode`), disparado por un `nightly-run.timer` real
  (`OnCalendar=*-*-* 00:00:00 UTC`) — no `yoyo-daily-cycle.sh` / `local-yoyo-daily.timer`
  como los nombra este artículo. Un dato que corrobora la desactualización: un comentario
  de documentación en Rust en `slm-doorman-server/src/idle_monitor.rs` todavía dice "see
  `yoyo-daily-cycle.sh`" — ese nombre es real, solo que aparentemente fue reemplazado por
  una renombración a `nightly-run.sh` que ni este artículo del wiki ni ese comentario en
  Rust han seguido.
- **El interruptor de emergencia en sí es correcto tal como se describe** —
  `/srv/foundry/data/yoyo-disabled`, verificado por `corpus-threshold.py` antes de
  cualquier llamada a `gcloud instances start`, coincide estrechamente con la fuente real
  (el texto del mensaje difiere ligeramente pero el mecanismo es idéntico).
- **El monitor de inactividad no es un temporizador systemd.** Es una tarea tokio en
  segundo plano dentro del proceso de `slm-doorman-server` (`idle_monitor.rs`), no una
  unidad llamada `yoyo-idle-monitor.timer` que se dispara externamente cada 5 minutos. Su
  intervalo de sondeo (5 min) y su umbral de inactividad (30 min por defecto) sí coinciden
  con los números de este artículo. Otra diferencia de comportamiento: emite un
  `instances.delete` de GCP (no un `instances.stop`) — el disco de arranque sobrevive
  porque la eliminación automática está deshabilitada en él, coincidiendo con un patrón
  nocturno de eliminar+crear, no de detener/arrancar.
- **Discrepancia abierta, no resuelta silenciosamente en ningún sentido**: un archivo
  `training-trigger.timer` separado (`service-slm/docs/deploy/training-trigger.timer`,
  "Phase 3 corpus threshold check," domingo 02:00 UTC) todavía existe en el repositorio
  con instrucciones de instalación activas orientadas al operador ("`sudo systemctl
  enable --now training-trigger.timer`") — esto se lee como un temporizador actualmente
  recomendado, en tensión con la afirmación de este artículo de que el temporizador de
  umbral de corpus "fue enmascarado." Esto puede ser un documento obsoleto para una unidad
  ya deshabilitada, o puede significar que la corrección de controlador único descrita
  aquí no es (o ya no es) la realidad desplegada. Necesita confirmación de
  project-totebox antes de corregir la afirmación central de este artículo en cualquier
  sentido.

## El problema de los dos temporizadores

El pipeline de lotes Yo-Yo tenía inicialmente dos temporizadores funcionando de forma
independiente:

- `local-yoyo-daily.timer` — ejecutaba el [[yoyo-daily-enrichment-cycle|ciclo de enriquecimiento diario]], que arrancaba y detenía la VM
- `local-corpus-threshold.timer` — comprobaba el corpus de entrenamiento y arrancaba la VM si se superaba el umbral

Ambos temporizadores llamaban a `gcloud instances start`. Solo el temporizador del ciclo
diario llamaba a `gcloud instances stop`. Cuando se disparaba `local-corpus-threshold.timer`,
podía arrancar la VM pero no tenía ruta para detenerla. Si el temporizador del ciclo diario
no se disparaba poco después, la VM permanecería en ejecución indefinidamente.

Al costo del nodo Yo-Yo de aproximadamente $0.71 por hora, un evento de arranque sin
control del temporizador de umbral costaría aproximadamente $0.85 antes de que el
siguiente ciclo diario se disparara para detenerlo — asumiendo que el ciclo se disparara.
Si el ciclo se omitía por un día festivo o por tener el interruptor de emergencia activo,
la VM podría ejecutarse durante 24 horas o más con un costo de aproximadamente $17.

## La solución de controlador único

La solución es arquitectónica: exactamente una unidad systemd controla el ciclo de vida
completo de cada VM. `local-corpus-threshold.timer` fue enmascarado (redirigido a `/dev/null`),
eliminando su capacidad de arrancar la VM. Todas las operaciones del ciclo de vida de
la VM — arrancar, enriquecer, comprobar umbral, entrenar opcionalmente, detener, verificar —
se realizan ahora dentro de una única invocación de `yoyo-daily-cycle.sh` disparada por
`local-yoyo-daily.timer`.

La comprobación del umbral del corpus es ahora la Fase 5 dentro del ciclo diario en lugar
de un temporizador independiente. El activador del entrenamiento es la Fase 6. Ambos se
ejecutan mientras la VM ya está en marcha para el enriquecimiento, sin ningún costo
adicional de arranque de VM.

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

Para el nodo de lotes Yo-Yo, el archivo del interruptor de emergencia es
`/srv/foundry/data/yoyo-disabled`.

El script del ciclo diario comprueba este archivo como su primera acción (Fase 0),
antes de emitir cualquier comando `gcloud`:

```bash
if [[ -e "$KILL_SWITCH" ]]; then
    log "INTERRUPTOR ACTIVO — $KILL_SWITCH presente; abortando ciclo de vida de VM"
    exit 0
fi
```

Crear el archivo es una acción de un solo comando que tiene efecto en el siguiente disparo
del temporizador:

```bash
touch /srv/foundry/data/yoyo-disabled
```

Eliminar el archivo reanuda el funcionamiento normal:

```bash
rm /srv/foundry/data/yoyo-disabled
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
detiene una VM que está en ejecución cuando no debería estarlo. El temporizador del
monitor de inactividad (`yoyo-idle-monitor.timer`) se dispara cada cinco minutos y
comprueba si la VM de lotes Yo-Yo ha estado en ejecución más de 30 minutos sin una
solicitud de inferencia activa. Si se cumple esa condición, el monitor emite un comando
de parada.

El monitor de inactividad es una medida de seguridad, no el controlador principal. Su
función es limitar la exposición al costo si el ciclo diario no completa su secuencia
de parada — por ejemplo, si la VM de trabajo pierde conectividad durante la Fase 8, o
si el ciclo es interrumpido por una señal de proceso antes de que se emita el comando
de parada.

La combinación de ciclo diario de controlador único, interruptor de emergencia con
archivo centinela y monitor de inactividad proporciona tres capas independientes:

1. El ciclo diario detiene la VM como su fase final (ruta prevista)
2. El monitor de inactividad detiene la VM si el ciclo falla (primera medida de seguridad)
3. El interruptor de emergencia evita que la VM arranque si el operador necesita pausar
   toda la actividad (anulación del operador en la Fase 0)

## El guardia en corpus-threshold.py

`corpus-threshold.py` contiene una función `_start_trainer_vm()` que originalmente era
llamada por el temporizador de umbral del corpus. Tras enmascarar el temporizador, esta
función fue modificada para comprobar el archivo del interruptor de emergencia antes
de emitir cualquier comando `gcloud instances start`. Esta es una medida de defensa en
profundidad: si la función alguna vez es llamada desde una ruta de código que omite el
ciclo diario, el interruptor de emergencia sigue teniendo efecto.

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

1. Identificar todos los temporizadores y scripts que llaman a `gcloud instances start`
   para la VM.
2. Consolidar todo el trabajo en un único script orquestador. El script arranca la VM,
   realiza todas las tareas en secuencia y detiene la VM como paso final.
3. Deshabilitar todas las demás rutas de arranque (enmascarar los temporizadores;
   modificar cualquier script que tuviera autoridad de arranque para que compruebe
   el archivo del interruptor de emergencia en su lugar).
4. Crear la ruta del archivo del interruptor de emergencia en un directorio que
   sobreviva a los reinicios (p. ej. `/srv/foundry/data/` o `/var/lib/`).
5. Añadir la comprobación del interruptor de emergencia como primera instrucción del
   script orquestador.
6. Añadir un monitor de inactividad como medida de seguridad de costo, apuntando al
   nombre y zona específicos de la VM.
