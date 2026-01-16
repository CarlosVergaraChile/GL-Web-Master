#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Backup del archivo original
if not os.path.exists('index.html.bak'):
    with open('index.html', 'r', encoding='utf-8') as f:
        content_backup = f.read()
    with open('index.html.bak', 'w', encoding='utf-8') as f:
        f.write(content_backup)
    print("✅ Backup creado: index.html.bak")

# Leer archivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Contador de reemplazos
original = "Gastón L'Huillier"
replacement = "Gastón L'Huillier Troncoso"

count = content.count(original)
print(f"📊 Encontradas {count} ocurrencias de '{original}'")

# Realizar reemplazo
content = content.replace(original, replacement)

# Guardar archivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Reemplazos completados: {count} instancias actualizadas")
print(f"✅ Nuevo nombre: {replacement}")
