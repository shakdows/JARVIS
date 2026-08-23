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

REM La lista de archivos vive en el repositorio (archivos.txt), asi el
REM actualizador nunca se queda con una lista vieja.
curl -sSfL -o archivos.txt "%BASE%/archivos.txt"
if errorlevel 1 (
  echo [X] No pude descargar la lista de archivos. Revisa tu internet.
  pause
  exit /b 1
)

for /f "usebackq eol=# delims=" %%F in ("archivos.txt") do (
  echo Descargando %%F ...
  curl -sSfL -o "%%F" "%BASE%/%%F"
  if errorlevel 1 echo [X] No pude descargar %%F
)

REM El propio actualizador se descarga a un archivo temporal y se
REM reemplaza al final (no se puede sobrescribir mientras corre).
curl -sSfL -o "actualizar.bat.nuevo" "%BASE%/actualizar.bat"

if exist venv (
  echo.
  echo Actualizando dependencias...
  venv\Scripts\python -m pip install -r requirements.txt
) else (
  echo [!] No existe el venv. Corre primero instalar.bat
)

echo.
(move /y "actualizar.bat.nuevo" "actualizar.bat" >nul 2>&1 & echo [OK] Actualizacion terminada. Siguiente paso: & echo(    venv\Scripts\python diagnostico.py & pause & exit /b 0)
