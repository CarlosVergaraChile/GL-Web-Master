# Guia Completa: Procesamiento de Fotos de LinkedIn (ASCII)

## Contenido

1. Que hace este script
2. Requisitos
3. Instalacion
4. Descargar fotos
5. Ejecutar
6. Resultados
7. Solucionar problemas

## Que hace este script

`automatizaciones/process_linkedin_photos.py`:
- Quita fondo (rembg) [opcional segun entorno]
- Centra en lienzo 1000x1000
- Mejora brillo/contraste
- Convierte a PNG
- Renombra consistente
- Respalda versiones anteriores

Entrada: `assets/raw_linkedin_photos/`
Salida:  `assets/images/`

## Requisitos
- Windows 10+
- Python 3.10–3.13 recomendado para rembg (3.14 no soporta rembg actualmente)
- VS Code
- Internet

Verifica Python:
```powershell
python --version
```

## Instalacion

```powershell
cd C:\Proyectos\GL-Web-Master
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Pillow --quiet
```

Para rembg (cuando el entorno sea compatible):
```powershell
pip install rembg
```

## Descargar fotos

1. Crea carpeta: `assets\raw_linkedin_photos`
2. En LinkedIn: click derecho en foto -> Guardar imagen como...
3. Guarda como: `Nombre Apellido.png`

## Ejecutar

```powershell
python automatizaciones\process_linkedin_photos.py
```

Veras progreso y archivos en `assets\images\`.

## Resultados esperados
- PNG optimizados 1000x1000
- Transparencia si rembg disponible
- Nombres normalizados

## Solucionar problemas
- "No module Pillow": `pip install Pillow`
- "rembg no disponible": usa solo normalizacion (sin remover fondo) o instala rembg en entorno compatible
- "ExecutionPolicy": `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

