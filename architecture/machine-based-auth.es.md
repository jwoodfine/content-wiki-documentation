---
schema: foundry-doc-v1
title: "Autorización basada en hardware"
slug: machine-based-auth
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
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

La autorización basada en hardware elimina el secreto memorizable. El acceso es un emparejamiento criptográfico de dos piezas de hardware físico — el par es el permiso. Cuando un dispositivo solicita acceso, ambos extremos demuestran posesión de material clave complementario; si el par se verifica, la conexión se forma; si no, las máquinas son mutuamente invisibles. Este modelo se denomina **Seguridad Geométrica**: el acceso está definido por la topología de los emparejamientos activos, no por la transmisión de secretos compartidos. Una máquina que no está emparejada no puede conectarse, independientemente de lo que sepa o presente.

Como la autorización se vincula al hardware y no a un secreto memorizado, no hay tabla de usuarios que vulnerar, no hay formulario de inicio de sesión que suplantar y no hay contraseña que restablecer. La revocación es física: el emparejamiento se corta en la máquina, y toda la clase de ataques de robo remoto de credenciales queda eliminada por estructura, no por política.

Para un comprador regulado la consecuencia es concreta. Una clase de ataque desaparece, y cada evento de acceso es atribuible a un hardware específico en el libro de auditoría. Este artículo cubre cómo funcionan los emparejamientos, los cuatro tipos, las ventajas estructurales sobre las contraseñas y la relación con las capas [[diode-standard|Diodo]] y de auditoría.

> **Dirección planificada — acceso nativo anfitrión a través de internet.** Está previsto que os-console se ejecute de forma nativa en el equipo del operador y se empareje con un Archivo Totebox remoto a través de internet público. El transporte previsto es TLS mutuo hacia un endpoint Totebox verificado, con la autorización basada en máquinas sin cambios como límite de acceso. La dirección de refuerzo planificada incluye la revocación de emparejamientos y certificados de dispositivo de corta duración. *Nota de honestidad:* la ruta actual a través de internet utiliza un túnel de reenvío SSH que aún no verifica la identidad del servidor remoto, por lo que la propiedad de extremo a extremo — el proveedor no puede leer los datos del operador en tránsito — es **prevista pero aún no entregada** en ese salto; se confirma una vez que el TLS mutuo verificado esté disponible. Véase `BRIEF-os-console-rebuild-2030.md` Capa 1.

## Infraestructura y aplicación: dos capas independientes

La MBA opera en la capa de aplicación, por encima e independientemente de cualquier infraestructura de red. Esta separación es central en la arquitectura.

La [[ppn-mesh-architecture|Red Privada de PointSav]] — la malla WireGuard que conecta los nodos de flota — proporciona el transporte en el que se ejecutan los servicios `os-*`. La pertenencia a la red significa que una máquina puede alcanzar otras máquinas en la malla. No otorga acceso a lo que esas máquinas alojan. Un nodo en la PPN sin emparejamientos MBA puede alcanzar la red; no puede abrir ningún archivo.

Dos capas de seguridad independientes protegen una conexión completa `os-console` → `os-totebox`:

**Capa 1 — Pertenencia a la red (PPN):** La máquina que se conecta debe ser un par WireGuard registrado. El tráfico de red de pares no registrados se descarta en la capa de red.

**Capa 2 — Emparejamiento de aplicación (MBA):** El servicio `os-*` que se conecta debe presentar una huella de clave pública registrada a `system-gateway-mba`, el componente de pasarela a nivel de aplicación que se ejecuta en el servicio de destino. Si no existe ningún registro de emparejamiento para esa huella, la conexión se rechaza — incluso si la capa de red permitió el tráfico.

Una máquina puede estar en la PPN sin ningún emparejamiento MBA. Puede alcanzar la red; no puede abrir ninguna puerta. Esta es la frontera de soberanía: la parte que posee la infraestructura de red no obtiene acceso a nivel de aplicación a los datos que se ejecutan en ella.

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

