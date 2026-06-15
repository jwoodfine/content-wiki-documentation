---
schema: foundry-doc-v1
title: "Cómo escalar los niveles de acceso de usuario"
slug: scale-user-tiers
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: scale-user-tiers.md
---

Los niveles de acceso de usuario determinan qué operaciones de la plataforma puede realizar una sesión. A medida que crece un despliegue, el administrador necesita promover a los usuarios desde el acceso de solo lectura (`READ`) al acceso de sesión estándar (`USER`) o al acceso completo de operador (`INPUT`). Esta guía cubre la identificación de las asignaciones de nivel actuales, la promoción de usuarios individuales y la actualización masiva de un conjunto de usuarios a medida que un equipo crece.

Para el modelo de autorización que define los niveles, véase [[machine-based-auth]]. Para emitir los tokens que codifican las asignaciones de nivel, véase [[issue-capability-token]].

## Requisitos previos

- Acceso de administrador al servicio de emisión de tokens
- Una lista de usuarios a promover con sus claves públicas actuales o identificadores de dispositivo
- Un espacio de nombres de tenant ya configurado (véase [[configure-tenant-namespace]])

## Los tres niveles de acceso

| Nivel | Valor de alcance | Caso de uso típico |
|---|---|---|
| `READ` | read | Socios externos, revisores de auditoría, consumidores de datos |
| `USER` | user | Miembros del equipo principal; consultas al DataGraph, inferencia SLM, lecturas wiki |
| `INPUT` | input | Operadores de la plataforma; escrituras en el libro mayor WORM, Máquina de Entrada F12, acceso completo a la consola |

Promueva a los usuarios al nivel mínimo que requiere su rol. Las sesiones con privilegios excesivos crean una superficie de auditoría innecesaria.

## Paso 1: Listar las asignaciones de nivel actuales

Consulte los tokens activos del tenant para ver las asignaciones de nivel actuales:

```
curl -s "http://<host-servicio-emisión>:<puerto>/v1/tenants/<tenant-id>/tokens" \
  -H "Authorization: Bearer <token-admin>"
```

La respuesta lista los tokens activos con sus campos `scope`, `subject_pubkey` y `expires_at`. Tome nota de qué usuarios están en el alcance `READ` o `USER` si necesitan promoción a `INPUT`.

## Paso 2: Promover a un usuario individual

Para promover a un usuario, emita un nuevo token con el alcance más alto. El token antiguo sigue siendo válido hasta que vence o es revocado explícitamente — no hay actualización en su lugar.

Emita un nuevo token:

```
curl -X POST http://<host-servicio-emisión>:<puerto>/v1/tokens \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<clave-publica-usuario>",
    "scope": "input",
    "tenant_id": "<tenant-id>",
    "expires_in_seconds": 86400
  }'
```

Entregue el nuevo token al usuario. Una vez que lo cargue, su sesión de consola adquiere el nuevo nivel.

## Paso 3: Revocar el token de nivel inferior antiguo

Después de que el usuario confirme que el nuevo token funciona, revoque el token de nivel inferior antiguo para cerrar la ventana de transición:

```
curl -X DELETE http://<host-servicio-emisión>:<puerto>/v1/tokens/<id-token-antiguo> \
  -H "Authorization: Bearer <token-admin>"
```

Revocar el token antiguo garantiza que no haya credenciales simultáneas READ e INPUT para el mismo dispositivo — una sola sesión tiene exactamente un nivel en cualquier momento.

## Paso 4: Actualización masiva de un equipo

Para promociones a escala de equipo, prepare una lista de claves públicas y emita tokens en secuencia. Un bucle de shell simple sobre un archivo JSON de claves públicas funciona:

```
while IFS= read -r pubkey; do
  curl -X POST http://<host-servicio-emisión>:<puerto>/v1/tokens \
    -H "Authorization: Bearer <token-admin>" \
    -H "Content-Type: application/json" \
    -d "{\"subject_pubkey\": \"$pubkey\", \"scope\": \"user\", \"tenant_id\": \"<tenant-id>\", \"expires_in_seconds\": 86400}"
done < pubkeys.txt
```

Registre cada ID de token emitido. Después de que el equipo confirme que sus nuevos tokens funcionan, ejecute un bucle de revocación correspondiente sobre los IDs de token antiguos.

## Puntos clave

- Las promociones de nivel requieren emitir un nuevo token; los tokens existentes no pueden actualizarse en su lugar
- Mantenga la ventana de transición corta — revoque el token antiguo después de que el usuario confirme que el nuevo funciona
- Las sesiones con privilegios excesivos aumentan la superficie de auditoría; emita el nivel mínimo para cada rol
- Se crean entradas en el libro mayor WORM para cada emisión y revocación de token — los cambios de nivel son permanentemente auditables

## Véase también

- [[machine-based-auth]] — el modelo de autorización que define lo que permite cada nivel
- [[issue-capability-token]] — pasos detallados para emitir un solo token de capacidad
- [[rotate-keys]] — reemplazar un token al vencer o tras una posible compromisión
- [[configure-tenant-namespace]] — configurar el espacio de nombres antes de que se asignen los niveles de usuario
- [[verify-worm-ledger]] — confirmar los eventos de emisión de tokens en el libro mayor de auditoría
