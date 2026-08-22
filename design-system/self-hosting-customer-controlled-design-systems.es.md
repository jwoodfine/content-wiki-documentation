---
schema: foundry-doc-v1
title: "Autoalojar un sistema de diseño, y por qué es distinto de usar los tokens"
slug: self-hosting-customer-controlled-design-systems
short_description: "Explica las dos ofertas diferenciadas del Sistema de Diseño PointSav — usar directamente los datos de tokens bajo Apache-2.0, que no requiere nada, y por separado autoalojar el motor de publicación para operar el sistema de diseño propio y distinto de otra organización — incluyendo el procedimiento real de bifurcación en cinco pasos, la superficie de configuración de tres variables, la gobernanza basada en git y los límites precisos de licencia entre datos de tokens, código del servidor y texto del artículo."
category: design-system
type: topic
content_type: topic
quality: complete
index_group: token-concepts-and-tooling
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: self-hosting-customer-controlled-design-systems.md
cites: []
---

El Sistema de Diseño PointSav hace dos ofertas, dirigidas a lectores
distintos. La primera — la principal — son los propios datos de tokens:
decisiones de color, tipografía, espaciado, movimiento, voz de contenido y
formato documental publicadas como JSON en formato DTCG del W3C bajo
Apache-2.0. Cualquiera puede usarlos como los equipos usan Carbon de IBM o
Material de Google: incorporar el grafo de tokens a su propio proceso de
construcción y seguir adelante. No se requiere nada más: ni cuenta, ni
servidor, ni bifurcación, ni relación alguna con PointSav.

La segunda oferta es autoalojar el motor que sirve este sitio. Esa oferta no
es una versión ampliada de la primera, y no es una manera de replicar los
tokens de PointSav en hardware propio. Está pensada para una organización
distinta que quiere construir y operar su **propio** sistema de diseño — sus
propios tokens, su propia marca, su propio dominio — sobre la misma
maquinaria de publicación que opera PointSav, abordando la misma brecha de
mercado de precios de nivel empresarial que describe
[[design-philosophy|la filosofía del sistema de diseño]] para el propio
sustrato de PointSav. Las dos ofertas son separables por diseño, y
confundirlas tergiversa ambas. Este artículo explica cada una en sus propios
términos, y dónde pasa exactamente la línea entre ellas.

## Usar los tokens no requiere nada

El problema del *formato* de los tokens de diseño está resuelto. El Design
Tokens Community Group del W3C publicó la primera versión estable de su
Format Module en octubre de 2025, y el formato está implementado en las
principales herramientas de autoría y construcción. El grafo de tokens de
PointSav — más de 200 tokens hoja resueltos entre los niveles primitivo,
semántico y de tema oscuro, en crecimiento junto con el sistema — se
publica en ese formato, bajo
Apache-2.0, en un repositorio git público.

Esa es toda la transacción. Un equipo que quiere los tokens clona o descarga
los datos, los resuelve con las herramientas que ya usa, y publica. Los
tokens no llaman a casa, no requieren que el servidor de PointSav exista, y
no imponen ninguna obligación más allá de los términos de atribución de
Apache-2.0. Si design.pointsav.com desapareciera mañana, cada copia de los
datos de tokens seguiría funcionando, porque los datos nunca estuvieron
acoplados al servicio que los publica.

Si eso es lo que vino a buscar, puede dejar de leer aquí.

## Qué es realmente el autoalojamiento

El autoalojamiento atiende un problema distinto: no "cómo consumo un grafo de
tokens", sino "cómo gobierna, versiona, documenta y publica mi organización
su propio grafo de tokens a lo largo del tiempo". El software que hace esto —
la capa que ocupan comercialmente zeroheight, Supernova, Knapsack y
plataformas similares — se entrega casi exclusivamente como software como
servicio alojado por el proveedor, lo que exige que los datos de tokens del
cliente residan en la infraestructura del proveedor. El zeroheight Design
Systems Report 2026 encuentra que solo el 40% de los equipos encuestados
tiene siquiera una cadena automatizada de tokens; el resto sincroniza a
mano. Y para una clase específica de comprador — servicios financieros,
jurídicos, gobierno — el alojamiento por terceros no es solo incómodo sino
con frecuencia descalificante, porque la postura de cumplimiento que
gobierna dónde pueden residir los artefactos de una organización rara vez
contempla una excepción para los activos de diseño. La investigación sobre
dependencia de proveedor en la nube documenta la asimetría de fondo:
Opara-Martins, Sahandi y Tian, encuestando a 114 profesionales empresariales
en 2016, identificaron la portabilidad de datos y la incompatibilidad de
integración como los riesgos dominantes de dependencia una vez que los
activos pasan a infraestructura controlada por el proveedor.

