---
schema: foundry-doc-v1
title: "El sustrato de aprendizaje"
slug: apprenticeship-substrate.es
lang: es
paired_with: apprenticeship-substrate.md
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "El mecanismo de plataforma que enruta el trabajo de código y editorial primero a través de un modelo de lenguaje pequeño local, captura un veredicto sénior firmado para cada intento, y usa los pares de preferencia resultantes como señal de preentrenamiento continuo."
status: active
bcsc_class: public-disclosure-safe
forward_looking: true
last_edited: 2026-05-22
editor: pointsav-engineering
cites:
 - ni-51-102
---

Cuando un ingeniero sénior revisa el trabajo de un júnior, la corrección es el artefacto más valioso de la sala — y casi toda organización lo descarta. El razonamiento detrás de un arreglo se dice una vez, se aplica una vez y nunca se captura. El siguiente júnior, y el siguiente modelo, empiezan desde cero.

El sustrato de aprendizaje lo captura. <!--claim id=route-and-capture confidence=structural cites=[]-->Cada tarea de código y editorial se enruta primero a través de un [[service-slm|modelo de lenguaje pequeño local]]; un revisor sénior firma luego un veredicto sobre el intento. El desacuerdo firmado entre el intento del aprendiz y el veredicto del sénior se convierte en datos de pares de preferencia.<!--/claim-->

<!--claim id=three-stage-routing confidence=structural cites=[]-->El enrutamiento opera en tres etapas por tipo de tarea — `review`, `spot-check` y `autonomous` — con umbrales de promoción precisos. Un tipo de tarea graduado elimina los tokens de autoría sénior en esa clase de trabajo, y el enrutamiento en sombra recoge datos de entrenamiento de cada otro commit de código en la flota.<!--/claim-->

Para un comprador regulado la consecuencia es concreta. La IA mejora sobre el trabajo de la propia organización, y ese trabajo nunca sale del despliegue. Por el lenguaje de [[disclosure-substrate|divulgación continua]] de `[ni-51-102]`, la trayectoria hacia la eliminación de tokens en tipos de tarea graduados es prospectiva; la estructura de enrutamiento está operativa hoy.

## Descripción general

La observación capturada entrena al modelo sobre lo que escribió el sénior. La interacción capturada — intento del aprendiz más veredicto sénior firmado — entrena con un orden de magnitud más eficiencia por tupla. Los datos de preferencia firmados son la entrada de entrenamiento más valiosa, un hallazgo establecido en la literatura de aprendizaje por retroalimentación de 2024-2026.

Este patrón de enrutamiento produce esas tuplas de interacción sobre trabajo de producción real, no sobre benchmarks sintéticos. Cada sesión ejercita al aprendiz; cada veredicto firmado es una tupla de entrenamiento; cada tipo de tarea graduado elimina tokens externos de forma monótona.

## Anillo y función

El sustrato de aprendizaje abarca el Anillo 3 — Inteligencia Opcional — y la infraestructura del corpus de entrenamiento. [[service-slm]], el [[compounding-doorman|Doorman]], es el servicio del Anillo 3 que ejecuta el enrutamiento del aprendiz. El libro de promoción y los scripts de captura del corpus viven dentro del propio despliegue del [[totebox-archive|cliente]].

## Las tres etapas

El enrutamiento opera por tipo de tarea. La promoción es automática al cruzar el umbral; la degradación es automática ante cualquier reversión post-commit rastreada a un diff del aprendiz.

| Etapa | Enrutamiento | Revisión sénior |
|---|---|---|
| `review` | El aprendiz intenta; el sénior revisa cada diff antes del commit | Cada diff |
| `spot-check` | El aprendiz commitea; el sénior revisa una muestra 1-en-N y anomalías auto-marcadas | Muestreado y marcado |
| `autonomous` | El aprendiz commitea autónomamente; auditoría mensual por lotes | Auditoría por lotes |

<!--claim id=promotion-thresholds confidence=structural cites=[]-->La promoción de `review` a `spot-check` exige al menos 50 veredictos con una tasa de aceptación de 0,85 sobre los 50 más recientes. La promoción a `autonomous` exige al menos 100 veredictos con una tasa de 0,95 sobre los 100 más recientes, con cero reversiones post-commit rastreadas a diffs del aprendiz.<!--/claim--> Una sola reversión rastreada a un diff del aprendiz degrada el tipo de tarea una etapa. Los tipos nuevos empiezan en `review`.

