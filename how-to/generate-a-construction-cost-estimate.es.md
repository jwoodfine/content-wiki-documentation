---
schema: foundry-doc-v1
title: "Generar un informe de estimación de costes de construcción"
slug: generate-a-construction-cost-estimate
short_description: "Ejecuta el binario de informes de construcción sobre un directorio de datos CSV para producir informes de costes y de cronograma en HTML y PDF, con registros de conciliación y validación — la única interfaz existente, ya que la herramienta no tiene pantalla de consola ni analiza argumento alguno de línea de comandos."
category: how-to
index_group: financial-construction-tools
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con las manos en el teclado); operadores del cliente"
last_edited: 2026-09-01
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: generate-a-construction-cost-estimate.md
---

## Requisitos previos

- Un conjunto de herramientas Rust funcional (véase [[install-toolchain]])
- Una copia del espacio de trabajo que contenga los crates de construcción
- Un directorio de datos con `cost_estimate.csv` y `schedule.csv` según los esquemas indicados más abajo
- Permiso de escritura sobre ese directorio — la ejecución crea un subdirectorio de salida dentro de él

Esta tarea no requiere ningún servicio en ejecución. Otros binarios del mismo crate sí dependen de servicios residentes en el archivo; este lee dos ficheros y escribe seis.

## Propósito

Producir los dos documentos iniciales de un proyecto de construcción — un informe de costes y un cronograma con diagrama de Gantt — en HTML y PDF, junto con dos registros verificables por máquina que indican si los datos de origen son internamente coherentes.

Es una tarea por lotes en la línea de comandos, y la línea de comandos es toda la interfaz. `tool-construction` no tiene pantalla de terminal, ni ranura de tecla de función, ni superficie gráfica de ningún tipo. No hay nada que pulsar ni vista que abrir; una guía que describiera una estaría describiendo algo que no existe.

Para el diseño del libro mayor sobre el que se apoyan estos informes, véase [[tool-construction]].

## Procedimiento

### 1. Indicar a la herramienta su directorio de datos

```bash
export TCO26_DATA_DIR=/data/construction/proyecto-ejemplo
```

Defina esta variable. Si no está definida, el binario recurre a una ruta absoluta fijada en el código, propia del despliegue para el que se compiló originalmente — una ruta que no existirá en su máquina, de modo que la ejecución falla en la primera lectura con un error que nombra un directorio desconocido. Ese valor de reserva es una comodidad para una sola máquina, no un valor predeterminado en el que convenga confiar.

### 2. Comprobar los dos ficheros de entrada

La herramienta lee exactamente dos ficheros de ese directorio, ambos CSV con fila de encabezado.

`cost_estimate.csv`:

```
category,component,quantity,unit,unit_cost,price,rate_per_sf,rate_per_sm,pct_of_total,tier,excluded_flag,source_doc,source_page
```

`schedule.csv`:

```
task_id,task_name,parent_id,indent_level,task_type,duration_days,start_date,finish_date,phase,source_doc,source_page
```

Dos campos se comportan de forma menos simple de lo que su nombre sugiere, y conviene revisar ambos antes de la primera ejecución:

- **`quantity`**, en la estimación de costes, es realmente cuatro cosas distintas según la fila: una cantidad medida con su unidad, una tasa aplicada sobre una base, la cadena literal `Excluded`, o vacío. El lector modela los cuatro casos. No es una columna numérica con algunos huecos.
- **`start_date`** y **`finish_date`** admiten el formato ISO `2026-06-13`, el estadounidense `6/13/2026` o `6/13/26`, una forma con prefijo de día de la semana como `Mon 6/13/26` (lo que exporta habitualmente una herramienta de planificación por defecto) y `Jun 13, 2026`. Cualquier otra cosa se interpreta como ausente. El analizador devuelve un valor vacío en lugar de adivinar — véase el paso de verificación, donde eso importa más de lo que parece.

### 3. Ejecutar el binario de informes

Desde la raíz del espacio de trabajo:

```bash
cargo run -p tool-construction-tco-26
```

Ese es el comando completo. No hay opciones, ni subcomandos, ni argumentos posicionales — el binario no analiza la línea de comandos en absoluto, de modo que no existe un `--help` que consultar, ni un `--output` con el que redirigir, ni forma de ejecutar solo la etapa de costes o solo la de cronograma. Una invocación ejecuta siempre ambas, primero la estimación de costes y después el cronograma. Todos los parámetros de la herramienta son variables de entorno.

### 4. Leer el resumen en consola

Una ejecución correcta imprime recuentos estructurales y rutas de fichero, y nada más:

```
[cost estimate] 0 variance(s) — see /data/construction/proyecto-ejemplo/outputs/2026/cost_estimate_reconciliation.log
Wrote /data/construction/proyecto-ejemplo/outputs/2026/cost_estimate.html
Wrote /data/construction/proyecto-ejemplo/outputs/2026/cost_estimate.pdf
[cost estimate] categories: 7, allowances: 4
[schedule] 0 defect(s) — see /data/construction/proyecto-ejemplo/outputs/2026/schedule_validation.log
Wrote /data/construction/proyecto-ejemplo/outputs/2026/schedule.html
Wrote /data/construction/proyecto-ejemplo/outputs/2026/schedule.pdf
[schedule] tasks: 118, phases: 8
```

La ausencia de importes y fechas es deliberada, no un descuido. Una compilación temprana imprimía totales de conciliación en el terminal; se cambió el comportamiento para que la salida estándar lleve solo recuentos y todo lo sustantivo acabe en un fichero. No añada una sentencia de impresión para "comprobar rápidamente una cifra" — escríbala en el directorio de salida.

