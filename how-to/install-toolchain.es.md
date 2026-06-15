---
schema: foundry-doc-v1
title: "Cómo instalar el conjunto de herramientas de desarrollo"
slug: install-toolchain
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: install-toolchain.md
---

El código de la plataforma es un espacio de trabajo Rust. El conjunto de herramientas de desarrollo consta del compilador Rust y las herramientas estándar de compilación Cargo, más el asistente de confirmación del espacio de trabajo que aplica la identidad del nivel de preparación y la firma de confirmaciones SSH. Esta guía cubre la instalación de ambos, la verificación de la instalación y la realización de la primera compilación de prueba.

Para la arquitectura más amplia del espacio de trabajo, véase [[totebox-orchestration-development]]. Para abrir su primera sesión después de configurar el conjunto de herramientas, véase [[open-first-totebox-session]].

## Requisitos previos

- Un dispositivo emparejado con acceso de nivel INPUT (véase [[pair-a-new-device]])
- Acceso SSH a la VM del espacio de trabajo (`foundry-workspace`)
- Una sesión de shell en la VM del espacio de trabajo

## Paso 1: Instalar el conjunto de herramientas Rust

El espacio de trabajo utiliza una versión del conjunto de herramientas Rust fijada especificada en `rust-toolchain.toml` en la raíz del monorepo. Instale `rustup`, el gestor del conjunto de herramientas Rust, si no está ya presente:

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Después de la instalación, cargue el archivo de entorno o abra una nueva sesión de shell. Rustup lee `rust-toolchain.toml` automáticamente cuando entra en un directorio con uno — no es necesaria ninguna selección explícita de versión.

## Paso 2: Verificar la instalación de Rust

Ejecute una verificación de versión desde dentro del clon del monorepo:

```
cd ~/Foundry/clones/<su-archivo>/pointsav-monorepo
cargo --version
rustc --version
```

Ambos comandos deben mostrar la versión fijada de `rust-toolchain.toml`. Si rustup informa que el conjunto de herramientas no está instalado, ejecute `rustup show` para desencadenar la instalación automática de la versión fijada.

## Paso 3: Ejecutar una compilación base

Compile el espacio de trabajo completo para confirmar que el conjunto de herramientas funciona de extremo a extremo:

```
cargo build
```

Una compilación limpia en la primera ejecución descarga y compila todas las dependencias y puede llevar varios minutos. Las compilaciones posteriores son incrementales. Si la compilación falla con una dependencia faltante, instale la biblioteca del sistema nombrada a través del gestor de paquetes (`apt-get install <lib>` en Debian/Ubuntu) y vuelva a ejecutar.

## Paso 4: Verificar el asistente de confirmación

El asistente de confirmación del espacio de trabajo (`~/Foundry/bin/commit-as-next.sh`) requiere un agente SSH en funcionamiento con la clave de firma del nivel de preparación cargada. El `git commit` directo está bloqueado por una compuerta pre-confirmación — todas las confirmaciones deben pasar por el asistente.

Verifique que el asistente sea accesible:

```
ls ~/Foundry/bin/commit-as-next.sh
```

Verifique que haya una clave SSH cargada:

```
ssh-add -l
```

Si no se lista ninguna clave, añada la clave de preparación:

```
ssh-add ~/Foundry/identity/jwoodfine/id_jwoodfine
```

El asistente de confirmación alterna la identidad de autor entre `jwoodfine` y `pwoodfine` automáticamente — no se necesita selección manual.

## Paso 5: Ejecutar pruebas

Confirme que la suite de pruebas pasa antes de comenzar a trabajar:

```
cargo test
```

Todas las pruebas deben pasar en un clon limpio. Un fallo de prueba antes de cualquier cambio local indica un clon obsoleto o un problema de entorno de compilación — verifique `git status` y compare el commit HEAD con la rama de preparación aguas arriba.

## Puntos clave

- La versión del conjunto de herramientas está fijada en `rust-toolchain.toml`; rustup la lee automáticamente
- `cargo build` / `cargo test` / `cargo clippy` / `cargo fmt` siempre están permitidos sin aprobación
- Todas las confirmaciones usan `commit-as-next.sh`; el `git commit` directo está bloqueado en la compuerta pre-confirmación
- Una clave SSH debe estar cargada en el agente antes de que el asistente de confirmación pueda firmar confirmaciones

## Véase también

- [[totebox-orchestration-development]] — la arquitectura de sesión que admite este conjunto de herramientas
- [[open-first-totebox-session]] — la secuencia completa de inicio de sesión después de configurar el conjunto de herramientas
- [[pair-a-new-device]] — cómo un dispositivo adquiere el acceso de nivel INPUT que permite las confirmaciones
- [[read-write-totebox-archives]] — el flujo completo de lectura/escritura para trabajar en un archivo
