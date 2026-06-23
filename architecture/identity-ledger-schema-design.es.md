---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: identity-ledger-schema-design
title: "Diseño del esquema del registro de identidades"
short_description: "El registro de identidades define tres tipos de registros — Persona, Ancla y Afirmación — que en conjunto representan quién es conocido por el sistema, cómo fue observada esa identidad y qué atributos se han registrado, todo persistido mediante disciplina WORM sin intervención de IA en ninguna etapa."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: identity-ledger-schema-design.md
category: architecture
status: active
quality: complete
last_edited: 2026-06-23
---

El registro de identidades es la primitiva de identidad determinista en el centro de la ingestión de datos en el Anillo 1. Define tres tipos de registros — Persona, Ancla y Afirmación — que en conjunto representan quién es conocido por el sistema, cómo fue observada esa identidad y qué atributos se han registrado sobre ella. Los tres se escriben a través de `service-fs`, produciendo una pista de auditoría inmutable y de solo adición sin intervención de IA en ninguna etapa. Véase también [[worm-ledger-design|el diseño del registro WORM]], [[three-ring-architecture]] y [[machine-based-auth|la autorización basada en máquinas]].

## Puntos clave

- La resolución de identidades es completamente determinista. El identificador primario es un UUIDv5 derivado de la dirección de correo electrónico principal normalizada en minúsculas: el mismo correo siempre produce el mismo UUID en cualquier máquina, en cualquier momento, sin IA ni coincidencia probabilística. Esto satisface el requisito de SYS-ADR-07 de que la extracción en el Anillo 1 no pase por inferencia.
- Los registros de identidad siguen la [[worm-ledger-architecture|disciplina WORM]]. Los tres tipos de registros se escriben a través de `service-fs` como una pista de auditoría de solo adición. Los registros no pueden eliminarse ni modificarse después del hecho.
- Un único registro Persona es la fuente de autoridad para una identidad conocida. Los servicios intermedios resuelven la identidad a partir de este registro: no derivan ni almacenan en caché la suya propia.
- Las identidades ambiguas o en conflicto se exponen al operador del sistema en lugar de fusionarse de forma silenciosa. Extracción determinista en el Anillo 1; resolución humana para las excepciones. Ningún modelo probabilístico realiza fusiones silenciosas durante la ingestión.

## 1. La primitiva de identidad

Cada identidad en el Anillo 1 es un UUID versión 5 derivado de una dirección de correo electrónico normalizada en minúsculas:

```
id = UUIDv5(NAMESPACE_DNS, lowercase(primary_email))
```

Esta derivación es determinista: la misma dirección de correo siempre produce el mismo UUID en cualquier máquina, en cualquier lenguaje, en cualquier momento. No existe semilla aleatoria, clasificación por IA ni consulta a un servicio externo. Dos sistemas que ingieran de forma independiente la misma dirección de correo llegarán al mismo UUID.

Esta propiedad es la base de la garantía de composibilidad de la primitiva de identidad: un UUID producido por `service-people` puede ser referenciado por `service-email`, `service-input` o cualquier componente del Anillo 2 sin necesidad de un registro de identidad compartido. La derivación es el registro.

## 2. El registro Persona

El registro Persona es el objeto de identidad primario. Lo crea la herramienta MCP `identity.append` y se almacena en el `PeopleStore` en proceso de `service-people`, para luego escribirse en `service-fs`.

```
Person {
    id:              UUIDv5(NAMESPACE_DNS, lowercase(primary_email))
    name:            String
    primary_email:   String  // siempre normalizado en minúsculas
    email_aliases:   Vec<String>
    organisation:    Option<String>
    created_at:      DateTime<UTC>  // RFC3339
    updated_at:      DateTime<UTC>  // RFC3339
}
```

El campo `id` siempre se deriva; nunca lo asigna el código llamante. El campo `primary_email` siempre se almacena en minúsculas independientemente de cómo fue suministrado. Estos invariantes se hacen cumplir en `Person::new()`: no existe ningún constructor que los omita.

## 3. El registro Ancla

Un Ancla es una observación inmutable de que una dirección de correo electrónico fue vista en un contexto específico. La produce automáticamente la herramienta MCP `identity.scan_text` cuando se encuentra una coincidencia de la expresión regular de correo en un bloque de texto.

```
Anchor {
    target_uuid:   String  // UUIDv5(NAMESPACE_DNS, lowercase(email))
    anchor_source: String  // la dirección de correo tal como fue observada
    timestamp:     String  // RFC3339
}
```

Un Ancla no afirma que el correo pertenezca a una persona con nombre. Registra la observación de una dirección de correo y deriva el UUID que correspondería a esa dirección. Los Anclas son estrictamente de solo adición: el sistema nunca modifica ni retracta un Ancla una vez escrita.

## 4. El registro Afirmación

Una Afirmación es una observación de atributo con procedencia. La produce `identity.scan_text` junto con cada Ancla, y registra qué atributo fue inferido y desde qué fuente.

