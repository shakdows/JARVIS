# ============================================================
#  JARVIS — Configuración central
#  Todas las constantes del proyecto viven aquí.
#  Si quieres cambiar una tecla, el modelo o el vocabulario,
#  este es el único archivo que hay que tocar.
# ============================================================

# --- Teclas ---
TECLA_DICTADO = "f9"        # mantener presionada para dictar, soltar para pegar
# TECLA_COMANDO = "f10"     # (Fase 2 — todavía no activa)

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
