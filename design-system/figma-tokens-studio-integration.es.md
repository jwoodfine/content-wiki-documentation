---
schema: foundry-doc-v1
title: "Figma y Tokens Studio: consumir los tokens del sistema de diseño en una herramienta de diseño"
slug: figma-tokens-studio-integration
short_description: "Cómo los diseñadores incorporan a Figma la exportación de tokens DTCG del Sistema de Diseño PointSav mediante la sincronización por URL del plugin Tokens Studio — una lectura de solo consulta desde el JSON alojado por el propio sistema, sin paso de exportación/importación — y por qué esa dirección de solo lectura es una característica de gobernanza, con una comparación honesta con Penpot."
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
paired_with: figma-tokens-studio-integration.md
cites: []
---

El Sistema de Diseño PointSav publica su conjunto completo de tokens como un
único archivo en el formato de intercambio del Design Tokens Community Group
(DTCG), la especificación del grupo comunitario del W3C cuyo Format Module
alcanzó su primera versión estable en octubre de 2025. Ese archivo no es un
artefacto de compilación enterrado en un repositorio; lo sirve el propio
sitio del sistema de diseño, en una URL estable, regenerado desde el mismo
registro que genera las páginas de documentación. Como la exportación usa el
formato de intercambio comunitario y no uno propietario, cualquier
herramienta que lea JSON DTCG puede consumirlo — y la consecuencia más
práctica de eso, para un equipo de diseño, es que los tokens pueden llevarse
directamente a Figma.

Esta es una vía documentada y en funcionamiento hoy, no un punto de hoja de
ruta. La propia guía de inicio para diseñadores del sistema de diseño la
registra en una línea: apuntar el plugin Tokens Studio al archivo de tokens
publicado. Este artículo explica qué significa esa línea, por qué la
integración tiene la forma que tiene y dónde están sus bordes.

## La vía, en concreto

Tokens Studio es un plugin de uso extendido para Figma, disponible en el
directorio de plugins de Figma Community, que gestiona tokens de diseño
dentro de un archivo de Figma y los aplica a los elementos del diseño. Dos
de sus capacidades documentadas sostienen esta integración:

- **Soporte del formato DTCG.** El plugin puede operar con tokens en formato
  W3C DTCG — la estructura con prefijo de signo de dólar `$value` / `$type`
  / `$description` que este sistema de diseño publica — seleccionable en la
  configuración del plugin. La documentación del plugin presenta esta opción
  de formato sin requisito de plan de pago.
- **Sincronización por URL.** El plugin puede apuntarse a un archivo JSON
  alojado y extraer los tokens desde él. Su documentación describe este
  proveedor como de solo lectura: el plugin obtiene los tokens y permite al
  diseñador aplicarlos a elementos de Figma, pero no escribe cambios de
  vuelta a la URL. A medida que los tokens del sistema de diseño cambian en
  el origen, el plugin muestra indicadores de actualización para que el
  archivo de Figma pueda ponerse al día. La documentación no declara
  ninguna restricción de plan de pago sobre este proveedor.

Conectando ambas: un diseñador instala el plugin, agrega la exportación de
tokens publicada del sistema de diseño como fuente de sincronización por URL
y extrae. Los valores de tokens de esta versión quedan entonces disponibles
dentro del archivo de Figma — sin ceremonia de exportación/importación, sin
reingreso manual de valores, sin una copia del conjunto de tokens mantenida
a mano. Ese es el mismo encuadre que usa el propio sitio del sistema de
diseño, y este artículo es el contexto detrás de él.

El plugin en sí es gratuito de instalar, y las dos capacidades de las que
depende esta vía están documentadas sin un nivel de pago asociado. Tokens
Studio vende funciones pro — entre ellas la sincronización remota
multi-archivo y el cambio de ramas — pero esta integración no las requiere.
Esa distinción se enuncia con cuidado a propósito: los precios del proveedor
son del proveedor y pueden cambiar, y la afirmación que aquí se hace es
sobre lo que dice su documentación al momento de escribir.

## Por qué solo lectura es la dirección correcta

