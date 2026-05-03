---
schema: foundry-doc-v1
title: "Doctrina Foundry 2030 — Resumen"
slug: foundry-doctrine-overview.es
category: architecture
type: topic
quality: published
short_description: Resumen público fiel de la carta constitucional de la Doctrina Foundry — seis pilares, cincuenta y dos afirmaciones de salto adelante, ocho invenciones operativas entre industrias, y el modelo económico que las sostiene.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - mcp-spec
  - olmo3-allenai
paired_with: foundry-doctrine-overview.md
---

La **Doctrina Foundry 2030** es la carta constitucional del entorno de desarrollo de software de PointSav. Define los seis pilares de la arquitectura de la plataforma, cincuenta y dos afirmaciones de salto adelante que constituyen sus compromisos estructurales, ocho invenciones operativas entre industrias, y el modelo económico que la sostiene. La propia doctrina es un artefacto público — versionada, firmada y publicada bajo CC BY 4.0 en cada versión MINOR.

Este artículo es un resumen público de la doctrina v0.1.0 ALPHA (ratificada el 30 de abril de 2026). El texto autorizado es DOCTRINE.md, disponible a través del repositorio `pointsav/factory-release-engineering`.

## Los Seis Pilares

Los seis pilares son los invariantes de la arquitectura. No son principios aspiracionales; son restricciones aplicadas.

**1. Solo texto plano.** UTF-8 Markdown para prosa, YAML simple para el enrutamiento. Sin formatos binarios, sin bases de datos, sin daemons, sin índices activos a nivel del sustrato.

**2. Alcance geométrico.** El rol de una sesión está determinado por el directorio en el que comienza — no por configuración ni declaración. Master en la raíz del espacio de trabajo; Root en cualquier raíz de repositorio de ingeniería; Task dentro de un directorio de clúster por proyecto.

**3. Flujo unidireccional.** El desarrollo de software siempre procede proveedor → cliente → despliegues. Sin escrituras directas inversas. Todas las solicitudes entre capas viajan a través de un buzón de archivos.

**4. Buzón en cada límite.** Cada rol tiene una bandeja de entrada y una bandeja de salida — archivos Markdown de texto plano, con control de versiones, duraderos.

**5. Artefactos autodescriptivos.** Cada directorio con el que vale la pena interactuar lleva un `MANIFEST.md` que declara su origen, propietario, linaje y estado actual.

**6. Sobre de garantía humana en el bucle.** El trabajo rutinario se ejecuta de forma autónoma. La atención humana se reserva para el conjunto definido de eventos de punto de control estricto: despliegues de nuevos modelos en producción, operaciones destructivas, cambios de gobernanza.

## Las Afirmaciones de Salto Adelante

La tesis central de la doctrina: una plataforma cuyo modelo cabe completamente en texto plano en una sola VM, funciona sin una API externa y sobrevive 100 años en un disco duro se vuelve más valiosa a medida que la conectividad global se fragmenta y los entornos regulatorios divergen.

