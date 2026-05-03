---
schema: foundry-doc-v1
title: "Taxonomía Semilla como Bootstrap para PYMEs"
slug: seed-taxonomy-as-smb-bootstrap.es
category: architecture
type: topic
quality: published
short_description: "Cada despliegue de inquilino Foundry provisiona una taxonomía semilla de cuatro partes — Arquetipos, Plan de Cuentas, Dominios, Temas — como el arranque del grafo de conocimiento."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: seed-taxonomy-as-smb-bootstrap.md
---

Cada despliegue de inquilino Foundry comienza con una **taxonomía semilla**: una estructura compacta, ajustable manualmente y de cuatro partes que forma el andamiaje inicial del grafo de conocimiento por inquilino. Las cuatro partes son Arquetipos, Plan de Cuentas, Dominios y Temas. Cada entidad lleva palabras clave de gravedad — anclajes de palabras clave explicables que impulsan la clasificación del contenido entrante. Este patrón codifica la reclamación doctrinal #47.

## Las cuatro partes

**Arquetipos — quién actúa.** Cinco a siete identidades de rol por patrón cognitivo. El valor predeterminado de Foundry lleva cinco roles universales que aparecen en alguna forma en cualquier negocio: el Ejecutivo (Dirección Estratégica), el Guardián (Riesgo y Cumplimiento), el Fiduciario (Integridad de Recursos), el Arquitecto (Diseño del Sistema) y el Constructor (Realización Física). Los roles específicos de la industria se añaden a través de los Paquetes de Semilla Vertical.

**Plan de Cuentas — qué negocio es este.** Cinco a diez perfiles de negocio específicos de la industria, cada uno con un identificador, un nombre de perfil, un subdominio y palabras clave de gravedad. Los perfiles reflejan las categorías reales de ingresos y gastos del negocio.

**Dominios — categorías macro de trabajo.** Tres a cinco categorías macro que agrupan unidades de trabajo. El valor predeterminado proporciona Corporativo, Proyectos y Documentación. Cada Dominio contiene un Glosario y una colección de Temas.

**Temas — iniciativas acotadas en el tiempo.** Cuatro a diez temas activos que representan el enfoque estratégico actual. Los Temas son la parte más volátil de la taxonomía — pueden cambiar trimestralmente a medida que las iniciativas se abren y cierran.

## El mecanismo de palabras clave de gravedad

La clasificación del nuevo contenido usa coincidencia de palabras clave en lugar de similitud de embeddings. Este enfoque es deliberado: la clasificación basada en palabras clave es explicable (el operador puede leer y verificar "este documento fue clasificado como Bienes Raíces porque coincidieron los términos Arrendamiento, Oficina e Industrial"), auditable y ajustable manualmente. La similitud de embeddings se proporciona como capa adicional para los casos donde las palabras clave explícitas no coinciden, pero no reemplaza el mecanismo de palabras clave.

## Diferencia estructural con los enfoques de ontología empresarial

Las plataformas de software empresariales tienden a optimizar sus ontologías para la exhaustividad en todos los clientes posibles. Cualquier cliente específico enfrenta una jerarquía extensa y normalmente necesita personal especializado para configurarla.

La taxonomía semilla de Foundry optimiza para la acción de un cliente específico. Toda la taxonomía está prevista para ser legible y comprensible por los propios operadores del cliente en una sesión única. La contrapartida es que la taxonomía no se transfiere sin cambios entre clientes — cada paquete vertical es específico de la industria. El beneficio es que el cliente puede operar la taxonomía por sí mismo sin contratar especialistas en ontología.

## Relación con el grafo de conocimiento

La taxonomía sembrada se convierte en la estructura inicial del grafo de conocimiento por inquilino en `service-content`. A medida que opera el despliegue, las nuevas entidades descubiertas durante la inferencia se añaden al grafo, haciendo crecer la taxonomía orgánicamente a partir del uso real.

## Véase También

- [[vertical-seed-packs-marketplace]] — paquetes específicos de la industria que pueblan la taxonomía semilla en el aprovisionamiento
- [[knowledge-graph-grounded-apprenticeship]] — el grafo sembrado es la fuente de fundamentación para la inferencia
- [[customer-owned-graph-ip]] — la taxonomía personalizada del cliente es su propiedad intelectual

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-seed-taxonomy-as-smb-bootstrap.md` (refinado el 30 de abril de 2026).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
