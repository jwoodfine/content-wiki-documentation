---
schema: foundry-doc-v1
title: "Código para Máquinas Primero"
slug: code-for-machines-first.es
category: architecture
type: topic
quality: published
short_description: "Cada contrato entre servicios Foundry, registro de auditoría, configuración y ontología es legible por máquinas como superficie primaria; las interfaces para humanos son capas sobre APIs primero-para-máquinas."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: code-for-machines-first.md
---

**Código para Máquinas Primero** es la disciplina de diseño por la cual cada contrato entre servicios Foundry, registro de auditoría, archivo de configuración y ontología debe ser legible por máquinas como su superficie primaria. Las interfaces para el operador — la TUI de terminal, las interfaces web, los clientes móviles — son capas sobre APIs primero-para-máquinas. Esta disciplina codifica la reclamación doctrinal #51.

## Los formatos de datos

La plataforma usa un conjunto consistente de formatos en todas las superficies: la comunicación entre servicios usa MCP; el registro de auditoría usa JSONL con versionado de esquema; las taxonomías semilla usan JSON; la configuración de servicios usa TOML o YAML; las convenciones y la documentación usan Markdown con frontmatter estructurado; la configuración por inquilino usa YAML.

Cada artefacto es mutable e introspectable por máquinas. El endpoint `describe` de MCP en cualquier servicio devuelve el catálogo de herramientas actual en formato legible por máquinas. No existe ninguna superficie de configuración que requiera que un operador humano interprete campos no documentados.

## Por qué esto importa

**Observabilidad consistente.** Los datos estructurados en cada capa significan que las consultas de auditoría y las métricas tienen una forma uniforme entre servicios e inquilinos. Una consulta del operador contra el registro de auditoría y una verificación de cumplimiento automatizada consultan el mismo esquema JSONL.

**Extensión del cliente sin bifurcar.** Los clientes añaden fuentes de datos específicas de su vertical escribiendo servidores MCP que usan el mismo protocolo que todos los servicios integrados. No se requiere ningún adaptador personalizado para conectar una herramienta construida por el cliente a la plataforma.

**Composición nativa de IA.** El substrato es consumible por agentes de IA — sesiones de tarea, agentes construidos por el cliente, integraciones de socios — sin un paso de retrofit. Esto es lo que hace posible el patrón [[knowledge-graph-grounded-apprenticeship]]: el grafo ya es legible por máquinas; el Portero puede consultarlo programáticamente en tiempo de inferencia.

**Facilidad de migración.** La exportación de datos es una operación rutinaria de máquinas que produce un paquete en formato abierto. No existe ningún proyecto de migración que involucre cooperación del proveedor, porque los datos nunca estuvieron bloqueados en un formato específico del proveedor.

## Las dos excepciones limitadas

Los documentos de doctrina y convención en prosa, incluido este artículo, tienen la prosa como su superficie primaria. El frontmatter es legible por máquinas; el cuerpo está escrito para lectores humanos. La documentación de temas y guías sigue el mismo patrón. Estas excepciones son explícitas y limitadas. El valor predeterminado es primero-para-máquinas.

## Composición

Esta disciplina es la reclamación estructural que [[mcp-substrate-protocol]] realiza a nivel de cable. Cada servicio expone su contrato a través del `describe` de MCP, que devuelve un catálogo de herramientas legible por máquinas. Las superficies orientadas al ser humano consumen este catálogo de la misma manera que lo haría cualquier cliente automatizado.

## Véase También

- [[mcp-substrate-protocol]] — la realización estructural de los contratos de servicio primero-para-máquinas vía MCP
- [[knowledge-graph-grounded-apprenticeship]] — las consultas del grafo son llamadas de herramientas MCP primero-para-máquinas
- [[substrate-without-inference-base-case]] — los paquetes de exportación son formatos abiertos legibles por máquinas

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-code-for-machines-first.md` (refinado el 30 de abril de 2026). No hay reclamaciones comerciales prospectivas en esta convención.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
