---
schema: foundry-doc-v1
title: "Cómo instalar el conjunto de herramientas de desarrollo"
slug: install-toolchain
short_description: "Instala el conjunto de herramientas Rust fijado con rustup, ejecuta una compilación y pruebas base, y verifica el asistente de commits y la clave SSH de firma necesarios antes de trabajar en un archivo del monorepo."
category: how-to
index_group: getting-started
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); new contributors"
last_edited: 2026-08-06
editor: pointsav-engineering
language_protocol: TRANSLATE-ES
paired_with: install-toolchain.md
research_trail:
  sources: [pointsav-monorepo rust-toolchain.toml, bin/commit-as-next.sh, identity/ store layout]
  verification_method: "verified against the real rust-toolchain.toml pin and the commit-as-next.sh pre-commit gate already documented in read-write-totebox-archives.md"
---

El código de la plataforma es un espacio de trabajo Rust. El conjunto de herramientas de desarrollo consta del compilador Rust y las herramientas estándar de compilación Cargo, más el asistente de confirmación del espacio de trabajo que aplica la identidad del nivel de preparación y la firma de confirmaciones SSH. Esta guía cubre la instalación de ambos, la verificación de la instalación y la realización de la primera compilación de prueba.

Para la arquitectura más amplia del espacio de trabajo, véase [[totebox-orchestration-development]]. Para abrir su primera sesión después de configurar el conjunto de herramientas, véase [[open-first-totebox-session]].

## Requisitos previos

- Un dispositivo emparejado con el espacio de trabajo (véase [[pair-a-new-device]])
- Acceso SSH a su VM del espacio de trabajo
- Una sesión de shell en esa VM

## Propósito

Instalar el conjunto de herramientas Rust fijado, confirmar que compila y prueba el espacio de trabajo sin errores, y verificar que el asistente de confirmación y la clave de firma SSH estén listos — el conjunto completo de condiciones previas para hacer una primera confirmación en un archivo del monorepo.

## Procedimiento

1. **Instalar el conjunto de herramientas Rust.** El espacio de trabajo utiliza una versión del conjunto de herramientas Rust fijada especificada en `rust-toolchain.toml` en la raíz del monorepo. Instale `rustup`, el gestor del conjunto de herramientas Rust, si no está ya presente:

   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   Después de la instalación, cargue el archivo de entorno o abra una nueva sesión de shell. Rustup lee `rust-toolchain.toml` automáticamente cuando entra en un directorio con uno — no es necesaria ninguna selección explícita de versión.

2. **Verificar la instalación de Rust.** Ejecute una verificación de versión desde dentro del clon del monorepo:

   ```bash
   cd ~/Foundry/clones/<su-archivo>/pointsav-monorepo
   cargo --version
   rustc --version
   ```

   Ambos comandos deben mostrar la versión fijada de `rust-toolchain.toml`. Si rustup informa que el conjunto de herramientas no está instalado, ejecute `rustup show` para desencadenar la instalación automática de la versión fijada.

3. **Ejecutar una compilación base.** Compile el espacio de trabajo completo para confirmar que el conjunto de herramientas funciona de extremo a extremo:

   ```bash
   cargo build
   ```

   Una compilación limpia en la primera ejecución descarga y compila todas las dependencias y puede llevar varios minutos. Las compilaciones posteriores son incrementales. Si la compilación falla con una dependencia faltante, instale la biblioteca del sistema nombrada a través del gestor de paquetes (`apt-get install <lib>` en Debian/Ubuntu) y vuelva a ejecutar.

4. **Verificar el asistente de confirmación.** El asistente de confirmación del espacio de trabajo (`~/Foundry/bin/commit-as-next.sh`) requiere un agente SSH en funcionamiento con la clave de firma del nivel de preparación cargada. El `git commit` directo está bloqueado por una compuerta pre-confirmación — todas las confirmaciones deben pasar por el asistente.

   Verifique que el asistente sea accesible:

   ```bash
   ls ~/Foundry/bin/commit-as-next.sh
   ```

   Verifique que haya una clave SSH cargada:

   ```bash
   ssh-add -l
   ```

   Si no se lista ninguna clave, añada la clave de su identidad de preparación:

   ```bash
   ssh-add ~/Foundry/identity/<su-identidad>/<su-clave>
   ```

   Los equipos de nivel de preparación normalmente alternan la autoría de las confirmaciones entre dos o más identidades automáticamente — consulte el almacén de identidades de su espacio de trabajo para ver los nombres exactos en uso.

5. **Ejecutar pruebas.** Confirme que la suite de pruebas pasa antes de comenzar a trabajar:

   ```bash
   cargo test
   ```

## Resultado esperado

`cargo build` y `cargo test` se completan sin errores en la versión fijada del conjunto de herramientas, el script del asistente de confirmación es accesible, y una clave SSH está cargada en el agente — el espacio de trabajo está listo para una primera confirmación.

## Verificación

Todas las pruebas deben pasar en un clon limpio. Un fallo de prueba antes de cualquier cambio local indica un clon obsoleto o un problema de entorno de compilación — verifique `git status` y compare el commit HEAD con la rama de preparación aguas arriba.

## Reversión

La instalación del conjunto de herramientas no tiene ningún efecto secundario destructivo que revertir. Si `rustup` se instaló por error, elimínelo con `rustup self uninstall`; esto no afecta al clon del monorepo en sí.

## Próximos pasos

- [[read-write-totebox-archives]] — el flujo completo de lectura/escritura para trabajar en un archivo
- [[open-first-totebox-session]] — la secuencia completa de inicio de sesión después de configurar el conjunto de herramientas

## Véase también

- [[totebox-orchestration-development]] — la arquitectura de sesión que admite este conjunto de herramientas
- [[pair-a-new-device]] — cómo se empareja un dispositivo con el espacio de trabajo en primer lugar
