---
schema: foundry-doc-v1
title: "Decisiones de arquitectura"
slug: architecture-decisions.es
lang: es
paired_with: architecture-decisions.md
category: governance
type: governance
quality: complete
short_description: "Doce decisiones de arquitectura vinculantes — compromisos registrados que gobiernan la construcción de la plataforma PointSav y restringen toda la ingeniería futura en el manejo de datos, la supervisión humana, la separación de sistemas y la custodia del despliegue."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: architecture-decisions.md
---

Las decisiones de arquitectura son compromisos registrados — elecciones tomadas deliberadamente, por razones declaradas, que vinculan toda la ingeniería futura de la plataforma. A diferencia de las convenciones, que describen cómo el equipo prefiere trabajar, las decisiones de arquitectura describen lo que la plataforma no hará independientemente de la conveniencia. Doce decisiones gobiernan la plataforma PointSav en la versión actual. Tres de ellas — ADR-07, ADR-10 y ADR-19 — tienen el mayor peso regulatorio: juntas definen el límite entre el procesamiento automatizado y la autoridad humana sobre los [[worm-ledger-design|registros permanentes]] de la plataforma. Al final de este artículo, un lector comprenderá las tres decisiones que más afectan la postura de cumplimiento, las decisiones que gobiernan la separación estructural, y las decisiones que gobiernan la custodia del despliegue.

## Las tres decisiones que gobiernan la IA y la autoridad humana

Estas tres decisiones definen dónde se detiene el procesamiento automatizado y dónde comienza la autoridad humana. Son las decisiones que un auditor, un evaluador de adquisiciones o un revisor de diligencia debida técnica debe leer primero.

**ADR-07 — Los datos deben clasificarse antes de que el límite de IA los toque.**
Cada archivo que ingresa a la plataforma se clasifica por tipo antes de que ocurra cualquier procesamiento. Los datos estructurados — hojas de cálculo, entradas de libro mayor, exportaciones de bases de datos, documentos firmados — se dirigen a motores de análisis deterministas que producen resultados verificables y reproducibles. El texto humano no estructurado — correspondencia, notas de reuniones, informes narrativos — se dirige al límite del modelo de lenguaje. Nada cruza el límite sin clasificar. Esto evita que la plataforma aplique razonamiento de IA a registros que deberían recibir un tratamiento determinista y auditable.

**ADR-10 — Cada entrada del libro mayor de activos base requiere un punto de control humano.**
La [[service-input|interfaz de entrada F12]] de la plataforma es el punto de control obligatorio con un humano en el bucle para todos los compromisos del libro mayor de activos base. Ningún proceso automatizado puede escribir un registro verificado en el almacenamiento a largo plazo sin que un humano confirme la decisión de enrutamiento en la puerta F12. El diseño refleja la estructura de control de una cámara de compensación regulada: la plataforma puede procesar, clasificar y proponer — pero el compromiso pertenece a un humano autorizado.

**ADR-19 — Sin publicación automatizada en libros mayores verificados.**
Los procesos automatizados tienen prohibido publicar en los libros mayores de almacenamiento a largo plazo. Todos los registros verificados se comprometen únicamente mediante una acción autenticada por humanos en la interfaz F12. La decisión cierra el círculo entre ADR-07 (clasificar primero) y ADR-10 (punto de control humano): la clasificación propone, el punto de control confirma, y el compromiso con el registro permanente requiere la acción intencional del operador. No existe ningún canal secundario a través del cual el sistema pueda registrar un hecho sin un humano en la secuencia.

Juntas, estas tres decisiones producen una estructura de registros que satisface el requisito de custodia común a las operaciones financieras y de propiedad reguladas: el sistema genera propuestas estructuradas, los humanos autorizan los registros permanentes, y la pista de auditoría captura ambos.

## Las decisiones que gobiernan la estructura de datos y la separación interna

**ADR-17 — Tres niveles de datos, un nivel autenticado por humanos.**
Los datos de la plataforma se modelan en tres niveles. El primer nivel son los activos base en bruto — documentos y registros originales tal como se reciben, tratados como inmutables. El segundo nivel es un índice de taxonomía autocorrectivo — la clasificación de esos activos por parte de la plataforma, que puede actualizarse a medida que cambian las reglas sin alterar el registro subyacente. El tercer nivel es la producción sintetizada — informes, resúmenes y extractos estructurados derivados de los activos base. Solo el nivel de activos base requiere un compromiso autenticado por humanos según ADR-10. Las capas de taxonomía y síntesis pueden autocorregirse sin más acción humana, porque derivan su autoridad del [[worm-ledger-architecture|nivel inmutable subyacente]].

