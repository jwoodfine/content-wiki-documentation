---
schema: foundry-doc-v1
title: "Almacén Vertical (VWH)"
slug: vertical-warehouse
category: archetypes
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-02
editor: pointsav-engineering
paired_with: vertical-warehouse.md
short_description: "Un Almacén Vertical es un edificio de 3–6 plantas usado para manufactura ligera, logística justo-a-tiempo y entrega de última milla en ubicaciones urbanas o periurbanas — uno de los tres arquetipos de Inteligencia de Localización."
cites: []
---

Un **Almacén Vertical** es un edificio de 3–6 plantas utilizado para manufactura ligera, logística justo-a-tiempo y entrega de última milla en ubicaciones urbanas o periurbanas. El tipo de edificio apila funciones que tradicionalmente se distribuirían horizontalmente en un área industrial de planta baja: fabricación, almacenamiento de componentes, ensamblaje y despacho de salida.

Código de tres letras: **VWH**. Uno de los tres arquetipos de Inteligencia de Localización junto a los [[professional-centres|Centros Profesionales (PRO)]] y las [[parking-structures|Estructuras de Aparcamiento (PKS)]].

## Qué hace un Almacén Vertical

Mezcla típica de inquilinos:

- **Manufactura ligera** — ensamblaje electrónico, integración robótica, formulación de pinturas y recubrimientos, fabricación de precisión
- **Entrega justo-a-tiempo** — centro de distribución regional para cadenas de suministro de comercio electrónico y manufactura; las mercancías llegan por camión, se procesan y salen el mismo día o al día siguiente
- **Logística de última milla** — clasificación y despacho final para zonas de entrega urbana; se requiere proximidad a la población densa

El factor de forma vertical está impulsado por el costo del suelo urbano. Donde un almacén horizontal requeriría 1,6–3,2 hectáreas en la periferia urbana, un Almacén Vertical logra el área de piso equivalente en 0,4–0,8 hectáreas al ganar altura. El acceso de camiones en planta baja y los niveladores de muelle se conservan; los pisos superiores son servidos por ascensores de carga para cargas de montacargas.

## Dónde se ubican los Almacenes Verticales

**Firma espacial:** 5–25 km del centro metropolitano más cercano, en la zona de transición industrial-suburbana. Ubicados a lo largo de arterias de varios carriles o intercambios de autopistas con acceso directo para camiones. Zonificación industrial o industrial ligera.

**Qué hay cerca:**
- Anclas de ferretería (Home Depot, Leroy Merlin, OBI, clase Bauhaus) — suministro para oficios de la construcción
- Tiendas de piezas de automóviles (AutoZone, O'Reilly, Halfords) — mantenimiento de vehículos de flota
- Sucursales de alquiler de herramientas (United Rentals, Sunbelt, Loxam, Kiloutou) — equipos para instalaciones
- Distribuidores industriales MRO (Würth, Fastenal, Grainger, Hilti) — fijaciones, herramientas, consumibles
- Suministro de pisos y azulejos (Floor & Decor, Topps Tiles) — materiales de acabado, suministro para contratistas
- Madera y materiales de construcción (84 Lumber, Builders FirstSource) — suministro estructural

**Qué NO hay cerca:** hipermercados de alimentación, anclas de estilo de vida (IKEA), tiendas club (Costco/Sam's Club en su función de consumo). Una zona VWH se define en parte por la *ausencia* de comercio minorista anclado en alimentación.

## Señales de selección de sitio

**Esenciales — requeridas para un sitio VWH viable:**

| Señal | Umbral | Justificación |
|---|---|---|
| Intercambio de autopista | ≤2 km | Los camiones no pueden usar vías residenciales locales para entregas masivas diarias |
| Vecinos de uso de suelo industrial | Adyacente o dentro de 500 m | Compatibilidad de zonificación; ecosistema logístico existente |
| Área de captación laboral | 300.000+ habitantes / 30 min en coche | Los puestos de manufactura y logística requieren mano de obra accesible |
| Acceso ferroviario de carga | ≤2 km (donde disponible) | Entrega de componentes justo-a-tiempo; materia prima a granel |

**Significativas — valor añadido:**

| Señal | Umbral | Justificación |
|---|---|---|
| Aeropuerto de carga aérea | ≤20 km | Componentes electrónicos, reposición rápida |
| Centro logístico (FedEx/UPS/DHL/Amazon) | ≤5 km | Infraestructura compartida de última milla |
| Corredor de transporte público | ≤500 m | Los trabajadores sin vehículo necesitan acceso en autobús/tren |
| Subestación eléctrica | ≤2 km | Manufactura de robótica y electrónica: carga eléctrica pesada |

## Datos de prueba actuales — resultados al 2026-06-01

La detección de VWH está prevista. La prueba actual usa un indicador sustituto: clústeres donde hay cadenas de ferretería pero ningún hipermercado de alimentación, ubicados a 5–80 km de un centro metropolitano.

**360 candidatos indicadores** identificados globalmente en 17 países:

| País | Candidatos | Ejemplos representativos |
|---|---|---|
| EE.UU. | 99 | Colorado Springs (Lowe's, sin alimentación, 7,5 km del centro) |
| DE | 77 | Suburbios de Múnich (clústeres Hagebaumarkt + MediaMarkt) |
| MX | 56 | Periferia de Monterrey (Home Depot + Sam's Club, sin alimentación) |
| FR | 44 | Periferia de Rennes (Leroy Merlin + Decathlon, sin alimentación) |
| IT | 28 | Periferia de Turín (Leroy Merlin + Decathlon) |
| NL | 28 | Eindhoven (Praxis + Gamma + parque comercial IKEA, sin alimentación) |
| CA | 13 | Hamilton ON (Home Depot, sin alimentación, 6,6 km de Hamilton) |
