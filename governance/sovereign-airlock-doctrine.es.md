---
schema: foundry-doc-v1
title: "La exclusa soberana"
slug: sovereign-airlock-doctrine.es
category: governance
type: topic
quality: complete
short_description: "La exclusa soberana es el protocolo de commits por etapas que impone una separación estricta entre las identidades de staging que escriben trabajo y las identidades de repositorio canónico que lo publican — dos autores de staging para todos los commits, dos identidades de administrador para los pushes canónicos, sin ruta directa entre ellos."
status: active
bcsc_class: public-disclosure-safe
language: es
language_protocol: PROSE-TOPIC
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: sovereign-airlock-doctrine.md
---

La **exclusa soberana** es el protocolo de commits y despliegue que impone una separación estructural entre las identidades que escriben trabajo y las identidades que lo publican en repositorios canónicos. Ningún autor de commits tiene acceso push directo a un repositorio canónico. Ninguna identidad push canónica es autora de commits. Las dos funciones están separadas criptográficamente: una sesión que escribe código no puede hacer push sin pasar por el paso explícito de promoción Stage 6, y ese paso de promoción no puede ejecutarlo la misma identidad que realizó el commit. Esto no es una política impuesta por la configuración de herramientas — es una imposibilidad estructural, ya que la clave de autor de commit y la clave de push pertenecen a directorios de identidad distintos.

## Las cuatro identidades

El almacén de identidades de la plataforma define cuatro identidades en `~/Foundry/identity/`, cada una respaldada por una clave SSH dedicada:

| Identidad | Clave | Función | Ámbito |
|---|---|---|---|
| `jwoodfine` | `id_jwoodfine` | Staging — Jennifer | Todos los commits en repos de ingeniería |
| `pwoodfine` | `id_pwoodfine` | Staging — Peter | Todos los commits en repos de ingeniería |
| `ps-administrator` | `id_pointsav-administrator` | Solo push | Org canónica `pointsav` en GitHub |
| `mcorp-administrator` | `id_woodfine-administrator` | Solo push | Org canónica `woodfine` en GitHub |

Las identidades de staging (`jwoodfine`, `pwoodfine`) se usan exclusivamente a través de `bin/commit-as-next.sh`. Sus claves solo existen en `~/Foundry/identity/` y nunca se elevan a derechos de push en repos canónicos. Las identidades de administrador tienen derechos de push en repositorios canónicos pero nunca se usan como autores de commits.

## El flujo de commits

El trabajo fluye a través de tres niveles:

```
Nivel de staging (commits de jwoodfine, pwoodfine)
       │
       │ bin/promote.sh  (Stage 6 — iniciado por el operador, solo sesión Command)
       ▼
Nivel vendor canónico  (pointsav/* — push vía alias SSH ps-administrator)
       │
       │ gobernanza factory-release-engineering
       ▼
Nivel customer canónico  (woodfine/* — push vía alias SSH mcorp-administrator)
```

`bin/commit-as-next.sh` alterna la autoría entre `jwoodfine` y `pwoodfine` en commits sucesivos. `bin/promote.sh` empaqueta los commits staged y los envía al remoto canónico correspondiente usando el alias SSH de la identidad administradora. Las claves de las identidades administradoras están configuradas solo para autenticación de push; no aparecen como autores de commits en `git log`.

## La garantía estructural

La garantía de la exclusa no es "es poco probable que los usuarios hagan push directo" sino "el push directo desde una sesión de staging es estructuralmente imposible." Una sesión de staging que intenta `git push origin main` desde dentro de un archivo Totebox está haciendo push al remoto de staging, no al origen canónico. Hacer push al canónico requiere el alias SSH administrador, que requiere la clave administradora, que requiere que el operador invoque explícitamente `bin/promote.sh` desde una sesión Command.

Esta separación cumple dos funciones para los operadores regulados. Primero, convierte el nivel de staging en un límite de revisión genuino: los commits promovidos llevan implícita la aprobación de que el operador revisó el trabajo desde una sesión Command antes de autorizar el push canónico. Segundo, mantiene el historial de commits limpio — cada commit en el repositorio canónico fue creado por una identidad de staging conocida, revisado en un momento conocido, y promovido mediante una acción deliberada del operador.

## Custodia de claves

Las cuatro claves residen en `~/Foundry/identity/` con permisos `0600`, accesibles únicamente al usuario del sistema `mathew`. Las herramientas de sesión leen las claves desde este directorio; ninguna clave se copia en un repositorio ni se exporta al entorno de la sesión. La regla `chmod` está impuesta por un hook pre-commit que bloquea commits que contengan material de clave con el patrón `**/id_*`.

## Véase también

- [[pairing-as-permission]] — el patrón de emparejamiento criptográfico que gobierna qué nodos pueden conectarse
- [[machine-based-auth]] — el protocolo de autenticación basado en máquina de la plataforma
- [[single-boundary-compute-discipline]] — el límite de inferencia de IA que aplica la misma disciplina de separación de claves en la capa de modelo
