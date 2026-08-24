---
schema: foundry-doc-v1
title: "Estado operativo de SLM y Yo-Yo"
slug: service-slm-yoyo-operational
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-3-ai-gateway
short_description: "Cómo operan el enrutador de inferencia de tres niveles de service-slm y la VM de ráfaga GPU Yo-Yo: el límite del Doorman, los niveles local y de ráfaga, la cola de aprendizaje, y el techo de costo por apagado en inactividad."
status: active
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
 - olmo3-allenai
paired_with: service-slm-yoyo-operational.md
---

`service-slm` es el componente [[three-ring-architecture|Ring 3]] de la plataforma — la capa
de inteligencia opcional. Es un enrutador de inferencia por niveles que los clústeres y
colaboradores usan para delegar trabajo rutinario: pulido editorial, ediciones mecánicas
conformes a esquema, borradores de traducción bilingüe, y generación de salida estructurada.
El trabajo se maneja localmente o en una VM de ráfaga GPU dedicada, sin enrutarse a una API de
terceros por defecto. Los Rings 1 y 2 (ingesta de límite y procesamiento de conocimiento)
funcionan completamente sin él — el Ring 3 es estructuralmente opcional.

**Yo-Yo** es la instancia GPU de ráfaga bajo demanda de la plataforma — una VM de GCE que
ejecuta un modelo más grande del que puede manejar el nivel local, se inicia bajo demanda, y
se apaga tras un período de inactividad. Existe un tercer nivel (API externa) en la
configuración de enrutamiento, pero no se usa en la operación normal, reservado para los
casos que genuinamente lo requieren.

## El límite del Doorman

Cada solicitud de inferencia cruza el [[doorman-protocol|Doorman]] antes de llegar a un nivel
de modelo. El Doorman no se ejecuta como proceso propio independiente — está empaquetado
junto con service-content dentro de un único servicio (`local-totebox.service`). Sus
responsabilidades cubren todo el ciclo de vida de la solicitud: mantener cada clave de API
para que ninguna clave se disperse entre sitios de llamada, enrutar solicitudes al nivel
correcto según complejidad, anexar cada tránsito a un libro de auditoría por inquilino, y
drenar la cola de aprendizaje descrita más abajo.

## Nivel local — siempre disponible

El nivel local ejecuta `llama-server` (el servidor HTTP en C++ de llama.cpp) en la propia CPU
de la VM de espacio de trabajo. El modelo cargado es una compilación cuantizada de OLMo 3 7B
**Instruct** — la variante de instrucción, no la variante de razonamiento "Think". El
rendimiento en una VM solo-CPU es del orden de unos pocos tokens por
segundo — suficiente para briefs cortos y completaciones triviales, no para trabajo editorial
rutinario a escala. Este techo de latencia es lo que motivó el nivel de ráfaga a continuación.

## Nivel Yo-Yo — ráfaga GPU

La instancia Yo-Yo ejecuta `llama-server` con soporte GPU en una instancia GCE separada en
`us-central1-a`, con hardware con una GPU NVIDIA L4 (24 GB de VRAM), aprovisionada bajo
demanda en lugar de como instancia spot — la capacidad spot para esta clase de GPU resultó
poco confiable en múltiples zonas de EE.UU. durante el arranque inicial. El modelo es un
modelo OLMo 3 más grande ajustado para razonamiento más profundo. El acceso de red al puerto
de inferencia de la instancia está restringido por regla de firewall a la dirección interna
de la VM de espacio de trabajo únicamente, y cada solicitud se autentica con un token
portador que mantiene el Doorman.

**Actualmente caído.** Al momento de escribir esto, la verificación de salud en vivo del
Doorman reporta el circuito del nivel Yo-Yo abierto en las tres etiquetas configuradas,
debido a fallos sostenidos en la sonda de salud — este nivel no ha estado sirviendo
solicitudes durante un período extendido. Las solicitudes que se enrutarían aquí actualmente
retroceden o se encolan en lugar de completarse en este nivel; este es un hecho operativo en
vivo, no una descripción de diseño.

