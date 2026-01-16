#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Crear placeholders para las 3 personas faltantes
personas = [
    ("javier_delamaza.png", "Javier\nDelamaza", "#004E89"),
    ("julio_munoz.png", "Julio\nMuñoz", "#1B998B"),
    ("alejandro_rodo.png", "Alejandro\nRodó", "#FF6B35"),
]

os.makedirs("assets/images", exist_ok=True)

for filename, nombre, color in personas:
    filepath = f"assets/images/{filename}"
    
    # Crear imagen circular (avatar style)
    img = Image.new("RGB", (400, 400), color=color)
    draw = ImageDraw.Draw(img)
    
    # Dibujar nombre
    draw.text((200, 200), nombre, fill="white", anchor="mm")
    
    img.save(filepath, "PNG")
    print(f"✓ {filename}")

print("\n✅ Fotos de directores regionales creadas")
