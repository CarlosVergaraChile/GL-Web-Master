#!/usr/bin/env python3
from PIL import Image, ImageDraw
import os

logos = [
    ("logos_01.png", "RETAIL", "#FF6B35"),
    ("logos_02.png", "ESTADO", "#004E89"),
    ("logos_03.png", "EDUCACIÓN", "#1B998B"),
    ("logos_04.png", "FINANCIERO", "#F7DC6F"),
    ("logos_05.png", "UTILITIES", "#A569BD"),
]

os.makedirs("assets/images", exist_ok=True)

for filename, text, color in logos:
    filepath = f"assets/images/{filename}"
    img = Image.new("RGB", (1200, 400), color=color)
    draw = ImageDraw.Draw(img)
    draw.text((600, 200), text, fill="white", anchor="mm")
    img.save(filepath, "PNG")
    print(f"✓ {filename}")

print("\n✅ Todos los logos creados")
