#!/usr/bin/env python3
"""
Procesa fotos de LinkedIn: quita fondo (rembg), centra y mejora (ASCII)
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
try:
    from rembg import remove
    REMBG_OK = True
except Exception:
    REMBG_OK = False
import io
import re

CARPETA_ENTRADA = Path("assets/raw_linkedin_photos")
CARPETA_SALIDA = Path("assets/images")
TAM_LIENZO = 1000
BRILLO = 1.05
CONTRASTE = 1.10

def normalizar_nombre_archivo(nombre_original: str) -> str:
    nombre_sin_ext = Path(nombre_original).stem
    nombre = nombre_sin_ext.lower()
    nombre = (nombre
              .replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
              .replace('ä','a').replace('ë','e').replace('ï','i').replace('ö','o').replace('ü','u')
              .replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u'))
    nombre = re.sub(r'[\s\-]+','_', nombre)
    nombre = re.sub(r'[^a-z0-9_]', '', nombre)
    nombre = re.sub(r'_+','_', nombre).strip('_')
    return f"{nombre}.png"

def quitar_fondo(imagen_path: Path) -> Image.Image:
    if not REMBG_OK:
        raise Exception("rembg no disponible en este entorno")
    with open(imagen_path, 'rb') as f:
        datos = f.read()
    datos_sin = remove(datos)
    img = Image.open(io.BytesIO(datos_sin))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return img

def centrar_en_lienzo(imagen: Image.Image, tamaño: int) -> Image.Image:
    lienzo = Image.new('RGBA', (tamaño, tamaño), (255, 255, 255, 0))
    margen = 50
    disponible = tamaño - (margen * 2)
    imagen.thumbnail((disponible, disponible), Image.Resampling.LANCZOS)
    x = (tamaño - imagen.width) // 2
    y = (tamaño - imagen.height) // 2
    lienzo.paste(imagen, (x, y), imagen)
    return lienzo

def mejorar_brillo_contraste(imagen: Image.Image, brillo: float, contraste: float) -> Image.Image:
    imagen = ImageEnhance.Brightness(imagen).enhance(brillo)
    imagen = ImageEnhance.Contrast(imagen).enhance(contraste)
    return imagen

def encontrar_siguiente_backup(ruta: Path) -> Path:
    if not ruta.exists():
        return None
    base = ruta.stem
    ext = ruta.suffix
    n = 1
    while True:
        cand = ruta.parent / f"{base}_{n:02d}{ext}"
        if not cand.exists():
            return cand
        n += 1

def respaldar_archivo_existente(ruta: Path):
    if not ruta.exists():
        return None
    b = encontrar_siguiente_backup(ruta)
    ruta.rename(b)
    return b

def procesar_imagen(imagen_entrada: Path, imagen_salida: Path, tamaño: int, brillo: float, contraste: float) -> bool:
    try:
        print("  Quitando fondo...", end=" ")
        imagen = quitar_fondo(imagen_entrada)
        print("OK", end=" ")
        print("Centrando...", end=" ")
        imagen = centrar_en_lienzo(imagen, tamaño)
        print("OK", end=" ")
        print("Mejorando...", end=" ")
        imagen = mejorar_brillo_contraste(imagen, brillo, contraste)
        print("OK", end=" ")
        print("Guardando...", end=" ")
        backup = respaldar_archivo_existente(imagen_salida)
        if backup:
            print(f"\n     Respaldado anterior: {backup.name}")
            print("  ", end="")
        imagen.save(imagen_salida, 'PNG', optimize=True)
        print("OK")
        return True
    except Exception as e:
        print(f"\n     Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("PROCESADOR DE FOTOS DE LINKEDIN - GL Strategic")
    print("="*70 + "\n")
    if not CARPETA_ENTRADA.exists():
        print(f"ERROR: No existe la carpeta de entrada: {CARPETA_ENTRADA}")
        print("\nCrea la carpeta manualmente:")
        print(f"   mkdir {CARPETA_ENTRADA}")
        print("\nDescarga las fotos y guardalas ahi.\n")
        sys.exit(1)
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    extensiones = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    imagenes = [f for f in CARPETA_ENTRADA.iterdir() if f.is_file() and f.suffix.lower() in extensiones]
    if not imagenes:
        print(f"No se encontraron imagenes en: {CARPETA_ENTRADA}\n")
        sys.exit(0)
    print(f"Procesando {len(imagenes)} imagen(es) de {CARPETA_ENTRADA}...\n")
    exitosas = 0
    fallidas = 0
    for idx, imagen_entrada in enumerate(imagenes, 1):
        nombre_original = imagen_entrada.name
        nombre_normalizado = normalizar_nombre_archivo(nombre_original)
        imagen_salida = CARPETA_SALIDA / nombre_normalizado
        print(f"[{idx}/{len(imagenes)}] {nombre_original}")
        print(f"       -> {nombre_normalizado}")
        print("       ", end="")
        if procesar_imagen(imagen_entrada, imagen_salida, TAM_LIENZO, BRILLO, CONTRASTE):
            exitosas += 1
        else:
            fallidas += 1
        print()
    print("\n" + "="*70)
    print("RESUMEN DEL PROCESAMIENTO")
    print("="*70)
    print(f"Exitosas: {exitosas}")
    print(f"Fallidas: {fallidas}")
    print(f"Total: {len(imagenes)}")
    print(f"\nSalida: {CARPETA_SALIDA.absolute()}\n")
    if exitosas == len(imagenes):
        print("Todas las imagenes se procesaron correctamente!\n")
    elif fallidas > 0:
        print(f"{fallidas} imagen(es) tuvieron errores. Revisa arriba.\n")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
