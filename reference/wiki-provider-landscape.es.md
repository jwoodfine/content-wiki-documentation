---
schema: foundry-doc-v1
title: "Panorama de proveedores de wiki — cómo se ve el campo en 2026"
slug: wiki-provider-landscape
short_description: "Una auditoría estructural del mercado de superficies de conocimiento con forma de wiki, por arquetipo, que documenta razones estructurales por las que ningún arquetipo ha cerrado la brecha enciclopédica de Wikipedia."
status: active
category: reference
type: topic
content_type: topic
quality: complete
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: wiki-provider-landscape.md
cites:
 - ni-51-102
 - np-51-201
---

El wiki de documentación de PointSav en `documentation.pointsav.com` es uno de los
participantes en un campo donde un gran número de proveedores distinguibles ofrecen
alguna variación de "superficie de conocimiento con forma de wiki" en 2026. La mayoría
no son plataformas de conocimiento enciclopédico; son herramientas de productividad
para equipos privados, generadores de sitios de documentación para desarrolladores, o
sistemas de pensamiento personal en red. Ninguno ha reemplazado a Wikipedia para el
conocimiento enciclopédico de profundidad general. Esta TOPIC documenta el campo por
arquetipo estructural, nombra las razones estructurales por las que ningún arquetipo ha
cerrado la brecha, e identifica las ventajas genuinas que cada arquetipo tiene sobre
Wikipedia.

La auditoría es estructural, no promocional. Cada arquetipo se describe factualmente
por su patrón de posicionamiento publicado más fuerte y la limitación estructural que le
impide llenar la brecha del conocimiento enciclopédico.

## Los cuatro arquetipos

- **Arquetipo A — Bases de conocimiento colaborativas**: construidas para la gestión de
  conocimiento organizacional privado. Venden licencias de usuario a TI empresarial.
- **Arquetipo B — Motores wiki de acceso público**: los más cercanos en forma a una
  plataforma de clase Wikipedia; la mayor variación en gobernanza editorial dentro del
  arquetipo.
- **Arquetipo C — Generadores de sitios de documentación para desarrolladores**:
  generan sitios de documentación; primero estático, edición colaborativa en segundo
  lugar o ninguna.
- **Arquetipo D — Herramientas personales y de pensamiento en red**: principalmente
  gestión de conocimiento personal de un solo autor, con algunas superficies de
  publicación.

## Modos de falla transversales

Las ocho razones estructurales por las que ningún arquetipo ha reemplazado a Wikipedia:

**(i) Desajuste de audiencia.** Los Arquetipos A y C fueron construidos para diferentes
públicos — gestión de conocimiento organizacional privado y documentación de proyectos
de software, respectivamente. La publicación enciclopédica pública requiere lo
opuesto: editores anónimos, fuentes verificables, navegación orientada al lector.

**(ii) Sin constitución editorial.** La NPOV, Notabilidad, Fuentes Fiables, Sin
Investigación Original y Manual de Estilo de Wikipedia constituyen una constitución
editorial refinada durante décadas. Ningún arquetipo en esta auditoría ofrece
equivalente como característica de producto.

**(iii) Piso de densidad de información.** Los generadores de sitios de documentación
(Arquetipo C) optimizan para elegancia de prosa y estética de desarrollador. Los
artículos de Wikipedia son deliberadamente densos — infocajas, hatnotes, referencias
con 100+ notas al pie, navboxes, etiquetas de esbozo, páginas de desambiguación.

**(iv) Primitivas de navegación ausentes.** La pila de navegación de Wikipedia —
wikilinks con señalización de enlace rojo, superficie de artículo aleatorio, grafo de
categorías — existe completa solo en la implementación de referencia del Arquetipo B, y
como máximo parcialmente en otros lugares.

**(v) Las citas son decorativas, no constitutivas.** El sistema de notas al pie de
Wikipedia hace las afirmaciones verificables a nivel de declaración. En los Arquetipos
A, C y D, las citas están ausentes por completo o implementadas como hipervínculos en
línea sin estructura formal.

**(vi) Sin sustrato de páginas de Discusión.** Cada artículo de Wikipedia tiene una
página de Discusión — el registro público del debate editorial. Las herramientas del
Arquetipo A tienen comentarios en línea, no debate editorial público archivado.

**(vii) Fragilidad estructural.** Varios productos del Arquetipo A usan formatos de
serialización propietarios con riesgo de vendor lock-in. El wikitexto de Wikipedia es
texto plano exportable y archivable por cualquiera.

**(viii) Homogeneización de plantillas.** Los sitios del Arquetipo C tienden a verse
estructuralmente idénticos entre sí — la estética de documentación que el lector de
Wikipedia no asocia con autoridad enciclopédica.

## Por qué existe la brecha del estándar de oro en 2026

La brecha tiene cinco causas estructurales reforzadas mutuamente: desalineación de
incentivos comerciales (los arquetipos A y C ganan dinero vendiendo licencias, no
invirtiendo en gobernanza editorial); el trabajo editorial no puede automatizarse (la
autoridad de Wikipedia son veinte años de labor editorial acumulada); el costo de
coordinación de código abierto (el motor de referencia del Arquetipo B tiene 25 años y
una enorme superficie de compatibilidad heredada); expansión de alcance en un lado,
alcance estrecho en el otro; y la brecha de "memoria muscular de Wikipedia" — ningún
competidor ha invertido en replicar la experiencia de navegación que miles de millones
de lectores de Wikipedia conocen por reflejo.

## Lo que esto significa para documentation.pointsav.com

El motor wiki [[app-mediakit-knowledge]] se convierte en la demostración instalable por
el cliente de ese sustrato. El argumento estructural para la afirmación de salto
generacional — adoptar lo que cada arquetipo hace bien sin heredar su debilidad
estructural — es lo que este artículo documenta: la brecha existe por las cinco causas
estructurales anteriores; cerrarla requiere las condiciones previas de soberanía de
sustrato, enrutamiento de cómputo de tres niveles y captura de corpus de aprendizaje
que PointSav ya tiene como intención de diseño.

## Véase también

- [[app-mediakit-knowledge]]
- [[compounding-substrate]]
