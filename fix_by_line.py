#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reemplazo directo por número de línea"""

# Leer todas las líneas
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total de líneas: {len(lines)}')

# Líneas a modificar (índice 0-based, así que restamos 1)
lines_to_fix = {
    1873: ('L'Huillier<', 'L'Huillier Troncoso<'),  # línea 1874
    2154: ('"Gastón L'Huillier"', '"Gastón L'Huillier Troncoso"'),  # línea 2155
    2165: ('Gastón L'Huillier,', 'Gastón L'Huillier Troncoso,'),  # línea 2166
    2166: ('"Gastón L'Huillier"', '"Gastón L'Huillier Troncoso"'),  # línea 2167
}

replaced_count = 0
for line_idx, (old_substr, new_substr) in lines_to_fix.items():
    if line_idx < len(lines):
        original = lines[line_idx]
        if old_substr in original:
            lines[line_idx] = original.replace(old_substr, new_substr)
            replaced_count += 1
            print(f'✓ Línea {line_idx+1} actualizada')
        else:
            print(f'✗ Línea {line_idx+1} no contiene el texto esperado')
            print(f'  Contenido: {original.strip()[:80]}...')

print(f'\nTotal de reemplazos: {replaced_count}/4')

if replaced_count > 0:
    # Escribir el archivo actualizado
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('\n✓ Archivo actualizado exitosamente!')
else:
    print('\n✗ No se realizaron cambios')
