---
schema: foundry-doc-v1
title: "os-orchestration — El agregador de flota"
slug: os-orchestration
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-orchestration.md
short_description: "os-orchestration es el sistema operativo de nivel comercial que permite a un único operador ver, consultar y comandar muchos archivos Totebox a la vez — el Agregador de Flota para portafolios multi-entidad y despliegues empresariales."
cites: []
---

`os-orchestration` es el sistema operativo de nivel comercial que permite a un único operador ver, consultar y comandar muchos [[totebox-archive|archivos Totebox]] a la vez. Mientras [[console-os|`os-console`]] se conecta a un único [[totebox-os|`os-totebox`]], `os-orchestration` es el concentrador entre la Consola de un operador y una flota de Toteboxes. Es lo que un ejecutivo visualiza cuando quiere la posición de cada propiedad en un portafolio, cada entidad en una sociedad holding o cada proyecto en un pipeline de desarrollo — una respuesta única y unificada a "¿cuál es el estado de todo el patrimonio ahora mismo?" Este artículo cubre qué hace `os-orchestration`, qué no hace deliberadamente, cómo funciona la agregación, las funciones comerciales que agrega y cuándo desplegarlo.

## Qué no hace

`os-orchestration` no almacena registros sin procesar. No tiene estado. Extrae metadatos de los Toteboxes, sintetiza una vista unificada y la presenta a través de `os-console`. Los datos sin procesar nunca abandonan su Totebox soberano. El agregador solo ve lo que el Totebox tiene permitido exponer.

Este límite es estructuralmente importante: incluso si `os-orchestration` se ve comprometido, los Toteboxes subyacentes permanecen sellados. El agregador no posee claves a los archivos.

## Su lugar en la línea de productos

| Componente | Rol | Modelo de licencia (previsto) |
|---|---|---|
| `os-console` | Terminal de cara al operador | Apache 2.0 (previsto como gratuito) |
| `os-totebox` | Archivo de datos por entidad | Apache 2.0 (previsto como gratuito) |
| `os-orchestration` | Agregador de flota | Propietario (previsto como producto comercial) |

La línea comercial se traza en el agregador. La Consola y el Totebox están previstos como libres y libremente transferibles. El agregador de Orquestación es el producto de pago — un operador individual que gestiona una sola entidad nunca lo necesita.

## Cómo funciona la agregación

`os-orchestration` se conecta a los Toteboxes a través del Protocolo PointSav (PSP) — un protocolo binario basado en [[capability-based-security|capacidades]] que tuneliza a través de TLS estándar en el borde. Dentro del túnel:

1. El agregador envía un objeto de capacidad firmado que concede permiso para leer una fila específica de un Totebox específico durante una ventana de tiempo fija.
2. El Totebox verifica la capacidad, ejecuta la consulta internamente y emite solo el resultado — nunca el registro sin procesar.
3. El agregador combina resultados de muchos Toteboxes en una vista única unificada.

El pipeline de promesas y la asignación de memoria de copia cero hacen que la experiencia se sienta local incluso cuando los Toteboxes están distribuidos en múltiples regiones.

## Las funciones comerciales

Tres capacidades están reservadas exclusivamente a `os-orchestration`:

| Función | Qué permite |
|---|---|
| Agregación | Leer metadatos de múltiples Toteboxes simultáneamente |
| Multi-tenancy | Servir a múltiples operadores contra la misma flota subyacente |
| Vistas complejas | Paneles entre archivos — resúmenes de portafolio, conciliación entre entidades, resúmenes ejecutivos |

Estas funciones están intencionalmente ausentes del código base abierto de `os-console`. Viven en el código base de `os-orchestration` y en ningún otro lugar.

## La disciplina Diodo

`os-orchestration` puede emitir comandos a los Toteboxes que gestiona. Los Toteboxes no pueden emitir comandos de vuelta. El agregador es él mismo un sujeto [[diode-standard|Diodo]]: recibe comandos solo de `os-console`, nunca de un Totebox. Esto hace que el movimiento lateral sea estructuralmente imposible — un Totebox comprometido no puede usar el agregador como puente hacia la Consola del operador. El artículo [[totebox-orchestration|Orquestación Totebox]] cubre la gestión del ciclo de vida y el aprovisionamiento de contenedores.

## Cuándo desplegarlo

`os-orchestration` es un producto comercial para operadores multi-entidad. Los operadores de entidad única que gestionan un Totebox no lo necesitan. Los operadores multi-entidad — portafolios inmobiliarios, empresas públicas con subsidiarias, oficinas familiares con múltiples tenencias — lo despliegan cuando la carga cognitiva de ejecutar Consolas separadas contra Toteboxes individuales justifica el agregador.

## Véase también

- [[console-os]] — la distinción entre modo Directo y modo Agregado; os-console se empareja con os-orchestration en modo Agregado
- [[totebox-os]] — los archivos que se están agregando
- [[diode-standard]] — la disciplina de comandos unidireccional que rige el agregador
- [[machine-based-auth]] — cómo los emparejamientos aseguran las conexiones del agregador con los Toteboxes
- [[deployment-patterns]] — cómo os-orchestration aparece en las configuraciones de despliegue comerciales
- [[os-family-overview]] — la familia de ocho SO y cómo encaja os-orchestration
