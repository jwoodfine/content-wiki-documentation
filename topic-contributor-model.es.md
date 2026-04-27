# El modelo de contribuyentes en tres niveles (resumen)

El sustrato de Foundry es demasiado amplio para que un solo
equipo lo mantenga, y demasiado valioso para atarlo a la
cadencia de lanzamiento de un solo equipo. El modelo de
contribuyentes que se sigue de esta restricción produce
operativamente tres niveles distintos — Núcleo, Pagado y
Abierto — con caminos de movilidad explícitos entre ellos.

## Los tres niveles

| Nivel | Tamaño objetivo | Financiamiento | Rol |
|---|---|---|---|
| **Núcleo** | 4-7 | Empleados de PointSav; salario; participación accionaria | Administración cotidiana del sustrato |
| **Pagado** | 50-100 | Contratos financiados por PointSav; entregables por resultado | Trabajo de ingeniería a nivel de proyecto vía PRs en GitHub |
| **Abierto** | 10.000+ | Ninguno — contribuciones bajo Apache 2.0 / MIT / CC BY 4.0 | Contribuciones al sustrato público; sin CLA requerido |

### Núcleo

Posee documentos del *workspace*, enmiendas a la doctrina,
convenciones y el registro de citaciones. Las decisiones
arquitectónicas fluyen por este nivel. Pequeño por diseño;
tres primitivas arquitectónicas lo mantienen tratable: el
sustrato es lo bastante auto-suficiente operativamente, el
sustrato de trayectoria lo hace auto-documentado, y el álgebra
de composición de adaptadores hace la personalidad operativa
componible en vez de dependiente de la persona.

### Pagado

50-100 es la banda donde la reputación de cada contribuyente
puede rastrearse mediante la atribución del sustrato de
trayectoria, los contratos por entregable son tratables
operativamente sin burocracia de aprovisionamiento empresarial,
y los ingresos por servicios de agregación multi-inquilino
pueden sostener la nómina sin capital de escala VC.

### Abierto

**Sin CLA requerido** para contribuciones al núcleo abierto,
según las mejores prácticas del manual *open-core* de 2026.
El 10.000+ es plausible: el kernel de Linux sostiene
aproximadamente 14.000 contribuyentes por año; la Apache
Foundation supera decenas de miles; Kubernetes lleva más de
4.000 en un solo proyecto; PostgreSQL opera con aproximadamente
700 contribuyentes centrales más muchos ocasionales.

## Movilidad entre niveles

El modelo no es de castas. **Abierto → Pagado**: un
contribuyente cuyo trabajo recurrente muestra calidad operativa
recibe contratos pagos; la reputación deriva de la atribución
del sustrato de trayectoria. **Pagado → Núcleo**: raro; requiere
alineación con la administración del sustrato a largo plazo y
confianza operativa a nivel sénior. **Cualquiera puede
bifurcar**: la propiedad *Designed-for-Breakout* aplica al
nivel de contribuyente — un contribuyente puede llevarse su
trabajo, sus adaptadores, sus datos de inquilino y operar
independientemente.

## Por qué la matemática funciona

Cálculo ingenuo: 4-7 empleados + 50-100 contratistas + 10.000+
contribuyentes abiertos producen un sustrato con el alcance de
un equipo de plataforma a escala de hiperescalador
(~1.000+) a aproximadamente el 5% del costo de nómina.

Es la ventaja estructural. Tres primitivas la hacen real: la
atribución criptográfica de la reputación de contribuyente, el
álgebra de composición de adaptadores que permite enviar
adaptadores sin poseer todo el sustrato, y la propiedad
*Designed-for-Breakout* que mantiene voluntaria la relación.

## Qué no es este modelo

No es jerarquía de dignidad. El nivel Abierto no es "inferior"
al Núcleo; tiene alcance distinto. No reemplaza la
gobernanza; el proceso de Convención Constitucional es la
sede de los desacuerdos a nivel de sustrato. No es modelo
laboral de escala VC; el nivel Pagado se sostiene de ingresos
de agregación multi-inquilino sin capital de escala VC.

## Véase también

- [Documento canónico en inglés](topic-contributor-model.md)
- [El sustrato compuesto](topic-compounding-substrate.md)
- [El sustrato de aprendizaje](topic-apprenticeship-substrate.md)
- [Hospedaje por el cliente](topic-customer-hostability.md)
- [Postura de derechos de autor canadiense-simple](topic-canadian-simple-copyright.md)
