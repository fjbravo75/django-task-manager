# Django Task Manager

Aplicación web de gestión de tareas construida con Django.  
En la interfaz, la aplicación se muestra como **Gestor de tareas**.

## Resumen

**Django Task Manager** es una aplicación web desarrollada con Django para organizar tareas de una forma clara y visual. Aunque el nombre técnico del proyecto está en inglés, dentro de la app el nombre visible es **Gestor de tareas**, porque refleja mejor cómo la vería una persona real al utilizarla.

La aplicación parte de una idea sencilla: cada usuario puede crear sus propios tableros, organizar listas dentro de ellos y gestionar tareas con información útil para el día a día, como prioridad, fecha límite, etiquetas y asignación. No he intentado convertir este proyecto en una herramienta enorme ni llenarlo de complejidad innecesaria. La intención ha sido construir una base sólida, clara y fácil de seguir.

Este proyecto me ha servido para trabajar una parte muy práctica de Django: modelos relacionados, vistas, formularios, validaciones, permisos, pruebas y una entrega final más limpia. En esta fase de cierre también queda preparado para arrancar en local con una demo reproducible y con una configuración de entorno sencilla, pensada para facilitar un despliegue posterior con PostgreSQL.

## Qué permite hacer

La aplicación permite:

- registrarse, iniciar sesión y cerrar sesión
- crear, editar y eliminar tableros
- crear y organizar listas dentro de cada tablero
- crear, editar y eliminar tareas
- asignar prioridad y fecha límite
- usar etiquetas por tablero
- asignar tareas a usuario
- limitar el acceso para que cada usuario solo vea y modifique su propio contenido
- exportar en CSV la información de un tablero
- cargar una demo reproducible con un comando manual

He intentado que el alcance se quede en un punto razonable: suficiente para que la aplicación tenga sentido de verdad, pero sin añadir funciones que luego costaría justificar o mantener.

## Stack utilizado

El proyecto está construido con una base directa:

- Python
- Django
- SQLite en local
- configuración preparada por entorno para PostgreSQL
- plantillas HTML renderizadas en servidor
- CSS propio
- pruebas con `Django TestCase`

He preferido mantener el proyecto como una aplicación renderizada con Django, sin separar frontend ni abrir más capas de las que realmente hacían falta en esta etapa.

## Decisiones del proyecto

### Aplicación renderizada con Django

He optado por trabajar la aplicación directamente con Django y sus plantillas. Para este proyecto me parecía más útil reforzar bien la parte backend, los formularios, las vistas, los permisos y la relación entre modelos, antes que dividir la arquitectura con un frontend aparte.

### Alcance contenido

Una decisión importante ha sido no intentar aparentar más de lo que el proyecto necesita. He preferido una aplicación más contenida, pero bien resuelta en lo principal, antes que una app más grande solo sobre el papel.

### Demo reproducible

En vez de dejar la revisión del proyecto apoyada en una base SQLite con datos cargados manualmente, la aplicación incluye un comando `seed_demo` que crea o actualiza un espacio demo con datos realistas. Eso hace que el proyecto sea más cómodo de levantar y más claro de revisar.

### Preparación para el siguiente paso

El despliegue real todavía no forma parte de este cierre, pero sí he dejado la configuración orientada a trabajar por entorno, con SQLite como fallback local y con preparación limpia para PostgreSQL más adelante. La idea ha sido cerrar bien esta fase sin adelantar infraestructura que todavía no tocaba abrir.

## Cómo ejecutar el proyecto en local

### 1. Clonar el repositorio

    git clone <URL_DEL_REPOSITORIO>
    cd django-task-manager

### 2. Crear y activar un entorno virtual

En Linux o WSL:

    python -m venv .venv
    source .venv/bin/activate

En Windows:

    python -m venv .venv
    .venv\Scripts\activate

### 3. Instalar dependencias

    pip install -r requirements.txt

### 4. Crear el archivo de entorno

Puedes partir del archivo de ejemplo:

    cp .env.example .env

Si no se define una base de datos externa, el proyecto usará SQLite en local por defecto.

### 5. Aplicar migraciones

    python manage.py migrate

### 6. Cargar la demo opcional

Si quieres revisar la aplicación con contenido de ejemplo desde el principio:

    python manage.py seed_demo

### 7. Arrancar el servidor

    python manage.py runserver

La aplicación quedará disponible en la dirección local habitual de Django.

## Variables de entorno

El proyecto incluye un archivo `.env.example` con las variables principales:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DEMO_USER_PASSWORD`
- `DATABASE_URL`

También se puede definir la base de datos con variables separadas como `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT`, pero para desarrollo local no hace falta complicarse demasiado: si no se configura una base externa, la aplicación funciona con SQLite.

La intención aquí ha sido mantener una configuración simple para trabajar en local y, al mismo tiempo, dejar preparado el proyecto para un entorno posterior más serio cuando toque desplegarlo.

## Demo reproducible

La aplicación incorpora este comando:

    python manage.py seed_demo

Este comando crea o actualiza un espacio demo pensado para poder revisar la aplicación con contenido desde el principio. La demo incluye:

- 1 usuario demo
- 5 tableros
- 20 listas
- 50 tareas

El comando está planteado para no duplicar contenido del espacio demo cuando se ejecuta más de una vez y no modifica datos de otros usuarios.

Por defecto, las credenciales demo son:

- usuario: `demo`
- contraseña: `DemoAccess123!`

La contraseña se puede cambiar mediante la variable de entorno `DEMO_USER_PASSWORD`.

## Tests

El proyecto incluye una suite de pruebas para validar el comportamiento principal de la aplicación. En esta fase final también se han añadido pruebas específicas para el comando `seed_demo`, cubriendo casos como:

- creación desde una base vacía
- ejecuciones repetidas sin duplicados
- login del usuario demo
- no alteración de datos de otros usuarios
- conflicto con un usuario `demo` ajeno al espacio demo del comando

Para ejecutar los tests:

    python manage.py test

## Estado actual del proyecto

A día de hoy, el proyecto queda cerrado como una entrega funcional en local, con una demo reproducible y una configuración de entorno más limpia que depender simplemente de una base de datos ya rellenada a mano.

Todavía no incluye despliegue real, Docker, servidor configurado ni PostgreSQL funcionando en producción, porque ese no era el objetivo de esta fase. Lo que sí deja es una base mejor preparada para dar ese paso después de una forma ordenada.

## Aprendizajes

Este proyecto me ha servido para trabajar una parte bastante práctica de Django: construir una aplicación web completa, relacionar modelos, trabajar formularios, controlar permisos, validar flujos y acompañar todo eso con pruebas.

También me ha ayudado a pensar mejor el cierre de una entrega. No solo en hacer que una funcionalidad exista, sino en dejar el proyecto más fácil de revisar, más claro de levantar en local y mejor preparado para el siguiente paso sin mezclarlo todo antes de tiempo.

He intentado que el resultado final no se quede solo en una práctica de curso, sino en un proyecto pequeño, serio y explicable, que pueda enseñar con naturalidad y defender con honestidad.
