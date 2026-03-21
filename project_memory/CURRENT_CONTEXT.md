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

El arranque de autenticación básica integrada ya queda cerrado a nivel operativo.

Login, logout y registro con inicio automático de sesión quedaron implementados y validados en navegador durante la sesión actual.

La validación real también confirmó una incidencia de coherencia pendiente: un usuario nuevo autenticado sigue viendo tableros ajenos.

## Siguiente paso exacto

El siguiente paso correcto ya no es seguir puliendo la maquetación de `Board`.

El siguiente microbloque exacto pasa a ser protección básica coherente por usuario sobre las vistas visibles de `Board` y `Task`.

El bloque pendiente de autenticación debe centrarse ahora en:

1. impedir que un usuario autenticado vea por defecto tableros y tareas ajenos
2. aplicar protección básica coherente con las relaciones a usuario ya existentes en `Board` y `Task`
3. dejar para una fase posterior permisos avanzados, roles, invitaciones o ACL complejas

## Restricciones operativas vigentes

- Mantener aplicación Django server-rendered.
- No abrir frontend separado.
- No introducir React, Vue, websockets ni complejidad de frontend innecesaria.
- No abrir extras mientras el núcleo principal siga incompleto.
- No reabrir el refactor de modelo ya cerrado salvo incidencia real.
- No reintroducir `status` como fuente de estado de `Task`.
- No devolver el centro visible del producto al listado global plano de tareas.
- No tratar el siguiente bloque como un `login_required` superficial si deja visibles tableros ajenos a cualquier usuario autenticado.
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

Todavía no están cerrados protección básica coherente por usuario, gestión visible de tableros/listas ni una experiencia kanban más rica.

## Archivos previsiblemente implicados en la siguiente fase

- `config/settings.py`
- `config/urls.py`
- `tasks/views.py`
- `tasks/urls.py`
- `tasks/forms.py`
- plantillas de autenticación
- templates de `tasks/board_*` y `tasks/task_*`

## Nota de uso

Este archivo resume el estado operativo real del repo tras cerrar autenticación básica integrada como arranque y dejar preparado como siguiente microbloque la protección básica coherente por usuario sobre boards y tareas visibles.
