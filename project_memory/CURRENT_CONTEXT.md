# CURRENT_CONTEXT

## Proyecto
django-task-manager

## Estado actual
El repositorio local está asentado con Git y sincronizado con origin/main. La app tasks mantiene fuera del admin listado, alta básica, detalle, edición y borrado de tarea con confirmación previa. El flujo visible actual cubre ya el CRUD básico fuera del admin: listar, crear, entrar al detalle, editar una tarea existente, iniciar borrado desde interfaz, confirmar por POST, eliminar y volver al listado. La capa visible actual del CRUD quedó integrada sobre Tailwind CSS por CLI simple, con una base local de plantillas en tasks, CSS de entrada dedicado y CSS compilado servido desde los estáticos de la app. Listado, formulario, detalle y confirmación de borrado comparten ahora una presentación más sobria, uniforme y enseñable para portfolio. La cabecera de detalle quedó reajustada como un bloque vertical compacto para absorber títulos largos sin desequilibrio visual y el texto de confirmación de borrado quedó afinado con una redacción más natural. El microbloque de presentabilidad profesional de este flujo quedó consolidado.

## Bloque activo
Microbloque de integración Tailwind CLI y presentabilidad del CRUD visible cerrado.

## Siguiente paso exacto
Definir con prompt cerrado la siguiente fase funcional después del cierre visual actual, previsiblemente autenticación, sin abrirla todavía en el código.

## Restricciones vigentes
- No abrir todavía borrado ni autenticación.
- No abrir nuevos frentes de configuración salvo necesidad real.
- No añadir librerías ni complejidad innecesaria.
- Priorizar funcionalidad visible, coherencia general y presentabilidad suficiente sobre perfeccionismo gráfico.
- Usar prompts cerrados y concretos al trabajar con Codex.

## Archivos foco del bloque actual
- package.json
- tasks/static/tasks/tailwind.input.css
- tasks/static/tasks/styles.css
- tasks/templates/tasks/base.html
- tasks/templates/tasks/task_list.html
- tasks/templates/tasks/task_form.html
- tasks/templates/tasks/task_detail.html
- tasks/templates/tasks/task_confirm_delete.html

## Última actualización
2026-03-17
