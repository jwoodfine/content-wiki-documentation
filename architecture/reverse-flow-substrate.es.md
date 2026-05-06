---
schema: foundry-doc-v1
title: "Substrato de Flujo Inverso"
slug: reverse-flow-substrate.es
category: architecture
type: topic
quality: published
short_description: "La puerta de enlace del Portero y el registro de auditoría que aplican la disciplina de datos de entrada están planificados para también aplicar flujos comerciales de salida — mercado de datos e intercambio de anuncios — ambos opt-in por inquilino."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: reverse-flow-substrate.md
---

El **Substrato de Flujo Inverso** es la extensión planificada de la puerta de enlace del Portero, el registro de auditoría y el identificador de módulo por inquilino para gobernar los flujos comerciales de salida. La misma frontera que media las solicitudes de inferencia de entrada está prevista para también mediar dos flujos de salida: un mercado de datos y un intercambio de anuncios. Ambos están planificados como opt-in por inquilino, estructuralmente deshabilitados por defecto, y requieren procedencia criptográfica por registro. Este patrón codifica la reclamación doctrinal #52.

## Los dos flujos inversos planificados

**Mercado de Datos.** El grafo de conocimiento acumulado, el registro de auditoría y los pesos del adaptador entrenado del cliente están previstos para ser activos vendibles. La puerta de enlace del mercado planificada (`service-marketplace`) está prevista para exponer el inventario por inquilino a compradores externos. Las categorías de inventario planificadas incluyen consultas agregadas anonimizadas contra el grafo por inquilino, pesos del adaptador entrenado vendibles a otros inquilinos en la misma vertical con permiso explícito, material de wiki de contenido curado con términos de consentimiento y licencia, y tuplas de corpus firmadas con veredicto con procedencia criptográfica para compradores de datos de entrenamiento de IA.

**Intercambio de Anuncios.** El cliente tiene previsto operar como vendedor y comprador en un intercambio de pujas en tiempo real conforme a estándares. Como vendedor, la audiencia propia del cliente — con consentimiento por registro y clasificación de intención de IA — está prevista para ser inventario de subasta en tiempo real. Como comprador, el adaptador del cliente puede clasificar la intención de su propia audiencia para apoyar campañas de salida dirigidas.

## Disciplina de opt-in por inquilino

Los flujos inversos están estructuralmente deshabilitados por defecto. Habilitarlos requiere que el operador se autentique como la identidad principal del inquilino, ejecute el comando de habilitación apropiado en la TUI y complete un flujo de consentimiento guiado. La configuración es firmada por la clave de identidad del operador y se registra en el registro de auditoría. No existe ninguna ruta de API que habilite el mercado o el intercambio de anuncios sin consentimiento firmado por el operador.

## Registro de auditoría como prueba de derechos

Cada transacción planificada en cualquiera de los flujos inversos está prevista para registrar los términos de consentimiento vigentes en el momento de la transacción, la cadena de auditoría desde los datos fuente hasta el elemento de inventario, la identidad del comprador y el evento de liquidación. El registro de auditoría es el registro legalmente admisible previsto de que los datos se vendieron con consentimiento y que no se produjo ninguna fuga de datos entre inquilinos.

## Aislamiento por inquilino en los flujos inversos

La misma disciplina de identificador de módulo que impide la traversal de grafo entre inquilinos también impide la fuga de inventario entre inquilinos. Los listados del mercado están delimitados por inquilino; un comprador no puede consultar entre inquilinos sin concesiones explícitas por inquilino. El inventario de impresiones del intercambio de anuncios usa tokens opacos delimitados por inquilino; el comprador nunca ve la audiencia subyacente del inquilino.

## Composición con otros principios

Los flujos inversos planificados dependen de [[single-boundary-compute-discipline]], [[customer-owned-graph-ip]] y [[direct-payment-settlement]]. La disciplina de límite único asegura que el tráfico de monetización pase por la misma frontera de auditoría que la inferencia. La propiedad del grafo del cliente establece que el inventario es su propiedad intelectual y que las decisiones de monetización son del cliente. El acuerdo de pago directo garantiza que los ingresos de la monetización de la PI del cliente lleguen directamente al cliente.

## Véase También

- [[customer-owned-graph-ip]] — el principio de propiedad que hace que los flujos inversos sean una decisión controlada por el cliente
- [[direct-payment-settlement]] — el mecanismo de pago planificado para las transacciones del mercado y el intercambio de anuncios
- [[vertical-seed-packs-marketplace]] — los paquetes planificados como inventario de primera clase del mercado
- [[single-boundary-compute-discipline]] — la frontera del Portero que gobierna los flujos de salida además de los de entrada

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-reverse-flow-substrate.md` (refinado el 30 de abril de 2026). Todas las reclamaciones de mercado, intercambio de anuncios y liquidación llevan encuadre "planificado," "previsto" y "está previsto para" conforme a la postura de divulgación continua BCSC.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
