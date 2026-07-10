---
schema: foundry-doc-v1
title: "Inteligencia de Ubicación: Recopilación de Datos"
slug: collect-location-intelligence-data.es
lang: es
paired_with: collect-location-intelligence-data.md
short_description: "Ingesta de datos de cadenas e infraestructura VWH y PKS al pipeline de inteligencia de ubicación desde OpenStreetMap — manual de referencia para reingestar o extender a nuevas cadenas y países."
category: how-to
content_type: how-to
type: how-to
status: active
audience: vendor-internal
bcsc_class: no-disclosure-implication
language_protocol: GUIDE-OPERATIONS
last_edited: 2026-07-10
editor: editorial
---

> **Estado (2026-06-11):** Los siete pasos siguientes están completos. Compilación de
> producción VWH: 6,368 clústeres (T1=852/T2=1,327/T3=4,189). Compilación de producción
> PKS: 6,953 clústeres (T1=691/T2=2,658/T3=3,604). Este manual se conserva como referencia
> operativa para reingestar o extender a nuevas cadenas y países.

Configuración inicial del pipeline para ingestar datos de cadenas e infraestructura VWH
(Vertical Warehouse) y PKS (Parking Structures). Los pasos se registran en orden de
ejecución.

Directorio de trabajo para todos los comandos: `app-orchestration-gis/` (dentro del clon
del monorepo de GIS).

## Prerrequisitos

- Acceso a la API de Overpass (las consultas se ejecutan vía `ingest-osm.py`; no requiere
  clave de API)
- Python 3.11+ con las dependencias del pipeline instaladas
- `TOTEBOX_DATA_PATH` apuntando al directorio de datos del despliegue activo

Verificar que el pipeline esté limpio:
```bash
python3 -c "from taxonomy import CATEGORIES, BRAND_FILL; print('taxonomy OK')"
python3 -c "from config import TOTEBOX_DATA_PATH; print('config OK')"
```

## Paso 1 — Ejecutar las ingestas YAML existentes (VWH autopartes + pintura)

Cinco YAML de cadenas fueron creadas el 2026-06-01. Ejecutar la ingesta para descargar los
registros de OSM:

```bash
python3 ingest-osm.py --chain \
  autozone-us \
  oreilley-auto-us \
  napa-us \
  sherwin-williams-us \
  halfords-uk
```

Archivos de salida esperados en `$TOTEBOX_DATA_PATH/service-fs/service-business/`:
- `autozone-us.jsonl` — se esperan 5,000–7,000 registros
- `oreilley-auto-us.jsonl` — se esperan 5,000–7,000 registros
- `napa-us.jsonl` — se esperan 3,000–6,000 registros (red de franquicias; cobertura
  parcial en OSM)
- `sherwin-williams-us.jsonl` — se esperan 3,000–5,000 registros
- `halfords-uk.jsonl` — se esperan 300–450 registros

Verificar:
```bash
for f in autozone-us oreilley-auto-us napa-us sherwin-williams-us halfords-uk; do
  echo "$f: $(wc -l < $TOTEBOX_DATA_PATH/service-fs/service-business/$f.jsonl) records"
done
```

Si una cadena devuelve 0 registros, verificar si la cobertura de etiquetas de Wikidata es
escasa en OSM y agregar el respaldo `name_query:` al YAML.

## Paso 2 — Agregar Würth (mayor vacío MRO en la UE)

Würth es la cadena de mayor valor aún no incluida en la taxonomía. ~1,500 sucursales en la
UE en parques industriales en DE/FR/IT/PL/AT/NL y más. OSM tiene `brand:wikidata=Q183759`
aplicado a muchos registros.

**2a. Crear el YAML:**

```bash
cat > $TOTEBOX_DATA_PATH/service-fs/service-business/wurth-de.yaml << 'EOF'
schema: service-business-chain-v1
chain_id: wurth-de
country: Germany
country_code: DE
region: europe-central
category: Industrial MRO supply
category_slug: mro-industrial
naics_code: "423840"
top_category: Industrial and Personal Service Paper and Related Products
sub_category: Industrial MRO Supply
overture_taxonomy:
  - industrial
  - wholesale
brand_family: MROIndustrial
retailer: Würth
canonical_name: "Adolf Würth GmbH & Co. KG"
parent_company: "Würth Group"
website: wuerth.de
wikidata_id: Q183759
osm_overpass_tag: brand:wikidata=Q183759
store_count_approx: 1500
locations_file: locations/wurth-de.jsonl
locations_status: pending
last_updated: 2026-06-01
notes: "VWH archetype signal. MRO distributor; branches in industrial parks across EU. Multi-country — set country_code per-ISO ingest or use multi_country: true."
EOF
```

