---
schema: foundry-doc-v1
title: "Cómo está organizada esta base de conocimiento"
slug: wiki-structure
category: reference
type: topic
content_type: topic
quality: complete
short_description: "Un mapa para el lector de la base de conocimiento de
  la plataforma: catorce áreas que cubren qué construye PointSav, cómo
  está construida, por qué se puede confiar en ella y cómo la operan los
  clientes — escrito para que tanto ingenieros como lectores del ámbito
  financiero puedan navegarla."
status: active
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
paired_with: wiki-structure.md
---

[[pointsav-overview|PointSav]] construye sistemas operativos y servicios para empresas
reguladas que necesitan ser dueñas por completo de sus datos, de su IA
y de su registro documental. La plataforma se ejecuta sobre el hardware
del cliente, está construida para producir registros con calidad de
divulgación continua por su propia estructura, y funciona plenamente
sin IA para los compradores que requieren un aislamiento total
(air-gap). Esta base de conocimiento documenta esa plataforma. Los
artículos son técnicos — escritos ante todo para desarrolladores — pero
el mapa siguiente está escrito para todos, incluyendo a quienes llegan
desde la base de conocimiento corporativa sin formación en ingeniería.
El nombre de cada área dice con claridad qué contiene.

## Qué es y cómo está construido

- **Cómo está construido** — cómo se compone la plataforma: una
  construcción en tres partes que separa lo que entra, el núcleo de
  registro documental y la IA opcional — y el principio que la sostiene:
  el cliente es dueño de su instancia en ejecución por completo, sobre
  su propio hardware. Empiece aquí para la visión de conjunto, incluido
  cómo el modelo de negocio se deriva de la arquitectura.
- **Los componentes** — las piezas reutilizables con las que está
  construida la plataforma. Si un artículo en otra parte nombra un
  mecanismo que no reconoce, su definición vive aquí.
- **Patrones de diseño** — las formas nombradas y repetibles que la
  plataforma reutiliza para resolver problemas de coordinación y de
  propiedad, redactadas una vez y referenciadas en todas partes.

## Por qué se puede confiar en ella

- **Seguridad y confianza** — cómo se protege la plataforma y cómo se
  verifican sus registros: identidad y permisos, verificación
  criptográfica, límites de aislamiento, cómo se manejan y se mantienen
  privados los datos, y los controles de cadena de suministro diseñados
  para mantener el código honesto desde quien contribuye hasta
  producción.
- **Cómo se usa y se contiene la IA** — la decisión de diseño más
  distintiva de la plataforma, dicha con claridad: el flujo de datos
  central se ejecuta enteramente sin IA, y donde se usa IA esta no puede
  escribir en el registro autorizado. Estos artículos explican el límite
  que lo impone, cómo se enrutan las solicitudes entre modelos, y los
  modelos pequeños, del lado del cliente, diseñados para aprender el
  entorno propio de cada cliente.

## La plataforma, pieza por pieza

- **Sistemas operativos** — los sistemas operativos que entrega
  PointSav, un artículo por sistema.
- **Servicios de la plataforma** — los servicios de fondo siempre
  activos, un artículo por servicio: qué hace y qué datos posee.
- **Aplicaciones** — las aplicaciones que la gente realmente usa, desde
  los sitios públicos de conocimiento hasta las consolas internas.
- **Dónde se ejecuta** — dónde vive físicamente todo: hardware del
  cliente, despliegue, almacenamiento, telemetría y la red de cómputo
  compartida que agrupa hardware entre distintos sitios.
- **Diseño y marca** — cómo se ve y cómo habla la plataforma: filosofía
  de diseño, vocabulario visual y superficies de marca. (El "sistema de
  diseño", *design system*, se documenta aquí como componente de la
  plataforma.)

## Cómo se toman las decisiones

- **Gobernanza y estándares** — cómo se toman y se registran las
  decisiones de ingeniería: registros de decisiones, estructura legal y
  de licencias, y disciplina de divulgación. Los lectores del ámbito
  financiero encontrarán aquí el material de cumplimiento.

## Trabajar con la plataforma

- **Cómo se opera** — instrucciones paso a paso para el trabajo
  práctico: instalar, configurar, desplegar, operar. Los clientes operan
  su propia instancia, así que están escritas para un lector frente al
  teclado.
- **Glosario y referencia** — cada término definido en palabras
  sencillas, más los catálogos usados en toda la base de conocimiento.
  La vía más rápida hacia un término desconocido.
- **Investigación** — artículos de investigación extensos, publicados
  como borradores de trabajo bajo un aviso permanente de preprint:
  argumentos completos, más que documentación.

Cada artículo se publica en inglés y en español. Las páginas de
categoría listan sus artículos alfabéticamente; cada una abre con una
guía curada del área antes del listado completo.
