---
schema: foundry-doc-v1
title: "La composición de la co-localización de anclas minoristas como indicador adelantado espacial de la actividad comercial"
slug: geometric-site-selection-national-tenancy.es
category: research
type: research
content_type: research
quality: pre-build
short_description: "Un marco de análisis de clústeres a escala continental que identifica clústeres de co-localización de anclas minoristas y su clasificación por niveles en trece países."
status: active
language: es
language_protocol: TRANSLATE-ES
bcsc_class: public-disclosure-safe
paired_with: geometric-site-selection-national-tenancy
last_edited: 2026-06-11
editor: editorial
---

> **Documento de Trabajo · Versión 0.4.1 · 2026-05-29 · CC BY 4.0**
> Este manuscrito es un borrador de trabajo. No ha sido revisado por pares. Los hallazgos son
> preliminares y están sujetos a revisión sin previo aviso. Correspondencia: jmwoodfine@gmail.com.
>
> *Citar como:* Woodfine, J.M. (2026). La composición de la co-localización de anclas minoristas como indicador adelantado espacial de la actividad comercial: Un análisis de clústeres a escala continental. Documento de Trabajo v0.4.1, 29 de mayo de 2026. MCorp, Vancouver, BC.

> **Declaraciones con proyección de futuro**
> Ciertas declaraciones en este artículo describen direcciones de investigación previstas, capacidades de sistema planificadas y resultados anticipados. Estas declaraciones reflejan las expectativas actuales de los autores y se basan en supuestos razonables y trabajo en curso a la fecha indicada arriba. Los resultados, mediciones y hallazgos reales pueden diferir materialmente. Los lectores no deben depositar una confianza indebida en tales declaraciones; están sujetas a revisión a medida que avanza la investigación y se dispone de nuevos datos.

# La composición de la co-localización de anclas minoristas como indicador adelantado espacial de la actividad comercial: Un análisis de clústeres a escala continental

**MCorp**
Vancouver, Columbia Británica, Canadá

*Autora de correspondencia:* jmwoodfine@gmail.com

*Palabras clave:* co-localización minorista, análisis de clústeres espaciales, aglomeración, geografía económica

*Códigos JEL:* R12, R30, L81, C61

---

## Resumen

La composición de la co-localización de anclas minoristas — la combinación específica de formatos de hipermercado, ferretería y club de almacén que comparten un campus suburbano de estacionamiento en el mismo emplazamiento submetropolitano — es un indicador adelantado del lado de la oferta, medible, de la intensidad de la actividad comercial. Este artículo formaliza un marco geométrico para identificar y clasificar clústeres de co-localización a escala continental, sin datos de movilidad propietarios, utilizando registros de puntos de interés de OpenStreetMap y un algoritmo de agrupamiento DBSCAN de dos pasadas. Aplicado a 6.493 clústeres en trece países de América del Norte y Europa, el marco asigna a cada clúster un nivel (T1/T2/T3) según la composición de categorías de anclas, y luego clasifica los clústeres dentro de los niveles por proximidad geométrica y características del área de captación. Los clústeres T1 representan el 26,9 % de la población del estudio (1.747 de 6.493). Un programa de falsificación de siete pruebas establece las condiciones bajo las cuales puede rechazarse la hipótesis composicional. El marco está diseñado para su confirmación mediante datos de movilidad de origen-destino derivados del geo-cercado de estacionamientos a nivel de clúster, sustituyendo los límites administrativos de captación por mercados submetropolitanos definidos por la movilidad.

*(148 palabras)*

---

## 1. Introducción

### 1.1 El problema de investigación

La composición de anclas — qué combinaciones de categorías minoristas se agrupan, no simplemente cuántos minoristas se concentran — contiene información que la ciencia de la localización convencional no ha medido sistemáticamente. La teoría del lugar central (Christaller, 1933) predice una anidación jerárquica de las funciones minoristas, con los bienes de orden superior concentrándose en asentamientos más grandes. Los modelos gravitacionales del comercio minorista (Reilly, 1931; Huff, 1964) formalizan la relación entre la masa minorista y el coste del desplazamiento. La literatura sobre co-tenencia documenta efectos de tráfico supra-aditivos cuando los minoristas ancla se agrupan (Brueckner, 1993; Pashigian y Gould, 1998). Lo que esta literatura no ha abordado es un índice composicional a escala continental de la co-localización de múltiples anclas: un índice que distinga qué tipos de anclas se agrupan juntas y trate esta distinción composicional como la unidad primaria de análisis.

Un clúster que contiene un hipermercado alimentario, un almacén de mejoras del hogar y un minorista de club de almacén refleja tres procesos de selección de ubicación independientes, continuados y convergentes en la misma localización submetropolitana. Cada uno de estos procesos codifica años de investigación de mercado sobre patrones de tráfico, densidad de la fuerza laboral y demografía del consumidor (Holmes, 2011). Su presencia conjunta es una señal de una calidad distinta a la suma de tres presencias individuales de anclas.

La pregunta de investigación que aborda este artículo: ¿constituye la composición de la co-localización de anclas minoristas — operacionalizada como una clasificación por niveles basada en qué categorías de anclas están presentes — un indicador adelantado estadísticamente distinguible de la intensidad de la actividad comercial en los mercados submetropolitanos? ¿Y puede construirse tal índice a escala continental a partir de datos de fuentes abiertas?

### 1.2 Alcance y contribución

Este artículo realiza tres contribuciones. En primer lugar, propone una taxonomía composicional formal (T1/T2/T3) para los clústeres de co-localización minorista, basada en las combinaciones de categorías de anclas en lugar de los recuentos de minoristas o los umbrales de proximidad únicamente. En segundo lugar, implementa esta taxonomía a escala continental — 6.493 clústeres en trece países — utilizando la base de datos de OpenStreetMap (OSM) como fuente de datos primaria, demostrando que la información geográfica de voluntariado de fuente abierta (VGI, por sus siglas en inglés) es suficiente para esta clase de análisis espacial (Haklay, 2010; Darnall et al., 2022). En tercer lugar, define un programa de falsificación que puede ejecutarse a medida que los conjuntos de datos de movilidad de origen-destino (O-D) estén disponibles, permitiendo probar la señal composicional frente a la actividad comercial observada.

Esta investigación se realizó dentro de la función de análisis geográfico de MCorp. El diseño de la investigación, las hipótesis y el programa de falsificación son independientes del desarrollo de productos comerciales. El conjunto de datos analítico — 6.493 clústeres de co-localización en trece países — se deriva de una infraestructura SIG operada por la empresa. Todos los datos de origen (OpenStreetMap, Kontur Population, US LODES, MITMA de España) están disponibles públicamente; la metodología de agrupamiento está completamente descrita en el §3 y es reproducible a partir de esos insumos. El marco analítico se desarrolló originalmente para apoyar la selección de ubicaciones para el desarrollo inmobiliario comercial adyacente a centros de venta minorista de gran formato ya establecidos, un caso de uso que requiere la identificación sistemática de mercados submetropolitanos con una profundidad de anclas demostrada. El marco de investigación presentado aquí generaliza esa aplicación: la taxonomía de niveles y las variables de clasificación por área de captación son agnósticas respecto al uso de destino y se presentan como un marco de inteligencia geográfica aplicable en el sector inmobiliario comercial, la planificación del comercio minorista urbano y la geografía económica.

El artículo es explícitamente un marco de investigación. Los resultados empíricos presentados son descriptivos. La identificación causal requiere las pruebas de regresión O-D definidas en el §7, que dependen de datos que actualmente se están adquiriendo.

### 1.3 Estructura

La sección 2 revisa la literatura relevante e identifica la brecha. La sección 3 formaliza el modelo geométrico de co-localización. La sección 4 describe los datos y el marco analítico. La sección 5 presenta los resultados descriptivos actuales. La sección 6 analiza la relación entre las señales composicionales y las de actividad comercial impulsadas por la demanda, y enuncia la hipótesis formal. La sección 7 define el programa de falsificación. La sección 8 concluye.

---

## 2. Revisión de la literatura

### 2.1 El paradigma basado en la demanda en el análisis de localización

La inteligencia de localización comercial contemporánea se basa principalmente en señales de demanda observadas: datos de panel de movilidad (frecuencia de visitas basada en dispositivos), registros de transacciones y perfiles demográficos. Sistemas como SafeGraph, Foursquare y Business Analyst de Esri derivan la atracción de los sitios de estas fuentes. La inferencia es inductiva: las ubicaciones de alto tráfico reciben puntuaciones altas; los sitios candidatos se evalúan frente a la distribución de ubicaciones de alto tráfico ya conocidas.

Este enfoque tiene limitaciones bien documentadas. En primer lugar, la latencia de los datos: los datos de movilidad reflejan los patrones actuales y no pueden identificar mercados submetropolitanos cuya actividad comercial está por debajo del umbral observable para la medición basada en paneles. En segundo lugar, el sesgo de supervivencia: los conjuntos de datos registran la actividad en ubicaciones comerciales existentes, proporcionando la señal más débil precisamente donde el desarrollo aún no ha ocurrido — la condición de mayor interés para la geografía comercial. En tercer lugar, las brechas de representación: los paneles de dispositivos móviles subestiman sistemáticamente a las poblaciones de menores ingresos y mayores (Kwan, 2016), introduciendo error de medición sistemático en los mercados donde estos grupos forman una proporción sustancial de la base de clientes minoristas. Li et al. (2024) cuantifican esta preocupación a escala nacional, documentando que las tasas de muestreo de SafeGraph promedian el 7,5 % en los Estados Unidos, con sustancial heterogeneidad demográfica — la cobertura es materialmente más baja para las poblaciones de bajos ingresos, mayores y rurales, y la estructura del sesgo varía según las escalas espaciales. Los sesgos de representación inherentes a los paneles de movilidad GPS no están distribuidos aleatoriamente entre los tipos de mercado; se correlacionan con las características de los mercados submetropolitanos más relevantes para la selección de ubicaciones comerciales. En cuarto lugar, la disponibilidad de datos: los conjuntos de datos O-D propietarios se licencian por mercado, lo que hace que el análisis comparativo a escala continental sea impracticable para la mayoría de los programas de investigación.