**2b. Agregar la categoría `mro_industrial` a taxonomy.py:**

En `taxonomy.py`, dentro del diccionario CATEGORIES, después del bloque `paint`:
```python
"mro_industrial": {
    "label": "Industrial MRO Supply",
    "naics": "423840",
    "description": "Maintenance, repair, and operations distributor — VWH signal. Never gates tier.",
},
"flooring": {
    "label": "Flooring & Tile Supply",
    "naics": "442210",
    "description": "Contractor-facing flooring/tile warehouse — VWH signal. Never gates tier.",
},
"tool_rental": {
    "label": "Tool & Equipment Rental",
    "naics": "532412",
    "description": "Equipment rental branch — VWH signal; deliberate hardware co-location. Never gates tier.",
},
"lumber": {
    "label": "Lumber & Building Materials",
    "naics": "444190",
    "description": "Lumber yard or building materials dealer — VWH signal. Never gates tier.",
},
"car_rental": {
    "label": "Car Rental",
    "naics": "532111",
    "description": "Car rental branch — PKS signal; defines transit node commercial zone. Never gates tier.",
},
```

Ninguna de estas categorías entra en `_RETAIL_CATS` — nunca afectan la lógica de nivel
T1/T2/T3.

**2c. Agregar entradas BRAND_FILL para todas las categorías nuevas:**

En el diccionario BRAND_FILL, después del bloque `paint` existente:
```python
"mro_industrial": {
    "DE": ["wurth-de"],
    "FR": ["wurth-de"],   # Würth is multi-country; chain_id shared
    "IT": ["wurth-de"], "ES": ["wurth-de"], "PL": ["wurth-de"],
    "AT": ["wurth-de"], "NL": ["wurth-de"], "GB": ["wurth-de"],
    "US": ["fastenal-us", "grainger-us"],
    "CA": [], "MX": [],
    "SE": ["wurth-de"], "DK": ["wurth-de"], "NO": ["wurth-de"],
    "FI": ["wurth-de"], "IS": [], "GR": [], "PT": [],
},
"flooring": {
    "US": ["floor-decor-us"],
    "GB": ["topps-tiles-uk"],
    "CA": [], "MX": [], "FR": [], "DE": [], "ES": [], "IT": [],
    "GR": [], "PL": [], "AT": [], "NL": [], "PT": [],
    "SE": [], "DK": [], "NO": [], "FI": [], "IS": [],
},
"tool_rental": {
    "US": ["united-rentals-us", "sunbelt-rentals-us"],
    "CA": ["united-rentals-us"],
    "FR": ["loxam-fr", "kiloutou-fr"],
    "MX": [], "GB": [], "DE": [], "ES": [], "IT": [],
    "GR": [], "PL": [], "AT": [], "NL": [], "PT": [],
    "SE": [], "DK": [], "NO": [], "FI": [], "IS": [],
},
"lumber": {
    "US": ["84-lumber-us", "builders-firstsource-us"],
    "CA": ["kent-building-supplies-ca"],
    "MX": [], "GB": [], "FR": [], "DE": [], "ES": [], "IT": [],
    "GR": [], "PL": [], "AT": [], "NL": [], "PT": [],
    "SE": [], "DK": [], "NO": [], "FI": [], "IS": [],
},
"car_rental": {
    "US": ["enterprise-us", "hertz-us", "avis-us"],
    "CA": ["enterprise-us", "hertz-us"],
    "MX": [],
    "DE": ["sixt-de"], "FR": ["europcar-fr", "sixt-de"],
    "GB": ["europcar-fr", "sixt-de"], "ES": ["europcar-fr"],
    "IT": ["europcar-fr"], "NL": ["europcar-fr"],
    "GR": [], "PL": [], "AT": ["sixt-de"], "PT": [],
    "SE": ["sixt-de"], "DK": ["sixt-de"], "NO": [], "FI": [], "IS": [],
},
```

**2d. Ejecutar la ingesta de Würth:**
```bash
python3 ingest-osm.py --chain wurth-de
```
Se esperan 800–1,500 registros. Las sucursales de Würth suelen estar etiquetadas como
`shop=trade` o `shop=wholesale` en OSM — la etiqueta `brand:wikidata` es la señal confiable.

## Paso 3 — Agregar cadenas VWH minoristas/de alquiler de Nivel A

