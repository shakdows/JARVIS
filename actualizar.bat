@echo off
setlocal
REM ============================================================
REM  JARVIS - Actualizador
REM  Descarga la ultima version de los archivos del proyecto
REM  desde GitHub y actualiza las dependencias.
REM  No borra el venv ni tus datos.
REM ============================================================
cd /d "%~dp0"

set "RAMA=claude/jarvis-voice-assistant-7sh10d"
set "BASE=https://raw.githubusercontent.com/shakdows/JARVIS/%RAMA%"

for %%F in (config.py jarvis.py transcriptor.py grabadora.py portapapeles.py sonidos.py voz.py cerebro.py herramientas.py diagnostico.py requirements.txt instalar.bat README.md ESPECIFICACION.md) do (
  echo Descargando %%F ...
  curl -sSL -o "%%F" "%BASE%/%%F"
  if errorlevel 1 echo [X] No pude descargar %%F
)

REM El propio actualizador se descarga a un archivo temporal y se
REM reemplaza al final (no se puede sobrescribir mientras corre).
curl -sSL -o "actualizar.bat.nuevo" "%BASE%/actualizar.bat"

if exist venv (
  echo.
  echo Actualizando dependencias...
  venv\Scripts\python -m pip install -r requirements.txt
) else (
  echo [!] No existe el venv. Corre primero instalar.bat
)

echo.
(move /y "actualizar.bat.nuevo" "actualizar.bat" >nul 2>&1 & echo [OK] Actualizacion terminada. Siguiente paso: & echo(    venv\Scripts\python diagnostico.py --modelo & pause & exit /b 0)
