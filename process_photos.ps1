# Script PowerShell para procesar fotos de LinkedIn
# Uso: .\process_photos.ps1

$tempDir = "temp_photos"
$outputDir = "assets\images"

# Crear directorios si no existen
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
    Write-Host "✅ Creado directorio: $tempDir" -ForegroundColor Green
    Write-Host "   Descarga manualmente las fotos de LinkedIn y guárdalas ahí" -ForegroundColor Yellow
}

# Mapeo de archivos
$photoMapping = @{
    "guillermo.jpg" = "guillermo_munoz.png"
    "claus.jpg" = "claus_van.png"
    "claudio_maggi.jpg" = "claudio_maggi.png"
    "pablo_canobra.jpg" = "pablo_canobra.png"
    "javier.jpg" = "javier_delamaza.png"
    "jose_martinez.jpg" = "jose_martinez_esp.png"
    "paula_jadue.jpg" = "paula_jadue.png"
    "jaime_soto.jpg" = "jaime_soto.png"
}

Write-Host "`n🚀 Procesando fotos...`n" -ForegroundColor Cyan

$processed = 0
foreach ($temp in $photoMapping.Keys) {
    $inputPath = Join-Path $tempDir $temp
    $outputName = $photoMapping[$temp]
    $outputPath = Join-Path $outputDir $outputName
    
    if (Test-Path $inputPath) {
        # Respaldar si existe
        if (Test-Path $outputPath) {
            $backupPath = $outputPath -replace '\.png$', '_01.png'
            Copy-Item $outputPath $backupPath -Force
            Write-Host "  ⚠️  Respaldado: $outputName → $($backupPath | Split-Path -Leaf)" -ForegroundColor Yellow
        }
        
        # Copiar y convertir a PNG usando .NET
        $img = [System.Drawing.Image]::FromFile((Resolve-Path $inputPath))
        $img.Save((Resolve-Path $outputDir).Path + "\$outputName", [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()
        
        Write-Host "  ✅ Procesado: $temp → $outputName" -ForegroundColor Green
        $processed++
    }
    else {
        Write-Host "  ⚠️  No encontrado: $temp" -ForegroundColor Yellow
    }
}

Write-Host "`n✨ Completado: $processed/$($photoMapping.Count) fotos procesadas" -ForegroundColor Cyan
Write-Host "📁 Fotos en: $outputDir`n" -ForegroundColor Gray

# Instrucciones para quitar fondo
Write-Host "📌 Para quitar el fondo de las fotos:" -ForegroundColor Magenta
Write-Host "   1. Ve a https://remove.bg" -ForegroundColor White
Write-Host "   2. Sube cada foto desde $outputDir" -ForegroundColor White
Write-Host "   3. Descarga el resultado y reemplaza el archivo" -ForegroundColor White
