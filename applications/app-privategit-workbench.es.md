---
schema: foundry-doc-v1
title: "Estación de trabajo para desarrolladores (navegador)"
slug: app-privategit-workbench
category: applications
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-06-20
editor: pointsav-engineering
language_protocol: TRANSLATE-ES
short_description: "app-privategit-workbench es un editor de archivos basado en navegador incluido en el sistema operativo host os-privategit, que presenta una interfaz de tres columnas — árbol de archivos, visor y editor — para trabajar con archivos de texto plano y código fuente a través del árbol de archivos del clúster sin necesidad de sesión de terminal."
paired_with: app-privategit-workbench.md
cites: []
---

`app-privategit-workbench` es un editor de archivos basado en navegador incluido
en el sistema operativo host [[os-privategit|`os-privategit`]]. Presenta un endpoint HTTP local
que sirve una aplicación de página única con un diseño de tres columnas: una
barra lateral con el árbol de archivos, un visor de contenido y un editor de
texto plano.

La estación de trabajo es la superficie de creación y revisión principal para
los operadores de [[totebox-orchestration|Totebox Orchestration]] y los Miembros de la Comunidad que
desean acceso directo al [[totebox-archive|árbol de archivos del clúster]] desde el navegador, sin
necesidad de una sesión de terminal. No es una superficie de publicación —
escribe en el sistema de archivos local y depende del flujo de control de
versiones basado en git para el historial y la promoción.

---

## Arquitectura

La estación de trabajo es un único crate de Rust (`app-privategit-workbench`,
Apache 2.0) en el `pointsav-monorepo`. Tiene dos componentes:

**Servicio de escritura (Rust/axum):** Un servidor HTTP que gestiona lecturas y
escrituras de archivos. Se vincula a una dirección de loopback y nunca se expone
directamente a redes externas. El servicio aplica contención de raíz
(todas las rutas se canonicalizan y verifican contra las raíces declaradas),
una lista de extensiones permitidas y detección de conflictos basada en mtime.

**Aplicación de página única:** Un archivo HTML autónomo incrustado en el
binario en tiempo de compilación mediante `include_str!`. La SPA realiza llamadas
a la API a través de un proxy nginx al servicio de escritura para lecturas y
escrituras de archivos, y a rutas de autoindex de nginx para listados de
directorios. No se cargan recursos externos en tiempo de ejecución.

El binario se compila para el host `os-privategit` y es gestionado por una
unidad de systemd. Las rutas de intranet de nginx enrutan `/_api/edit/*` al
servicio de escritura y sirven autoindex JSON en `/_api/command/`,
`/_api/clones/` y prefijos por sandbox.

---

## Árbol de archivos

La barra lateral lista las raíces declaradas en `config.toml`. Cada raíz asigna
un prefijo URL (por ejemplo, `_clones/project-development`) a una ruta del
sistema de archivos (por ejemplo, `/srv/foundry/clones/project-development`).
Las raíces pueden ser con o sin permiso de escritura. La raíz del espacio de
trabajo de Command (`/srv/foundry`) es siempre de solo lectura; las raíces de
los clústeres tienen permiso de escritura.

El contenido de los directorios se recupera al expandir desde el autoindex JSON
de nginx. El árbol admite expansión anidada a profundidad arbitraria.

---

## Visor

La columna central renderiza el archivo seleccionado según su extensión:

- **Markdown (`.md`):** Renderizado como HTML usando un parser integrado.
  Se admiten bloques de código delimitados, código en línea, encabezados,
  listas, enlaces y tablas. El clic desde los encabezados y párrafos
  renderizados mueve el cursor del editor a la línea de código fuente
  correspondiente.
- **HTML (`.html`):** Mostrado en un iframe en modo aislado.
- **Imágenes:** Mostradas en línea.
- **Todos los demás tipos:** Mostrados como texto plano.

El visor y el editor operan de forma independiente. Al abrir un archivo de
solo lectura se muestra el visor sin el panel del editor.

---

## Editor

La columna derecha aparece cuando el archivo abierto se encuentra en una raíz
con permiso de escritura. El editor es un `<textarea>` con las siguientes
características:

