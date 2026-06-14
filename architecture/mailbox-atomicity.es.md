---
schema: foundry-doc-v1
title: "Atomicidad del buzón — Escritura exclusiva con flock e idempotencia por msg-id"
slug: mailbox-atomicity
language: es
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: mailbox-atomicity.md
---

Las sesiones se comunican añadiendo mensajes al principio de buzones en archivos planos situados en `.agent/inbox.md` y `.agent/outbox.md`. Los mensajes llevan un sobre YAML (from, to, re, created, status, msg-id opcional) seguido de un cuerpo de texto libre. Los mensajes más recientes aparecen al inicio, de modo que la sesión concentradora que lee una bandeja de salida ve la actividad más reciente primero.

El problema de atomicidad: dos sesiones que añaden al mismo buzón sin coordinación producen la condición de carrera clásica de leer-modificar-escribir. La sesión A lee el archivo actual, añade su mensaje y escribe de vuelta. La sesión B hace lo mismo simultáneamente. El que escribe último gana; el otro mensaje se pierde. Esto es reproducible con sub-agentes de IA en paralelo; la concurrencia entre usuarios lo hace inevitable.

El script auxiliar `mailbox-prepend` resuelve esto con `flock`. Toma la ruta del buzón de destino, deriva una ruta de bloqueo para buzones de alcance de archivo, y adquiere un bloqueo exclusivo con un tiempo de espera de 30 segundos antes de realizar la lectura-modificación-escritura. Dos llamadas simultáneas se serializan en lugar de colisionar.

Una segunda salvaguarda: idempotencia por msg-id. Si el cuerpo del mensaje contiene un campo `msg-id:`, el script analiza las primeras 200 líneas del archivo de destino en busca de una entrada existente con el mismo id y omite la adición si la encuentra. Esto significa que un script que se reintenta — un temporizador que se activa dos veces, un operador que lo vuelve a ejecutar, un hook que falla y reintenta — no enviará el mensaje dos veces. La ventana de 200 líneas es suficientemente generosa para detectar duplicados del mismo día sin hacer el análisis costoso en archivos grandes.

Esto es un envoltorio de dos líneas alrededor de `flock` y `grep`. El modo de fallo sin él es silencioso — un mensaje perdido simplemente nunca llega, y el remitente no tiene ninguna indicación. Consolidar esta disciplina en un script compartido que tanto las sesiones como la automatización realmente llaman es más barato que construir una cola más sofisticada.

## Véase también

- [[multi-engine-session-coordination]] — el protocolo de bloqueo de sesión que esta disciplina de buzón complementa
- [[totebox-session]] — el modelo de sesión cuya comunicación inter-sesión esta atomicidad protege
- [[totebox-orchestration-development]] — la capa de orquestación que enruta mensajes entre sesiones
- [[learning-datagraph-architecture]] — el ledger de auditoría cuyos hooks de captura enfrentan las mismas condiciones de carrera de escritura concurrente
