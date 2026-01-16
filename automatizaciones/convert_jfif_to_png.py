#!/usr/bin/env python3
"""
Convierte .jfif a .png y estandariza nombres (ASCII)
"""

from pathlib import Path
from PIL import Image
import os

CARPETA = Path("assets/images")

print("\n" + "="*70)
print("NORMALIZADOR DE FOTOS EXISTENTES")
print("="*70 + "\n")

jfif_files = list(CARPETA.glob("*.jfif"))

if jfif_files:
    print(f"Encontrados {len(jfif_files)} archivo(s) .jfif\n")
    for jfif_file in jfif_files:
        nombre_base = jfif_file.stem.lower()
        png_file = CARPETA / f"{nombre_base}.png"
        if png_file.exists():
            print(f"  Ya existe {png_file.name}, saltando")
            continue
        try:
            img = Image.open(jfif_file)
            if img.mode in ('RGBA', 'LA', 'P'):
                fondo = Image.new('RGB', img.size, (255, 255, 255))
                fondo.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = fondo
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(png_file, 'PNG', optimize=True)
            print(f"  OK: {jfif_file.name} -> {png_file.name}")
        except Exception as e:
            print(f"  Error con {jfif_file.name}: {e}")

print("\n" + "="*70)
print("Normalizacion completada")
print("="*70 + "\n")

team_files = sorted([f for f in CARPETA.glob("*.png") if f.stem not in ['logo_gl_strategic_transparent', 'logo_gl_strategic']])
print(f"Fotos de equipo disponibles: {len(team_files)}\n")
for f in team_files[:20]:
    print(f"  * {f.name}")
if len(team_files) > 20:
    print(f"  ... y {len(team_files) - 20} mas")

print()
