"""Bips de aviso: agudo al empezar a grabar, grave al terminar.

Usa winsound (viene con Python en Windows, sin dependencias).
Los bips corren en un hilo aparte para no retrasar la grabación.
"""

import sys
import threading

import config

if sys.platform == "win32":
    import winsound


def _bip(hz, ms):
    if sys.platform != "win32":
        return
    threading.Thread(target=winsound.Beep, args=(hz, ms), daemon=True).start()


def bip_inicio():
    _bip(config.BIP_INICIO_HZ, config.BIP_INICIO_MS)


def bip_fin():
    _bip(config.BIP_FIN_HZ, config.BIP_FIN_MS)
