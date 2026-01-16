#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NORMALIZADOR DE FOTOS (ASCII)
==========================================

- Convierte JFIF/JPG/PNG a PNG estandar
- Centra en lienzo 1000x1000
- Ajusta brillo (+5%) y contraste (+10%)
- Crea respaldos si sobrescribe
- Nombres: minusculas, sin acentos, espacios a _

Uso:
    python automatizaciones/normalize_all_photos.py
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
import unicodedata
import re

CARPETA_IMAGENES = Path("assets/images")
TAM_LIENZO = 1000

stats = {"procesadas": 0, "saltadas": 0, "errores": 0, "normalizadas": 0}

def normalizar_nombre(filename: str) -> str:
    name, _ = os.path.splitext(filename)
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    name = name.lower().strip()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9_]', '', name)
    return f"{name}.png"

def siguiente_backup(ruta_archivo: str) -> str:
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        return ruta_archivo
    stem = ruta.stem
    parent = ruta.parent
    n = 1
    while True:
        cand = parent / f"{stem}_{n:02d}.png"
        if not cand.exists():
            return str(cand)
        n += 1

def respaldar(ruta_archivo: str) -> None:
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        return
    dest = siguiente_backup(ruta_archivo)
    ruta.rename(dest)
    print(f"  Backup creado: {Path(dest).name}")

def centrar_en_lienzo(img: Image.Image, tam: int = TAM_LIENZO) -> Image.Image:
    lienzo = Image.new('RGBA', (tam, tam), (0, 0, 0, 0))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    margen = 50
    disp = tam - (margen * 2)
    img.thumbnail((disp, disp), Image.Resampling.LANCZOS)
    x = (tam - img.width) // 2
    y = (tam - img.height) // 2
    lienzo.paste(img, (x, y), img)
    return lienzo

def mejorar_brillo_contraste(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    return img

def procesar(ruta_entrada: str, ruta_salida: str) -> bool:
    try:
        img = Image.open(ruta_entrada)
        print(f"  Abierta: {img.size} {img.mode}")
        img = centrar_en_lienzo(img)
        print("  Centrando en lienzo 1000x1000...")
        img = mejorar_brillo_contraste(img)
        print("  Ajustando brillo/contraste...")
        if Path(ruta_salida).exists():
            respaldar(ruta_salida)
        img.save(ruta_salida, 'PNG', optimize=True, quality=95)
        print(f"  Guardada: {Path(ruta_salida).name}")
        return True
    except Exception as e:
        print(f"  Error procesando: {e}")
        return False

def main():
    print("\nNORMALIZADOR MAESTRO DE FOTOS")
    print("="*47)

    if not CARPETA_IMAGENES.exists():
        print(f"ERROR: Carpeta no encontrada: {CARPETA_IMAGENES}")
        return

    extensiones = ('.png', '.jpg', '.jpeg', '.jfif', '.bmp', '.gif')
    archivos = [f for f in CARPETA_IMAGENES.iterdir() if f.is_file() and f.suffix.lower() in extensiones]

    print(f"Fotos encontradas: {len(archivos)}\n")
    if not archivos:
        print(f"No hay archivos de imagen en {CARPETA_IMAGENES}")
        return

    for i, archivo in enumerate(sorted(archivos), 1):
        print(f"[{i}/{len(archivos)}] {archivo.name}")
        nombre_norm = normalizar_nombre(archivo.name)
        destino = CARPETA_IMAGENES / nombre_norm
        if archivo.suffix.lower() == '.png' and archivo.name == nombre_norm:
            print("  Ya esta normalizado, saltando")
            stats["saltadas"] += 1
            continue
        if procesar(str(archivo), str(destino)):
            stats["procesadas"] += 1
            if archivo.name != nombre_norm:
                try:
                    archivo.unlink()
                    print(f"  Original eliminado: {archivo.name}")
                    stats["normalizadas"] += 1
                except Exception as e:
                    print(f"  No se pudo eliminar original: {e}")
        else:
            stats["errores"] += 1
        print()

    print("\n" + "="*60)
    print("REPORTE FINAL\n")
    print(f"Procesadas: {stats['procesadas']}")
    print(f"Saltadas: {stats['saltadas']}")
    print(f"Errores: {stats['errores']}")
    print(f"Normalizadas: {stats['normalizadas']}\n")
    print("Todas las fotos ahora estan en: assets/images/*.png")
    print("Proceso completado - Listo para usar!\n")

if __name__ == "__main__":
    main()
