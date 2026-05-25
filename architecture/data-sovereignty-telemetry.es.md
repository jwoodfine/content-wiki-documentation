---
schema: foundry-doc-v1
type: topic
slug: data-sovereignty-telemetry
short_description: "La plataforma recopila solo telemetría geoespacial anonimizada y enmascarada por IP sin información de identificación personal retenida, añadiendo divulgación regulatoria obligatoria a las interfaces públicas."
title: Soberanía de datos y telemetría de estado cero
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: data-sovereignty-telemetry.md
last_edited: 2026-05-25
category: architecture
---

Las interfaces de la plataforma PointSav operan sobre una arquitectura de telemetría de estado cero: no se recopila información de identificación personal (PII), no se despliegan cookies de seguimiento y no se retiene ningún estado de sesión. Las métricas operativas se limitan a señales geoespaciales anónimas y enmascaradas por IP utilizadas para la auditoría de la infraestructura. Los operadores en sectores regulados obtienen una postura pública coherente con el RGPD, PIPEDA y requisitos equivalentes de minimización de datos, sin necesidad de marcos de consentimiento de cookies.

## Infraestructura sin cookies

La plataforma prohíbe las cookies de seguimiento, el rastreo en almacenamiento local persistente y las integraciones de analítica de terceros. Las interfaces públicas no incluyen scripts de analítica de terceros, eliminando la obligación legal de mostrar banners de consentimiento de cookies según la Directiva ePrivacy y regímenes equivalentes.

## Protocolo de anonimización geoespacial

Las métricas operativas se recopilan a través de una arquitectura de ping de primera parte. El servidor de ingestión aplica enmascaramiento de IP obligatorio — el último octeto de la dirección IP entrante se elimina al recibirla (por ejemplo, `192.168.1.45` se convierte en `192.168.1.0`). El registro resultante es una señal geoespacial imprecisa sin identificación a nivel de red. Los datos de interacción — como los eventos de acceso a documentos — se utilizan para auditar la seguridad de la infraestructura y medir los patrones de uso de la plataforma; ningún registro está vinculado a una identidad individual.

## Divulgación regulatoria obligatoria

Todas las interfaces públicas añaden la siguiente declaración a sus bloques legales:

> "Infraestructura digital y postura de privacidad: esta interfaz opera sobre una arquitectura de ejecución cero y telemetría de estado cero. No despliega cookies de seguimiento, no retiene estados de sesión ni recopila información de identificación personal. Las interacciones del sistema se limitan a la recopilación de datos de enrutamiento de red anonimizados y enmascarados, con el único fin de auditar la seguridad de la infraestructura y verificar el acceso a documentos."

## Véase también

- [[sovereign-telemetry]]
- [[machine-based-auth]]
- [[zero-execution-routing]]
- [[cryptographic-ledgers]]
