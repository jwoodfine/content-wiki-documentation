---
schema: foundry-doc-v1
title: "Cómo vincular un nuevo dispositivo"
slug: pair-a-new-device
category: how-to
content_type: how-to
type: how-to
status: active
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: pair-a-new-device.md
---

Vincular un dispositivo lo registra con la plataforma mediante autorización basada en hardware — un protocolo de enlace criptográfico que asocia el acceso a tu hardware en lugar de a un nombre de usuario y contraseña. Una vez vinculado, el dispositivo posee las claves necesarias para establecer conexiones. Un dispositivo sin vinculación no tiene ningún camino hacia los recursos protegidos — no es acceso denegado, sino estructuralmente inalcanzable.

Para la teoría detrás de este modelo, consulta [[machine-based-auth|autorización basada en máquinas]] y [[pairing-as-permission|vinculación como permiso]].

## Requisitos previos

- Una cuenta de PointSav con al menos acceso P3 (consulta [[personnel-permissions]])
- La aplicación `os-console` instalada en el dispositivo que vas a vincular
- Acceso de red al punto de conexión Command asignado a tu cuenta

## Pasos

### 1. Abre la solicitud de vinculación desde os-console

Inicia `os-console` en el nuevo dispositivo y navega a **Configuración → Dispositivos → Vincular este dispositivo**. La consola genera un código de vinculación temporal — una cadena corta y legible por humanos que es válida durante 10 minutos.

### 2. Aprueba la vinculación desde un dispositivo de confianza

En un dispositivo ya vinculado a tu cuenta (tu máquina diaria de nivel INPUT), abre `os-console` y navega a **Configuración → Dispositivos → Vinculaciones pendientes**. Aquí aparecen el código de vinculación y la huella de hardware del nuevo dispositivo.

Verifica que la huella mostrada en el nuevo dispositivo coincida con la que aparece en tu dispositivo de confianza antes de aprobar. Esta verificación cruzada impide que un dispositivo no autorizado se inserte en tu cuenta.

### 3. Selecciona el tipo de vinculación

Elige el nivel de acceso para el nuevo dispositivo:

| Nivel | Qué puede hacer |
|---|---|
| INPUT | Acceso completo de lectura/escritura a tus archivos y datos — úsalo en tu máquina diaria |
| USER | Acceso de solo lectura — úsalo en dispositivos compartidos o secundarios |
| INTERFACE | Solo metadatos — úsalo para integraciones de orquestación y monitoreo |

Las vinculaciones ADMIN requieren la aprobación del administrador del sistema y no pueden auto-emitirse.

### 4. Confirma y completa

Aprueba la vinculación desde tu dispositivo de confianza. El `os-console` del nuevo dispositivo se actualiza automáticamente y la sesión Totebox queda disponible. El evento de vinculación se registra inmediatamente en el libro mayor de auditoría.

## Verifica la vinculación

En el nuevo dispositivo, abre `os-console` y navega a **Configuración → Dispositivos → Este dispositivo**. El estado del dispositivo debería mostrar **Vinculado** con el nivel que seleccionaste y la marca de tiempo del evento de vinculación.

Ejecuta una operación de lectura de prueba en cualquier archivo para confirmar la conectividad.

## Revocar una vinculación

Para eliminar un dispositivo de tu cuenta, navega a **Configuración → Dispositivos** desde cualquier dispositivo vinculado, selecciona el dispositivo objetivo y elige **Revocar**. El dispositivo revocado queda inmediatamente inaccesible a tus recursos — no se requiere cierre de sesión ni espera de TTL.

## Puntos clave

- La vinculación ES el permiso; no hay lista central de control de acceso que actualizar
- Siempre verifica la huella de hardware antes de aprobar una nueva vinculación
- Las vinculaciones INPUT otorgan acceso completo de lectura/escritura — asígnalas a máquinas que controles directamente
- La revocación es inmediata y a nivel de hardware; no se necesita expiración de sesión o token

## Véase también

- [[machine-based-auth]] — cómo funciona la autorización basada en máquinas arquitectónicamente
- [[pairing-as-permission]] — el patrón de capacidad de objeto que implementa la vinculación
- [[personnel-permissions]] — los cuatro niveles de acceso y lo que puede hacer cada uno
- [[open-first-totebox-session]] — abrir una sesión en un dispositivo recién vinculado
