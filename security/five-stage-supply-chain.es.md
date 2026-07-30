---
schema: foundry-doc-v1
title: "Cadena de suministro soberana de cinco etapas"
slug: five-stage-supply-chain
category: security
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-30
editor: pointsav-engineering
paired_with: five-stage-supply-chain.md
short_description: "Recorrido del código del entorno del contribuyente a producción en cinco etapas, con brecha de aire de doble ciego que aparta credenciales y datos de producción del contribuyente."
cites: []
references:
  - id: 1
    text: "OpenSSF. 'Supply Chain Levels for Software Artifacts (SLSA) v1.0.' Open Source Security Foundation, 2023."
    url: "https://slsa.dev/spec/v1.0/"
  - id: 2
    text: "Hammant, P. 'Trunk Based Development.' trunkbaseddevelopment.com, 2017."
    url: "https://trunkbaseddevelopment.com/"
---

**Corrección — Etapas 2/3 reformuladas como planificadas/previstas (2026-07-30):**
este artículo describía un modelo de bifurcación de GitHub → pull request →
squash-and-merge en tiempo presente sin matices. El mecanismo real actual de
commit/promoción funciona de otra manera: `commit-as-next.sh` confirma directamente en
la rama de trabajo con identidad de autor alternante, y `promote.sh` aplica cherry-pick
de los commits directamente sobre la rama canónica — confirmado leyendo ambos scripts,
y reconfirmado por una búsqueda más amplia en ~25 archivos (cero coincidencias de
`octokit`/`gh pr create`/`gh pr merge` en ningún lugar). El concepto de brecha de aire
de doble ciego y la topología de tres organizaciones siguen siendo descripciones
estructurales precisas y se dejan en tiempo presente a continuación — solo la mecánica
específica de PR/squash-merge de las Etapas 2/3 se reformula como planificada/prevista,
ya que el mecanismo real logra un efecto similar mediante commit-directo-y-cherry-pick.

El código se mueve desde el entorno local de un contribuyente hasta una implementación de producción a través de cinco etapas distintas — cada una con un actor definido, una acción específica y un equivalente estándar de la industria. El arreglo es deliberadamente circular: cada sesión de trabajo comienza restableciendo al estado del proveedor verificado más reciente, eliminando la deriva lógica que se acumula cuando los contribuyentes construyen sobre sus propias ramas desactualizadas. Una única puerta de gobernanza — el squash-and-merge del administrador — es donde se transfiere la propiedad intelectual y los commits experimentales se colapsan en un único registro corporativo. [^1] Este artículo cubre las cinco etapas, la brecha de aire de doble ciego y la topología del repositorio.

## Las cinco etapas

| Etapa | Actor | Acción | Equivalente en la industria |
|---|---|---|---|
| 1 — Respaldo | Contribuyente | `git push` a su bifurcación personal de GitHub | Respaldo remoto / push de rama de características |
| 2 — Oferta *(mecánica planificada)* | Contribuyente → Proveedor | Hoy: commit directo vía `commit-as-next.sh`. Diseño previsto: abrir pull request en `pointsav/<repo>` | Envío de revisión de código |
| 3 — Auditoría | Proveedor (`ps-administrator`) | Hoy: `promote.sh` aplica cherry-pick del commit sobre la rama canónica. Diseño previsto: squash-and-merge en el libro mayor del proveedor | Commit atómico / creación del maestro dorado |
| 4 — Transferencia | Proveedor → Cliente | Push espejo del tag de lanzamiento verificado | Propagación de lanzamiento |
| 5 — Implementación | Cliente → Producción | `git pull --ff-only` en hosts de producción | Implementación de imagen dorada |
| (Bucle) — Reinicio | Proveedor → Contribuyente | `git fetch upstream && git rebase` | Sincronización basada en trunk |

## Lo que logra cada etapa

**Etapa 1 — Respaldo.** El contribuyente envía el trabajo en progreso a su propia bifurcación de GitHub (`jwoodfine/...` o `pwoodfine/...`). La bifurcación es la red de seguridad privada del contribuyente. Nada en el libro mayor corporativo se ve aún afectado.

