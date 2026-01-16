@echo off
REM ============================================
REM GESTOR DE NOTICIAS - GL Strategic
REM ============================================
setlocal enabledelayedexpansion
set "ROOT=%~dp0.."
cd /d "%ROOT%"

cls
echo.
echo ===========================================================
echo              GESTOR DE NOTICIAS - GL Strategic
echo ===========================================================
echo.
echo Agregar, editar, eliminar noticias de LinkedIn
echo en el website dinamicamente
echo.

set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\gestor_noticias.py"
) else (
	echo [ERROR] Python no encontrado en %PY%
	pause
	goto :eof
)

echo.
pause
goto :eof