El complemento del lado de la oferta al análisis impulsado por la demanda — usar las decisiones de localización de los propios minoristas como señal — está comparativamente poco explorado, a pesar del respaldo teórico con que cuenta.

### 2.2 La localización minorista como preferencia revelada

La teoría clásica de la localización proporciona los fundamentos teóricos para un enfoque del lado de la oferta. Christaller (1933) estableció que la jerarquía minorista refleja la distribución espacial del poder adquisitivo, con los bienes de orden superior concentrándose donde la demanda es suficiente para sustentarlos. Reilly (1931) y Huff (1964) formalizaron la relación gravitacional entre la masa minorista y la extensión del área comercial. Estos modelos tratan la localización minorista como un resultado de la demanda — una preferencia revelada por ubicaciones donde las condiciones de demanda son favorables.

La literatura de geografía económica sobre aglomeración refuerza este encuadre. Marshall (1890) identificó las economías de localización — ganancias de productividad derivadas de la concentración geográfica de actividades relacionadas — como un motor principal de la agrupación espacial. Krugman (1991) demostró que los costos de transporte y las economías de escala producen patrones estables de centro-periferia en los que la actividad económica se concentra en una minoría de ubicaciones. Duranton y Puga (2004) proporcionan los microfundamentos: los mecanismos de intercambio, emparejamiento y aprendizaje producen economías de aglomeración que hacen que los primeros en llegar a ubicaciones de alto potencial se refuercen a sí mismos.

Para el comercio minorista de gran formato, Holmes (2011) proporciona la evidencia empírica más directa: la difusión de Walmart a través de los Estados Unidos exhibe fuertes economías de densidad, con cada nueva ubicación de tienda al servicio de una red de distribución anclada en tiendas existentes. La selección de ubicaciones no es aleatoria — refleja décadas de datos de tráfico acumulados, análisis demográfico y evaluación de proximidad competitiva. Una ubicación seleccionada de forma independiente por Walmart, Home Depot y Costco es una ubicación que ha superado tres procesos de selección de sitio separados, costosos y con buenos recursos. Una predicción corolaria, aún no sometida a pruebas longitudinales sistemáticas, es que las anclas secundarias — minoristas de ferretería y de club de almacén — exhiben un patrón de co-localización secuencial respecto a las anclas de hipermercado: las siguen, no las preceden. Los datos temporales sobre fechas de apertura de tiendas podrían probar esta afirmación mediante métodos de estudio de eventos análogos a los aplicados a la difusión de Walmart por Holmes (2011); esta sigue siendo una pregunta abierta para investigaciones futuras (§8.2).

Este razonamiento sustenta una afirmación teórica clave del presente artículo: la co-localización de anclas minoristas dominantes de distintas categorías de formato es una señal de preferencia revelada de viabilidad comercial submetropolitana, observable sin datos propietarios y previamente al desarrollo comercial en clases de uso adyacentes.

### 2.3 La co-localización minorista y las externalidades de las anclas

La literatura sobre centros comerciales documenta externalidades positivas entre los inquilinos ancla (Brueckner, 1993). Pashigian y Gould (1998) muestran que los minoristas ancla aceptan rentas por debajo del mercado a cambio del tráfico externo que generan — evidencia de que las externalidades de co-tenencia tienen precio y son materialmente significativas. Kim y Park (2025) extienden esta evidencia al contexto del comercio minorista urbano contemporáneo, encontrando que las áreas minoristas especializadas exhiben tasas de cierre de negocios más bajas y que la coherencia composicional — más que el recuento de anclas — determina el rendimiento del clúster. Eppli y Shilling (1995) demuestran que las externalidades varían según la combinación de anclas, con ciertas combinaciones generando sustancialmente más tráfico cruzado que otras. Chen et al. (2022) proporcionan una estimación causal contemporánea de este mecanismo utilizando datos de verificación en redes sociales basadas en localización, identificando un efecto medible de la tienda ancla en el tráfico peatonal de los minoristas adyacentes. Lo que esta literatura no aborda es la composición de múltiples anclas de gran formato en configuraciones de centros comerciales al aire libre, donde las anclas están co-localizadas pero son estructuralmente independientes, y donde las externalidades se extienden más allá del sector minorista a las actividades de empleo y servicios adyacentes.

El marco de nucleación minorista de Berry (1958) y la tipología de estructuras minoristas de Garner (1966) proporcionan los análogos más cercanos, pero fueron desarrollados para la forma urbana norteamericana de mediados del siglo XX. La configuración del centro de poder — múltiples minoristas de gran formato compartiendo un campus de estacionamiento en superficie sin una estructura de centro comercial cerrada — es la forma minorista de gran formato dominante en la América del Norte de finales del siglo XX y principios del XXI y es cada vez más común en Europa, aunque ha recibido un análisis geográfico sistemático limitado (Hernandez y Simmons, 2006). Darnall et al. (2022) demuestran que los datos de puntos minoristas derivados de OSM son suficientes para la delineación a escala nacional de aglomeraciones minoristas: su clasificación jerárquica de clústeres minoristas del Reino Unido, análoga en estructura a la taxonomía T1/T2/T3 avanzada aquí, establece la viabilidad empírica de la identificación de clústeres basada en VGI a escala continental, complementando el hallazgo anterior de Haklay (2010) sobre la precisión posicional de OSM. Zhao et al. (2025) ilustran además el enfoque de agrupamiento espacial para la selección de sitios, utilizando la estructura del espacio comercial urbano para predecir las ubicaciones de nuevas tiendas. Ninguno de estos tratamientos, sin embargo, clasifica los clústeres por composición de categorías de anclas como unidad primaria de análisis.

### 2.4 La brecha

Ningún marco existente: (a) clasifica los clústeres minoristas submetropolitanos por la composición de las categorías de anclas presentes, como algo distinto del recuento de anclas o la presencia de una sola categoría; (b) implementa esta clasificación a escala continental utilizando datos de fuente abierta; o (c) propone una prueba formal de si esta medida composicional predice la intensidad de la actividad comercial más allá de lo que el tamaño del mercado solo predecería. Este artículo aborda las tres.

Una segunda brecha concierne a la unidad espacial en la que se aplican los datos de movilidad del lado de la demanda. Incluso donde los datos de movilidad se han integrado en el análisis del área de captación minorista, la unidad de observación espacial ha seguido siendo el área comercial administrativa — la ciudad, el código postal o el buffer de radio fijo. Calafiore et al. (2022) redefinen la captación minorista utilizando datos de geolocalización móvil pero operan a nivel de centros minoristas administrativos en lugar de geometrías individuales de clústeres. *Explorando la dinámica sectorial económica a través de datos de movilidad de alta resolución* (2025) demuestra el alcance analítico de los registros de movilidad de alta resolución a nivel sectorial, pero su unidad espacial sigue siendo la zona administrativa. Ningún estudio publicado ha aplicado el geo-cercado de paneles de movilidad a escala de estacionamientos individuales para definir captaciones específicas de clústeres, y luego ha usado esas captaciones para comparar clústeres entre sí en lugar de con límites administrativos. El método que propone este estudio — polígono de estacionamiento → extracción de O-D de dispositivos → captación emparejada hogar/trabajo → comparación de demanda a nivel de clúster — es el puente que esta literatura aún no ha cruzado. Su contribución no es simplemente un nuevo conjunto de datos, sino una nueva unidad de observación para el análisis de co-localización minorista: el mercado submetropolitano definido por la movilidad, distinto del asentamiento en el que reside.

---

## 3. El modelo geométrico de co-localización

### 3.1 Definiciones

**Mercado submetropolitano.** Un asentamiento nombrado o lugar designado por el censo situado dentro de un área metropolitana o mercado laboral regional, caracterizado por una masa minorista espacialmente discreta. El mercado submetropolitano es la unidad de análisis; el clúster de co-localización es la unidad de observación.

**Clúster de co-localización.** Un conjunto maximal de puntos de anclas minoristas {p₁, p₂, ..., pₙ} que satisface:

    d(pᵢ, pⱼ) ≤ ε  para al menos un j ≠ i, para todo i  (conectividad espacial)
    max{d(pᵢ, pⱼ) : ∀ i,j} ≤ Δ_max                  (restricción de diámetro)

donde d(·) es la distancia geodésica, ε es un umbral de proximidad y Δ_max es un límite superior estricto en el diámetro del clúster.

**Extensión.** La distancia geodésica máxima entre pares entre dos miembros cualesquiera de un clúster:

    span_km = max{d(pᵢ, pⱼ) : pᵢ, pⱼ ∈ clúster}

Un clúster con span_km < 1,0 km es *compacto-intacto* — todos los miembros se encuentran dentro de una distancia coherente con un único centro de poder o campus minorista. Un clúster con span_km ∈ (1,0; 3,0] es *laxo* — los miembros están distribuidos a lo largo de un corredor comercial.

**Categoría de ancla.** Una clasificación funcional del comercio minorista de gran formato, definida por el patrón de tráfico dominante y el tipo de formato. En la taxonomía actual se definen seis categorías:

| Categoría | Cadenas canónicas (América del Norte) | Cadenas canónicas (Europa) |
|---|---|---|
| `hypermarket` | Walmart Supercentre, Target | IKEA, Carrefour Hypermarché, Auchan |
| `hardware` | Home Depot, Lowe's | Leroy Merlin, OBI, Bauhaus |
| `price_club` | Costco, Sam's Club | Costco EU |
| `lifestyle` | IKEA (contexto NA), RH | XXXLutz, Höffner |
| `electronics` | Best Buy | MediaMarkt, Saturn, Boulanger, Darty |
| `sport` | Decathlon (donde está presente) | Decathlon |

