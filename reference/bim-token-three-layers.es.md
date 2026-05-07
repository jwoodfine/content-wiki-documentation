---
schema: foundry-doc-v1
title: "Las Tres Capas de un BIM Token"
slug: bim-token-three-layers
language: es
category: reference
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c, ashrae-90-1]
paired_with: bim-token-three-layers.md
---

Un BIM Token tiene tres capas: Especificación, Normativa y Zona climática. Las tres son datos incorporados en el token — ninguna es una opción seleccionable en tiempo de ejecución. Un diseñador no "cambia" entre zonas climáticas, así como tampoco cambia el código de construcción aplicable. Las tres capas se presentan simultáneamente como tablas de referencia estáticas, mostrando todas las superposiciones registradas para el tipo de elemento del token. Esta estructura refleja una realidad física: un elemento constructivo tiene un tipo fijo (Especificación), existe en una jurisdicción fija (Normativa) y opera en un clima fijo (Zona climática).

## Por qué tres capas

Los tokens de sistemas de diseño de software tienen dos preocupaciones: qué ES un valor (su función semántica) y qué valor resuelve (su resultado calculado). Los BIM Tokens abordan un espacio de problema fundamentalmente diferente que requiere tres preocupaciones.

Una especificación de elemento del entorno construido debe responder simultáneamente:

- **¿Qué es este elemento?** — su tipo en un esquema neutro e independiente de herramienta (IFC), su clasificación en un sistema de referencia neutro (Uniclass) y su identidad semántica en un diccionario que abarca múltiples jurisdicciones (bSDD).
- **¿Qué exige la jurisdicción?** — los requisitos normativos específicos impuestos por la legislación del lugar donde se ubica el edificio, incluyendo restricciones geométricas (retranqueos, espacios libres, compartimentos contra incendios) que no pueden expresarse como valores numéricos.
- **¿Qué exige el clima?** — los requisitos de rendimiento térmico, de humedad y estructural impuestos por el clima físico del emplazamiento, expresados en códigos energéticos (ASHRAE 90.1, NBC Parte 11, EN ISO 52000).

## Capa 1 — Especificación

La capa de Especificación es la identidad permanente del token. No varía según la jurisdicción ni el clima. Cada instancia desplegada del token lee la misma capa de Especificación, independientemente de dónde se ubique el proyecto.

Los campos incluyen: clase de entidad IFC (por ejemplo, `IfcWall`), tipo predefinido IFC donde corresponda, código Uniclass 2015, URI de concepto bSDD, descripción en lenguaje natural (máximo 280 caracteres), conjuntos de propiedades IFC aplicables y tipo de token DTCG extendido.

Cada registro de Especificación incluye la ruta completa de herencia IFC desde `IfcRoot` hasta la clase específica, lo que permite a las herramientas presentar la posición del elemento en la jerarquía IFC sin requerir un documento de esquema separado.

## Capa 2 — Normativa

La capa de Normativa contiene los requisitos específicos de la jurisdicción. Es una tabla de superposiciones registradas — una fila por jurisdicción por restricción — no un valor único. La tabla muestra todas las superposiciones registradas simultáneamente.

Cada fila de superposición incluye: código ISO 3166-1/2 de jurisdicción, referencia al documento normativo, tipo de restricción (numérica, geométrica, clasificación o aprobación), parámetro, valor requerido, unidad, archivo IDS 1.0 y, si corresponde, fragmento geométrico IFC de exclusión.

A v0.0.1, la mayoría de los tokens no tienen superposiciones normativas registradas — la estructura está definida pero no poblada. El hito v0.0.3 tiene previsto entregar el primer conjunto de superposiciones: requisitos de zonificación residencial RS-1 de Columbia Británica para muros exteriores, losas y ventanas.

## Capa 3 — Zona climática

La capa de Zona climática contiene los requisitos de rendimiento basados en el clima. Como la capa de Normativa, es una tabla de filas de zona climática registradas — todas las zonas se muestran simultáneamente.

Los sistemas de clasificación de zonas climáticas utilizados incluyen: las zonas climáticas ASHRAE 90.1 (1A–8, referencia para EE. UU. e internacional), las zonas climáticas del Código Nacional de Edificación de Canadá (NBC 2020) y las zonas de rendimiento energético EN ISO 52000 (estados miembros de la UE).

## Regla de composición

Cuando la Normativa y la Zona climática especifican restricciones numéricas sobre el mismo parámetro de rendimiento, el requisito efectivo es el valor más restrictivo:

```
valor_efectivo = max(requisito_normativo, requisito_climático)
```

Los fragmentos de exclusión geométrica IFC tienen precedencia incondicional sobre cualquier restricción numérica. Cuando una capa no tiene datos registrados para un tipo de elemento dado, el token sigue siendo válido y funciona solo con la Especificación — estado válido para las fases iniciales de diseño antes de que se establezca la jurisdicción.

## Diferencia con los conjuntos de propiedades IFC

Un conjunto de propiedades IFC (`Pset_WallCommon`) declara qué propiedades puede tener un elemento de un tipo dado. No declara qué valores deben tener esas propiedades. La capa de Normativa del BIM Token consume la estructura del conjunto de propiedades IFC pero añade los valores que la especificación del conjunto de propiedades omite: el valor requerido, la jurisdicción para la que aplica y el archivo IDS 1.0 que codifica formalmente la restricción.

Esta es la misma relación que existe entre una especificación de propiedad CSS (que declara que `color` acepta un valor de color) y un token de diseño (`--color-primario: #164679`). El conjunto de propiedades define la forma; el token rellena los valores y añade la jerarquía de restricciones.

## Véase también

- [[bim-token-what-it-is]]
- [[building-design-system-bim]]
- [[city-code-as-composable-geometry]]
- [[flat-file-bim-leapfrog]]
- [[open-bim-regulatory-acceptance]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
