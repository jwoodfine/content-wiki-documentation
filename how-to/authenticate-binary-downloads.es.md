---
schema: foundry-doc-v1
title: "Cómo autenticar descargas de binarios"
slug: authenticate-binary-downloads
category: how-to
content_type: how-to
type: how-to
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: authenticate-binary-downloads.md
---

El punto de distribución privado de PointSav en `software.pointsav.com` emite versiones de binarios firmadas con Ed25519. Cada descarga se verifica contra la clave pública del editor antes de ejecutar el binario. Esta guía cubre la solicitud de un token de licencia, la descarga de una versión y la verificación de la firma.

Para la arquitectura detrás del sistema de distribución, consulta [[private-git-paid-customer-endpoint]] y [[software-distribution-substrate]].

## Antes de empezar

Necesitas:

- Una cuenta verificada en `software.pointsav.com`
- Una licencia activa para el producto que deseas descargar
- Un servidor Linux o macOS con `curl` instalado

## Paso 1: Obtén tu token de licencia

Inicia sesión en `software.pointsav.com` y navega a **Licencias**. Cada
licencia activa muestra un token firmado con Ed25519 en el formato
`psv1_<producto>_<ulid>.<firma>`. Copia el token completo.

El token codifica el identificador del producto, la fecha de vencimiento y un
vínculo criptográfico con la clave de tu cuenta. El punto de distribución
devuelve `401` para un token vencido y `403` si el token no cubre el producto
solicitado.

## Paso 2: Descarga el archivo de la versión

Pasa el token de licencia como credencial bearer en la solicitud de descarga:

```shell
curl -fsSL \
  -H "Authorization: Bearer <tu-token-de-licencia>" \
  "https://software.pointsav.com/releases/<producto>/<versión>/linux-x86_64.tar.gz" \
  -o release.tar.gz
```

Reemplaza `<producto>` y `<versión>` con los valores que aparecen en la
página **Versiones** de tu licencia. Las plataformas disponibles aparecen
junto a cada versión.

## Paso 3: Descarga el archivo de firma separado

Cada archivo de versión tiene un archivo `.sig` acompañante firmado con la
clave privada Ed25519 del editor:

```shell
curl -fsSL \
  -H "Authorization: Bearer <tu-token-de-licencia>" \
  "https://software.pointsav.com/releases/<producto>/<versión>/linux-x86_64.tar.gz.sig" \
  -o release.tar.gz.sig
```

## Paso 4: Importa la clave pública del editor

La clave de firma está disponible en una ruta conocida del punto de
distribución:

```shell
curl -fsSL \
  "https://software.pointsav.com/.well-known/pointsav-signing-key.pub" \
  -o pointsav-signing-key.pub
```

Confirma que la huella digital de la clave coincide con el valor publicado en
las notas de la versión que estás descargando antes de continuar.

## Paso 5: Verifica la firma Ed25519

Crea un archivo de firmantes autorizados y ejecuta `ssh-keygen -Y verify`:

```shell
echo "releases@pointsav.com $(cat pointsav-signing-key.pub)" > allowed_signers

ssh-keygen -Y verify \
  -f allowed_signers \
  -I releases@pointsav.com \
  -n release \
  -s release.tar.gz.sig \
  < release.tar.gz
```

Una verificación exitosa imprime:
`Good "release" signature for releases@pointsav.com`

Si el comando imprime `Signature verification failed`, el archivo ha sido
modificado durante la transferencia o el archivo de firma no corresponde al
archivo descargado. No continúes — vuelve a descargar ambos archivos y
verifica de nuevo antes de usar el binario.

## Paso 6: Extrae y ejecuta el binario

```shell
tar -xzf release.tar.gz
chmod +x <producto>
./<producto> --version
```

El binario valida su token de licencia al iniciar. Si el token ha vencido
desde la descarga, el proceso termina con un mensaje que indica la fecha exacta
de vencimiento. Renueva el token en `software.pointsav.com` y reinicia.

## Véase también

- [[private-git-paid-customer-endpoint]] — la arquitectura del punto de conexión para clientes de pago
- [[software-distribution-substrate]] — el sustrato de distribución de software
- [[machine-based-auth]] — cómo se autoriza el acceso al punto de distribución
