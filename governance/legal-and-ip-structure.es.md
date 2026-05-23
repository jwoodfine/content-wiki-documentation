---
schema: foundry-doc-v1
title: "Estructura legal y de propiedad intelectual"
slug: legal-and-ip-structure
short_description: "La topología de tres corporaciones que rige la transferencia de propiedad intelectual de contribuidores a proveedor a cliente, con squash-and-merge como el evento de transferencia de propiedad intelectual atómico y separación estricta que impide exposición de código no auditado o registros operacionales."
category: governance
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: legal-and-ip-structure.md
cites:
 - ni-51-102
 - osc-sn-51-721
---

La estructura legal de PointSav describe la topología de tres corporaciones que rige la transferencia de propiedad intelectual desde los contribuyentes hasta el proveedor y, posteriormente, hasta el cliente. Una operación git de squash-and-merge sirve como el evento atómico de transferencia de propiedad intelectual; el proveedor es el único puente entre los contribuyentes y el cliente. El diseño es intencional: los commits experimentales de los contribuyentes nunca llegan al cliente, y los registros operativos del cliente nunca llegan al proveedor. Este artículo cubre la topología de tres corporaciones, el mecanismo de transferencia de propiedad intelectual, el protocolo de contribuyentes, la estructura de licencias prevista y las corrientes de patentes planificadas.

## Las tres corporaciones

PointSav existe dentro de una topología deliberada de tres corporaciones:

| Entidad | Tipo | Función |
|---|---|---|
| Woodfine Capital Projects Inc. | Matriz | Propietaria al 100% de ambas subsidiarias; empresa operadora de activos inmobiliarios |
| PointSav Digital Systems | Subsidiaria (proveedor) | Titular de la propiedad intelectual; diseña y construye la tecnología |
| Woodfine Management Corp. | Subsidiaria (cliente) | Opera activos inmobiliarios; primer cliente de referencia de PointSav |

El flujo interempresarial es unidireccional: el proveedor construye → el cliente adopta → el cliente despliega. PointSav nunca recibe los registros operativos del cliente; el cliente nunca edita el código fuente del proveedor.

## La transferencia de propiedad intelectual mediante squash-and-merge

El mecanismo legal más distintivo es cómo la propiedad intelectual se transfiere desde un contribuyente a la empresa proveedora y luego al cliente. La transferencia se trata como un evento legal atómico implementado mediante una operación git específica: squash-and-merge.

| Fase | Actor | Acción | Significado legal |
|---|---|---|---|
| Oferta | Contribuyente (`jwoodfine` o `pwoodfine`) | Enviar y abrir una solicitud de extracción | Presentación del trabajo; aún no aprobado ni pagado |
| Adquisición | Proveedor (PointSav) | Squash-and-merge | Se elimina el historial de commits del contribuyente; se acuña un único commit corporativo; la propiedad se transfiere a PointSav |
| Distribución | Proveedor (PointSav) | Etiquetar una versión | El código auditado se convierte en una Versión de Producto empaquetada |
| Adquisición por el cliente | Cliente (Woodfine Management Corp.) | Sincronización upstream | El cliente extrae solo las etiquetas de versión firmadas del proveedor; nunca toca al contribuyente |
| Ejecución | Host de producción | Despliegue | La copia con licencia del cliente se ejecuta en producción |
| Reinicio | Contribuyente | Rebase basado en trunk | El entorno local del contribuyente se limpia para coincidir con el estándar verificado del proveedor, listo para el siguiente ciclo |

El squash-and-merge realiza el trabajo legal porque reescribe el historial. Los commits experimentales, los intentos de prototipo y los enfoques abandonados del contribuyente no sobreviven en el libro de registros corporativo. Lo que sobrevive es un único commit limpio propiedad de PointSav y firmado por el administrador del sistema.

## La barrera de doble ciego

Una separación estricta rige los tres roles:

| Interacción prohibida | Razón |
|---|---|
| Contribuyente enviando directamente a repositorios de Woodfine | Elimina la posibilidad de que código de contratista no auditado llegue al cliente |
| Cliente leyendo repositorios bifurcados del contribuyente | Elimina la exposición a trabajo en curso o rechazado |
| Proveedor permitiendo cualquiera de las anteriores | Disolvería al proveedor como puerta de verificación |

PointSav (la organización proveedora en GitHub) es la única entidad que ve tanto a los contribuyentes como al cliente. El puente pasa por el proveedor y solo por el proveedor.

