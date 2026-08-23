"""El cerebro del modo comando (Fase 2).

Manda la petición al CLI de Claude Code en modo headless (claude -p)
y devuelve la respuesta. Reutiliza la sesión de Claude Code ya iniciada
en la máquina: no hay que manejar ninguna clave de API.

Al arrancar se verifica con `claude --help` que el flag --print exista
de verdad, en vez de asumirlo.
"""

import os
import shutil
import subprocess
import sys

import config


class CerebroNoDisponible(Exception):
    pass


def encontrar_claude():
    """Busca el ejecutable de Claude Code aunque no esté en el PATH."""
    ruta = shutil.which("claude")
    if ruta:
        return ruta
    if sys.platform == "win32":
        candidatos = [
            os.path.expandvars(r"%USERPROFILE%\.local\bin\claude.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\claude\claude.exe"),
        ]
        for candidato in candidatos:
            if os.path.isfile(candidato):
                return candidato
    return None


def _armar_prompt(texto):
    claves = ", ".join(sorted(config.APLICACIONES))
    return (
        "Eres JARVIS, el asistente de voz local de esta máquina con Windows. "
        "Tu respuesta se lee en voz alta: responde en español, en una a tres "
        "frases, sin listas ni formato markdown. "
        "Si el usuario pide abrir una aplicación o una página web, tu "
        "respuesta debe ser SOLO una línea con este formato exacto: "
        "[ABRIR] objetivo — donde objetivo es una de estas claves: "
        f"{claves}; o bien una URL completa que empiece con https://. "
        "Si pide abrir varias cosas, una línea [ABRIR] por cada una. "
        "Para cualquier otra petición, contesta normal.\n\n"
        "Petición dicha por voz (puede traer pequeños errores de "
        f'transcripción): "{texto}"'
    )


class Cerebro:
    def __init__(self):
        self.ruta = encontrar_claude()
        if not self.ruta:
            raise CerebroNoDisponible(
                "no encontré el comando 'claude'. Instala Claude Code en esta "
                "máquina e inicia sesión una vez (https://claude.com/claude-code)."
            )
        try:
            ayuda = self._correr(["--help"], timeout=30)
        except Exception as error:
            raise CerebroNoDisponible(f"'claude --help' falló: {error}")
        if "--print" not in ayuda:
            raise CerebroNoDisponible(
                "tu versión del CLI de claude no tiene el modo --print; actualízala."
            )
        self._primera_pregunta = True
        print(f"[OK] Cerebro listo: {self.ruta}")

    def _correr(self, args, timeout):
        extras = {}
        if sys.platform == "win32":
            extras["creationflags"] = subprocess.CREATE_NO_WINDOW
        resultado = subprocess.run(
            [self.ruta, *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            **extras,
        )
        if resultado.returncode != 0:
            detalle = (resultado.stderr or resultado.stdout or "").strip()
            raise RuntimeError(detalle[:500] or f"claude terminó con código {resultado.returncode}")
        return resultado.stdout.strip()

    def preguntar(self, texto):
        args = []
        if config.CONTINUAR_CONVERSACION and not self._primera_pregunta:
            args.append("--continue")
        if config.MODELO_CEREBRO:
            args += ["--model", config.MODELO_CEREBRO]
        args += ["-p", _armar_prompt(texto)]
        respuesta = self._correr(args, timeout=config.TIMEOUT_CEREBRO_SEG)
        self._primera_pregunta = False
        return respuesta
