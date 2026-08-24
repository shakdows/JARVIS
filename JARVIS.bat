@echo off
REM ============================================================
REM  Lanzador de JARVIS: doble clic y listo.
REM ============================================================
cd /d "%~dp0"

if not exist venv (
  echo [X] Falta instalar. Corre primero instalar.bat
  pause
  exit /b 1
)

title JARVIS
venv\Scripts\python jarvis.py

echo.
echo JARVIS se cerro.
pause
