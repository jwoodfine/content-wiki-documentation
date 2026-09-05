---
schema: foundry-doc-v1
title: "Conexión de claves del nivel C"
slug: tier-c-key-wiring
category: infrastructure
index_group: fleet-and-edge-deployment
type: topic
content_type: topic
quality: complete
short_description: El procedimiento operativo para gestionar las claves de API externas en el servicio Doorman — dónde viven las claves, cómo se aprovisionan, cómo rotan y cómo se contiene una brecha.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
paired_with: tier-c-key-wiring.md
---

El Nivel C de la [[service-slm-operationalization-plan|arquitectura de enrutamiento de cómputo de PointSav]] enruta las solicitudes asistidas por inteligencia artificial a proveedores externos de modelos de lenguaje a través de HTTPS. El servicio [[doorman-protocol|Doorman]] es el único componente del marco que conserva las claves de API de los proveedores. Este artículo describe la forma operativa de la gestión de claves del Nivel C: dónde se almacenan las claves, cómo se aprovisionan y rotan, cómo se auditan el costo y el uso, y cómo se contiene un compromiso sospechado.

El principio universal es que las claves de API viven únicamente en el portal — nunca en el código de la aplicación, nunca en archivos rastreados por control de versiones y nunca en registros o entradas de auditoría. Este artículo es la contraparte operativa de ese principio.

## Dónde viven las claves

Las claves de API de los proveedores se conservan juntas en un único archivo de entorno gestionado por el operador en el host del portal, cargado mediante una sola directiva de anulación de archivo de entorno aplicada a toda la unidad del Doorman — las claves de los proveedores admitidos viven todas en ese único archivo, no en archivos de extensión separados por proveedor. Rotar la clave de un proveedor significa editar ese archivo compartido y recargar el servicio; no está aislado de la configuración de los demás proveedores como lo estaría con una extensión real por proveedor.

El archivo de entorno es propiedad de root y solo lo puede leer el usuario del servicio que ejecuta el Doorman. No está rastreado en ningún repositorio de control de versiones, no se incluye en ninguna copia de seguridad que se publique fuera del host, y no aparece en ningún punto del historial de Git.

El binario del Doorman lee las claves de su entorno en el momento de inicio y las conserva en la memoria del proceso. Las claves nunca se escriben en disco por el Doorman, nunca se reflejan en los cuerpos de respuesta y nunca se incluyen en la salida de registro en ningún nivel. Las entradas del registro de auditoría dejan constancia del nombre del proveedor, no de ninguna parte de la clave.

Un endurecimiento futuro de esta postura, previsto para un hito posterior, sustituirá el archivo de entorno en texto plano por un archivo cifrado que el Doorman descifra en su entorno de ejecución mediante una clave de descifrado en poder del operador que nunca está presente en el host en texto plano. El enfoque actual es la base operativa hasta que ese hito llegue.

## Aprovisionamiento de una clave

Activar una nueva clave de proveedor requiere la presencia del operador en cada paso que toca el valor de la clave, siguiendo un procedimiento interno documentado en lugar de un proceso improvisado. En resumen: la clave se obtiene de la consola del proveedor, se maneja de forma temporal solo con permisos restringidos, se escribe en el archivo de entorno compartido, y el servicio se recarga y se verifica para confirmar que la nueva configuración surtió efecto. Una llamada de prueba de bajo costo confirma que la clave enruta correctamente y produce la entrada esperada en el registro de auditoría antes de eliminar de forma segura los artefactos del manejo temporal. La propia activación se registra en un registro operativo interno — nombre del proveedor, fecha, y una referencia a la entrada correspondiente del registro de auditoría — pero el valor de la clave nunca aparece en ese registro ni en ningún mensaje de commit.

## Rotación

La rotación trimestral por proveedor es el ritmo predeterminado, alineado con los trimestres del calendario. El procedimiento genera una nueva clave en la consola del proveedor mientras la clave anterior sigue activa, sustituye la línea de esa clave en el archivo de entorno compartido, recarga el servicio, verifica el funcionamiento, y conserva la clave anterior en el lado del proveedor durante una breve ventana de solapamiento por si se necesita revertir. Un marcador de evento de rotación en el registro de auditoría delimita el uso previo y posterior a la rotación, lo que respalda la investigación posterior a un incidente.

