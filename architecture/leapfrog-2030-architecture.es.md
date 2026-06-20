---
schema: foundry-doc-v1
title: "La arquitectura Leapfrog 2030"
slug: leapfrog-2030-architecture
short_description: "La arquitectura Leapfrog 2030 describe el posicionamiento estructural de la plataforma en respuesta a tres fuerzas convergentes: modelos de lenguaje pequeño viables en hardware de commodities, el Model Context Protocol como el estándar para composición de servicios nativa de IA y locales como el tipo de implementación SMB de más rápido crecimiento. Los clientes poseen su hardware, datos y pesos de adaptador; PointSav toma tarifas de transacción cuando el valor fluye en lugar de ingresos de suscripción recurrente."
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: leapfrog-2030-architecture.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
 - id: 1
 text: "IDC. 'The SMB 2026 Digital Landscape: How AI is Redefining Growth.' IDC Research, 2026."
 url: "https://www.idc.com/resource-center/blog/the-smb-2026-digital-landscape-how-ai-is-redefining-growth/"
 - id: 2
 text: "Anthropic, Google y colaboradores. 'Model Context Protocol Specification.' modelcontextprotocol.io, 2024."
 url: "https://modelcontextprotocol.io/"
---

Tres fuerzas de mercado que convergen en 2026 — modelos de lenguaje ligeros viables en hardware de consumo, el [[mcp-substrate-protocol|Protocolo de Contexto de Modelos]] como estándar de composición de servicios de inteligencia artificial, y el despliegue en instalaciones propias como el segmento de mayor crecimiento en el mercado de software para pymes — abren un espacio estructural que los grandes proveedores de nube no pueden ocupar sin desmantelar su propio modelo de negocio. La Arquitectura Leapfrog 2030 es el compromiso de [[pointsav-overview|PointSav]] con ese espacio: código de plataforma soberano, servicios componibles e ingresos por transacción en lugar de cuotas de licencia recurrentes. El cliente posee su hardware, sus datos y sus pesos de adaptador; [[pointsav-overview|PointSav]] toma un porcentaje por transacción cuando el valor fluye mediante [[direct-payment-settlement|liquidación de pago directo]]. Este artículo cubre los cinco cambios estructurales que describe la tesis, el sustrato que los realiza y el [[compounding-substrate|ciclo de composición]] que hace durable el compromiso.

## Los cinco cambios estructurales

| Desde (patrón incumbente) | Hacia (patrón PointSav) |
|---|---|
| Interfaz SaaS arrendada | Sistema operativo propio |
| Base de datos centralizada en la nube del proveedor | Archivo [[totebox-os|Totebox]] por entidad |
| Usuario + contraseña (RBAC) | Emparejamiento vinculado al hardware ([[machine-based-auth|MBA]]) |
| Fuente única de verdad | Libro mayor de afirmaciones autocorrector |
| Informes de auditoría anuales de 50 páginas | Prueba continua legible por máquina |

Cada cambio es una decisión arquitectónica única con consecuencias en cadena. Cada uno se aplica a nivel del núcleo o del protocolo, no mediante políticas.

## Lo que la tesis no es

La tesis no es contraria a la nube. PointSav usa extensivamente proveedores de nube comerciales. No es contraria a la inteligencia artificial. PointSav integra modelos de lenguaje en toda la arquitectura. No es un rechazo del código abierto. Los sistemas operativos principales de PointSav están previstos para su publicación bajo Apache 2.0.

La tesis es estructural: el activo que posee el cliente es la instancia en ejecución, no un asiento de suscripción.

## Por qué ahora

Tres corrientes institucionales convergen en 2026. Primero, los modelos de lenguaje ligeros de código abierto han cruzado el umbral de utilidad práctica para tareas especializadas: OLMo 2 1B Instruct produce resultados viables de administración de sistemas a cinco o quince tokens por segundo en hardware de cuatro vCPU de consumo. Segundo, el Protocolo de Contexto de Modelos se ha convertido en el estándar de composición de servicios con inteligencia artificial [^2]. Tercero, el despliegue en instalaciones propias es el segmento de mayor crecimiento dentro del mercado de software para pymes [^1].

