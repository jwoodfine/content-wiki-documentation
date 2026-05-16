---
schema: foundry-doc-v1
title: "compliance-and-continuous-disclosure"
slug: compliance-and-continuous-disclosure
category: governance
type: concept
quality: complete
short_description: "Cumplimiento y divulgación continua describe los marcos regulatorios que aborda la arquitectura PointSav y el enfoque estructural que adopta para exponer evidencia de auditoría de forma continua, en lugar de mediante ciclos anuales de certificación puntual."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: compliance-and-continuous-disclosure.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
 - id: 1
 text: "NIST, Open Security Controls Assessment Language (OSCAL) — formatos legibles por máquina para representar catálogos de controles de seguridad, líneas base, planes de seguridad del sistema y resultados de evaluaciones."
 url: "https://pages.nist.gov/OSCAL/"
 - id: 2
 text: "Organización Internacional de Normalización, ISO/IEC 42001:2023 — Sistema de Gestión de Inteligencia Artificial (AIMS): requisitos para organizaciones que gestionan sistemas de IA de manera responsable."
 url: "https://www.iso.org/standard/81230.html"
---

Cumplimiento y divulgación continua describe los marcos regulatorios que aborda la arquitectura PointSav y el enfoque estructural que adopta para evidenciar esos controles. El cumplimiento empresarial convencional se basa en auditorías anuales en un momento puntual: un auditor examina una muestra, produce un informe escrito y el cliente posee un certificado que puede quedar desactualizado semanas después de su emisión. El sustrato PointSav está diseñado para un modelo continuo: controles legibles por máquina que se actualizan en tiempo real y exponen una superficie de atestación consultable. Todas las certificaciones de cumplimiento y objetivos de marcos descritos aquí son planificados o previstos; se aplica lenguaje prospectivo en todo momento según los requisitos de divulgación continua de valores canadienses [ni-51-102] [osc-sn-51-721]. Al finalizar este artículo, el lector comprenderá los objetivos del marco de cumplimiento, el enfoque de controles estructurales y la disciplina de estado de documentos que aplica la arquitectura.

## Cómo la prueba continua reemplaza los ciclos de auditoría anuales

La limitación de la auditoría en un momento puntual es arquitectónica: un certificado emitido después de un período de evaluación de seis meses es preciso para ese período y potencialmente inexacto en cada momento posterior. Para los clientes que gestionan registros regulados — Emisores de información, profesionales médicos, profesionales legales — la brecha entre la evaluación y la postura actual es una responsabilidad.

El sustrato PointSav aborda esto colocando controles a un nivel donde no pueden ser evitados administrativamente: si un control puede ser desactivado por un administrador, es una política. Si no puede ser desactivado, es una garantía arquitectónica. El enfoque previsto mueve los controles de la capa de políticas al nivel del sistema — por debajo del sistema operativo — para que el registro de auditoría no sea una función que fue habilitada, sino una propiedad estructural que nunca estuvo ausente. [^1]

## Marcos de cumplimiento que aborda la arquitectura

| Marco | Tipo | Lo que proporciona la arquitectura |
|---|---|---|
| SOC 3 (Controles del Sistema y la Organización 3) | Confianza operativa | Planeado: controles continuos sobre Seguridad, Disponibilidad, Integridad de Procesamiento, Confidencialidad, Privacidad |
| Paquete de Resolución de Activos Digitales (DARP) | Soberanía estructural | Planeado: segregación criptográfica de activos para que permanezcan transferibles ante el fallo del proveedor |
| OSCAL (Lenguaje de Evaluación de Controles de Seguridad Abierto de NIST) [^1] | Cumplimiento legible por máquina | Planeado: manifiestos en `oscal-manifests/` por repositorio; ciclo de autoauditoría de 60 segundos |
| ISO 19650 | Gestión de registros | Sufijos de estado de documentos aplicados en artefactos BIM e inmobiliarios |
| ISO/IEC 42001:2023 — Sistema de Gestión de IA [^2] | Transparencia algorítmica | Planeado: registro inmutable de cada decisión de enrutamiento de IA a través del límite de auditoría del [[doorman-protocol\|Portero]] |
| DORA (Ley de Resiliencia Operativa Digital de la UE) | Regulación sectorial de la UE | Objetivo: apoya los despliegues previstos de clientes en la UE |
| FedRAMP | Gobierno de EE.UU. | Objetivo: apoya los despliegues previstos en el sector público de EE.UU. |
| GDPR | Privacidad en la UE | Objetivo: apoya el cumplimiento previsto de privacidad en la UE |
| BCSC (NI 51-102, OSC SN 51-721) [ni-51-102] [osc-sn-51-721] | Divulgación continua | Todas las afirmaciones prospectivas llevan lenguaje de planeado/previsto/puede/objetivo |
| SLSA (Niveles de la Cadena de Suministro para Artefactos de Software) | Integridad de la cadena de suministro | Planeado: atestación de construcción del lado del proveedor |
| ISO 15489 | Gestión de registros | Convenciones de nomenclatura de documentación del repositorio |
| ISO 24495-1 | Lenguaje claro | Disciplina de voz y tono para las salidas de [[service-content\|service-content]] |