## Resultado esperado

Seis ficheros en `<directorio-de-datos>/outputs/<año>/`, que la ejecución crea si no existe:

| Fichero | Qué es |
|---|---|
| `cost_estimate.html` / `.pdf` | El informe de costes — categorías, partidas, previsiones, exclusiones, totales |
| `schedule.html` / `.pdf` | El informe de cronograma, con diagrama de Gantt y páginas por fase |
| `cost_estimate_reconciliation.log` | Si cada total del origen cuadra con las líneas que lo componen |
| `schedule_validation.log` | Defectos estructurales hallados en el árbol de tareas y en sus fechas |

## Verificación

Tres comprobaciones, en este orden. La tercera no es opcional.

**Lea el registro de conciliación.** La herramienta vuelve a sumar los precios de las líneas no excluidas de cada categoría y compara el resultado con el total impreso de esa categoría; después hace lo mismo con el total base, el total de previsiones y el total general frente a base más previsiones. La tolerancia es de dos céntimos. Una lista de variaciones vacía significa que el documento de origen es internamente coherente. Una lista no vacía es un hallazgo real sobre los datos de entrada, no un fallo de la herramienta — cada entrada nombra el ámbito, la cifra calculada, la cifra impresa y la diferencia.

**Lea el registro de validación.** La comprobación del cronograma informa de una tarea cuyo padre declarado no existe, de una tarea cuyo nivel de sangría no concuerda con la profundidad de su padre y de una tarea que termina antes de empezar, además de cualquier defecto registrado al analizar el fichero.

**Abra el PDF y mírelo.** Los dos defectos reales que ha producido esta vía de informes fueron invisibles para los registros y evidentes en la página. Una columna demasiado estrecha truncaba identificadores en puntos suspensivos mientras todos los recuentos y comprobaciones informaban de éxito. Por separado, un formato de fecha que el analizador aún no aceptaba produjo columnas de inicio y fin vacías y una línea temporal en blanco — y como la comprobación de intervalo invertido solo se ejecuta cuando *ambas* fechas se analizan correctamente, ese fallo se comunicó como **cero defectos**. Un registro limpio junto a una columna de fechas vacía es la firma de ese fallo, no la prueba de un cronograma correcto.

## Lo que esta tarea no hace

- **No estima.** El informe de costes representa y verifica las cifras que el CSV ya declara. No construye una estimación ascendente a partir de paquetes de trabajo, cantidades y tarifas de mano de obra. Esa vía existe — son los binarios `calibrate`, `solve_rate` y `post_ledger` del mismo crate — pero depende de que los servicios de materiales, cronograma y notificación residentes en el archivo estén accesibles, y es una tarea distinta de esta.
- **No informa del valor ganado.** La cantidad instalada, observada de forma independiente, es la entrada de la que depende toda cifra de valor ganado y de rendimiento de coste, y hoy no existe ninguna fuente para ella en este modelo de datos. Los informes que la consumirían están previstos; este comando no produce ninguno.
- **Todavía no es multiproyecto.** El crate de informes es específico de un despliegue y su nombre lleva un sufijo propio de ese despliegue. Hoy, un segundo despliegue significa un segundo crate binario y no un argumento de proyecto — que es la razón honesta por la que el paso 3 no tiene una opción `--project` que documentar.
- **No escribe asientos en el libro mayor.** Este comando lee dos ficheros y representa documentos. Registrar asientos es tarea de `post_ledger`.

## Casos límite

- **Un `cost_estimate.csv` ausente o ilegible** imprime `Failed to load <ruta>: <error>` en la salida de error y termina con estado 1. No se escribe nada.
- **Un `schedule.csv` ausente** falla igual — pero solo después de que el informe de costes ya se haya escrito. Medio conjunto de salidas es el resultado esperado de ese fallo, no una corrupción. Corrija la entrada y vuelva a ejecutar; los ficheros se sobrescriben.
- **Una fila con menos campos que el encabezado** no se omite con una advertencia. Ambos lectores indexan posiciones de columna fijas, de modo que una fila corta aborta la ejecución. Repare el CSV en lugar de sortearlo.
- **Los ficheros de salida se sobrescriben en el sitio.** No hay versionado, ni directorio con marca de tiempo, ni confirmación. Copie lo que necesite conservar antes de volver a ejecutar.
- **Una fecha que el analizador no sabe leer se deja vacía en lugar de forzarse.** Es el comportamiento correcto y también la forma en que puede representarse una línea temporal entera vacía sin un solo error — de ahí la comprobación visual anterior.

## Reversión

No hay nada que deshacer en los datos de origen: la ejecución lee `cost_estimate.csv` y `schedule.csv` y nunca escribe en ellos. Sus únicas escrituras son los seis ficheros bajo `outputs/<año>/`. Bórrelos, o vuelva a ejecutar para reemplazarlos.

## Pasos siguientes

- [[export-structured-data]] — llevar la salida representada o sus registros de origen a otro lugar
- [[install-toolchain]] — si `cargo run` todavía no está disponible en su máquina

## Véase también

- [[tool-construction]] — el diseño del libro mayor, el modelo de códigos de coste y el enfoque de valor ganado que representan estos informes
- [[tool-accounting]] — el motor contable hermano, diseñado para recibir el coste de este libro mayor
- [[financial-and-construction-tools-overview]] — dónde encaja esta herramienta entre las herramientas financieras y de construcción
