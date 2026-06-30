---
schema: foundry-doc-v1
title: "La cadena de suministro soberana de cinco etapas"
slug: five-stage-supply-chain
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
paired_with: five-stage-supply-chain.md
short_description: "La cadena de suministro soberana de cinco etapas describe cómo el código se mueve desde el entorno local de un contribuyente hasta una implementación de producción a través de cinco etapas distintas, con una brecha de aire de doble ciego que permite a los contribuyentes trabajar en sistemas de producción sin tocar credenciales de producción ni ver datos de producción."
cites: []
references:
  - id: 1
    text: "OpenSSF. 'Supply Chain Levels for Software Artifacts (SLSA) v1.0.' Open Source Security Foundation, 2023."
    url: "https://slsa.dev/spec/v1.0/"
  - id: 2
    text: "Hammant, P. 'Trunk Based Development.' trunkbaseddevelopment.com, 2017."
    url: "https://trunkbaseddevelopment.com/"
---

El código se mueve desde el entorno local de un contribuyente hasta una implementación de producción a través de cinco etapas distintas — cada una con un actor definido, una acción específica y un equivalente estándar de la industria. El arreglo es deliberadamente circular: cada sesión de trabajo comienza restableciendo al estado del proveedor verificado más reciente, eliminando la deriva lógica que se acumula cuando los contribuyentes construyen sobre sus propias ramas desactualizadas. Una única puerta de gobernanza — el squash-and-merge del administrador — es donde se transfiere la propiedad intelectual y los commits experimentales se colapsan en un único registro corporativo. [^1] Este artículo cubre las cinco etapas, la brecha de aire de doble ciego y la topología del repositorio.

## Las cinco etapas

| Etapa | Actor | Acción | Equivalente en la industria |
|---|---|---|---|
| 1 — Respaldo | Contribuyente | `git push` a su bifurcación personal de GitHub | Respaldo remoto / push de rama de características |
| 2 — Oferta | Contribuyente → Proveedor | Abrir pull request en `pointsav/<repo>` | Envío de revisión de código |
| 3 — Auditoría | Proveedor (`ps-administrator`) | Squash-and-merge en el libro mayor del proveedor | Commit atómico / creación del maestro dorado |
| 4 — Transferencia | Proveedor → Cliente | Push espejo del tag de lanzamiento verificado | Propagación de lanzamiento |
| 5 — Implementación | Cliente → Producción | `git pull --ff-only` en hosts de producción | Implementación de imagen dorada |
| (Bucle) — Reinicio | Proveedor → Contribuyente | `git fetch upstream && git rebase` | Sincronización basada en trunk |

## Lo que logra cada etapa

**Etapa 1 — Respaldo.** El contribuyente envía el trabajo en progreso a su propia bifurcación de GitHub (`jwoodfine/...` o `pwoodfine/...`). La bifurcación es la red de seguridad privada del contribuyente. Nada en el libro mayor corporativo se ve aún afectado.

**Etapa 2 — Oferta.** El contribuyente abre un pull request desde su bifurcación hacia la organización del proveedor (`pointsav/...`). El trabajo se vuelve visible para el administrador. Pueden ejecutarse verificaciones automatizadas; comienza la revisión de código.

**Etapa 3 — Auditoría.** El administrador (`ps-administrator`) realiza un squash-and-merge. Este es el momento legalmente significativo: el historial de commits del contribuyente se colapsa en un único commit corporativo firmado con la clave SSH del administrador. La propiedad se transfiere a [[pointsav-overview|PointSav Digital Systems]]. Los commits experimentales anteriores, los intentos de prototipo y los enfoques abandonados no sobreviven en el libro mayor corporativo.

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
| `github.com/pointsav` | Proveedor — fuente de verdad | Solo `ps-administrator` (acepta fusiones); `jwoodfine`/`pwoodfine` (bifurcación y PR) |
| `github.com/woodfine` | Cliente — libro mayor de producción | Solo `mcorp-administrator` |
| Cuentas personales de contribuyentes | Forja — sandbox | El contribuyente posee su bifurcación por completo |

Los repositorios canónicos a mediados de 2026 incluyen:

| Repositorio | Rol |
|---|---|
| `pointsav/pointsav-monorepo` | Todo el código `os-*`, `app-*`, `service-*`, `system-*` (véase [[os-family-overview|familia de SO]]) |
| `pointsav/content-wiki-documentation` | Wiki de documentación pública |
| `woodfine/woodfine-fleet-deployment` | Catálogo de implementación del cliente y artículos GUIDE |

## Por qué esta estructura escala

Un nuevo contribuyente no necesita aprender un nuevo protocolo. Bifurca, envía, abre un pull request. Las puertas arquitectónicas — la transferencia de PI por squash-merge, el espejo del cliente, la implementación fast-forward, el reinicio basado en trunk — suceden por encima de ellos. La experiencia diaria del contribuyente es solo la Etapa 1.

La estructura escala a muchos contribuyentes sin perder la brecha de aire, porque la brecha de aire es impuesta por la puerta del administrador, no por reglas sociales.

## Véase también

- [[three-layer-architecture]] — las capas SOFTWARE / ESCAPARATE / INSTANCIAS que abarca la cadena de suministro
- [[six-tier-sovereignty-matrix]] — la taxonomía de directorios del monorepo del proveedor en la Etapa 1
- [[legal-and-ip-structure]] — la mecánica de transferencia de PI que implementa la Etapa 3