```
Claim {
    claim_id:         String  // UUIDv4 — único por invocación
    target_uuid:      String  // la identidad que se anota
    attribute:        String  // p. ej. "email"
    value:            String  // el valor observado
    confidence_score: f32     // 1.0 para verificación por regex; <1.0 reservado para uso futuro
    source_id:        String  // identificador de procedencia suministrado por el llamante
    timestamp:        String  // RFC3339
}
```

El `claim_id` es un UUIDv4 (aleatorio, no derivado): es único por invocación de Afirmación. El `confidence_score` es `1.0` para todas las Afirmaciones producidas por la implementación actual porque el único método de extracción en uso es una expresión regular determinista. Una puntuación inferior a `1.0` está reservada para métodos de extracción futuros que operen bajo las restricciones de SYS-ADR-07.

## 5. Detección de conflictos

Cuando se agrega un registro Persona al `PeopleStore`, el almacén comprueba si algún correo del registro (primario o alias) ya está vinculado a un UUID distinto. En ese caso, el almacén devuelve un error `ConflictingIdentity` en lugar de fusionar o sobrescribir de forma silenciosa.

```
PeopleStoreError::ConflictingIdentity {
    email:       String  // el correo que desencadenó el conflicto
    existing_id: Uuid    // el UUID ya vinculado a ese correo
    new_id:      Uuid    // el UUID que el nuevo registro asignaría
}
```

Los conflictos se exponen al llamante: nunca se resuelven automáticamente. Esto implementa el requisito F12 (SYS-ADR-10): cuando la coincidencia determinista descubre ambigüedad, el sistema la presenta al operador en lugar de resolverla con heurísticas o inferencia de IA.

## 6. Cumplimiento de SYS-ADR-07: cero IA en el Anillo 1

El esquema del registro de identidades está diseñado de forma que cada operación sea determinista y verificable sin estado de modelo:

- La extracción de correos utiliza una única expresión regular compilada (`(?i)[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}`).
- La derivación de UUID emplea el algoritmo UUIDv5 (SHA-1 con un UUID de espacio de nombres fijo — determinista, no aprendido).
- Las puntuaciones de confianza se asignan por regla (`1.0` para coincidencia por regex), no mediante un modelo.
- La detección de conflictos compara UUIDs por igualdad: sin coincidencia difusa, sin similitud por vectores, sin ajuste de umbrales.

No existen pesos de modelo en `service-people`. No se realiza ninguna llamada de red a un punto de inferencia durante la ingestión de identidades. Estas son restricciones irrevocables de SYS-ADR-07, no preferencias de implementación.

## 7. Persistencia WORM

Los tres tipos de registros — Persona, Ancla y Afirmación — se persisten escribiendo a través de `service-fs` mediante `FsClient`. La ruta de escritura utiliza:

- HTTP POST a `/v1/append` en la instancia de service-fs
- Cabecera `X-Foundry-Module-ID` establecida al valor de `PEOPLE_MODULE_ID` (variable de entorno, p. ej. `foundry-workspace`)
- Cuerpo de registro serializado en JSON

Cada observación de identidad se escribe en el registro WORM en el momento de la ingestión. Los registros no pueden eliminarse ni modificarse después del hecho. La garantía de solo adición proviene de la disciplina de escritura atómica D4 de service-fs y de la cadena hash SHA-256 lineal.

Existen tres rutas de escritura:

1. `identity.append` (herramienta MCP) — escribe un registro Persona
2. `identity.scan_text` (herramienta MCP) — escribe un Ancla y una o más Afirmaciones por cada dirección de correo encontrada en el texto de entrada
3. No existe ruta de escritura directa para Ancla o Afirmación de forma aislada: siempre se producen como par mediante `scan_text`

## 8. Perspectiva: extensión de identidad en el Anillo 2

El esquema descrito anteriormente es la base determinista del Anillo 1. Las extensiones planificadas para el Anillo 2 incluyen:

- **Compartición de identidades entre dominios** — una interfaz de consulta prevista para buscar identidades entre límites de módulo, destinada a componentes del Anillo 2 como `service-extraction` que necesitan correlacionar entidades observadas en distintos contextos de ingestión.
- **Coincidencia difusa basada en vectores** — una capa de similitud opcional, prevista para ejecutarse en el Anillo 2, que puede sugerir fusiones candidatas de identidades para revisión del operador. Está condicionada por SYS-ADR-07: cualquier sugerencia basada en inferencia debe presentarse al operador para su confirmación; no puede escribir en el registro WORM del Anillo 1 sin una acción explícita del operador.

Estas extensiones son planificadas e intencionadas; no están presentes en la implementación actual.

## Véase también

- [[machine-based-auth]]
- [[capability-based-security]]
- [[worm-ledger-design]]
- [[cryptographic-ledgers]]
- [[service-people]]
