#!/usr/bin/env python3
"""
Analisis de fotos de equipo vs referencias en index.html (ASCII)
"""

import re
from pathlib import Path

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'src=["\']assets/images/([^"\']+\.(?:png|jfif))'
referencias = set(re.findall(pattern, html))

carpeta = Path('assets/images')
existentes = {f.name for f in carpeta.glob('*')}

nombres = [
    'gaston','claudio','guillermo','rafael','edith','carlos','pablo',
    'jose','javier','jaime','jenny','alejandro','juan','gilberto',
    'elena','maurice','mario','claus','paula'
]

equipo_refs = {f for f in referencias if any(x in f.lower() for x in nombres)}
equipo_existentes = {f for f in existentes if any(x in f.lower() for x in nombres)}

faltantes = equipo_refs - equipo_existentes

print("\n" + "="*70)
print("ANALISIS DE FOTOS DE EQUIPO")
print("="*70 + "\n")

print(f"Fotos esperadas en HTML: {len(equipo_refs)}")
print(f"Fotos existentes: {len(equipo_existentes)}")
print(f"Fotos FALTANTES: {len(faltantes)}\n")

if faltantes:
    print("FOTOS FALTANTES:")
    for foto in sorted(faltantes):
        print(f"  - {foto}")
    print()

print("FOTOS DISPONIBLES:")
for foto in sorted(equipo_existentes):
    print(f"  * {foto}")

print("\n" + "="*70 + "\n")
