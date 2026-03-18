# AGENTS.md

## 1. Propósito

Este repositorio forma parte de un reto de empleabilidad junior backend orientado a Python, SQL, Django, GitHub y despliegue básico.

El objetivo del proyecto es construir una aplicación Django clara, funcional, presentable y defendible, con valor real como pieza de portfolio. En su fase actual, debe evolucionar como una aplicación Django server-rendered de gestión de tareas tipo kanban, con alcance razonable y validación real.

## 2. Alcance real de este agente

Este agente trabaja solo sobre el repositorio local abierto.

No tiene acceso directo a fuentes externas al repo salvo que el prompt actual las resuma o pegue explícitamente.

Debe basarse en este orden:

1. prompt actual de la sesión
2. `AGENTS.md`
3. memoria local del repositorio
4. estado real comprobable del código

## 3. Jerarquía operativa local

Dentro del repositorio, la referencia es esta:

1. prompt actual
2. `AGENTS.md`
3. `project_memory/CURRENT_CONTEXT.md`
4. `project_memory/DECISIONS.md` solo si la tarea afecta criterio técnico, estructura o convenciones
5. `project_memory/SESSION_LOG.md` solo si la tarea depende de continuidad reciente o cierre operativo
6. estado real del repositorio

Si el prompt actual contradice la memoria local, prevalece el prompt actual.

Si la memoria local contradice el estado real del repo, debe priorizarse el estado real y corregir la memoria solo si corresponde al cierre de la tarea.

## 4. Memoria local

La memoria local se compone de:

- `project_memory/CURRENT_CONTEXT.md`
- `project_memory/DECISIONS.md`
- `project_memory/SESSION_LOG.md`

### Función de cada archivo

**`CURRENT_CONTEXT.md`**  
Resume el estado operativo actual: bloque activo, siguiente paso exacto, restricciones y archivos foco.

**`DECISIONS.md`**  
Guarda decisiones técnicas o de criterio que deban seguir vigentes.

**`SESSION_LOG.md`**  
Registra sesiones o bloques con entidad suficiente para dejar trazabilidad útil.

## 5. Reglas de lectura

Leer siempre antes de actuar:

- `AGENTS.md`
- `project_memory/CURRENT_CONTEXT.md`

Leer `project_memory/DECISIONS.md` solo si la tarea afecta arquitectura, estructura, criterio técnico o convenciones.

Leer `project_memory/SESSION_LOG.md` solo si la tarea depende de continuidad reciente, trazabilidad o cierre de sesión.

No leer más memoria ni más repo de lo necesario.

## 6. Reglas de escritura

Actualizar memoria solo cuando haya motivo real y comprobable.

### `CURRENT_CONTEXT.md`
Actualizar solo si cambió el estado operativo actual del repo.

### `DECISIONS.md`
Actualizar solo si se fijó o cambió una decisión relevante.

### `SESSION_LOG.md`
Añadir entrada solo si la sesión tuvo entidad suficiente para dejar continuidad útil.

No escribir por rutina.  
No inventar.  
No registrar hipótesis como hechos.  
No duplicar información sin motivo claro.

## 7. Reglas de ejecución

- Mantener cambios pequeños y acotados.
- No abrir frentes nuevos sin indicación explícita.
- No añadir complejidad innecesaria.
- Preferir soluciones simples, legibles y coherentes con Django.
- No interpretar “subir nivel” como añadir tecnología por lucimiento.
- Si una tarea aparentemente pequeña exige rediseño previo, detenerse y explicarlo.

## 8. Ejecutar o planificar primero

### Ejecutar directamente
Cuando la tarea sea concreta, local, de poco riesgo y con validación clara.

### Planificar primero
Cuando la tarea sea estructural, ambigua, transversal, delicada o con varias alternativas razonables.

Si el prompt dice “no ejecutes todavía y propón plan”, no debe tocarse ningún archivo.

## 9. Reglas específicas del proyecto actual

Mientras el prompt no indique otra cosa:

- mantener aplicación Django server-rendered
- no abrir frontend separado
- no introducir React, Vue, websockets ni complejidad de frontend innecesaria
- priorizar funcionalidad visible, claridad, estructura y presentabilidad
- priorizar núcleo funcional antes que extras
- mantener coherencia con una aplicación tipo kanban razonable y defendible

## 10. Validación

Ninguna tarea debe darse por cerrada sin validación mínima coherente con el cambio realizado.

Según el caso, validar con una o varias de estas acciones:

- `python manage.py check`
- `python manage.py makemigrations` si procede
- `python manage.py migrate` si procede
- comprobación de imports
- arranque del servidor
- verificación de ruta o flujo afectado
- validación de formulario o CRUD
- revisión de `git status` o `git diff`

La validación debe ser real, no asumida.

Si algo no se pudo validar, debe decirse.

## 11. Reglas de alcance

Trabajar solo dentro del alcance definido por el prompt.

Si el prompt delimita archivos o carpetas, no salir de esa zona.

Si el prompt prohíbe tocar ciertos archivos, no tocarlos.

Si para completar bien la tarea hubiera que salir del alcance, explicarlo primero y no improvisar cambios.

## 12. Cierre

Al terminar una tarea, la salida debe indicar de forma breve y técnica:

1. qué se cambió
2. qué archivos se tocaron
3. cómo se validó
4. si se actualizó memoria local y por qué
5. desde qué punto exacto puede retomarse la siguiente sesión

No presentar como validado algo que no se comprobó.

## 13. Instrucción final

Si una tarea depende de contexto estratégico externo al repositorio, ese contexto debe venir ya resumido dentro del prompt actual.

Este agente no debe asumir acceso a fuentes externas.

Su trabajo consiste en ejecutar bien dentro del alcance real disponible: prompt actual, memoria local y estado real del repositorio.