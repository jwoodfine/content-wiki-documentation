---
schema: foundry-doc-v1
title: "Inferencia sin contenedores"
slug: zero-container-inference
short_description: "La inferencia sin contenedor es el patrón de implementación planeado para cómputo GPU de Tier B utilizando binarios Linux nativos bajo systemd en máquinas virtuales en la nube sin tiempo de ejecución de contenedor, logrando economía viable de SMB a través de temporizadores de apagado inactivo que detienen la facturación de GPU cuando las colas de inferencia están vacías."
category: architecture
status: stub
bcsc_class: forward-looking
last_edited: 2026-04-28
editor: pointsav-engineering
language: es
paired_with: zero-container-inference.md
cites:
 - osc-sn-51-721
---

La inferencia sin contenedores es el patrón de despliegue previsto para el [[yoyo-compute-substrate|cómputo GPU de Nivel B]] de la plataforma: binarios Linux nativos bajo systemd en instancias de máquina virtual de GCE, sin entorno de ejecución de contenedores ni orquestador. La economía funciona porque los temporizadores de apagado en reposo garantizan que la facturación de GPU se detiene exactamente cuando la inferencia no está en ejecución — una ventana diaria de 30 minutos en una A100 de renta interrumpible cuesta aproximadamente 7–8 USD al mes. El conjunto de inferencia de Nivel B que encarna este patrón está previsto; no está en producción actualmente.

## Por qué sin contenedores

Las imágenes OCI implican un registro de contenedores: el registro se convierte en el artefacto duradero, y el operador debe mantener cadenas de construcción de imágenes, credenciales de registro y remediación de CVE para imágenes base. Para una VM de inferencia de uso puntual que arranca, opera 30 minutos y se detiene, la capa de contenedores añade superficie operativa sin resolver ningún problema que el enfoque de máquina virtual no aborde más directamente.

## Qué se usa en su lugar

Un binario nativo en una familia de imágenes GCE `pointsav-public`. Una unidad systemd. OpenTofu para aprovisionamiento y gestión del ciclo de vida de la VM. Un temporizador de apagado en reposo. Pesos del modelo en caché en GCS. Secret Manager para claves de API. nginx para terminación TLS. Controladores CUDA integrados en la imagen GCE en tiempo de construcción.

## Economía SMB

Una instancia A100 80 GB de renta interrumpible cuesta aproximadamente 0,50–0,70 USD por hora en Google Cloud. Una ventana activa diaria de 30 minutos cuesta aproximadamente 7–10 USD al mes. La economía funciona porque el apagado en reposo es la primitiva que soporta el modelo: la instancia está activa exactamente cuando se ejecuta la inferencia, no por conveniencia del operador.

## El único inconveniente honesto: el arranque en frío

Una instancia GPU de GCE desde estado detenido tarda aproximadamente 60–120 segundos en alcanzar el estado listo para inferencia. Para cargas de trabajo en lote nocturnas — el caso de uso principal para el preentrenamiento continuo y la extracción de corpus — el coste del arranque en frío es el precio del cero coste en reposo y es una compensación razonable.

## Lo que se descarta

Plataformas de orquestación de contenedores gestionadas, entornos de ejecución de contenedores, marcos de abstracción multinube, registros de imágenes OCI y cadenas de construcción de contenedores en capas. No se excluyen por ser inferiores en general; se excluyen porque introducen superficie operativa incompatible con el compromiso estructural [[zero-container-runtime]] y el caso económico SMB descrito anteriormente.

## Véase también

- [[zero-container-runtime]] — el compromiso estructural que subyace a este patrón de despliegue
- [[doorman-protocol]] — la ruta de enrutamiento de Nivel B que distribuye al conjunto de inferencia
- [[substrate-without-inference-base-case]] — el sustrato funciona completamente sin Nivel B; la inferencia es aditiva

## Referencias

- [[zero-container-runtime]] — especificación del compromiso de despliegue sin contenedores.
- **Aviso de personal OSC 51-721** — Divulgación de información prospectiva. El conjunto de inferencia de Nivel B y los plazos de despliegue en este artículo son declaraciones prospectivas sujetas a cambios.
