@echo off
chcp 65001 >nul
cls

:menu
echo.
echo ════════════════════════════════════════════════════════
echo   GL STRATEGIC - AUTOMATIZADOR LINKEDIN
echo ════════════════════════════════════════════════════════
echo.
echo [1] Descargar fotos del equipo desde LinkedIn
echo [2] Extraer noticias y redactarlas (AUTOMÁTICO)
echo [3] Redactar noticia manualmente (RECOMENDADO)
echo [4] Salir
echo.
set /p opcion="Selecciona opcion: "

if "%opcion%"=="1" goto fotos
if "%opcion%"=="2" goto noticias
if "%opcion%"=="3" goto manual
if "%opcion%"=="4" exit /b 0

goto menu

:fotos
echo.
echo [INICIANDO] Descarga de fotos...
echo.
.\.venv\Scripts\python.exe automatizaciones/sync_linkedin_photos_v2.py
echo.
pause
goto menu

:noticias
echo.
echo [INICIANDO] Extracción de noticias...
echo.
.\.venv\Scripts\python.exe automatizaciones/harvest_linkedin_posts.py
echo.
pause
goto menu

:manual
echo.
echo [INICIANDO] Redactor de noticias...
echo.
.\.venv\Scripts\python.exe automatizaciones/redactor_noticias_simple.py
echo.
pause
goto menu
	goto :eof
)

echo.
echo [OK] Finalizado
echo.
pause
goto :eof
