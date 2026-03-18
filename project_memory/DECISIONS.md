# DECISIONS.md

## 2026-03-13 — Proyecto B como pieza principal activa del reto

### Decisión
El Proyecto B queda confirmado como `django-task-manager` y pasa a ser la pieza principal activa del reto.

### Motivo
Aporta más valor directo a empleabilidad seguir construyendo una aplicación Django visible que seguir dedicando tiempo a pulido marginal o práctica sin salida clara de portfolio.

### Impacto práctico
- El foco principal del reto pasa a Django.
- El trabajo debe concentrarse en hacer el Proyecto B visible, serio y presentable.

### Estado
Vigente

## 2026-03-13 — Proyecto C como evolución pequeña del Proyecto B

### Decisión
El Proyecto C no debe convertirse en otro proyecto grande desde cero, sino en una evolución pequeña y coherente del propio Proyecto B.

### Motivo
Reduce dispersión y permite aprovechar mejor el trabajo ya construido.

### Impacto práctico
- Se evita abrir un tercer frente grande.
- Se refuerza la coherencia del portfolio.

### Estado
Vigente

## 2026-03-13 — Priorizar funcionalidad visible sobre perfeccionismo de configuración

### Decisión
En esta fase compensa más construir funcionalidad visible en Django que dedicar sesiones enteras a Git aislado o a perfeccionismo de configuración con poco retorno inmediato.

### Motivo
El objetivo del reto es empleabilidad funcional, no perfección técnica absoluta.

### Impacto práctico
- Git y GitHub se trabajan de forma práctica y vinculada al proyecto real.
- La prioridad sigue siendo construir valor visible y defendible.

### Estado
Vigente

## 2026-03-13 — Terminal neutral y activación manual del entorno

### Decisión
El entorno de terminal no debe quedar secuestrado por activaciones globales en `~/.zshrc`. Se trabajará con terminal neutral y activación manual del entorno adecuado según el proyecto.

### Motivo
La activación global previa generó fricción innecesaria entre proyectos y confundió el contexto real de trabajo.

### Impacto práctico
- Cada proyecto debe activar su entorno de forma explícita.
- Se evita perder tiempo en automatismos con poco retorno.

### Estado
Vigente

## 2026-03-13 — Método de colaboración con Codex

### Decisión
ChatGPT se usa para orquestar y revisar dirección. Codex se usa como ejecutor de tareas concretas, delimitadas y verificables dentro del repositorio abierto.

### Motivo
Este reparto reduce fricción, mejora precisión y encaja mejor con el trabajo real del proyecto.

### Impacto práctico
- Las tareas para Codex deben definirse con prompts cerrados.
- Toda salida relevante debe revisarse a nivel de archivos y validarse cuando proceda.

### Estado
Vigente

## 2026-03-13 — Las preferencias técnicas deben formularse como requisitos explícitos

### Decisión
Cuando se quiera que Codex implemente algo con una preferencia técnica concreta, esa preferencia debe formularse como requisito explícito y no dejarse implícita.

### Motivo
En la primera generación del modelo `Task`, algunos detalles importantes no se fijaron porque no se habían pedido de forma suficientemente cerrada.

### Impacto práctico
- Los prompts deben indicar archivo, requisitos obligatorios, restricciones y salida esperada.
- Se reduce el riesgo de correcciones evitables.

### Estado
Vigente

## 2026-03-16 — Dar por suficiente la base visual inicial del Proyecto B

### Decisión
La base visual inicial del CRUD visible fuera del admin se acepta como suficiente, uniforme y presentable para esa fase. No compensa seguir iterando diseño fino sobre ese mismo bloque.

### Motivo
El objetivo era visibilidad funcional y coherencia general del producto, no perfeccionismo gráfico sobre una base ya suficiente.

### Impacto práctico
- Las siguientes iteraciones deben priorizar funcionalidad visible y continuidad del flujo.
- El criterio visual pasa a ser coherencia general y presentabilidad suficiente.
- No se reabre ese bloque para pulido fino salvo necesidad clara.

### Estado
Vigente

## 2026-03-17 — Integrar Tailwind CSS por CLI simple

### Decisión
La mejora visual de la capa visible actual del CRUD fuera del admin se implementa con Tailwind CSS por CLI simple, sin PostCSS y sin introducir una toolchain frontend más compleja.

### Motivo
Permite elevar la presentabilidad del proyecto con una integración pequeña, mantenible y suficiente para un portfolio Django junior sin abrir un frente técnico innecesario.

### Impacto práctico
- `npm` queda limitado a lo necesario para compilar Tailwind.
- El CSS de entrada se mantiene dentro de los estáticos de `tasks`.
- El CSS compilado se sirve desde la ruta estática ya usada por las plantillas.
- La base común de plantillas para esta integración se limita a `tasks/templates/tasks/`.

### Estado
Vigente

## 2026-03-18 — Redefinir Proyecto B como aplicación tipo kanban

### Decisión
Proyecto B deja de tratarse como una app Django básica de tareas y pasa a redefinirse como una aplicación Django server-rendered de gestión de tareas tipo kanban.

### Motivo
Se busca que el mismo proyecto sirva a la vez como pieza fuerte de portfolio y como entregable serio del máster, evitando duplicar esfuerzo en dos proyectos casi iguales.