"Objetivo" en la tabla significa que la arquitectura está diseñada teniendo en cuenta los requisitos del marco; la certificación contra ese marco está prevista pero no se ha obtenido.

## Controles diseñados por debajo del sistema operativo

Dos componentes están planeados a nivel del sistema para asumir las obligaciones de SOC 3 y DARP:

| Componente planeado | Función |
|---|---|
| `service-audit` | Un registro de solo adición inmutable previsto que se ejecutará junto al gestor basado en capacidades. Cada comunicación de un [[totebox-os\|Totebox]] con el exterior está previsto que registre el enrutamiento de capacidades en el log del micronúcleo. Dado que el componente está previsto para ejecutarse por debajo del SO, un administrador no podría deshabilitarlo sin deshabilitar el sistema operativo. |
| `service-resolution` | El empaquetador criptográfico planeado para DARP. Previsto para garantizar que cada Totebox esté estructuralmente segregado. Ante el fallo del proveedor o la detención deliberada del sistema, este componente planeado separará los datos y los devolverá limpiamente al propietario legal. |

El principio de diseño es que los controles en la capa de políticas son válidos hasta que un administrador los anula; los controles a nivel del sistema no pueden anularse sin detener el sistema.

## Los tres activos que constituyen la Prueba Continua

Cuando el panel previsto sea realizado, está previsto que exponga tres activos legibles por máquina que juntos constituyen lo que la arquitectura llama Prueba Continua:

| Activo planeado | Contenidos |
|---|---|
| Lista de Materiales de Hardware (HBOM) | Cada componente de hardware en el perfil de referencia de [[os-workplace\|os-workplace]] del cliente |
| Lista de Materiales de Software (SBOM) | Cada dependencia usada en el sustrato desplegado del cliente |
| Registro de Auditoría en Tiempo Real | El latido operativo actual del [[diode-standard\|Estándar Diodo]], previsto para ser consultable bajo demanda por los propios sistemas de gestión de riesgos del cliente |

Los tres son salidas planeadas; el plazo de entrega previsto no se publica aquí.

## Convenciones de sufijos de estado de documentos ISO 19650

La arquitectura adopta los códigos de estado de documentos ISO 19650 como convenciones de sufijos de nombres de archivo.

| Sufijo | Estado ISO 19650 | Significado |
|---|---|---|
| `_JW` | S0 | Trabajo en curso — borrador, aún no compartido |
| `_FIN` | S4 | Final, compartido para aprobación o coordinación |
| `_PUB` | A0 | Publicado y aprobado para uso |
| `_EXE` | CR | Ejecutado o firmado — estado de registro o como construido |
| `_MCH` / `_DAT` | (coincide con el padre) | Versión legible por máquina del documento padre |

Un archivo `_EXE` ha pasado la confirmación del operador en la [[app-console-input|puerta de entrada F12]] y está sellado en el [[worm-ledger-design|libro mayor WORM]].

## Cómo aplica la postura de divulgación continua de la BCSC

PointSav opera dentro de un marco regulatorio canadiense. La Comisión de Valores de Columbia Británica requiere que las declaraciones prospectivas lleven el lenguaje de advertencia apropiado y que las afirmaciones sobre el cumplimiento actual reflejen con precisión el estado actual.

Cada documento público que publica la plataforma aplica la siguiente disciplina: lenguaje de planeado y previsto para controles aún no desplegados; sin afirmaciones de certificación actual sin confirmación del operador; todas las referencias a la Fundación de Datos Soberanos solo en términos planeados y previstos, hasta que el operador conceda autorización para una clasificación diferente.

## Véase también

- [[architecture-decisions|SYS-ADR-07]] — la decisión arquitectónica que prohíbe que los datos estructurados pasen por IA sin verificación humana
- [[architecture-decisions|SYS-ADR-19]] — la decisión arquitectónica que prohíbe la publicación automatizada de IA en libros mayores verificados
- [[worm-ledger-design]] — el sustrato del libro mayor WORM que aplica el mantenimiento de registros de solo adición
- [[doorman-protocol]] — la puerta de IA cuyo límite de auditoría apoya las intenciones de registro ISO/IEC 42001
- [[diode-standard]] — flujo de comandos unidireccional que aplica la restricción de control de dirección única
- [[structural-positioning]] — los ocho compromisos arquitectónicos que apoya la postura de cumplimiento
