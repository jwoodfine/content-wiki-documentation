---
schema: foundry-doc-v1
title: "Caché de compilación por usuario — prevención de condiciones de carrera en Cargo"
slug: cargo-target-per-user-discipline
language: es
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: cargo-target-per-user-discipline.md
---

La caché de compilación incremental de Cargo vive en `target/`. Por defecto eso es un directorio por crate dentro de cada crate. El espacio de trabajo anula esto mediante la variable de entorno `CARGO_TARGET_DIR` que apunta a una ruta compartida, de modo que la caché de compilación se comparte entre todos los crates del monorepo — ahorrando espacio en disco y tiempo de recompilación.

## Puntos clave

- Con un `CARGO_TARGET_DIR` compartido, dos llamadas concurrentes a `cargo build` compiten por `target/.cargo-lock` y entrecruzan la propiedad de archivos, causando errores esporádicos de `Permission denied` durante reconstrucciones incrementales — incluso cuando los crates compilados no están relacionados.
- Solución: un script de perfil del sistema establece `CARGO_TARGET_DIR` en `<raíz-compartida>/$USER/`, dando a cada desarrollador un subdirectorio privado de caché de compilación. La compilación incremental dentro de un usuario se preserva; las colisiones de propiedad de archivos entre usuarios se eliminan.
- `CARGO_TARGET_DIR` tiene precedencia sobre el ajuste `target-dir` de `~/.cargo/config.toml`. El cambio surte efecto en cualquier shell nueva sin ediciones por usuario de los dotfiles — un script de perfil a nivel de sistema es el punto de cumplimiento.
- La lección generaliza más allá de Cargo: cualquier ruta compartida de escritura grupal necesita diseño explícito sobre qué operaciones son seguras de compartir (lecturas, adiciones de contenido) y cuáles requieren partición por usuario (estado de compilación, archivos de bloqueo, directorios temporales).

Esto funciona para un único desarrollador. Con dos desarrolladores en el grupo del espacio de trabajo se convierte en una carrera. El `target/.cargo-lock` de Cargo serializa las compilaciones de árbol completo, de modo que dos invocaciones de `cargo build` en diferentes crates se bloquean mutuamente. Peor aún, la propiedad mezclada de archivos — artefactos de compilación escritos por un usuario entremezclados con los de otro — causa errores esporádicos de `Permission denied` durante la recompilación incremental, incluso cuando los crates parecen no estar relacionados.

La solución: un script de perfil del sistema exporta `CARGO_TARGET_DIR` apuntando a un subdirectorio por usuario (`<raíz-compartida>/$USER/`). Cada usuario obtiene un subdirectorio privado. La caché de compilación permanece compartida dentro de un usuario — la optimización original se conserva — pero ya no cruza entre usuarios. La variable de entorno tiene precedencia sobre el ajuste `target-dir` de `~/.cargo/config.toml`, por lo que el cambio surte efecto en cualquier shell nueva sin ediciones por usuario de los dotfiles.

La migración implicó mover la caché existente de 3,3 GiB al subdirectorio del primer usuario. El estado incremental de ese desarrollador se preserva; el otro comienza con una caché vacía que se llena en la primera compilación.

Las cuentas de servicio en el grupo del espacio de trabajo (local-doorman, local-design y similares) no ejecutan Cargo y no reciben un directorio de caché por usuario. El script de perfil solo exporta cuando existe la raíz de caché compartida, por lo que los contextos que no son del espacio de trabajo no se ven afectados.

La lección generaliza: cualquier ruta compartida de escritura grupal necesita diseño explícito sobre qué operaciones son seguras de compartir (lecturas, adiciones de contenido) y cuáles requieren partición por usuario (estado de compilación, archivos de bloqueo, temporales). Cargo es el ejemplo prominente; la misma lógica aplica a cualquier cosa con estado mutable bajo una raíz compartida.

## Véase también

- [[foundry-services-slice-model]] — la partición cgroup que protege los recursos de servicios compartidos en el mismo entorno multi-desarrollador
- [[multi-engine-session-coordination]] — el protocolo de bloqueo de sesión que previene una clase relacionada de conflictos en el mismo repositorio
- [[totebox-session]] — el modelo de sesión alrededor del cual está construido el espacio de trabajo multi-operador
