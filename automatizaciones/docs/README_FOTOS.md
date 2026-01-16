# Sistema Automatico de Normalizacion de Fotos (ASCII)

Este sistema normaliza fotos del equipo GL Strategic:

- Convierte JPG/JPEG/JFIF a PNG optimizado
- Redimensiona a 1000x1000 en lienzo transparente
- Centra la imagen con margen
- Mejora brillo (+5%) y contraste (+10%)
- Normaliza nombres (minusculas, sin espacios, sin acentos)
- Crea respaldos automaticos (_01.png, _02.png)
- Valida que todas las fotos esperadas existan

## Uso rapido

Opcion automatica (recomendado):

```powershell
cd C:\Proyectos\GL-Web-Master
powershell -NoProfile -ExecutionPolicy Bypass -File .\post_process.ps1
```

Paso a paso:

```powershell
cd C:\Proyectos\GL-Web-Master
python automatizaciones\normalize_all_photos.py
python automatizaciones\audit_fotos.py
```

## Scripts

- automatizaciones\normalize_all_photos.py
- automatizaciones\audit_fotos.py
- post_process.ps1 (en raiz)
- automatizaciones\process_linkedin_photos.py (IA opcional)

## Carpetas

```
GL-Web-Master/
├── index.html
├── AUTOMATOR.bat
├── post_process.ps1
├── automatizaciones/
│   ├── normalize_all_photos.py
│   ├── audit_fotos.py
│   ├── watchdog_fotos.py
│   ├── convert_jfif_to_png.py
│   ├── process_linkedin_photos.py
│   └── docs/
│       └── README_FOTOS.md
├── assets/
│   ├── images/
│   ├── data/
│   └── videos/
└── .venv/
```

## Instalacion (Pillow)

```powershell
cd C:\Proyectos\GL-Web-Master
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Pillow --quiet
```

## Notas

- Para IA (rembg), se recomienda Python 3.12 y luego instalar `rembg`.
- Si el menu muestra caracteres raros, los scripts ya fueron convertidos a ASCII.