La rotación acelerada es apropiada cuando se sospecha un compromiso (véase la sección de respuesta a brechas), cuando el proveedor exige rotación en su propio calendario, o cuando el operador elige un ritmo más frecuente para un despliegue de alto volumen.

## Especificidades operativas por proveedor

El Doorman admite tres proveedores externos desde el despliegue inicial: Anthropic Claude, al que se accede mediante la API de Mensajes; Google Gemini, al que se accede mediante la API de Lenguaje Generativo; y OpenAI, al que se accede mediante la API de Chat Completions. Cada proveedor tiene una convención de autenticación distinta — basada en encabezados para Anthropic y OpenAI, basada en parámetros de URL para Gemini — y cada uno tiene una semántica de límite de tasa propia, que el Doorman gestiona con retroceso exponencial y un tope de reintentos.

Cuando un proveedor devuelve un error de servidor, el Doorman recurre a la inferencia local de Nivel A en lugar de devolver un error al solicitante. El solicitante recibe una respuesta marcada como degradada, y la entrada del registro de auditoría deja constancia de la reversión. El agotamiento del presupuesto se gestiona de otra manera: una solicitud que excedería el presupuesto diario por inquilino se rechaza de inmediato en lugar de degradarse silenciosamente a la inferencia local, porque devolver un error de presupuesto excedido es preferible a entregar una respuesta degradada que el solicitante no pidió.

## Postura de auditoría

Cada llamada al Nivel C produce una entrada en el registro de auditoría que deja constancia del proveedor, el modelo, los conteos de tokens, el costo calculado, la latencia, el identificador del inquilino, el propósito de la llamada y el estado de éxito. Las llamadas están restringidas a una lista fija de propósitos permitidos — trabajo editorial y de construcción del grafo de conocimiento, no uso abierto — y cualquier llamada fuera de esa lista se rechaza en el Doorman.

Una revisión periódica del operador agrega el uso del período anterior por proveedor, señala picos de costo y anomalías en la tasa de éxito, y verifica que la facturación del lado del proveedor coincida con los totales de costo del registro dentro de un margen razonable. La divergencia persistente entre la facturación del proveedor y el registro es un disparador de investigación, no una tolerancia.

## Respuesta a brechas

Una brecha es cualquier evento que exponga el valor de una clave más allá del límite del Doorman: registro accidental, commit accidental a un repositorio, un rastro de pila de un fallo que refleja variables de entorno, inclusión en un registro de mensajes, o aparición en una transcripción usada como paso de reproducción. La secuencia de respuesta es fija y el primer paso no es negociable: revocar la clave en la consola del proveedor de inmediato, antes de limpiar la fuente de la filtración. La revocación deja la clave filtrada sin valor y acota cualquier ventana potencial de uso indebido. Los pasos restantes — eliminar la clave comprometida del archivo de entorno compartido, aprovisionar una clave nueva mediante el procedimiento estándar, revisar el registro de auditoría en busca de actividad anómala entre la marca de tiempo de la filtración y la de la revocación, y registrar el incidente — se siguen en orden.

El incidente se registra en un registro operativo interno, que recoge la fuente de la filtración, la marca de tiempo de la revocación, los hallazgos de la revisión del registro de auditoría, y la causa raíz junto con la acción correctiva. Esta disciplina de registro forma parte del sustrato de divulgación continua: los eventos operativos materiales se registran en commits firmados y fechados, aptos para revisión.

## Véase también

- [[service-slm-operationalization-plan]] — la arquitectura de enrutamiento de cómputo más amplia que define la estructura de los niveles A, B y C
- [[doorman-protocol]] — la arquitectura del servicio Doorman: enrutamiento, autenticación y postura de auditoría
- [[machine-based-auth]] — la capa de autorización basada en máquinas que opera junto al acceso de Nivel C basado en claves
