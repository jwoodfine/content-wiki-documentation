---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: bim-market-context
short_description: "La Modelización de Información de Construcción es ahora un mandato gubernamental en las jurisdicciones más relevantes para bienes raíces institucionales, con ISO 19650 e IFC como estándares globales, y el Golden Thread del Reino Unido creando demanda de mercado legal para registros digitales de edificios portátiles y continuamente mantenidos."
title: "Contexto del mercado BIM y marco regulatorio"
category: reference
language: es
paired_with: bim-market-context.md
bcsc_class: public-disclosure-safe
status: active
last_edited: 2026-06-20
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, iso-19650]
---

La arquitectura de la transformación digital del sector de la construcción está definida. Los estándares son ISO. Los formatos son abiertos. Los mandatos regulatorios están publicados. Lo que permanece sin resolver es quién construirá la capa de infraestructura que conecta geometría, registros, sensores y títulos legales en un único archivo portátil que sobreviva a todos los proveedores de software que lo utilicen. El [[totebox-archive|Archivo Totebox]] es esa capa de infraestructura: un [[worm-ledger-architecture|registro de solo adición]] de cada dato del edificio, transferible en la venta e independientemente verificable.

## El mandato global de BIM

La Modelización de Información de Construcción ya no es una preferencia del sector. Es un mandato gubernamental en las jurisdicciones que más importan para los bienes raíces institucionales.

### Reino Unido — El pionero

El Reino Unido estableció como obligatorio el BIM de Nivel 2 para todos los proyectos públicos adquiridos de forma centralizada en abril de 2016, convirtiéndose en el primer país en exigir BIM 3D colaborativo en todo un programa de construcción pública. El mandato exige la entrega de datos compatibles con IFC y la adopción de los estándares de gestión de la información ISO 19650. A partir de 2026, el país avanza hacia un estándar de ciclo de vida más integrado, con la Ley de Seguridad en Edificios de 2022 añadiendo una obligación legal de registros digitales continuos para los edificios de mayor riesgo.

### Unión Europea — El marco regulatorio

La Directiva de la UE 2014/24/EU sobre contratación pública anima explícitamente a los estados miembros a exigir BIM para la construcción financiada con fondos públicos. El Grupo de Trabajo BIM de la UE, con el apoyo de DG GROW de la Comisión Europea, publicó su Documento de Posición sobre BIM para Contratación Pública en noviembre de 2025, describiendo el BIM bajo ISO 19650 como "no simplemente una tecnología, sino un enfoque estructurado para gestionar la información a lo largo del ciclo de vida de un activo público". El Comité Europeo de Normalización (CEN/TC 442) ha adoptado todos los principales estándares ISO de BIM como Normas Europeas, incluidas EN ISO 16739-1 (IFC), EN ISO 19650 y EN ISO 29481.

**Mandatos nacionales en Europa:**

| País | Mandato | Formato requerido | Año |
|---|---|---|---|
| Dinamarca | Todos los proyectos públicos superiores a 677.000 € | IFC | 2007 (primero en el mundo) |
| Noruega | Todos los proyectos públicos (Statsbygg) | IFC | 2010 |
| Finlandia | Senate Properties — todos los proyectos principales | IFC | 2012 |
| Países Bajos | Infraestructura de Rijkswaterstaat | IFC | 2012 |
| Reino Unido | Todos los proyectos públicos adquiridos centralmente | IFC / ISO 19650 | 2016 |
| Alemania | Plan federal por etapas — mandato gradual | IFC | Desde 2017 |
| España | Comisión BIM — grandes infraestructuras | IFC | 2018+ |
| Italia | D.Lgs. 36/2023 — obras públicas por fases | IFC | 2023+ |
| Francia | Fomentado en obras públicas | IFC | Activo |
| Polonia | Proyectos de más de 10 M€ para 2025, todos para 2030 | IFC | Por fases |
| Singapur | Todas las nuevas solicitudes de edificación (CORENET X) | IFC | 2025 |

La convergencia es clara: ISO 19650 como estándar de proceso e IFC como formato de datos son el estándar gubernamental global por defecto para información de edificación. Ningún país que haya mandatado BIM ha mandatado ningún formato propietario. Los mandatos se redactan en torno a estándares abiertos.

### ISO 19650 — El estándar de proceso, en revisión activa

