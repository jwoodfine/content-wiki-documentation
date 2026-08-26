---
schema: foundry-doc-v1
title: "El código urbanístico como geometría componible"
slug: city-code-as-composable-geometry
language: es
category: patterns
index_group: sovereignty-and-infrastructure-patterns
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "Un patrón de composición previa que codifica los requisitos normativos en las especificaciones de los elementos como restricciones geométricas y numéricas, en lugar de aplicarlos después del diseño, de modo que una configuración no conforme no llega a poder colocarse."
cites: [ifc-4-3, ids-1-0, bsdd-v1]
paired_with: city-code-as-composable-geometry.md
---

Toda herramienta de verificación normativa en producción sigue la misma arquitectura: se envía un modelo terminado a un motor de reglas, este emite un informe de incumplimientos y una persona lo revisa y corrige antes de volver a enviarlo. Ese modelo de validación posterior al diseño lleva veinte años siendo el estándar del sector y genera una tensión estructural: cuanto más exhaustivo es el motor de reglas, más largo es cada ciclo de revisión.

Existe otra arquitectura posible. Si los requisitos normativos se codifican en los propios elementos disponibles para quien diseña — no como reglas aplicadas a un modelo terminado, sino como restricciones geométricas y numéricas incorporadas a la especificación del elemento — las configuraciones no conformes no pueden colocarse. Ese es el patrón del código urbanístico como geometría componible, y es la afirmación arquitectónica que subyace a la biblioteca de Objetos BIM.

**Por qué importa:** el coste de un incumplimiento normativo pasa de semanas de retrabajo a cero, porque el incumplimiento nunca llega a entrar en el modelo.

## El paradigma de validación posterior

Las herramientas de validación posterior comparten una misma forma: se crea el modelo en una herramienta de autoría compatible con IFC, se exporta a IFC y se envía a un servicio de validación; el servicio aplica un conjunto de reglas y produce un informe de incumplimientos; una persona lo revisa, vuelve a la herramienta de autoría, corrige y reenvía. El ciclo se repite hasta que el modelo pasa. La mayoría de las herramientas de autoría no imponen nada en el momento de la colocación: cualquier elemento puede ir a cualquier sitio hasta que un validador externo objete.

Las consecuencias son operativas. Los equipos presupuestan tiempo de iteración para la revisión normativa y, en proyectos complejos, esa revisión añade semanas a las fases de diseño. El validador es una compuerta situada fuera del entorno de diseño que se comunica con él de forma asíncrona.

**Por qué importa:** el retraso no es un defecto de herramienta que nadie haya arreglado — es inherente a comprobar a posteriori en lugar de restringir de antemano.

## Estado del arte

La investigación realizada en abril de 2026 identificó cuatro categorías de estado del arte, todas en el cuadrante de validación posterior.

**IDS 1.0.** El estándar IDS de buildingSMART codifica restricciones de propiedades en XML. Un archivo IDS declara qué contiene un modelo válido: es un lenguaje de validación, no una restricción sobre la paleta de elementos. Los archivos IDS son entradas de los validadores, no restricciones aplicadas durante la autoría.

**bSDD.** El Diccionario de Datos de buildingSMART aporta identidad semántica a los tipos de elemento entre jurisdicciones y herramientas. No codifica restricciones normativas ni requisitos de desempeño por zona climática. Una URI de bSDD es un ancla de identidad, no una especificación de restricción.

**Plataformas comerciales de validación.** Operan después del diseño. Sus motores de reglas comprueban geometría, topología, valores de propiedades y relaciones espaciales, pero como herramientas de auditoría sobre modelos ya enviados.

**CORENET X (Singapur).** El sistema gubernamental de presentación BIM más avanzado en producción pública. Acepta modelos IFC para solicitudes de licencia y ejecuta comprobaciones automáticas contra la normativa singapurense. Sigue siendo un validador: los modelos se crean libremente, se envían y se devuelven con informes de incumplimientos. La implementación de 2024 añade orientación en tiempo real en algunos complementos de autoría, lo que estrecha la brecha sin cerrarla. Es específico de su jurisdicción y no está disponible como plataforma neutral para otras.

**Valoración.** Todo el estado del arte identificado ocupa el cuadrante de validación posterior. El cuadrante de composición previa — codificar las restricciones en las especificaciones de los elementos antes de la autoría — no tiene estado del arte establecido en producción pública a fecha de 2026.

## El mecanismo compositivo

**Capa 1 — identidad semántica mediante bSDD.** Cada Objeto BIM porta una URI de concepto bSDD que identifica su tipo de elemento en una referencia neutral respecto a jurisdicción y herramienta. Esa URI es la identidad estable que permite a las capas de Regulación y Zona Climática referirse al mismo tipo de elemento con independencia de la deriva de versiones de IFC.

**Capa 2 — restricción normativa mediante IDS 1.0.** Cada capa jurisdiccional registrada incluye un archivo de restricciones IDS 1.0 que codifica límites numéricos y de propiedades: transmitancias máximas, clasificaciones estructurales mínimas, clases de resistencia al fuego, holguras de accesibilidad. Al colocar el objeto, sus restricciones IDS registradas forman parte de su especificación: el entorno de autoría las recibe como requisitos del elemento en el momento de la colocación, no como reglas posteriores.

