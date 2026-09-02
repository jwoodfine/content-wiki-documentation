---
schema: foundry-doc-v1
title: "Generar un registro de nóminas"
slug: generate-a-payroll-register
short_description: "Ejecuta el binario de nóminas para agregar las horas de mano de obra presupuestadas por división en un registro HTML y PDF — un informe estrecho que no calcula salario bruto, ni frecuencia de pago, ni remisión, y que imprime una raya en lugar de una cifra allí donde no la tiene."
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
paired_with: generate-a-payroll-register.md
---

## Requisitos previos

- Un conjunto de herramientas Rust funcional (véase [[install-toolchain]])
- Una copia del espacio de trabajo que contenga los crates de construcción — el crate de nóminas es miembro de él y lee dos ficheros de referencia del directorio del propio crate de construcción, por una ruta que se resuelve al compilar
- Un directorio de datos de construcción con `work_packages.csv`
- Permiso de escritura sobre el directorio de salida

Esta tarea no requiere ningún servicio en ejecución. Es una tarea por lotes en la línea de comandos, y la línea de comandos es toda la interfaz — no hay pantalla de consola, ni ranura de tecla de función, ni nada que pulsar.

Hay un requisito que no es configurable y que le sorprenderá: **el directorio de salida es una ruta absoluta fijada en el código, sin variable de entorno que la sustituya.** La ejecución lo crea y falla sin más si no puede. El directorio de datos de *entrada* sí es redirigible; el de salida no. Esa asimetría es la inversa de la de la herramienta contable hermana, y es una carencia real, no una postura de diseño.

## Propósito

Producir el Registro de Nóminas (por División) — una única hoja de trabajo con las horas de mano de obra presupuestadas y el tamaño de cuadrilla, una fila por división de construcción, en HTML y PDF.

Lea el párrafo siguiente antes de ejecutar nada, porque el nombre del informe promete bastante más de lo que el informe entrega.

**Este comando no calcula ninguna retribución.** No calcula salario bruto, ni neto, ni deducción alguna. No determina una frecuencia de pago, ni una fecha de pago, ni un calendario de remisión. No lee un parte de horas — las horas que agrega son horas *presupuestadas* procedentes de estimaciones de paquetes de trabajo, no horas que nadie haya trabajado. No tiene concepto de empleado: sus filas son divisiones, y el tamaño de cuadrilla junto a cada una es un supuesto de planificación, no una plantilla real. Las columnas tituladas *Pay Freq.* y *Gross Pay* existen en la página y todas sus celdas son una raya.

Es deliberado, y el documento lo dice en su propia cara. El cálculo de bruto a neto y el modelo de datos de la frecuencia de pago están ambos explícitamente sin diseñar en esta etapa, y el renderizador imprime una raya antes que una cifra inventada. Para lo que el registro sirve de verdad es para lo que dicen sus dos columnas pobladas: cuántas horas de mano de obra presupuestadas lleva cada división y qué tamaño de cuadrilla supone el plan para ella.

Para el diseño del que este informe es una primera porción, véase [[tool-payroll]]. Para la herramienta de la que proceden las horas, véase [[tool-construction]].

## Procedimiento

### 1. Indicar el directorio de datos de construcción

```bash
export TCO26_DATA_DIR=/data/construction/proyecto-ejemplo
```

Es la misma variable que usa el binario de informes de construcción, y se comporta igual: si no está definida, el binario recurre a una ruta absoluta fijada en el código, propia del despliegue para el que se compiló originalmente, y la ejecución falla en una lectura de fichero nombrando un directorio desconocido.

### 2. Comprobar las cuatro entradas

La ejecución lee cuatro ficheros CSV de tres lugares distintos. Dos llegan con la copia del repositorio, uno procede del directorio que acaba de exportar y otro vive en el directorio de datos del propio crate de nóminas.

| Fichero | De dónde procede | Qué se lee de él |
|---|---|---|
| `division_crosswalk.csv` | Datos de referencia versionados del crate de construcción | Prefijo de código de coste y nombre de división |
| `crew_assumptions.csv` | Datos de referencia versionados del crate de construcción | Nombre de división y tamaño de cuadrilla |
| `work_packages.csv` | `TCO26_DATA_DIR` | Código de coste y horas de mano de obra presupuestadas |
| `wage_payment_rules.csv` | Datos de referencia versionados del propio crate de nóminas | La fila de jurisdicción impresa en la nota |

`division_crosswalk.csv`:

```
uniformat_prefix,csi_division,division_name
```

`crew_assumptions.csv`:

```
csi_division,division_name,crew_size,hours_per_day
```

`wage_payment_rules.csv`:

```
jurisdiction_code,max_pay_period_days,max_days_to_pay_after_period_end,day_counting,remitting_authority,comp_authority,source_ref,effective_from
```

De `work_packages.csv` — un fichero más ancho, propiedad de la herramienta de construcción — esta ejecución lee exactamente dos campos: `cost_code` y `labor_hours_budget`. Todo lo demás de la fila se ignora.