**Etapa 2 — Oferta.** Hoy, el trabajo confirmado del contribuyente se vuelve visible para el administrador directamente a través del commit de `commit-as-next.sh` — no hay paso de pull request ni puerta de revisión en las herramientas actuales. El diseño previsto exige que el contribuyente abra un pull request desde su bifurcación hacia la organización del proveedor; esto aún no es como funciona el mecanismo.

**Etapa 3 — Auditoría.** Hoy, `promote.sh` aplica cherry-pick del commit verificado directamente sobre la rama canónica y hace push — este es el mecanismo real que transfiere una contribución al libro mayor del proveedor. El diseño previsto describe esto en cambio como un squash-and-merge realizado por el administrador; esa mecánica específica no es la que se ejecuta hoy, aunque el efecto — la propiedad transfiriéndose a [[pointsav-overview|PointSav Digital Systems]] mediante un único commit canónico — se logra de cualquier manera.

**Etapa 4 — Transferencia.** La administración del proveedor refleja el tag de lanzamiento verificado desde `pointsav/<repo>` a `woodfine/<repo>`. El cliente recibe solo tags firmados y nunca ve commits de contribuyentes en vuelo. Este es el paso de propagación de lanzamiento que aísla al cliente del riesgo ascendente.

**Etapa 5 — Implementación.** El cliente extrae el tag verificado en sus hosts de producción. La restricción `--ff-only` garantiza que la producción no pueda acumular conflictos de fusión — debe reflejar exactamente el libro mayor de GitHub del cliente. Si una implementación falla, el fallo se manifiesta inmediatamente en lugar de divergir silenciosamente.

**El Bucle — Reinicio.** El contribuyente obtiene el estado verificado del proveedor en su entorno local y reorganiza su próximo trabajo sobre él. Cada sesión de trabajo comienza desde el mismo punto que todos los demás contribuyentes. [^2]

## La brecha de aire de doble ciego

El ciclo tiene una regla estructural más allá de su mecánica: el contribuyente nunca envía a la organización del cliente, y el cliente nunca lee las bifurcaciones de los contribuyentes. El proveedor es la única entidad que ve ambos extremos. El contribuyente y el cliente son mutuamente invisibles entre sí a través de la cadena de suministro.

Esta es la brecha de aire que permite a los contratistas trabajar en sistemas de producción sin tocar credenciales de producción ni ver datos de producción.

## Topología del repositorio

La cadena de suministro opera en tres organizaciones de GitHub, cada una con un rol específico:

| Organización | Propósito | Quién escribe |
|---|---|---|
| `github.com/pointsav` | Proveedor — fuente de verdad | Solo `ps-administrator` (promueve/hace push); `jwoodfine`/`pwoodfine` (commit a espejos de staging) |
| `github.com/woodfine` | Cliente — libro mayor de producción | Solo `mcorp-administrator` |
| Cuentas personales de contribuyentes | Forja — sandbox | El contribuyente posee su bifurcación por completo |

Los repositorios canónicos a mediados de 2026 incluyen:

| Repositorio | Rol |
|---|---|
| `pointsav/pointsav-monorepo` | Todo el código `os-*`, `app-*`, `service-*`, `system-*` (véase [[os-family-overview|familia de SO]]) |
| `pointsav/content-wiki-documentation` | Wiki de documentación pública |
| `woodfine/woodfine-fleet-deployment` | Catálogo de implementación del cliente y artículos GUIDE |

## Por qué esta estructura escala

Un nuevo contribuyente no necesita aprender un nuevo protocolo. Hoy, eso significa: confirmar vía `commit-as-next.sh`, y las puertas de promoción — cherry-pick a canónico, el espejo del cliente, la implementación fast-forward, el reinicio basado en trunk — suceden por encima de ellos. La experiencia diaria del contribuyente es solo la Etapa 1.

La estructura escala a muchos contribuyentes sin perder la brecha de aire, porque la brecha de aire es impuesta por la puerta del administrador, no por reglas sociales.

## Véase también

- [[three-layer-architecture]] — las capas SOFTWARE / ESCAPARATE / INSTANCIAS que abarca la cadena de suministro
- [[six-tier-sovereignty-matrix]] — la taxonomía de directorios del monorepo del proveedor en la Etapa 1
- [[legal-and-ip-structure]] — la mecánica de transferencia de PI que implementa la Etapa 3
