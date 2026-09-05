---
schema: foundry-doc-v1
title: "Ordenamiento cliente-primero"
slug: customer-first-ordering
category: patterns
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-infrastructure-patterns
short_description: El principio de que un proveedor de software que construye algo que un cliente instalará debe construirlo en el mismo orden que el cliente lo instalará, en el mismo sustrato que el cliente usará.
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: customer-first-ordering.md
---

Un proveedor de software que construye sus propias herramientas fuera de orden — publicando la API antes que el cliente, el manual operativo después del despliegue, la documentación de configuración meses después del primer usuario — entrega un producto que refleja la conveniencia de desarrollo del proveedor y no la realidad operativa del cliente. El ordenamiento cliente-primero es la disciplina que lo evita, haciendo que la secuencia de instalación del cliente sea la secuencia de construcción del proveedor, y ancla el [[compounding-substrate|sustrato compuesto]] en la realidad operativa verificada.

## El principio

Al construir algo que un cliente instalará, construirlo en el mismo orden que el cliente lo instalará, en el mismo sustrato que el cliente usará. El propio despliegue del proveedor de su producto es la primera instalación de ese producto. Si la instalación del proveedor funciona limpiamente en ese orden y en ese sustrato, el manual operativo del cliente es verdadero por construcción.

**Por qué importa:** un cliente que sigue un manual operativo nunca es la primera entidad en intentar esa secuencia exacta — el proveedor ya la ejecutó, en el mismo tipo de sustrato, antes de publicarla.

## Por qué importa el proveedor-como-primer-cliente

El espacio de trabajo en el que se desarrolla una plataforma de software se declara como una instancia de la entrada de catálogo que la plataforma distribuye. Esto es estructural, no una cuestión de estilo: el espacio de trabajo es la primera instancia numerada del despliegue que describe. Cada paquete que la plataforma distribuye se instala primero en este espacio de trabajo, en la misma secuencia numerada, usando los mismos scripts de arranque y despliegue que ejecutaría un cliente.

La consecuencia es que las brechas en la experiencia del cliente emergen durante el desarrollo del proveedor en lugar de aparecer el primer día del cliente. Si un script de arranque falla, un archivo de configuración no está documentado o falta una dependencia en un manual operativo, el proveedor lo descubre antes de publicar. El cliente recibe un manual operativo verificado contra una instalación real.

**Por qué importa:** un paso roto nunca llega al primer día del cliente, porque el propio espacio de trabajo del proveedor ya lo encontró y lo corrigió primero.

## Responsabilidad de tres capas

El principio se asigna a una estructura de responsabilidad de tres capas:

**Pasos de nivel operador** reflejan lo que hace el cliente en los límites de hardware — comprar equipo, configurar acceso de red, ejecutar flujos de autenticación contra proveedores de nube desde fuera del sistema en ejecución. Estos pasos no pueden automatizarse desde dentro del sistema en ejecución; requieren acción humana en el límite físico o de red.

**Pasos de nivel plataforma** reflejan lo que hace el cliente para instalar y configurar la plataforma — ejecutar scripts de arranque, instalar paquetes de servicio, aprovisionar infraestructura en tiempo de ejecución. Los ejecuta quien esté cumpliendo el rol de cliente en el contexto de desarrollo actual.

**Pasos de nivel característica** reflejan lo que hace el cliente para extender la plataforma — añadir ingesta de datos, configurar el enrutamiento de IA, integrar servicios externos. Este es el trabajo de construcción de la propia plataforma.

Una prueba útil para cualquier tarea: si el paso aparece en el manual operativo de instalación del cliente, pertenece a la capa de plataforma o de operador. Si el paso es "construir el paquete que instala el cliente", pertenece a la capa de característica.

**Por qué importa:** quien no esté seguro de a qué capa pertenece una tarea tiene una prueba mecánica que aplicar, en lugar de un juicio que distintas personas responderían de forma diferente.

## Excepciones documentadas

Algunos pasos no pueden probarse internamente porque son estructuralmente imposibles de realizar desde dentro de un sistema en ejecución:

**Pasos en el límite de hardware.** Un script que detiene una máquina virtual no puede ejecutarse en esa máquina virtual. El equivalente del cliente es comprar y instalar hardware físico — tampoco realizado desde dentro de un sistema en ejecución. Ambos requieren acción en el límite de hardware o de cuenta.

**Pasos de publicación.** Construir imágenes, publicar paquetes y configurar repositorios públicos de artefactos son actividades previas que los clientes consumen pero no realizan. Solo la organización que publica ejecuta estos pasos; los clientes consumen el resultado.

**Investigación de preproducción.** Validar una configuración de modelo antes de publicar valores predeterminados recomendados es investigación que produce la recomendación. Los clientes consumen la recomendación; el proveedor hace la investigación que la produce.

**Por qué importa:** nombrar estas excepciones explícitamente significa que "no pudimos probarlo internamente" nunca es una excusa silenciosa para un paso indocumentado — cada excepción es una imposibilidad estructural nombrada, no una brecha que el proveedor eligió no cerrar.

## Conexión con la topología proveedor-cliente

El principio de ordenamiento cliente-primero es la forma operativa de la topología de tres niveles — código fuente del proveedor, catálogo de guías del cliente, instancias de despliegue — aplicada a nivel de desarrollo. El proveedor construye software (capa de característica); el cliente lo instala siguiendo una guía (capa de plataforma); el operador aprovisiona el hardware sobre el que se ejecuta (capa de límite de hardware). El ordenamiento cliente-primero mantiene estos tres niveles alineados: el proveedor desarrolla contra la misma secuencia que el cliente instala, evitando que los atajos internos del proveedor se conviertan en los problemas del primer día del cliente.

**Por qué importa:** la topología de tres niveles y la disciplina de desarrollo son la misma forma vista desde dos ángulos — un cliente que entiende una ya entiende por qué la otra funciona como funciona.

## Véase también

- [[compounding-substrate]] — la arquitectura de sustrato que este principio sirve
- [[data-vault-bookkeeping-substrate]] — un ejemplo de producto construido en orden de instalación del cliente
- [[deployment-patterns]] — las seis configuraciones canónicas desplegadas siguiendo este principio
- [[three-ring-architecture]] — el modelo de anillos que el cliente instala en secuencia
