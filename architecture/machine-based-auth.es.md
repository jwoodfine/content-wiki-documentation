---
schema: foundry-doc-v1
title: "Autorización basada en hardware"
slug: machine-based-auth
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: machine-based-auth.md
short_description: "La autorización basada en hardware reemplaza las estructuras de usuario y contraseña con el emparejamiento criptográfico del hardware físico — el par es el permiso, y toda una clase de robo remoto de credenciales queda eliminada por estructura."
cites: []
references:
 - id: 1
 text: "Perrin, T. 'The Noise Protocol Framework.' noiseprotocol.org, 2016."
 url: "https://noiseprotocol.org/noise.html"
 - id: 2
 text: "Donenfeld, J. A. 'WireGuard: Next Generation Kernel Network Tunnel.' NDSS Symposium, 2017."
 url: "https://www.ndss-symposium.org/ndss2017/ndss-2017-programme/wireguard-next-generation-kernel-network-tunnel/"
---

Cada contraseña es un secreto que una persona debe recordar y, por tanto, un secreto que un atacante puede tomar. Phishing, adivinación de contraseñas, relleno de credenciales, ingeniería social — toda la clase del robo remoto de credenciales existe porque la credencial es algo que un humano sabe.

La autorización basada en hardware elimina el secreto memorizable. <!--claim id=pair-is-permission confidence=structural cites=[]-->El acceso es un emparejamiento criptográfico de dos piezas de hardware físico — el par es el permiso. Cuando un dispositivo solicita acceso, ambos extremos demuestran posesión de material clave complementario; si el par se verifica, la conexión se forma; si no, las máquinas son mutuamente invisibles.<!--/claim-->

Como la autorización se vincula al hardware y no a un secreto memorizado, no hay tabla de usuarios que vulnerar, no hay formulario de inicio de sesión que suplantar y no hay contraseña que restablecer. <!--claim id=attack-class-eliminated confidence=structural cites=[]-->La revocación es física: el emparejamiento se corta en la máquina, y toda la clase de ataques de robo remoto de credenciales queda eliminada por estructura, no por política.<!--/claim-->

Para un comprador regulado la consecuencia es concreta. Una clase de ataque desaparece, y cada evento de acceso es atribuible a un hardware específico en el libro de auditoría. Este artículo cubre cómo funcionan los emparejamientos, los cuatro tipos, las ventajas estructurales sobre las contraseñas y la relación con las capas [[diode-standard|Diodo]] y de auditoría.

## Cómo funciona un emparejamiento

Un emparejamiento es un protocolo criptográfico entre dos máquinas. Los dos extremos poseen material de clave pública y privada complementario. Cuando un [[console-os|Libro Mayor de Comandos]] se conecta a un [[totebox-os|Totebox]], ambos lados demuestran posesión de la clave correspondiente. Si el par se verifica, la conexión se establece. Si no, las máquinas son invisibles entre sí.

`service-pairing` gestiona estos emparejamientos con el Noise Protocol [^1] y claves de estilo WireGuard [^2], derivadas de la atestación de hardware donde la plataforma subyacente lo admite.

| Propiedad | Comportamiento |
|---|---|
| Autenticación | La clave de emparejamiento en sí — no se transmite ni almacena ninguna contraseña |
| Autorización | La presencia del emparejamiento; el permiso es el par |
| Revocación | El emparejamiento se corta en uno o ambos extremos; las máquinas se vuelven mutuamente invisibles |
| Vinculación al hardware | Donde es posible, la clave privada está sellada en el enclave de hardware del equipo |

## Los cuatro tipos de emparejamiento

Un [[totebox-os|Totebox]] reconoce cuatro tipos de emparejamiento, distinguidos por la relación entre los extremos del par y los datos.

| Emparejamiento | Extremo | Acceso | Función |
|---|---|---|---|
| ADMIN | Máquina principal del propietario ↔ Totebox | Absoluto | Clave maestra para el control de VM y hardware, migración y gestión de claves |
| INPUT | Máquina de uso diario del operador ↔ Totebox | Lectura / escritura | El estado predeterminado — plena agencia sobre datos personales, correo y archivos |
| USER | Máquina de acceso restringido ↔ Totebox | Solo lectura | Consultar los datos sin modificarlos — auditores, asesores |
| INTERFACE | Agregador de orquestación ↔ Totebox | Solo metadatos | Visibilidad de la flota sin acceso a registros individuales |

