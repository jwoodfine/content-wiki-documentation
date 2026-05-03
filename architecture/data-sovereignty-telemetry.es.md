---
schema: foundry-doc-v1
type: topic
slug: data-sovereignty-telemetry
title: Soberanía de Datos y Telemetría de Estado Cero
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: data-sovereignty-telemetry.md
---

# Soberanía de Datos y Telemetría de Estado Cero

Los sistemas de PointSav están diseñados para garantizar la soberanía absoluta de los datos mediante una arquitectura de "Estado Cero" que elimina la recolección de información de identificación personal (PII).

## Infraestructura sin Cookies

Foundry prohíbe estrictamente el uso de cookies de seguimiento y analíticas de terceros. Esto elimina la necesidad legal de banners de consentimiento de cookies, permitiendo una interfaz más limpia y profesional.

## Inteligencia mediante Anonimización de IP

La recopilación de datos operativos se realiza exclusivamente mediante una arquitectura interna que protege la privacidad:
- **Enmascaramiento de IP:** El sistema elimina automáticamente el último octeto de la dirección IP (por ejemplo, `192.168.1.45` se convierte en `192.168.1.0`).
- **Datos Geosociales Anónimos:** Esto convierte la información personal en datos geográficos agregados, permitiendo auditar la seguridad y el uso de la plataforma sin identificar a usuarios individuales.

## Transparencia Institucional

Todas las interfaces públicas incluyen una declaración de privacidad que certifica que el sistema no rastrea estados de sesión ni cosecha datos personales, cumpliendo con los estándares más exigentes de seguridad y confidencialidad.