ISO 19650 define cómo se gestiona la información a lo largo del ciclo de vida de un activo construido utilizando BIM. La Parte 6, centrada en datos de salud y seguridad, se publicó en 2025. El estándar está actualmente en revisión — los cambios propuestos incluyen una terminología más clara, la eliminación de contenido repetitivo, un flujo de trabajo más lógico y una mayor atención a la información del ciclo de vida completo que abarca operaciones, mantenimiento y desmantelamiento.

**Lo que esto significa para PointSav:** Todo proyecto financiado por gobiernos en Europa y en la mayoría de los mercados principales fuera de Estados Unidos exige legalmente entregables en formato IFC y gestión de la información alineada con ISO 19650. El archivo de archivos planos de PointSav, canonizado en IFC-SPF, es la infraestructura que hace que esos mandatos sean sostenibles más allá de la fase de construcción. El [[sel4-microkernel-substrate|microkernel seL4]] aborda el requisito de soberanía de datos que las plataformas BIM en la nube no pueden satisfacer estructuralmente.

---

## El Golden Thread del Reino Unido

La Ley de Seguridad en Edificios del Reino Unido de 2022 es la pieza legislativa de construcción más relevante comercialmente en una generación. Surgió directamente del incendio de la Torre Grenfell en 2017, en el que murieron 72 personas, y de la posterior Revisión Hackitt, que identificó fallos sistémicos en la forma en que se creaba, gestionaba y entregaba la información sobre edificios.

### Qué exige el Golden Thread

La Sección 88 de la Ley de Seguridad en Edificios de 2022 establece el Hilo Dorado de información como requisito legal para los Edificios de Mayor Riesgo (HRB, por sus siglas en inglés) — edificios de al menos 7 plantas o 18 metros con al menos 2 unidades residenciales. El requisito: un registro electrónico completo y continuamente mantenido de toda la información crítica para la seguridad de un edificio, desde el primer diseño hasta la ocupación, incluidas todas las decisiones de diseño y los materiales, todos los cambios realizados durante la construcción y la ocupación, los informes de inspección y los registros de mantenimiento, la estrategia de seguridad contra incendios y los datos de seguridad estructural, y los registros de propietarios anteriores.

La Building Safety Alliance publicó orientaciones detalladas sobre el Golden Thread en mayo de 2025, coordinadas con expertos en estándares de datos ISO y europeos.

### La conexión con el gemelo digital

El Golden Thread ha creado, por estatuto, un mercado legal para exactamente lo que un Archivo de Propiedad de PointSav ofrece: un registro digital portátil, con control de versiones y continuamente mantenido de un edificio, transferible en la entrega, independientemente verificable, sin dependencia continua de la existencia de ningún proveedor. Este es un argumento de adquisición, no un argumento tecnológico.

---

## La pila de estándares BIM abiertos

El ecosistema de estándares BIM abiertos alcanzó la madurez de producción entre 2023 y 2025. Cada componente descrito a continuación es un estándar ISO, un estándar oficial de buildingSMART o un estándar comunitario OGC.

### buildingSMART International

buildingSMART International (bSI) es el organismo de normalización sin ánimo de lucro responsable de IFC, BCF, IDS y el Diccionario de Datos de buildingSMART. Sus estándares se desarrollan abiertamente y se publican bajo términos que permiten la implementación libre.

### IFC — El estándar canónico

IFC (Industry Foundation Classes) se publica como **ISO 16739-1:2024**. Define un esquema completo para representar edificios, puentes, carreteras, ferrocarriles, puertos y vías navegables. Abarca geometría, estructura espacial, propiedades de elementos, cantidades, clasificaciones, relaciones e información de procesos.

IFC tiene tres formatos de serialización estables:
- **IFC-SPF** (`.ifc`) — Archivo Físico STEP ISO 10303-21, ASCII de texto claro. El formato de archivo canónico.
- **ifcXML** (`.ifcXML`) — Serialización XML del mismo esquema.
- **IFCZIP** (`.ifczip`) — Compresión ZIP de IFC-SPF. Útil para transmisión.

### IFC 5 — La próxima generación

IFC 5 está en desarrollo activo en buildingSMART. Su cambio definitorio es la introducción de **IFCX**, una nueva serialización basada en JSON inspirada en OpenUSD de Pixar que utiliza la descomposición entidad-componente-sistema (ECS). Principios clave: composición multifichero, capas y sobreescritura al estilo USD, y codificación nativa JSON con UTF-8 correcto. El modelo de objetos de PointSav está diseñado para la compatibilidad con IFC 5/IFCX como migración prospectiva.

