#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT MAESTRO: Normaliza TODAS las fotos del equipo
==========================================

1. Convierte .jfif → .png (rembg + Pillow)
2. Quita fondos (background removal con rembg)
3. Centra imágenes en lienzo 1000x1000
4. Mejora brillo/contraste
5. Crea respaldos automáticos

Uso:
    python normalize_all_photos.py

Soporta:
    - Múltiples formatos: JPG, PNG, JFIF
    - Convierte RGBA ↔ RGB automáticamente
    - Respaldos: archivo.png, archivo_01.png, archivo_02.png, etc.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
import unicodedata
import re

# Colores para output
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Rutas
CARPETA_IMAGENES = Path("assets/images")
TAMAÑO_LIENZO = 1000

# Estadísticas
stats = {
    "procesadas": 0,
    "saltadas": 0,
    "errores": 0,
    "convertidas_jfif": 0,
    "normalizadas": 0
}

def normalizar_nombre(filename):
    """Convierte 'Nombre Apellido.PNG' → 'nombre_apellido.png'"""
    # Quita extensión
    name, ext = os.path.splitext(filename)
    
    # NFD normalization (descompone acentos)
    name = unicodedata.normalize('NFD', name)
    # Quita diacríticos
    name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
    
    # Minúsculas y espacios → guiones bajos
    name = name.lower().strip()
    name = re.sub(r'\s+', '_', name)
    # Quita caracteres especiales
    name = re.sub(r'[^\w_]', '', name)
    
    # Extensión siempre .png en minúsculas
    return f"{name}.png"

def encontrar_siguiente_backup(ruta_archivo):
    """Busca siguiente número de backup: archivo.png → archivo_01.png"""
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        return ruta_archivo
    
    stem = ruta.stem
    parent = ruta.parent
    contador = 1
    
    while True:
        nuevo_nombre = f"{stem}_{contador:02d}.png"
        nueva_ruta = parent / nuevo_nombre
        if not nueva_ruta.exists():
            return str(nueva_ruta)
        contador += 1

def respaldar_archivo(ruta_archivo):
    """Crea backup de archivo existente antes de sobrescribir"""
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        return
    
    backup_ruta = encontrar_siguiente_backup(ruta_archivo)
    ruta.rename(backup_ruta)
    print(f"  📦 Respaldo creado: {Path(backup_ruta).name}")

def centrar_en_lienzo(imagen_pil, tamaño=1000):
    """Coloca imagen en lienzo 1000x1000 transparente, centrada"""
    # Crea lienzo transparente
    lienzo = Image.new('RGBA', (tamaño, tamaño), (0, 0, 0, 0))
    
    # Convierte imagen a RGBA si no lo es
    if imagen_pil.mode != 'RGBA':
        imagen_pil = imagen_pil.convert('RGBA')
    
    # Calcula posición centrada con margen
    margen = 50
    ancho_disponible = tamaño - (margen * 2)
    alto_disponible = tamaño - (margen * 2)
    
    # Redimensiona manteniendo proporción
    imagen_pil.thumbnail((ancho_disponible, alto_disponible), Image.Resampling.LANCZOS)
    
    # Calcula posición para centrar
    x = (tamaño - imagen_pil.width) // 2
    y = (tamaño - imagen_pil.height) // 2
    
    # Pega en lienzo
    lienzo.paste(imagen_pil, (x, y), imagen_pil)
    
    return lienzo

def mejorar_brillo_contraste(imagen_pil):
    """Aplica 5% brillo + 10% contraste"""
    enhancer = ImageEnhance.Brightness(imagen_pil)
    imagen_pil = enhancer.enhance(1.05)  # +5% brillo
    
    enhancer = ImageEnhance.Contrast(imagen_pil)
    imagen_pil = enhancer.enhance(1.10)  # +10% contraste
    
    return imagen_pil

