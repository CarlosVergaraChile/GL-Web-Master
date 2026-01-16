#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Monitor de Descargas - Descarga fotos de LinkedIn → assets/images
Solo actualiza si la foto ha cambiado (comparación hash)
Guarda directamente como PNG optimizado (1000x1000, brillo +5%, contraste +10%)
"""

import os
import sys
import shutil
import time
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageEnhance

# ==================== CONFIG ====================
DESCARGAS = Path.home() / "Downloads"
PROJECT_ROOT = Path("c:/Proyectos/GL-Web-Master").resolve()
OUTPUT = PROJECT_ROOT / "assets" / "images"
HASH_FILE = PROJECT_ROOT / "automatizaciones" / ".photo_hashes.json"

# Detectar modo
MODE_ONCE = "--once" in sys.argv

# Crear carpetas
OUTPUT.mkdir(parents=True, exist_ok=True)

print(f"[MONITOR] Monitoreando: {DESCARGAS}")
print(f"[OUTPUT] Guardará en: {OUTPUT}")
print("[INFO] Descarga fotos de LinkedIn, se procesarán automáticamente")
print("[INFO] Solo actualiza si la foto es diferente")
if not MODE_ONCE:
    print("[PARAR] Presiona Ctrl+C para detener")
print()

# ==================== HELPER ====================
def load_hashes():
    """Carga hashes de fotos anteriores"""
    if HASH_FILE.exists():
        try:
            return json.loads(HASH_FILE.read_text(encoding='utf-8'))
        except:
            return {}
    return {}

def save_hashes(hashes):
    """Guarda hashes de fotos"""
    HASH_FILE.write_text(json.dumps(hashes, ensure_ascii=False, indent=2), encoding='utf-8')

def get_file_hash(filepath):
    """Calcula hash SHA256 de un archivo"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def process_photo(input_path, output_path):
    """
    Procesa foto: redimensiona 1000x1000, mejora brillo/contraste, guarda PNG
    Retorna True si éxito
    """
    try:
        # Abrir imagen
        img = Image.open(input_path)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar a 1000x1000 (LANCZOS)
        img = img.resize((1000, 1000), Image.Resampling.LANCZOS)
        
        # Mejorar brillo y contraste
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.10)
        
        # Guardar como PNG
        img.save(output_path, 'PNG', quality=95)
        return True
        
    except Exception as e:
        print(f"[ERROR] No se pudo procesar {input_path.name}: {e}")
        return False

# ==================== MAIN ====================
hashes = load_hashes()
archivos_vistos = set()

while True:
    try:
        for archivo in DESCARGAS.glob("*.png"):
            if archivo.name not in archivos_vistos:
                archivos_vistos.add(archivo.name)
                print(f"\n[DETECTADO] {archivo.name}")
                
                # Calcular hash del archivo descargado
                archivo_hash = get_file_hash(archivo)
                
                # Determinar nombre de salida (limpio)
                nombre_limpio = archivo.stem.lower().replace(" ", "_").replace(".", "_") + ".png"
                salida = OUTPUT / nombre_limpio
                
                # Verificar si el archivo ya existe con el mismo hash
                if nombre_limpio in hashes and hashes[nombre_limpio] == archivo_hash:
                    print(f"[SKIP] {nombre_limpio} (ya actualizado, sin cambios)")
                    continue
                
                # Procesar foto
                print(f"[PROCESANDO] Redimensionando, mejorando, guardando...")
                if process_photo(archivo, salida):
                    # Guardar nuevo hash
                    hashes[nombre_limpio] = archivo_hash
                    save_hashes(hashes)
                    print(f"[OK] Guardado en: {salida}")
                else:
                    print(f"[ERROR] No se pudo procesar {archivo.name}")
        
        # Si modo --once, salir después de una iteración
        if MODE_ONCE:
            break
        
        time.sleep(2)  # Revisar cada 2 segundos
        
    except KeyboardInterrupt:
        print("\n[INFO] Monitor detenido")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)