### BCF — Formato de Colaboración BIM

BCF 3.0 es el estándar de buildingSMART para comunicar incidencias, informes de conflictos y consultas de diseño entre herramientas BIM. Sin comprimir, es una estructura de directorios de texto plano compatible con Git.

### IDS — Especificación de Entrega de Información

IDS 1.0 se convirtió en el estándar oficial de buildingSMART el 1 de junio de 2024. Un archivo `.ids` es un documento XML que valida de forma automatizada si un modelo IFC contiene las propiedades requeridas para un caso de uso específico. El módulo `ifctester` de IfcOpenShell valida cualquier archivo IFC contra cualquier archivo IDS.

### bSDD — Diccionario de Datos de buildingSMART

bSDD publica clasificaciones de elementos de construcción y definiciones de propiedades como URLs desreferenciables que devuelven JSON-LD. Un URI de bSDD es un identificador globalmente único y estable para un tipo de elemento de construcción que cualquier herramienta puede consultar y obtener una definición legible por máquinas.

### CityJSON y CityJSONSeq

CityJSON 2.0 es un Estándar Comunitario OGC — una codificación JSON del estándar de modelo urbano CityGML. **CityJSONSeq** es su variante de transmisión: un objeto JSON por línea. TU Delft utiliza CityJSONSeq para servir todo el parque inmobiliario de los Países Bajos (~10 millones de registros) a través del conjunto de datos 3DBAG. Para vistas de cartera de múltiples edificios, CityJSONSeq es el formato natural para la capa de agregación de `app-orchestration-bim`.

---

## Formatos de archivo

### Formatos de importación — no formatos de archivo

**RVT** es un formato binario cerrado. Para proyectos conformes con ISO 19650, el arquitecto exporta IFC en cada hito del proyecto. PointSav ingiere IFC. El archivo RVT permanece en el entorno de autoría del arquitecto. Esta es la arquitectura de información correcta bajo cualquier mandato gubernamental de BIM — no es un compromiso.

La Open Design Alliance (ODA) proporciona una implementación legalmente limpia para leer formatos DWG/DXF. **DXF** es completamente abierto (especificación publicada); **DWG** es legible a través de la membresía en ODA.

### La pila de archivo abierto

Cada formato a continuación es un estándar ISO, un estándar W3C o una especificación abierta publicada. Todos serán legibles en 2076 con herramientas que todavía no existen.

| Formato | Estándar | Función |
|---|---|---|
| IFC-SPF (`.ifc`) | ISO 16739-1:2024 | Formato de archivo canónico. Modelo completo del edificio. |
| SVG (`.svg`) | W3C | Plantas 2D. GUIDs de IFC incrustados como IDs de elemento. |
| glTF 2.0 (`.glb`) | ISO/IEC 12113:2022 | Caché del visualizador 3D. Regenerado desde el IFC canónico bajo demanda. |
| BCF 3.0 (`.bcf` descomprimido) | buildingSMART | XML por incidencia + capturas PNG. Compatible con Git. |
| IDS 1.0 (`.ids`) | buildingSMART (junio 2024) | Esquema de validación de conformidad. |
| Archivos auxiliares YAML | Nativo de PointSav | Metadatos operativos por elemento, indexados por GUID de IFC. |
| CityJSONSeq | Comunidad OGC | Cartera y contexto urbano. Un edificio por línea. |

**La prueba de legibilidad a 50 años:** IFC-SPF, SVG, glTF, YAML y BCF XML la superan — estándares ISO con especificaciones publicadas, legibles por cualquier herramienta conforme. Los formatos binarios cerrados no la superan: están bloqueados a la versión y dependen de la continuidad del proveedor.

---

## Conectividad ciberfísica — La brecha del gemelo digital

### Qué requiere un gemelo digital

El Programa Nacional de Gemelo Digital del Reino Unido y la ISO 23247 convergen en una definición que exige tres componentes simultáneamente presentes:

1. **Representación geométrica** — un modelo espacialmente preciso del activo físico
2. **Datos de sensores en tiempo real** — lecturas operativas en vivo del activo físico
3. **Contexto operativo y legal** — los registros que dan sentido a los datos de los sensores

Un modelo BIM 3D sin sensores es un registro geométrico, no un gemelo digital. Una red de sensores sin geometría es un flujo de datos. Un gemelo digital requiere los tres — vinculados con suficiente precisión semántica para que la consulta de una dimensión recupere datos correlacionados de las demás.

