"""Pegado por portapapeles.

Todo texto se pega copiándolo al portapapeles y mandando Ctrl+V
(nunca simulando teclas letra por letra: el teclado físico no tiene
ñ ni tildes). Después se restaura lo que hubiera antes en el
portapapeles.
"""

import time

import keyboard
import pyperclip

import config


def pegar_texto(texto):
    try:
        anterior = pyperclip.paste()
    except pyperclip.PyperclipException:
        anterior = None  # había algo que no es texto (imagen, archivo)

    pyperclip.copy(texto)
    time.sleep(0.05)  # margen para que Windows registre el nuevo contenido
    keyboard.send("ctrl+v")
    time.sleep(config.ESPERA_PEGADO_SEG)

    if anterior is not None:
        try:
            pyperclip.copy(anterior)
        except pyperclip.PyperclipException:
            pass
