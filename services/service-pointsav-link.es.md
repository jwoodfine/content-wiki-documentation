---
schema: foundry-doc-v1
title: "service-pointsav-link"
slug: service-pointsav-link
short_description: "service-pointsav-link es un concepto de adaptador nombrado pero no construido para conectar un nodo os-* a una flota PointSav — no existe un paquete correspondiente en el monorepo hoy."
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: service-pointsav-link.md
last_edited: 2026-08-22
editor: pointsav-engineering
---

`service-pointsav-link` nombra un concepto, no un paquete distribuido: un adaptador de
conexión en caliente que conectaría un nodo `os-*` a la gestión de flota, traduciendo
comandos de autoridad en operaciones ejecutables por el sujeto. No existe ningún crate con
este nombre, ni un paquete `pointsav-protocol`, en ninguna parte del código fuente de la
plataforma. El concepto aparece en material de planificación interna con un estado de
"conceptual" — definido y nombrado, pero no construido.

## Lo que haría el diseño

La forma descrita, según el material de planificación: un nodo Sujeto se distribuye sin el
adaptador instalado por defecto, por lo que no contiene código capaz de iniciar contacto con
una autoridad. Un operador lo activa con un solo comando, que instala el adaptador y registra
el nodo en un registro de emparejamiento de flota. Si el adaptador falla o se elimina, el
Sujeto continúa ejecutando sus propias cargas de trabajo — solo la visibilidad de la flota
sobre él desaparece. Esta forma, de construirse, sería una implementación concreta del
[[diode-standard|Estándar Diode]]: un canal de autoridad a sujeto sin ruta de retorno para
comandos.

## Lo que existe en su lugar

Los mecanismos unidireccionales reales de la plataforma están documentados en
[[diode-standard]]. Cubre cada uno en detalle: un par de egreso de extracción-y-borrado, una
canalización de telemetría basada en extracción, un componente de ingesta que nombra su
propia lógica "el diodo de ingreso," y una canalización de promoción de código direccional
con protecciones contra el flujo inverso. Ninguno de estos es el adaptador descrito aquí, y
ninguno es un enlace de comando de flota de propósito general — cada uno satisface la regla
unidireccional para su propio propósito estrecho.

Si este adaptador específico es un componente planificado aún no construido, o un diseño
renombrado o superado por uno de esos otros mecanismos, es una pregunta abierta señalada al
grupo de ingeniería responsable. Este artículo no aventura una respuesta.

## Véase también

- [[diode-standard]] — la regla de diseño que este adaptador implementaría, y los mecanismos
  reales que la siguen hoy
- [[machine-based-auth]] — cómo se autentican dos máquinas antes de que se permita cualquier
  conexión, real o conceptual
- [[os-network-admin]] — el lado de autoridad al que se conectaría el diseño de este adaptador
