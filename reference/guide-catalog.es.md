---
schema: foundry-doc-v1
title: "Índice de Guías para Desarrolladores"
slug: guide-catalog
category: reference
type: topic
content_type: topic
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: guide-catalog.md
aliases:
  - developer-guide-index
---

El Índice de Guías para Desarrolladores enumera las guías prácticas de la plataforma PointSav, organizadas por área de interés del desarrollador. Cada guía cubre una tarea específica que un desarrollador realiza al construir con la plataforma o desplegarla. Para la arquitectura subyacente en la que se basa cada guía, siga los enlaces a los artículos dentro de cada guía.

Los manuales operativos internos para el despliegue de flota Woodfine no se incluyen aquí — son documentos operativos para aprovisionamiento y mantenimiento, no guías públicas para desarrolladores.

## Primeros pasos

Estas guías cubren los primeros pasos para un desarrollador nuevo en la plataforma: configurar la autorización del dispositivo y abrir una sesión de trabajo.

- [[pair-a-new-device]] — registra un nuevo dispositivo y asígnale un nivel de emparejamiento (INPUT, USER o INTERFACE)
- [[open-first-totebox-session]] — abre una sesión de trabajo en un Archivo Totebox y navega por el ciclo de vida de la sesión

## Autorización por hardware

Estas guías cubren el emparejamiento criptográfico de dispositivos que controla el acceso a la plataforma.

- [[pair-a-new-device]] — el flujo de emparejamiento principal; cubre los cuatro tipos de emparejamiento (ADMIN, INPUT, USER, INTERFACE) y cómo verificar y revocar

Para el modelo de autorización que sustenta el emparejamiento, consulta [[machine-based-auth]] y [[pairing-as-permission]].

## Integración y datos

Estas guías cubren el consumo de datos de la plataforma y la conexión de aplicaciones externas.

- [[build-a-colocation-map]] — autentícate contra la API de tiles SIG y renderiza marcadores de clústeres con color por nivel en MapLibre
- [[authenticate-binary-downloads]] — verifica las versiones de binarios firmados con Ed25519 desde el punto de distribución privado
- [[federate-archives-via-content-mounts]] — declara un montaje de contenido secundario en `knowledge.toml` y accede a artículos federados entre instancias

## Autoalojamiento

Estas guías cubren el despliegue y la ejecución de componentes de la plataforma en infraestructura controlada por el operador.

- [[self-host-a-deployment]] — aprovisiona una instancia de despliegue nombrada, inicia la pasarela y conéctala a la plataforma central
- [[run-local-slm-inference]] — inicia el servicio SLM local, verifica el punto de conexión de salud del Doorman y envía solicitudes de inferencia desde os-console

## Véase también

- [[machine-based-auth]] — el modelo de autorización por hardware que sustenta todo el acceso a la plataforma
- [[totebox-orchestration-development]] — el modelo de orquestación de sesiones que rige el uso de los Archivos Totebox
- [[app-mediakit-knowledge]] — el motor wiki que sirve esta instancia de documentación