### Aprovisionamiento

Una instancia Yo-Yo nueva se construye desde un script de inicio que cubre instalación de
paquetes, una compilación de toolkit CUDA y `llama-server` desde código fuente, descarga del
modelo, generación de token portador, y configuración de unidad systemd — un proceso
documentado de múltiples pasos cuyo historial de iteración (discrepancias de versión de
controlador/kernel, límites de memoria de compilación, confiabilidad de descarga) se preserva
en los propios comentarios inline del script y en el registro de cambios del espacio de
trabajo.

## La cola de briefs de aprendizaje

Cada commit dispara un gancho de captura que escribe una tupla de corpus de ingeniería y un
brief sombra en una cola durable. El trabajador de drenaje del Doorman sondea esta cola,
despacha cada brief al nivel local por defecto (o al nivel de ráfaga por encima de un umbral
de tamaño), y al completarse escribe una tupla de corpus en la etapa de revisión. Este
mecanismo es durable a través de ventanas de apagado por inactividad de Yo-Yo, reinicios del
Doorman, y tiempos de espera del aprendiz — la cola se acumula mientras el nivel de ráfaga
está detenido, y el backlog se drena sin pérdida una vez que se reinicia. Al momento de
escribir esto, la cola en vivo reporta varios miles de entradas pendientes y un conteo
envenenado (fallido y en cuarentena) grande en relación con las completadas — merece una
mirada dedicada de quien sea responsable de esta canalización, no algo que este artículo
resuelva.

## Techo de costo — el monitor de apagado por inactividad

Un monitor de apagado por inactividad sondea la VM Yo-Yo en busca de actividad de inferencia
activa en un horario regular, y detiene la instancia tras un período sostenido sin ninguna,
evitando que el costo de GPU siempre-encendida aplique al tiempo inactivo. El monitor se
ejecuta desde la VM de espacio de trabajo en lugar de la propia VM Yo-Yo, ya que la cuenta de
servicio de la VM de espacio de trabajo mantiene los permisos de nube necesarios para detener
una instancia y la de la VM Yo-Yo no.

## Qué se ejecuta en el nivel de ráfaga

El flujo de trabajo de ingeniería de la plataforma enruta aquí el trabajo rutinario:
actualizaciones mecánicas de documentación, ediciones conformes a esquema, refactorizaciones
basadas en patrones, borradores de traducción bilingüe, informes de estado rutinarios, y
código repetitivo. Las decisiones arquitectónicas, el diseño novedoso, y la coordinación
entre capas se enrutan en cambio a un nivel de modelo de frontera. `service-slm` es el
multiplicador para el trabajo rutinario; el modelo de frontera se reserva para los juicios.

## Véase también

- [[compounding-substrate]] — el patrón arquitectónico que esto implementa
- [[service-slm]] — la visión general de enrutamiento por niveles de service-slm
- [[apprenticeship-substrate]] — cómo se acumula la señal de entrenamiento a partir de tuplas de corpus operativas
- [[brief-queue-substrate]] — la cola durable que conecta la cola de briefs con el procesamiento por niveles
- [[worm-ledger-architecture]] — el libro de auditoría que registra cada llamada externa

## Referencias

1. Capa de Inteligencia Opcional — el Ring 3 es estructuralmente opcional; los Rings 1 y 2 funcionan sin él.
2. Familia de modelos OLMo 3 de AllenAI. Apache 2.0 (pesos del modelo); Open Data Commons (datos de entrenamiento). [olmo3-allenai] https://huggingface.co/allenai
3. NI 51-102 Obligaciones de Divulgación Continua. British Columbia Securities Commission. [ni-51-102] https://www.bcsc.bc.ca/securities-law/law-and-policy/instruments-and-policies/5-ongoing-requirements-for-issuers-insiders/current/51-102
4. CSA National Policy 51-201 Divulgación de Información Prospectiva. Ontario Securities Commission. [np-51-201] https://www.osc.ca/en/securities-law/instruments-rules-policies/5/51-721/osc-staff-notice-51-721-forward-looking-information-disclosure
