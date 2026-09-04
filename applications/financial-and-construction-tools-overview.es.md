---
schema: foundry-doc-v1
title: "La familia de herramientas financieras y de construcción — un diseño compartido en tres productos"
slug: financial-and-construction-tools-overview
category: applications
type: tool
content_type: topic
quality: complete
index_group: financial-and-construction-tools
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: financial-and-construction-tools-overview.md
short_description: "Cómo se relacionan tool-accounting, tool-construction y tool-payroll como una sola familia de productos — un diseño compartido de partida doble, alimentaciones de datos unidireccionales entre ellos y un límite compartido de arquitectura gratuita/pagada."
cites: []
---

[[tool-accounting]], [[tool-construction]] y [[tool-payroll]] son tres productos separados que comparten un mismo linaje de diseño, no tres herramientas independientes que simplemente resultan estar cerca entre sí. Este artículo cubre lo que comparten y cómo se conectan; cada artículo de herramienta cubre su propio dominio en profundidad.

## Un diseño de partida doble, tres dominios

Las tres herramientas están construidas sobre, o diseñadas en torno a, la misma disciplina de libro contable de partida doble: cada asiento es una entrada balanceada, nada se almacena si puede derivarse de lo que ya está registrado, y se mantiene un historial completo e inalterable de cada entrada en lugar de sobrescribirla. `tool-accounting` aplica esta disciplina a los estados financieros. `tool-construction` aplica la misma disciplina a las cantidades físicas de construcción junto con los dólares, en un diseño de dos libros contables (un libro de producción para cantidades, un libro de costos para dólares) construido específicamente porque el seguimiento de costos de construcción necesita ambos a la vez. `tool-payroll` está diseñado para aplicar la misma disciplina subyacente al cálculo de pago bruto a neto y a la temporización de las remesas estatutarias.

**Por qué importa:** un diseño compartido significa que una corrección o mejora en la mecánica subyacente del libro contable está pensada para beneficiar a las tres herramientas, no solo a una, y un desarrollador o auditor que entiende el modelo contable de una herramienta ya entiende la forma de las otras dos.

## Cómo se mueven los datos entre ellas — solo alimentaciones unidireccionales

Las tres herramientas están diseñadas para conectarse mediante puentes de datos unidireccionales, nunca una tabla compartida y nunca un valor que se convierte de vuelta a su origen:

- **`tool-construction` → `tool-accounting`**: costo en dólares, que alimenta los estados financieros del propietario como obra en construcción en proceso.
- **`tool-construction` → `tool-payroll`**: horas y clase de mano de obra, que alimentan la nómina como tarjetas de tiempo. Este puente está diseñado para funcionar en un solo sentido — los dólares regresan únicamente como asientos ordinarios de nómina y cuentas por pagar hacia el libro de costos de construcción, a través de la misma ruta de revisión que cualquier otra transacción de origen, nunca como una conversión automática de horas mediante una tarifa. Esa brecha entre una estimación de horas por tarifa y los dólares reales de nómina es una característica de diseño deliberada, no una omisión: es la variación de tarifa de mano de obra, y cerrar el ciclo automáticamente destruiría precisamente la señal que existe para revelar.

**Por qué importa:** un propietario o auditor que evalúa estas herramientas en conjunto no necesita conciliar los números entre ellas manualmente — el diseño unidireccional significa que el propio libro contable de cada herramienta sigue siendo la fuente autorizada de su propio dominio, y cada otra herramienta lo recibe como una entrada fechada, nunca como un valor mutable compartido.

## Límite de arquitectura gratuita/pagada compartido

Las tres herramientas se apoyan en la misma arquitectura de plataforma subyacente: el sustrato de archivo y la terminal que las aloja son gratuitos (Apache-2.0); la agregación entre archivos — la única capacidad que un archivo aislado genuinamente no puede realizar por sí mismo — es el límite pagado en toda la plataforma. Cada una de las tres herramientas está diseñada como su propia superficie comercial adicional y separada sobre ese límite compartido, vendiendo la ingeniería de dominio en sí (el motor contable, la mecánica del libro contable de construcción, el motor de cálculo de nómina) en lugar de un margen sobre una infraestructura que ya es gratuita de operar.

## Licenciamiento

`tool-accounting`, `tool-construction` y `tool-payroll` están licenciados bajo
AGPL-3.0-or-later. Existe una licencia PointSav-Commercial independiente como alternativa
de pago para quien necesite distribuir una versión modificada, u ofrecerla como servicio
de red, sin la obligación de copyleft.

## Estado de construcción, lado a lado

| Herramienta | Estado real hoy |
|---|---|
| `tool-accounting` | La más avanzada: `tool-accounting-core` y `tool-typeset` son reales, están construidos y verificados de extremo a extremo contra un año fiscal histórico real — asientos, libro mayor, balance de comprobación y estados financieros renderizados. El plegado de consolidación, los datos de diario de las entidades subsidiarias y el renderizado interino (trimestral) ya son reales; la consolidación sin propiedad total, la entrada o salida a mitad de año y los saldos de apertura siguen sin construirse. |
| `tool-construction` | Un CLI piloto real (`tool-construction-tco-26`) renderiza cuatro informes reales — una estimación de costos, un cronograma de ruta crítica, un listado de materiales y un informe mensual de estado — contra los datos reales de paquetes de trabajo de un sitio piloto registrado. El libro de costos en dólares, el reporte de costos reales y el modelo de plazos estatutarios en días laborables siguen sin construirse. |
| `tool-payroll` | Existe un informe real: un Registro de Nómina por división que agrega las horas laborales presupuestadas del piloto de construcción bajo una fila citada de reglas salariales de una sola jurisdicción (un alcance explícitamente piloto, no cobertura de plataforma). El cálculo bruto-a-neto, la frecuencia de pago y el cálculo de remesas siguen siendo solo diseño. |

**Por qué importa:** las tres herramientas se discuten frecuentemente juntas por su diseño
compartido, pero no están en la misma etapa de madurez — cada una tiene hoy al menos un
informe real en funcionamiento, pero ninguna ofrece cobertura completa de plataforma, y
nada en ninguna de las tres debe interpretarse como software listo para producción.

## Véase también

- [[tool-accounting]]
- [[tool-construction]]
- [[tool-payroll]]
