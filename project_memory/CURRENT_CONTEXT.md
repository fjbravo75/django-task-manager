# CURRENT_CONTEXT

## Proyecto
django-task-manager

## Estado actual
El repositorio local está asentado con Git y sincronizado con origin/main. La app tasks mantiene fuera del admin listado, alta básica, detalle, edición y borrado de tarea con confirmación previa. El flujo visible actual cubre ya el CRUD básico fuera del admin: listar, crear, entrar al detalle, editar una tarea existente, iniciar borrado desde interfaz, confirmar por POST, eliminar y volver al listado. task_form, task_list, task_detail y la confirmación de borrado comparten una base visual uniforme, limpia y suficientemente presentable. La cabecera de detalle quedó reajustada como un bloque vertical compacto para absorber títulos largos sin desequilibrio visual y el texto de confirmación de borrado quedó afinado con una redacción más natural. El microbloque de cierre funcional y visual de este flujo quedó consolidado.

## Bloque activo
CRUD visible fuera del admin cerrado.

## Siguiente paso exacto
Definir con prompt cerrado si la siguiente fase será autenticación, sin abrirla todavía en el código.

## Restricciones vigentes
- No abrir todavía borrado ni autenticación.
- No abrir nuevos frentes de configuración salvo necesidad real.
- No añadir librerías ni complejidad innecesaria.
- Priorizar funcionalidad visible, coherencia general y presentabilidad suficiente sobre perfeccionismo gráfico.
- Usar prompts cerrados y concretos al trabajar con Codex.

## Archivos foco del bloque actual
- tasks/views.py
- tasks/urls.py
- tasks/templates/tasks/task_detail.html
- tasks/templates/tasks/task_confirm_delete.html

## Última actualización
2026-03-17
