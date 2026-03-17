# DECISIONS

## 2026-03-13 — Proyecto B como pieza principal activa del reto

### Decisión
El Proyecto B queda confirmado como django-task-manager y pasa a ser la pieza principal activa del reto.

### Motivo
Aporta más valor directo a empleabilidad seguir construyendo una aplicación Django visible que seguir perdiendo tiempo en pulido marginal del Proyecto 1 o en práctica aislada sin salida clara de portfolio.

### Impacto práctico
- El foco actual del reto pasa a Django como pieza principal.
- El siguiente trabajo debe concentrarse en hacer el Proyecto B visible, serio y presentable.

### Estado
Vigente

## 2026-03-13 — Proyecto C como evolución pequeña del Proyecto B

### Decisión
El Proyecto C no debe convertirse en otro proyecto grande desde cero, sino en una evolución pequeña y coherente del propio Proyecto B.

### Motivo
Reduce dispersión y permite aprovechar mejor el trabajo ya construido.

### Impacto práctico
- Se evita abrir un tercer frente grande.
- Se refuerza la coherencia del portfolio.

### Estado
Vigente

## 2026-03-13 — Priorizar funcionalidad visible sobre perfeccionismo de configuración

### Decisión
En esta fase compensa más construir funcionalidad visible en Django que dedicar sesiones enteras a Git aislado o a perfeccionismo de configuración con poco retorno inmediato.

### Motivo
El objetivo del reto es empleabilidad funcional, no perfección técnica absoluta.

### Impacto práctico
- Git y GitHub se trabajan de forma práctica y vinculada al proyecto real.
- La siguiente capa útil después de Git será la primera interfaz web fuera del admin.

### Estado
Vigente

## 2026-03-13 — Terminal neutral y activación manual del entorno

### Decisión
El entorno de terminal no debe quedar secuestrado por activaciones globales en ~/.zshrc. Por ahora se trabajará con terminal neutral y activación manual del entorno adecuado según el proyecto.

### Motivo
La activación global previa generó fricción innecesaria entre proyectos y confundió el contexto real de trabajo.

### Impacto práctico
- Cada proyecto debe activar su entorno de forma explícita.
- Se evita seguir perdiendo tiempo en automatismos finos con poco retorno inmediato.

### Estado
Vigente

## 2026-03-13 — Método de colaboración con Codex

### Decisión
ChatGPT se usará para orquestar y revisar dirección. Codex se usará como ejecutor de tareas concretas, delimitadas y verificables dentro del repositorio abierto.

### Motivo
Este reparto reduce fricción, mejora precisión y encaja mejor con el trabajo real del proyecto.

### Impacto práctico
- Las tareas para Codex deben definirse con prompts cerrados.
- Toda salida relevante debe revisarse a nivel de archivos y validarse cuando proceda.

### Estado
Vigente

## 2026-03-13 — Las preferencias técnicas deben formularse como requisitos explícitos

### Decisión
Cuando se quiera que Codex implemente algo con una preferencia técnica concreta, esa preferencia debe formularse como requisito explícito y no dejarse implícita.

### Motivo
En la primera generación del modelo Task, algunos detalles importantes no se fijaron porque no se habían pedido de forma suficientemente cerrada.

### Impacto práctico
- Los prompts deben indicar archivo, requisitos obligatorios, restricciones y salida esperada.
- Se reduce el riesgo de correcciones evitables.

### Estado
Vigente

## 2026-03-16 — Dar por suficiente la base visual inicial del Proyecto B

### Decisión
La base visual actual de task_form y task_list se acepta como suficiente, uniforme y presentable para esta fase. No compensa seguir iterando diseño fino a ojo sobre este mismo bloque.

### Motivo
El objetivo actual es visibilidad funcional y coherencia general del producto, no perfeccionismo gráfico sobre una base ya suficiente.

### Impacto práctico
- Las siguientes iteraciones deben priorizar funcionalidad visible y continuidad del flujo.
- El criterio visual para próximos pasos será coherencia general y presentabilidad suficiente.
- No se reabre este bloque para pulido fino salvo necesidad clara.

### Estado
Vigente

## 2026-03-17 — Integrar Tailwind CSS por CLI simple sobre la capa visible actual

### Decisión
La mejora visual de la capa visible actual del CRUD fuera del admin se implementa con Tailwind CSS por CLI simple, sin PostCSS y sin introducir una toolchain frontend más compleja.

### Motivo
Permite elevar la presentabilidad del proyecto con una integración pequeña, mantenible y suficiente para un portfolio Django junior sin abrir un frente técnico innecesario.

### Impacto práctico
- npm queda limitado a lo necesario para compilar Tailwind.
- El CSS de entrada se mantiene dentro de los estáticos de tasks.
- El CSS compilado se sirve desde la ruta estática ya usada por las plantillas de la app.
- La base común de plantillas para esta integración se limita a tasks/templates/tasks/.

### Estado
Vigente
