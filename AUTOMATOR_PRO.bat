@echo off
REM ============================================
REM AUTOMATOR PRO - AUTO DESCARGAS
REM ============================================
setlocal enabledelayedexpansion
set "ROOT=%~dp0"
cd /d "%ROOT%"

cls
echo.
echo =============================================================
echo               AUTOMATOR - AUTO DESCARGAS
echo =============================================================
echo.
echo SIMPLEMENTE:
echo 1. Presiona [1]
echo 2. Ve a LinkedIn
echo 3. Click derecho en foto - Guardar imagen como
echo 4. Se procesa AUTOMATICAMENTE
echo 5. Presiona Ctrl+C cuando termines
echo.
echo [1] INICIAR MONITOR
echo [2] SALIR
echo.

set /p option="Opcion: "

if "%option%"=="1" goto start_monitor
if "%option%"=="2" goto :eof

echo ERROR: Opcion invalida
timeout /t 1 /nobreak >nul
goto :eof

:start_monitor
cls
echo [INFO] Monitor iniciado
echo.
echo - Ve a LinkedIn
echo - Click derecho en foto - Guardar imagen como
echo - Se procesa AUTOMATICAMENTE
echo.
echo Para DETENER: Presiona Ctrl+C
echo.

set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\auto_descargas.py" "%ROOT%\assets\raw_linkedin_photos" "%ROOT%\assets\images"
) else (
	echo [ERROR] Python no encontrado
	pause
	goto :eof
)
pause
goto :eof

:linkedin_auto
cls
echo [INFO] Abriendo LinkedIn...
start https://www.linkedin.com
echo.
echo [TIMER] Esperando 15 minutos...
echo Mientras tanto:
echo - Descarga fotos de LinkedIn (click derecho > Guardar imagen como)
echo - Se guardan automaticamente en descargas (o donde quieras)
echo - El programa va a procesar despues
echo.
echo Puedes cerrar LinkedIn cuando termines, o dejar abierto.
echo El programa seguira contando...
echo.

REM 15 minutos = 900 segundos
timeout /t 900 /nobreak

cls
echo [INFO] Tiempo terminado. Procesando fotos con IA...
echo.
echo Despues de que termines:
echo 1. Busca las fotos que bajaste (Descargas)
echo 2. Cópialas a: C:\Proyectos\GL-Web-Master\assets\raw_linkedin_photos\
echo 3. Presiona ENTER para procesar con IA
echo.
pause

set "PY=%ROOT%\.venv312\Scripts\python.exe"
if exist "%PY%" (
	echo [PROCESANDO]...
	"%PY%" "%ROOT%\automatizaciones\process_linkedin_photos.py"
) else (
	echo [ERROR] Python 3.12 no encontrado
	pause
	goto :eof
)
echo.
echo [OK] Fotos procesadas y listas en: assets\images\
echo Website actualizado automaticamente
echo.
pause
goto :eof

:process_now
echo.
echo [INFO] Monitor iniciado... Presiona Ctrl+C para detener
echo.
:process_now
cls
echo [INFO] Procesando fotos con IA...
echo.
set "PY=%ROOT%\.venv312\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\process_linkedin_photos.py"
) else (
	echo [ERROR] Python 3.12 no encontrado
	pause
	goto :eof
)
echo.
echo [OK] Fotos procesadas en: assets\images\
echo.
pause
goto :eof

:quick_audit
cls
set "PY=%ROOT%\.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" "%ROOT%\automatizaciones\audit_fotos.py"
) else (
	python "%ROOT%\automatizaciones\audit_fotos.py"
)
echo.
pause
goto :eof
