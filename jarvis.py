"""JARVIS — Fases 1 y 2.

F9  (mantener): dictado — el texto se pega donde tengas el cursor.
F10 (mantener): comando — le hablas a JARVIS y te contesta con voz.
Esc: corta la lectura en voz alta.
Ctrl+C en esta consola para salir.
"""

import threading

import keyboard
import pyperclip

import config
import herramientas
import portapapeles
import sonidos
from cerebro import Cerebro, CerebroNoDisponible
from grabadora import Grabadora
from transcriptor import Transcriptor
from voz import Voz


def main():
    print("=" * 52)
    print("  JARVIS — dictado (F9) y comandos (F10)")
    print("=" * 52)
    print("Cargando modelo Whisper (la primera vez se descarga)...")

    transcriptor = Transcriptor()
    grabadora = Grabadora()
    voz = Voz()

    try:
        cerebro = Cerebro()
    except CerebroNoDisponible as error:
        cerebro = None
        print(f"[!] Modo comando (F10) desactivado: {error}")

    modo_actual = [None]  # None, "dictado" o "comando"
    ocupado = threading.Lock()  # un procesamiento a la vez

    def al_presionar(modo):
        def manejador(_evento):
            # La tecla mantenida se auto-repite: solo cuenta la primera.
            if modo_actual[0] is not None or ocupado.locked():
                return
            if modo == "comando" and cerebro is None:
                print("[!] F10 está desactivado: falta el CLI de claude (mira arriba)")
                return
            voz.callar()  # si estaba hablando, el usuario tiene la palabra
            modo_actual[0] = modo
            try:
                grabadora.iniciar()
            except Exception as error:
                modo_actual[0] = None
                print(f"[X] No pude abrir el micrófono: {error}")
                return
            sonidos.bip_inicio()

        return manejador

    def al_soltar(modo):
        def manejador(_evento):
            if modo_actual[0] != modo:
                return
            audio = grabadora.detener()
            modo_actual[0] = None
            sonidos.bip_fin()
            segundos = len(audio) / config.FRECUENCIA_MUESTREO
            if segundos < config.DURACION_MINIMA_SEG:
                print("(grabación demasiado corta, ignorada)")
                return
            threading.Thread(target=procesar, args=(modo, audio), daemon=True).start()

        return manejador

    def procesar(modo, audio):
        with ocupado:
            try:
                texto = transcriptor.transcribir(audio)
            except Exception as error:
                print(f"[X] Falló la transcripción: {error}")
                return
            if not texto:
                print("(no se entendió nada)")
                return
            if modo == "dictado":
                print(f">> {texto}")
                portapapeles.pegar_texto(texto)
            else:
                comandar(texto)

    def comandar(texto):
        print(f"Tú: {texto}")
        print("(pensando...)")
        try:
            respuesta = cerebro.preguntar(texto)
        except Exception as error:
            print(f"[X] El cerebro falló: {error}")
            voz.hablar("Perdón, no pude procesar eso.")
            return

        # Ejecutar las acciones [ABRIR] y separar el texto normal.
        dichos = []
        resto = []
        for linea in respuesta.splitlines():
            limpia = linea.strip()
            if limpia.upper().startswith("[ABRIR]"):
                objetivo = limpia[len("[ABRIR]"):].strip()
                resultado = herramientas.abrir(objetivo)
                print(f"JARVIS: {resultado}")
                dichos.append(resultado)
            elif limpia:
                resto.append(limpia)

        texto_respuesta = " ".join(resto).strip()
        if texto_respuesta:
            print(f"JARVIS: {texto_respuesta}")
            if len(texto_respuesta) > config.RESPUESTA_LARGA_CARACTERES:
                pyperclip.copy(texto_respuesta)
                corte = texto_respuesta[: config.RESPUESTA_LARGA_CARACTERES]
                if ". " in corte:
                    corte = corte.rsplit(". ", 1)[0] + "."
                dichos.append(corte + " Te dejé la respuesta completa en el portapapeles.")
            else:
                dichos.append(texto_respuesta)

        if dichos:
            voz.hablar(" ".join(dichos))

    keyboard.on_press_key(config.TECLA_DICTADO, al_presionar("dictado"))
    keyboard.on_release_key(config.TECLA_DICTADO, al_soltar("dictado"))
    keyboard.on_press_key(config.TECLA_COMANDO, al_presionar("comando"))
    keyboard.on_release_key(config.TECLA_COMANDO, al_soltar("comando"))
    keyboard.on_press_key(config.TECLA_CALLAR, lambda _e: voz.callar())

    print()
    print(f"Listo.  {config.TECLA_DICTADO.upper()} = dictar   "
          f"{config.TECLA_COMANDO.upper()} = darle una orden   "
          f"{config.TECLA_CALLAR.upper()} = callarlo")
    print("Ctrl+C aquí para salir.")
    print()

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        voz.callar()
        print("\nHasta luego.")


if __name__ == "__main__":
    main()
