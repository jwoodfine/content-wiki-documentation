---
schema: foundry-doc-v1
title: "Guías para Desarrolladores"
slug: how-to
category: how-to
content_type: how-to
type: topic
status: active
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: _index.md
---

Guías paso a paso para construir con y sobre la plataforma PointSav. Cada guía aborda una tarea específica; síguelas de principio a fin y consulta los artículos de arquitectura relacionados cuando necesites la teoría subyacente.

Para los conceptos detrás de cada guía, comienza en [[architecture|Arquitectura]] o [[patterns|Patrones]]. Para una visión general de la arquitectura de la plataforma, consulta [[totebox-orchestration-development]].

## Primeros pasos

La base: autentica tu dispositivo y abre tu primera sesión.

- [[pair-a-new-device|Vincular un nuevo dispositivo]] — registra una máquina mediante autorización basada en hardware; sin nombre de usuario ni contraseña
- [[open-first-totebox-session|Abrir tu primera sesión Totebox]] — navega a un archivo, lee tu bandeja de entrada y empieza a contribuir

## Autorización de máquinas

Operaciones de credenciales y control de acceso.

- [[pair-a-new-device|Vincular un nuevo dispositivo]] — el flujo de registro principal
- [[authenticate-binary-downloads|Autenticar descargas de binarios]] — verifica y descarga binarios firmados desde el punto de distribución privado

## Integración y datos

Conecta tuberías de datos externas y crea aplicaciones de inteligencia de ubicación.

- [[build-a-colocation-map|Construir un mapa de co-ubicación]] — consulta la API del motor GIS y renderiza una capa de clústeres con MapLibre
- [[federate-archives-via-content-mounts|Federar archivos mediante montajes de contenido]] — monta contenido wiki de un archivo en una segunda instancia usando montajes TOML declarativos

## Autoalojamiento

Despliega la plataforma en tu propia infraestructura.

- [[self-host-a-deployment|Autoalojar un despliegue]] — provisiona un archivo Totebox en un nodo de cómputo compatible
- [[run-local-slm-inference|Ejecutar inferencia SLM local]] — enruta la inferencia a través de Doorman hacia el modelo de lenguaje en las instalaciones

## Véase también

- [[architecture/_index|Arquitectura]] — arquitectura transversal de la plataforma
- [[patterns/_index|Patrones]] — patrones de diseño nombrados utilizados en toda la plataforma
- [[totebox-session]] — qué es una sesión Totebox y qué puede hacer
- [[machine-based-auth]] — cómo funciona la autorización basada en máquinas
