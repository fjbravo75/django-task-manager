# CURRENT_CONTEXT.md

## Estado técnico actual

La base relacional mínima tipo kanban ya está implantada y validada en el repo.

Bloques ya cerrados y consolidados en la rama principal:

- refactor de modelo hacia `Board`, `TaskList`, `Tag` y `Task` relacional
- transición de `Task` desde `status` a `task_list` como fuente real de estado
- alineación del flujo heredado de tareas con el nuevo modelo
- navegación principal ya centrada en `Board`
- creación de tareas contextualizada desde `Board`
- edición de tareas contextualizada al `Board` real, sin permitir moverlas a listas de otros tableros por el flujo contextual

## Bloque activo

Refuerzo del flujo principal centrado en `Board` y reducción progresiva de dependencia del flujo heredado global de tareas.

## Siguiente paso exacto

El siguiente microbloque correcto es mejorar las acciones visibles directas desde `Board` hacia cada tarea, para ver y editar desde el propio tablero con menos dependencia del flujo heredado global.

Ese bloque debe centrarse en:

1. accesos más directos desde el tablero a cada tarea
2. continuidad clara entre vista de tablero, detalle y edición
3. mantener las rutas heredadas solo como soporte secundario, no como centro del producto

## Restricciones operativas vigentes

- Mantener aplicación Django server-rendered.
- No abrir frontend separado.
- No introducir React, Vue, websockets ni complejidad de frontend innecesaria.
- No abrir extras mientras el núcleo principal siga incompleto.
- No reabrir el refactor de modelo ya cerrado salvo incidencia real.
- No reintroducir `status` como fuente de estado de `Task`.
- No devolver el centro visible del producto al listado global plano de tareas.

## Núcleo funcional ya sostenido por el repo

La base actual ya sostiene estas piezas del núcleo:

- tableros a nivel de modelo y de navegación principal
- listas o columnas a nivel de modelo y de visualización básica
- tareas integradas en esa estructura
- creación y edición de tareas coherentes con el contexto del tablero
- prioridad
- etiquetas
- fechas límite
- asignación opcional a usuario

Todavía no están cerrados autenticación funcional, gestión visible de tableros/listas ni una experiencia kanban más rica.

## Archivos previsiblemente implicados en la siguiente fase

- `tasks/views.py`
- `tasks/urls.py`
- templates de `tasks/board_*` y `tasks/task_*`

## Nota de uso

Este archivo resume el estado operativo real del repo tras los microbloques ya consolidados alrededor de `Board`.
