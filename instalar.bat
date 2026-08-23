@echo off
setlocal
REM ============================================================
REM  JARVIS - Instalador (una sola vez)
REM  Crea el entorno virtual "venv" dentro del proyecto e
REM  instala las dependencias. No toca nada global.
REM ============================================================
cd /d "%~dp0"

set "PY="

py -3.12 -c "pass" >nul 2>&1
if not errorlevel 1 set "PY=py -3.12"

if not defined PY (
  py -3.13 -c "pass" >nul 2>&1
  if not errorlevel 1 set "PY=py -3.13"
)

if not defined PY (
  py -3 -c "pass" >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)

if not defined PY (
  echo [X] No encontre Python. Instala Python 3.12 o 3.13 desde python.org
  echo     y vuelve a correr este archivo.
  pause
  exit /b 1
)

echo [OK] Usando: %PY%
%PY% -c "import sys; print('      Version:', sys.version.split()[0])"

if not exist venv (
  echo.
  echo Creando entorno virtual en .\venv ...
  %PY% -m venv venv
  if errorlevel 1 (
    echo [X] No pude crear el entorno virtual.
    pause
    exit /b 1
  )
)

echo.
echo Instalando dependencias (puede tardar unos minutos)...
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo [X] Fallo la instalacion de dependencias. Lee el error de arriba.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo [OK] Instalacion lista. Siguiente paso:
echo.
echo     venv\Scripts\python diagnostico.py --modelo
echo.
echo ============================================================
pause
