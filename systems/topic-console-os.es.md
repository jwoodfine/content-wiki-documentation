---
schema: foundry-doc-v1
title: "Console OS"
slug: topic-console-os
category: systems
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: topic-console-os.md
cites: []
## Véase también

- [[topic-totebox-os]]
- [[topic-infrastructure-os]]
- [[topic-mediakit-os]]
- [[topic-privategit-os]]

---

Console OS es el sistema operativo basado en terminal diseñado para la administración de los servicios e infraestructura de PointSav. Opera como la interfaz principal para los administradores del sistema y los usuarios avanzados, proporcionando acceso directo a los mecanismos subyacentes de la plataforma.

## Arquitectura de hipervisor

En el sistema de PointSav, Console OS funciona como un **Hipervisor de Tipo II**. Típicamente se despliega dentro de una máquina virtual en un dispositivo anfitrión, permitiendo a los usuarios ejecutar sistemas operativos de escritorio estándar en su hardware local mientras mantienen un entorno seguro y aislado para la gestión institucional.

Para los usuarios que requieren un entorno de ejecución nativo, Console OS también puede desplegarse directamente en hardware bare-metal.

## Interfaz operativa

Console OS prioriza la estabilidad y la eficiencia sobre la novedad gráfica. La arquitectura del sistema está construida alrededor de dos modelos de interacción principales:

1. **Interfaz de Línea de Comandos (CLI):** Proporciona el control más granular para la configuración técnica, la orquestación del despliegue y los scripts.
2. **Interfaz de Usuario de Terminal (TUI):** Ofrece un entorno semi-gráfico controlado por teclado para tareas administrativas rutinarias, como la gestión de los estados de Totebox Archive y el monitoreo de la telemetría del sistema.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
