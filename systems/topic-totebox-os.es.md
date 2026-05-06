---
schema: foundry-doc-v1
title: "Totebox OS"
slug: topic-totebox-os
category: systems
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: topic-totebox-os.md
cites: []
## Véase también

- [[topic-totebox-archive]]
- [[topic-totebox-orchestration]]
- [[topic-console-os]]
- [[topic-infrastructure-os]]

---

Totebox OS es la capa de archivo de datos central de la plataforma PointSav. Se ejecuta en un microkernel seL4 y aplica una separación estricta entre los motores de ejecución de software y los libros contables corporativos que esos motores leen y escriben. Cada registro institucional vive como un archivo plano inerte — Markdown, YAML o CSV — que no requiere ningún tiempo de ejecución propietario para abrirse o interpretarse décadas después.

## Modelo de directorio

Un despliegue de Totebox sigue un diseño de tres directorios:

```
cluster-totebox-corporate/
├── app-console-input/      # software de ejecución
├── assets/                 # bóveda física — PDFs, imágenes
└── ledger/                 # máquina de estados — metadatos YAML, libros contables CSV
```

La ejecución del software y los datos que procesa ocupan directorios distintos, conectados solo a través de rutas de acceso explícitas y auditadas.

## Por qué importa el texto sin formato

Un registro institucional en formato de texto sin formato puede ser leído por cualquier herramienta estándar — ahora, dentro de diez años, o dentro de treinta años. Un registro en un formato de base de datos propietario depende de que el proveedor siga siendo solvente y mantenga el software de decodificación. La arquitectura de Totebox OS elige la legibilidad a largo plazo sobre la conveniencia a corto plazo.

## Atestación de integridad

Cada archivo en el directorio de activos y libro contable está respaldado por checksums SHA-256. El Totebox OS ejecuta verificación de integridad periódica; cualquier discrepancia entre el hash almacenado y el contenido del archivo activo activa una alerta al operador.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
