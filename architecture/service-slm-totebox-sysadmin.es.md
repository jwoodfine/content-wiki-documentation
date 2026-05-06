---
title: "service-slm como Administrador del Sistema Totebox"
slug: service-slm-totebox-sysadmin.es
category: architecture
status: stable
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
---

`service-slm` — el Portero — es el administrador del sistema operativo y el centro de soporte previsto para los despliegues de Totebox Archive y Totebox Orchestration. Este documento delimita lo que el modelo necesita saber, cómo se captura ese conocimiento de las operaciones reales y la trayectoria del producto para el cliente en tres niveles que resulta de ello.

## Las diez familias de tareas operativas del Totebox

Una encuesta de los archivos de guías operativas en los despliegues activos produce una taxonomía clara de lo que un administrador del sistema Totebox maneja día a día:

- **Aprovisionamiento de nodos**: secuencia de arranque físico: alimentación, unidad de arranque, protocolo de enlace MBA, montaje de contenedor aislado, Estándar Diodo, bloqueo del terminal.
- **Operaciones de entrada**: programación del recolector de API de grafos, monitorización del bucle de síntesis, vigilante del daemon de spool.
- **Extracción de datos soberanos (DARP)**: extracción de grafo de conocimiento y libro mayor verificado a local; verificación de destrucción del archivo temporal en la nube.
- **Egreso de almacenamiento en frío**: rsync trimestral a unidad segura adjunta; verificación de integridad.
- **Supervisión de ejecución SLM**: revisión de extracciones de IA en bruto (borradores) frente a libro mayor verificado (finalizado); decisiones de avance.
- **Operaciones de búsqueda soberana**: mantenimiento del índice Tantivy; diagnóstico de consultas booleanas.
- **Operaciones de identidad y capacidad**: credenciales de inquilino aisladas; gestión de claves de Zero-Touch Parser; protocolo de enlace MBA por nodo.
- **Inyección de adaptadores**: colocación de adaptador privado por inquilino; validación de límite de volumen; verificación de conformidad con el Estándar Diodo.
- **Reconciliación de pista de auditoría**: verificación cruzada del libro mayor de auditoría por inquilino frente al Libro Mayor Inmutable WORM; verificación del ancla de Sigstore Rekor.
- **Importación de datos conforme al esquema**: validación del término canónico del Glosario; mapeo de Arquetipos; conformidad con la gramática de etiquetas estructurales YAML.

## Por qué service-slm en lugar de una API externa

Cuatro propiedades estructurales hacen que estas cargas de trabajo sean especialmente adecuadas para el Portero local:

**Soberanía**: cada familia de tareas toca datos del inquilino. Enviar consultas rutinarias de administración del sistema a una API externa es una ruptura estructural de soberanía que la arquitectura del Portero previene por construcción.

**Velocidad**: la inferencia local de Nivel A y el Yo-Yo de Nivel B responden en segundos. Una latencia de diez segundos por paso en una secuencia de aprovisionamiento de nueve pasos marca la diferencia entre un asistente útil y uno frustrante.

**Forma de costes**: el coste amortizado de Nivel B en el sustrato Yo-Yo planificado supone aproximadamente $0,0001 por consulta de administración del sistema típica — muy por debajo del equivalente de API externa una vez que las instrucciones incluyen el contexto del inquilino.

**Personalización**: los adaptadores LoRA por clúster entrenados en los patrones operativos propios del cliente hacen que service-slm sea un asistente mucho mejor para ese cliente que cualquier modelo genérico.

## Trayectoria del producto en tres niveles

**Nivel 1 — Cliente pyme de un único Totebox**: OLMo 3 7B Q4 ejecutándose localmente en el dispositivo del cliente. El Portero maneja las consultas rutinarias de administración del sistema. Soberanía completa; sin flujo de datos al lado del proveedor para operaciones rutinarias.

**Nivel 2 — Cliente multi-Totebox (planificado)**: el mismo sustrato más una suscripción a Nivel B Yo-Yo (32B Think) alojado por el proveedor. Los adaptadores LoRA por clúster entrenados en el corpus de tipos de tareas del cliente despliegan en el Nivel B. El precio está previsto que sea estructuralmente inferior a las ofertas de código cerrado comparables. Sujeto a la tasa de acumulación del corpus y a los precios de cómputo en el momento del despliegue.

**Nivel 3 — Producto especializado PointSav-LLM (planificado)**: PointSav-OLMo-N alojado por el proveedor, con preentrenamiento continuo. La IA resuelve entre un 80 y un 90% previsto de las consultas de los clientes de forma autónoma; los humanos en el bucle gestionan las escaladas; cada respuesta del Nivel L2 retroalimenta el corpus de aprendizaje. El calendario de despliegue y los precios son objetivos planificados sujetos a la acumulación del corpus y la disponibilidad de cómputo.

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ y Foundry™ son marcas no registradas de Woodfine Capital Projects Inc.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
