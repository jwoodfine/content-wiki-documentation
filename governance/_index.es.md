---
schema: foundry-doc-v1
content_type: topic
title: "Gobernanza y Estándares"
slug: governance-index
short_description: "Registros formales de decisiones, postura de licenciamiento, modelo de contribuidor y requisitos de cumplimiento que rigen cómo se construye, licencia y modifica la plataforma PointSav — incluyendo las doce decisiones arquitectónicas vinculantes, la postura de divulgación continua BCSC y la matriz de licencias."
lang: es
paired_with: _index.md
category: governance
index_type: thematic
index_scope: governance
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
---

Esta categoría cubre los registros de decisiones formales, la postura de licencias, el modelo de colaboración y los requisitos de cumplimiento que rigen cómo se construye, licencia y modifica la plataforma PointSav a lo largo del tiempo. Los artículos de gobernanza son el registro escrito de decisiones tomadas y su justificación; no son declaraciones de intención.

Las doce [[architecture-decisions|decisiones de arquitectura vinculantes]] son las entradas más importantes de esta categoría para la diligencia debida técnica y la revisión regulatoria: definen dónde se detiene el procesamiento automatizado y dónde comienza la autoridad humana, cómo se separan los datos y dónde deben residir las claves criptográficas. La postura de divulgación continua de la BCSC documenta los requisitos de la normativa canadiense de valores tal como se aplican a la plataforma y su documentación pública.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí** para la evaluación de adquisición, seguridad y cumplimiento: [[procurement-overview]] — lo que adquiere un comprador regulado, y las propiedades de cumplimiento aplicadas por arquitectura en lugar de por promesa contractual.

<!-- END-START-HERE-HIGHLIGHT -->

## Debida diligencia institucional

Punto de entrada para la evaluación de adquisición, seguridad y cumplimiento.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: institutional-due-diligence -->
- [[procurement-overview]] — Lo que un comprador regulado adquiere al implementar PointSav: hardware que el cliente posee íntegramente, datos que el proveedor nunca posee, sin compromiso de gasto mínimo, y propiedades de cumplimiento ejecutadas por arquitectura en lugar de promesas contractuales.
- [[security-overview]] — La postura de seguridad de la plataforma: aislamiento de hardware basado en capacidades, el estándar unidireccional Diode de flujo de comandos, el límite de inteligencia artificial Doorman, el registro de auditoría WORM, y cómo cada propiedad se ejecuta por arquitectura en lugar de controles de política que pueden configurarse incorrectamente.
- [[compliance-and-continuous-disclosure]] — Cumplimiento y divulgación continua describe los marcos regulatorios que aborda la arquitectura PointSav y el enfoque estructural que adopta para exponer evidencia de auditoría de forma continua, en lugar de mediante ciclos anuales de certificación puntual.
<!-- END AUTO-GENERATED -->

## Registros de decisiones formales

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: formal-decision-records -->
- [[architecture-decisions]] — Doce decisiones de arquitectura vinculantes — compromisos registrados que gobiernan la construcción de la plataforma PointSav y restringen toda la ingeniería futura en el manejo de datos, la supervisión humana, la separación de sistemas y la custodia del despliegue.
- [[adr-07-zero-ai-in-ring-1]] — SYS-ADR-07 prohíbe la inferencia de IA en todos los servicios de ingestión del Ring 1, garantizando operaciones exclusivamente deterministas en la ruta de escritura WORM para asegurar auditabilidad y composabilidad.
<!-- END AUTO-GENERATED -->

## Licencias y contribución

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: licensing-and-contribution -->
- [[contributor-model]] — El Modelo de Contribuidor de Tres Capas organiza los contribuidores del sustrato PointSav en Core (4–7 ingenieros asalariados), Paid (50–100 contribuidores de proyectos contratados) y Open (10.000 o más participantes públicos), con trayectorias explícitas de movilidad entre capas.
- [[canadian-simple-copyright]] — La propiedad intelectual de la plataforma se concentra en una única sociedad holding matriz canadiense por operación del artículo 13(3) de la Ley de Derechos de Autor canadiense, sin cesión entre empresas, y está diseñada para evolucionar de forma incremental a medida que madura la estructura corporativa.
- [[legal-and-ip-structure]] — La topología de tres corporaciones que rige la transferencia de propiedad intelectual de contribuidores a proveedor a cliente, con squash-and-merge como el evento de transferencia de propiedad intelectual atómico y separación estricta que impide exposición de código no auditado o registros operacionales.
<!-- END AUTO-GENERATED -->

## Soberanía de ingeniería

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: engineering-sovereignty -->
- [[sovereign-replacement-initiative]] — La Iniciativa de Reemplazo Soberano es el programa de gobernanza de ingeniería que rastrea dependencias de terceros, las aísla en directorios de componentes en cuarentena, y coordina los programas moonshot activos que construyen reemplazos nativos.
- [[moonshot-initiatives]] — Las iniciativas moonshot son programas de ingeniería activos que construyen reemplazos nativos para dependencias de terceros en cuarentena, con el objetivo de eliminar el bloqueo de proveedor y reducir la superficie de ataque externa de la plataforma a lo largo del tiempo.
- [[sovereign-airlock-doctrine]] — La exclusa soberana es el protocolo de commits por etapas que impone una separación estricta entre las identidades de staging que escriben trabajo y las identidades de repositorio canónico que lo publican — dos autores de staging para todos los commits, dos identidades de administrador para los pushes canónicos, sin ruta directa entre ellos.
<!-- END AUTO-GENERATED -->

## Disciplinas de plataforma

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-disciplines -->
- [[ontological-governance]] — Cuatro libros contables de vocabulario de referencia mantenidos deliberadamente acotados, más un bucle de verificación humana que revisa los fragmentos de identidad extraídos antes de comprometerlos al libro contable verificado.
- [[anti-homogenization-discipline]] — La disciplina anti-homogenización es la postura arquitectónica que resiste que los asistentes de escritura con IA empujen a los colaboradores hacia una voz única, marcando posibles problemas por defecto en lugar de reescribir el texto silenciosamente.
- [[api-key-boundary-discipline]] — La regla que establece que todas las credenciales externas de LLM pertenecen exclusivamente al servicio de pasarela y nunca a los motores de inferencia.
- [[favicon-matrix]] — El wiki sirve un único favicon SVG estático — un glifo de documento azul marino, enlazado desde un archivo estático, la misma marca en cada pestaña sin importar el inquilino.
- [[doctrine-invention-7-rekor-anchoring]] — Cómo el binario emisor-de-ancla de Foundry publica un punto de control firmado en Sigstore Rekor cada mes, proporcionando evidencia independiente y verificable del estado del espacio de trabajo.
<!-- END AUTO-GENERATED -->

## Véase también

- [Inicio del wiki](/)
- [Cómo Está Construido](/architecture/)
- [Dónde Se Ejecuta](/infrastructure/)
- [Referencia](/reference/)
