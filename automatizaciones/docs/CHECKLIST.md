# CHECKLIST RAPIDO - GL STRATEGIC FOTOS (ASCII)

## Estado Actual

- Todas las fotos normalizadas (83 total)
- 20/20 fotos de equipo presentes
- Nombres consistentes (minusculas, sin acentos)
- Tamaños 1000x1000
- HTML actualizado (.jfif -> .png)
- Dependencias instaladas (Pillow)
- Scripts listos
- Documentacion completa

## Como Ejecutar

Automático (recomendado):

```powershell
cmd /c AUTOMATOR.bat
```

Manual:

```powershell
python automatizaciones\normalize_all_photos.py
python automatizaciones\audit_fotos.py
python automatizaciones\watchdog_fotos.py
```

## Agregar Nuevas Fotos

1) Copia a `assets\images\` y luego normaliza
2) O usa `assets\raw_linkedin_photos\` con IA (rembg) y corre `automatizaciones\process_linkedin_photos.py`
3) O deja el watchdog corriendo y sube fotos

## Verificar Estado

```powershell
python automatizaciones\audit_fotos.py
Get-ChildItem assets\images -Filter "*.png" | Format-Table Name
```

## Especificaciones

- Canvas 1000x1000 RGBA
- Brillo +5%, Contraste +10%
- PNG optimize=True
- Margen 50px
- Nombres .png minusculas

## Resumen de Estado

- Todo OK, listo para produccion