## Protocolo de asignación para contribuyentes

Para los contribuyentes pagados, el contrato vinculante para una asignación específica es una nota manuscrita, no un ticket digital. El protocolo aplica un registro físico y deliberado de quién acordó qué y cuándo — un registro de autoridad de asignación que satisface los requisitos de documentación de la gobernanza fiduciaria y de gestión de riesgos de personal.

Una nota manuscrita es más difícil de falsificar, más difícil de perder y más clara en su intención que una entrada de seguimiento digital o un hilo de mensajería.

## Roles de contribuyentes y designación fiduciaria

La práctica regulatoria canadiense distingue entre roles con autoridad fiduciaria — toma de decisiones estratégicas y financieras — y roles con autoridad operativa — ejecución diaria. Los permisos de GitHub de PointSav reflejan esta división:

- Las organizaciones `pointsav` y `woodfine` en GitHub son propiedad tanto de los responsables estratégicos como de los operativos.
- Las contribuciones rutinarias fluyen a través de las identidades contribuyentes del nivel de preparación (`jwoodfine` y `pwoodfine`), que se alternan por commit.
- La identidad de administrador del sistema (`ps-administrator`) posee el material clave administrativo entre organizaciones y no participa en el trabajo rutinario del nivel de preparación.

Las decisiones estratégicas y fiduciarias se escalan fuera del nivel de contribuyentes rutinario; el administrador del sistema es la única identidad con acceso de escritura entre organizaciones a los repositorios canónicos.

## Estrategia de licencias (prevista)

La estrategia de licencias prevista sigue un modelo de núcleo abierto. Todos los objetivos de licencias son previstos y están sujetos a la postura de divulgación continua de la BCSC [ni-51-102] [osc-sn-51-721]:

| Componente | Licencia planificada |
|---|---|
| `os-totebox`, `os-console`, `os-workplace` (núcleo abierto) | Apache 2.0 + Addendum Soberano (previsto) |
| `os-orchestration` (agregador comercial) | Propietario (previsto) |
| `service-pointsav-link` (el adaptador [[diode-standard|Diodo]]) | Propietario, vendido como complemento empresarial (previsto) |

El Addendum Soberano es la extensión de licencia prevista para garantizar que la instancia en ejecución — no solo el código fuente — permanezca como propiedad del usuario y sea libremente transferible entre sustratos de hardware. El patrón sigue el modelo de núcleo abierto: el núcleo abierto atrae la adopción; los servicios propietarios producen ingresos.

## Estrategia de patentes (prevista)

Se planifican dos corrientes distintas de patentes. Todas las afirmaciones sobre patentes son declaraciones prospectivas sujetas a la postura de divulgación continua de la BCSC [ni-51-102] [osc-sn-51-721]:

| Corriente de patentes | Propietario | Objeto |
|---|---|---|
| Técnica | PointSav Digital Systems (previsto) | El puente del micronúcleo seL4, el Gestor Basado en Capacidades, el protocolo [[diode-standard|Diodo]] |
| Operativa | Woodfine (previsto) | La Solución de Tenencia Directa y la tokenización sistemática de bienes inmuebles como activo real |

Las corrientes no se superponen: PointSav Digital Systems tiene previsto patentar el sustrato; Woodfine tiene previsto patentar el mecanismo de negocio del cliente.

## La Fundación de Datos Soberanos (prevista)

Un socio de gobernanza previsto, la Fundación de Datos Soberanos, está destinado a supervisar la integridad de los componentes de código abierto del sustrato PointSav. La Fundación de Datos Soberanos se menciona únicamente en términos previstos e intencionales; no se afirma ningún rol de supervisión activo, posición accionaria ni autoridad de gobernanza en este momento. Todas las referencias a la Fundación de Datos Soberanos en comunicaciones públicas llevan lenguaje exclusivamente previsto e intencional, conforme a la postura de divulgación continua de la BCSC [ni-51-102] [osc-sn-51-721].

## Véase también

- [[five-stage-supply-chain]] — la cadena de suministro git completa desde el contribuyente hasta el cliente
- [[diode-standard]] — el protocolo de flujo de comandos unidireccional
- [[compliance-and-continuous-disclosure]] — la postura de divulgación continua de la BCSC que rige todas las declaraciones prospectivas de este artículo
- [[structural-positioning]] — los compromisos arquitectónicos que sustentan la separación proveedor/cliente
