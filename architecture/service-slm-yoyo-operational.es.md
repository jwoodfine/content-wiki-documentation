---
schema: foundry-doc-v1
title: "service-SLM y Yo-Yo — Estado Operativo"
slug: service-slm-yoyo-operational.es
category: architecture
type: topic
quality: complete
short_description: "Visión general del enrutador de inferencia de tres niveles de service-SLM y la instancia GPU de explosión Yo-Yo, incluyendo el límite de costo y el techo de gastos mensuales."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - olmo3-allenai
paired_with: service-slm-yoyo-operational.md
---

**service-SLM** es el componente Ring 3 de Foundry: la capa de Inteligencia Opcional (Doctrine claim #16). Actúa como enrutador de inferencia de tres niveles, dirigiendo el trabajo de rutina — ediciones editoriales, traducción bilingüe, generación de salida estructurada — hacia el modelo apropiado sin necesidad de enviar datos a una API de terceros. Los anillos 1 y 2 (ingesta de límites y procesamiento de conocimiento) funcionan de forma completa sin él; Ring 3 es estructuralmente opcional.

El **Yo-Yo** es la instancia GPU de explosión a demanda de Foundry: una máquina virtual en GCE que ejecuta un modelo de 32 mil millones de parámetros a aproximadamente 50-100 tokens por segundo. Se inicia bajo demanda y se apaga automáticamente tras 30 minutos de inactividad.

## Arquitectura de tres niveles

El sistema define tres niveles de cómputo, enrutados por el Doorman:

- **Tier A — local**: `llama-server` ejecutando `OLMo-3-1125-7B-Think-Q4_K_M.gguf` en la CPU de la VM de trabajo (`e2-standard-4`). Siempre disponible. Rendimiento: aproximadamente 2-3 tokens por segundo. Suficiente para tareas cortas; insuficiente para trabajo editorial a escala.
- **Tier B — Yo-Yo**: `llama-server` con soporte CUDA en `yoyo-tier-b-1` (`g2-standard-4`, GPU NVIDIA L4 de 24 GB), ejecutando `OLMo-2-0325-32B-Instruct-Q4_K_S.gguf`. Rendimiento: aproximadamente 50-100 tokens por segundo. A demanda, no spot.
- **Tier C — API externa**: configurado para uso futuro; sin claves activas en el espacio de trabajo v0.1.91.

## El límite del Doorman

Todas las solicitudes de inferencia pasan por el Doorman antes de llegar a cualquier nivel. El Doorman es un binario Rust (`local-doorman.service`) vinculado a `127.0.0.1:9080`. Sus responsabilidades:

- Retener todas las claves API (tokens de Tier C y el token bearer de Tier B). Las claves no existen en ningún otro punto de la ruta de solicitud.
- Enrutar solicitudes al nivel correcto según heurísticas de complejidad (tamaño de la solicitud, requisitos de salida estructurada).
- Registrar cada tránsito en el libro de auditoría por inquilino (`/var/lib/local-doorman/audit/<tenant>/<YYYY-MM>.jsonl`).
- Drenar la cola de borradores de aprendizaje §7C (`data/apprenticeship/queue/`).

## Cola de aprendizaje (§7C)

Cada confirmación en el espacio de trabajo activa el gancho `bin/capture-edit.py`, que escribe un borrador de aprendizaje en `data/apprenticeship/queue/`. El trabajador de drenaje del Doorman sondea la cola cada 30 segundos, envía el borrador al nivel apropiado (Tier A por defecto; Tier B cuando el borrador supera `SLM_BRIEF_TIER_B_THRESHOLD_CHARS=500` caracteres) y registra el resultado en el corpus de entrenamiento. La cola es durable: acumula trabajos mientras el Yo-Yo está detenido y los procesa cuando se reinicia.

## Techo de costos — monitor de inactividad

La VM Yo-Yo cuesta aproximadamente $0.71 USD por hora en funcionamiento. El monitor de inactividad (`bin/yoyo-idle-monitor.sh`, programado cada cinco minutos) sondea el endpoint `/slots` del Yo-Yo. Tras 30 minutos consecutivos sin inferencias activas, el monitor llama a `gcloud compute instances stop yoyo-tier-b-1`.

Con una utilización típica de desarrollo de aproximadamente el 25 por ciento, el techo de apagado por inactividad reduce el gasto mensual a aproximadamente $130-150 USD. Los clientes que replican este patrón operan bajo la misma economía.

## Convención SERVICE-SLM-PROPOSAL

El sistema de Tasks en clústeres identifica trabajo de rutina que service-SLM puede manejar y lo propone mediante el buzón de salida. Master agrupa las propuestas en la cola de aprendizaje; service-SLM produce intentos; los veredictos senior firman las salidas de calidad en el corpus DPO. Las decisiones arquitectónicas, el diseño original y la coordinación entre capas permanecen fuera del alcance de service-SLM.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
