---
schema: foundry-doc-v1
title: "Cómo usar el modelo de cartuchos de tecla de función"
slug: use-f-key-model
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: use-f-key-model.md
---

El modelo de teclas de función es la interfaz de operador de `os-console`. Cada ranura de tecla de función aloja un Cartucho — un módulo independiente compilado en el binario que controla su renderizado, manejo de teclado y ciclo de vida. Entender las asignaciones de ranuras y cómo funciona cada Cartucho permite moverse eficientemente entre funciones de la plataforma sin salir del terminal.

Para la interfaz Cartridge y cómo se compilan las ranuras, véase [[app-console-keys]]. Para los fundamentos de navegación, véase [[navigate-console-tui]].

## Asignaciones de ranura predeterminadas

| Tecla de función | Cartucho | Función principal |
|---|---|---|
| F3 | Correo electrónico | Leer y redactar mensajes; véase [[app-console-email]] |
| F9 | SLM | Inferencia local y panel de estado de Doorman; véase [[app-console-slm]] |
| F12 | Máquina de Entrada | Entrada de registros verificada por humanos; obligatorio según SYS-ADR-10; véase [[app-console-input]] |

Las ranuras no enumeradas están reservadas o no cargadas. Una etiqueta atenuada en la franja de navegación indica que la ranura no está cargada en la sesión actual.

## Cómo funciona un Cartucho

Un Cartucho está compilado en el binario de `os-console`. No es un complemento ni un script en tiempo de ejecución. Al presionar una tecla de función, el binario transfiere el control al Cartucho registrado para esa ranura.

Cada Cartucho:
- Renderiza su propia vista de pantalla completa en el área de ranura
- Maneja eventos de teclado para esa ranura
- Reporta a la barra de estado cuál ranura está activa
- Se conecta al servicio de plataforma correspondiente (correo, SLM, libro mayor) usando la conexión MBA activa

Un Cartucho que no puede alcanzar su servicio de respaldo muestra un indicador de estado en el área de ranura en lugar de fallar silenciosamente.

## Usar el Cartucho de Correo (F3)

1. Presione **F3** para abrir el Cartucho de Correo.
2. Aparece la lista de bandeja de entrada con recuentos de no leídos y resúmenes de remitentes.
3. Navegue con las teclas de flecha; presione **Enter** para abrir un mensaje.
4. Presione **c** para redactar un nuevo mensaje.

Los mensajes salientes se enrutan a través de `service-email`. No se usan conexiones SMTP directas — el Cartucho actúa como Diodo de Comunicación, aplicando la política de comunicación del inquilino antes de enviar.

Para detalles sobre el flujo de correo, véase [[app-console-email]].

## Usar el Cartucho SLM (F9)

1. Presione **F9** para abrir el Cartucho SLM.
2. El panel de estado de Doorman muestra cuál nivel de inferencia (A, B o C) está activo y el recuento de entidades del DataGraph.
3. Presione **R** para actualizar manualmente el estado de salud.
4. Ingrese un prompt en la línea de entrada. La respuesta se transmite al área de ranura.

Todas las solicitudes de inferencia se enrutan a través de Doorman. Los datos del prompt no salen del hardware del operador.

Para la arquitectura de inferencia, véase [[app-console-slm]] y [[doorman-protocol]].

## Usar la Máquina de Entrada (F12)

La ranura F12 es la compuerta de intervención humana requerida por SYS-ADR-10. Es el único camino por el que un registro verificado por un operador puede entrar al libro mayor WORM.

1. Presione **F12** para abrir la Máquina de Entrada.
2. Revise el registro o documento mostrado para verificación.
3. Confirme o rechace usando las combinaciones de teclas mostradas en la franja de navegación.

Un registro confirmado se escribe en el libro mayor de inmediato. Un registro rechazado se enruta a cuarentena.

Para el fundamento del diseño, véase [[app-console-input]] y [[worm-ledger-architecture]].

## Puntos clave

- Cada ranura está compilada en el momento de construcción — no hay tiempo de ejecución de complementos ni intercambio de ranuras en caliente
- Un Cartucho que pierde su servicio de respaldo degrada con gracia y muestra un indicador de estado
- F12 no puede reasignarse; es estructuralmente la compuerta de verificación humana para el libro mayor
- El modelo de Diodo de Comunicación en F3 significa que el enrutamiento de correo aplica política del inquilino — no puede omitirse desde dentro del Cartucho

## Véase también

- [[app-console-keys]] — arquitectura del chasis, interfaz Cartridge, componentes de la barra de estado
- [[app-console-email]] — Cartucho de Correo: bandeja de entrada, lectura, redacción y modo texto plano
- [[app-console-slm]] — Cartucho SLM: panel de Doorman e inferencia local
- [[app-console-input]] — Máquina de Entrada: la compuerta de verificación humana F12
- [[navigate-console-tui]] — disposición general de la TUI y navegación de ranuras
- [[worm-ledger-architecture]] — el libro mayor en el que escribe F12