Conviene conocer tres detalles antes de la primera ejecución:

- **`hours_per_day` se carga y nunca se usa.** El lector de supuestos de cuadrilla lo analiza en memoria; este informe consume solo `crew_size`. No es una columna que deba acertar para esta tarea.
- **Un código de coste se une a una división por el prefijo coincidente más largo.** Cada fila de la tabla de correspondencia declara un prefijo; el código de coste de un paquete de trabajo se compara con todos ellos y gana el más largo. Un código que no coincide con ningún prefijo no se une a nada — véase la tercera comprobación de verificación, donde eso importa más de lo que parece.
- **La jurisdicción está fijada en el código.** No hay opción, ni variable de entorno, ni columna en ningún sitio que seleccione qué fila de jurisdicción se lee. Un código de jurisdicción es una constante del binario, y solo esa fila se consulta.

### 3. Ejecutar el binario

Desde la raíz del espacio de trabajo:

```bash
cargo run -p tool-payroll-tco-26
```

Ese es el comando completo. No hay opciones, ni subcomandos, ni argumentos posicionales — el binario no analiza la línea de comandos en absoluto, de modo que no existe un `--help` que consultar, ni un `--jurisdiction` con el que sustituir la constante, ni forma de representar solo una parte del informe. Todo lo configurable que tiene es la única variable de entorno del paso 1.

### 4. Leer la línea de consola

Una ejecución correcta imprime exactamente una línea:

```
[payroll_register] 9 division(s), 4820 total budgeted hour(s) — written to <directorio de salida>
```

Los recuentos son inventados para esta guía; la forma es real. Conviene leer ambos números en lugar de saltárselos — son el único resumen que produce la ejecución, y el recuento de divisiones es lo primero que delata una tabla de correspondencia rota.

## Resultado esperado

Dos ficheros en el directorio de salida fijado en el código, que la ejecución crea si no existe:

| Fichero | Qué es |
|---|---|
| `payroll_register.html` | El registro como página web |
| `payroll_register.pdf` | El mismo registro como documento impreso |

El documento tiene tres partes: una cabecera con la etiqueta de proyecto propia del despliegue, el título del informe y el recuento de divisiones; una nota de *Bases de preparación*; y una tabla.

La tabla tiene cinco columnas — Division, Crew Size, Budgeted Hours, Pay Freq., Gross Pay — y repite su encabezado entre páginas. Dos de las cinco están pobladas. El registro se compone tipográficamente como documento de trabajo y no como estado presentado, que es la clasificación correcta para una hoja de cifras presupuestadas.

La nota de *Bases de preparación* declara en el propio documento que el tamaño de cuadrilla y las horas presupuestadas son reales y proceden de los datos de paquetes de trabajo de la herramienta de construcción, que la frecuencia de pago y el salario bruto no se muestran porque ninguno de los dos ha sido diseñado, y que nunca se ha registrado un parte de horas ni una transacción de nómina para el proyecto. Un segundo párrafo, presente solo cuando se encuentra la fila de jurisdicción, indica el tope de pago de salarios de esa jurisdicción en días, si esos días se cuentan como naturales o hábiles, qué autoridad administra la remisión, cuál administra la declaración de accidentes de trabajo, y la cita que respalda todo ello.

Ese segundo párrafo es un *enunciado de la norma*, no una aplicación de ella. Nada en esta ejecución calcula una fecha de pago, y nada la contrasta con el tope.

## Verificación

**Contraste el recuento de divisiones con la tabla de correspondencia.** El número de la línea de consola es cuántas divisiones distintas recibieron al menos un paquete de trabajo emparejado. Si es inferior al número de divisiones en las que espera ver trabajo, la correspondencia no está emparejando lo que usted cree.

**Contraste el total con la tabla.** El total de horas presupuestadas de la línea de consola es la suma de la columna Budgeted Hours. También debería coincidir con la cifra de horas-hombre que produce el informe de estado de construcción hermano a partir de los mismos datos de paquetes de trabajo — la unión y la agregación replican aquí deliberadamente la lógica de aquel informe, de modo que los dos nunca puedan discrepar en silencio sobre las mismas cifras subyacentes. Si difieren, uno de los dos se ha desviado, y ese es un hallazgo que merece perseguirse.

**Sume usted mismo `labor_hours_budget` y compare.** Esta comprobación no es opcional, y es la única forma de detectar el único fallo silencioso del informe. Una fila de paquete de trabajo cuyo código de coste no coincida con ningún prefijo, o cuyo `labor_hours_budget` esté vacío o no se analice como número, se descarta de la agregación sin advertencia, sin contador y sin mención alguna ni en la línea de consola ni en el documento representado. El registro parecerá completo. Sume la columna en su fichero de origen: si su total es mayor que el de la línea de consola, la diferencia son filas descartadas, no un error aritmético.

