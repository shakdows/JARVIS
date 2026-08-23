# JARVIS — asistente de voz local

Especificación del proyecto. Claude Code: lee esto completo antes de escribir
código. Se construye **por fases**; no empieces una fase sin que la anterior
esté probada y funcionando.

---

## Contexto de la máquina

- ASUS TUF Gaming A15 (FA506NCR), Windows 11 Home 25H2
- AMD Ryzen 7 7435HS · 16 GB RAM
- NVIDIA GeForce RTX 3050 Laptop GPU, **4 GB de VRAM** (límite real, respétalo)
- Python 3.13.7 instalado — verifica con `py -0` qué otras versiones hay
- Teclado físico australiano (layout US, sin ñ ni tildes); escribo en español
- Uso personal, proyectos de programación

## Reglas que aplican a todo el proyecto

1. **Verifica, no asumas.** Antes de instalar, comprueba versiones, driver
   NVIDIA, micrófono. Si algo falla, lee el error real y arréglalo.
2. **Todo pegado va por portapapeles** (copiar + Ctrl+V), nunca simulando
   teclas: mi teclado no tiene ñ ni acentos.
3. **Todo lo local.** El audio no sale de la máquina.
4. **Confirmación antes de escribir.** Leer lo que quiera; cualquier acción
   que borre, envíe, publique o modifique archivos me pregunta primero.
5. **Nada global sin permiso.** Todo en un entorno virtual dentro del
   proyecto. Pregúntame antes de tocar configuración de Windows.
6. **Explícame en español, sin tecnicismos de más.**
7. **Un archivo de configuración** (`config.py`) con todas las constantes
   arriba: teclas, rutas, modelo, vocabulario. Nada quemado en el código.

---

## FASE 1 — Dictado global

Mantengo **F9**, hablo, la suelto, el texto se pega donde tenga el cursor.

- `faster-whisper` sobre CUDA. Modelo `small`, `compute_type="int8_float16"`.
  Si la precisión no alcanza, prueba `medium` con `int8` (también entra en 4 GB).
- En Windows hace falta instalar `nvidia-cublas-cu12` y `nvidia-cudnn-cu12`, y
  exponer sus rutas con `os.add_dll_directory()` **antes** de importar
  faster_whisper.
- Si CUDA falla, cae solo a CPU y avisa en consola. No crashea.
- Restaura mi portapapeles anterior después de pegar.
- Bip agudo al empezar a grabar, grave al terminar.
- `initial_prompt` configurable con vocabulario de programación en español
  mezclado con inglés: React, Supabase, Vercel, Three.js, deploy, commit,
  endpoint, repositorio, componente.

**Prueba:** dicto una frase con ñ y tildes en el Bloc de notas y sale limpia.
Debe decir que arrancó en GPU, no en CPU.

---

## FASE 2 — Modo comando (voz → acción)

Segunda tecla, **F10**: en vez de pegar el texto, lo manda al modelo, que
decide qué hacer, y me contesta hablado.

- **Cerebro:** usa el CLI de Claude Code en modo headless desde Python
  (algo como `claude -p "..."`). Verifica el flag correcto con `claude --help`
  antes de escribirlo — no lo adivines. Así reutiliza mi sesión y no hace
  falta manejar una clave de API.
- **Voz de respuesta:** `pyttsx3` (usa las voces de Windows, offline, cero
  configuración). Si la voz en español suena mal, evaluamos otra opción
  después — no te distraigas con esto ahora.
- Las respuestas largas no se leen completas: dice un resumen y deja el texto
  completo en el portapapeles.
- Ctrl+C o una tecla corta la lectura en voz alta a media frase.

**Prueba:** pregunto algo por voz y me responde hablado en menos de 5 segundos.

---

## FASE 3 — Herramientas propias

Aquí está el valor real: que el asistente toque **mis** cosas. Expónlas como
funciones que el modelo pueda invocar (servidor MCP local si es lo más limpio,
o funciones directas si resulta más simple — tú decides y me explicas por qué).

Herramientas mínimas:

| Herramienta | Qué hace |
|---|---|
| `listar_proyectos` | Escanea mi carpeta de repos: nombre, rama actual, si hay cambios sin commitear, último commit |
| `abrir_proyecto` | Abre una carpeta en VS Code |
| `buscar_en_codigo` | Busca un texto en todos mis proyectos (ripgrep si está disponible) |
| `resumen_del_dia` | Todos los commits que hice hoy, en todos los repos |
| `nota_rapida` | Agrega una línea con fecha a `notas.md` |
| `abrir` | Abre una app o una URL |
| `estado_pc` | Disco libre, RAM, batería, temperatura y uso de GPU |

Todas las rutas van en `config.py`. Pregúntame dónde tengo mis repos antes de
inventar una ruta.

**Prueba:** digo "¿qué proyectos tengo con cambios sin subir?" y me responde
bien, hablado.

---

## FASE 4 — Que arranque y actúe solo

- Arranque con Windows sin ventana de consola: acceso directo en
  `shell:startup` apuntando a `pythonw.exe` del entorno virtual.
- Un icono en la bandeja del sistema (`pystray`) con: estado, pausar, salir.
  Sin esto no sé si está corriendo.
- **Brief matutino** vía Programador de tareas de Windows: a las 7 a.m. arma
  un resumen (proyectos con cambios pendientes, commits de ayer, espacio en
  disco si baja de 40 GB) y lo deja en un archivo. Que no me hable sin que yo
  se lo pida — la notificación pasiva se agradece, la voz sorpresa no.

---

## FASE 5 — Memoria

- Un `memoria.md` local con lo que le voy contando: en qué proyecto ando, mis
  preferencias, atajos que uso.
- Se lee al arrancar y se le pasa al modelo como contexto.
- Solo escribe ahí cuando se lo pido explícitamente ("recuerda que...").

---

## Cómo quiero que trabajemos

Al terminar cada fase: párate, dime qué quedó funcionando, cómo lo pruebo, y
espera mi visto bueno antes de seguir con la siguiente.

Al final de todo: dos líneas de cómo lo arranco mañana.