Estas tres fuerzas abren un espacio estructural.

Los grandes proveedores de nube están comprometidos con el modelo de cómputo concentrado más pila integrada más ingresos recurrentes. Su nivel para pymes es un nivel empresarial con descuento. Sus funciones de inteligencia artificial requieren flujo continuo de datos hacia su nube. Su modelo de precios presupone que el cliente arrienda capacidad, no que la posee.

La apertura es para un compromiso diferente: sustrato soberano más servicios componibles más ingresos por transacción. El cliente posee su hardware, sus datos, sus pesos de adaptador y sus relaciones comerciales. PointSav Digital Systems es el proveedor del sustrato; el cliente es el operador del sustrato; los ingresos fluyen cuando fluye el valor.

## Qué significa "Leapfrog 2030"

Tres distinciones estructurales frente a la pila de los grandes proveedores de nube:

**Soberanía sobre el servicio.** El [[totebox-os|Totebox]] del cliente — el archivo de datos del cliente, un dispositivo compacto en instalaciones propias — está diseñado para arrancar, ejecutar, consultar, auditar y exportar sin ninguna dependencia continua de PointSav. Si PointSav Digital Systems cesa operaciones, el sustrato del cliente está previsto para continuar funcionando. Esto no es una función de copia de seguridad; es el modo operativo predeterminado de diseño.

**Especialización sobre generalización.** El nivel de inferencia A — siempre activo, instalado en el sitio del cliente — es un especialista en administración de sistemas de mil millones de parámetros, no un generalista de 32 mil millones. Se ejecuta en CPU de consumo. Se entrena con el corpus propio de ingeniería y soporte técnico del cliente. Con el tiempo se vuelve específicamente útil para el entorno de ese cliente. El nivel generalista (nivel B, modelos de 32 mil millones de parámetros en GPU) es opcional y por demanda; el nivel de precisión (nivel C, API externa) es poco frecuente y se divulga por razones de soberanía.

**Composición en lugar de captura.** Los ingresos previstos de PointSav Digital Systems se acumulan junto con los ingresos del cliente, no a expensas de ellos. El sustrato de liquidación directa está diseñado para enrutar las transacciones del mercado de datos directamente del comprador al cliente; PointSav toma un porcentaje por transacción en la liquidación, no una cuota de suscripción por acceso. El cliente está previsto como socio de ingresos, no como pagador de licencias.

## El sustrato de un vistazo

Un despliegue compone tres anillos:

**Anillo 1 — Ingesta en el límite.** Servidores MCP por inquilino que gestionan datos entrantes: service-fs (libro mayor WORM), service-input (archivos, correo y voz), [[service-extraction]] (extracción de entidades), [[service-people]] (CRM), [[service-email]]. Cada uno está delimitado, es auditable y es determinista en su nivel base.

**Anillo 2 — Conocimiento y procesamiento.** Multi-inquilino mediante identificador de módulo: [[service-content]] (el grafo por inquilino y el almacén vectorial), [[service-egress]] (formateado de salida), service-marketplace (puerta de enlace del mercado de datos), service-ad-exchange (puerta de enlace IAB OpenRTB 2.6+), service-settlement (Stripe Connect y riel de criptomonedas).

**Anillo 3 — Inteligencia opcional.** [[service-slm]] Doorman como puerta de enlace MCP; especialista en administración de sistemas de nivel A de 1B (siempre activo); generalista de nivel B de 32B (GPU por demanda); API externa de nivel C (poco frecuente; lista de permitidos).

La Disciplina de Cómputo de Límite Único hace del Doorman el único camino hacia el cómputo de inferencia. Los tokens portadores, las claves de API y las URLs de endpoints viven exclusivamente en la configuración del Doorman. La omisión está estructuralmente impedida — mediante firewall, iptables por propietario UID y solo-portador-en-Doorman — no solo mediante políticas.

## Cómo funciona para la pequeña empresa

