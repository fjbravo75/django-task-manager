# SESSION_LOG

## 2026-03-13

### Objetivo
Dejar arrancado de verdad el Proyecto B del portfolio y validarlo como base funcional inicial en Django.

### Trabajo realizado
- Se creó el repositorio local django-task-manager dentro de WSL Ubuntu.
- Se preparó un entorno conda independiente para el proyecto.
- Se instaló Django y se generó el proyecto con config como carpeta de configuración.
- Se aplicaron las migraciones iniciales del framework.
- Se verificó el arranque correcto del servidor de desarrollo en local.
- Se creó la app tasks y se integró en INSTALLED_APPS.
- Se creó el modelo Task con título, descripción opcional, estado, prioridad, fecha de creación y fecha de actualización.
- Se definieron choices explícitos para estado y prioridad.
- Se fijaron valores por defecto coherentes para status y priority.
- Se generó y aplicó la migración inicial de la app tasks.
- Se registró Task en el panel de administración.
- Se creó un superusuario.
- Se accedió con éxito al admin en local.
- Se creó una tarea real de prueba desde el admin para validar el flujo completo.
- Se revisó el modo de trabajo con Codex y se fijó como criterio usar prompts más cerrados y concretos.

### Archivos tocados
- manage.py
- config/settings.py
- tasks/models.py
- tasks/admin.py
- db.sqlite3
- migraciones iniciales del proyecto y de la app tasks

### Resultado
El Proyecto B deja de estar en fase de preparación y pasa a tener una base Django funcional real ya validada de punta a punta.

### Pendiente inmediato
- Asentar Git y GitHub del Proyecto B.
- Después, crear la primera vista, URLs y plantilla HTML fuera del admin.