**Capa 3 — geometría de exclusión mediante fragmento IFC.** Cuando un requisito tiene expresión geométrica — un límite de sector de incendio que un elemento no debe cruzar, un retranqueo respecto al lindero, una envolvente de accesibilidad que debe permanecer libre — la capa jurisdiccional incluye un fragmento IFC: geometría sólida en formato IFC que define el espacio excluido o exigido. El fragmento se asocia al objeto y se resuelve en el momento de la colocación, y no puede anularse mediante restricciones numéricas.

La composición de las tres capas es lo que hace que la geometría "codifique" el código. La restricción no reside en una base de datos de validación aparte que se consulta después; reside en la especificación del objeto y se instancia con el elemento.

**Por qué importa:** como la restricción viaja con el elemento, la normativa de una jurisdicción puede cambiar sin que nadie tenga que reauditar los modelos existentes — la siguiente colocación simplemente toma la capa vigente.

## La geometría de exclusión en detalle

El mecanismo del fragmento IFC atiende a la clase de requisitos que las restricciones numéricas no pueden expresar.

Considérese un muro de sector de incendio en un edificio de varias plantas. El requisito no es solo "este muro debe tener clase de resistencia al fuego REI 90". Es también "este muro debe formar un plano continuo desde la losa de suelo hasta la de techo, sin penetraciones salvo las cubiertas por dispositivos de cierre con la clasificación adecuada". El segundo requisito es topológico y geométrico: el muro debe ocupar una relación espacial concreta con los elementos que lo rodean.

Una restricción numérica IDS puede expresar REI 90; no puede expresar la continuidad topológica. Un fragmento IFC de exclusión geométrica sí: codifica el volumen espacial que el límite debe ocupar y los volúmenes adyacentes que debe rellenar construcción conforme. Las herramientas de autoría que consumen el fragmento pueden mostrar la geometría exigida como guía de diseño y señalar desviaciones en tiempo real.

**Por qué importa:** quien diseña ve la configuración espacial exigida mientras diseña, no después de enviar. Esa es la diferencia cualitativa entre este patrón y la validación.

## Restricciones estructurales de los enfoques centralizados

**Soberanía de los datos normativos.** La normativa jurisdiccional es derecho público. Codificarla como un servicio alojado en una nube comercial genera problemas de contratación y soberanía para jurisdicciones fuera de Estados Unidos bajo los requisitos de residencia de datos de la UE, el GDPR y marcos nacionales equivalentes. Para una adopción amplia se requiere estructuralmente una plataforma neutral que ciudades y gobiernos nacionales puedan autoalojar o hacer alojar bajo marcos de nube nacionales.

**Requisito de funcionamiento sin conexión.** Las obras operan con frecuencia sin conectividad fiable. Los proyectos restringidos por ITAR, los emplazamientos remotos y muchas infraestructuras públicas necesitan los datos de restricción disponibles sin red. Un servicio de validación dependiente de la nube no puede atenderlos; un archivo de objetos clonado y almacenado localmente está disponible sin conexión de forma incondicional.

**Neutralidad de plataforma.** Los gobiernos que emiten requisitos normativos necesitan publicarlos a todas las plataformas BIM conformes, no a proveedores concretos. Publicar los requisitos en un estándar JSON abierto y neutral (W3C DTCG con extensiones BIM) y distribuirlos mediante repositorios públicos es análogo a publicar los códigos de edificación en PDF: neutral, reproducible e independiente del proveedor.

## Etapas de implementación

**Etapa 1 (actual, prevista para v0.0.3).** Archivo de objetos con la capa de Especificación completa. Esqueleto de la capa de Regulación con un primer conjunto de capas jurisdiccionales: residencial de Columbia Británica (zonificación RS-1), ilustrativa del código de zonificación residencial de una jurisdicción representativa. Capa de Zona Climática poblada con los parámetros de desempeño de la zona templada costera de BC (equivalente ASHRAE 5C).

**Etapa 2 (prevista, v0.1.x).** Generación de archivos de restricción IDS 1.0. Para cada capa de Regulación registrada se genera un archivo IDS 1.0 conforme a partir de los datos del objeto, publicado junto al JSON DTCG, de modo que los validadores compatibles con IDS ya existentes puedan consumir especificaciones de restricción creadas por PointSav.

**Etapa 3 (prevista, futura).** Integración con herramientas de autoría — un complemento o superficie de API que entregue las restricciones del objeto a las herramientas compatibles con IFC en el momento de la colocación y no en el del envío, con la paleta de elementos limitada a los objetos conformes para la jurisdicción y la zona climática del proyecto.

## Véase también

- [[flat-file-bim-leapfrog]] — la postura sin conexión y de estándares abiertos de la que esto depende
- [[leapfrog-2030-architecture]] — el programa arquitectónico más amplio
