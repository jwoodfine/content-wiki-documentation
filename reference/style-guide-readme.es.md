---
schema: foundry-doc-v1
title: "Guía de estilo: README"
slug: style-guide-readme.es
short_description: "Estándares editoriales para archivos README.md en raíces de repositorio y proyecto en la plataforma, cubriendo secciones requeridas, orientación del lector y la disciplina de pares bilingües."
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-readme.md
---

Un archivo `README.md` es lo primero que lee un colaborador o sistema automatizado al ingresar a un repositorio. Responde tres preguntas en orden: qué es esto, qué necesito saber para usarlo y dónde busco más información. La [[root-files-discipline|disciplina de archivos en la raíz]] rige qué archivos compañeros pueden aparecer junto al README en la raíz de un repositorio.

## Cuándo usar esta plantilla

Toda raíz de repositorio debe incluir un `README.md`. Los proyectos dentro de un monorepo (`pointsav-monorepo/<prefijo>-<nombre>/`) incluyen su propio `README.md` en la raíz cuando son lo suficientemente significativos para ser abordados de forma independiente. Los repositorios con contenido bilingüe (conforme al §6 del espacio de trabajo) también incluyen un `README.es.md` al mismo nivel.

## Estructura requerida

La plantilla exige cinco secciones en este orden:

1. **Opening** — un párrafo: qué es este repositorio o proyecto y para quién está dirigido. Sin encabezados antes de este párrafo.
2. **What this is** — alcance, no características. De dos a cuatro oraciones.
3. **Layout** — árbol de directorios anotado. Una frase por entrada. Describe estructura, no comportamiento.
4. **Using it** — la secuencia mínima para leer, ejecutar o construir el contenido. Requisitos previos, luego comandos, luego resultado esperado.
5. **Where to look next** — lista de apuntadores a documentación más detallada.

## Registro

Inglés llano, dirigido directamente al lector. Promedio de veinte palabras por oración; ninguna supera las cuarenta. Se aplica la lista de vocabulario prohibido. Los pares bilingües son adaptaciones estratégicas, no traducciones literales: la versión en español puede reestructurarse y reformularse para un contexto diferente mientras mantiene el mismo contenido factual.

## Véase también

- [[style-guide-topic|Guía de estilo — TOPIC]]
- [[style-guide-guide|Guía de estilo — GUIDE]]
- [[language-protocol-substrate|Substrato del Protocolo de Lenguaje]]
