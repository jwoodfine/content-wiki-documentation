---
schema: foundry-doc-v1
title: "Propiedad Intelectual del Grafo del Cliente"
slug: customer-owned-graph-ip.es
category: architecture
type: topic
quality: published
short_description: "El grafo de conocimiento por inquilino y los pesos del adaptador entrenado son propiedad intelectual del cliente, portátiles y exportables sin aprobación del proveedor."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: customer-owned-graph-ip.md
---

La **Propiedad Intelectual del Grafo del Cliente** es el principio por el cual el grafo de conocimiento por inquilino mantenido en `service-content` es propiedad intelectual del cliente, no un subproducto del uso de la plataforma Foundry. Los adaptadores del modelo entrenados con el corpus de ese cliente también son propiedad del cliente. Este principio codifica la reclamación doctrinal #48.

## Lo que significa la propiedad operacionalmente

Cada nodo, arista, mutación y entrada del registro de auditoría con alcance en el identificador de módulo de un inquilino es propiedad de ese inquilino. Foundry no tiene derecho a agregar, revender ni usar los datos del grafo del inquilino fuera de los consentimientos explícitos por inquilino definidos en otras partes de la Doctrina.

La propiedad conlleva cuatro propiedades operacionales: exportación en cualquier momento mediante un único comando que produce un paquete completo en formatos abiertos; sin bloqueo de formato (volcado Cypher para el grafo, JSONL para el registro de auditoría, formatos de tensor estándar para los pesos del adaptador); sin licencia agregada (Foundry no retiene derechos para usar los datos del cliente en el entrenamiento de modelos entre inquilinos sin consentimiento explícito); y transferencia de propiedad sin involucrar a Foundry.

## Por qué esto invierte el patrón SaaS

La mayoría de las plataformas de software empresariales moldean los datos del cliente según la ontología del proveedor. Cuando un cliente intenta salir, los datos deben re-moldearse para adaptarse al sistema de destino — un proyecto de migración que típicamente requiere cooperación del proveedor y personal especializado.

El enfoque de Foundry invierte esto. Los datos del cliente son moldeados por su propia taxonomía semilla. La exportación es una operación de un solo comando que produce un paquete en formato abierto. El acceso del cliente a sus datos no depende de que los servidores de Foundry permanezcan operativos.

El complemento económico es el modelo de comisión por transacción: el cliente paga a Foundry una comisión solo cuando gana de sus datos, no una suscripción recurrente por acceso a sus propios registros.

## Aislamiento por inquilino

El identificador de módulo que determina el alcance de cada grafo también lo aísla. El grafo de conocimiento y el corpus de entrenamiento de un inquilino no pueden ser accedidos por otro inquilino ni utilizados para entrenar el adaptador de otro inquilino. Los límites son estructurales, no de política.

## Véase También

- [[seed-taxonomy-as-smb-bootstrap]] — la taxonomía semilla personalizada del cliente es parte de su propiedad intelectual
- [[reverse-flow-substrate]] — mecanismos planificados para monetizar activos del grafo del cliente
- [[direct-payment-settlement]] — el modelo de pago que hace que la propiedad del cliente sea comercialmente significativa
- [[substrate-without-inference-base-case]] — el flujo de transferencia de propiedad que hace ejercitable el derecho de propiedad

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-customer-owned-graph-ip.md` (refinado el 30 de abril de 2026). Las reclamaciones de monetización llevan encuadre "planificado" y "opt-in" conforme a la postura de divulgación continua BCSC.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