Una empresa de cinco empleados instala un [[totebox-os|Totebox]]: un mini-PC de entre 300 y 500 dólares en sus instalaciones. El Totebox ejecuta la pila del sustrato: libro de registros, grafo de conocimiento, ingesta y el especialista en administración de sistemas de nivel A. El operador selecciona un Paquete Semilla Vertical: un conjunto de arquetipos, perfiles del Plan de Cuentas, dominios y temas iniciales. La personalización toma aproximadamente 30 minutos — el paquete es su punto de partida, no una ontología impuesta por el proveedor.

Desde el primer día, el operador puede hacer preguntas operativas al especialista de nivel A. Las respuestas llegan en segundos. Cada interacción es un posible ejemplo de entrenamiento para el adaptador propio del cliente; con el tiempo, el especialista está previsto para calibrarse específicamente para ese entorno.

Cuando el operador necesita trabajo editorial o bilingüe puede activar el nivel B por demanda. La instancia de GPU se activa, procesa la solicitud y vuelve al estado inactivo. El costo se mide por minuto, no por asiento.

Cuando el operador quiere monetizar sus datos propios puede activar el mercado. Un comprador consulta el listado, realiza la transacción a través de la puerta de enlace y paga directamente a la cuenta bancaria o billetera digital del operador. PointSav toma su comisión por transacción en la liquidación.

Cuando el operador vende el negocio, el nuevo propietario importa el paquete Totebox y opera desde el primer día sin reentrenamiento, sin migración de datos y sin cooperación del proveedor.

## Cómo funciona para la institución más grande

Una firma de 300 abogados despliega un clúster Totebox: múltiples unidades más un equipo GPU de nivel B. El aislamiento del grafo por asunto — identificador de módulo por inquilino a la granularidad del asunto — proporciona muros éticos nativos en la arquitectura. El razonamiento de los socios senior capturado como veredictos de interfaz está previsto para entrenar el adaptador de la firma; la siguiente pregunta a nivel asociado se beneficia de una respuesta con mayor orientación de socio.

Un hospital regional despliega un Totebox por línea de servicio. Los grafos de pacientes están aislados; la soberanía de datos es el modo predeterminado — los datos no salen sin consentimiento explícito y el nivel C está estructuralmente deshabilitado para este inquilino. El grafo de conocimiento clínico se construye a partir de notas de consulta; el grafo fundamenta la siguiente pregunta de decisión clínica.

Una empresa inmobiliaria construye una taxonomía semilla ajustada a sus operaciones — Relaciones con Inversores, Proyectos de Capital, Cumplimiento, Construcción. Los temas entran y salen a medida que las iniciativas se cierran y nuevas se lanzan. El grafo es su propiedad, creciendo con el negocio.

En cada caso la forma es la misma: sustrato, grafo, especialista, generalista opcional, auditoría, mercado. El contenido difiere por industria.

## Lo que las plataformas centralizadas no pueden igualar

Los proveedores de plataformas centralizadas están comprometidos con los ingresos recurrentes integrados. Su modelo presupone que el cómputo se concentra en su nube, los datos fluyen a su nube, las cuotas de suscripción se cobran independientemente del uso del cliente y el bloqueo aumenta a medida que se acumulan datos.

El modelo previsto de PointSav presupone que el cómputo se distribuye al hardware del cliente, los datos permanecen en el cliente, las comisiones por transacción se cobran cuando fluye el valor y la transferencia es una operación de un solo comando.

Estas no son diferencias menores de configuración. Son inversiones estructurales. Un proveedor de plataforma centralizada no puede adoptar el modelo comercial de PointSav sin desmantelar su base de ingresos existente. Esta es la ventana estructural en la que PointSav puede ser la única respuesta realista para la institución que quiere operaciones con inteligencia artificial sin bloqueo de proveedor.

## El ciclo de composición

La arquitectura tiene un ciclo de retroalimentación positiva:

1. El Totebox del cliente ejecuta operaciones deterministas sobre sus datos — el caso base de sustrato sin inferencia
2. El especialista de nivel A se entrena con el corpus de ingeniería y los veredictos de interfaz del cliente
3. El especialista se vuelve más útil → el operador lo usa más → más veredictos → especialista mejorado
4. El grafo crece a partir de inferencias aceptadas → más fundamentación para la siguiente inferencia → menos alucinaciones → más inferencias aceptadas
5. Los datos del cliente acumulan valor a medida que crece el grafo; los flujos del mercado pueden comenzar a generar ingresos
6. La liquidación directa enruta los ingresos directamente al cliente; PointSav toma una comisión por transacción
7. Las contribuciones de paquetes al mercado pueden hacer más rápida la incorporación del siguiente cliente del sector