**ADR-06 — Libro mayor de cumplimiento separado del grupo de inteligencia.**
El libro mayor de cumplimiento inmutable — el [[service-email|servicio que maneja las comunicaciones entrantes]] y la correspondencia regulada — está físicamente separado del [[service-slm|grupo de inteligencia autocorrectivo]] que la plataforma utiliza para clasificar y vincular documentos. La separación previene un modo de fallo común en los sistemas de recuperación: cuando el registro de cumplimiento y el índice de búsqueda comparten una capa de datos, una actualización del índice puede alterar silenciosamente lo que parece contener el registro de cumplimiento. La separación física elimina ese riesgo por construcción.

**ADR-11 — Chasis de consola separado de los cartuchos de ejecución.**
La consola del operador se divide en un chasis de presentación — el shell de interfaz de usuario que maneja el diseño, la navegación y los atajos de teclado — y un conjunto de cartuchos de ejecución, cada uno de los cuales implementa una función específica de la consola. El chasis y los cartuchos pueden desplegarse y actualizarse de forma independiente. Un cambio en el cartucho de revisión de cumplimiento no requiere redeplegar el shell de presentación, y viceversa. Esta separación hace que las funciones individuales de la consola sean auditables y reemplazables sin riesgo para la estabilidad del shell.

**ADR-14 — Los activos estáticos y los comandos en vivo utilizan rutas de proxy separadas.**
Los activos de interfaz de usuario estáticos — los archivos que un navegador descarga una vez para renderizar la consola — se sirven desde un servidor web de borde optimizado para caché y entrega. Los comandos API en vivo — las instrucciones que un operador envía a la plataforma — viajan a través de una red de malla cifrada hacia el backend. Las rutas nunca se mezclan. Eliminar el backend de Rust como servidor de archivos estáticos elimina una clase de problemas de latencia y caché que de otro modo solo aparecerían bajo condiciones de carga en producción.

## Las decisiones que gobiernan la custodia y el despliegue

**ADR-13 — Las claves criptográficas permanecen en el hardware del operador.**
El nodo de enrutamiento maestro y sus claves criptográficas residen en la [[totebox-os|máquina local del operador como una máquina virtual de Tipo II]]. No están alojados en infraestructura de nube comercial. Esta decisión refleja un principio de custodia específico: la entidad que posee las claves de firma para un conjunto de registros regulados debe ser la entidad regulada, no un proveedor de nube externo. El modelo de despliegue está diseñado para que un cliente pueda satisfacer este requisito sin gestionar infraestructura de metal desnudo.

**ADR-08 — systemd es una dependencia en cuarentena.**
El sistema de inicio systemd, requerido en los nodos actuales de Debian en la nube, está formalmente clasificado como un componente en cuarentena — una dependencia que la plataforma acepta temporalmente mientras se planifica el reemplazo del microkernel. La decisión se registra para que el trabajo de ingeniería futuro no profundice inadvertidamente la dependencia. Los servicios de la plataforma que actualmente se ejecutan bajo systemd están diseñados para ser portables al microkernel objetivo sin reelaboración arquitectónica.

## Las decisiones que gobiernan la integridad operativa

**ADR-15 — Las páginas de consola nunca se almacenan en caché.**
Todas las páginas de la consola del operador se sirven con encabezados que deshabilitan el caché y parámetros de obtención versionados. La decisión elimina un modo de fallo que aparece en las herramientas operativas reguladas: un navegador que presenta un estado de consola obsoleto almacenado en caché mientras los datos subyacentes han cambiado. Un operador que actúa sobre una vista de consola almacenada en caché puede tomar una acción basada en información que ya no refleja el estado de la plataforma. La plataforma lo previene por construcción en lugar de por disciplina del operador.

**ADR-16 — Los comandos entre pares viajan como unidifusión, no como difusión.**
Los comandos enviados a los nodos pares en la red de malla de la plataforma viajan como entregas unidifusión individuales — un comando por nodo — en lugar de como una difusión de red. La difusión UDP nativa es incompatible con la malla cifrada WireGuard que la plataforma utiliza para la comunicación entre nodos. El bucle unidifusión preserva las garantías de entrega sin requerir una capa de difusión separada.

**ADR-18 — La consola del operador es una pantalla de información.**
La consola del operador está diseñada como una pantalla de información que conecta a los operadores con la arquitectura de datos derivados de la plataforma. Cada tecla de función se mapea a un viewport de cartucho distinto — una vista delimitada de una parte de los datos de la plataforma — en lugar de a una interfaz de forma libre. El diseño limita la superficie de cada interacción del operador, lo que reduce las categorías de error que un operador puede introducir en una sola sesión.

## Véase también

- [[doorman-protocol]] — el servicio Doorman que aplica el límite de clasificación de datos de ADR-07 en producción
- [[app-console-input]] — la puerta de entrada F12 que implementa el punto de control humano de ADR-10
- [[worm-ledger-design]] — la arquitectura del libro mayor WORM que hace que la prohibición de ADR-19 sea aplicable
- [[three-ring-architecture]] — la estructura de anillos que la separación de ADR-06 refleja en la capa de servicios
- [[disclosure-substrate]] — la arquitectura que produce la cadena de registros auditable que estas decisiones protegen