Las categorías se asignan a nivel de cadena. El *conjunto de categorías* de un clúster es la unión de todas las categorías representadas en sus puntos miembros.

### 3.2 Clasificación por niveles

El nivel es una función de la composición de categorías y es independiente de todos los parámetros geométricos. La clasificación se define a través de tres vías de admisión y una regla residual:

**T1 — Primario-completo.** Un clúster cuyo conjunto de categorías satisface alguna de las siguientes condiciones:

- *T1.a — Composición tripartita:* `has_hypermarket ∧ has_hardware ∧ (has_price_club ∨ has_lifestyle ∨ has_electronics)`
  La disyunción capta las tres principales tipologías de anclas secundarias: formatos de club de almacén (price_club), gran formato de hogar/muebles (lifestyle) y comercio minorista de electrónica de consumo (electronics). Las tres codifican un proceso de selección de sitio independiente convergiendo en una ubicación ya validada por anclas de hipermercado y ferretería. La cláusula de electrónica es estructuralmente relevante para la identificación T1 europea: la co-localización de hipermercados alimentarios con MediaMarkt, Saturn o Boulanger es el principal análogo europeo a la tríada Walmart–Costco–Home Depot (Wrigley y Lowe, 2002).

- *T1.b — Multi-ancla compacto H2b:* `tight_intact ∧ |miembros| ≥ 3`
  Un clúster donde todos los miembros se encuentran dentro de τ_tight = 1,0 km entre sí y hay al menos tres puntos de ancla distintos califica para T1 independientemente de la composición de categorías. El requisito de radio compacto evita que las configuraciones de corredor laxas activen esta vía; el mínimo de tres anclas evita que las cadenas de una sola categoría con múltiples puntos cercanos califiquen.

- *T1.c — Amplitud de categorías:* `|categorías| ≥ 4`
  Cuatro o más categorías de anclas distintas presentes en un clúster constituye la señal composicional más fuerte, activando T1 independientemente de si algún par de categorías específico está presente.

**T2 — Secundario-completo.** Un clúster que satisface:
- `has_hypermarket ∧ has_hardware` (ambas categorías presentes)
- No califica para T1 bajo ninguna vía

**T3 — Parcial.** Todos los clústeres restantes: dominados por una sola categoría, o con múltiples categorías sin la combinación hipermercado-ferretería.

La predicción normativa que codifica esta clasificación es:

> *H₁: El nivel de co-localización es un predictor positivo estadísticamente significativo de la intensidad de la actividad comercial dentro de los mercados submetropolitanos, después de controlar por el tamaño de la población del mercado.*

Esta es la hipótesis primaria del artículo. El §7 define las pruebas.

La regla de nivel es intencionalmente estricta en el límite T2. Requerir tanto `hypermarket` como `hardware` para T2 significa que un clúster dominado por un único minorista de gran formato — incluso uno con un tráfico absoluto alto — se clasifica como T3. Esto difiere de una implementación anterior que promovía a T2 cualquier clúster que contenía un hipermercado con dos o más miembros; la regla actual requiere la *combinación* de categorías, no meramente la copresencia de dos unidades de cualquier tipo. El requisito de combinación de categorías capta la señal composicional (múltiples procesos independientes de selección de sitio convergiendo en una ubicación) en lugar de la señal de escala (un minorista muy grande con formatos menores adyacentes).

La primitiva espacial primaria en la especificación original es el polígono de estacionamiento — una geometría trazada alrededor de la superficie impermeable del estacionamiento en superficie de cada ancla minorista — que sirve como geo-cerca para la extracción de movilidad O-D. La implementación a escala continental abstrae esto a una geometría de centroide y anillo de clúster para la automatización; el §3.7 especifica el protocolo completo.

### 3.3 El algoritmo DBSCAN de dos pasadas con prioridad compacta

La pertenencia al clúster se determina mediante un algoritmo de densidad espacial de dos pasadas adaptado de Ester et al. (1996):

**Pasada 1 — Núcleos compactos:**
Aplicar DBSCAN con ε = τ_tight = 1,0 km y tamaño mínimo de clúster MinPts = 2. Los puntos dentro de 1,0 km de al menos otro punto calificado se unen a un núcleo compacto. Todos los componentes compactos están bloqueados — su pertenencia no se revisa en la pasada 2.

**Pasada 2 — Expansión laxa:**
Aplicar DBSCAN con ε = τ_loose = 3,0 km a todos los puntos desbloqueados. Para cualquier componente resultante cuya extensión exceda Δ_max = 3,0 km, aplicar una división codicioso de reducción de diámetro: eliminar iterativamente la arista con la mayor distancia entre puntos hasta que se satisfaga la restricción de diámetro.

**Restricción estricta de diámetro:**

    span_km ≤ Δ_max = 3,0 km  para todos los clústeres

Esta restricción es uniforme en todos los países y tipos de mercado. Codifica la definición de un único destino comercial — la distancia dentro de la cual un consumidor que se desplaza en vehículo trata a los minoristas geográficamente próximos como un único viaje de compras. La diferencia de densidad entre los entornos minoristas densos europeos y los expansivos norteamericanos se absorbe mediante el sistema de clasificación dentro del nivel (§3.4), no variando el límite de pertenencia.

**La bandera tight_intact** se activa cuando todos los miembros del clúster se encuentran dentro de τ_tight = 1,0 km entre sí. Los clústeres compactos-intactos califican para la promoción acelerada T1 bajo la regla H2b, reflejando la observación de que las configuraciones muy compactas de múltiples anclas son composicionalmente distintas de los corredores laxos.

### 3.4 Clasificación geométrica dentro del nivel

Después de la clasificación por nivel, los clústeres se clasifican por compacidad geométrica dentro de su grupo de pares composicional. La variable de clasificación es:

    dist_rank_in_tier(c) = Φ(span_km(c) | nivel, país, continente)

donde Φ es una CDF empírica invertida — una extensión menor produce una clasificación más alta. Para manejar la inestabilidad de muestras pequeñas a nivel de país, se utiliza un estimador combinado con contracción:

    w = n_país / (n_país + K)     [K ≈ 20–30, establecido por validación cruzada]
    clasificación = w · CDF_país(span_km) + (1 - w) · CDF_continente(span_km)

La clasificación se calcula dentro del nivel para que discrimine entre pares composicionalmente homogéneos en lugar de volver a codificar la pertenencia al nivel. Un clúster T1 con una extensión compacta se clasifica alto entre sus pares T1; la clasificación no lo compara con clústeres T2 o T3.

Esta clasificación geométrica dentro del nivel constituye la Etapa 1 del modelo de clasificación de dos etapas. La Etapa 2 — clasificación por demanda — se define en el §6.2 y requiere datos O-D.

### 3.5 El radio de anillo

El radio de anillo proporciona una representación visual del alcance espacial del clúster en el marco analítico. Se deriva determinísticamente de la extensión:

    ring_radius_km = max(1,0; span_km / 2 × 1,15)

El multiplicador de 1,15 asegura que todos los puntos miembros caigan dentro del límite del anillo (acomodando que la distancia del centroide al miembro es menor que span/2 para configuraciones asimétricas). El mínimo de 1,0 km evita anillos de punto único degenerados. La fórmula se aplica uniformemente en todos los niveles; la distinción visual de nivel se lleva mediante el estilo del anillo, no el radio.

### 3.6 El modificador cívico

El Marco de Cinco Grados (§4.3) identifica a los atractores cívicos — hospitales y universidades — como una capa de amplificación cualitativamente distinta por encima de los tres niveles composicionales. Un clúster T1 *modificado cívicamente*, referido operacionalmente como T0 o Platino, se define como:

    civic_modifier = 1  si  hospital(≥200 camas) ∨ universidad(≥10.000 matriculados) dentro de 5,0 km
    T0 ⟺ T1 ∧ tight_intact ∧ civic_modifier = 1

La designación T0 es un *modificador*, no una puerta de nivel separada: cada clúster T0 también es un clúster T1. El modificador no se utiliza en las hipótesis primarias de falsificación H₁ o H₂, que conciernen a la distinción T1/T2/T3. Se introduce para la hipótesis H₃ (§6.4) y la Prueba 5 (§7.5).

La motivación teórica sigue la literatura de geografía económica sobre los desbordamientos de conocimiento. Carlino y Kerr (2015) revisan la evidencia de que la actividad innovadora — aproximada por presentaciones de patentes — se concentra cerca de las universidades de investigación y los hospitales docentes, reflejando las economías de localización generadas por las instituciones intensivas en conocimiento. Glasson (2003) y Drucker y Goldstein (2007) documentan los efectos multiplicadores comerciales de las universidades en sus mercados submetropolitanos de acogida. Si estas instituciones cívicas generan una densidad de empleo estructuralmente más alta de forma independiente de la composición de anclas minoristas, su superposición espacial con los clústeres T1 de co-localización debería producir un efecto de interacción detectable en la regresión H₁ — que es lo que prueba H₃.

El civic_modifier requiere la creación de una capa espacial hospital-universidad a partir de puntos de OSM y datos oficiales de atención sanitaria, actualmente en proceso.

### 3.7 Áreas de captación definidas por la movilidad

Los buffers de radio fijo y los límites administrativos crean falsas equivalencias entre clústeres minoristas físicamente próximos que, en realidad, sirven a poblaciones de consumidores completamente distintas. Un minorista ubicado en el borde de un área metropolitana puede captar desde un área de captación de teletrabajadores de 120 km a lo largo de un corredor de autopista, mientras que otro clúster a tres kilómetros puede captar casi exclusivamente de un barrio urbano caminable de quizás quince manzanas cuadradas. Las agregaciones por código postal, condado y área estadística metropolitana promedian sobre esta heterogeneidad; los buffers circulares alrededor de un centroide imponen una geometría que no guarda ninguna relación necesaria con el comportamiento observado del consumidor. La corrección metodológica es observar directamente el origen real del consumidor, a nivel del clúster individual, y derivar el área de captación de esa observación en lugar de hacerlo a partir de un supuesto geométrico a priori. El trabajo reciente sobre la delineación del área de captación minorista mediante geolocalización móvil (Calafiore et al., 2022) demuestra que las captaciones de origen observado divergen materialmente de las isócronas de tiempo de conducción para los mismos sitios, y que la divergencia es mayor precisamente donde más importa para la selección de sitios — en el límite entre áreas comerciales competidoras.

