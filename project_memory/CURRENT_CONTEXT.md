# CURRENT_CONTEXT.md

## Estado técnico actual

La base relacional mínima tipo kanban ya existe y está validada en el repo.

Bloques cerrados y ya integrados en `main`:

- refactor de modelo hacia `Board`, `TaskList`, `Tag` y `Task` relacional
- transición de `Task` desde `status` a `task_list` como fuente real de estado
- alineación del CRUD visible heredado de tareas con el nuevo modelo
- validación real con migraciones, `migrate`, `check` y prueba funcional mínima del flujo heredado
- commit y push reales de los dos microbloques ya cerrados

## Bloque activo

Transición del centro de navegación desde el listado global plano de tareas hacia `Board` como contexto principal.

## Siguiente paso exacto

El siguiente microbloque correcto es empezar a mover la navegación y el flujo visible hacia `Board` como contexto principal, dejando de depender del listado global plano de tareas.

En ese bloque debe abordarse, como mínimo:

1. una entrada visible basada en tableros
2. una vista de tablero simple como contexto de listas y tareas
3. continuidad del flujo actual sin abrir todavía autenticación completa ni extras

## Restricciones operativas vigentes

- Mantener aplicación Django server-rendered.
- No abrir frontend separado.
- No introducir React, Vue, websockets ni complejidad de frontend innecesaria.
- No abrir extras mientras el núcleo principal siga incompleto.
- No reabrir el refactor de modelo ya cerrado salvo incidencia real.
- No reintroducir `status` como fuente de estado de `Task`.

## Núcleo funcional ya sostenido por el repo

La base actual ya sostiene estas piezas del núcleo:

- tableros a nivel de modelo
- listas o columnas a nivel de modelo
- tareas integradas en esa estructura
- prioridad
- etiquetas
- fechas límite
- asignación opcional a usuario

Todavía no está cerrada la navegación visible centrada en tableros ni la autenticación funcional del producto.

## Archivos previsiblemente implicados en la siguiente fase

- `tasks/views.py`
- `tasks/urls.py`
- templates de `tasks/`
- `config/urls.py` solo si el flujo visible lo exige

## Nota de uso

Este archivo resume el estado operativo real actual del repo tras los dos microbloques ya cerrados.
