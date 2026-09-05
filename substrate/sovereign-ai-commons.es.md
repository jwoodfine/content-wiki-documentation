---
schema: foundry-doc-v1
title: "Bien común de IA soberana"
slug: sovereign-ai-commons
category: substrate
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-customer-ownership
short_description: "El posicionamiento de PointSav como administrador de infraestructura de IA abierta y compartida para pequeñas y medianas empresas reguladas: cinco propiedades estructurales que los grandes proveedores de servicios en la nube no pueden ofrecer sin desmantelar sus propios modelos de facturación."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "McMahan, B. et al. 'Communication-Efficient Learning of Deep Networks from Decentralized Data.' AISTATS, 2017."
    url: "https://arxiv.org/abs/1602.05629"
paired_with: sovereign-ai-commons.md
---


PointSav construye y administra un bien común de IA soberana: un sustrato, una pila de protocolos y una federación diseñados para que las pequeñas y medianas empresas reguladas puedan ejecutar IA soberana sin ceder la [[customer-owned-graph-ip|propiedad de sus datos]] ni pagar por infraestructura que no controlan.

## El mercado que sirve el bien común

Las PYME reguladas. No las grandes cuentas empresariales — atendidas por plataformas con estructuras de ventas y certificaciones de cumplimiento dimensionadas para contratos anuales de seis cifras. No las aplicaciones de consumo masivo — no reguladas y servidas por productos de masa. El segmento intermedio es donde opera el bien común.

Las características definitorias del cliente objetivo:

- Valor contractual anual para herramientas de IA en el rango de $5,000 a $50,000 — por
  debajo del mínimo económicamente viable para un proceso de venta empresarial
- Exposición regulatoria bajo marcos que incluyen HIPAA, PIPEDA, GDPR, FINRA y
  regulaciones provinciales equivalentes
- Un requisito de que los datos y la infraestructura de IA permanezcan en
  infraestructura que el cliente controla, no en la nube de un proveedor

Pequeñas clínicas, despachos de abogados regionales, asesores financieros de mediana
capitalización, operadores inmobiliarios con archivos de documentos corporativos,
pequeños contratistas del sector público y family offices describen concretamente este
segmento. Estos clientes son, en conjunto, un mercado grande — la economía de las PYME
reguladas es una fracción sustancial de la actividad comercial en los mercados
desarrollados — pero individualmente demasiado pequeños y demasiado regulados para las
plataformas construidas en torno a la economía de hiperescala.

## Lo que es común, lo que es soberano

El código del sustrato, el modelo base, las especificaciones de protocolo y los desarrollos publicados sobre aprendizaje federado son bienes comunes: abiertos, compartidos, mejorados por la contribución colectiva. El [[knowledge-graph-grounded-apprenticeship|grafo de conocimiento]] del cliente, los [[adapter-composition|adaptadores LoRA]] por inquilino, la configuración del inquilino y el [[worm-ledger-architecture|libro de auditoría]] son soberanos: permanecen en la infraestructura del cliente y no salen de ella sin acción explícita del cliente.

Los bienes comunes aumentan el valor de los despliegues soberanos: cada cliente se beneficia de las mejoras al sustrato compartido. Los despliegues soberanos protegen lo que hace único a cada cliente. Ambos están codiseñados, no en tensión.

## Cinco propiedades estructurales no disponibles en otro lugar

El diseño de la plataforma incorpora cinco propiedades que, en conjunto, son estructuralmente inaccesibles para los grandes proveedores de servicios en la nube:

**Soberanía del sustrato.** El código del sustrato es abierto y bifurcable. Un cliente que desee operar de forma independiente del proveedor tiene un camino completo para hacerlo. Para un servicio de nube gestionado, bifurcar el sustrato socavaría el modelo de ingresos; la arquitectura no puede estructurarse de esa manera.