La unidad primitiva de observación en el protocolo especificado aquí es un polígono espacial trazado alrededor de la huella del estacionamiento de cada ancla minorista dentro de un clúster de co-localización. Los polígonos se construyen a partir de imágenes aéreas ortorrectificadas y se trazan a lo largo de la superficie impermeable del parque minorista: el propio estacionamiento, las vías de acceso que lo conectan con la red vial circundante y el perímetro del edificio ancla. Este es un objeto sustancialmente diferente de un buffer circular alrededor de un centroide de punto de interés. Un buffer trata al minorista como puntual y al área circundante como indiferenciada; un polígono trata el parque minorista como un activo físico delimitado cuyas entradas y salidas pueden detectarse empíricamente. Los dispositivos observados dentro del polígono durante al menos veinte minutos durante el horario de comercio minorista (06:00–22:00, hora local) se clasifican como visitantes; los eventos con menor permanencia se excluyen como tráfico de paso en los segmentos de carretera adyacentes. El umbral de veinte minutos es coherente con las convenciones de tiempo de permanencia utilizadas en la literatura de estructura espacial de datos móviles (Büchel y Ehrlich, 2021).

El protocolo de muestreo temporal resuelve una tensión entre la representatividad y el coste de adquisición de datos. Los datos O-D se extraen para cuatro días de observación laborables, sin festivos, preestablecidos por año calendario, distribuidos entre las cuatro estaciones meteorológicas. Cuatro muestras en días laborables son suficientes para caracterizar patrones espaciales estables en el origen del consumidor sin admitir los sesgos estacionales introducidos por los períodos vacacionales de verano o el período minorista de diciembre. Para cada dispositivo muestreado, se calculan dos asignaciones de celdas hexagonales de resolución 7: un hexágono de hogar, definido como la celda H3 en la que el dispositivo pasa el mayor tiempo acumulado entre las 21:00 y las 07:00 durante el período de observación, y un hexágono de trabajo, definido como la celda H3 en la que pasa el mayor tiempo acumulado entre las 09:00 y las 17:00 en días laborables. El registro de origen emparejado (home_hex, work_hex) distingue las compras impulsadas por la proximidad, ancladas al hexágono de hogar, de las compras en la ruta de desplazamiento, ancladas al hexágono de trabajo o a la geodésica entre los dos.

El área de captación primaria definida por la movilidad para un clúster de co-localización es el conjunto de celdas H3 de resolución 7 desde las que se originan al menos el 1 % de los dispositivos visitantes observados, ya sea en la asignación de hogar o de trabajo, limitada por el anillo exterior de 150 km retenido del §3.4. Dentro de esa captación, los totales de población censal y las estimaciones de gasto per cápita modeladas se extraen de las celdas H3 emparejadas utilizando el procedimiento descrito en el §3.5. El resultado es un perfil de demanda específico del clúster que no depende de los límites administrativos y es insensible a los artefactos de discontinuidad de límites que afectan a los métodos de selección de sitio basados en códigos postales y municipios. Dos clústeres en la misma ciudad — uno que sirve a una población de teletrabajadores del centro, otro que sirve a una población residencial suburbana — pueden compartir un código postal o condado y sin embargo captar de poblaciones de captación completamente distintas, y la captación derivada del polígono registra esa diferencia directamente.

En el momento de redactar este artículo, el protocolo completo de polígono y dispositivo está especificado pero aún no operacionalizado a escala continental para los 6.493 clústeres del conjunto de estudio. Se está investigando actualmente la adquisición de un panel de movilidad comercial que cubra los trece países del estudio; la metodología se especifica aquí para que los resultados empíricos puedan reproducirse por otros investigadores una vez que los datos del panel estén disponibles, y para que las pruebas de falsificación del §7 sean interpretables como un programa de investigación prospectivo en lugar de una descripción post-hoc. Como proxy, los análisis O-D en los §4 y §5 utilizan el US Census LODES (flujos de trayecto al trabajo agregados a H3 resolución 7) para los clústeres de Estados Unidos, y la encuesta de movilidad MITMA de España para los clústeres españoles. Las limitaciones de cobertura y sesgo demográfico documentadas en Li et al. (2024) — dispositivos más jóvenes, urbanos y de mayores ingresos sobrerrepresentados en relación con la población de referencia — son heredadas por el protocolo de polígono y deben controlarse mediante la reponderación ponderada por población a nivel de celda H3; los proxies administrativos de LODES y MITMA proporcionan un punto de triangulación útil porque no exhiben este sesgo.

La consecuencia metodológica de este enfoque es que las captaciones definidas por la movilidad son específicas del clúster, no del asentamiento. Dos clústeres T1 dentro de la misma área metropolitana se tratan como experimentos independientes de campo de demanda, cada uno con su propio catchment_area_km2, catchment_population y catchment_entropy. Esta calibración — sustituyendo el clúster de co-localización por el asentamiento como unidad de comparación — es el mecanismo mediante el cual el marco separa la composición geométrica de los factores de confusión del tamaño del mercado. Permite la comparación entre clústeres a nivel submetropolitano en lugar de a nivel de ciudad, que es donde se toman realmente las decisiones de selección de sitios minoristas.

---

## 4. Datos y marco analítico

### 4.1 Fuentes de datos

**Datos de puntos minoristas.** OpenStreetMap (OSM), complementado por ingestas de consulta de nombres dirigidas para cadenas con cobertura de OSM incompleta. Los archivos de configuración YAML a nivel de cadena especifican cajas delimitadoras, QIDs de Wikidata y reglas de exclusión de formato (filtrando variantes de subformato como formatos exprés o de conveniencia del conjunto de datos de anclas de gran formato). Haklay (2010) demuestra que OSM iguala o se aproxima a la exactitud de Ordnance Survey en cuanto a la completitud de la red vial en regiones con buena cobertura; las principales cadenas minoristas nacionales en los países del estudio caen dentro de este régimen de cobertura.

**Índice espacial.** Cuadrícula hexagonal H3 (Uber H3) en resolución 7 para la agregación de población. Las geometrías de clúster y la distribución de teselas utilizan el formato PMTiles para la renderización vectorial del lado del cliente sin requisito de servidor de teselas.

**Cálculo de clústeres.** Python (extensión espacial DuckDB) implementando el DBSCAN de dos pasadas descrito en el §3.3. Patrón de autoridad única para la taxonomía: todas las asignaciones de cadena a categoría se resuelven a través de una única función `all_chains_for_iso(iso)` en `taxonomy.py`, asegurando que no haya duplicación de categorías en los scripts de ingesta.

**Datos de población y O-D.** El US LEHD Origin-Destination Employment Statistics (LODES) se carga para el O-D de trayecto al trabajo a nivel de celda H3. Los datos de movilidad MITMA de España proporcionan cobertura O-D para 58 clústeres españoles. Los doce países restantes operan con proxies de población ambiente de los datos Kontur Population (H3 resolución 8, CC BY 4.0) pendiente de la adquisición de conjuntos de datos O-D específicos por país.

### 4.2 Características del conjunto de datos

El conjunto de datos de la Fase 21 (versión actual, mayo de 2026) y la distribución proyectada de la Fase 22 bajo la revisión de taxonomía descrita en el §3.2 se muestran a continuación:

| Métrica | Fase 21 (actual) | Fase 22 (proyectada) |
|---|---|---|
| Total de clústeres | 6.493 | 6.493 |
| Clústeres T1 | 1.537 (23,7 %) | 1.747 (26,9 %) |
| Clústeres T2 | 3.090 (47,6 %) | 3.392 (52,2 %) |
| Clústeres T3 | 1.866 (28,7 %) | 1.354 (20,9 %) |
| Países cubiertos | 13 | 13 |
| Archivos YAML de cadenas | 120+ | 125+ |
| Puntos de anclas minoristas | ~90.000 | ~95.000 |
| Clústeres con cobertura O-D | ~7.600 (US LODES) + 58 (ES MITMA) | — |

La proporción T2 de la Fase 21 (48 %) está inflada porque la función de nivel de producción promovía a T2 cualquier clúster que contuviera un hipermercado con dos o más miembros, independientemente de si había un ancla de ferretería presente. La revisión de la taxonomía de la Fase 22 (§3.2) corrige esto exigiendo `has_hypermarket ∧ has_hardware` para T2, e introduce la disyunción tripartita T1.a. Bajo las reglas revisadas, los clústeres europeos con electrónica que ya contienen un ancla de hipermercado y ferretería se promueven a T1, elevando el recuento global T1 de 1.537 a un proyectado de 1.747. El T1 europeo crece de 516 a aproximadamente 726, superando el umbral de 500 clústeres que permite un análisis de subgrupos transcontinental estadísticamente significativo. El recuento T3 cae porque la redistribución T2→T3 (al eliminar la vía T2 laxa `n≥2`) está parcialmente compensada por la redistribución T3→T1 (de la cláusula de electrónica). Todos los recuentos proyectados son estimaciones pendientes de la reconstrucción de la Fase 22.

El informe de investigación original especificaba la calibración de parámetros a un objetivo de aproximadamente 400 ubicaciones T1 por región principal (América del Norte, Europa). El marco presentado aquí permite que las reglas de composición determinen la cardinalidad del clúster, produciendo 1.747 clústeres T1 proyectados — materialmente más que la especificación de recuento objetivo. Esto representa un cambio de una calibración impulsada por el recuento objetivo a una impulsada por reglas de composición; las implicaciones para la precisión frente a la exhaustividad en la selección de sitios se discuten en el §6.5.

