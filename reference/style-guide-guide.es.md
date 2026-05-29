---
schema: foundry-doc-v1
title: "Guía de estilo — GUIDE"
slug: style-guide-guide.es
short_description: "Cómo escribir un archivo GUIDE: el formato de runbook operativo para subcarpetas de implementación de plataforma, cubriendo estructura requerida de seis secciones, voz imperativa lacónica, actores nombrados, formato de comando, verificación concreta y la distinción de archivos TOPIC."
lang: es
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
paired_with: style-guide-guide.md
---

Un archivo GUIDE es un manual operativo: cómo ejecutar, configurar o recuperarse de una falla. Le indica al operador qué hacer, en orden, con los comandos exactos que copiará y pegará. No explica el razonamiento detrás del procedimiento; eso corresponde a un archivo TOPIC.

## Ubicación

Los GUIDEs viven dentro de la subcarpeta de despliegue que operan. Hay dos niveles:

| Nivel | Ruta | Propósito |
|---|---|---|
| Catálogo | `customer/woodfine-fleet-deployment/<nombre-despliegue>/guide-*.md` | Define cómo se opera este despliegue. |
| Instancia | `deployments/<instancia>/guide-*.md` | Solo cuando una instancia tiene desviaciones operativas significativas frente a su GUIDE de catálogo. |

Un GUIDE en la raíz de un catálogo de flota, sin subcarpeta de despliegue contenedora, está mal ubicado. Trasládelo a la subcarpeta correspondiente.

## Solo en inglés

Los archivos GUIDE son solo en inglés. Son operativos, no de cara al público — las parejas bilingües añaden costo de mantenimiento sin beneficio para una audiencia de operadores con competencia de trabajo en inglés.

## Estructura obligatoria de seis secciones

Cada GUIDE tiene seis secciones en este orden:

1. **Requisitos previos** — todo lo que el operador debe tener antes de comenzar.
2. **Propósito** — una oración que indica qué logra este GUIDE.
3. **Procedimiento** — pasos numerados en voz imperativa.
4. **Resultado esperado** — la post-condición que este GUIDE pretende establecer; enunciada como un hecho verificable.
5. **Verificación** — la secuencia de comandos que el operador ejecuta para confirmar que el resultado esperado se cumple.
6. **Recuperación** — cómo deshacer el procedimiento si la verificación falla. Nombre el modo de falla, el comando de diagnóstico y los pasos correctivos.

Las secciones que no se aplican no se omiten — explican por qué no se aplican. Una sección de Requisitos previos que no lista nada dice explícitamente: "Sin requisitos previos; el procedimiento es autocontenido."

## Voz imperativa terse

Los GUIDEs usan oraciones más cortas que los TOPICs. Presupuesto de longitud de oración: promedio de catorce palabras, máximo de veinticuatro. Voz imperativa — `ejecute`, `confirme`, `reinicie`, `verifique`. Voz activa siempre; la voz pasiva en un manual operativo oculta quién o qué realiza la acción, lo que importa cuando algo falla.

**Actores nombrados.** Cada paso nombra al agente y al objeto: "el operador ejecuta el siguiente comando", no "el siguiente comando se ejecuta". Cuando un paso cambia el estado de un servicio o sistema, diga qué cambia. Un paso que el operador no puede verificar no ocurrió.

La [[editorial-language-registers|lista de vocabulario prohibido]] se aplica. No tiene lugar en un manual operativo ninguna palabra que no describa algo que el operador pueda verificar.

## Comandos copiables y pegables

Cada comando en un GUIDE está en un bloque de código cercado, solo en su línea, listo para copiar y pegar. El código entre comillas en línea es para referirse a un comando, no para ejecutarlo.

Los marcadores de posición son obvios — `<id-inquilino>`, `<nombre-instancia>`, `<sha-commit>` — nunca `xxx`, `SU_VALOR` ni `[insertar aquí]`.

## Verificación concreta

Cada paso tiene una comprobación que el operador puede ejecutar para confirmar que el paso funcionó. La comprobación es un comando con una salida esperada, no una narración. "Verifique que el servicio esté activo" no es una comprobación. "`systemctl is-active local-doorman.service` devuelve `active`" sí lo es.

## Recuperación concreta

Las instrucciones de recuperación nombran el modo de falla que abordan, el comando de diagnóstico que lo confirma y los pasos correctivos. Mejor escribir "no hay recuperación automática; escale al equipo de guardia" que sugerir al operador que tiene opciones cuando el procedimiento no ha sido pensado hasta el final.

Dos casos especiales se manejan explícitamente:

- **Procedimiento idempotente**: "Este procedimiento es idempotente. Si se interrumpe, reinícielo desde el paso 1 — no hay estado parcial que limpiar."
- **Procedimiento irreversible**: "Esta operación no se puede deshacer. Verifique los requisitos previos y el resultado esperado antes de ejecutar el paso N."

## Qué no es un GUIDE

- No es un [[style-guide-topic|TOPIC]]. El razonamiento o la intención de diseño que motiva un procedimiento vive en un TOPIC.
- No es un script. Un script que el GUIDE invoca vive en el directorio `scripts/` del proyecto; el GUIDE lo referencia por ruta.
- No es un artefacto de cara al público. El detalle operativo pertenece a GUIDEs leídos por operadores con acceso al despliegue.

## Véase también

- [[style-guide-topic|Guía de estilo — TOPIC]]
- [[language-protocol-substrate|Sustrato de protocolo de lenguaje]]
- [[customer-hostability|Hospedaje por el cliente]]