- Canaleta de números de línea con resaltado de la línea activa
- Indicador de posición del cursor (línea y columna) en la barra del editor
- Indicador de estado con cambios no guardados (punto naranja)
- Guardar: `Cmd+S` o el botón Guardar — escribe mediante `PUT /file` con el
  mtime actual para detectar ediciones concurrentes; muestra un diálogo de
  conflicto en HTTP 409
- Barra de Buscar / Reemplazar (`Cmd+F`): resaltado incremental de coincidencias,
  navegación anterior/siguiente, Reemplazar y Reemplazar Todo; preserva la
  pila de deshacer nativa mediante `execCommand`
- Panel de Esquema del Documento (`Cmd+Shift+O`): lista todos los encabezados
  de markdown (H1–H6) o las cabeceras de tabla TOML del archivo actual; filtrar
  escribiendo; clic o Intro para saltar el cursor a ese símbolo
- Botón de alternar comentario de línea: según la extensión (`//` para
  Rust/JS/TS, `#` para TOML/YAML/shell); alterna las líneas seleccionadas
- Ir a línea (`Ctrl+G`)
- El tabulador inserta dos espacios
- Cierre automático de llaves `{`, `[`, `(`
- Mover línea arriba / abajo (`Alt+↑` / `Alt+↓`)
- Duplicar línea (`Shift+Alt+↓`)

---

## Modelo de seguridad

El servicio de escritura aplica cuatro capas de contención alineadas con el
enfoque de [[pre-commit-defense-in-depth|defensa en profundidad pre-commit]] utilizado en toda la
plataforma:

**Contención de raíz:** Cada ruta se canonicaliza con `std::fs::canonicalize`
y se verifica para que permanezca dentro de la ruta del sistema de archivos
de la raíz declarada. Las rutas que se resuelven fuera de la raíz se rechazan
con HTTP 400.

**Protección CSRF:** Cada solicitud `PUT /file` requiere el encabezado
`X-Foundry-Editor: 1`. La política de origen cruzado del navegador impide
que páginas de terceros añadan este encabezado.

**Lista de extensiones permitidas:** Las escrituras solo se permiten para
extensiones de texto plano y código fuente reconocidas. Los formatos binarios
y las extensiones desconocidas son de solo lectura a través de la estación
de trabajo.

**Indicador de escritura:** La declaración `writable = false` en una entrada
de raíz provoca que todos los intentos de escritura en esa raíz sean
rechazados con HTTP 403, independientemente de los permisos del sistema de
archivos.

La unidad de systemd se ejecuta con `ProtectSystem=strict` y `ReadWritePaths=`
limitado a las raíces con permiso de escritura declaradas. Añadir una nueva
raíz con permiso de escritura requiere actualizar tanto `config.toml` como el
archivo de servicio de systemd; omitir la actualización del archivo de servicio
provoca fallos de escritura silenciosos en la capa del sistema de archivos.

---

## Relación con os-privategit

`app-privategit-workbench` se incluye en el sistema operativo host
[[os-privategit|`os-privategit`]] junto a `app-privategit-design-system` y
`service-privategit`. Es la superficie de creación para los operadores que
utilizan el nivel privategit — un entorno de desarrollo alojado localmente y
aislado en red para instancias de [[totebox-orchestration|Totebox Orchestration]]. El acceso a las
raíces con permiso de escritura está gobernado por el modelo de
[[machine-based-auth|autorización basada en máquinas]].

El crate tiene licencia Apache, Versión 2.0, y está destinado a la
implementación en instancias de nivel cliente de `os-privategit`. Una guía de
configuración operativa está disponible en el catálogo de despliegue de flota
para clientes.

---

## Adiciones planificadas

- **Fase 4 (planificada/prevista):** Integración de CodeMirror 6 para
  resaltado de sintaxis; raíces autenticadas con ámbito de escritura por usuario.

## Véase también

- [[os-privategit]] — el sistema operativo host que incluye esta estación de trabajo
- [[totebox-archive]] — el árbol de archivos del clúster con el que trabajan los operadores
- [[machine-based-auth]] — el modelo de autorización que rige el acceso a raíces con permiso de escritura
- [[pre-commit-defense-in-depth]] — la disciplina de defensa en profundidad aplicada por el servicio de escritura