**Inteligencia opcional.** Los Anillos 1 y 2 — todo el manejo determinista de datos y el procesamiento de conocimiento — funcionan completamente sin la capa de IA en el Anillo 3. Los clientes pueden operar la plataforma sin IA, añadir IA cuando tienen un uso específico para ella, y retirarla sin perder el resto del sistema. Véase [[substrate-without-inference-base-case]] para la operación exclusivamente determinista. Para una plataforma donde el cómputo de IA es la principal fuente de ingresos, hacer que la IA sea genuinamente opcional elimina el incentivo comercial.

**Enrutamiento de cómputo multi-nivel.** El [[compounding-doorman|Portero]] selecciona entre un modelo local, una [[yoyo-compute-substrate|instancia de GPU en ráfaga]] y servicios de API externos por solicitud. La selección abarca infraestructura que incluye los modelos de frontera de la competencia en el Nivel C. Ninguna organización controla los tres niveles a la vez, y la configuración de enrutamiento del cliente rige qué nivel maneja cada solicitud.

**Composición federada.** La ruta prevista para mejorar la capacidad de IA de la plataforma implica agrupar señal de entrenamiento preservada con privacidad de los adaptadores LoRA de muchos clientes en mejoras a un modelo base compartido. [^1] Las estructuras de facturación y cumplimiento por inquilino hacen que este arreglo no esté disponible para plataformas donde los datos de cada cliente son custodiados por el proveedor bajo un acuerdo de servicio gestionado.

**Camino de preentrenamiento continuo.** El modelo base es OLMo 3, publicado bajo Apache 2.0 con datos de entrenamiento completos y código de entrenamiento disponibles. Este es el único modelo abierto no chino de 2026 que permite a una organización que lo despliega continuar entrenando la base, partiendo de un punto de control conocido, sobre material de corpus que la propia organización acumula a través del [[trajectory-substrate|sustrato de trayectoria]]. El resultado previsto — un modelo base especializado propiedad del cliente — requiere esta propiedad. No está disponible en ningún modelo cuyos datos de entrenamiento sean cerrados.

## El papel de PointSav

PointSav opera como administrador, no como guardián. La distinción es operativa:

Lo que PointSav hace: opera la pila de protocolos bajo una estructura de gobernanza diseñada para ser transferida a una convención constitucional; cura el modelo base mediante preentrenamiento continuo planificado; opera la infraestructura de federación para el mercado de LoRA y el pool de KV; vende dispositivos ToteboxOS, integración y soporte; y mantiene el despliegue de referencia.

Lo que PointSav no hace: encerrar a los clientes en la infraestructura de PointSav; custodiar datos de clientes bajo un acuerdo de servicio gestionado; cobrar el cómputo de IA como fuente principal de ingresos; competir con los grandes proveedores de nube en volumen de IA en la nube.

## Trayectoria prevista hacia 2030

La trayectoria prevista del bien común para los próximos años, según se planifica actualmente:

Para 2030, el resultado previsto incluye una variante de modelo PointSav-OLMo-N competitiva con los modelos propietarios de frontera en tareas de PYME reguladas; una base de despliegues de clientes SMB activos en la federación; una pila de protocolos versionada que ha sido ratificada mediante convención constitucional; y el reconocimiento como implementación de referencia de infraestructura de IA abierta para el mercado de PYME reguladas.

Estas son declaraciones de futuro basadas en el diseño y la trayectoria actuales de la plataforma. Llevan supuestos materiales: que los términos de licencia de OLMo 3 permanecen vigentes, que los costos de cómputo GPU continúan disminuyendo, que las técnicas de aprendizaje federado subyacentes al mercado siguen siendo viables a escala, y que la plataforma alcanza la base de clientes necesaria para financiar el preentrenamiento continuo. Cada supuesto podría verse alterado. El fundamento estructural de la trayectoria está en su lugar; la ejecución aún debe demostrarse.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales en detalle arquitectónico
- [[economic-model]] — la estructura comercial de dos niveles que financia el bien común
- [[llm-substrate-decision]] — por qué OLMo 3 permite el camino de preentrenamiento continuo
- [[four-tier-slm-substrate]] — los cuatro niveles de despliegue por los que avanzan los clientes