El emparejamiento INPUT es el predeterminado y el más potente: el propietario de un Totebox tiene plena agencia por defecto, y las restricciones son degradaciones deliberadas, no configuraciones predeterminadas.

## Por qué supera a las contraseñas

Tres ventajas estructurales se siguen de reemplazar las contraseñas con emparejamientos.

**Sin base de datos central que vulnerar.** No existe ninguna tabla de usuarios en ninguna parte de la arquitectura. Una vulneración exitosa de cualquier componente no produce material de credenciales útil en otro lugar.

**Sin superficie de phishing.** No se puede engañar a un operador para que escriba un emparejamiento en un formulario de inicio de sesión falso, porque un emparejamiento nunca se escribe. Lo demuestra criptográficamente el propio hardware.

**Revocación física.** Cuando el acceso de un operador debe terminar, el emparejamiento se corta a nivel de máquina. Una copia conservada del binario es inerte sin el material clave; no hay contraseña que restablecer.

## La disciplina de límite

El emparejamiento por sí solo no concede acceso a los datos. Concede la capacidad de intentar el acceso. El [[diode-standard|Estándar Diodo]] rige lo que fluye a través de un par establecido; el libro de auditoría registra cada comando y cada respuesta. El par es el prerrequisito; el Diodo y el [[worm-ledger-design|libro mayor WORM]] son las puertas.

La combinación — emparejamiento como acceso, Diodo como dirección, auditoría como registro — hace que el sistema sea auditable de extremo a extremo, sin ninguna política de rotación de contraseñas.

## Conexiones arquitectónicas

La autorización basada en hardware se conecta a otras tres capas arquitectónicas.

- **[[sel4-microkernel-substrate|Micronúcleo seL4]]** — el núcleo aplica que los tokens de capacidad no pueden ser falsificados por software que se ejecuta en privilegio de usuario.
- **[[capability-based-security|Seguridad basada en capacidades]]** — el gestor de capacidades emite y revoca tokens vinculados al hardware; el modelo de control de acceso depende de la vinculación al hardware para sus garantías.
- **[[worm-ledger-design|Libro mayor WORM]]** — cada evento de autorización se registra en el libro de solo adición, un registro verificable externamente de qué hardware accedió a qué recurso y cuándo.
- **`system-gateway-mba`** — el crate de pasarela a nivel de aplicación que aplica los registros de emparejamiento en cada frontera de servicio `os-*`; el componente que comprueba las huellas de claves entrantes contra el registro de emparejamientos y rechaza las conexiones sin un registro coincidente.

## Por qué se rechazó service-auth

Los primeros diseños consideraron `service-auth`, modelado en un servicio de directorio tradicional, como proveedor de identidad. La decisión se revirtió: un servicio de directorio se estructura en torno a usuarios, contraseñas y jerarquías de grupos — exactamente el modelo que [[pointsav-overview|PointSav]] está reemplazando. `service-pairing` se creó como la alternativa deliberada, y `service-auth` se eliminó de la arquitectura antes de escribir código. Véase [[pairing-as-permission|emparejamiento como permiso]].

## Véase también

- [[diode-standard]] — el flujo de comandos unidireccional que rige lo que pasa a través de un par establecido
- [[worm-ledger-design]] — el libro mayor de solo adición que registra cada evento de autorización
- [[sel4-microkernel-substrate]] — el micronúcleo seL4 que aplica la integridad de los tokens de capacidad
- [[compliance-and-continuous-disclosure]] — cómo la autorización vinculada al hardware apoya el cumplimiento de prueba continua
- [[deployment-patterns]] — cómo el emparejamiento MBA se aplica en las seis configuraciones de despliegue canónicas
- [[ppn-mesh-architecture]] — la capa de infraestructura de malla WireGuard en la que se ejecutan los servicios `os-*`; la MBA opera por encima e independientemente de la PPN
