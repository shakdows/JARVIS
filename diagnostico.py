"""Chequeos previos: Python, GPU, micrófono y dependencias.

Uso (desde la carpeta del proyecto):

    venv\\Scripts\\python diagnostico.py            -> chequeos rápidos
    venv\\Scripts\\python diagnostico.py --modelo   -> además descarga y
                                                      prueba el modelo Whisper
                                                      (la primera vez baja ~500 MB)
"""

import platform
import subprocess
import sys

OK = "[OK]"
MAL = "[X] "
AVISO = "[!] "


def chequear_python():
    version = platform.python_version()
    mayor, menor = sys.version_info[:2]
    if mayor == 3 and 10 <= menor <= 13:
        print(f"{OK} Python {version}")
    else:
        print(f"{AVISO} Python {version}: probado con 3.10–3.13, otra versión puede dar problemas")


def chequear_gpu():
    try:
        salida = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=15,
        )
    except FileNotFoundError:
        print(f"{MAL} nvidia-smi no encontrado: el driver de NVIDIA no está instalado o no está en el PATH")
        return
    except Exception as error:
        print(f"{MAL} No pude consultar la GPU: {error}")
        return
    if salida.returncode != 0:
        print(f"{MAL} nvidia-smi falló: {salida.stderr.strip()}")
        return
    print(f"{OK} GPU: {salida.stdout.strip()}")


def chequear_dlls_cuda():
    """Verifica que las DLLs de cuBLAS/cuDNN estén instaladas en el venv."""
    if sys.platform != "win32":
        return
    from pathlib import Path

    base = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    if not base.is_dir():
        print(f"{MAL} Faltan los paquetes CUDA de pip (no existe {base})")
        print("      Corre: venv\\Scripts\\python -m pip install -r requirements.txt")
        return
    dlls = list(base.rglob("*.dll"))
    cublas = next((d for d in dlls if d.name.lower().startswith("cublas64")), None)
    cudnn = next((d for d in dlls if d.name.lower().startswith("cudnn64")), None)
    if cublas:
        print(f"{OK} cuBLAS: {cublas}")
    else:
        print(f"{MAL} No encontré cublas64_*.dll dentro de {base}")
    if cudnn:
        print(f"{OK} cuDNN: {cudnn}")
    else:
        print(f"{MAL} No encontré cudnn64_*.dll dentro de {base}")
    if not cublas or not cudnn:
        print("      Corre: venv\\Scripts\\python -m pip install -r requirements.txt")
        if dlls:
            print("      DLLs que sí están:")
            for d in dlls[:20]:
                print(f"        {d.relative_to(base)}")


def chequear_microfono():
    try:
        import sounddevice as sd
    except Exception as error:
        print(f"{MAL} No se pudo importar sounddevice: {error}")
        return
    try:
        indice = sd.default.device[0]
        if indice is None or indice < 0:
            print(f"{MAL} No hay micrófono por defecto configurado en Windows")
            return
        dispositivo = sd.query_devices(indice)
        print(f"{OK} Micrófono por defecto: {dispositivo['name']}")
    except Exception as error:
        print(f"{MAL} No pude consultar el micrófono: {error}")


def chequear_dependencias():
    faltan = []
    for paquete in ("numpy", "keyboard", "pyperclip"):
        try:
            __import__(paquete)
        except ImportError:
            faltan.append(paquete)
    try:
        import transcriptor  # esto prepara las DLLs de CUDA e importa faster_whisper
        _ = transcriptor
    except ImportError as error:
        faltan.append(f"faster_whisper ({error})")
    if faltan:
        print(f"{MAL} Faltan dependencias: {', '.join(faltan)} — corre instalar.bat de nuevo")
    else:
        print(f"{OK} Todas las dependencias instaladas")


def chequear_cerebro():
    """Verifica el CLI de Claude Code para el modo comando (F10)."""
    import shutil

    ruta = shutil.which("claude")
    if not ruta:
        print(f"{AVISO} No encontré el comando 'claude': el modo comando (F10) no va a funcionar")
        print("      Instala Claude Code (https://claude.com/claude-code) e inicia sesión una vez.")
        return
    try:
        salida = subprocess.run(
            [ruta, "--help"], capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace",
        )
        if "--print" in (salida.stdout or ""):
            print(f"{OK} CLI de Claude Code listo (modo --print disponible): {ruta}")
        else:
            print(f"{AVISO} 'claude' existe pero no veo el modo --print; actualiza Claude Code")
    except Exception as error:
        print(f"{MAL} 'claude --help' falló: {error}")


def chequear_voz():
    """Verifica pyttsx3 y busca una voz en español de Windows."""
    if sys.platform != "win32":
        return
    try:
        import pyttsx3

        motor = pyttsx3.init()
        voces = motor.getProperty("voices")
        en_espanol = [
            v.name for v in voces
            if "spanish" in f"{v.id} {v.name}".lower()
            or "es-" in f"{v.id} {v.name}".lower()
            or "es_" in f"{v.id} {v.name}".lower()
        ]
        if en_espanol:
            print(f"{OK} Voz en español disponible: {en_espanol[0]}")
        else:
            nombres = ", ".join(v.name for v in voces[:5])
            print(f"{AVISO} No hay voz en español instalada; se usará la primera disponible ({nombres})")
            print("      Puedes agregar una en Configuración → Hora e idioma → Voz")
    except Exception as error:
        print(f"{MAL} pyttsx3 no funcionó: {error}")


def chequear_modelo():
    print()
    print("Cargando el modelo Whisper (la primera vez se descarga, ten paciencia)...")
    from transcriptor import Transcriptor

    t = Transcriptor()
    if t.dispositivo == "GPU":
        print(f"{OK} El modelo corre en GPU: todo listo para dictar rápido")
    else:
        print(f"{AVISO} El modelo corre en CPU: funciona, pero lento. Revisa los mensajes de arriba.")


def main():
    print("JARVIS — diagnóstico")
    print("-" * 40)
    chequear_python()
    chequear_gpu()
    chequear_dlls_cuda()
    chequear_microfono()
    chequear_dependencias()
    chequear_cerebro()
    chequear_voz()
    if "--modelo" in sys.argv:
        chequear_modelo()
    else:
        print()
        print("Para probar también el modelo Whisper:")
        print("    venv\\Scripts\\python diagnostico.py --modelo")


if __name__ == "__main__":
    main()
