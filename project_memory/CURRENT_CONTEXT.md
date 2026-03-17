# CURRENT_CONTEXT

## Proyecto
django-task-manager

## Estado actual
El repositorio local está asentado con Git y sincronizado con origin/main. La app tasks mantiene fuera del admin listado, alta básica, detalle, edición y borrado de tarea con confirmación previa. El flujo visible actual cubre ya el CRUD básico fuera del admin: listar, crear, entrar al detalle, editar una tarea existente, iniciar borrado desde interfaz, confirmar por POST, eliminar y volver al listado. La capa visible actual del CRUD quedó integrada sobre Tailwind CSS por CLI simple, con una base local de plantillas en tasks, CSS de entrada dedicado y CSS compilado servido desde los estáticos de la app. Listado, formulario, detalle y confirmación de borrado comparten ahora una presentación más sobria, uniforme y enseñable para portfolio. La cabecera de detalle quedó reajustada como un bloque vertical compacto para absorber títulos largos sin desequilibrio visual, el texto de confirmación de borrado quedó afinado con una redacción más natural y el listado recibió el ajuste fino final necesario para quedar estable. El microbloque de presentabilidad profesional de este flujo quedó consolidado y cerrado.

## Bloque activo
Bloque de presentabilidad del CRUD visible cerrado.

## Siguiente paso exacto
Paginación simple del listado de tareas.

## Restricciones vigentes
- No abrir todavía borrado ni autenticación.
- No abrir nuevos frentes de configuración salvo necesidad real.
- No añadir librerías ni complejidad innecesaria.
- Priorizar funcionalidad visible, coherencia general y presentabilidad suficiente sobre perfeccionismo gráfico.
- Usar prompts cerrados y concretos al trabajar con Codex.

## Archivos foco del bloque actual
- tasks/views.py
- tasks/urls.py
- tasks/templates/tasks/task_list.html

## Última actualización
2026-03-17
