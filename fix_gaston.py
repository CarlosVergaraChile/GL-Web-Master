#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazo del apellido de Gastón
content = content.replace(
    "Gastón L'Huillier</h4>",
    "Gastón L'Huillier Troncoso</h4>"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Apellido actualizado: Gastón L'Huillier Troncoso")
