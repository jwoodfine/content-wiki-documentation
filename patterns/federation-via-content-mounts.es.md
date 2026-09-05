---
schema: foundry-doc-v1
title: "Montajes de contenido y federación"
slug: federation-via-content-mounts
short_description: "El motor wiki renderiza artículos curados comprometidos directamente en su repositorio junto con contenido montado desde directorios locales separados, compartiendo una superficie de URL e índice de búsqueda."
category: patterns
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: federation-via-content-mounts.md
index_group: interface-and-user-experience
---

El patrón de montajes de contenido combina dos modos de autoría en una única instancia wiki: artículos editoriales curados comprometidos directamente en el repositorio de conocimiento, y contenido montado desde un directorio local separado. **Un lector que navega el wiki no puede distinguir qué modo produjo un artículo dado** — ambos se renderizan en las mismas páginas de categoría, el mismo índice de búsqueda, la misma navegación. El montaje de directorios locales ya funciona hoy; una extensión adicional — montar contenido obtenido automáticamente de un repositorio git remoto en lugar de una ruta ya local — sigue siendo una dirección de diseño, no una capacidad implementada.

## El modelo híbrido

Una instancia wiki desplegada se configura mediante un manifiesto `knowledge.toml` en la raíz del directorio de contenido. El manifiesto declara uno o más montajes, cada uno apuntando a un directorio local, junto con cualquier artículo comprometido directamente en el repositorio. Exactamente un montaje puede llevar el rol `primary` — el conjunto editable; cualquier montaje adicional es de solo lectura.

Los commits directos al montaje primario son la opción correcta para contenido de naturaleza editorial. Un montaje de solo lectura es la opción correcta para contenido cuyo hogar canónico es un repositorio distinto por completo — el wiki lo muestra sin asumir la responsabilidad de editarlo.

**Por qué importa:** una instancia wiki puede mostrar contenido que no le pertenece sin volverse jamás responsable de editarlo — el hogar canónico permanece donde el contenido realmente vive.

## Cómo funcionan los montajes hoy

Una entrada de montaje en `knowledge.toml` declara una ruta local, un rol (`primary` o solo lectura) y un `blueprint_set` — una lista de tipos de contenido que se espera que contenga el montaje. El motor recorre el directorio de cada montaje declarado al iniciar y construye su índice de contenido a partir de lo que encuentra; el directorio de un montaje debe existir ya en disco cuando el motor arranca.

**Lo que esto todavía no hace: obtener contenido de un repositorio remoto por iniciativa propia del wiki.** Un montaje hoy es un puntero a un directorio local ya presente, no un remoto git que el motor clona o actualiza según un calendario. Llevar contenido de un repositorio separado al directorio de un montaje es un paso que ocurre fuera del motor wiki.

**Por qué importa:** un operador que evalúe este patrón hoy debe esperar mantener poblado él mismo el directorio de un montaje — el motor lee lo que ya está ahí, todavía no va a buscar nada por su cuenta.

## Planos (blueprints)

El campo `blueprint_set` permite que un montaje declare qué tipos de contenido se espera que contenga — `TOPIC` y `GUIDE` son los dos nombres en uso actual. Es una expectativa declarada en la configuración; todavía no impulsa validación o enrutamiento específico por tipo de contenido más allá de esa declaración.

**Por qué importa:** un lector que inspeccione la configuración de un montaje puede saber qué tipo de contenido esperar ahí sin abrir un solo archivo — la declaración misma es la documentación.

## Aislamiento por instancia

Cada instancia wiki lee solo los montajes declarados en su propio `knowledge.toml`. El aislamiento es una propiedad de la configuración de cada instancia, no algo coordinado centralmente.

**Por qué importa:** una configuración incorrecta en los montajes de una instancia wiki nunca puede filtrar contenido hacia otra instancia, ni extraerlo de ella — el conjunto de artículos de cada instancia depende únicamente de su propia configuración.

## Lo que añadiría una extensión de obtención remota

Extender el montaje de rutas locales a la obtención de repositorios remotos — que el propio motor wiki clone y actualice periódicamente un remoto git dentro del directorio de un montaje, en lugar de depender de un proceso externo — es una dirección de diseño real para este patrón, todavía no construida. La extensión natural junto a ella son los metadatos de procedencia por artículo y el enrutamiento de edición hacia el repositorio fuente — ninguno de los cuales existe en la configuración de montajes hoy.

**Por qué importa:** nombrar esto como una dirección planificada y no como una función ya implementada evita que un lector piense erróneamente que el motor ya gestiona repositorios remotos por su cuenta.

## Relación con la inversión de la fuente de verdad

Este patrón extiende [[source-of-truth-inversion]] desde una topología de un solo repositorio hacia una de múltiples repositorios. El invariante es el mismo: git es canónico, el binario en ejecución es una vista.

**Por qué importa:** un lector que ya entiende la inversión de la fuente de verdad no necesita un segundo modelo mental para los montajes — es el mismo invariante canónico/vista, solo que con más de un repositorio canónico en juego.

## Véase también

- [[app-mediakit-knowledge]] — el motor que implementa este patrón
- [[source-of-truth-inversion]] — la decisión de diseño fundacional que extiende este patrón
- [[knowledge-wiki-leapfrog-architecture]] — la filosofía más amplia de arquitectura de información y navegación
