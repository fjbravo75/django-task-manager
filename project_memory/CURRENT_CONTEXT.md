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

El bloque visual inmediato de pantallas de `Board` queda cerrado. El foco activo pasa al siguiente frente del núcleo funcional pendiente: autenticación básica integrada.

## Siguiente paso exacto

El siguiente paso correcto ya no es seguir puliendo la maquetación de `Board`.

El siguiente microbloque exacto ya queda decidido: registro + login/logout + protección básica de vistas visibles, a ejecutar cuando el entorno permita validación real de Django.

Ese bloque debe centrarse en:

1. introducir registro, login y logout con la base nativa de Django
2. proteger de forma básica las vistas visibles actuales de `Board` y `Task`
3. dejar para una fase posterior el filtrado fino por `owner` o `members`, sin abrir todavía permisos complejos

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

- `config/settings.py`
- `config/urls.py`
- `tasks/views.py`
- `tasks/urls.py`
- `tasks/forms.py`
- plantillas de autenticación
- templates de `tasks/board_*` y `tasks/task_*`

## Nota de uso

Este archivo resume el estado operativo real del repo tras cerrar el bloque visual local de `Board` y dejar decidido que el siguiente microbloque prioritario es autenticación básica integrada.