### La brecha estructural

Ninguna plataforma comercial actual ofrece acceso simultáneo controlado por el propietario al registro geométrico, datos de sensores, registro de arrendamientos, libro mayor financiero e historial de mantenimiento de un edificio en un único archivo portátil con capacidad sin conexión. Esto no es un descuido. Es consecuencia de la arquitectura de nube multiusuario: combinar la geometría BIM de un inquilino con su libro mayor financiero en un único registro controlado por el propietario es arquitectónicamente incompatible con los modelos de residencia de datos, control de acceso e ingresos de cualquier plataforma en la nube compartida.

---

## La capa de integración IoT-BIM

La capa de web semántica que conecta los datos de sensores con la geometría del edificio ha convergido en tres estándares complementarios.

### Brick Schema

Brick (brickschema.org) es una ontología basada en RDF para metadatos de edificios, centrada en sistemas de HVAC, eléctricos, de fontanería y de sensores. Brick 1.3 (2023) incluye alineación con IFC 4.3. Cada elemento HVAC en el modelo IFC lleva un URI de Brick Schema en su archivo auxiliar YAML; el archivo auxiliar de cada sensor hace referencia al GUID IFC del elemento al que está vinculado.

### SAREF — Ontología de Referencia para Aplicaciones Inteligentes

SAREF es un estándar IoT de ETSI (SAREF4BLDG para la extensión de edificios). Se alinea con IFC a nivel de elemento, permitiendo la reutilización de información entre el BIM de la fase de diseño y los datos IoT de la fase de operaciones.

### Project Haystack

Project Haystack es una taxonomía de etiquetado de código abierto para datos de equipos de edificios, especialmente puntos de sistemas de gestión de edificios (BMS). Donde Brick proporciona una ontología basada en grafos, Haystack proporciona etiquetado plano que muchos proveedores de BMS admiten de forma nativa. Los dos son complementarios.

### El patrón de integración IoT de PointSav

```
Sensor físico (BACnet / KNX / MQTT)
 ↓ broker MQTT local en nodo ToteboxOS
ingestión de service-bim
 ↓ escribe en archivo auxiliar YAML del elemento
elements/{IFC-GUID}/sensors.yaml
```

Las lecturas de los sensores se añaden a un archivo de series temporales JSONL. El archivo crece solo por adición. No se requiere ningún motor de base de datos. Todo el historial de sensores es legible por cualquier herramienta compatible con JSONL.

---

## El argumento de interoperabilidad

El flujo de entrega de proyectos conformes con ISO 19650 que ya utilizan todos los proyectos mandatados por gobiernos es:

```
El arquitecto trabaja en su herramienta de autoría BIM
 ↓ Exportación IFC (en cada hito del proyecto)
Plataforma de coordinación
 ↓ IFC como formato de intercambio
Plataforma de FM / archivo (PointSav PropertyArchive)
 ↓ IFC como registro permanente
```

PointSav se sitúa al final de este flujo de trabajo como el archivo permanente — el "Modelo de Información del Activo" que ISO 19650 Parte 3 exige entregar y mantener. El arquitecto nunca abre PointSav. El contratista nunca abre PointSav. Entregan IFC en la entrega, que es lo que la ley ya exige en cualquier proyecto mandatado.

PointSav produce DXF como salida de coordinación — legible en cualquier herramienta de dibujo. Los planos SVG son legibles en cualquier navegador y editor de gráficos vectoriales. glTF es visualizable en cualquier aplicación 3D principal. El archivo produce derivados para cualquier flujo de trabajo sin comprometer el IFC canónico.

---

## La tesis del salto adelante

Cinco capacidades están ausentes en todas las plataformas BIM comerciales actualmente disponibles — no por descuido, sino por incompatibilidad estructural con el modelo de nube por suscripción:

1. **BIM anclado al activo.** Un PointSav PropertyArchive, exportado como imagen de disco arrancable, se transfiere con la escritura de propiedad. El comprador recibe la memoria institucional completa del edificio. Ninguna plataforma actual puede ofrecer esto de forma creíble porque socavaría la renovación de suscripciones.

2. **BIM con capacidad sin conexión.** Los sótanos, las azoteas, los sitios de construcción rurales, las instalaciones de defensa aisladas por aire, los campus de salud con estrictos requisitos de residencia de datos y las regiones con menor conectividad son estructuralmente inaccesibles para las plataformas BIM que priorizan la nube.

