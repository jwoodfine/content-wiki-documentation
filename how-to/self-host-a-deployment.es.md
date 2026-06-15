---
schema: foundry-doc-v1
title: "Cómo autoalojar un despliegue"
slug: self-host-a-deployment
category: how-to
content_type: how-to
type: how-to
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: self-host-a-deployment.md
---

Un despliegue de PointSav es una instancia nombrada y numerada de una configuración de gateway provisionada en infraestructura controlada por el operador. Cada despliegue ejecuta el mismo sustrato de distribución de software que el servicio alojado, con todos los datos y claves almacenados localmente. Esta guía cubre el provisionamiento de una nueva instancia de despliegue, la verificación de que el gateway inicia correctamente y su conexión a la plataforma central.

Para la arquitectura de despliegue, consulta [[deployment-patterns]] y [[edge-deployment]]. Para el modelo de distribución de software que suministra binarios firmados a tu instancia, consulta [[software-distribution-substrate]].

## Antes de empezar

Necesitas:

- Un servidor Linux con al menos 4 GB de RAM y 20 GB de disco disponible
- Una cuenta verificada en `software.pointsav.com` con una licencia de despliegue activa
- Un nombre de dominio o dirección IP estática para el punto de conexión del gateway
- Un certificado TLS y su clave privada para la dirección de enlace del gateway

## Paso 1: Descarga y verifica el binario del gateway

Sigue [[authenticate-binary-downloads]] para descargar y verificar la versión
del gateway para tu plataforma. Una vez verificada, instala el binario:

```shell
sudo mv pointsav-gateway /usr/local/bin/
sudo chmod +x /usr/local/bin/pointsav-gateway
pointsav-gateway --version
```

El indicador `--version` imprime el SHA del build junto al número de versión.
Confirma que coincide con la entrada de las notas de versión que descargaste.

## Paso 2: Crea los directorios del despliegue

```shell
sudo mkdir -p /etc/pointsav/gateway
sudo mkdir -p /var/lib/pointsav/data
```

Toda la configuración vive en `/etc/pointsav/gateway/`. Los datos en tiempo de
ejecución — el registro WORM, la caché local y el almacén de claves — se
escriben en `/var/lib/pointsav/data/`. Ambas rutas deben ser propiedad del
usuario de proceso que ejecutará el gateway.

## Paso 3: Escribe el manifiesto del despliegue

Crea `/etc/pointsav/gateway/manifest.toml`:

```toml
[deployment]
name          = "<nombre-de-tu-despliegue>"
instance      = 1
licence_token = "<tu-token-de-licencia>"

[gateway]
bind     = "0.0.0.0:443"
tls_cert = "/etc/pointsav/gateway/tls.crt"
tls_key  = "/etc/pointsav/gateway/tls.key"

[data]
root = "/var/lib/pointsav/data"
```

`name` debe coincidir con el nombre de despliegue registrado en
`software.pointsav.com`. `instance` es un número entero que distingue
múltiples despliegues de la misma configuración nombrada. Coloca tu
certificado TLS y clave privada en las rutas declaradas bajo `[gateway]`.

## Paso 4: Inicia el gateway

```shell
sudo -u <usuario-del-proceso> pointsav-gateway \
  --manifest /etc/pointsav/gateway/manifest.toml
```

Para producción, registra esto como un servicio systemd con
`Restart=on-failure`. El gateway registra en stderr; redirige al destino de
registro preferido en el archivo de unidad.

## Paso 5: Verifica que el gateway está en buen estado

```shell
curl -sk https://localhost/healthz
# esperado: {"status":"ok","deployment":"<nombre-de-tu-despliegue>-1"}
```

Si la respuesta es `{"status":"licence_error"}`, el token de licencia ha
vencido o el campo `name` no coincide con el nombre de despliegue registrado.
Renueva el token en `software.pointsav.com` y reinicia. Si la respuesta es un
rechazo de conexión, confirma que el gateway está en ejecución y que el puerto
de enlace está abierto en el firewall del servidor.

## Paso 6: Provisiona los módulos posteriores

Con el gateway en buen estado, provisiona los módulos relevantes para tu
patrón de despliegue — consulta [[deployment-patterns]] para el catálogo de
configuraciones disponibles. Para agregar capacidad de inferencia local,
configura el servicio Doorman a continuación: consulta [[configure-doorman]].

## Véase también

- [[deployment-patterns]] — patrones de configuración de gateway y topologías de despliegue
- [[edge-deployment]] — arquitectura de instancia edge y modelo de conectividad
- [[software-distribution-substrate]] — cómo se entregan las versiones de binarios firmados
- [[authenticate-binary-downloads]] — verifica el binario antes de ejecutarlo
- [[configure-doorman]] — configura el gateway de inferencia después de que el despliegue esté en funcionamiento
