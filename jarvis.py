"""JARVIS — Fase 1: dictado global.

Mantén F9 presionada, habla, suéltala: el texto se pega donde tengas
el cursor. Ctrl+C en esta consola para salir.
"""

import threading

import keyboard

import config
import portapapeles
import sonidos
from grabadora import Grabadora
from transcriptor import Transcriptor


def main():
    print("=" * 52)
    print("  JARVIS — Fase 1: dictado global")
    print("=" * 52)
    print("Cargando modelo Whisper (la primera vez se descarga)...")

    transcriptor = Transcriptor()
    grabadora = Grabadora()
    grabando = threading.Event()
    ocupado = threading.Lock()  # una transcripción a la vez

    def al_presionar(_evento):
        # La tecla mantenida dispara auto-repetición: solo cuenta la primera.
        if grabando.is_set() or ocupado.locked():
            return
        grabando.set()
        try:
            grabadora.iniciar()
        except Exception as error:
            grabando.clear()
            print(f"[X] No pude abrir el micrófono: {error}")
            return
        sonidos.bip_inicio()

    def al_soltar(_evento):
        if not grabando.is_set():
            return
        audio = grabadora.detener()
        grabando.clear()
        sonidos.bip_fin()
        segundos = len(audio) / config.FRECUENCIA_MUESTREO
        if segundos < config.DURACION_MINIMA_SEG:
            print("(grabación demasiado corta, ignorada)")
            return
        threading.Thread(target=procesar, args=(audio,), daemon=True).start()

    def procesar(audio):
        with ocupado:
            try:
                texto = transcriptor.transcribir(audio)
            except Exception as error:
                print(f"[X] Falló la transcripción: {error}")
                return
            if not texto:
                print("(no se entendió nada)")
                return
            print(f">> {texto}")
            portapapeles.pegar_texto(texto)

    keyboard.on_press_key(config.TECLA_DICTADO, al_presionar)
    keyboard.on_release_key(config.TECLA_DICTADO, al_soltar)

    print()
    print(f"Listo. Mantén {config.TECLA_DICTADO.upper()}, habla y suéltala.")
    print("El texto se pega donde tengas el cursor.")
    print("Ctrl+C aquí para salir.")
    print()

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nHasta luego.")


if __name__ == "__main__":
    main()
