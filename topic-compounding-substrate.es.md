# El sustrato compuesto (resumen)

El patrón arquitectónico que PointSav construye y administra.
Cinco propiedades estructurales se combinan para producir un
sustrato donde cada interacción operativa genera señal de
entrenamiento que se compone a través de los despliegues — y
cada propiedad nombra una razón específica por la que la IA
gestionada por hiperescaladores no puede igualarla
estructuralmente.

## Definición

Un sustrato compuesto es una arquitectura donde:

1. El código del sustrato es abierto y bifurcable.
2. La capa de datos determinista funciona independientemente
   de cualquier cómputo de IA.
3. La IA se añade como **Capa de Inteligencia Opcional** que
   cualquier inquilino puede componer adentro o afuera.
4. Cada interacción operativa genera señal de entrenamiento
   que se compone a través de los despliegues.
5. Un curador (PointSav) integra periódicamente la señal
   acumulada en modelos base mejorados que regresan a todos los
   despliegues sin alterar la soberanía de datos del cliente.

Es el patrón de la Apache Software Foundation combinado con el
modelo de distribución de Red Hat, aplicado al sustrato de IA.

## Cinco propiedades estructurales

| Propiedad | Brecha estructural del hiperescalador |
|---|---|
| **Soberanía del sustrato** — el cliente posee toda la pila | Su negocio es monetizar el sustrato como servicio rentado |
| **Inteligencia opcional** — datos y procesamiento determinista funcionan sin IA | Su producto IA acopla cómputo a servicios de datos |
| **Ruteo multi-nivel de cómputo** — Doorman único entre local / nube-burst / API externa | Cada nivel es una relación de facturación distinta |
| **Composición federada** — agregación que preserva privacidad de adaptadores | Su facturación por inquilino hace ilegal el agrupamiento entre inquilinos |
| **Camino de pre-formación continuada** — base anual curada de la federación | No pueden dejar que datos del cliente entrenen un modelo base que el cliente luego posee |

## La inversión de la cadena de valor

La cadena de valor del hiperescalador depende de que el cliente
permanezca en el sustrato del proveedor. La cadena de valor del
sustrato compuesto depende de que el cliente componga *fuera*
del sustrato del proveedor. Los dos modelos de negocio están
matemáticamente opuestos; uno no puede adoptar el otro sin
desmantelarse.

## Qué es PointSav en este patrón

No es proveedor. No es guardián. **Administrador.**

Administrador del protocolo, administrador del modelo base,
administrador del mercado, operador de registro (vende
appliances con integración y soporte), cliente de referencia
(el propio Foundry y Woodfine — prueba de que el patrón
funciona).

El sustrato se vuelve patrimonio común abierto; el valor migra
hacia operaciones, integración, y el mercado de bibliotecas de
LoRA.

## El premio 2030

El patrón apunta a producir una federación de cien-y-más
clientes, cada uno con su pila completa, cada uno
contribuyendo al patrimonio común y beneficiándose de él. No
desplaza a los hiperescaladores en volumen — captura el
mercado PYME regulado que los hiperescaladores no pueden
alcanzar económicamente.

## Véase también

- [Documento canónico en inglés](topic-compounding-substrate.md)
- [El sustrato de aprendizaje](topic-apprenticeship-substrate.md)
- [El modelo de contribuyentes en tres niveles](topic-contributor-model.md)
- [El sustrato de protocolo de lenguaje](topic-language-protocol-substrate.md)
- [Hospedaje por el cliente](topic-customer-hostability.md)

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.