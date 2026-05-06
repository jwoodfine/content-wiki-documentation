---
schema: foundry-doc-v1
type: topic
slug: sovereign-airlock-doctrine
title: La Doctrina del Exclusa Soberana (Sovereign Airlock)
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: sovereign-airlock-doctrine.md
## Véase también

- [[sovereign-ai-routing]]
- [[machine-based-auth]]
- [[service-slm]]
- [[capability-based-security]]

---


La Doctrina del Exclusa Soberana establece los protocolos obligatorios de seguridad e identidad para la transmisión de datos y el despliegue de código en Foundry. Al separar estrictamente las identidades del Proveedor (PointSav) y del Cliente (Woodfine), garantizamos la integridad operativa y el control total de los activos digitales.

## Arquitectura de Cuatro Silos

La infraestructura se organiza en cuatro silos aislados:
- **factory-pointsav/:** Fuente del Proveedor. Código base propiedad de PointSav AG.
- **fleet-woodfine/:** Operaciones del Cliente. Datos exclusivos de Woodfine Management Corp.
- **stage-pwoodfine/:** Exclusa de Ingeniería. Entorno de pruebas para ingenieros.
- **stage-jwoodfine/:** Exclusa de Operaciones. Entorno de pruebas operativo.

## El Protocolo de Exclusa

Está prohibido editar directamente en las carpetas `stage-*`. El flujo de información es unidireccional y controlado:
1. **Desarrollo:** Los cambios se realizan solo en las carpetas de origen.
2. **Sincronización:** Se copian los datos a la exclusa eliminando metadatos innecesarios.
3. **Verificación:** Se audita la corrección de los archivos.
4. **Transmisión:** Se envían los datos usando llaves SSH específicas y aisladas para cada identidad.
5. **Finalización:** Un administrador realiza la fusión final hacia los repositorios de la organización.

Esta doctrina asegura que ningún fallo de seguridad individual pueda comprometer la separación entre la infraestructura del proveedor y los datos críticos del cliente.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
