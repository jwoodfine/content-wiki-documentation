---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: data-sovereignty-telemetry
short_description: "La arquitectura de telemetría de la plataforma hoy: qué se recopila realmente, cómo se usa, y una brecha conocida frente al diseño de estado cero que se pretende alcanzar."
title: Soberanía de datos y telemetría de estado cero
audience: vendor-public
bcsc_class: forward-looking
language: es
paired_with: data-sovereignty-telemetry.md
last_edited: 2026-07-30
category: security
status: archived
archived: 2026-08-03
archived_reason: "reemplazado por el piloto de autoría fresh-draft-first frente a los nuevos tokens de content-schema (schema-topic.yaml)"
superseded_by: data-sovereignty-telemetry
---

**Corrección mayor (2026-07-30):** este artículo describía anteriormente un
mecanismo de enmascaramiento de IP en vigor y enmarcaba la postura de telemetría de
la plataforma como una arquitectura de estado cero conforme con RGPD/PIPEDA en tiempo
presente. Verificado directamente contra el código de ingestión real
(`app-mediakit-telemetry/src/bin/telemetry-daemon.rs`, `omni-matrix-engine.rs`): no
existe ningún enmascaramiento en el pipeline hoy. El cuerpo a continuación se ha
reescrito para describir el comportamiento actual con exactitud, en lugar del diseño
originalmente previsto. Escalado a Command/project-totebox por correo
(`command-20260730-active-privacy-compliance-discrepancy-se`) dado lo que está en
juego en materia de cumplimiento — no resuelto unilateralmente. Esta reescritura
refleja solo lo verificado sobre el manejo de IP; las afirmaciones sobre cookies y
ausencia de estado de sesión no se reverificaron de forma independiente en este pase
y se mantienen tal como estaban en el artículo original, no revalidadas.

El objetivo de diseño declarado de [[pointsav-overview|PointSav]] es una arquitectura de telemetría de estado cero — sin información de identificación personal retenida, sin cookies de seguimiento, sin estado de sesión. **Ese objetivo no se cumple totalmente hoy.** El pipeline de ingestión real registra actualmente la dirección IP completa y sin enmascarar del solicitante, la marca de tiempo, el URI solicitado y el user-agent en cada solicitud — lo opuesto a la señal enmascarada y anonimizada que este artículo afirmaba anteriormente. Esta es una brecha conocida frente al diseño previsto, no una postura de cumplimiento actualmente exacta. Véase también [[sovereign-telemetry|telemetría soberana]] y [[telemetry-architecture|la arquitectura de telemetría]].

## Puntos clave

- El diseño previsto es de estado cero: sin PII, sin cookies, sin retención de sesión. **La parte de manejo de IP de ese diseño no está implementada hoy** — véase abajo.
- No ocurre ningún enmascaramiento de IP actualmente. La dirección IP completa se escribe en un registro en texto plano tal como se recibe; no se elimina, trunca ni anonimiza en ningún punto del pipeline.
- No se muestra actualmente ningún banner de consentimiento de cookies; las interfaces públicas de la plataforma no parecen desplegar cookies de seguimiento (mantenido del artículo original, no reverificado independientemente en este pase).
- Cualquier texto de divulgación que describa la postura de privacidad de este sistema en tiempo presente debe tratarse como una descripción del diseño *previsto*, no del sistema tal como funciona hoy.

## Lo que el pipeline realmente hace hoy

La ruta de ingestión real es `app-mediakit-telemetry/src/bin/telemetry-daemon.rs`: lee el encabezado `x-forwarded-for` literal de cada solicitud entrante y añade la dirección IP completa — junto con la marca de tiempo, el URI solicitado y el user-agent completo — a un archivo CSV en texto plano (`assets/ledger_telemetry.csv`). No ocurre ninguna eliminación de octetos, truncamiento ni hashing en ninguna parte de esta función. Un proceso posterior, `omni-matrix-engine.rs`, realiza entonces una búsqueda GeoIP de MaxMind directamente contra esa misma dirección IP completa para derivar una señal geográfica aproximada — una dirección enmascarada no produciría una búsqueda útil, por lo que el diseño actual del pipeline depende activamente de conservar la dirección completa, en lugar de retenerla incidentalmente.

## Brecha conocida y remediación

Cerrar esta brecha — de modo que el sistema coincida realmente con el diseño de estado cero previsto — requiere enmascarar la IP antes de la persistencia (aceptando una geolocalización más gruesa) o reestructurar el paso de GeoIP para que funcione a partir de un valor ya enmascarado. Ninguna de las dos opciones se ha implementado a la fecha de esta redacción. Esto se señala al equipo propietario de `app-mediakit-telemetry` como un elemento real de remediación, no meramente una corrección documental — el sistema subyacente, no solo este artículo, necesita cambiar antes de que la afirmación de estado cero pueda hacerse con exactitud nuevamente.

## Divulgación regulatoria — tratar como intención, no como estado actual

Algunas interfaces públicas pueden llevar texto de divulgación que describa este sistema en términos de estado cero y enmascarado. Hasta que se cierre la brecha anterior, dicha divulgación debe entenderse como una descripción de la postura prevista de la plataforma, no como una afirmación técnica actualmente exacta — este wiki no reproduce aquí ese texto de divulgación, para evitar reiterar una afirmación que se sabe inexacta hoy.

## Véase también

- [[sovereign-telemetry]]
- [[machine-based-auth]]
- [[zero-execution-routing]]
- [[cryptographic-ledgers]]
