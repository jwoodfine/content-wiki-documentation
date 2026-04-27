# Guía de estilo — GUIDE (resumen)

Un archivo GUIDE (`GUIDE-<asunto>.md`) es un manual operativo —
cómo ejecutar, configurar o recuperarse de una falla. Le indica
al operador qué hacer, en orden, con los comandos exactos que
copiará y pegará. No explica el por qué; eso corresponde a un
archivo TOPIC.

## Ubicación

Los GUIDEs viven dentro de la subcarpeta de despliegue que
operan. Hay dos niveles:

| Nivel | Ruta | Propósito |
|---|---|---|
| Catálogo | `customer/woodfine-fleet-deployment/<nombre-despliegue>/GUIDE-*.md` | Define cómo se opera este nombre de despliegue. |
| Instancia | `~/Foundry/deployments/<instancia>/GUIDE-*.md` | Variación solo cuando una instancia tiene desviaciones operativas significativas frente a su GUIDE de catálogo. |

Un GUIDE en la raíz de un catálogo, sin subcarpeta de
despliegue contenedora, está mal ubicado. Trasládelo a la
subcarpeta correspondiente.

## Reglas centrales

- **Solo en inglés.** Los GUIDEs son operativos, no de cara al
  público. Las parejas bilingües añaden costo de mantenimiento
  sin beneficio para una audiencia de operadores.
- **Estructura obligatoria.** Cuatro secciones: Propósito,
  Procedimiento (pasos numerados, voz imperativa), Verificación
  (cómo confirma el operador que cada paso funcionó),
  Recuperación (qué hacer si un paso falla).
- **Voz imperativa terse.** Promedio de oraciones cerca de
  catorce palabras; máximo cerca de veinticuatro. Voz activa
  siempre.
- **Comandos copiables y pegables.** Cada comando en un bloque
  de código cercado, solo en su línea, listo para copiar y
  pegar. Los marcadores de posición son obvios
  (`<id-inquilino>`, `<sha-commit>`), nunca `xxx` ni
  `INSERTAR_AQUÍ`.
- **Verificación concreta.** Cada paso tiene una comprobación
  ejecutable con salida esperada — un comando, no una
  narración.
- **Recuperación concreta.** Las instrucciones de recuperación
  nombran el modo de falla, el comando de diagnóstico que lo
  confirma, y el procedimiento correctivo. Mejor "no hay
  recuperación automática; escalar al equipo de guardia" que
  un gesto vago hacia la recuperación.

## Qué no es un GUIDE

- No es un TOPIC. El razonamiento o la intención de diseño que
  motiva un procedimiento vive en un TOPIC.
- No es un script. Un script que el GUIDE invoca vive en
  `scripts/` del proyecto; el GUIDE lo referencia por ruta.
- No es un artefacto de cara al público. El detalle operativo
  pertenece a archivos leídos por operadores con acceso al
  despliegue.

## Véase también

- [Documento canónico en inglés](topic-style-guide-guide.md)
- [Guía de estilo — README](topic-style-guide-readme.md)
- [Guía de estilo — TOPIC](topic-style-guide-topic.md)
