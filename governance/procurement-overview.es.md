---
schema: foundry-doc-v1
title: "Resumen de adquisición"
slug: procurement-overview.es
short_description: "Lo que un comprador regulado adquiere al implementar PointSav: hardware que el cliente posee íntegramente, datos que el proveedor nunca posee, sin compromiso de gasto mínimo, y propiedades de cumplimiento ejecutadas por arquitectura en lugar de promesas contractuales."
lang: es
category: governance
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: procurement-overview.md
---

PointSav entrega una plataforma de datos sobre hardware que el cliente posee por completo. No hay nube compartida, no hay claves de cifrado en manos del proveedor, y no se requiere un compromiso de gasto mínimo para alcanzar una infraestructura de grado regulatorio. Cada registro que el cliente escribe vive en el almacenamiento propio del cliente desde el momento en que se escribe, y puede presentarse a un regulador sin coordinar con el proveedor.

Cada artefacto incluye un script de arranque que levanta toda la pila en una máquina que el cliente proporciona — sin dependencia SaaS, sin inicio de sesión con el proveedor, sin API en la nube con medición. Un cliente que rescinde la relación conserva todos los registros que escribió, todos los adaptadores de IA que financió y el libro de auditoría completo de cada acción tomada sobre sus datos.

La arquitectura de tres anillos de la plataforma separa la ingesta en el límite (Anillo 1), el procesamiento determinista (Anillo 2) y la inferencia de IA opcional (Anillo 3). La IA nunca escribe en el registro autoritativo; esa ruta pertenece exclusivamente a los servicios deterministas del Anillo 2. Un despliegue que excluye el Anillo 3 por completo sigue entregando toda la pila de gestión de registros de grado regulatorio.

Para un comprador regulado bajo obligaciones de divulgación continua, esta arquitectura tiene una consecuencia concreta en términos de auditoría: el registro autoritativo está en hardware que el comprador controla, el libro es criptográficamente de solo anexado, y el comprador puede satisfacer la solicitud de registros de un regulador sin depender de la operación continuada del proveedor. `[ni-51-102]`

## Qué posee el cliente

Tres propiedades están garantizadas estructuralmente — no prometidas contractualmente:

**Los datos.** Cada registro escrito por un servicio del Anillo 1 se escribe en el almacenamiento local del cliente en formato WORM de solo anexado. La red del proveedor nunca transporta el contenido no cifrado del registro del cliente.

**Los adaptadores.** Cuando el adaptador de IA opcional del cliente entrena sobre el corpus del cliente, los pesos del modelo resultante viven dentro del sustrato del cliente — no en los servidores del proveedor. Los registros del corpus privados del inquilino nunca atraviesan la red del proveedor.

**El libro de auditoría.** El libro de auditoría por inquilino — el registro de cada acción editorial, cada llamada de inferencia de IA, cada ingesta de datos — vive en el despliegue del cliente. Una interrupción del proveedor no impide que el cliente presente este libro a un regulador.

## Estructura comercial (planificada)

Por `[osc-sn-51-721]`, lo siguiente describe la trayectoria comercial planificada.

**Nivel Abierto (sin costo).** Acceso de lectura a los recursos comunitarios, foro comunitario y documentación pública. El punto de entrada previsto para colaboradores individuales y organizaciones que evalúan la plataforma.

**Nivel C de pago (por token, suscripción).** Acceso al modelo especialista planificado [[pointsav-llm|PointSav-LLM]] a través del Portero local del cliente. Precio por token destinado a ser accesible a tamaños de contrato PYME — sin gasto mínimo de nivel empresarial.

**Nivel C+ de pago (premium).** Acceso por token más horas de escalado reservadas para soporte humano en el bucle L2/L3. Los clientes que contribuyen con datos de trayectoria al corpus de entrenamiento están destinados a recibir tarifas por token preferenciales en ciclos de facturación posteriores.

## Propiedades de cumplimiento

La postura de cumplimiento de la plataforma es estructural, no procedimental. El cumplimiento no se logra mediante controles de política que un administrador con errores de configuración pueda anular — se logra mediante la arquitectura del motor de almacenamiento y los límites del servicio.

- **Inmutabilidad de registros.** El libro WORM satisface la Regla SEC 17a-4(f), la preservación de registros electrónicos cualificados de eIDAS y SOC 2. La modificación no está prohibida a nivel de política; está prohibida por el motor de almacenamiento, que no tiene operación de eliminación ni sobreescritura.
- **Pista de auditoría de IA.** Cada llamada de inferencia de IA pasa por el Portero y genera una fila de auditoría en el libro local del cliente. La puerta de enlace del proveedor genera una segunda fila de auditoría simultáneamente.
- **Divulgación continua BCSC.** La plataforma produce registros de grado de divulgación continua como salida estructural del procesamiento del Anillo 2. Un emisor informante bajo NI 51-102 que despliega la plataforma dentro de su propio sustrato puede satisfacer las obligaciones de divulgación continua contra registros que posee y controla.
- **Residencia de datos.** Los datos del cliente nunca salen del hardware designado del cliente excepto a través de una llamada de egreso explícita auditada en el libro.

## Véase también

- [[customer-hostability]] — el compromiso arquitectónico que hace estructurales las propiedades de adquisición
- [[architecture-decisions]] — las doce decisiones de ingeniería vinculantes, incluidas las reglas de separación de datos y autoridad de IA
- [[compliance-and-continuous-disclosure]] — cómo la plataforma produce registros de grado de divulgación continua
- [[worm-ledger-design]] — el libro WORM que satisface SEC 17a-4(f), eIDAS y SOC 2 por estructura
- [[economic-model]] — la estructura comercial de dos niveles y su justificación
- [[security-overview]] — la arquitectura de seguridad de la plataforma para la debida diligencia técnica