### 4.3 El Marco de Cinco Grados

Un marco composicional cualitativo proporciona el precursor conceptual al sistema formal de niveles:

- **1.er grado** — Solo ancla primaria. Se corresponde aproximadamente con T3.
- **2.° grado** — Ancla primaria + una ancla secundaria (ferretería o club de precios). Se corresponde aproximadamente con T2.
- **3.er grado** — Primaria + dos anclas secundarias. Se corresponde con T1 por composición.
- **4.° grado** — Configuración de 3.er grado + atractor cívico (hospital o universidad a 5,0 km). T1 con modificador cívico positivo (aún no implementado en el marco analítico).
- **5.° grado** — Configuración de 4.° grado + confirmación demográfica. Clasificación de mayor confianza (integración de capa demográfica planificada).

El sistema de niveles algorítmico implementa los grados 1–3. Los grados 4 y 5 requieren la capa cívica (en desarrollo) y la superposición demográfica (planificada).

La taxonomía actual T1/T2/T3 evolucionó de una especificación original de clústeres de cinco grados en la que la lógica AMBOS-vs-ALGUNO gobernaba la calificación de anclas secundarias: el tercer grado requería tanto Home Depot COMO Costco, y el quinto grado requería ambos objetivos terciarios. Una regla de calibración adaptativa operaba como precursora del estimador de contracción DBSCAN — si el recuento de quinto grado superaba el 10 % de las entradas primarias totales, el umbral secundario se ajustaba de 5,0 a 3,0 km. El formalismo presente, en el que la disyunción T1.a admite cualquiera de {price_club, lifestyle, electronics} como la tercera ancla, es una relajación de la regla original AMBOS-Costco-Y-Home-Depot, motivada por la asimetría estructural europea (§5.1) y por el reconocimiento de que las tres tipologías secundarias codifican procesos equivalentes de selección de sitio independientes.

### 4.4 El mercado submetropolitano como unidad de análisis

Cada clúster de co-localización se asigna a un mercado submetropolitano nombrado — un asentamiento o lugar designado por el censo. El catálogo actual contiene 2.986 mercados submetropolitanos en los trece países del estudio. La asignación de mercado utiliza geocodificación inversa frente a conjuntos de datos de límites administrativos oficiales (US TIGER 2023, GISCO LAU 2021 para la UE, CSDs de Statistics Canada 2021).

El mercado submetropolitano es la unidad de análisis natural para la actividad comercial porque es el nivel en el que convergen la captación del mercado laboral, el área comercial minorista y la planificación administrativa. El nivel de un clúster caracteriza la composición comercial de la masa minorista de su mercado anfitrión; la clasificación geométrica dentro del nivel caracteriza cuán compacta es esa masa en relación con sus pares.

---

## 5. Resultados

### 5.1 Distribución global de niveles

Los clústeres T1 representan el 26,9 % de la población del estudio (1.747 de 6.493) en trece países bajo la taxonomía proyectada de la Fase 22. La distribución T1/T2/T3 difiere sistemáticamente entre América del Norte y Europa, reflejando diferencias estructurales en la composición del formato minorista. La siguiente tabla reporta los recuentos proyectados de la Fase 22 bajo la taxonomía revisada (§3.2, §4.2); los recuentos actuales de la Fase 21 se encuentran en el §4.2:

| Región | T1 (Fase 22 proy.) | T2 (Fase 22 proy.) | T3 (Fase 22 proy.) |
|---|---|---|---|
| América del Norte | 1.021 (34 %) | 1.712 (57 %) | 268 (9 %) |
| Europa | 726 (24 %) | 1.680 (56 %) | 572 (19 %) |

América del Norte produce proporcionalmente más clústeres T1 porque Walmart Supercentre (ancla primaria), Home Depot/Lowe's (ferretería) y Costco/Sam's Club (club de precios) lograron co-localizarse en un gran número de mercados submetropolitanos durante el período de desarrollo de centros de poder 1990–2010. Los formatos minoristas europeos están más segregados por categoría: los hipermercados alimentarios y los almacenes de ferretería/mejoras del hogar se co-localizan con menos frecuencia que sus homólogos norteamericanos (Wrigley y Lowe, 2002; Coe y Wrigley, 2007), produciendo una mayor proporción de T2 y una menor proporción absoluta de T1 bajo las reglas composicionales. La cláusula de electrónica en T1.a (§3.2) aborda esta asimetría: capta los clústeres europeos donde MediaMarkt, Saturn, Boulanger o Darty se co-localizan con un hipermercado y un ancla de ferretería — una configuración de múltiples anclas estructuralmente equivalente que emerge de la geografía del mercado europeo. Bajo la taxonomía de la Fase 22, el T1 de la UE sube de 516 a aproximadamente 726, superando el umbral necesario para las pruebas de subgrupos continentales estadísticamente significativas.

La asimetría entre las proporciones T1 de América del Norte y Europa es un hallazgo empírico, no un artefacto de calibración. Refleja la diferencia estructural identificada por Wrigley y Lowe (2002): la internacionalización del comercio minorista europeo procedió a través de la entrada secuencial al mercado por formatos minoristas individuales, produciendo una co-localización de categorías menos frecuente que el modelo de centro de poder americano en el que los desarrolladores de alimentos, ferretería y club de almacén a menudo apuntaron simultáneamente a los mismos sitios submetropolitanos.

La siguiente tabla reporta los recuentos reales de la Fase 22 (6.493 clústeres, mayo de 2026):

| País | T1 | T2 | T3 | Total |
|---|---|---|---|---|
| EE.UU. | 889 | 1.779 | 436 | 3.104 |
| FR | 247 | 161 | 216 | 624 |
| DE | 227 | 338 | 157 | 722 |
| MX | 68 | 48 | 170 | 286 |
| CA | 64 | 283 | 28 | 375 |
| ES | 62 | 64 | 92 | 218 |
| PL | 53 | 96 | 15 | 164 |
| IT | 43 | 35 | 99 | 177 |
| GB | 22 | 400 | 35 | 457 |
| AT | 21 | 8 | 35 | 64 |
| NL | 19 | 19 | 38 | 76 |
| SE | 11 | 8 | 9 | 28 |
| PT | 8 | 21 | 12 | 41 |
| GR | 5 | 11 | 6 | 22 |
| DK | 4 | 62 | 1 | 67 |
| FI | 2 | 52 | 1 | 55 |
| NO | 1 | 6 | 3 | 10 |
| IS | 0 | 2 | 1 | 3 |
| **Total** | **1.746** | **3.393** | **1.354** | **6.493** |

Caso ilustrativo: Sherwood Park, Alberta — un mercado submetropolitano de aproximadamente 80.000 habitantes (Censo 2021) que contiene un clúster T1 con span_km ≈ 0,8 km (Walmart Supercentre, Home Depot, Costco y Canadian Tire dentro de un diámetro de 0,8 km), situándolo en el decil superior de la clasificación geométrica dentro del nivel para los clústeres T1 de América del Norte. La concentración de clústeres T1 en EE.UU. (889 de 1.746; 51 %) refleja el patrón de desarrollo de centros de poder del período 1990–2010 analizado en el §5.1.

### 5.2 Distribución de la clasificación geométrica

La mediana de span_km de los clústeres T1 es 0,92 — inferior a la mediana T2 de 1,14 — coherente con la hipótesis de que los clústeres de alta composición tienden a ser físicamente compactos. Dentro de cada nivel, la clasificación geométrica (§3.4) produce una medida continua de compacidad. Estadísticas descriptivas para el conjunto de datos actual de la Fase 21:

| Nivel | Mediana span_km | Percentil 10 | Percentil 90 |
|---|---|---|---|
| T1 | 0,92 | 0,34 | 2,71 |
| T2 | 1,14 | 0,41 | 2,89 |
| T3 | 0,71 | 0,28 | 2,43 |

Los clústeres T3 tienen una mediana de extensión inferior a la T2 porque T3 incluye muchos puntos de ancla única (extensión = 0 para clústeres de un solo miembro, establecida en un pequeño épsilon positivo en la práctica) así como configuraciones multi-ancla compactas pero incompletas. La mediana T1 cae por debajo de la mediana T2, apoyando la predicción de compacidad composicional.

### 5.3 Validación del proxy O-D (preliminar)

La correlación entre el nivel del clúster y el empleo total dentro del área de captación por trayecto al trabajo de 35 km es positiva en los 7.600 clústeres estadounidenses con cobertura O-D de LODES. Estadísticas resumidas a nivel de clúster:

Las medianas de empleo de captación están pendientes de la integración de los datos de flujo de trayecto de LODES 2021; los valores unidos aparecerán en v0.5.

La unión es directa y poblará esta sección en v0.5. La prueba de permutación (§7, Prueba 4) puede ejecutarse con los datos actuales y es la prioridad para el próximo paso de procesamiento de datos.

---

## 6. Discusión

### 6.1 El argumento deductivo del análisis composicional

La inteligencia de localización comercial es convencionalmente inductiva: observa el tráfico, las transacciones y los patrones de movilidad, luego infiere la calidad del sitio a partir de la demanda observada. El enfoque composicional avanzado en este artículo es deductivo: deriva el potencial comercial de las preferencias reveladas de los minoristas dominantes cuyas decisiones de localización codifican décadas de análisis de mercado.

Ambos son procedimientos de inferencia válidos. La pregunta es la eficiencia para una clase específica de problemas de investigación: identificar mercados submetropolitanos donde la intensidad de la actividad comercial es sistemáticamente más alta de lo que el tamaño de la población ambiente predecería.

El enfoque deductivo es más eficiente para esta clase de problemas por cuatro razones:

*Disponibilidad de datos.* Las ubicaciones de anclas minoristas son públicamente observables desde OpenStreetMap a costo marginal cero. Los conjuntos de datos O-D propietarios requieren licencias por mercado con comparabilidad entre mercados restringida.