<!--claim id=input-default confidence=structural cites=[]-->El emparejamiento INPUT es el predeterminado y el más potente: el propietario de un Totebox tiene plena agencia por defecto, y las restricciones son degradaciones deliberadas, no configuraciones predeterminadas.<!--/claim-->

## Por qué supera a las contraseñas

Tres ventajas estructurales se siguen de reemplazar las contraseñas con emparejamientos.

<!--claim id=no-central-db confidence=structural cites=[]-->**Sin base de datos central que vulnerar.** No existe ninguna tabla de usuarios en ninguna parte de la arquitectura. Una vulneración exitosa de cualquier componente no produce material de credenciales útil en otro lugar.<!--/claim-->

<!--claim id=no-phishing confidence=structural cites=[]-->**Sin superficie de phishing.** No se puede engañar a un operador para que escriba un emparejamiento en un formulario de inicio de sesión falso, porque un emparejamiento nunca se escribe. Lo demuestra criptográficamente el propio hardware.<!--/claim-->

<!--claim id=physical-revocation confidence=structural cites=[]-->**Revocación física.** Cuando el acceso de un operador debe terminar, el emparejamiento se corta a nivel de máquina. Una copia conservada del binario es inerte sin el material clave; no hay contraseña que restablecer.<!--/claim-->

## La disciplina de límite

El emparejamiento por sí solo no concede acceso a los datos. Concede la capacidad de intentar el acceso. El [[diode-standard|Estándar Diodo]] rige lo que fluye a través de un par establecido; el libro de auditoría registra cada comando y cada respuesta. El par es el prerrequisito; el Diodo y el [[worm-ledger-design|libro mayor WORM]] son las puertas.

La combinación — emparejamiento como acceso, Diodo como dirección, auditoría como registro — hace que el sistema sea auditable de extremo a extremo, sin ninguna política de rotación de contraseñas.

## Conexiones arquitectónicas

La autorización basada en hardware se conecta a otras tres capas arquitectónicas.

- **[[sel4-microkernel-substrate|Micronúcleo seL4]]** — el núcleo aplica que los tokens de capacidad no pueden ser falsificados por software que se ejecuta en privilegio de usuario.
- **[[capability-based-security|Seguridad basada en capacidades]]** — el gestor de capacidades emite y revoca tokens vinculados al hardware; el modelo de control de acceso depende de la vinculación al hardware para sus garantías.
- **[[worm-ledger-design|Libro mayor WORM]]** — cada evento de autorización se registra en el libro de solo adición, un registro verificable externamente de qué hardware accedió a qué recurso y cuándo.

## Por qué se rechazó service-auth

<!--claim id=service-auth-rejected confidence=structural cites=[]-->Los primeros diseños consideraron `service-auth`, modelado en un servicio de directorio tradicional, como proveedor de identidad. La decisión se revirtió: un servicio de directorio se estructura en torno a usuarios, contraseñas y jerarquías de grupos — exactamente el modelo que [[pointsav-overview|PointSav]] está reemplazando.<!--/claim--> `service-pairing` se creó como la alternativa deliberada, y `service-auth` se eliminó de la arquitectura antes de escribir código. Véase [[pairing-as-permission|emparejamiento como permiso]].

## Véase también

- [[diode-standard]] — el flujo de comandos unidireccional que rige lo que pasa a través de un par establecido
- [[worm-ledger-design]] — el libro mayor de solo adición que registra cada evento de autorización
- [[sel4-microkernel-substrate]] — el micronúcleo seL4 que aplica la integridad de los tokens de capacidad
- [[compliance-and-continuous-disclosure]] — cómo la autorización vinculada al hardware apoya el cumplimiento de prueba continua
- [[deployment-patterns]] — cómo el emparejamiento MBA se aplica en las seis configuraciones de despliegue canónicas