## Brief, intento, veredicto

El sénior que escribiría un diff emite en su lugar un **brief**. El brief declara qué se está haciendo, los invariantes que el diff debe preservar, las restricciones citadas y la prueba de aceptación que el aprendiz debe hacer pasar.

El aprendiz responde con un **intento**: razonamiento que cita los invariantes del brief, una confianza propia calibrada contra su registro previo en este tipo de tarea, y un diff unificado. Si la confianza cae por debajo de 0,5, el aprendiz escala sin diff.

El sénior lee el intento y firma un **veredicto**: `accept`, `refine`, `reject` o `defer-tier-c`. <!--claim id=verdict-signature confidence=structural cites=[]-->Los veredictos `refine` y `reject` llevan una nota de una oración — los datos de entrenamiento de mayor señal que produce el corpus. La firma usa `ssh-keygen -Y sign` con una etiqueta de espacio de nombres que la vincula a este protocolo, de modo que una firma de commit no puede reutilizarse como veredicto.<!--/claim-->

## Enrutamiento de producción y enrutamiento en sombra

Dos rutas corren en paralelo.

<!--claim id=production-routing confidence=structural cites=[]-->El enrutamiento de producción opera sobre tipos de tarea graduados: el sénior emite un brief antes de escribir un diff, el intento del aprendiz es el diff candidato, y en `accept` ese diff se incluye en el commit. Esto elimina los tokens de autoría sénior en los tipos graduados.<!--/claim-->

<!--claim id=shadow-routing confidence=structural cites=[]-->El enrutamiento en sombra opera sobre cada otro commit de código en cada cluster activo. Después de que el diff se escribe de la forma habitual, la sesión envía un brief al aprendiz; la triple (brief, intento, diff-real) se captura al corpus sin veredicto y sin firma.<!--/claim-->

La producción elimina tokens en los tipos graduados. La sombra genera los datos que gradúan el siguiente tipo. Las dos rutas se componen.

## Tubería de captura

El corpus de aprendizaje es un cuarto corpus junto a los corpus constitucional, de ingeniería y de runtime de inquilino. La partición por inquilino vive a nivel de directorio:

```
data/training-corpus/apprenticeship/<task-type>/<tenant>/<ulid>.jsonl
```

Un archivo contiene una triple (brief, intento, veredicto). <!--claim id=tenant-private-corpus confidence=structural cites=[]-->Los registros privados del inquilino nunca salen de su infraestructura.<!--/claim--> Un veredicto `refine` o `reject` produce además una triple de Optimización Directa de Preferencias — intento rechazado, diff corregido, etiqueta de violación de restricción — que alimenta el entrenamiento de adaptadores.

## Configuración

El primer tipo de tarea registrado es `version-bump-manifest`. Cada incremento MINOR y PATCH de la plataforma toca `MANIFEST.md` y `CHANGELOG.md`: trabajo bien formado, sin juicio arquitectónico, fácilmente verificable. El aprendiz gradúa este tipo primero; los tokens sénior bajan en esa clase de trabajo; el siguiente tipo se registra.

<!--claim id=four-conditions confidence=structural cites=[]-->Cuatro condiciones hacen funcionar el sustrato, y las cuatro son propiedades estructurales de un [[customer-hostability|despliegue propiedad del cliente]]: una carta de gobernanza por cliente, identidades de firma por cliente, granularidad por tipo de tarea en el libro de promoción, y preentrenamiento continuo por cliente.<!--/claim--> Una plataforma de IA gestionada en la nube carece de las cuatro — entrenar sobre datos de interacción del cliente exige agruparlos, lo que elimina la garantía de aislamiento por cliente.

Por `[ni-51-102]`, la trayectoria hacia la eliminación de tokens es prospectiva; la forma del enrutamiento está establecida hoy.

## Véase también

- [[compounding-substrate]]
- [[contributor-model]]
- [[language-protocol-substrate]]
- [[trajectory-substrate]]
- [[customer-hostability]]
