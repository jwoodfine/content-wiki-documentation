---
schema: foundry-doc-v1
title: "os-orchestration — El agregador de flota"
slug: os-orchestration
category: systems
type: concept
content_type: topic
quality: complete
index_group: operator-surfaces
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
paired_with: os-orchestration.md
short_description: "os-orchestration es el sistema operativo de nivel comercial que permite a un único operador ver, consultar y comandar muchos archivos Totebox a la vez — el Agregador de Flota para portafolios multi-entidad y despliegues empresariales."
cites: []
---

**Corrección, 2026-08-03 (paridad con la versión en inglés).** Verificado directamente contra `origin/main` del monorepo: `os-orchestration/` existe como crate registrado (`Cargo.toml` propio, `license = "FSL-1.1-ALv2"`), pero su `src/lib.rs` es un scaffold de 4 líneas ("SYSTEM EVENT: os-orchestration scaffold verified.") — sin lógica de agregación. La afirmación del "Protocolo PointSav (PSP)" se confirmó fabricada — cero huella de código en `origin/main` — y se elimina más abajo; la descripción del protocolo de agregación ahora se presenta como previsto/planeado, sin inventar un nombre de protocolo. El resto del artículo también se ha reformulado en este pase con lenguaje previsto/planeado — la funcionalidad descrita aún no está construida. La afirmación de licencia "Propietario" en la tabla se mantiene como hecho actual confirmado, ya que la clasificación del archivo `LICENSE` aplica hoy aunque el código de agregación todavía no exista.

`os-orchestration` está previsto como el sistema operativo de nivel comercial que permitiría a un único operador ver, consultar y comandar muchos [[totebox-archive|archivos Totebox]] a la vez. Mientras [[console-os|`os-console`]] se conecta a un único [[totebox-os|`os-totebox`]], `os-orchestration` está pensado como el concentrador entre la Consola de un operador y una flota de Toteboxes — lo que un ejecutivo vería para conocer la posición de cada propiedad en un portafolio, cada entidad en una sociedad holding o cada proyecto en un pipeline de desarrollo, en una respuesta única y unificada a "¿cuál es el estado de todo el patrimonio ahora mismo?" Este artículo cubre el diseño previsto: qué está planeado que haga `os-orchestration`, qué está diseñado para no hacer deliberadamente, cómo se prevé que funcione la agregación, las funciones comerciales planeadas y cuándo se desplegaría. **Nada de esto está construido todavía** — véase la corrección anterior.

## Qué está diseñado para no hacer

`os-orchestration` está diseñado para no almacenar registros sin procesar — para no tener estado. La intención es que extraiga metadatos de los Toteboxes, sintetice una vista unificada y la presente a través de `os-console`, sin que los datos sin procesar abandonen nunca su Totebox. Bajo este diseño, el agregador solo vería lo que el Totebox tiene permitido exponer.

Se prevé que este límite sea estructuralmente importante: incluso si `os-orchestration` se viera comprometido, los Toteboxes subyacentes permanecerían sellados, ya que el agregador no está pensado para poseer claves a los archivos.

## Dónde está previsto que se sitúe en la línea de productos

| Componente | Rol | Modelo de licencia (previsto) |
|---|---|---|
| `os-console` | Terminal de cara al operador | Código fuente AGPL-3.0-or-later; BETA gratuita actualmente |
| `os-totebox` | Archivo de datos por entidad | FSL-1.1-ALv2, código disponible desde ya; se convierte a Apache-2.0 tras 2 años; BETA gratuita actualmente |
| `os-orchestration` | Agregador de flota (previsto) | Propietario — confirmado hoy vía el archivo `LICENSE` del monorepo, por delante de la propia lógica de agregación |

Se prevé que la línea comercial se trace en el agregador. La Consola y el Totebox están previstos como libres y libremente transferibles. El agregador de Orquestación está planeado como el producto de pago — un operador individual que gestiona una sola entidad nunca lo necesitaría.

## Cómo se prevé que funcione la agregación

La intención de diseño es que `os-orchestration` se conecte a los Toteboxes a través de un protocolo basado en [[capability-based-security|capacidades]] que tunelice a través de TLS estándar en el borde — no hay ningún nombre de protocolo específico comprometido en código hoy. Dentro del túnel, el flujo previsto sería:

1. El agregador enviaría un objeto de capacidad firmado que concede permiso para leer una fila específica de un Totebox específico durante una ventana de tiempo fija.
2. El Totebox verificaría la capacidad, ejecutaría la consulta internamente y emitiría solo el resultado — nunca el registro sin procesar.
3. El agregador combinaría resultados de muchos Toteboxes en una vista única unificada.

Si se construye según lo diseñado, se prevé que el pipeline de promesas y la asignación de memoria de copia cero hagan que la experiencia se sienta local incluso cuando los Toteboxes estén distribuidos en múltiples regiones.

## Las funciones comerciales (previstas)

Se prevé que tres capacidades queden reservadas exclusivamente a `os-orchestration`:

| Función | Qué está previsto que permita |
|---|---|
| Agregación | Leer metadatos de múltiples Toteboxes simultáneamente |
| Multi-tenancy | Servir a múltiples operadores contra la misma flota subyacente |
| Vistas complejas | Paneles entre archivos — resúmenes de portafolio, conciliación entre entidades, resúmenes ejecutivos |

Está previsto que estas funciones permanezcan intencionalmente ausentes del código base abierto de `os-console` — planeadas para vivir en el código base de `os-orchestration` y en ningún otro lugar, una vez construidas.

## La disciplina Diodo (prevista)

El diseño prevé que `os-orchestration` pueda emitir comandos a los Toteboxes que gestiona, sin que los Toteboxes puedan emitir comandos de vuelta. Está previsto que el agregador sea él mismo un sujeto [[diode-standard|Diodo]]: recibiendo comandos solo de `os-console`, nunca de un Totebox. Esto está diseñado para hacer que el movimiento lateral sea estructuralmente imposible — un Totebox comprometido no podría usar el agregador como puente hacia la Consola del operador. El artículo [[totebox-orchestration|Orquestación Totebox]] cubre la gestión del ciclo de vida y el aprovisionamiento de contenedores.

## Cuándo se desplegaría

`os-orchestration` está planeado como un producto comercial para operadores multi-entidad. Los operadores de entidad única que gestionan un Totebox no lo necesitarían. Los operadores multi-entidad — portafolios inmobiliarios, empresas públicas con subsidiarias, oficinas familiares con múltiples tenencias — serían el cliente previsto una vez que la carga cognitiva de ejecutar Consolas separadas contra Toteboxes individuales justifique el agregador.

## Véase también

- [[console-os]] — la distinción entre modo Directo y modo Agregado; os-console se empareja con os-orchestration en modo Agregado
- [[totebox-os]] — los archivos que se están agregando
- [[diode-standard]] — la disciplina de comandos unidireccional que rige el agregador
- [[machine-based-auth]] — cómo los emparejamientos aseguran las conexiones del agregador con los Toteboxes
- [[deployment-patterns]] — cómo os-orchestration aparece en las configuraciones de despliegue comerciales
- [[os-family-overview]] — la familia de ocho SO y cómo encaja os-orchestration