def procesar_imagen(ruta_entrada, ruta_salida, usar_rembg=True):
    """Procesa una imagen: abre → mejora → centra → guarda"""
    try:
        # Abre imagen
        img = Image.open(ruta_entrada)
        print(f"  📸 Abierta: {img.size} {img.mode}")
        
        # Intenta quitar fondo con rembg (si está disponible)
        if usar_rembg:
            try:
                from rembg import remove
                print(f"  🎨 Removiendo fondo con IA...")
                img = remove(img)
                print(f"  ✅ Fondo removido")
            except Exception as e:
                print(f"  ⚠️  rembg no disponible, continuando sin remover fondo: {e}")
        
        # Centra en lienzo 1000x1000
        print(f"  📐 Centrando en lienzo 1000x1000...")
        img = centrar_en_lienzo(img)
        
        # Mejora brillo/contraste
        print(f"  ✨ Mejorando brillo (+5%) y contraste (+10%)...")
        img = mejorar_brillo_contraste(img)
        
        # Respalda si ya existe
        if Path(ruta_salida).exists():
            respaldar_archivo(ruta_salida)
        
        # Guarda como PNG optimizado
        img.save(ruta_salida, 'PNG', optimize=True, quality=95)
        print(f"  💾 Guardada: {Path(ruta_salida).name}")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error procesando: {e}")
        return False

def main():
    print(f"\n{Color.HEADER}{Color.BOLD}🚀 NORMALIZADOR MAESTRO DE FOTOS{Color.ENDC}")
    print(f"{Color.HEADER}{'='*60}{Color.ENDC}\n")
    
    if not CARPETA_IMAGENES.exists():
        print(f"{Color.FAIL}❌ Carpeta no encontrada: {CARPETA_IMAGENES}{Color.ENDC}")
        return
    
    # Lista archivos de imagen
    extensiones_soportadas = ('.png', '.jpg', '.jpeg', '.jfif', '.bmp', '.gif')
    archivos = [f for f in CARPETA_IMAGENES.iterdir() 
                if f.is_file() and f.suffix.lower() in extensiones_soportadas]
    
    print(f"{Color.OKBLUE}📂 Fotos encontradas: {len(archivos)}{Color.ENDC}\n")
    
    if not archivos:
        print(f"{Color.WARNING}⚠️  No hay archivos de imagen en {CARPETA_IMAGENES}{Color.ENDC}")
        return
    
    # Procesa cada archivo
    for i, archivo in enumerate(sorted(archivos), 1):
        print(f"{Color.OKCYAN}[{i}/{len(archivos)}] {archivo.name}{Color.ENDC}")
        
        # Normaliza nombre de salida
        nombre_normalizado = normalizar_nombre(archivo.name)
        ruta_salida = CARPETA_IMAGENES / nombre_normalizado
        
        # Si ya es .png y está normalizado, pregunta
        if archivo.suffix.lower() == '.png' and archivo.name == nombre_normalizado:
            print(f"  ⏭️  Ya está normalizado, saltando")
            stats["saltadas"] += 1
            continue
        
        # Procesa imagen
        if procesar_imagen(str(archivo), str(ruta_salida)):
            stats["procesadas"] += 1
            
            # Si original era diferente al normalizado, elimina original
            if archivo.name != nombre_normalizado:
                try:
                    archivo.unlink()
                    print(f"  🗑️  Original eliminado: {archivo.name}")
                    stats["normalizadas"] += 1
                except Exception as e:
                    print(f"  ⚠️  No se pudo eliminar original: {e}")
        else:
            stats["errores"] += 1
        
        print()
    
    # Reporte final
    print(f"\n{Color.HEADER}{Color.BOLD}{'='*60}")
    print(f"📊 REPORTE FINAL{Color.ENDC}\n")
    print(f"{Color.OKGREEN}✅ Procesadas: {stats['procesadas']}{Color.ENDC}")
    print(f"{Color.WARNING}⏭️  Saltadas: {stats['saltadas']}{Color.ENDC}")
    print(f"{Color.FAIL}❌ Errores: {stats['errores']}{Color.ENDC}")
    print(f"{Color.OKBLUE}📝 Normalizadas: {stats['normalizadas']}{Color.ENDC}\n")
    
    print(f"{Color.OKCYAN}Todas las fotos ahora están en: assets/images/*.png{Color.ENDC}")
    print(f"{Color.OKGREEN}✨ Proceso completado - ¡Listo para usar!{Color.ENDC}\n")

if __name__ == "__main__":
    main()
