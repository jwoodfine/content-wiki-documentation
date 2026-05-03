---
schema: foundry-doc-v1
title: "El Bien Común de IA Soberana"
slug: sovereign-ai-commons.es
category: architecture
type: topic
quality: published
short_description: "El posicionamiento de PointSav como administrador de infraestructura de IA abierta y compartida para pequeñas y medianas empresas reguladas: cinco propiedades estructurales que los grandes proveedores de servicios en la nube no pueden ofrecer sin desmantelar sus propios modelos de facturación."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: sovereign-ai-commons.md
---

PointSav construye y administra un bien común de IA soberana: un sustrato, una pila de protocolos y una federación diseñados para que las pequeñas y medianas empresas reguladas puedan ejecutar IA soberana sin ceder la propiedad de sus datos ni pagar por infraestructura que no controlan.

## El mercado que sirve el bien común

Las PYME reguladas. No las grandes cuentas empresariales — atendidas por plataformas con estructuras de ventas y certificaciones de cumplimiento dimensionadas para contratos anuales de seis cifras. No las aplicaciones de consumo masivo — no reguladas y servidas por productos de masa. El segmento intermedio es donde opera el bien común.

Las características definitorias del cliente objetivo: valor contractual anual para herramientas de IA entre $5,000 y $50,000; exposición regulatoria bajo marcos como HIPAA, PIPEDA, GDPR, FINRA y equivalentes provinciales canadienses; y un requisito de que los datos y la infraestructura de IA permanezcan bajo el control del propio cliente.

## Lo que es común, lo que es soberano

El código del sustrato, el modelo base, las especificaciones de protocolo y los desarrollos publicados sobre aprendizaje federado son bienes comunes: abiertos, compartidos, mejorados por la contribución colectiva. El grafo de conocimiento del cliente, los adaptadores LoRA por inquilino, la configuración del inquilino y el libro de auditoría son soberanos: permanecen en la infraestructura del cliente y no salen de ella sin acción explícita del cliente.

Los bienes comunes aumentan el valor de los despliegues soberanos: cada cliente se beneficia de las mejoras al sustrato compartido. Los despliegues soberanos protegen lo que hace único a cada cliente. Ambos están codiseñados, no en tensión.

## Cinco propiedades estructurales no disponibles en otro lugar

El diseño de la plataforma incorpora cinco propiedades que, en conjunto, son estructuralmente inaccesibles para los grandes proveedores de servicios en la nube:

1. **Soberanía del sustrato.** El código es abierto y bifurcable; un cliente que desee operar de forma independiente del proveedor tiene un camino completo para hacerlo.
2. **Inteligencia opcional.** Los anillos 1 y 2 — todo el procesamiento determinista — funcionan completamente sin la capa de IA en el anillo 3.
3. **Enrutamiento de cómputo de múltiples capas.** El Doorman selecciona entre modelo local, ráfaga GPU y API externas por solicitud, incluyendo modelos frontier de terceros en la Capa C.
4. **Composición federada.** La señal de entrenamiento preservada con privacidad de múltiples adaptadores LoRA de clientes puede agregarse para mejorar el modelo base compartido.
5. **Camino de preentrenamiento continuo.** El modelo base OLMo 3 publica datos de entrenamiento, código y puntos de control bajo licencias que permiten continuar el preentrenamiento desde un punto conocido sobre corpus propio.

## El papel de PointSav

PointSav opera como administrador, no como guardián: opera la pila de protocolos bajo una estructura de gobernanza diseñada para ser transferida a una convención constitucional; planifica el preentrenamiento continuo del modelo base; opera la infraestructura de federación; y vende instalaciones ToteboxOS, integración y soporte.

Lo que PointSav no hace: retener a los clientes mediante dependencia de infraestructura propietaria; custodiar datos de clientes bajo acuerdos de servicio gestionado; cobrar el cómputo de IA como fuente principal de ingresos.

## Trayectoria prevista hacia 2030

La trayectoria prevista, como se planifica actualmente, contempla para 2030 un modelo PointSav-OLMo-N competitivo con modelos frontier propietarios en tareas de PYME reguladas; una base de clientes activos en la federación; y una pila de protocolos ratificada a través de convención constitucional. Estas son declaraciones de futuro basadas en el diseño y la trayectoria actuales de la plataforma, sujetas a supuestos materiales que podrían verse afectados por cambios en el entorno tecnológico, regulatorio o de mercado.

## Ver también

- [[compounding-substrate]] — las cinco propiedades estructurales en detalle arquitectónico
- [[economic-model]] — la estructura comercial de dos niveles que financia el bien común

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
