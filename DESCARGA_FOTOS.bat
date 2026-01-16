@echo off
REM ============================================
REM AUTOMATIZADOR FOTOGRACIAS - OPCION FINAL
REM ============================================
setlocal enabledelayedexpansion
set "ROOT=%~dp0"
cd /d "%ROOT%"

cls
echo.
echo ===========================================================
echo           DESCARGA FOTOS - PROCESA AUTOMATICAMENTE
echo ===========================================================
echo.
echo Como usar:
echo 1. Descarga fotos de LinkedIn normalmente desde el navegador
echo    (sitio en navegador, click derecho en foto, Guardar imagen)
echo.
echo 2. Este script detecta y procesa automaticamente:
echo    - Redimensiona a 1000x1000px
echo    - Mejora brillo y contraste
echo    - Guarda como PNG
echo    - Aparecen en el website al instante
echo.
echo Ventaja: Sin bloqueos de LinkedIn, sin CAPTCHA
echo.
echo [1] INICIAR MONITOR (Esperar descargas)
echo [2] PROCESAR AHORA (Procesar fotos en Downloads)
echo [3] VER DESCARGAS (Abrir carpeta Downloads)
echo [4] SALIR
echo.

set /p option="Opcion: "

if "%option%"=="1" goto start_monitor
if "%option%"=="2" goto process_now
if "%option%"=="3" goto open_downloads
if "%option%"=="4" goto :eof

echo ERROR
timeout /t 1 /nobreak >nul
goto :eof

:start_monitor
cls
echo [INFO] Monitor iniciado - Solo actualiza fotos que cambiaron
echo [INFO] Guarda directamente en: assets\images\
echo.
set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\auto_descargas_v2.py"
) else (
	echo [ERROR] Python no encontrado
	pause
	goto :eof
)
pause
goto :eof

:process_now
cls
echo [INFO] Procesando fotos en Downloads (una sola vez)...
echo.
set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\auto_descargas_v2.py" --once
) else (
	echo [ERROR] Python no encontrado
	pause
	goto :eof
)
echo.
echo [OK] Finalizado
pause
goto :eof

:open_downloads
cls
echo [INFO] Abriendo carpeta de descargas...
start "" "%USERPROFILE%\Downloads"
timeout /t 2 /nobreak >nul
goto :eof
