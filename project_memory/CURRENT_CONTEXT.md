# CURRENT_CONTEXT.md

## Estado técnico actual

La base visible inicial del proyecto ya está construida y validada en local.

Bloques ya cerrados en la versión actual del repo:

- listado de tareas
- alta de tareas
- detalle de tarea
- edición de tarea
- borrado de tarea
- refinado visual base
- integración contenida de Tailwind
- paginación simple

El proyecto no debe seguir tratándose como un CRUD básico en expansión. Esa fase base ya está cerrada.

## Bloque activo

Rediseño estructural previo a la siguiente evolución técnica del proyecto.

Todavía no debe ejecutarse una ampliación grande de código sin planificación previa.

## Siguiente paso exacto

Antes de modificar modelos, vistas, URLs o templates para la nueva fase del proyecto, hay que definir con precisión la siguiente versión objetivo.

Si la tarea es estructural o el prompt actual pide planificación, no modificar código todavía.

En esa planificación debe quedar cerrado, como mínimo:

1. modelo de datos objetivo
2. alcance mínimo de la siguiente fase
3. orden de implementación por fases pequeñas
4. dependencias y riesgos principales

## Estructura objetivo de la siguiente fase

La siguiente evolución del proyecto debe orientarse a una estructura basada en estas entidades:

- `Board`
- `TaskList`
- `Task`
- `Tag`
- relación clara con `User`

## Restricciones operativas vigentes

- Mantener aplicación Django server-rendered.
- No abrir frontend separado.
- No introducir React, Vue, websockets ni complejidad de frontend innecesaria.
- No abrir extras mientras el núcleo principal de la siguiente fase no esté sólido.
- Si una tarea afecta varias capas o exige rediseño, primero debe resolverse por planificación.
- No continuar ampliando la versión antigua del CRUD como si siguiera siendo el bloque principal.

## Núcleo funcional objetivo de la siguiente fase

La evolución del proyecto debe orientarse, por fases, a este núcleo:

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

## Archivos previsiblemente implicados en la siguiente fase

Estos archivos o zonas del repo son los candidatos más probables para inspección o cambio en la siguiente etapa, solo si el prompt lo autoriza:

- `tasks/models.py`
- `tasks/views.py`
- `tasks/urls.py`
- templates de `tasks/`
- migraciones nuevas si la tarea lo requiere

## Nota de uso

Este archivo describe el estado operativo actual del repo.

No autoriza cambios por sí solo.

La tarea concreta, el alcance y los archivos que pueden tocarse los define siempre el prompt actual.