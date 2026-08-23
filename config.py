# ============================================================
#  JARVIS — Configuración central
#  Todas las constantes del proyecto viven aquí.
#  Si quieres cambiar una tecla, el modelo o el vocabulario,
#  este es el único archivo que hay que tocar.
# ============================================================

# --- Teclas ---
TECLA_DICTADO = "f9"        # mantener presionada para dictar, soltar para pegar
TECLA_COMANDO = "f10"       # mantener presionada para dar una orden por voz
TECLA_CALLAR = "esc"        # corta la lectura en voz alta a media frase

# --- Audio ---
FRECUENCIA_MUESTREO = 16000  # Whisper trabaja a 16 kHz
CANALES = 1
DURACION_MINIMA_SEG = 0.3    # grabaciones más cortas se descartan (tecla rozada)

# --- Bips ---
BIP_INICIO_HZ = 1200         # agudo: empezó a grabar
BIP_INICIO_MS = 120
BIP_FIN_HZ = 440             # grave: terminó de grabar
BIP_FIN_MS = 150

# --- Modelo Whisper ---
MODELO = "small"               # si la precisión no alcanza, prueba "medium"
COMPUTE_GPU = "int8_float16"   # para "medium" en 4 GB de VRAM usa "int8"
COMPUTE_CPU = "int8"           # se usa solo si CUDA falla
IDIOMA = "es"

# Vocabulario que se le pasa al modelo como contexto para que
# reconozca bien los términos de programación mezclados con español.
VOCABULARIO = (
    "Estoy programando en español. Uso React, Supabase, Vercel, Three.js, "
    "TypeScript y Python. Hago deploy, commit y push al repositorio, "
    "creo un endpoint, un componente, una branch."
)

# --- Pegado ---
ESPERA_PEGADO_SEG = 0.4      # cuánto esperar tras Ctrl+V antes de restaurar
                             # el portapapeles anterior

# --- Cerebro (Fase 2: modo comando con F10) ---
MODELO_CEREBRO = ""            # vacío = el modelo por defecto de tu sesión de Claude Code
CONTINUAR_CONVERSACION = True  # mantiene el hilo de la charla mientras JARVIS esté abierto
TIMEOUT_CEREBRO_SEG = 120      # segundos máximos de espera por una respuesta

# --- Voz de respuesta ---
VOZ_PREFERIDA = "spanish"    # texto a buscar en el nombre de la voz de Windows
                             # (ej. "sabina", "helena"); "" = automática
VOZ_VELOCIDAD = 175          # palabras por minuto, aprox.

# Respuestas más largas que esto no se leen completas: se lee un resumen
# y el texto entero queda en el portapapeles.
RESPUESTA_LARGA_CARACTERES = 350

# --- Aplicaciones que JARVIS puede abrir por voz ---
# clave (como la dirías) -> ejecutable, ruta o URL.
# Ajusta las rutas a tu máquina si alguna no abre.
APLICACIONES = {
    "claude": r"%LOCALAPPDATA%\AnthropicClaude\claude.exe",
    "vs code": "code",
    "visual studio code": "code",
    "bloc de notas": "notepad",
    "calculadora": "calc",
    "explorador de archivos": "explorer",
    "navegador": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
}
