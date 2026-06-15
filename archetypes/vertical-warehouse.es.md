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
language_protocol: TRANSLATE-ES
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

## Conjunto de datos de producción

El sistema de producción VWH utiliza clústeres DBSCAN de cadenas de ferretería, suministro para el sector de la construcción y comercio minorista industrial-ligero. La calibración usa ubicaciones de ferreterías existentes como anclas indicadoras: un sistema calibrado debe situar anclas de ferretería a menos de 3 km de al menos el 73% de los clústeres T1 y T2. La versión de junio de 2026 cumplió este umbral.

**6.368 clústeres** en 17 países de visualización según la calibración de junio de 2026:

| Nivel | Recuento | Proporción |
|---|---|---|
| T1 Centro de Comercio Completo | 852 | 13,4% |
| T2 Comercio Consolidado | 1.327 | 20,8% |
| T3 Emergente | 4.189 | 65,8% |

Distribución por país (los ocho principales): EE.UU. · DE · GB · CA · FR · NL · IT · PL.

El T3 representa la mayoría porque los clústeres con una sola categoría de ferretería califican como sitios VWH básicos. Los centros de comercio completo que combinan ferretería, distribución MRO industrial, alquiler de herramientas y repuestos de automóviles son genuinamente escasos — esta distribución con predominio T3 refleja la rareza real de los sitios en el nivel T1.

## Clasificación por niveles

Los niveles VWH utilizan un **modelo de colapso por grupo**: la asignación de nivel se basa en el número de grupos de categorías de suministro para el sector distintos presentes en un clúster, no en el recuento total de miembros. Un clúster con muchas ferreterías pero sin otras categorías comerciales no califica para T1; la diversidad entre categorías de comercio distintas es lo que importa.

**T1 Centro de Comercio Completo:** Al menos dos grupos de suministro para el sector distintos presentes — por ejemplo, ferretería más distribución MRO industrial, o ferretería más alquiler de herramientas. Esto indica un ecosistema genuino de contratistas y logística.

**T2 Comercio Consolidado:** Ancla de ferretería con al menos una categoría secundaria de suministro para el sector (repuestos de automóviles, materiales de construcción o pavimentos).

**T3 Emergente:** Ancla de ferretería presente sin co-ubicación adicional de suministro para el sector. Sitios VWH básicos de una sola categoría.

## El indicador de contaminación minorista

Casi la mitad de los clústeres VWH tienen un hipermercado de alimentación a menos de 1 km. Los hipermercados sí aparecen cerca de zonas industriales y de almacenamiento en la periferia urbana, especialmente en Europa donde los parques industriales y los parques comerciales comparten frecuentemente vías de acceso. En lugar de excluir estos sitios de uso mixto, el conjunto de datos de producción los marca con un indicador de *contaminación minorista*, señalando que el sitio tiene proximidad a un ancla de alimentación.

Un sitio marcado no queda descalificado como ubicación VWH, pero el análisis de selección de sitio debe tener en cuenta el tráfico minorista y la dinámica de zonificación que conlleva la proximidad al ancla de alimentación — estas son zonas de uso mixto, no recintos industriales puros.

## Plan de recopilación de datos

### Adiciones prioritarias — cadenas de Nivel A (señal definitiva de VWH)

| Cadena | Mercado | Notas |
|---|---|---|
| Floor & Decor | EE.UU. | Pavimentos de formato almacén para contratistas |
| Topps Tiles | Reino Unido | Venta de azulejos para contratistas en polígonos industriales |
| United Rentals | NA | Se ubica deliberadamente junto a anclas de ferretería |
| Sunbelt Rentals | NA | Misma estrategia; nunca en parques comerciales de alimentación |
| Loxam | UE | Alquiler de herramientas; polígonos industriales |
| Kiloutou | FR | Alquiler de herramientas |
| Würth | UE | Distribuidor MRO; presente en todos los polígonos industriales de la UE |
| Fastenal | NA | MRO industrial; siempre en zona industrial |
| Grainger | NA | MRO industrial |
| Hilti | UE | Herramientas de precisión; Centros Hilti en polígonos industriales |
| 84 Lumber | EE.UU. | Los almacenes de madera son definitivamente periferia industrial |
| Builders FirstSource | EE.UU. | Materiales de construcción B2B |

### Categorías taxonómicas necesarias

`flooring` (pavimentos), `tool_rental` (alquiler de herramientas), `mro_industrial`, `lumber` (madera) — estas enriquecen los arrays de miembros del clúster VWH pero no determinan la lógica de niveles T1/T2/T3.

## Referencias

- [Almacén](https://en.wikipedia.org/wiki/Warehouse) — Wikipedia, acceso 2026-06-14
- [Parque comercial](https://en.wikipedia.org/wiki/Retail_park) — Wikipedia, acceso 2026-06-14

*Contenido de Wikipedia reproducido bajo [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*
