<div align="center">

# PointSav — Wiki de Documentación Técnica
### *La Biblioteca de Ingeniería de la Plataforma PointSav*

<br/>

**[→ Monorepo de Ingeniería](https://github.com/pointsav/pointsav-monorepo)** &nbsp;·&nbsp; **[→ Sistema de Diseño](https://github.com/pointsav/pointsav-design-system)** &nbsp;·&nbsp; **[→ pointsav.com](https://pointsav.com)**

</div>

---

## Sobre Este Repositorio

Esta es la biblioteca técnica de la plataforma PointSav. Contiene Registros de Decisiones de Arquitectura, especificaciones de servicios, guías operativas y el glosario de la plataforma. Donde el monorepo de ingeniería contiene el código, este repositorio contiene el razonamiento detrás de él.

El lector objetivo es cualquiera que necesite entender no solo qué hace la plataforma, sino por qué se tomaron decisiones arquitectónicas específicas — auditores, nuevos colaboradores, socios institucionales y revisores de diligencia debida técnica.

---

## Registros de Decisiones de Arquitectura

Los ADR son compromisos formales con decisiones de diseño específicas. No son propuestas — representan decisiones ya tomadas, implementadas y vinculantes para todo desarrollo futuro.

**Cumplimiento y Arquitectura de Datos**

`SYS-ADR-06.yaml` — Por qué el archivo de cumplimiento y la capa de inteligencia son dos sistemas físicamente separados, y por qué consultar uno para el propósito del otro produce resultados incorrectos.

`SYS-ADR-07.yaml` — Por qué los datos estructurados (CSV, JSON, hojas de cálculo) tienen prohibido enrutarse a través del procesamiento de IA, y por qué todos los archivos compuestos entrantes deben almacenarse antes de aplicar cualquier lógica de extracción.

`SYS-ADR-10.yaml` — Por qué F12 es el punto de control humano obligatorio para el ingreso de todos los activos base y por qué no existe una ruta de importación masiva que lo evite.

**Arquitectura de Seguridad**

`SYS-ADR-13.yaml` — Por qué el nodo de enrutamiento maestro y sus claves criptográficas residen en hardware físico que el ejecutivo controla, en lugar de en infraestructura de nube.

`SYS-ADR-19.yaml` — Por qué la publicación automatizada de IA en registros verificados está prohibida, y el modelo de Verificación Airgap (Git para el Conocimiento) que lo aplica.

**Arquitectura de Interfaz de Usuario**

`SYS-ADR-11.yaml` — Por qué ConsoleOS está dividido en un Chasis sin estado y Cartuchos aislados, y por qué cada función de tecla F es una unidad desplegable de forma independiente.

`SYS-ADR-17.yaml` — La Arquitectura Derivada: Activos Base, Primera Derivada y Tercera Derivada — y por qué estas tres capas nunca deben confundirse.

---

## Especificaciones de Servicios

`topic-service-slm.md` — Cómo el Pasarela de IA opera en dos roles simultáneos: ejecución local puntual y el protocolo portero que evita que los registros corporativos lleguen a modelos de IA externos.

`topic-service-people.md` — Cómo funciona el libro mayor de personal como máquina de estado de archivos planos, el flujo de trabajo del Inspector de Verificación y el diseño del límite de verificación diaria.

`topic-service-search.md` — Cómo el índice invertido basado en Tantivy proporciona búsqueda de texto completo sin un motor de base de datos en ejecución, y qué requiere el cumplimiento DARP.

`topic-ppn-topology.md` — La arquitectura de la Red Privada PointSav, el diseño de la malla WireGuard y el modelo de Autoridad de Comando.

---

## Glosarios

| Glosario | Contenido |
|:---|:---|
| `glossary-corporate.csv` | Terminología financiera y de inversión — Soluciones de Tenencia Directa, estructuras LP, entidades en cuatro jurisdicciones, términos de cumplimiento |
| `glossary-projects.csv` | Bienes raíces y arquitectura física — tipologías de edificios, estrategia de coubicación, certificaciones de sostenibilidad |
| `glossary-documentation.csv` | Plataforma y tecnología — todos los tipos de SO, servicios, prefijos de despliegue, variantes de ConsoleOS |

---

*© 2026 PointSav Digital Systems™. Todos los derechos reservados.*

*→ English version: [README.md](./README.md)*
