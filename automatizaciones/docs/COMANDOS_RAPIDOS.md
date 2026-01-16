# COMANDOS RAPIDOS - Procesamiento de Fotos LinkedIn (ASCII)

## Flujo Completo

```powershell
mkdir assets\raw_linkedin_photos
```

Descarga fotos manualmente en `assets\raw_linkedin_photos` con nombres "Nombre Apellido.png".

Crear venv (opcional):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Pillow --quiet
```

Ejecutar:

```powershell
python automatizaciones\process_linkedin_photos.py
```

## Estructura final

```
GL-Web-Master/
├── automatizaciones/
│   ├── process_linkedin_photos.py
│   └── docs/
│       └── COMANDOS_RAPIDOS.md
├── assets/
│   ├── raw_linkedin_photos/
│   └── images/
```

## Problemas comunes

- "python not found" -> Instala Python con "Add to PATH".
- "No module rembg" -> Instala rembg en entorno compatible (Python 3.10-3.13).
- "ExecutionPolicy" -> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.
