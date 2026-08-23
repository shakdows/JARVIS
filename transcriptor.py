"""Carga del modelo Whisper y transcripción de audio.

Intenta cargar el modelo en GPU (CUDA). Si algo falla —driver, DLLs,
memoria— cae solo a CPU y lo avisa en consola, sin crashear.

En Windows, las DLLs de cuBLAS y cuDNN vienen de los paquetes pip
nvidia-cublas-cu12 y nvidia-cudnn-cu12; hay que exponer sus rutas con
os.add_dll_directory() ANTES de importar faster_whisper.
"""

import os
import sys
from pathlib import Path

import numpy as np

import config


def _preparar_dlls_cuda():
    # La estructura interna de los paquetes de NVIDIA cambia entre
    # versiones, así que se busca cualquier carpeta que contenga DLLs
    # bajo site-packages/nvidia en vez de asumir una ruta fija.
    if sys.platform != "win32":
        return
    base = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    if not base.is_dir():
        return
    carpetas = sorted({dll.parent for dll in base.rglob("*.dll")})
    for carpeta in carpetas:
        os.add_dll_directory(str(carpeta))
    # Refuerzo vía PATH: algunas DLLs se cargan por dependencia indirecta
    # y Windows solo las resuelve buscando en PATH.
    if carpetas:
        os.environ["PATH"] = (
            os.pathsep.join(str(c) for c in carpetas)
            + os.pathsep
            + os.environ.get("PATH", "")
        )


_preparar_dlls_cuda()

from faster_whisper import WhisperModel  # noqa: E402  (después de las DLLs)


class Transcriptor:
    def __init__(self):
        self.dispositivo = None  # "GPU" o "CPU", se fija al cargar
        self.modelo = self._cargar()

    def _cargar(self):
        try:
            modelo = WhisperModel(
                config.MODELO,
                device="cuda",
                compute_type=config.COMPUTE_GPU,
            )
            # Transcribir medio segundo de silencio obliga a ejecutar los
            # kernels de CUDA de verdad: si cuDNN o la VRAM fallan, falla
            # aquí y no a mitad de un dictado.
            silencio = np.zeros(config.FRECUENCIA_MUESTREO // 2, dtype=np.float32)
            segmentos, _ = modelo.transcribe(silencio, language=config.IDIOMA)
            list(segmentos)
            self.dispositivo = "GPU"
            print(f"[OK] Modelo '{config.MODELO}' cargado en GPU (CUDA, {config.COMPUTE_GPU})")
            return modelo
        except Exception as error:
            print(f"[!] CUDA no funcionó: {error}")
            print("[!] Usando CPU. El dictado va a tardar más de lo normal.")

        modelo = WhisperModel(
            config.MODELO,
            device="cpu",
            compute_type=config.COMPUTE_CPU,
        )
        self.dispositivo = "CPU"
        print(f"[OK] Modelo '{config.MODELO}' cargado en CPU ({config.COMPUTE_CPU})")
        return modelo

    def transcribir(self, audio):
        """Recibe audio float32 a 16 kHz y devuelve el texto (str)."""
        segmentos, _info = self.modelo.transcribe(
            audio,
            language=config.IDIOMA,
            initial_prompt=config.VOCABULARIO,
            beam_size=5,
            vad_filter=True,
        )
        return " ".join(s.text.strip() for s in segmentos).strip()
