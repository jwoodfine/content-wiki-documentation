---
schema: foundry-doc-v1
title: "El Código Urbano como Geometría Composable"
slug: city-code-as-composable-geometry
language: es
category: architecture
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
paired_with: city-code-as-composable-geometry.md
---

Toda herramienta de verificación de cumplimiento normativo en producción sigue la misma arquitectura: un modelo de diseño terminado se envía a un motor de reglas, que genera un informe de infracciones, que un profesional debe revisar y corregir antes de reenviar. Este modelo de validación posterior al diseño ha sido el estándar de la industria durante veinte años y genera una tensión estructural entre la velocidad de iteración del diseño y la verificación del cumplimiento. Es posible una arquitectura diferente: si los requisitos normativos se codifican directamente en los elementos disponibles para un diseñador — no como reglas aplicadas a un modelo terminado, sino como restricciones geométricas y numéricas incorporadas en la especificación del elemento — entonces las configuraciones no conformes no pueden colocarse. Este es el modelo del Código Urbano como Geometría Composable, y es la afirmación arquitectónica subyacente a la plataforma de BIM Tokens (Doctrina, afirmación #41, 2026).

## El paradigma de validación posterior

Las herramientas de validación posterior al diseño operan con un patrón común: el diseñador crea un modelo en una herramienta de autoría BIM compatible con IFC, lo exporta en formato IFC, lo envía a un servicio de validación que aplica un conjunto de reglas y produce un informe de infracciones, y luego un profesional revisa el informe, vuelve a la herramienta de autoría, realiza correcciones y reenvía. La mayoría de las herramientas de autoría no aplican ninguna restricción en el momento de colocación.

Las consecuencias son operativas. Los equipos de diseño presupuestan tiempo de iteración para la revisión normativa. En proyectos complejos, los ciclos de revisión regulatoria añaden semanas a las fases de diseño.

## El mecanismo composicional

El Código Urbano como Geometría Composable opera a través de un mecanismo técnico de tres capas.

**Capa 1: Identidad semántica mediante bSDD.** Cada BIM Token lleva una URI de concepto bSDD que identifica su tipo de elemento de manera neutral a la jurisdicción y a la herramienta.

**Capa 2: Restricción normativa mediante IDS 1.0.** Cada superposición jurisdiccional registrada para un BIM Token incluye un archivo de restricción IDS 1.0 que codifica restricciones numéricas y de propiedades: valores máximos de transmitancia térmica, clasificaciones mínimas estructurales, requisitos de clase de resistencia al fuego, espacios libres de accesibilidad. Cuando se coloca un BIM Token, sus restricciones IDS registradas son parte de su especificación — la herramienta de autoría las recibe como requisitos del elemento en el momento de la colocación, no como reglas post-colocación.

**Capa 3: Geometría de exclusión mediante fragmento IFC.** Donde un requisito normativo tiene expresión geométrica — un límite de compartimento contra incendios, un retranqueo de lindero, una envolvente de accesibilidad que debe permanecer libre — la superposición jurisdiccional incluye un fragmento IFC: una geometría sólida codificada en formato IFC que define el espacio excluido o requerido. Este fragmento se instancia en el momento de la colocación y no puede ser anulado por restricciones numéricas.

## Relevancia para América Latina y España

Los mandatos de BIM para obras públicas están en expansión en la región hispanohablante. España tiene previsto el mandato completo de BIM para todas las obras públicas en 2026 bajo el Plan de Impulso de la Contratación Pública (PPRE 2022–2026). México, Colombia, Chile y Argentina cuentan con iniciativas BIM en distintas fases de implementación, con Chile entre los más avanzados (Estrategia Nacional BIM 2023–2025). En todos estos contextos, la pregunta no es si se adoptará BIM, sino qué plataformas pueden cumplir los requisitos de soberanía de datos adjuntos a estos mandatos.

El modelo del Código Urbano como Geometría Composable es especialmente relevante para entornos donde los datos regulatorios son información pública: publicar los requisitos normativos en un estándar JSON neutro y abierto y distribuirlos mediante repositorios git públicos es análogo a publicar códigos de construcción en PDF — neutral, reproducible e independiente de proveedores.

## Etapas de implementación

**Etapa 1 (actual, prevista para v0.0.3):** bóveda de BIM Tokens con capa de Especificación completa. Esqueleto de la capa de Normativa con el primer conjunto de superposiciones: requisitos de zonificación residencial RS-1 de Columbia Británica.

**Etapa 2 (prevista, v0.1.x):** generación de archivos de restricción IDS 1.0 para cada superposición normativa registrada, permitiendo que los validadores IDS existentes consuman especificaciones de restricción de PointSav.

**Etapa 3 (prevista, futuro):** integración en herramientas de autoría BIM mediante un plugin o superficie API que entregue las restricciones del BIM Token en el momento de la colocación, no al enviar el modelo.

## Véase también

- [[bim-token-what-it-is]]
- [[bim-token-three-layers]]
- [[flat-file-bim-leapfrog]]
- [[open-bim-regulatory-acceptance]]
- [[leapfrog-2030-architecture]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