Crear los YAML siguiendo el esquema abajo, luego ejecutar la ingesta.

**Esquema YAML de referencia:**
```yaml
schema: service-business-chain-v1
chain_id: floor-decor-us          # matches BRAND_FILL key
country: United States
country_code: US
region: north-america
category: Flooring supply          # display only
category_slug: flooring-supply
naics_code: "442210"
top_category: Floor Covering Stores
sub_category: Floor Covering Stores
brand_family: Flooring             # matches category
retailer: Floor & Decor
canonical_name: "Floor & Decor Holdings, Inc."
parent_company: "Floor & Decor Holdings, Inc. (public; NYSE: FND)"
website: flooranddecor.com
wikidata_id: Q22350998
osm_overpass_tag: brand:wikidata=Q22350998
store_count_approx: 240
locations_file: locations/floor-decor-us.jsonl
locations_status: pending
last_updated: 2026-06-01
notes: "VWH Tier A. Warehouse-format contractor flooring; same footprint as Home Depot."
```

**Cadenas a crear (copiar y adaptar el esquema anterior):**

| chain_id | retailer | wikidata_id | country_code | approx_count |
|---|---|---|---|---|
| `floor-decor-us` | Floor & Decor | Q22350998 | US | 240 |
| `topps-tiles-uk` | Topps Tiles | Q7825827 | GB | 300 |
| `united-rentals-us` | United Rentals | Q7889284 | US | 1,400 |
| `sunbelt-rentals-us` | Sunbelt Rentals | Q7645154 | US | 1,100 |
| `loxam-fr` | Loxam | Q6692217 | FR | 1,100 |
| `kiloutou-fr` | Kiloutou | Q3197034 | FR | 600 |
| `fastenal-us` | Fastenal | Q1394323 | US | 3,400 |
| `grainger-us` | Grainger | Q904633 | US | 600 |
| `hilti-ch` | Hilti | Q565285 | CH | 600 |
| `84-lumber-us` | 84 Lumber | Q4641204 | US | 310 |
| `builders-firstsource-us` | Builders FirstSource | Q4934620 | US | 570 |
| `kent-building-supplies-ca` | Kent Building Supplies | Q6383907 | CA | 45 |

Ejecutar todas de una vez después de crear los YAML:
```bash
python3 ingest-osm.py --chain \
  floor-decor-us topps-tiles-uk \
  united-rentals-us sunbelt-rentals-us loxam-fr kiloutou-fr \
  fastenal-us grainger-us hilti-ch \
  84-lumber-us builders-firstsource-us kent-building-supplies-ca
```

Nota: `fastenal-us` y `84-lumber-us` pueden devolver 0 registros vía wikidata — agregar el
respaldo `name_query: "Fastenal"` / `name_query: "84 Lumber"` si es necesario.

## Paso 4 — Escribir `ingest-osm-airports.py` (filtro de aeropuertos comerciales)

Los datos existentes de aeropuertos de Overture (20,841 registros) incluyen pistas
privadas, helipuertos y campos militares. Este script los reemplaza con aeropuertos
comerciales provenientes exclusivamente de OSM.

**Patrón:** copiar `ingest-osm-civic.py`, cambiar la consulta de Overpass a:
```python
QUERY = """
[out:json][timeout:60];
(
  node["aeroway"="aerodrome"]
    ["aerodrome:type"~"^(public|international|regional|domestic)$"]
    ({bbox});
  node["aeroway"="aerodrome"]["iata"~"."]({bbox});
  way["aeroway"="aerodrome"]
    ["aerodrome:type"~"^(public|international|regional|domestic)$"]
    ({bbox});
  way["aeroway"="aerodrome"]["iata"~"."]({bbox});
);
out center;
"""
```

Salida: `$TOTEBOX_DATA_PATH/service-places/cleansed-civic-airports.jsonl`

Esquema: igual que `cleansed-places.jsonl` con `category_id: "airport"`,
`naics_code: "488119"`. Enriquecer con el código IATA a partir de la etiqueta `iata` de
OSM cuando esté presente.

Ejecutar por país usando `COUNTRY_BBOX` de `config.py` (definido para los 17 ISO de
visualización).

Salida esperada: ~5,000–8,000 registros (frente a 20,841 de Overture).

## Paso 5 — Escribir `ingest-osm-railway.py` (estaciones interurbanas)

Salida: `$TOTEBOX_DATA_PATH/service-places/cleansed-civic-railway.jsonl`