**Lea las rayas como dos hechos distintos.** Una raya bajo Pay Freq. o Gross Pay significa que la plataforma no calcula esa magnitud en absoluto. Una raya bajo Crew Size significa algo más concreto y más accionable: ninguna fila de `crew_assumptions.csv` tiene un nombre de división que coincida con esa división. El renderizador se niega a imprimir `0` ahí, precisamente para que un supuesto ausente no pueda confundirse con una cuadrilla de nadie.

**Confirme que el párrafo de jurisdicción está presente.** Si la nota de *Bases de preparación* termina tras su primer párrafo, la consulta de jurisdicción no encontró nada y el documento ha perdido en silencio toda su información regulatoria. Véanse los casos límite.

## Lo que esta tarea no hace

- **No calcula el salario bruto.** No se lee ninguna tarifa salarial de ningún sitio. La columna es estructural.
- **No calcula el salario neto ni deducción alguna.** El cálculo de bruto a neto — tramos fiscales, fórmulas de deducción obligatoria — está explícitamente fuera del alcance de esta versión y no está implementado a medias.
- **No determina una frecuencia de pago.** Ningún campo que lleve una frecuencia de pago por cuadrilla o por empleado tiene sitio en ningún esquema que esta ejecución lea, y por eso la columna es una raya y no un valor predeterminado.
- **No calcula ni hace cumplir una fecha de pago.** El tope de pago de salarios de la jurisdicción se imprime como texto en una nota. Nada deriva una fecha de pago, y nada la contrasta con ese tope.
- **No remite nada, ni calcula un calendario de remisión.** Las autoridades de remisión y de accidentes de trabajo se nombran en la nota como hechos sobre la jurisdicción. No se calcula ningún calendario.
- **No lee partes de horas.** Toda hora de este informe es una estimación presupuestada asociada a un paquete de trabajo. Ninguna hora realmente trabajada aparece en ningún sitio.
- **No es por empleado.** No hay registro de empleado, ni plantilla, ni nombre alguno en esta cadena en ningún momento. Las filas son divisiones.
- **No selecciona jurisdicción.** Un código de jurisdicción es una constante de compilación; hoy, un operador en otra jurisdicción necesita un cambio de código, no un cambio de configuración.
- **No escribe asientos en el libro mayor.** La ejecución lee cuatro ficheros y escribe dos.

## Casos límite

- **Cualquier fichero de entrada ausente** aborta la ejecución con `read <ruta>: <error>` y una salida distinta de cero. No se escribe nada. El mensaje es un pánico en bruto y no un error formateado — nombra la ruta, que es la parte que usted necesita.
- **Una fila corta en cualquiera de los dos ficheros de referencia** aborta la ejecución de la misma forma abrupta. Ambos lectores de referencia indexan posiciones de columna fijas, de modo que una fila con menos campos de los esperados es un fallo de índice, no una línea omitida.
- **Una coma dentro de un nombre de división romperá la correspondencia.** El lector de paquetes de trabajo maneja campos entrecomillados; los dos lectores de referencia dividen por comas simples y no lo hacen. Un nombre de división con coma desplaza en silencio todos los campos posteriores.
- **Un valor de `day_counting` no reconocido** en la tabla de jurisdicciones aborta la ejecución nombrando el valor infractor. Solo se admiten dos formas.
- **Que no exista fila para la jurisdicción fijada en el código no es un error.** La ejecución termina bien, los dos ficheros se escriben, y la nota de *Bases de preparación* simplemente omite su párrafo de jurisdicción. Es el fallo más peligroso de la herramienta, porque el documento parece terminado y ha eliminado en silencio toda su información regulatoria. Compruebe que el párrafo está, en lugar de darlo por supuesto.
- **Las divisiones se ordenan alfabéticamente por nombre**, no por número de división. Si espera un orden numérico, el informe no está mal — está ordenado por la otra clave.
- **Los ficheros de salida se sobrescriben en el sitio.** Sin versionado, sin directorio con marca de tiempo, sin confirmación y sin variable de entorno que los envíe a otro lugar. Copie lo que necesite conservar antes de volver a ejecutar.

## Reversión

No hay nada que deshacer en los datos de origen: la ejecución lee cuatro ficheros y nunca escribe en ellos. Sus únicas escrituras son `payroll_register.html` y `payroll_register.pdf`. Bórrelos, o vuelva a ejecutar para reemplazarlos.

## Pasos siguientes

- [[generate-a-construction-cost-estimate]] — el informe que produce los datos de paquetes de trabajo que este registro agrega
- [[generate-a-financial-statement-package]] — la tarea contable hermana sobre el mismo renderizador compartido
- [[install-toolchain]] — si `cargo run` todavía no está disponible en su máquina

## Véase también

- [[tool-payroll]] — el diseño de cadencia de pago, remisión y jurisdicción del que este registro es una primera porción, incluido todo lo que aún no calcula
- [[tool-construction]] — el libro mayor cuyos datos de paquetes de trabajo alimentan este informe en un solo sentido
- [[tool-accounting]] — el destino en el que están diseñados para aterrizar los importes de nómina calculados, una vez existan
- [[financial-and-construction-tools-overview]] — dónde encaja esta herramienta entre las herramientas financieras y de construcción
