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
    chequear_microfono()
    chequear_dependencias()
    if "--modelo" in sys.argv:
        chequear_modelo()
    else:
        print()
        print("Para probar también el modelo Whisper:")
        print("    venv\\Scripts\\python diagnostico.py --modelo")


if __name__ == "__main__":
    main()