La oferta de autoalojamiento es el motor detrás de este sitio, operado por
otra organización para el sistema propio de esa organización. La empresa que
bifurca no hereda las decisiones de marca de PointSav — las reemplaza. Lo
que hereda es la maquinaria: la estructura del vault, el renderizado de la
galería de tokens, la cadena de exportación resuelta, los puntos de acceso
legibles por máquina y el modelo de gobernanza. Los tokens propios de
PointSav son, para un cliente que se autoaloja, contenido de ejemplo.

## El mecanismo: bifurcar y ejecutar

El procedimiento documentado tiene cinco pasos: hacer una bifurcación (fork)
del repositorio público; clonar el fork en su propio servidor; editar el
directorio de temas del vault para declarar las anulaciones primitivas de su
marca; ejecutar el binario de servicio apuntado a su directorio de vault; y
poner delante su propio proxy inverso y certificado TLS, bajo su propio
dominio.

Toda la superficie de configuración de arrendamiento son tres variables de
entorno. `DESIGN_VAULT_DIR` nombra la ruta del sistema de archivos a su
vault. `DESIGN_TENANT` nombra su marca, coincidiendo con un nombre de
archivo de tema dentro de ese vault. `DESIGN_BIND` nombra la dirección en la
que escucha el proceso. Un binario sirve el vault de un arrendatario por
proceso — no hay base de datos multiarrendatario ni infraestructura
compartida entre el despliegue de una organización y el de otra. Nada en el
procedimiento transmite sus datos de tokens o temas a PointSav, y la
instancia en ejecución no hace ninguna llamada a la infraestructura de
PointSav en tiempo de solicitud. Cambiar de proveedor, o dejar el despliegue
completamente fuera de línea para una auditoría, significa mover un
directorio y reiniciar un proceso, porque no hay paso de exportación de
datos: los datos nunca vivieron en otro lugar que su propio repositorio.

La gobernanza sale del mismo lugar. Las plataformas alojadas ofrecen
permisos de edición, historial de versiones y revisión de cambios mediante
controles de capa de aplicación sobre una base de datos operada por el
proveedor; el modelo de bifurcar-y-ejecutar ofrece el equivalente mediante
el control de versiones del propio cliente. Los cambios de tokens son
commits, los derechos de edición son protección de ramas, el historial es el
registro de git, la revisión es un pull request — infraestructura que un
comprador regulado ya opera y ya ha auditado.

## Qué licencia aplica a qué

Las dos ofertas también se separan con nitidez en la frontera de licencias,
y aquí la precisión importa:

- **Datos de tokens y componentes — Apache-2.0.** El JSON DTCG, las recetas
  de componentes y los archivos de investigación del repositorio del sistema
  de diseño. Es la capa que se consume directamente, y la capa que un fork
  reemplaza con su propio contenido.
- **Código del servidor — AGPL-3.0-or-later.** El motor de servicio
  (`app-privategit-design` en el monorepo de PointSav). Ejecutarlo sin
  modificaciones para la propia organización no conlleva ninguna carga
  inusual; una organización que modifica el servidor y lo ofrece a usuarios
  a través de una red asume la obligación de la Sección 13 de la AGPL de
  ofrecer a esos usuarios el código fuente modificado. Para las
  organizaciones que no pueden aceptar esa obligación, la matriz de
  licencias del proyecto ratifica un nivel comercial alternativo compatible
  con Apache; su presentación exacta a los clientes que se autoalojan aún
  está por definirse.
- **Este artículo — CC BY 4.0**, la licencia del wiki de documentación en el
  que se publica. El texto del artículo no es ni datos de tokens ni código
  del servidor, y ninguna de las tres licencias sustituye a las otras.

## Alcance y límites

Dicho con claridad: el procedimiento de bifurcación está documentado, y cada
uno de sus pasos usa herramientas ordinarias y verificables de forma
independiente — git, variables de entorno, una unidad de systemd, un proxy
inverso. Pero al momento de escribir, ninguna organización fuera de PointSav
ha ejecutado el procedimiento de principio a fin en producción; la propia
instancia de PointSav es el único despliegue. Toda afirmación de este
artículo sobre autoalojamiento externo es, por lo tanto, arquitectónica y
procedimental — un patrón que el sistema está construido para soportar y que
se prevé que soporte — no un informe de adopción observada por terceros. El
manuscrito de investigación que acompaña este artículo enuncia la misma
limitación, junto con un programa de falsación para las afirmaciones
implicadas, y este artículo prefiere publicar con ese estatus a la vista
antes que sugerir una base de clientes que no puede demostrar.

---

*Este artículo es material de contexto para los lectores de la documentación
del Sistema de Diseño PointSav que deciden cuál de las dos ofertas
necesitan. El manual operativo del procedimiento de bifurcación se mantiene
por separado como guía; el tratamiento con grado de investigación de la
arquitectura, incluidas sus hipótesis formales y limitaciones, es el
manuscrito acompañante sobre infraestructura de sistemas de diseño
controlada por el cliente.*