Sería natural leer "solo lectura" como una limitación. Para este sistema de
diseño es el comportamiento correcto, y vale la pena defenderlo
explícitamente.

El conjunto de tokens se gobierna en un solo lugar: el repositorio del
sistema de diseño, donde los cambios se proponen, se revisan, se versionan y
se publican. El archivo DTCG publicado es un producto de esa gobernanza,
generado desde el mismo registro que alimenta el sitio de documentación y la
API para máquinas. Si una herramienta de diseño pudiera escribir valores de
tokens de vuelta, habría dos fuentes de verdad — el repositorio y el archivo
de Figma que haya empujado más recientemente — y cada consumidor aguas abajo
heredaría la ambigüedad.

La extracción de solo lectura da a los diseñadores exactamente la relación
que ya tienen los consumidores de código: suscribirse a los valores
publicados, trabajar con ellos y encauzar los cambios propuestos a través
del proceso de contribución del sistema, no alrededor de él. Un diseñador
que necesita cambiar un token presenta el cambio contra el sistema de
diseño; cuando el cambio entra y una versión se publica, cada archivo de
Figma suscrito extrae el mismo valor corregido que extrae cada compilación
de hojas de estilo. Un cambio, en el token, en todas partes — que es el
argumento completo a favor de los tokens.

## Penpot, como comparación

La misma guía de inicio nombra una segunda herramienta de diseño: Penpot, la
plataforma de diseño de código abierto, que soporta tokens de diseño de
forma nativa — sin plugin. La implementación de Penpot se adhiere al Format
Module del DTCG e importa JSON de tokens directamente, y para los equipos
que eligen herramienta de diseño por criterios de estándares abiertos ese
soporte nativo es un punto genuino a su favor. Una salvedad honesta
corresponde a su lado: al momento de escribir, la discusión de la comunidad
de Penpot registra que su exportación de tokens emite JSON al estilo de
Tokens Studio y no salida DTCG estricta de la revisión vigente, de modo que
el viaje de ida y vuelta de tokens desde Penpot aún no es tan limpio como la
importación hacia él. Para la dirección de consumo que este artículo
describe — el sistema publica, la herramienta se suscribe — esa salvedad no
afecta: la exportación del sistema de diseño es la fuente, y ambas
herramientas la leen.

Los usuarios de Sketch quedan cubiertos por la misma vía de plugin: Tokens
Studio también se distribuye para Sketch, y el mismo archivo publicado le
sirve.

## Licencias

Aquí aplican dos licencias, y se asocian a cosas distintas. Los datos de los
tokens — el archivo JSON DTCG al que un diseñador apunta Tokens Studio — se
publican bajo Apache-2.0, la convención compartida por los grandes sistemas
de diseño abiertos, de modo que consumirlo en una herramienta de diseño, una
cadena de compilación o un producto derivado conlleva los términos permisivos
de Apache-2.0. El texto de este artículo, como parte del wiki de
documentación, está licenciado CC BY 4.0 — una licencia de contenido que
exige atribución, distinta de la licencia de los datos. Llevar los tokens a
Figma involucra la primera; citar o republicar este artículo involucra la
segunda.

## Alcance y límites

Dicho con claridad: lo demostrado es el lado de la publicación — la
exportación DTCG existe, la sirve el sitio del sistema de diseño y es la vía
documentada para diseñadores — y las capacidades del plugin citadas se toman
de la documentación vigente del propio Tokens Studio, leída directamente y
no asumida. Este artículo no afirma un resultado de adopción medido, no
habla por las hojas de ruta de Tokens Studio ni de Penpot, y señala en lugar
de ocultar los dos bordes blandos: la URL pública canónica de la exportación
está en proceso de reconciliación entre la forma corta de la guía y la ruta
de paquetes del servidor, y los precios y límites de funciones de terceros
están verificados al 2026-07-10, no garantizados hacia adelante.

---

*Este artículo es material de contexto para diseñadores que encuentran por
primera vez la exportación de tokens del sistema de diseño, previo a la guía
paso a paso para configurar Tokens Studio contra una instancia específica.*
