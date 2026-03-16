# AGENTS.md

## 1. Propósito
Este repositorio forma parte de un portfolio de empleabilidad junior backend.
El objetivo es construir una aplicación Django clara, funcional y presentable, orientada a gestión de tareas, con valor real como pieza visible en GitHub.

## 2. Jerarquía de fuentes
1. Plan Maestro del reto
2. Seguimiento Activo del reto
3. Memoria local del repositorio
4. Prompt actual de la sesión

Si detectas conflicto entre la memoria local y la fuente estratégica, la memoria local debe corregirse.

## 3. Estructura de memoria local
- ./project_memory/CURRENT_CONTEXT.md
- ./project_memory/DECISIONS.md
- ./project_memory/SESSION_LOG.md

## 4. Política de lectura
Lectura obligatoria en cada actuación:
1. AGENTS.md
2. project_memory/CURRENT_CONTEXT.md

Lectura condicional:
- Leer DECISIONS.md si la tarea afecta criterio técnico, estructura, convenciones o decisiones previas.
- Leer SESSION_LOG.md si la tarea depende de continuidad reciente, trazabilidad o archivos tocados antes.

No leer todos los archivos por defecto.

## 5. Política de escritura
- No modificar AGENTS.md salvo cambio real del sistema de trabajo.
- Actualizar CURRENT_CONTEXT.md al cerrar un bloque útil o cambiar el estado actual.
- Añadir entrada en SESSION_LOG.md al cerrar una sesión o bloque con entidad.
- Añadir entrada en DECISIONS.md solo si se fija o cambia una decisión relevante.

## 6. Reglas de escritura
- Escribir con formato fijo.
- Escribir solo hechos, estado, decisiones y pendientes.
- No duplicar la misma información en varios archivos.
- No añadir texto narrativo innecesario.
- Si hay duda, no escribir.

## 7. Reglas técnicas del repo
- Mantener cambios pequeños y acotados.
- No abrir frentes nuevos sin indicación explícita.
- No añadir librerías ni complejidad innecesaria.
- Preferir soluciones simples, legibles y coherentes con Django.
- Antes de cerrar una tarea, comprobar integración básica y resultado esperado.
- Si se usa una preferencia técnica concreta, tratarla como requisito explícito y no implícito.

## 8. Método de trabajo
- ChatGPT se usa para orquestar, afinar criterio y revisar dirección.
- Codex se usa como ejecutor de tareas concretas, delimitadas y verificables dentro del repositorio abierto.
- Toda salida relevante debe revisarse a nivel de archivos y, cuando proceda, validarse ejecutando comandos o arrancando el proyecto.

## 9. Formato de salida del trabajo
Cuando completes una tarea:
1. Resume qué cambiaste.
2. Indica qué archivos tocaste.
3. Indica cómo validar el resultado.
4. Actualiza la memoria local si corresponde.
