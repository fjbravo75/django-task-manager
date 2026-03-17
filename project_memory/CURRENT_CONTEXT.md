# CURRENT_CONTEXT

## Proyecto
django-task-manager

## Estado actual
El repositorio local está asentado con Git y sincronizado con origin/main. La app tasks mantiene fuera del admin listado, alta básica, detalle, edición y borrado de tarea con confirmación previa. El flujo visible actual cubre ya el CRUD básico fuera del admin: listar, crear, entrar al detalle, editar una tarea existente, iniciar borrado desde interfaz, confirmar por POST, eliminar y volver al listado. La capa visible actual del CRUD quedó integrada sobre Tailwind CSS por CLI simple, con una base local de plantillas en tasks, CSS de entrada dedicado y CSS compilado servido desde los estáticos de la app. Listado, formulario, detalle y confirmación de borrado comparten ahora una presentación más sobria, uniforme y enseñable para portfolio. El listado visible de tareas fuera del admin ya dispone de paginación simple funcional y validada. La vista del listado ordena las tareas por `pk`, utiliza `Paginator` de Django y muestra 5 tareas por página. La navegación entre páginas se resuelve mediante query string (`?page=`) y queda protegida frente a valores inválidos o fuera de rango mediante `get_page()`.

La presentación visual final de la paginación también ha quedado afinada y validada en navegador. El bloque se muestra centrado, en una sola línea, con navegación en español (`Anterior`, `Página X de Y`, `Siguiente`), sin botones innecesarios y con una jerarquía visual coherente con el resto de la interfaz.

## Bloque activo
Microbloque de paginación simple del listado cerrado.

## Siguiente paso exacto
Implementar edición de tareas fuera del admin, reutilizando el formulario ya existente y manteniendo el mismo criterio de alcance corto, validación real y presentación coherente.

## Restricciones vigentes
- No abrir todavía borrado ni autenticación.
- No abrir nuevos frentes de configuración salvo necesidad real.
- No añadir librerías ni complejidad innecesaria.
- Priorizar funcionalidad visible, coherencia general y presentabilidad suficiente sobre perfeccionismo gráfico.
- Usar prompts cerrados y concretos al trabajar con Codex.

## Archivos foco del bloque actual
- tasks/views.py
- tasks/templates/tasks/task_list.html
- tasks/static/tasks/styles.css

## Último commit asociado
- `f166773` — `Add pagination to task list`

## Última actualización
2026-03-17
