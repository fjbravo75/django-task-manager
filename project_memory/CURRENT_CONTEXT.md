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
- acciones directas desde `Board` hacia detalle y edición de tarea
- pulido visual local de `board_list` y `board_detail` ya integrado en el repo con recuperación de `board.description`

## Bloque activo

El bloque visual inmediato de pantallas de `Board` queda cerrado. El foco activo vuelve al cierre del núcleo funcional pendiente sin reabrir iteración de diseño fino.

## Siguiente paso exacto

El siguiente paso correcto ya no es seguir puliendo la maquetación de `Board`.

El siguiente microbloque exacto debe empezar con inspección y planificación previa del siguiente frente funcional del núcleo aún abierto, evitando tocar código hasta fijar el orden.

Ese bloque debe centrarse en:

1. elegir el siguiente frente funcional prioritario entre autenticación o gestión visible de tableros/listas
2. mantener `Board` como contexto principal del producto
3. no reabrir el bloque visual salvo corrección concreta detectada por revisión manual

## Restricciones operativas vigentes

- Mantener aplicación Django server-rendered.
- No abrir frontend separado.
- No introducir React, Vue, websockets ni complejidad de frontend innecesaria.
- No abrir extras mientras el núcleo principal siga incompleto.
- No reabrir el refactor de modelo ya cerrado salvo incidencia real.
- No reintroducir `status` como fuente de estado de `Task`.
- No devolver el centro visible del producto al listado global plano de tareas.
- No tratar la maquetación fina de estas pantallas como un frente abierto en Codex; para ajustes visuales concretos, usar revisión manual guiada y cambios directos acotados.

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
- `tasks/forms.py`
- templates de `tasks/board_*` y `tasks/task_*`

## Nota de uso

Este archivo resume el estado operativo real del repo tras cerrar el bloque visual local de `Board` y dejar las pantallas principales ya suficientemente presentables para seguir con núcleo funcional.
