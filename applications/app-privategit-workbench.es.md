---
schema: foundry-doc-v1
title: "Estación de trabajo para desarrolladores (navegador)"
slug: app-privategit-workbench.es
category: applications
type: topic
quality: stub
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-05-29
editor: project-editorial
short_description: "app-privategit-workbench es un editor de archivos basado en navegador incluido en el sistema operativo host os-privategit, que presenta una interfaz de tres columnas — árbol de archivos, visor y editor — para trabajar con archivos de texto plano y código fuente a través del árbol de archivos del clúster."
paired_with: app-privategit-workbench.md
---

> **Nota:** Esta página es un resumen provisional. La versión completa en español está prevista para una próxima revisión editorial.
> *See also:* [app-privategit-workbench](app-privategit-workbench.md) — English version (complete).

`app-privategit-workbench` es un editor de archivos basado en navegador incluido
en el sistema operativo host [[os-privategit|`os-privategit`]]. Presenta un endpoint HTTP local
que sirve una aplicación de página única con un diseño de tres columnas: una
barra lateral con el árbol de archivos, un visor de contenido y un editor de
texto plano.

La estación de trabajo es la superficie de creación y revisión principal para
los operadores de [[totebox-orchestration|Totebox Orchestration]] y los Miembros de la Comunidad que
desean acceso directo al [[totebox-archive|árbol de archivos del clúster]] desde el navegador, sin
necesidad de una sesión de terminal. No es una superficie de publicación —
escribe en el sistema de archivos local y depende del flujo de control de
versiones basado en git para el historial y la promoción.

El servicio de escritura (Rust/axum) aplica contención de raíz alineada con la [[pre-commit-defense-in-depth|defensa en profundidad]] utilizada en toda la plataforma, una lista de extensiones permitidas y detección de conflictos basada en mtime. El acceso a raíces con permiso de escritura está gobernado por el modelo de [[machine-based-auth|autorización basada en máquinas]]. La aplicación de página única está integrada en el binario en tiempo de compilación; no se cargan recursos externos en tiempo de ejecución.

El crate tiene licencia Apache 2.0 y está destinado a implementaciones en
instancias de nivel cliente de `os-privategit`.

## Véase también

- [[os-privategit]] — el sistema operativo host que incluye esta estación de trabajo
- [[totebox-archive]] — el árbol de archivos del clúster con el que trabajan los operadores
- [[machine-based-auth]] — el modelo de autorización que rige el acceso a raíces con permiso de escritura
- [[pre-commit-defense-in-depth]] — la disciplina de defensa en profundidad aplicada por el servicio de escritura
