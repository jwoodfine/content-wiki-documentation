---
schema: foundry-doc-v1
title: "Autorización Basada en Hardware"
slug: machine-based-auth
category: architecture
type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: machine-based-auth.md
cites: []
---

La autorización basada en hardware reemplaza las estructuras de nombre de usuario y contraseña por un modelo en el que la autorización requiere el emparejamiento criptográfico del hardware físico, verificado por el gestor de capacidades.

## El problema de las credenciales

La autenticación convencional depende de secretos compartidos: el usuario conoce una contraseña y el servidor la verifica contra un hash almacenado. Este modelo crea una superficie de ataque persistente — las contraseñas pueden filtrarse, adivinarse, interceptarse o extraerse mediante técnicas de ingeniería social que eluden la seguridad técnica de la plataforma.

La autorización basada en hardware desplaza el anclaje de confianza de "algo que el usuario sabe" a "algo que el hardware posee y puede demostrar criptográficamente".

## Cómo funciona

En la plataforma PointSav, el emparejamiento criptográfico es gestionado por la capa de seguridad basada en capacidades. Cada dispositivo autorizado posee un par de claves generado en el momento del aprovisionamiento; la clave privada nunca sale del dispositivo. Cuando el dispositivo solicita una concesión de capacidad a la plataforma, presenta una prueba criptográfica de posesión de esa clave. El gestor de capacidades verifica la prueba y emite tokens de capacidad apropiados para el rol declarado del dispositivo.

## Eliminación de ataques de phishing

Una sesión no puede establecerse desde hardware que no haya completado el emparejamiento criptográfico, independientemente de las credenciales que un atacante pueda haber obtenido. La clase completa de ataques de robo remoto de credenciales queda estructuralmente eliminada.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
