# CURRENT_CONTEXT

## Proyecto
django-task-manager

## Estado actual
El repositorio local está asentado con Git y sincronizado con origin/main. La app tasks mantiene fuera del admin listado, alta básica y detalle de tarea. El flujo listado -> crear -> guardar -> volver al listado está resuelto y el listado permite entrar al detalle individual de una tarea. task_form, task_list y task_detail comparten una base visual uniforme, limpia y suficientemente presentable. El microbloque de detalle quedó cerrado funcional y visualmente, con los ajustes finales de alineación del listado y de la descripción en detalle ya validados.

## Bloque activo
Microbloque de detalle de tarea fuera del admin cerrado.

## Siguiente paso exacto
Edición de tarea fuera del admin, sin abrir todavía borrado ni autenticación.

## Restricciones vigentes
- No abrir todavía edición, borrado ni autenticación.
- No abrir nuevos frentes de configuración salvo necesidad real.
- No añadir librerías ni complejidad innecesaria.
- Priorizar funcionalidad visible, coherencia general y presentabilidad suficiente sobre perfeccionismo gráfico.
- Usar prompts cerrados y concretos al trabajar con Codex.

## Archivos foco del bloque actual
- tasks/templates/tasks/task_list.html
- tasks/views.py
- tasks/urls.py
- tasks/templates/tasks/task_detail.html

## Última actualización
2026-03-16
