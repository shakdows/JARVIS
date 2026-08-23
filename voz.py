"""Voz de respuesta con pyttsx3 (las voces de Windows, offline).

La lectura corre en un hilo aparte y se puede cortar a media frase
con callar() — conectado a la tecla config.TECLA_CALLAR.
Se crea un motor nuevo por lectura: reutilizarlo tras un stop()
deja a pyttsx3 colgado en Windows.
"""

import threading

import config


class Voz:
    def __init__(self):
        self._motor = None
        self._candado = threading.Lock()

    def hablar(self, texto):
        """Lee el texto en voz alta sin bloquear. Corta la lectura anterior."""
        self.callar()
        threading.Thread(target=self._decir, args=(texto,), daemon=True).start()

    def _decir(self, texto):
        try:
            import pyttsx3

            motor = pyttsx3.init()
            with self._candado:
                self._motor = motor
            voz_id = self._buscar_voz(motor)
            if voz_id:
                motor.setProperty("voice", voz_id)
            motor.setProperty("rate", config.VOZ_VELOCIDAD)
            motor.say(texto)
            motor.runAndWait()
        except Exception as error:
            print(f"[!] Falló la voz: {error}")
        finally:
            with self._candado:
                self._motor = None

    def _buscar_voz(self, motor):
        voces = motor.getProperty("voices")
        preferida = config.VOZ_PREFERIDA.lower().strip()
        if preferida:
            for v in voces:
                if preferida in f"{v.id} {v.name}".lower():
                    return v.id
        for v in voces:
            etiqueta = f"{v.id} {v.name}".lower()
            if "spanish" in etiqueta or "es-" in etiqueta or "es_" in etiqueta:
                return v.id
        return None

    @property
    def hablando(self):
        return self._motor is not None

    def callar(self):
        with self._candado:
            if self._motor is not None:
                try:
                    self._motor.stop()
                except Exception:
                    pass
