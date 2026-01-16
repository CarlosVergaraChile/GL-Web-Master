#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para actualizar el apellido de Gastón L'Huillier a Gastón L'Huillier Troncoso"""

import sys

try:
    # Leer el archivo
    print("Leyendo index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Contar ocurrencias antes
    buscar = "Gastón L'Huillier"
    reemplazar = "Gastón L'Huillier Troncoso"
    
    ocurrencias_antes = contenido.count(buscar)
    print(f"Encontradas {ocurrencias_antes} ocurrencias de '{buscar}'")
    
    if ocurrencias_antes == 0:
        print("No se encontraron ocurrencias. El texto ya podría estar actualizado.")
        # Verificar si ya está actualizado
        if reemplazar in contenido:
            print(f"✓ El texto '{reemplazar}' ya existe en el archivo.")
            sys.exit(0)
        else:
            print("✗ ERROR: No se encontró ni el texto original ni el actualizado.")
            sys.exit(1)
    
    # Hacer el reemplazo
    print(f"Reemplazando por '{reemplazar}'...")
    contenido_nuevo = contenido.replace(buscar, reemplazar)
    
    # Verificar cuántas se reemplazaron
    ocurrencias_despues = contenido_nuevo.count(buscar)
    reemplazadas = ocurrencias_antes - ocurrencias_despues
    
    print(f"Se reemplazaron {reemplazadas} ocurrencias")
    
    # Crear backup
    print("Creando backup...")
    with open('index.html.backup', 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    # Escribir el nuevo contenido
    print("Escribiendo archivo actualizado...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(contenido_nuevo)
    
    print("\n✓ ¡Actualización completada exitosamente!")
    print(f"  - Reemplazos realizados: {reemplazadas}")
    print(f"  - Backup guardado en: index.html.backup")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