Cincuenta y dos afirmaciones constituyen este compromiso estructural. Las afirmaciones añadidas en v0.1.0 (#43–#54) constituyen el compromiso arquitectónico soberano para PYMEs:

- **Disciplina de Cómputo de Límite Único (#43)** — cada llamada de inferencia de IA pasa por un único límite de servicio, el Doorman.
- **Aprendizaje Fundamentado en Grafo de Conocimiento (#44)** — el servicio de inferencia consulta el grafo de conocimiento por inquilino antes de cada solicitud sustantiva.
- **TUI como Productor de Corpus (#45)** — cada interacción terminal con el servicio de inferencia es una contribución de corpus de entrenamiento curada.
- **MCP como Protocolo del Sustrato (#46)** — cada servicio de Ring 1 y Ring 2 expone una interfaz de servidor MCP como su contrato externo principal.
- **Taxonomía Semilla como Bootstrap para PYMEs (#47)** — cada despliegue de inquilino se aprovisiona con una taxonomía semilla de cuatro partes como el bootstrap de su grafo de conocimiento.
- **IP del Grafo de Propiedad del Cliente (#48)** — el grafo de conocimiento por inquilino es propiedad intelectual del cliente.
- **Especialista Soberano del Lado del Cliente Nivel 0 (#49)** — el despliegue de referencia Nivel 0 es un dispositivo de pequeño factor de forma que ejecuta el sustrato determinista completo más un modelo especialista de 1B, sin GPU requerida.
- **Mercado de Paquetes Semilla Verticales (#50)** — paquetes semilla específicos de la industria distribuidos como taxonomías iniciales para nuevos despliegues de inquilinos.
- **Código para Máquinas Primero (#51)** — cada contrato entre servicios, registro de auditoría, configuración y ontología es legible por máquinas como superficie primaria.
- **Sustrato de Flujo Inverso (#52)** — la misma puerta de enlace Doorman y el mismo registro de auditoría que aplican la disciplina entrante también aplican los flujos comerciales salientes: un mercado de datos y un intercambio de publicidad.
- **Liquidación de Cartera de Servicios (#53)** — los ingresos del mercado y el intercambio de publicidad se acumulan en un libro de contabilidad interno por inquilino; PointSav nunca es un intermediario de custodia.
- **Caso Base del Sustrato Sin Inferencia (#54)** — el Archivo Totebox permanece completamente operativo y libremente transferible incluso cuando ningún nivel de inferencia está disponible.

## La Arquitectura de Tres Anillos

La plataforma organiza los servicios en tres anillos. Los Anillos 1 y 2 son deterministas y funcionan completamente sin el Anillo 3.

**Anillo 1 — Ingesta en el Límite (por inquilino, servidores MCP).** Servicios para la ingesta de documentos, datos de personas, correo electrónico y entrada directa.

**Anillo 2 — Conocimiento y Procesamiento (multi-inquilino mediante moduleId).** Servicios de extracción, grafo de contenido, búsqueda y egreso. El núcleo determinista de la plataforma, funcional sin IA.

**Anillo 3 — Inteligencia Opcional (instancia única, multi-inquilino).** El Doorman (`service-slm`) es la totalidad del Anillo 3. Enruta entre tres niveles de cómputo: Nivel A local (OLMo 1B en hardware del cliente, costo marginal cero), Nivel B de ráfaga de GPU (OLMo 32B Think en una instancia de GPU de corta duración, controlada por el cliente), y Nivel C de API externa (API de proveedor externo con lista de permitidos explícita por solicitud). El Anillo 3 es estructuralmente opcional.

## Las Ocho Invenciones Entre Industrias

La doctrina extrae patrones operativos de ocho dominios fuera del software: Pasaporte del Espacio de Trabajo (marítimo), NOTAM (aviación), Procedimiento de Retiro (farmacéutico), Conocimiento de Embarque (transporte marítimo), Operación Diferida en el Tiempo (bancario/fiduciario), Modo Aprendiz (habilitación tipo aviación / residencia médica), Ancla de Integridad (notaría / sellado de tiempo público), y Convención Constitucional (IETF RFC / enmienda constitucional).

## El Modelo Económico

Los artefactos de conocimiento son la capa pública — publicados bajo licencias abiertas en cada versión MINOR de la Doctrina, libremente reutilizables. El umbral comercial es la agregación multi-Totebox. Un solo Totebox es infraestructura soberana; las operaciones que cruzan los límites del Totebox son un servicio de pago.

El modelo de contribuidores que sostiene esto: 4–7 empleados del Núcleo, 50–100 contribuidores de pago bajo contratos basados en resultados, y más de 10,000 contribuidores abiertos previstos construyendo sobre el sustrato público.

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales del Sustrato Compuesto (Afirmación #18)
- [[compounding-doorman]] — la disciplina de cómputo de límite único (Afirmación #43)
- [[adapter-composition]] — el Álgebra de Composición de Adaptadores (Afirmación #22)
- [[knowledge-commons]] — el modelo de Conocimiento Común / Comercio de Servicios (Afirmación #23)
- [[system-substrate-doctrine]] — el Registro de Capacidades y el Sustrato Soberano de Dos Bases (Afirmaciones #33, #34)

## Referencias

1. NI 51-102 Obligaciones de Divulgación Continua — Administradores de Valores de Canadá.
2. Aviso de Personal OSC 51-721 Divulgación de Información Prospectiva.
3. Especificación MCP — Protocolo de Contexto de Modelo, Anthropic, 2024.
4. OLMo 3 — Allen Institute for AI, Apache 2.0.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Atribución 4.0 Internacional](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