### Impacto práctico
- El CRUD básico ya construido se considera base reaprovechable, no destino final.
- Las siguientes decisiones técnicas deben evaluarse según su encaje con una estructura más madura.
- Antes de abrir una ampliación grande de código, debe cerrarse planificación previa.

### Estado
Vigente

## 2026-03-18 — Proyecto B con doble función: portfolio + máster

### Decisión
Proyecto B debe evolucionar para cumplir doble función real: pieza fuerte de portfolio técnico y entregable académico alineado con el “Gestor de Tareas Avanzado” del máster.

### Motivo
El nuevo marco del proyecto fija expresamente esa doble función como criterio vigente.

### Impacto práctico
- El proyecto debe medirse no solo por funcionar, sino por ser claro, enseñable y defendible.
- Las decisiones de alcance deben priorizar valor visible, coherencia y seriedad de entrega.
- No compensa abrir otro proyecto paralelo para cubrir el frente académico.

### Estado
Vigente

## 2026-03-18 — Mantener Proyecto B como aplicación server-rendered

### Decisión
Proyecto B debe seguir siendo una aplicación Django server-rendered. No se abrirá frontend separado ni se introducirá complejidad de frontend como forma de “subir nivel”.

### Motivo
El marco vigente del proyecto exige foco, cierre y realismo. El proyecto debe crecer en solidez funcional, no en dispersión tecnológica.

### Impacto práctico
- No proponer React, Vue, API separada, websockets ni toolchains frontend innecesarias.
- HTML, CSS y JavaScript ligero siguen siendo el marco razonable del proyecto.
- Cualquier mejora visual o interactiva debe mantenerse dentro de ese alcance.

### Estado
Vigente

## 2026-03-18 — Priorizar núcleo obligatorio antes que extras

### Decisión
Los extras del proyecto quedan expresamente subordinados al cierre sólido del núcleo obligatorio.

### Motivo
Primero debe cerrarse lo esencial del proyecto; los extras solo entran si existe tiempo real y estabilidad suficiente.

### Impacto práctico
- No abrir exportación CSV/JSON, notificaciones u otros extras mientras el núcleo principal siga incompleto.
- Los prompts deben recordar este criterio cuando una tarea pueda derivar hacia trabajo no prioritario.

### Estado
Vigente

## 2026-03-18 — Núcleo funcional objetivo de la siguiente fase

### Decisión
La siguiente fase del proyecto debe orientarse, por fases pequeñas, a este núcleo funcional:

- registro
- login
- logout
- tableros
- listas o columnas
- tareas integradas en esa estructura
- asignación de tareas a usuarios
- prioridad
- etiquetas
- fechas límite
- movimiento de tareas entre listas o columnas

### Motivo
Ese es el alcance mínimo que alinea Proyecto B con el nuevo marco del reto y con el tipo de entregable exigido por la academia.

### Impacto práctico
- Las siguientes fases deben ordenarse alrededor de este núcleo.
- Si una tarea no ayuda a cerrar este núcleo o a dejarlo mejor presentado, no es prioritaria.
- Las decisiones sobre modelos, vistas y flujo deben evaluarse en función de este objetivo.

### Estado
Vigente

## 2026-03-18 — Planificación previa obligatoria en cambios estructurales

### Decisión
Antes de modificar modelos, vistas, URLs o templates para una ampliación grande de Proyecto B, debe hacerse planificación previa si la tarea es estructural o afecta varias capas.

### Motivo
El proyecto ya no debe crecer sobre el CRUD antiguo con microextensiones aisladas; hace falta controlar bien la transición hacia la nueva estructura.

### Impacto práctico
- Si una tarea implica rediseño, primero se pide plan y no ejecución directa.
- El prompt debe indicar explícitamente cuándo toca inspeccionar y proponer plan sin tocar archivos.
- Se reduce el riesgo de rehacer trabajo por falta de secuencia.

### Estado
Vigente

## 2026-03-18 — `TaskList` pasa a ser la fuente real de estado de `Task`

### Decisión
En la nueva base del proyecto, `Task` ya no debe apoyarse en un campo `status` como fuente real de estado. Ese papel queda asumido por `TaskList`.

### Motivo
El refactor de modelo ya cerró la transición hacia una estructura tipo kanban mínima y conviene fijar esta decisión para no reintroducir incoherencias en sesiones futuras.

### Impacto práctico
- No duplicar estado entre `Task.status` y `Task.task_list`.
- Las vistas, formularios y plantillas deben leer el estado visible desde la lista o columna asociada.
- Los siguientes bloques deben construir navegación y flujo alrededor de `Board` y `TaskList`, no alrededor de un CRUD plano de estados.

### Estado
Vigente

## 2026-03-18 — `Board` pasa a ser el contexto principal visible del producto

### Decisión
La navegación principal del producto debe entrar por `Board`, y los flujos visibles de tareas deben subordinarse progresivamente a ese contexto.

### Motivo
Los microbloques ya cerrados consolidaron una transición real desde el CRUD plano de tareas hacia una estructura centrada en tableros.

### Impacto práctico
- La home ya no debe volver a depender del listado global plano de tareas.
- La creación y edición de tareas deben respetar el `Board` real de trabajo.
- Las rutas heredadas globales de tareas pueden sobrevivir como soporte secundario, pero no deben volver a ser el centro del producto.

### Estado
Vigente
