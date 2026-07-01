---
schema: foundry-doc-v1
title: "Seguridad por Oscuridad"
slug: security-through-obscurity
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-06-30
editor: woodfine-editorial
short_description: "La práctica de utilizar el secreto del diseño, la implementación o la configuración como mecanismo de seguridad principal — ampliamente rechazada en la práctica de seguridad profesional desde el principio de Kerckhoffs (1883) y la máxima de Claude Shannon de que 'el enemigo conoce el sistema' — aunque aceptada como una capa en una estrategia de defensa en profundidad cuando no se depende de ella como control único o principal."
paired_with: security-through-obscurity.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - 39cb3fb2b359af9559f290e25bbc9a30c74d95096497b2df8aed619c1c88c271
thesis_alignment: "La seguridad por oscuridad define un antipatrón de seguridad cuya crítica establece principios fundamentales de la arquitectura de seguridad y criptografía moderna — comprender su historia y limitaciones es esencial para razonar sobre el diseño de la seguridad del sistema."
keynote: false
---

La seguridad por oscuridad (o seguridad mediante la oscuridad) es la dependencia del secreto del diseño, la implementación o la configuración de un sistema como mecanismo de seguridad principal. Un sistema que usa la seguridad por oscuridad asume que su seguridad depende de que los atacantes no sepan cómo funciona el sistema, en lugar de que el sistema sea seguro incluso cuando su diseño sea completamente conocido. El término se usa predominantemente como una crítica — una acusación de que el diseño de un sistema de seguridad es defectuoso porque no puede resistir el análisis o un ataque por parte de una parte que ha aprendido cómo funciona el sistema.

El consenso de la comunidad de seguridad, codificado en el principio de Kerckhoffs (1883) y reformulado en la máxima de Claude Shannon (1949) y en las guías del NIST, sostiene que la seguridad por oscuridad no es un mecanismo de seguridad principal aceptable.

## Historia

**La controversia de la cerradura de Hobbs (1851).** En la Gran Exposición de 1851 en Londres, el cerrajero estadounidense Alfred Charles Hobbs abrió públicamente lo que entonces se consideraban las cerraduras más seguras disponibles — la cerradura Bramah y la cerradura detectora Chubb — demostrando que su seguridad descansaba en parte en la oscuridad de sus mecanismos más que en la resistencia inherente a la apertura no autorizada.

**El principio de Kerckhoffs (1883).** Auguste Kerckhoffs, criptógrafo holandés, publicó un artículo en el *Journal des sciences militaires* en el que declaró que "un criptosistema debe ser seguro incluso si todo lo relacionado con el sistema, excepto la clave, es de conocimiento público". Este principio establece la premisa fundamental del diseño criptográfico moderno: la seguridad de un sistema criptográfico debe derivarse enteramente del secreto de la clave, no del secreto del algoritmo.

**La máxima de Shannon (1949).** Claude Shannon reformuló el principio de Kerckhoffs como "el enemigo conoce el sistema" en su artículo de 1949 "Communication Theory of Secrecy Systems". La formulación de Shannon captura la realidad operativa del diseño de seguridad: un diseñador de sistemas debe asumir que los adversarios eventualmente aprenderán el diseño del sistema que se está protegiendo.

## Posición del NIST

El Instituto Nacional de Estándares y Tecnología (NIST) de Estados Unidos establece en sus directrices que "la seguridad del sistema no debe depender del secreto de la implementación o de sus componentes". Las guías del NIST distinguen entre usar la oscuridad como mecanismo de seguridad principal (no aceptable) y usarla como una capa en una estrategia de defensa en profundidad (aceptable cuando no se depende de ella como control principal).

## Defensa en profundidad

La posición moderna aceptada es que la seguridad por oscuridad puede usarse como una capa en una estrategia de defensa en profundidad — una arquitectura de seguridad que no depende de ningún control único sino que presenta al atacante múltiples capas independientes que deben ser derrotadas individualmente. Los ejemplos de usos aceptables de la oscuridad como una capa de defensa incluyen: cambiar los números de puerto predeterminados para reducir el ruido de escaneo automatizado; suprimir los banners de versión de software en las respuestas HTTP para reducir la explotación dirigida de vulnerabilidades conocidas; y usar protocolos no estándar para las comunicaciones internas.

En cada caso, la oscuridad reduce la conveniencia de los ataques pero no constituye el control de seguridad principal. Un modelo de seguridad que depende de que los atacantes no conozcan el número de puerto o la versión del software es un modelo que fallará cuando esa información sea descubierta.

---

*citas: [[application-programming-interface]], [[virtual-appliance]], [[computer-appliance]]*
