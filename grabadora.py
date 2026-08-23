"""Grabación desde el micrófono con sounddevice.

Se abre el stream al presionar la tecla y se cierra al soltarla.
El audio queda en memoria como float32 a 16 kHz, que es lo que
Whisper espera directamente (sin archivos temporales).
"""

import numpy as np
import sounddevice as sd

import config


class Grabadora:
    def __init__(self):
        self._trozos = []
        self._stream = None

    def iniciar(self):
        """Empieza a grabar. Lanza excepción si el micrófono no se puede abrir."""
        self._trozos = []
        self._stream = sd.InputStream(
            samplerate=config.FRECUENCIA_MUESTREO,
            channels=config.CANALES,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def _callback(self, indata, frames, tiempo, estado):
        self._trozos.append(indata.copy())

    def detener(self):
        """Para la grabación y devuelve el audio como arreglo 1-D float32."""
        if self._stream is None:
            return np.zeros(0, dtype=np.float32)
        try:
            self._stream.stop()
            self._stream.close()
        finally:
            self._stream = None
        if not self._trozos:
            return np.zeros(0, dtype=np.float32)
        audio = np.concatenate(self._trozos)
        self._trozos = []
        return audio[:, 0]
