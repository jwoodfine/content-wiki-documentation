---
schema: foundry-doc-v1
title: "Cómo autoalojar un despliegue"
slug: self-host-a-deployment
short_description: "Compila desde el código fuente las imágenes de appliance seL4/Microkit de os-totebox y app-orchestration-slm y las arranca bajo QEMU, con la configuración incrustada en tiempo de compilación mediante bootargs del device tree, y verifica que ambas arrancan en buen estado."
category: self-hosting
index_group: getting-the-platform-running
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language_protocol: TRANSLATE-ES
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: self-host-a-deployment.md
research_trail:
  sources: [pointsav-monorepo os-totebox/scripts/build-guest-rootfs.sh, app-orchestration-slm/scripts/build-guest-rootfs.sh, vendor-libvmm]
  verification_method: "re-verified 2026-09-05: build-guest-rootfs.sh exists for both os-totebox and app-orchestration-slm and produces a loader image as a build output; no evidence found that either appliance's loader image is published as a downloadable artifact under a fixed filename, so this guide describes building from source rather than downloading a release"
---

## Requisitos previos

- Un host capaz de ejecutar QEMU para `aarch64` (las imágenes de appliance apuntan a esta arquitectura con independencia de la CPU propia del host)
- El repositorio fuente, el SDK de Microkit y una cadena de herramientas de compilación cruzada para `aarch64` — para compilar una imagen de arranque de `os-totebox` y, opcionalmente, de `app-orchestration-slm`, desde el código fuente
- Un disco persistente, creado una sola vez y conservado — un archivo raw formateado en ext4 que el invitado monta en `/data`

## Propósito

Autoalojar un despliegue consiste en arrancar una de estas dos imágenes de appliance seL4/Microkit independientes y autocontenidas — o ambas — sobre infraestructura controlada por el operador:

- `os-totebox` — el Sovereign WORM Data Vault: DataGraph local, ingesta de corpus, operaciones de Tier A.
- `app-orchestration-slm` — el chasis de intermediación Yo-Yo: endpoints de salud, flota y descubrimiento; la intermediación de Tier B requiere licencia.

Cada una se ejecuta de forma autónoma por defecto; ninguna necesita que la otra esté presente para arrancar.

## Procedimiento

1. Cree su disco persistente, una sola vez:

   ```
   qemu-img create -f raw persistent.raw 2G
   ```

   Aquí es donde el estado del DataGraph, los pesos de los adaptadores y la identidad en caché sobreviven entre reinicios. Perder este archivo significa perder todo lo que el appliance haya acumulado — no se regenera a partir de la imagen.

2. Arranque la imagen mediante el mecanismo `-device loader` de QEMU (esta es la ruta de carga propia de Microkit, no la ruta `-kernel`/`-append` que usaría una máquina virtual Linux de propósito general):

   ```
   qemu-system-aarch64 \
     -machine virt,virtualization=on,secure=off -cpu cortex-a53 \
     -device loader,file=os-totebox-loader.img,addr=0x70000000,cpu-num=0 \
     -m size=2G -nographic -global virtio-mmio.force-legacy=false \
     -drive file=persistent.raw,format=raw,if=none,id=hd \
     -device virtio-blk-device,drive=hd,bus=virtio-mmio-bus.1 \
     -device virtio-net-device,netdev=netdev0,bus=virtio-mmio-bus.0 \
     -netdev user,id=netdev0,hostfwd=tcp::<host-port>-:<guest-port>
   ```

3. Entienda esto antes de compilar: **la configuración de ejecución queda incrustada en la imagen en tiempo de compilación**, dentro de los `bootargs` del device tree. No existe archivo de configuración posterior al arranque ni equivalente de `-append` en esta ruta de arranque. Fijar la configuración implica pasar sus propios valores de bootarg `foundry.*` a la compilación.

   | Clave | Appliance | Propósito |
   |---|---|---|
   | `foundry.orchestration_endpoint` | os-totebox | URL del chasis para la intermediación de Tier B |
   | `foundry.tier_b_subscribed` | os-totebox | `true` para reclamar una suscripción de pago en el registro |
   | `foundry.yoyo_default_endpoint` | app-orchestration-slm | URL del backend de cómputo Yo-Yo por defecto |
   | `foundry.license_token` / `foundry.license_pubkey_hex` | app-orchestration-slm | Licencia de Tier B firmada con Ed25519 |

4. Repita el Paso 2 con `app-orchestration-slm-loader.img` si también desea el chasis de intermediación Yo-Yo — es una imagen independiente, con su propia invocación de arranque, no un componente que se inicie desde dentro de `os-totebox`.

## Resultado esperado

`os-totebox` alcanza un estado saludable y autónomo a los pocos segundos del arranque, con o sin `app-orchestration-slm` presente — este comportamiento de degradar en lugar de rechazar es el diseño previsto, no un síntoma de mala configuración. `app-orchestration-slm`, si se arranca, responde de forma autónoma a las peticiones de salud, flota y descubrimiento; la intermediación de Tier B en sí permanece deshabilitada hasta que una licencia válida quede incrustada en una imagen recompilada.

## Verificación

```
curl http://<host>:<puerto-totebox>/healthz       # os-totebox
curl http://<host>:<puerto-orquestacion>/healthz  # app-orchestration-slm
curl http://<host>:<puerto-orquestacion>/readyz   # estado de licencia / flota / circuito
```

## Reversión

Detenga el proceso de QEMU. El disco persistente (`persistent.raw`) no se ve afectado al detener el invitado — reejecutar el mismo comando de arranque reanuda desde el mismo estado acumulado. Para descartar el estado acumulado por completo, elimine el propio archivo de disco persistente y cree uno nuevo (Paso 1); no existe mecanismo de reinicio parcial más allá de eso.

## Limitaciones conocidas, a fecha de envío (2026-08-03)

- No hay mecanismo de actualización automatizada — un cambio de configuración implica una recompilación y una sustitución completa de la imagen, no una edición en vivo.
- Estas imágenes no han pasado por una revisión de seguridad a escala de cliente; trátelas como una versión temprana.
- El entrenamiento real a escala de GPU requiere su propio backend de cómputo Yo-Yo — las imágenes no incluyen uno.

## Próximos pasos

- [[deploy-knowledge-instance]] — despliegue el motor que sirve el wiki, un asunto independiente de estas imágenes de appliance
- [[configure-doorman]] — configure el gateway de inferencia una vez que su despliegue esté en funcionamiento
- [[authenticate-binary-downloads]] — verifique la firma de una imagen descargada antes de arrancarla

## Véase también

- [[deployment-patterns]] — patrones de configuración de gateway y topologías de despliegue
- [[edge-deployment]] — arquitectura de instancia edge y modelo de conectividad
- [[software-distribution-substrate]] — cómo se entregan las versiones de binarios firmados
- [[authenticate-binary-downloads]] — verifica el binario antes de ejecutarlo
- [[configure-doorman]] — configura el gateway de inferencia después de que el despliegue esté en funcionamiento