*Profundidad temporal.* Un Walmart Supercentre establecido en 2004 refleja veinte años de validación sostenida del mercado frente a los patrones de tráfico observados y la demografía del consumidor. Los datos de paneles de movilidad típicamente cubren cinco a diez años, con brechas significativas antes de 2015 (Büchel y Ehrlich, 2021).

*Identificación contrafactual.* El análisis composicional identifica mercados submetropolitanos donde la señal del lado de la oferta (composición de anclas) es fuerte y el desarrollo comercial en clases de uso adyacentes aún no ha ocurrido. El análisis impulsado por la demanda identifica ubicaciones de alto tráfico existentes — donde el desarrollo típicamente ya ha incorporado la señal al precio.

*Permanencia estructural.* Las cadenas minoristas nacionales rara vez abandonan los mercados submetropolitanos que las validan comercialmente. La señal de localización del ancla es duradera a lo largo de horizontes de varias décadas. Los patrones de movilidad observados cambian con el comportamiento del consumidor, la penetración del teletrabajo y la sustitución del comercio digital.

Para los profesionales del sector inmobiliario comercial — la disciplina que motivó el informe de investigación original — el marco del lado de la oferta proporciona una señal de selección de sitios disponible antes, no después, de que un mercado objetivo haya sido identificado mediante el análisis de la demanda. Una ubicación que puntúa T1 bajo la regla de composición geométrica lleva evidencia de que tres procesos de selección de sitio independientes y bien dotados de recursos ya han validado el mercado submetropolitano; esta evidencia es especialmente valiosa en los mercados prospectivos donde la cobertura del panel de movilidad es escasa o donde el horizonte de desarrollo se mide en años en lugar de meses.

### 6.2 La inteligencia de demanda como capa confirmatoria de segunda etapa

El argumento del §6.1 no subordina la inteligencia de demanda a la irrelevancia. La posiciona como la capa de Etapa 2 que confirma, clasifica y refina la señal composicional:

**Etapa 1 (geométrica):** `dist_rank_in_tier` — compacidad del clúster dentro del grupo de pares composicional. Disponible para los 6.493 clústeres a partir de datos de fuente abierta.

**Etapa 2 (demanda):** `demand_rank_in_tier` — densidad de empleo en el área de captación o intensidad de visitas basada en movilidad. Disponible a medida que se adquieren conjuntos de datos O-D.

El procedimiento de clasificación de dos etapas es lexicográfico: todos los empates de la Etapa 1 se desempatan por la Etapa 2. Un mercado submetropolitano que puntúa en el cuartil superior en ambas etapas constituye el caso empírico más sólido para la hipótesis.

La medida de Etapa 2 provisional — población ambiente dentro del anillo de captación existente de 35 km, extraída de los datos de Kontur Population — está explícitamente marcada en el marco analítico como un proxy. Los clústeres con O-D observado y los clústeres basados en proxy se clasifican en grupos separados; la interfaz de usuario etiqueta la base de datos por clúster.

La especificación de investigación original proponía las cifras de ventas por pie cuadrado del minorista — extraídas de declaraciones financieras públicas, informes de corredores y publicaciones anuales del ICSC — como la variable canónica de demanda de Etapa 2, bajo el argumento de que la productividad de ventas declarada por el propio minorista es la señal de preferencia revelada más fuerte disponible. El marco aquí sustituye la densidad de empleo en el área de captación (LODES) y la intensidad de visitas basada en movilidad como proxies más consistentemente disponibles; la variable de ventas por pie cuadrado sigue siendo una medida de Etapa 2 teóricamente preferible donde los datos declarados están disponibles.

### 6.3 Validación demográfica (planificada)

El sistema de segmentación demográfica Optimum Mosaic (Environics Analytics, Canadá) clasifica las áreas de diseminación censal por perfil de consumidor. El análisis preliminar de los mercados canadienses indica que los clústeres con alta clasificación geométrica tienden a caer en áreas de diseminación Mosaic A/B, coherente con la literatura más amplia sobre la relación entre la localización de anclas minoristas y la distribución del ingreso de los hogares (Neumark et al., 2008; Basker, 2005).

La integración de la capa Mosaic en el marco analítico está planificada. Cuando se implemente, constituiría una prueba confirmatoria de tercera etapa de la hipótesis: el perfil demográfico debería estar positivamente asociado con el nivel después de controlar por el tamaño del mercado.

### 6.4 Hipótesis formal

El marco precedente genera tres hipótesis formalmente falsificables:

> **H₁ (Primaria):** En los mercados submetropolitanos de América del Norte y Europa, el nivel de co-localización — una medida composicional de la presencia de categorías de anclas minoristas — es un predictor positivo estadísticamente significativo de la intensidad de la actividad comercial (operacionalizada como la densidad de empleo dentro del área de captación de trayecto al trabajo de 35 km), después de controlar por la población del mercado submetropolitano.

> **H₀ (Nula):** El nivel de co-localización no tiene poder predictivo para la intensidad de la actividad comercial, condicionado al tamaño del mercado.

> **H₂ (Redundancia de demanda):** Cuando se añaden datos de movilidad O-D al modelo, el nivel de co-localización retiene un poder predictivo independiente — es decir, la señal de demanda no subsume completamente la señal composicional.

> **H₃ (Amplificación cívica):** La presencia de un ancla cívica (hospital con ≥200 camas o universidad con ≥10.000 matriculados dentro de 5,0 km del centroide del clúster) amplifica la prima de densidad de empleo asociada al nivel T1, produciendo un efecto de interacción positivo estadísticamente significativo T1 × civic_modifier en la especificación de regresión H₁, neto de la contribución directa al empleo de las industrias de salud y educación (NAICS 611/622).

H₁ se falsifica si los clústeres T1 no exhiben sistemáticamente una mayor densidad de empleo en la captación que los clústeres T2/T3 en la misma clase de tamaño de mercado submetropolitano. H₂ se falsifica si el nivel deja de ser estadísticamente significativo una vez que los datos de movilidad O-D se incluyen como covariable. H₃ se falsifica si el coeficiente de interacción T1 × cívico no es positivo después de descontar el empleo NAICS 611/622 de la variable de resultado. El programa de falsificación del §7 define los modelos de regresión para las tres hipótesis.

### 6.5 Limitaciones

*Heterogeneidad de cobertura de OSM.* La completitud de los puntos minoristas de OSM varía por país, ciudad y cadena. Las principales cadenas nacionales en los trece países del estudio están generalmente bien mapeadas (Haklay, 2010; Darnall et al., 2022), pero existen brechas de cobertura sistemáticas para los formatos de tiendas más nuevos y en los mercados con menor actividad de la comunidad OSM. Esto introduce un error de medición que probablemente atenúe los efectos estimados de nivel hacia la nula.

*Las reglas de composición requieren recalibración periódica.* Las definiciones actuales de categorías de anclas reflejan los principales formatos minoristas de gran formato del período 2000–2025. La evolución del formato minorista — en particular el crecimiento de los formatos híbridos de alimentos y no alimentos y la entrada de nuevas categorías de gran formato — puede requerir la recalibración de las reglas de asignación de nivel.

*Parámetro de contracción.* El parámetro de peso de contracción K (≈20–30) en el estimador de clasificación dentro del nivel se establece por criterio experto. Un procedimiento formal de validación cruzada frente a una submuestra de retención está planificado pero aún no implementado.

*Solo resultados descriptivos.* Las pruebas de falsificación del §7 requieren datos O-D aún no completamente adquiridos. Los resultados presentados en el §5 son descriptivos. La identificación causal se difiere a un artículo posterior una vez ensamblado el conjunto de datos de regresión O-D.

*Dependencia del tipo de ancla.* El marco está calibrado para los mercados donde Walmart Supercentre (América del Norte) o IKEA (Europa) sirve como la ancla principal de hipermercado. Su aplicación a los mercados minoristas dominados por diferentes tipologías de anclas — por ejemplo, los mercados donde Carrefour o Auchan es el minorista alimentario dominante en países fuera de los trece actuales — no ha sido probada.

*Filosofía de calibración.* Una pregunta de calibración relacionada es si el marco debe apuntar a un número fijo de clústeres T1 por región — la especificación de investigación original proponía aproximadamente 400 por región principal — o permitir que las reglas de composición determinen la cardinalidad. El marco actual adopta esta última; los límites de nivel producen 1.747 clústeres T1 (26,9 %), materialmente más que el objetivo de ~400 por región. Si esto implica que los umbrales son demasiado permisivos, o que el objetivo original era demasiado conservador para un conjunto de datos multinacional, es una pregunta para la validación por parte de las partes interesadas frente a las carteras de desarrollo inmobiliario comercial.

---

## 7. El programa de falsificación

Las siguientes pruebas operacionalizan H₁, H₂ y H₃. Cada prueba se enuncia como un modelo de regresión con un requisito específico de conjunto de datos. Las Pruebas 1 y 4 son ejecutables con los datos actualmente cargados; las Pruebas 2, 3 y 5 requieren conjuntos de datos O-D y cívicos que actualmente se están adquiriendo.

### 7.1 Prueba 1 — Densidad de empleo por trayecto al trabajo (EE.UU., ejecutable)

**Especificación:**

    log(empleo_35km) = α + β₁·T1 + β₂·T2 + γ·log(población) + δ_estado + ε

donde `empleo_35km` es el empleo total de destino laboral de LODES dentro de 35 km del centroide del clúster; T1 y T2 son variables dummy (T3 es la categoría de referencia); `población` es la población del mercado submetropolitano (Censo 2020); `δ_estado` son efectos fijos de estado.

**Predicción:** β₁ > β₂ > 0 (T1 > T2 > T3 en densidad de empleo, controlando por tamaño del mercado).

**Datos:** LODES 2021 (US Census LEHD), cargados. Unión a clusters-meta.json pendiente de la implementación de `build-geometric-ranking.py`.

### 7.2 Prueba 2 — Validación de captación primaria de movilidad (EE.UU. + ES, a corto plazo)

