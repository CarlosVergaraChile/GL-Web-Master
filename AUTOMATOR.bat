@echo off
REM ============================================
REM AUTOMATIZADOR MAESTRO - GL STRATEGIC
REM ============================================
REM Ejecuta el flujo de normalizacion y verificacion

setlocal enabledelayedexpansion
set "ROOT=%~dp0"
cd /d "%ROOT%"

REM Evitar problemas de encoding: usar solo ASCII en el menu
cls
echo.
echo =============================================================
echo                  AUTOMATIZADOR MAESTRO
echo -------------------------------------------------------------
echo   Normalizacion automatica de fotos - GL Strategic
echo =============================================================
echo.

echo Selecciona una opcion:
echo.
echo   [1] Opcion RAPIDA: Normalizar fotos (sin verificacion)
echo   [2] Opcion COMPLETA: Todo automaticamente (recomendado)
echo   [3] PROCESAR CON IA: Quitar fondos + normalizar fotos nuevas
echo   [4] AUDITORIA: Solo verificar que fotos faltan
echo   [5] MONITOR: Vigilar cambios en tiempo real
echo   [6] VER DOCUMENTACION (README)
echo   [7] SALIR
echo.

set /p option="Elige opcion (1-7): "

if "%option%"=="1" goto normalize
if "%option%"=="2" goto complete
if "%option%"=="3" goto rembg
if "%option%"=="4" goto audit
if "%option%"=="5" goto watchdog
if "%option%"=="6" goto docs
if "%option%"=="7" goto exit

echo ERROR: Opcion no valida
timeout /t 2 /nobreak >nul
goto :eof

:normalize
cls
echo [INFO] Normalizando fotos...
set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\normalize_all_photos.py"
) else (
	echo [WARN] No se encontro el interprete de la venv, usando 'python' del sistema
	python "%ROOT%\automatizaciones\normalize_all_photos.py"
)
echo [OK] Normalizacion completada
pause
goto :eof

:complete
cls
echo [INFO] Ejecutando flujo completo (post_process.ps1)...
REM Asegurar que PowerShell use el directorio raiz
powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-Location -LiteralPath '%ROOT%'; & '%ROOT%post_process.ps1'"
echo [OK] Flujo completo finalizado
pause
goto :eof

:rembg
cls
echo [INFO] Procesando fotos con IA (rembg) para quitar fondos...
echo.
echo Asegúrate de que las fotos estén en: assets\raw_linkedin_photos
echo.
set "PY=%ROOT%\.venv312\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\process_linkedin_photos.py"
) else (
	echo [ERROR] No se encontró Python 3.12 con rembg
	echo Ejecuta primero la opción de instalación
)
echo [OK] Procesamiento completado. Fotos en: assets\images
pause
goto :eof

:audit
cls
echo [INFO] Verificando estado de fotos...
set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\audit_fotos.py"
) else (
	echo [WARN] No se encontro el interprete de la venv, usando 'python' del sistema
	python "%ROOT%\automatizaciones\audit_fotos.py"
)
echo [OK] Auditoria finalizada
pause
goto :eof

:watchdog
cls
echo [INFO] Iniciando monitor en tiempo real (Ctrl+C para detener)...
set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\watchdog_fotos.py"
) else (
	echo [WARN] No se encontro el interprete de la venv, usando 'python' del sistema
	python "%ROOT%\automatizaciones\watchdog_fotos.py"
)
pause
goto :eof

:docs
cls
echo [INFO] Mostrando README_FOTOS.md
echo -------------------------------------------------------------
type "%ROOT%\automatizaciones\docs\README_FOTOS.md" | more
echo -------------------------------------------------------------
pause
goto :eof

:exit
echo.
echo [INFO] Saliendo...
timeout /t 1 /nobreak >nul
