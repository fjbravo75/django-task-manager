from dataclasses import dataclass
from datetime import date, timedelta


PRIORITY_LOW = "low"
PRIORITY_MEDIUM = "medium"
PRIORITY_HIGH = "high"

DEMO_USERNAME = "demo"
DEMO_EMAIL = "demo@django-task-manager.local"
DEMO_FIRST_NAME = "Demo"
DEMO_LAST_NAME = "Workspace"
DEFAULT_DEMO_PASSWORD = "DemoAccess123!"


@dataclass(frozen=True)
class DemoTaskDefinition:
    title: str
    description: str
    task_list: str
    priority: str
    due_in_days: int | None = None
    tags: tuple[str, ...] = ()
    assign_to_demo: bool = False

    def resolve_due_date(self, reference_date):
        if self.due_in_days is None:
            return None
        return reference_date + timedelta(days=self.due_in_days)


@dataclass(frozen=True)
class DemoBoardDefinition:
    name: str
    description: str
    task_lists: tuple[str, ...]
    tags: tuple[str, ...]
    tasks: tuple[DemoTaskDefinition, ...]


DEMO_BOARD_DEFINITIONS = (
    DemoBoardDefinition(
        name="Trabajo cliente web",
        description="Seguimiento semanal de mejoras, validaciones y entregas para un cliente recurrente.",
        task_lists=("Ideas", "Esta semana", "En revision", "Hecho"),
        tags=("Cliente", "Backend", "Frontend", "QA", "Urgente"),
        tasks=(
            DemoTaskDefinition(
                title="Revisar feedback del formulario de contacto",
                description="Agrupar comentarios del cliente antes de decidir ajustes.",
                task_list="Ideas",
                priority=PRIORITY_MEDIUM,
                due_in_days=3,
                tags=("Cliente", "Frontend"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Preparar alcance del sprint corto",
                description="Cerrar una lista breve de cambios asumibles esta semana.",
                task_list="Ideas",
                priority=PRIORITY_HIGH,
                due_in_days=2,
                tags=("Cliente", "Urgente"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Ajustar validacion del alta de leads",
                description="Evitar registros incompletos cuando faltan campos obligatorios.",
                task_list="Esta semana",
                priority=PRIORITY_HIGH,
                due_in_days=1,
                tags=("Backend", "Cliente"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Corregir desbordamiento en menu movil",
                description="Revisar el espaciado cuando el titulo del menu ocupa dos lineas.",
                task_list="Esta semana",
                priority=PRIORITY_MEDIUM,
                due_in_days=4,
                tags=("Frontend", "QA"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Revisar logs de errores 500",
                description="Comprobar si los ultimos fallos vienen del endpoint de contacto.",
                task_list="Esta semana",
                priority=PRIORITY_HIGH,
                due_in_days=0,
                tags=("Backend", "Urgente"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Validar copia final de la landing",
                description="Confirmar que los textos aprobados ya estan en la version de revision.",
                task_list="En revision",
                priority=PRIORITY_MEDIUM,
                due_in_days=2,
                tags=("Cliente", "QA"),
            ),
            DemoTaskDefinition(
                title="Confirmar envio del informe mensual",
                description="Dejar listo el correo con el resumen de cambios y proximos pasos.",
                task_list="En revision",
                priority=PRIORITY_LOW,
                due_in_days=5,
                tags=("Cliente",),
            ),
            DemoTaskDefinition(
                title="Cerrar ticket de favicon inconsistente",
                description="Verificado en escritorio y movil tras limpiar cache.",
                task_list="Hecho",
                priority=PRIORITY_LOW,
                due_in_days=-3,
                tags=("Frontend",),
            ),
            DemoTaskDefinition(
                title="Documentar cambios de checkout",
                description="Anotar que se modifico y que queda fuera del alcance actual.",
                task_list="Hecho",
                priority=PRIORITY_MEDIUM,
                due_in_days=-1,
                tags=("Backend", "Cliente"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Actualizar checklist de QA regresiva",
                description="Incluir comprobaciones rapidas para formulario, menu y tracking basico.",
                task_list="Hecho",
                priority=PRIORITY_MEDIUM,
                due_in_days=-5,
                tags=("QA",),
            ),
        ),
    ),
    DemoBoardDefinition(
        name="Formacion backend",
        description="Aprendizaje aplicado en Django, testing y preparacion gradual para PostgreSQL.",
        task_lists=("Pendiente", "En estudio", "En practica", "Cerrado"),
        tags=("Django", "Testing", "PostgreSQL", "Notas", "Arquitectura"),
        tasks=(
            DemoTaskDefinition(
                title="Repasar transacciones en Django",
                description="Entender donde conviene usar atomic y donde no aporta valor.",
                task_list="Pendiente",
                priority=PRIORITY_HIGH,
                due_in_days=6,
                tags=("Django", "PostgreSQL"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Leer sobre indices compuestos",
                description="Tomar notas de casos donde mejoran filtros y ordenaciones frecuentes.",
                task_list="Pendiente",
                priority=PRIORITY_MEDIUM,
                due_in_days=7,
                tags=("PostgreSQL", "Notas"),
            ),
            DemoTaskDefinition(
                title="Resumir diferencias entre TestCase y TransactionTestCase",
                description="Dejar una referencia rapida para futuras pruebas con comandos y transacciones.",
                task_list="Pendiente",
                priority=PRIORITY_MEDIUM,
                due_in_days=8,
                tags=("Testing", "Notas"),
            ),
            DemoTaskDefinition(
                title="Montar ejercicio de queryset optimizado",
                description="Practicar select_related y prefetch_related con un ejemplo pequeno.",
                task_list="En estudio",
                priority=PRIORITY_MEDIUM,
                due_in_days=3,
                tags=("Django", "Arquitectura"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Practicar managers personalizados",
                description="Crear un ejemplo corto para separar consultas frecuentes.",
                task_list="En estudio",
                priority=PRIORITY_LOW,
                due_in_days=5,
                tags=("Django",),
            ),
            DemoTaskDefinition(
                title="Comparar configuracion local y produccion",
                description="Anotar que variables de entorno necesita una app pequena antes de desplegar.",
                task_list="En practica",
                priority=PRIORITY_HIGH,
                due_in_days=4,
                tags=("Arquitectura", "PostgreSQL"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Escribir chuleta de comandos utiles",
                description="Recoger migraciones, tests puntuales y comandos de mantenimiento frecuentes.",
                task_list="En practica",
                priority=PRIORITY_LOW,
                tags=("Notas",),
            ),
            DemoTaskDefinition(
                title="Cerrar apuntes de validacion de formularios",
                description="Resumen corto de patrones utiles para formularios model y forms simples.",
                task_list="Cerrado",
                priority=PRIORITY_LOW,
                due_in_days=-2,
                tags=("Django", "Notas"),
            ),
            DemoTaskDefinition(
                title="Guardar ejemplo de test de comando",
                description="Tener una referencia rapida para futuros management commands.",
                task_list="Cerrado",
                priority=PRIORITY_MEDIUM,
                due_in_days=-1,
                tags=("Testing", "Django"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Anotar checklist para cambio a PostgreSQL",
                description="Separar lo que depende de entorno de lo que sigue igual con ORM.",
                task_list="Cerrado",
                priority=PRIORITY_MEDIUM,
                due_in_days=-4,
                tags=("PostgreSQL", "Arquitectura"),
            ),
        ),
    ),
    DemoBoardDefinition(
        name="Portfolio y CV",
        description="Bloque pequeno para mejorar presencia profesional sin abrir un proyecto paralelo.",
        task_lists=("Backlog", "Preparando", "Listo", "Publicado"),
        tags=("Portfolio", "CV", "Contenido", "Revision"),
        tasks=(
            DemoTaskDefinition(
                title="Revisar titular del perfil profesional",
                description="Ajustar el texto para que explique experiencia real sin exagerar.",
                task_list="Backlog",
                priority=PRIORITY_MEDIUM,
                due_in_days=6,
                tags=("CV", "Contenido"),
            ),
            DemoTaskDefinition(
                title="Ordenar proyectos por claridad tecnica",
                description="Poner primero los proyectos mejor explicables en una entrevista junior.",
                task_list="Backlog",
                priority=PRIORITY_MEDIUM,
                due_in_days=9,
                tags=("Portfolio",),
            ),
            DemoTaskDefinition(
                title="Definir captura principal del task manager",
                description="Elegir una vista que se entienda rapido y no dependa de explicaciones largas.",
                task_list="Preparando",
                priority=PRIORITY_HIGH,
                due_in_days=2,
                tags=("Portfolio", "Revision"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Pulir descripcion corta del proyecto kanban",
                description="Dejar un resumen breve centrado en Django, CRUD y autorizacion basica.",
                task_list="Preparando",
                priority=PRIORITY_MEDIUM,
                due_in_days=4,
                tags=("Portfolio", "Contenido"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Actualizar listado de tecnologias dominadas",
                description="Separar lo usado de verdad de lo que solo se ha tocado por encima.",
                task_list="Preparando",
                priority=PRIORITY_LOW,
                due_in_days=5,
                tags=("CV",),
            ),
            DemoTaskDefinition(
                title="Revisar tono del extracto personal",
                description="Evitar frases grandilocuentes y dejar un tono directo y defendible.",
                task_list="Listo",
                priority=PRIORITY_MEDIUM,
                due_in_days=3,
                tags=("CV", "Revision"),
            ),
            DemoTaskDefinition(
                title="Preparar mini guion para entrevista tecnica",
                description="Anotar como explicar decisiones de alcance, tests y despliegue futuro.",
                task_list="Listo",
                priority=PRIORITY_HIGH,
                due_in_days=7,
                tags=("Contenido", "Revision"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Publicar ajuste del enlace al portfolio",
                description="Verificar que el enlace funciona y no apunta a versiones antiguas.",
                task_list="Publicado",
                priority=PRIORITY_LOW,
                due_in_days=-2,
                tags=("Portfolio",),
            ),
            DemoTaskDefinition(
                title="Guardar version PDF del CV",
                description="Mantener una copia lista para enviar sin depender del editor online.",
                task_list="Publicado",
                priority=PRIORITY_LOW,
                due_in_days=-6,
                tags=("CV",),
            ),
            DemoTaskDefinition(
                title="Anotar mejoras futuras para la seccion de proyectos",
                description="Dejar pendientes que suman valor pero no son necesarias hoy.",
                task_list="Publicado",
                priority=PRIORITY_LOW,
                due_in_days=-1,
                tags=("Portfolio", "Contenido"),
            ),
        ),
    ),
    DemoBoardDefinition(
        name="Organizacion semanal",
        description="Tareas personales y de foco para combinar trabajo, estudio y descanso con mas orden.",
        task_lists=("Captura", "En marcha", "Esperando", "Hecho"),
        tags=("Rutina", "Salud", "Recados"),
        tasks=(
            DemoTaskDefinition(
                title="Planificar bloques de estudio del jueves",
                description="Reservar huecos realistas para teoria y practica sin saturar la tarde.",
                task_list="Captura",
                priority=PRIORITY_MEDIUM,
                due_in_days=2,
                tags=("Rutina",),
            ),
            DemoTaskDefinition(
                title="Anotar compra basica de la semana",
                description="Dejar lista corta para evitar varias salidas pequeñas.",
                task_list="Captura",
                priority=PRIORITY_LOW,
                due_in_days=1,
                tags=("Recados",),
            ),
            DemoTaskDefinition(
                title="Revisar presupuesto del mes",
                description="Comprobar gastos fijos y margen disponible antes de nuevas compras.",
                task_list="Captura",
                priority=PRIORITY_HIGH,
                due_in_days=4,
                tags=("Rutina",),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Preparar menu sencillo para tres dias",
                description="Pensar comidas que ayuden a ahorrar tiempo entre trabajo y estudio.",
                task_list="En marcha",
                priority=PRIORITY_LOW,
                due_in_days=3,
                tags=("Salud",),
            ),
            DemoTaskDefinition(
                title="Salir a caminar treinta minutos",
                description="Mantener una tarea visible para no dejarlo siempre al final del dia.",
                task_list="En marcha",
                priority=PRIORITY_MEDIUM,
                due_in_days=0,
                tags=("Salud",),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Ordenar bandeja de entrada personal",
                description="Vaciar correos pendientes y archivar lo que ya no necesita accion.",
                task_list="En marcha",
                priority=PRIORITY_MEDIUM,
                due_in_days=1,
                tags=("Rutina",),
            ),
            DemoTaskDefinition(
                title="Esperar confirmacion de cita medica",
                description="Pendiente de recibir hueco definitivo para la revision anual.",
                task_list="Esperando",
                priority=PRIORITY_HIGH,
                due_in_days=5,
                tags=("Salud",),
            ),
            DemoTaskDefinition(
                title="Esperar respuesta del casero sobre bombilla del portal",
                description="Recordatorio por si hace falta insistir a final de semana.",
                task_list="Esperando",
                priority=PRIORITY_LOW,
                due_in_days=6,
                tags=("Recados",),
            ),
            DemoTaskDefinition(
                title="Pagar recibo de internet",
                description="Gestion resuelta y comprobada en la banca online.",
                task_list="Hecho",
                priority=PRIORITY_MEDIUM,
                due_in_days=-4,
                tags=("Rutina",),
            ),
            DemoTaskDefinition(
                title="Renovar abono de transporte",
                description="Tarjeta activa para las proximas semanas.",
                task_list="Hecho",
                priority=PRIORITY_LOW,
                due_in_days=-7,
                tags=("Recados",),
            ),
        ),
    ),
    DemoBoardDefinition(
        name="Casa y gestiones",
        description="Pequena mezcla de mantenimiento domestico y tramites personales sin dramatizar tareas.",
        task_lists=("Pendiente", "Esta semana", "Compras", "Resuelto"),
        tags=("Casa", "Facturas", "Documentos"),
        tasks=(
            DemoTaskDefinition(
                title="Revisar contrato de luz",
                description="Comprobar permanencia y ultima subida antes de decidir cambios.",
                task_list="Pendiente",
                priority=PRIORITY_HIGH,
                due_in_days=8,
                tags=("Facturas", "Documentos"),
            ),
            DemoTaskDefinition(
                title="Anotar pequeñas reparaciones pendientes",
                description="Hacer lista corta para decidir si se resuelven este mes o el siguiente.",
                task_list="Pendiente",
                priority=PRIORITY_LOW,
                due_in_days=10,
                tags=("Casa",),
            ),
            DemoTaskDefinition(
                title="Comparar seguro del hogar",
                description="Guardar dos opciones realistas antes de renovar.",
                task_list="Pendiente",
                priority=PRIORITY_MEDIUM,
                due_in_days=12,
                tags=("Facturas", "Documentos"),
            ),
            DemoTaskDefinition(
                title="Pedir factura corregida del taller",
                description="Solicitar que aparezca el dato fiscal correcto antes de archivarla.",
                task_list="Esta semana",
                priority=PRIORITY_HIGH,
                due_in_days=2,
                tags=("Facturas", "Documentos"),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Llamar para revision de caldera",
                description="Cerrar fecha tentativa para no dejarlo a ultima hora.",
                task_list="Esta semana",
                priority=PRIORITY_MEDIUM,
                due_in_days=3,
                tags=("Casa",),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Comprar bombillas del salon",
                description="Elegir tono de luz neutro y revisar cuantas unidades faltan.",
                task_list="Compras",
                priority=PRIORITY_LOW,
                due_in_days=4,
                tags=("Casa",),
            ),
            DemoTaskDefinition(
                title="Comprar archivador para papeles",
                description="Separar facturas, contratos y documentos del coche.",
                task_list="Compras",
                priority=PRIORITY_LOW,
                due_in_days=5,
                tags=("Documentos",),
            ),
            DemoTaskDefinition(
                title="Guardar recibo del seguro medico",
                description="Documento archivado y pendiente ya cerrado.",
                task_list="Resuelto",
                priority=PRIORITY_LOW,
                due_in_days=-3,
                tags=("Documentos",),
            ),
            DemoTaskDefinition(
                title="Actualizar hoja de gastos fijos",
                description="Importes revisados con las ultimas facturas del mes.",
                task_list="Resuelto",
                priority=PRIORITY_MEDIUM,
                due_in_days=-2,
                tags=("Facturas",),
                assign_to_demo=True,
            ),
            DemoTaskDefinition(
                title="Llevar pilas usadas al punto limpio",
                description="Gestion pequena resuelta en el ultimo recado del barrio.",
                task_list="Resuelto",
                priority=PRIORITY_LOW,
                due_in_days=-6,
                tags=("Casa",),
            ),
        ),
    ),
)


def get_demo_totals():
    return {
        "boards": len(DEMO_BOARD_DEFINITIONS),
        "task_lists": sum(len(board.task_lists) for board in DEMO_BOARD_DEFINITIONS),
        "tasks": sum(len(board.tasks) for board in DEMO_BOARD_DEFINITIONS),
        "tagged_boards": sum(1 for board in DEMO_BOARD_DEFINITIONS if len(board.tags) > 3),
    }


def _validate_demo_dataset():
    totals = get_demo_totals()
    if totals["boards"] != 5:
        raise ValueError("The demo dataset must define exactly 5 boards.")
    if not 45 <= totals["tasks"] <= 60:
        raise ValueError("The demo dataset must define between 45 and 60 tasks.")
    if totals["tagged_boards"] < 2:
        raise ValueError("At least 2 boards must expose more than 3 tags.")

    for board in DEMO_BOARD_DEFINITIONS:
        if not 4 <= len(board.task_lists) <= 5:
            raise ValueError(f"{board.name} must define between 4 and 5 task lists.")

        list_names = set(board.task_lists)
        if len(list_names) != len(board.task_lists):
            raise ValueError(f"{board.name} has duplicated task list names.")

        tag_names = set(board.tags)
        if len(tag_names) != len(board.tags):
            raise ValueError(f"{board.name} has duplicated tag names.")

        seen_task_keys = set()
        for task in board.tasks:
            task_key = (task.task_list, task.title)
            if task.task_list not in list_names:
                raise ValueError(f"{task.title} points to an unknown task list in {board.name}.")
            if task_key in seen_task_keys:
                raise ValueError(f"{board.name} repeats the task {task.title!r} in {task.task_list!r}.")
            if not set(task.tags).issubset(tag_names):
                raise ValueError(f"{task.title} uses tags outside the board tag set.")
            if task.priority not in {PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH}:
                raise ValueError(f"{task.title} uses an unsupported priority value.")
            seen_task_keys.add(task_key)


_validate_demo_dataset()