3. **BIM superviviente a la obsolescencia del proveedor.** Un edificio dura 50-100 años. Una suscripción de software dura hasta que el proveedor cambia su modelo de precios. El archivo PointSav, escrito en IFC-SPF + YAML + SVG + glTF, será legible en 2076 con herramientas que todavía no existen.

4. **Integración IoT sin intermediario en la nube.** Un nodo [[totebox-os|ToteboxOS]] de PointSav ingiere datos de sensores BACnet/KNX/MQTT directamente en el archivo a través de un broker local — los datos nunca abandonan las instalaciones del propietario a menos que el propietario elija enviarlos.

5. **BIM + arrendamientos + libro mayor financiero en un único archivo portátil.** Un PropertyArchive que contenga la geometría de un edificio, el registro de arrendamientos, el libro mayor financiero y el historial de mantenimiento en un único archivo controlado por el propietario es arquitectónicamente imposible para cualquier plataforma compartida multiusuario. Para un propietario de inmuebles, estos no son cuatro conjuntos de datos — son un único registro sobre un único activo. El principio de [[customer-owned-graph-ip|gráfico propiedad del cliente]] implica que el registro pertenece al propietario del inmueble, no a ningún proveedor de plataforma.

### El horizonte 2030

La convergencia de tres fuerzas independientes para 2030 crea el mercado hacia el que PointSav está arquitecturando:

- **El mercado de tokenización.** El mercado de bienes raíces tokenizados se proyecta hacia los 30 billones de dólares para 2034. Cada propiedad tokenizada carece actualmente de un registro operativo. Un PointSav PropertyArchive, vinculado a un título de propiedad y entregado con el edificio en la venta, es el registro operativo que le falta al mercado de tokenización.
- **El mandato del Golden Thread.** El requisito del Golden Thread de la Ley de Seguridad en Edificios del Reino Unido (en vigor desde abril de 2024) crea una obligación legal para exactamente el registro de edificio continuo, transferible y mantenido digitalmente que un PropertyArchive ofrece.
- **La posición de seguridad de seL4.** Las propiedades de seguridad formalmente verificadas del microkernel seL4 abordan la preocupación que impide que los clientes clasificados, de salud y defensa adopten BIM en la nube: la soberanía de los datos.

---

## Bibliografía

1. buildingSMART International. *IFC 4.3 Formally Approved and Published as an ISO Standard.* Abril 2024.
2. ISO. *ISO 16739-1:2024 — Industry Foundation Classes (IFC).* 2024.
3. buildingSMART International. *IFC5 Development Repository.* github.com/buildingSMART/IFC5-development
4. buildingSMART International. *IDS 1.0 — Information Delivery Specification.* 1 de junio de 2024.
5. EU BIM Task Group. *Position Paper on BIM for Public Procurement.* Noviembre 2025.
6. Comisión Europea. *EU Directive 2014/24/EU on Public Procurement.* 2014.
7. ISO. *ISO 19650 — Information Management Using Building Information Modelling.* Partes 1–6. 2018–2025.
8. Gobierno del Reino Unido / HSE. *Keeping Information About a Higher-Risk Building: The Golden Thread.* GOV.UK. Septiembre 2024.
9. Parlamento del Reino Unido. *Building Safety Act 2022.* Sección 88 — Golden Thread.
10. Building Safety Alliance. *Golden Thread Guidance Documents.* Mayo 2025.
11. IfcOpenShell. *The Open Source IFC Toolkit and Geometry Engine.* ifcopenshell.org
12. ThatOpen Company. *web-ifc Documentation.*
13. Khronos Group. *glTF — Runtime 3D Asset Delivery.*
14. CDBB. *The Gemini Principles.* Centre for Digital Built Britain. 2018.
15. TU Delft. *3DBAG — CityJSONSeq Dataset of Dutch Building Stock.* 3dbag.nl
16. brickschema.org. *Brick Schema 1.3.*
17. ETSI. *SAREF — Smart Applications REFerence Ontology.* ETSI TS 103 264.
18. Chung, J. & Shelden, D. *A Framework of ifcJSON-Based Digital Twin Platform.* ICCCBE 2024. Springer, 2025.
19. Tandfonline. *Development and Demonstration of a Digital Twin Platform Leveraging Ontologies.* DOI: 10.1080/19401493.2025.2504005

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
