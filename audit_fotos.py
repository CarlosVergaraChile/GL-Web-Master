#!/usr/bin/env python3
"""
Listar fotos de equipo faltantes vs esperadas en el HTML
"""

import re
from pathlib import Path

# Leer index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extraer todas las referencias a fotos de equipo
pattern = r'src=["\']assets/images/([^"\']+\.(?:png|jfif))'
referencias = set(re.findall(pattern, html))

# Archivos que existen
carpeta = Path('assets/images')
existentes = {f.name for f in carpeta.glob('*')}

# Fotos de equipo (excluir logos, diagramas, etc)
equipo_refs = {f for f in referencias if any(x in f.lower() for x in [
    'gaston', 'claudio', 'guillermo', 'rafael', 'edith', 'carlos', 'pablo', 
    'jose', 'javier', 'jaime', 'jenny', 'alejandro', 'juan', 'gilberto', 
    'elena', 'maurice', 'mario', 'claus', 'paula'
])}

equipo_existentes = {f for f in existentes if any(x in f.lower() for x in [
    'gaston', 'claudio', 'guillermo', 'rafael', 'edith', 'carlos', 'pablo', 
    'jose', 'javier', 'jaime', 'jenny', 'alejandro', 'juan', 'gilberto', 
    'elena', 'maurice', 'mario', 'claus', 'paula'
])}

# Encontrar faltantes
faltantes = equipo_refs - equipo_existentes

print("\n" + "="*70)
print("📊 ANÁLISIS DE FOTOS DE EQUIPO")
print("="*70 + "\n")

print(f"Fotos esperadas en HTML: {len(equipo_refs)}")
print(f"Fotos existentes: {len(equipo_existentes)}")
print(f"Fotos FALTANTES: {len(faltantes)}\n")

if faltantes:
    print("❌ FOTOS FALTANTES:")
    for foto in sorted(faltantes):
        print(f"  - {foto}")
    print()

print("✅ FOTOS DISPONIBLES:")
for foto in sorted(equipo_existentes):
    print(f"  ✓ {foto}")

print("\n" + "="*70 + "\n")