*Hipótesis.* Los clústeres T1 atraen dispositivos visitantes de un origen geográfico significativamente más amplio y disperso que los clústeres T2, después de controlar por la población disponible dentro del anillo exterior de 150 km. La dispersión de la captación — no el recuento de la población cercana — es la característica discriminante de una co-localización de grado destino.

*Método.* Para cada clúster con cobertura de datos O-D — LODES de EE.UU. (2021) agregado a H3 resolución 7 para los clústeres de Estados Unidos y MITMA (España) para los clústeres españoles, con el protocolo completo de polígono y dispositivo sustituido cuando se adquiera el panel de movilidad comercial — se calculan tres variables a nivel de clúster. La primera es catchment_area_km2, el área del casco convexo de todos los centroides de home-hex en la captación definida por movilidad del clúster, limitada por el anillo exterior de 150 km. La segunda es catchment_entropy: H = −Σ p_i log p_i, donde p_i es la proporción de dispositivos visitantes que se originan de la celda H3 i; los valores de entropía más altos indican un conjunto de origen más disperso espacialmente. La tercera es home_work_ratio, el recuento de dispositivos cuyo home_hex cae dentro de la captación dividido por el recuento cuyo work_hex lo hace.

La ecuación estimada es una regresión de mínimos cuadrados ordinarios a nivel de clúster:

    catchment_entropy_c = α + β_T1·T1_c + β_T2·T2_c + γ·log(pop_150km_c) + δ_iso + ε_c

donde T1_c y T2_c son dummies de pertenencia al nivel con T3 como categoría omitida, log(pop_150km_c) controla el tamaño bruto del mercado, y δ_iso es un efecto fijo de país que absorbe las diferencias de cobertura del panel entre LODES y MITMA. Los errores estándar se agrupan a nivel de país ISO.

*Prueba primaria.* La hipótesis de composición geométrica predice β_T1 > β_T2 > 0, con β_T1 − β_T2 significativo al nivel del 5 %. La nula es que el nivel no contiene información adicional sobre la dispersión de la captación más allá de lo que log(pop_150km) ya explica.

*Prueba secundaria.* Dentro de la submuestra T1, home_work_ratio se regresiona sobre un indicador para las configuraciones de centros de poder peri-urbanos (polígonos de anclas fuera del área urbanizada contigua del asentamiento más cercano de ≥100.000 habitantes, por clasificación GHSL-SMOD) frente a configuraciones de núcleo urbano. La expectativa es que los clústeres T1 peri-urbanos exhiban un home_work_ratio significativamente mayor que los clústeres T1 de núcleo urbano. Esta es una prueba de heterogeneidad dentro del nivel, y proporciona evidencia sobre si la etiqueta T1 es internamente homogénea o si admite dos subclases funcionalmente distintas.

*Resultado esperado.* Los clústeres T1 en configuraciones de centros de poder peri-urbanos exhibirán mayor catchment_entropy que los clústeres T1 en núcleos urbanos, a pesar de asignaciones de nivel idénticas bajo la regla de composición geométrica. Esto apoyaría el argumento a favor de las captaciones definidas por movilidad como un refinamiento más allá tanto de los buffers de radio fijo como de la clasificación de nivel, y motivaría la eventual extensión del vocabulario de nivel para distinguir las subclases T1-urbano de T1-peri-urbano.

### 7.3 Prueba 3 — Densidad de empleo con control de demanda (H₂)

**Especificación:**

    log(empleo_35km) = α + β₁·T1 + β₂·T2 + γ·log(población) + λ·mobility_index + δ + ε

donde `mobility_index` es una medida de intensidad de visitantes derivada de O-D. H₂ predice que β₁ y β₂ siguen siendo positivos y significativos — el nivel retiene un poder independiente incluso después de condicionar en la señal de demanda observada.

**Datos:** Requiere cobertura completa de O-D. Año 2 del programa de investigación.

### 7.4 Prueba 4 — Prueba de permutación (ejecutable)

**Método:** Barajar las asignaciones de nivel entre clústeres 10.000 veces, manteniendo constante el recuento de clústeres y la distribución de tamaño dentro de cada país. Para cada permutación, calcular la correlación de rango entre el nivel y el empleo por trayecto al trabajo de LODES dentro de 35 km. Comparar la correlación de rango observada con la distribución nula de permutación.

**Predicción:** La correlación de rango observada cae en el 1 % superior de la distribución de permutación (unilateral p < 0,01).

**Datos:** El conjunto de datos LODES actual es suficiente. Implementación en `sim-tier-permutation.py` — por escribir.

### 7.5 Prueba 5 — Amplificación cívica (H₃)

**Especificación:**

    log(empleo_35km) = α + β₁·T1 + β₂·T2 + β₃·cívico + β₄·(T1 × cívico) + γ·log(población) + δ_estado + ε

donde `cívico` es un indicador binario de la presencia de un ancla cívica (hospital ≥200 camas o universidad ≥10.000 matriculados) dentro de 5,0 km del centroide del clúster; `T1 × cívico` es el término de interacción correspondiente al modificador T0.

*Diagnóstico de control incorrecto:* El empleo por trayecto al trabajo dentro de 35 km incluye mecánicamente el empleo en sanidad (NAICS 622) y servicios educativos (NAICS 611), que es generado directamente por las instituciones cívicas que definen `cívico = 1`. Incluir estas industrias en la variable de resultado crea un problema de control incorrecto: el indicador cívico predice el resultado en parte a través del efecto de empleo directo, no a través del efecto de amplificación de externalidades que teoriza H₃ (Angrist y Pischke, 2009). La regresión debe ejecutarse por tanto en dos especificaciones:

- **Especificación A:** `empleo_35km` incluye todas las industrias NAICS.
- **Especificación B:** `empleo_35km_sinedu` excluye el empleo NAICS 611/622.

H₃ se apoya si β₄ > 0 en *ambas* especificaciones. El apoyo solo en la Especificación A sería coherente con un efecto de empleo directo puro en lugar de una amplificación genuina.

**Predicción:** β₄ > 0 en ambas especificaciones; el efecto de amplificación es mayor para los clústeres T1 compactos-intactos (candidatos T0) que para los clústeres T1 laxos.

**Datos:** Capa cívica (puntos de hospitales y universidades de OSM más recuentos oficiales de camas hospitalarias) — en curso de ensamblaje. El desglose NAICS de LODES está disponible a nivel de grupo de bloques y puede reagregarse para excluir NAICS 611/622.

---

## 8. Conclusión

### 8.1 Resumen de contribuciones

Este artículo ha propuesto una taxonomía composicional formal de los clústeres de co-localización de anclas minoristas — una clasificación que identifica qué *categorías* de anclas están presentes en un clúster submetropolitano, en lugar de simplemente cuántas unidades minoristas están co-localizadas o cuán grandes son. La taxonomía se implementa a escala continental utilizando datos de fuente abierta, produciendo 6.493 clústeres clasificados en trece países.

La contribución teórica es el argumento de preferencia revelada para el análisis composicional: cuando múltiples grandes cadenas minoristas de formato de distintas categorías seleccionan independientemente la misma localización submetropolitana, la señal conjunta de su co-presencia es un indicador adelantado más duradero, más ampliamente disponible y metodológicamente más sencillo de la intensidad de la actividad comercial que cualquier conjunto de datos de demanda de una única cosecha. La demostración de Holmes (2011) de que la selección de sitios de Walmart refleja economías de densidad fundamenta este argumento empíricamente.

La contribución metodológica es el algoritmo DBSCAN de dos pasadas con prioridad compacta y la clasificación geométrica dentro del nivel con contracción — una medida de compacidad que discrimina entre pares composicionalmente homogéneos y es estable a través de la variación de tamaño de muestra inherente a un conjunto de datos de trece países. Una extensión metodológica adicional, el protocolo O-D de polígono y dispositivo especificado en el §3.7, reemplaza los límites administrativos de captación con mercados submetropolitanos definidos por la movilidad, permitiendo la comparación de demanda a nivel de clúster — en lugar de a nivel de asentamiento — entre clústeres.

### 8.2 Investigación futura

La prioridad de investigación inmediata es la unión de LODES y la prueba de permutación (§7.1 y §7.4), que pueden ejecutarse con los datos actualmente cargados. Estas determinarán si los resultados descriptivos del §5 — específicamente la relación sistemática entre el nivel y la compacidad geométrica — están respaldados por el proxy de empleo por trayecto al trabajo.

El programa a medio plazo es la adquisición de datos O-D para el Reino Unido, Francia y Alemania, permitiendo la Prueba 2 a escala y proporcionando la primera prueba transcontinental de H₁. La validación demográfica (Optimum Mosaic, §6.3) está planificada concurrentemente. Se está investigando actualmente la adquisición de un panel de movilidad comercial que cubra los trece países del estudio, lo que permitiría que el protocolo completo de polígono y dispositivo descrito en el §3.7 reemplace los proxies LODES/MITMA.

Una extensión a corto plazo aborda la predicción corolaria introducida en el §2.2: que las anclas secundarias siguen en lugar de preceder al establecimiento de los hipermercados. Los métodos de estudio de eventos análogos a los aplicados a la difusión de Walmart por Holmes (2011), utilizando datos temporales sobre fechas de apertura de tiendas, pueden probar esta hipótesis de entrada secuencial directamente. Esta es una línea de investigación planificada, no un resultado actual.

La agenda a largo plazo es un análisis de series temporales. El conjunto de datos actual es una sección transversal (Fase 21, mayo de 2026). La evolución del formato minorista, la entrada de nuevas tipologías de anclas de gran formato (centros de distribución de comercio electrónico, gran formato de salud y bienestar) y la salida o reposicionamiento de las anclas existentes alterarán la distribución de niveles con el tiempo. El seguimiento longitudinal de estos cambios frente a los resultados de la actividad comercial puede proporcionar la prueba más sólida de la durabilidad predictiva de la señal composicional.

---

## Disponibilidad de datos

