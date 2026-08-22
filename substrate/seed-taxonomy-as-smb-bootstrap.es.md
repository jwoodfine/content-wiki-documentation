---
schema: foundry-doc-v1
title: "Taxonomía semilla como Bootstrap para PYMEs"
slug: seed-taxonomy-as-smb-bootstrap
category: substrate
type: topic
content_type: topic
quality: complete
index_group: platform-mechanics
short_description: "Cada despliegue de inquilino provisiona una taxonomía semilla de cuatro partes — Arquetipos, Plan de Cuentas, Dominios, Temas — como el arranque del grafo de conocimiento."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: seed-taxonomy-as-smb-bootstrap.md
---


Cada despliegue de inquilino comienza con una **taxonomía semilla**: una estructura compacta, ajustable manualmente y de cuatro partes que forma el andamiaje inicial del [[knowledge-graph-grounded-apprenticeship|grafo de conocimiento]] por inquilino. Las cuatro partes son Arquetipos, Plan de Cuentas, Dominios y Temas. Cada entidad lleva palabras clave de gravedad — texto de referencia explicable que un operador lee al clasificar contenido nuevo dentro de [[service-content|la taxonomía]].

## Las cuatro partes

**Arquetipos — quién actúa.** Once identidades de rol por patrón cognitivo, cada una con un nombre, una firma (su función central), un "disparador de sanación" (el modo de fallo que el rol existe para detectar) y palabras clave de gravedad — por ejemplo el Ejecutivo (Dirección Estratégica, disparado por Estancamiento) o el Guardián (Riesgo y Cumplimiento, disparado por Brecha). El conjunto abarca roles estratégicos, operativos y de realización física. Los roles específicos de la industria se añaden a través de los Paquetes de Semilla Vertical.

**Plan de Cuentas — quién ocupa qué rol, no qué negocio es este.** Pese al nombre, no es una clasificación de industria ni de ingresos/gastos — es una taxonomía de roles de personal, organizada en subdominios (roles de gobierno personal, cumplimiento, finanzas y varios más), cada entrada con un número de referencia, un tipo de rol y palabras clave de gravedad para clasificar el cargo o función de una persona frente a ella.

**Dominios — categorías macro de trabajo.** Categorías macro que agrupan unidades de trabajo, cada una respaldada por su propio archivo semilla. El valor predeterminado proporciona Corporativo, Proyectos y Documentación. Cada Dominio contiene un Glosario y una colección de Temas.

**Temas — iniciativas acotadas en el tiempo.** Temas activos que representan el enfoque estratégico actual, cada uno con un identificador, un nombre, un alcance (táctico o estratégico), una tesis de una línea y palabras clave de gravedad. Los Temas son la parte más volátil de la taxonomía y son genuinamente específicos de cada inquilino — los despliegues reales siembran aquí prioridades estratégicas reales, a menudo comercialmente sensibles, no un conjunto de plantillas genéricas.

## El campo de palabras clave de gravedad

Cada entidad de la taxonomía lleva palabras clave de gravedad, pero su función hoy es más limitada que un clasificador automático: son texto de referencia que un operador humano lee antes de tomar una decisión de clasificación, no una entrada para un sistema automático de coincidencia de palabras clave o similitud de embeddings. En el único consumidor real confirmado de la plataforma — el flujo de trabajo [[radical-proofreader-ui|Verification Surveyor]] — un operador que revisa una entidad descubierta ve la lista de nombres de Arquetipos y elige uno manualmente; las palabras clave de gravedad orientan ese juicio humano en lugar de dirigirlo programáticamente.

El objetivo de explicabilidad para el que se diseñó el campo se mantiene incluso bajo selección manual: un operador puede leer las palabras clave de gravedad de una entidad de la taxonomía y entender por qué una entidad pertenecería o no a ella, y puede editar la lista de palabras clave a mano cuando una categoría necesita redefinirse. Si se añadirá un clasificador automático por palabras clave o por similitud de embeddings sobre este paso manual es un diseño que la plataforma aún no ha construido.

## Diferencia estructural con los enfoques de ontología empresarial

Las plataformas de software empresariales tienden a optimizar sus ontologías para la exhaustividad en todos los clientes posibles. Cualquier cliente específico enfrenta una jerarquía extensa y normalmente necesita personal especializado para configurarla.

La taxonomía semilla optimiza para la acción de un cliente específico. Toda la taxonomía está prevista para ser legible y comprensible por los propios operadores del cliente en una sesión única. La contrapartida es que la taxonomía no se transfiere sin cambios entre clientes — cada paquete vertical es específico de la industria. El beneficio es que el cliente puede operar la taxonomía por sí mismo sin contratar especialistas en ontología.

## Relación con el grafo de conocimiento

La taxonomía sembrada se convierte en la estructura inicial del grafo de conocimiento por inquilino en [[service-content]]. A medida que opera el despliegue, las nuevas entidades descubiertas durante la inferencia (con veredictos aceptados por el [[compounding-doorman|Portero]]) se añaden al grafo, haciendo crecer la taxonomía orgánicamente a partir del uso real.

## Véase También

- [[vertical-seed-packs-marketplace]] — paquetes específicos de la industria que pueblan la taxonomía semilla en el aprovisionamiento
- [[knowledge-graph-grounded-apprenticeship]] — el grafo sembrado es la fuente de fundamentación para la inferencia
- [[customer-owned-graph-ip]] — la taxonomía personalizada del cliente es su propiedad intelectual

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-seed-taxonomy-as-smb-bootstrap.md` (refinado el 30 de abril de 2026).

## Véase también

- [[vertical-seed-packs-marketplace]]
- [[knowledge-graph-grounded-apprenticeship]]
- [[customer-owned-graph-ip]]