Cada iteración del ciclo es una mejora marginal. La composición corre en tiempo del cliente, no en tiempo del proveedor. El incentivo comercial de PointSav Digital Systems es mantener los ciclos funcionando bien.

## El primer despliegue de referencia

El entorno de desarrollo de PointSav es el primer despliegue de referencia del sustrato. PointSav Digital Systems opera esta instancia como su propio entorno de producción; MCorp es el primer cliente. La plataforma compone la misma forma para ambos.

Esta es la realización estructural del principio de ordenación-cliente-primero: PointSav construye lo que Woodfine instalará, sobre el mismo sustrato que Woodfine usará, en el mismo orden en que Woodfine lo instalará.

## Lo que se publica y cuándo (previsto)

Todas las fases descritas aquí son objetivos previstos, no compromisos. Se aplica lenguaje prospectivo en todo momento conforme a los requisitos de divulgación continua de valores canadienses [ni-51-102] [osc-sn-51-721].

La implementación prevista se desarrolla a lo largo de 2026:

- **Fase 1 (mayo de 2026):** Arquitectura ratificada; intercambio de modelo de nivel A de 1B validado empíricamente
- **Fase 2 (mayo de 2026):** Planos de reconstrucción preparados en el monorepo de ingeniería; tareas de clúster inician
- **Fase 3 (mayo–junio de 2026):** service-content, service-extraction, service-input reconstruidos como servidores MCP
- **Fase 4 (junio de 2026):** Puerta de enlace MCP Doorman; slm-cli TUI Fase 1
- **Fase 5 (julio–agosto de 2026):** service-marketplace, service-ad-exchange, service-settlement; primeras transacciones del mercado
- **Fase 6 (T3 2026):** Primer Totebox de cliente aprovisionado; primer adaptador de soporte técnico entrenado
- **Fase 7 (T4 2026):** Inicio de contribuciones comunitarias de Paquetes Semilla Verticales
- **Fase 8+ (2027):** Mejora continua del modelo; segundo Totebox de cliente; lanzamiento del mercado federado

Supuestos materiales: tareas de clúster de ingeniería ejecutando en el alcance de reconstrucción; ratificación de la especificación de arquitectura por el operador; disposición de Woodfine para participar como cliente de referencia de la Fase 6.

## Lo que es, y lo que no es

Esto es **un compromiso estructural** con la soberanía, la componibilidad y el diseño orientado a pymes.

Esto **no** es un producto de reemplazo de plataformas centralizadas. PointSav no está diseñado para servir a empresas que quieren cómputo gestionado por el proveedor con cuotas de licencia recurrentes. Ese es un mercado bien atendido. La plataforma está diseñada para el mercado que no está bien atendido.

Esto **no** es una arquitectura nicho o experimental. La investigación de la industria de 2026 apunta consistentemente hacia la forma estructural que PointSav está construyendo. La plataforma está deliberadamente posicionada en la intersección donde los proveedores de plataformas centralizadas no pueden seguirla estructuralmente.

La plataforma está en su lugar. La arquitectura está ratificada. El primer despliegue está operativo. El siguiente capítulo es la escala.

## Véase también

- [[compounding-substrate]] — el modelo de propiedad compuesta que sustenta la tesis
- [[service-slm-yoyo-operational]] — el estado operacional del relay Yo-Yo y el Doorman
- [[source-of-truth-inversion]] — el patrón canónico/vista/efímero que sustenta el sustrato
- [[four-tier-slm-substrate]] — el modelo de inferencia de cuatro niveles (Nivel 0/A/B/C)
- [[machine-based-auth]] — el modelo de emparejamiento vinculado al hardware
- [[compliance-and-continuous-disclosure]] — la postura de prueba continua que reemplaza los ciclos de auditoría anuales