**Consulta de Overpass por país:**
```python
QUERY = """
[out:json][timeout:60];
(
  node["railway"="station"]
    ["station"!="subway"]
    ["station"!="light_rail"]
    ["station"!="tram"]
    ["station"!="monorail"]
    ({bbox});
  way["railway"="station"]
    ["station"!="subway"]
    ["station"!="light_rail"]
    ["station"!="tram"]
    ["station"!="monorail"]
    ({bbox});
);
out center;
"""
```

**Post-procesamiento:** filtrar solo a operadores interurbanos usando la etiqueta
`operator=`:

```python
INTERCITY_OPERATORS = {
    "US": ["Amtrak"],
    "CA": ["VIA Rail Canada", "Via Rail"],
    "FR": ["SNCF", "Société Nationale des Chemins de fer Français"],
    "DE": ["Deutsche Bahn", "DB", "DB Regio"],
    "ES": ["Renfe", "Renfe Operadora"],
    "IT": ["Trenitalia", "Italo", "Ferrovie dello Stato"],
    "AT": ["ÖBB", "Österreichische Bundesbahnen"],
    "NL": ["NS", "Nederlandse Spoorwegen"],
    "SE": ["SJ", "Norrtåg"],
    "DK": ["DSB", "Danske Statsbaner"],
    "NO": ["Vy", "NSB"],
    "FI": ["VR", "VR Group"],
    "PT": ["CP", "Comboios de Portugal"],
    "PL": ["PKP Intercity", "RegioJet"],
    "GB": None,  # All Network Rail TOCs qualify — no filtering needed
    "MX": None,  # No passenger rail — skip
    "IS": None,  # No passenger rail — skip
    "GR": ["TrainOSE"],
}
```

Para países donde aplica el filtrado por `operator=`: conservar solo las estaciones donde
la etiqueta `operator` coincida (subcadena, sin distinción de mayúsculas/minúsculas). Para
GB: conservar todas. Para MX e IS: omitir por completo.

Esquema: `category_id: "railway_station"`, `naics_code: "482111"`.

## Paso 6 — Agregar YAML de cadenas de alquiler de autos PKS

Crear cinco YAML siguiendo el mismo esquema del Paso 3:

| chain_id | retailer | wikidata_id | notes |
|---|---|---|---|
| `enterprise-us` | Enterprise Rent-A-Car | Q2283517 | Multi-country NA |
| `hertz-us` | Hertz | Q379425 | Multi-country NA + EU |
| `avis-us` | Avis | Q849144 | Multi-country |
| `sixt-de` | Sixt | Q704156 | EU primary; some NA |
| `europcar-fr` | Europcar | Q466704 | EU primary |

`naics_code: "532111"` (Passenger Car Rental). `brand_family: CarRental`.

Todas estas requieren `multi_country: true` en el YAML, ya que operan en múltiples ISO de
la lista de visualización.

Ejecutar la ingesta:
```bash
python3 ingest-osm.py --chain enterprise-us hertz-us avis-us sixt-de europcar-fr
```

Se esperan conteos altos debido a la ubicuidad en aeropuertos: `enterprise-us`
~4,000–8,000 registros; `sixt-de` ~500–800 registros en la UE.

## Paso 7 — Calibración de producción y despliegue (completado 2026-06-11)

`test-cluster-archetypes.py` fue reemplazado por scripts dedicados de compilación DBSCAN:
- `build-vwh-clusters.py` → `archetype-vwh.geojson` (6,368 elementos)
- `build-pks-clusters.py` → `archetype-pks.geojson` (6,953 elementos)

Para volver a ejecutar después de agregar nuevas cadenas:
```bash
python3 build-vwh-clusters.py   # VWH — outputs work/archetype-vwh.geojson
python3 build-pks-clusters.py   # PKS — outputs work/archetype-pks.geojson
```

Copiar las salidas al directorio de datos del despliegue activo, luego verificar que los
conteos de clústeres coincidan con la línea base de producción (VWH ≥ 6,368 elementos;
PKS ≥ 6,953 elementos).

## Véase también

- Urban Fringe — el modelo de arquetipo VWH y la taxonomía de cadenas
- Commuter — el modelo de arquetipo PKS y la taxonomía de cadenas
- Inteligencia de ubicación: arquetipos (projects.woodfinegroup.com/site-selection) —
  visión general de PRO/VWH/PKS e integración de mapas
- [[connect-osm-data-pipeline]] — ingesta genérica de una sola cadena para nuevas
  categorías minoristas
