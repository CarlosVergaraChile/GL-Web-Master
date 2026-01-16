#!/usr/bin/env python3
"""
Script rápido para normalizar extensiones PNG/JFIF existentes
Convierte .jfif a .png y estandariza nombres en minúsculas
"""

from pathlib import Path
from PIL import Image
import os

CARPETA = Path("assets/images")

print("\n" + "="*70)
print("🔄 NORMALIZADOR DE FOTOS EXISTENTES")
print("="*70 + "\n")

# Buscar archivos .jfif y convertirlos a .png
jfif_files = list(CARPETA.glob("*.jfif"))

if jfif_files:
    print(f"Encontrados {len(jfif_files)} archivo(s) .jfif\n")
    
    for jfif_file in jfif_files:
        # Nombre base sin extensión
        nombre_base = jfif_file.stem.lower()
        png_file = CARPETA / f"{nombre_base}.png"
        
        # Si ya existe .png con ese nombre, no convertir
        if png_file.exists():
            print(f"⏭️  {jfif_file.name} → Ya existe {png_file.name}, saltando")
            continue
        
        try:
            # Abrir imagen
            img = Image.open(jfif_file)
            
            # Convertir a RGB si es necesario (JFIF no soporta transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco
                fondo = Image.new('RGB', img.size, (255, 255, 255))
                # Pegar imagen sobre fondo
                fondo.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = fondo
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Guardar como PNG
            img.save(png_file, 'PNG', optimize=True)
            
            print(f"✅ {jfif_file.name} → {png_file.name}")
            
            # Opcional: eliminar .jfif original
            # jfif_file.unlink()
            
        except Exception as e:
            print(f"❌ Error con {jfif_file.name}: {e}")

print("\n" + "="*70)
print("✨ Normalización completada")
print("="*70 + "\n")

# Mostrar todas las fotos de equipo disponibles
team_files = sorted([f for f in CARPETA.glob("*.png") if f.stem not in ['logo_gl_strategic_transparent', 'logo_gl_strategic']])
print(f"Fotos de equipo disponibles: {len(team_files)}\n")
for f in team_files[:20]:
    print(f"  ✓ {f.name}")
if len(team_files) > 20:
    print(f"  ... y {len(team_files) - 20} más")

print()
