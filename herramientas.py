"""Acciones locales que JARVIS puede ejecutar.

Por ahora solo `abrir` (aplicaciones y URLs). En la Fase 3 se suman
las demás herramientas: listar_proyectos, buscar_en_codigo, etc.
Abrir una app no borra ni modifica nada, así que no pide confirmación.
"""

import os
import subprocess
import sys
import webbrowser

import config


def abrir(objetivo):
    """Abre una app conocida (clave de config.APLICACIONES) o una URL.

    Devuelve un texto corto para decir en voz alta.
    """
    objetivo = objetivo.strip().strip('"').strip()
    clave = objetivo.lower()
    destino = config.APLICACIONES.get(clave, objetivo)
    destino = os.path.expandvars(destino)

    if destino.startswith(("http://", "https://")):
        webbrowser.open(destino)
        return f"Abriendo {clave} en el navegador."

    try:
        if sys.platform == "win32":
            os.startfile(destino)  # respeta las asociaciones de Windows
        else:
            subprocess.Popen([destino])
        return f"Abriendo {clave}."
    except OSError:
        pass

    # Último intento: que lo resuelva el shell de Windows (apps en el PATH,
    # como "code" de VS Code).
    try:
        subprocess.Popen(f'start "" "{destino}"', shell=True)
        return f"Abriendo {clave}."
    except Exception as error:
        return f"No pude abrir {clave}: {error}"
