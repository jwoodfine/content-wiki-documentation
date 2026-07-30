---
schema: foundry-doc-v1
title: "Banco de trabajo de navegador os-privategit"
slug: os-privategit-workbench
short_description: "app-privategit-workbench es un editor de archivos basado en navegador incluido en os-privategit que proporciona una interfaz de tres columnas para trabajar con archivos de archivo sin una sesión de terminal."
category: systems
type: topic
content_type: topic
status: archived
archived: 2026-07-30
archived_reason: "Duplicado redundante de applications/app-privategit-workbench.md — mismo crate, misma arquitectura, texto casi idéntico. El propio slug de esta copia usaba incorrectamente un prefijo os- para lo que, según su propio cuerpo, es un crate app-*."
superseded_by: app-privategit-workbench
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: os-privategit-workbench.md
language: es
---

`app-privategit-workbench` es un editor de archivos basado en navegador incluido en el sistema operativo anfitrión [[os-privategit|`os-privategit`]]. Presenta un punto de acceso HTTP local que sirve una aplicación de página única con un diseño de tres columnas: una barra lateral de árbol de archivos, un visor de contenido y un editor de texto plano.

El banco de trabajo es la superficie principal de autoría y revisión para los operadores de [[totebox-orchestration|Totebox Orchestration]] y los Miembros de la Comunidad que desean acceso basado en navegador directo a su árbol de [[totebox-archive|archivos de archivo]] sin una sesión de terminal. No es una superficie de publicación — escribe en el sistema de archivos local y depende del canal de confirmación y promoción existente para el control de versiones.

## Arquitectura

El banco de trabajo es un único crate de Rust (`app-privategit-workbench`, AGPL-3.0-or-later) en `pointsav-monorepo`. Tiene dos componentes: un servicio de escritura (Rust/axum) que gestiona lecturas y escrituras de archivos, vinculado a una dirección de bucle invertido y nunca expuesto directamente a redes externas; y una aplicación de página única autocontenida incrustada en el binario en tiempo de compilación.

## Modelo de seguridad

El servicio de escritura aplica cuatro capas de contención alineadas con el enfoque de [[pre-commit-defense-in-depth|defensa en profundidad]] utilizado en toda la plataforma: contención de raíz (todas las rutas se canonizan y verifican para permanecer dentro de la ruta del sistema de archivos declarada); protección CSRF (cada solicitud `PUT /file` requiere la cabecera `X-Foundry-Editor: 1`); lista de extensiones permitidas (solo se permiten escribir extensiones de texto plano y código fuente reconocidas); y la bandera de escritura (`writable = false`) que rechaza todos los intentos de escritura a esa raíz.

## Relación con os-privategit

`app-privategit-workbench` está incluido en el sistema operativo anfitrión `os-privategit` junto a `app-privategit-design-system` y `service-privategit`. El crate está licenciado bajo AGPL-3.0-or-later.

La Fase 4 tiene previsto integrar CodeMirror 6 para el resaltado de sintaxis e introducir raíces autenticadas con alcance de escritura por usuario.

## Véase también

- [[os-privategit]] — el sistema operativo anfitrión que incluye el banco de trabajo
- [[totebox-archive]] — el Archivo Totebox con el que los operadores trabajan a través del banco de trabajo
- [[machine-based-auth]] — el modelo de autorización para raíces de banco de trabajo autenticadas
- [[os-family-overview]] — la familia de ocho SO y cómo encaja os-privategit
