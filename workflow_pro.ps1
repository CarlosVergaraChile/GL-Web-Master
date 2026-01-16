param(
    [switch]$LinkedIn = $false,
    [switch]$MonitorOnly = $false,
    [switch]$ProcessNow = $false
)

$ROOT = Split-Path -Parent $MyInvocation.MyCommandPath
$AutoDir = Join-Path $ROOT "automatizaciones"
$RawDir = Join-Path $ROOT "assets\raw_linkedin_photos"
$OutDir = Join-Path $ROOT "assets\images"

# Python 3.12 con rembg
$Py312 = Join-Path $ROOT ".venv312\Scripts\python.exe"
if (-not (Test-Path $Py312)) {
    Write-Host "[ERROR] Python 3.12 no encontrado" -ForegroundColor Red
    exit 1
}

# Abrir LinkedIn
if ($LinkedIn) {
    Write-Host "[INFO] Abriendo LinkedIn..." -ForegroundColor Cyan
    Start-Process "https://www.linkedin.com"
    Start-Sleep -Seconds 2
}

# Procesar ahora
if ($ProcessNow) {
    Write-Host "[INFO] Procesando fotos con IA..." -ForegroundColor Cyan
    & $Py312 (Join-Path $AutoDir "process_linkedin_photos.py")
    Write-Host "[OK] Fotos en: $OutDir" -ForegroundColor Green
    exit 0
}

# Monitor tiempo real
Write-Host "[INFO] Monitor iniciado (Ctrl+C para detener)" -ForegroundColor Cyan
Write-Host "[INFO] Descarga fotos a: $RawDir" -ForegroundColor Yellow
Write-Host "[INFO] Se procesaran AUTOMATICAMENTE" -ForegroundColor Yellow
Write-Host ""

& $Py312 (Join-Path $AutoDir "watchdog_fotos.py")