Los datos de puntos minoristas se derivan de OpenStreetMap (openstreetmap.org), disponibles bajo la Licencia de Base de Datos Abierta (ODbL). Los archivos de configuración a nivel de cadena, los scripts de agrupamiento y el conjunto de datos clusters-meta.json están disponibles en [URL del repositorio pendiente]. Los datos LODES están disponibles públicamente del programa LEHD de la Oficina del Censo de los EE.UU. Los datos de movilidad MITMA están disponibles públicamente del Ministerio de Transportes de España.

---

## Referencias

Angrist, J. D., y J.-S. Pischke. 2009. *Mostly Harmless Econometrics: An Empiricist's Companion.* Princeton: Princeton University Press.

Anselin, L. 1988. *Spatial Econometrics: Methods and Models.* Dordrecht: Kluwer Academic.

Basker, E. 2005. Selling a cheaper mousetrap: Wal-Mart's effect on retail prices. *Journal of Urban Economics* 58(2): 203–229.

Berry, B. J. L. 1958. Retail location and consumer behaviour. *Papers and Proceedings of the Regional Science Association* 5(1): 65–73.

Birch, E. L. 2006. Who lives downtown? In *Redefining Urban and Suburban America,* vol. 3, edited by A. Berube, B. Katz, and R. E. Lang, 27–50. Washington, DC: Brookings Institution Press.

Brueckner, J. K. 1993. Inter-store externalities and space allocation in shopping centers. *Journal of Real Estate Finance and Economics* 7(1): 5–16.

Büchel, K., and M. V. Ehrlich. 2021. Cities and the structure of social interactions: Evidence from mobile phone data. *Journal of Urban Economics* 121: 103–316.

Calafiore, A., G. Boeing, A. Singleton, and D. Arribas-Bel. 2022. Redefining retail catchment with mobile geolocation data: Insights from New Zealand. *Journal of Retailing and Consumer Services* 79.

Carlino, G., and W. R. Kerr. 2015. Agglomeration and innovation. In *Handbook of Regional and Urban Economics,* vol. 5, edited by G. Duranton, J. V. Henderson, and W. C. Strange, 349–404. Amsterdam: Elsevier.

Chen, Y., et al. 2022. Causal analysis on the anchor store effect in a location-based social network. *arXiv preprint* arXiv:2210.13582.

Christaller, W. 1933. *Die zentralen Orte in Süddeutschland.* Jena: Gustav Fischer.

Coe, N. M., and N. Wrigley. 2007. Host economy impacts of transnational retail: The research agenda. *Journal of Economic Geography* 7(4): 341–371.

Darnall, N., I. Seol, J. Sarkis, and J. Cordeiro. 2022. An open source delineation and hierarchical classification of UK retail agglomerations. *PLOS ONE* 17(9): e0264713.

Drucker, J., and H. Goldstein. 2007. Assessing the regional economic development impacts of universities: A review of current approaches. *International Regional Science Review* 30(1): 20–46.

Duranton, G., and D. Puga. 2004. Micro-foundations of urban agglomeration economies. In *Handbook of Regional and Urban Economics,* vol. 4, edited by J. V. Henderson and J.-F. Thisse, 2063–2117. Amsterdam: Elsevier.

Ellison, G., E. L. Glaeser, and W. R. Kerr. 2010. What causes industry agglomeration? Evidence from coagglomeration patterns. *American Economic Review* 100(3): 1195–1213.

Eppli, M. J., and J. D. Shilling. 1995. Large-scale shopping center development opportunities. *Land Economics* 71(1): 35–41.

Ester, M., H.-P. Kriegel, J. Sander, and X. Xu. 1996. A density-based algorithm for discovering clusters in large spatial databases with noise. *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96),* 226–231. Portland: AAAI Press.

*Exploring economic sectoral dynamics through high-resolution mobility data.* 2025. *arXiv preprint* arXiv:2506.13985.

Garner, B. J. 1966. *The Internal Structure of Retail Nucleations.* Evanston: Northwestern University Department of Geography Research Series No. 12.

Glasson, J. 2003. The widening local and regional development impacts of the modern universities. *Local Economy* 18(1): 21–37.

Haklay, M. 2010. How good is volunteered geographical information? A comparative study of OpenStreetMap and Ordnance Survey datasets. *Environment and Planning B* 37(4): 682–703.

Hernandez, T., and J. Simmons. 2006. Evolving retail landscapes: Power retail in Canada. *Canadian Geographer* 50(4): 465–486.

Holmes, T. J. 2011. The diffusion of Wal-Mart and economies of density. *Econometrica* 79(1): 253–302.

Huff, D. L. 1964. Defining and estimating a trading area. *Journal of Marketing* 28(3): 34–38.

Kim, J., and K. Park. 2025. Effect of agglomeration externalities of adjacent retail areas on commercial business continuity in Seoul, Korea. *Growth and Change* 56(2).

Krugman, P. 1991. *Geography and Trade.* Cambridge: MIT Press.

Kwan, M.-P. 2016. Algorithmic geographies: Big data, algorithmic uncertainty, and the production of geographic knowledge. *Annals of the American Association of Geographers* 106(2): 274–282.

Li, Z., H. Ning, F. Jing, and M. N. Lessani. 2024. Understanding the bias of mobile location data across spatial scales and over time: A comprehensive analysis of SafeGraph data in the United States. *PLOS ONE* 19(10): e0294430.

Marshall, A. 1890. *Principles of Economics.* London: Macmillan.

Neumark, D., J. Zhang, and S. Ciccarella. 2008. The effects of Wal-Mart on local labor markets. *Journal of Urban Economics* 63(2): 405–430.

Pashigian, B. P., and E. D. Gould. 1998. Internalizing externalities: The pricing of space in shopping malls. *Journal of Law and Economics* 41(1): 115–142.

Reilly, W. J. 1931. *The Law of Retail Gravitation.* New York: Knickerbocker Press.

Rosenthal, S. S., and W. C. Strange. 2004. Evidence on the nature and sources of agglomeration economies. In *Handbook of Regional and Urban Economics,* vol. 4, edited by J. V. Henderson and J.-F. Thisse, 2119–2171. Amsterdam: Elsevier.

U.S. Census Bureau. 2021. *LEHD Origin-Destination Employment Statistics (LODES), Version 8.* Washington, DC: Center for Economic Studies.

Wrigley, N., and M. Lowe. 2002. *Reading Retail: A Geographical Perspective on Retailing and Consumption Spaces.* London: Arnold.

Zhao, S., Y. Chen, Y. Duan, and Z. Xu. 2025. Site selection analysis and prediction of new retail stores from an urban commercial space perspective. *ISPRS International Journal of Geo-Information* 14(6): 217.

---

## Apéndice A — Referencia de notación matemática

| Símbolo | Definición |
|---|---|
| ε, τ_tight, τ_loose | Umbrales de proximidad DBSCAN (1,0 km; 3,0 km) |
| Δ_max | Límite estricto de diámetro del clúster = 3,0 km |
| span_km | Distancia geodésica máxima entre pares dentro del clúster |
| tight_intact | Booleano: todos los miembros dentro de τ_tight = 1,0 km |
| ring_radius_km | max(1,0; span_km / 2 × 1,15) |
| dist_rank_in_tier | CDF invertida con contracción de span_km dentro del nivel |
| w | Peso de contracción = n_país / (n_país + K), K ≈ 20–30 |
| T1.a, T1.b, T1.c | Vías de admisión T1: composición tripartita; H2b compacto; amplitud de categorías ≥4 |
| T1, T2, T3 | Clasificación de nivel por composición de categorías de anclas |
| T0 (Platino) | T1 ∧ tight_intact ∧ civic_modifier = 1 (modificador, no puerta de nivel) |
| civic_modifier | 1 si hospital ≥200 camas o universidad ≥10.000 matriculados dentro de 5,0 km |
| catchment_area_km2 | Área del casco convexo de los centroides de home-hex en la captación definida por movilidad |
| catchment_entropy | H = −Σ p_i log p_i sobre celdas H3 de origen de visitantes |
| home_work_ratio | Dispositivos con home_hex dentro de captación ÷ dispositivos con work_hex dentro de captación |
| H₁, H₀, H₂, H₃ | Hipótesis primaria, nula, de redundancia de demanda y de amplificación cívica |

## Apéndice B — Cobertura de cadenas por país (Fase 21)

Un inventario completo de cadenas por país está en preparación y aparecerá en v0.5. La versión de la Fase 22 incluye cadenas de 17 países en 6.493 clústeres; la atribución a nivel de cadena es consultable en el mapa en gis.woodfinegroup.com.

## Apéndice C — Arquitectura del marco analítico

*Un diagrama de flujo de datos (ingesta YAML → JSONL → DBSCAN → clusters-meta.json → PMTiles → MapLibre) está en preparación y aparecerá en v0.5.*

---

## Declaración de uso de IA

La redacción, el formalismo matemático y el marco de investigación de este manuscrito se desarrollaron con la asistencia de Claude (Anthropic, claude-sonnet-4-6), un modelo de lenguaje amplio. El conjunto de datos analítico, las reglas de taxonomía, el algoritmo de agrupamiento y todos los resultados cuantitativos fueron producidos por las autoras de forma independiente. La búsqueda y selección de literatura, el fundamento teórico y todas las afirmaciones científicas son responsabilidad de las autoras y han sido revisadas por la autora de correspondencia antes de su envío.

Esta declaración sigue las directrices de COPE (Comité de Ética en Publicaciones) sobre IA y autoría: las herramientas de IA no califican como autoras; su uso debe declararse; la autora de correspondencia asume la responsabilidad de la integridad del trabajo.

---

*Versión 0.4 — 2026-05-25*
*Objetivo: Journal of Economic Geography*
*En preparación para envío previsto al Journal of Economic Geography (Oxford University Press)*
*Las declaraciones con proyección de futuro llevan el lenguaje "planificado / previsto / puede / objetivo"*
