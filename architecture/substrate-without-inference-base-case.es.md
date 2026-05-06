---
schema: foundry-doc-v1
title: "El Substrato sin Inferencia — El Caso Base"
slug: substrate-without-inference-base-case.es
category: architecture
type: topic
quality: published
short_description: "El Archivo Totebox permanece completamente operativo y transferible libremente incluso cuando no hay ningún nivel de inferencia de IA disponible; el substrato determinístico es la base estructural."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: substrate-without-inference-base-case.md
---

El **Substrato sin Inferencia — El Caso Base** establece que el Archivo Totebox debe permanecer completamente operativo y transferible libremente incluso cuando `service-slm` no puede ejecutar ninguna inferencia. La inferencia de IA es un valor añadido. El substrato determinístico — el registro de archivos, el grafo de conocimiento, el pipeline de extracción y los servicios editoriales — es la base estructural. Esta distinción está codificada en la reclamación doctrinal #54.

## Lo que requiere el caso base

Cuando los tres niveles de cómputo (especialista local, GPU en ráfaga y API externa) están simultáneamente no disponibles, todos los servicios determinísticos deben seguir siendo operativos: el registro de archivos WORM (`service-fs`), el motor de conocimiento (`service-content`), el servicio de entrada, el servicio de extracción en su capa de análisis determinístico, el servicio de salida, y los servicios de personas, email y archivos. El Portero está vinculado y escuchando, devolviendo 503 a los endpoints de inferencia mientras mantiene los endpoints de salud y contrato siempre respondiendo. La TUI del operador funciona en modo solo-determinístico.

El caso base también cubre los servicios de mercado y liquidación cuando están habilitados: las transacciones pueden proceder sin fundamentación asistida por IA; los registros de auditoría y consentimiento siguen siendo aplicados.

## El flujo de transferencia de propiedad

La propiedad "transferible libremente" está implementada a través de un flujo de transferencia estructurado. El operador ejecuta un comando de preparación de transferencia para producir un paquete autónomo y firmado criptográficamente: el instantáneo del grafo por inquilino, el registro de auditoría, los pesos del adaptador entrenado, la taxonomía semilla, el manifiesto del paquete y la configuración del inquilino. El paquete es firmado por la clave de identidad del operador y su integridad está anclada en un registro de transparencia criptográfica público.

La parte receptora importa el paquete en un Totebox nuevo. Las operaciones determinísticas funcionan inmediatamente con el estado importado. Las operaciones asistidas por IA están disponibles cuando el nuevo operador configura el nivel de cómputo.

## Por qué esto importa comercialmente

La propiedad transferible libremente distingue un activo soberano de una suscripción a un servicio. Cuando se vende un negocio, el nuevo propietario importa el paquete del Totebox y tiene el historial operativo completo disponible inmediatamente — el grafo de conocimiento, el registro de auditoría y el vocabulario del flujo de trabajo — sin re-suscribirse a ninguna plataforma ni contratar consultores de migración.

Cuando se disuelve o divide un negocio, cada parte recibe su porción del grafo como un artefacto portátil firmado criptográficamente. En una adquisición corporativa, el sistema adquirente importa el paquete del Totebox y tiene el historial operativo con procedencia verificable disponible de inmediato.

Si Foundry cesa sus operaciones, el cliente continúa operando su Totebox indefinidamente. El substrato determinístico funciona sin Foundry. El cliente pierde la capacidad de recibir nuevos paquetes verticales y de transaccionar en el mercado de Foundry, pero sus operaciones existentes no se detienen.

## Requisito de implementación

El caso base restringe cada implementación de servicio. Cada servicio debe tener una base determinística que funcione sin IA. Las operaciones mejoradas por IA se documentan como que requieren el nivel de IA y se degradan elegantemente cuando no está disponible. La regresión en la base determinística — cualquier servicio que falla cuando todos los niveles están inactivos — es una señal a nivel doctrinal de que una función de soporte de carga ha sido hecha dependiente de la IA.

## Véase También

- [[tier-zero-customer-side-sovereign-specialist]] — el despliegue del Nivel 0 que este caso base garantiza
- [[customer-owned-graph-ip]] — el derecho de propiedad que el flujo de transferencia ejercita
- [[single-boundary-compute-discipline]] — el comportamiento del Portero en el caso base (503 desde los endpoints de inferencia; los endpoints de salud siempre responden)

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-substrate-without-inference-base-case.md` (refinado el 30 de abril de 2026). Las referencias al flujo de transferencia y al mercado llevan encuadre "previsto" donde la implementación de la Fase 5 está pendiente. Postura de divulgación continua BCSC aplicada.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
