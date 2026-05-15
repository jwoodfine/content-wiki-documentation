---
schema: foundry-doc-v1
title: "Autorización Basada en Hardware"
slug: machine-based-auth
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: machine-based-auth.md
short_description: "La autorización basada en hardware reemplaza las estructuras de usuario y contraseña con el emparejamiento criptográfico del hardware físico — el par es el permiso."
cites: []
references:
 - id: 1
 text: "Perrin, T. 'The Noise Protocol Framework.' noiseprotocol.org, 2016."
 url: "https://noiseprotocol.org/noise.html"
 - id: 2
 text: "Donenfeld, J. A. 'WireGuard: Next Generation Kernel Network Tunnel.' NDSS Symposium, 2017."
 url: "https://www.ndss-symposium.org/ndss2017/ndss-2017-programme/wireguard-next-generation-kernel-network-tunnel/"
---

La autorización basada en hardware reemplaza las estructuras de nombre de usuario y contraseña con el emparejamiento criptográfico del hardware físico — el par es el permiso. Cuando un dispositivo solicita acceso, ambos extremos del par demuestran posesión de material clave complementario; si el par se verifica, la conexión se establece; si no, las máquinas son mutuamente invisibles. Dado que la autorización está vinculada al hardware y no a un secreto memorizado, toda la clase de ataques de robo remoto de credenciales — phishing, adivinación de contraseñas e ingeniería social — queda estructuralmente eliminada. Este artículo cubre cómo funcionan los emparejamientos, los cuatro tipos de emparejamiento, las ventajas estructurales sobre las contraseñas y la relación con las capas [[diode-standard|Diodo]] y de auditoría.

## Cómo funciona un emparejamiento

Un emparejamiento es un protocolo criptográfico entre dos máquinas. Los dos extremos del par poseen material de clave pública/privada complementario. Cuando un [[console-os|Libro Mayor de Comandos]] se conecta a un [[totebox-os|Totebox]], ambos lados demuestran posesión de la clave correspondiente. Si el par se verifica, la conexión se establece. Si no, las máquinas son invisibles entre sí.

`service-pairing` gestiona estos emparejamientos utilizando Noise Protocol [^1] y claves de estilo WireGuard [^2], derivadas de la atestación de hardware donde la plataforma subyacente lo admite.

| Propiedad | Comportamiento |
|---|---|
| Autenticación | La clave de emparejamiento en sí misma — no se transmite ni almacena ninguna contraseña |
| Autorización | La presencia del emparejamiento; el permiso es el par |
| Revocación | El emparejamiento se corta en uno o ambos extremos; las máquinas se vuelven mutuamente invisibles |
| Vinculación al hardware | Donde es posible, la clave privada está sellada en el enclave de hardware del equipo |

## Los cuatro tipos de emparejamiento

Un [[totebox-os|Totebox]] reconoce cuatro tipos de emparejamiento, distinguidos por la relación entre los extremos del par y los datos:

| Emparejamiento | Extremo | Acceso | Función soberana |
|---|---|---|---|
| ADMIN | Máquina principal del propietario ↔ Totebox | Absoluto | Clave maestra para el control de VM y hardware, migración y gestión de claves |
| INPUT | Máquina de uso diario del operador ↔ Totebox | Lectura / Escritura | El estado predeterminado — plena agencia sobre datos personales, correo y archivos |
| USER | Máquina de acceso restringido ↔ Totebox | Solo lectura | Consultar los datos sin modificarlos — auditores, asesores |
| INTERFACE | Agregador de orquestación ↔ Totebox | Solo metadatos | Visibilidad de la flota de alto nivel sin acceso a registros individuales |

El emparejamiento INPUT es el predeterminado y el más potente. El propietario del Totebox tiene plena agencia por defecto; las restricciones son degradaciones deliberadas, no configuraciones predeterminadas.

## Por qué supera a las contraseñas

Tres ventajas estructurales emergen al reemplazar las contraseñas con emparejamientos:

**Sin base de datos central que vulnerar.** No existe ninguna "tabla de usuarios" en ninguna parte de la arquitectura. Una vulneración exitosa de cualquier componente no produce material de credenciales útil en otros lugares.

**Sin superficie de phishing.** Un operador no puede ser engañado para que escriba su emparejamiento en un formulario de inicio de sesión falso porque el emparejamiento nunca se escribe. Lo demuestra criptográficamente el propio hardware.

**Revocación física.** Cuando se debe eliminar el acceso de un operador, el emparejamiento se corta a nivel de máquina. Aunque conserve una copia del binario de software, carece del material clave para conectarse. No hay contraseña que restablecer; la máquina simplemente deja de estar emparejada.

## La disciplina de límite

El emparejamiento por sí solo no concede acceso a los datos. Concede la capacidad de intentar el acceso. El [[diode-standard|Estándar Diodo]] rige lo que fluye a través de cualquier par establecido. El libro de auditoría registra cada comando y cada respuesta. El par es el prerrequisito; el Diodo y el [[worm-ledger-design|libro mayor WORM]] son las puertas.

La combinación — emparejamiento como acceso, Diodo como dirección, auditoría como registro — hace que el sistema sea auditable de extremo a extremo sin requerir nunca una política de rotación de contraseñas.

## Conexiones arquitectónicas

La autorización basada en hardware se conecta a otras tres capas arquitectónicas:

- **[[sel4-microkernel-substrate|Micronúcleo seL4]]** — el núcleo aplica que los tokens de capacidad no pueden ser falsificados por software que se ejecuta en privilegio de usuario.
- **Seguridad basada en capacidades** — el gestor de capacidades emite y revoca tokens vinculados al hardware; el modelo de control de acceso depende de la vinculación al hardware para sus garantías de seguridad.
- **[[worm-ledger-design|Libro mayor WORM]]** — cada evento de autorización se registra en el libro de solo adición, proporcionando un registro verificable externamente de qué hardware accedió a qué recursos y cuándo.

## Por qué se rechazó service-auth

Los primeros diseños consideraron `service-auth`, modelado en un servicio de directorio tradicional, como proveedor de identidad. La decisión se revirtió: un servicio de directorio tradicional está estructurado en torno a usuarios, contraseñas y jerarquías de grupos — exactamente el modelo que PointSav está reemplazando. `service-pairing` fue creado como alternativa deliberada, y `service-auth` fue eliminado de la arquitectura antes de que se escribiera ningún código.

## Véase también

- [[diode-standard]] — el flujo de comandos unidireccional que rige lo que pasa a través de un par establecido
- [[worm-ledger-design]] — el libro mayor de solo adición que registra cada evento de autorización
- [[sel4-microkernel-substrate]] — el micronúcleo seL4 que aplica la integridad de los tokens de capacidad
- [[compliance-and-continuous-disclosure]] — cómo la autorización vinculada al hardware apoya el cumplimiento de prueba continua
- [[deployment-patterns]] — cómo el emparejamiento MBA se aplica en las seis configuraciones de despliegue canónicas
