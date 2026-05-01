# Hospedaje por el cliente — *We Own It* (resumen)

La disciplina de hospedaje por el cliente en Foundry es el
compromiso arquitectónico de que cada artefacto que un cliente
adopta puede ejecutarse sobre metal del cliente, con datos del
cliente, contra llaves del cliente, con un libro de auditoría
del cliente. El cliente puede bifurcarlo desde el día uno.

No es un nivel de precios ni una opción de despliegue. Es la
forma del sustrato. Una versión de Foundry que requiera
infraestructura alojada por el proveedor para funcionar no es,
por construcción, Foundry.

## Tres compromisos concretos

1. **Bootstrap auto-hospedable.** Cada servicio Foundry envía un
   `bootstrap.sh` que levanta el servicio en la máquina propia
   del cliente — sin dependencia SaaS, sin login con proveedor,
   sin API medida.
2. **Adaptadores por inquilino en el sistema de archivos del
   cliente.** Cuando el adaptador del cliente entrena sobre el
   corpus del cliente, el `.lora` resultante vive en
   `data/adapters/` dentro del sustrato del cliente.
3. **Libro de auditoría anclado en el cliente.** El corpus de
   aprendizaje vive en `data/training-corpus/apprenticeship/`
   dentro del sustrato del cliente. Los registros privados de
   inquilino nunca salen, según Doctrine §IV.b.

## Por qué los hiperescaladores no pueden replicar esto

Su economía unitaria depende de entrenamiento central, raíces
de confianza compartidas y atestación anclada en el proveedor.
La pre-formación continuada por cliente no calza a escala PYME
con esa economía. Foundry está construido para que la postura
regulatoria del cliente no dependa de la del proveedor.

## Qué no es el hospedaje por el cliente

- No es licencia de código abierto permisiva. Una licencia
  permisiva sobre un servicio que requiere plano de control
  alojado no satisface el hospedaje por el cliente.
- No es "el proveedor lo aloja por ti". El alojamiento por
  proveedor es una opción operativa, no la forma canónica.
- No es exportación de datos. El hospedaje por el cliente es
  estructural — los datos ya están en el metal del cliente
  desde el momento en que se escribieron.

## Prueba operativa

Un servicio Foundry nuevo es hospedable por el cliente si éste
puede clonar los repositorios, ejecutar `bootstrap.sh` en una
máquina propia, generar y servir adaptadores desde disco local,
operar el servicio sin contactar nunca un endpoint del
proveedor, y auditar cada petición, respuesta y actualización
de adaptador localmente.

## Véase también

- [Documento canónico en inglés](topic-customer-hostability.md)
- [El sustrato de protocolo de lenguaje](topic-language-protocol-substrate.md)
- [Disciplina anti-homogenización](topic-anti-homogenization-discipline.md)

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.