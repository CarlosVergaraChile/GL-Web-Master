# ============================================
# SCRIPT DE POST-PROCESAMIENTO AUTOMATICO (ASCII)
# ============================================
# Normaliza fotos, verifica estado y limpia temporales

$Root = Split-Path -Parent $PSCommandPath
$AutoDir = Join-Path $Root "automatizaciones"
$pyVenv = Join-Path $Root ".venv\Scripts\python.exe"

function Run-PyScript {
	param([string]$scriptName)
	$scriptPath = Join-Path $AutoDir $scriptName
	if (Test-Path $pyVenv) {
		& $pyVenv $scriptPath
	} else {
		Write-Host "[WARN] No se encontro venv; usando 'python' del sistema" -ForegroundColor Yellow
		python $scriptPath
	}
}

Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "                POST-PROCESAMIENTO EN MARCHA" -ForegroundColor Cyan
Write-Host "-------------------------------------------------------------" -ForegroundColor Cyan

Write-Host "[1/3] Normalizando todas las fotos..." -ForegroundColor Yellow
Run-PyScript "normalize_all_photos.py"

Write-Host "[2/3] Verificando estado de fotos..." -ForegroundColor Yellow
Run-PyScript "audit_fotos.py"

Write-Host "[3/3] Limpiando archivos temporales..." -ForegroundColor Yellow
Get-ChildItem (Join-Path $Root "assets\images") -Filter "*_[0-9][0-9].png" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "[OK] Archivos temporales eliminados" -ForegroundColor Green

$summary = @"
=============================================================
				POST-PROCESAMIENTO COMPLETADO
-------------------------------------------------------------

- Fotos: PNG 1000x1000, centradas
- Nombres: minusculas, sin espacios, sin acentos
- Brillo/Contraste: +5% / +10%
- Respaldos: creados si hay duplicados

Ubicacion: assets\images\*.png
Listo para: index.html

Proximos pasos:
  1) Abrir index.html en navegador
  2) Agregar faltantes a assets\raw_linkedin_photos\
	3) IA background removal (opcional): python automatizaciones\process_linkedin_photos.py
"@
Write-Host $summary -ForegroundColor Green

Read-Host "Presiona ENTER para cerrar..."
