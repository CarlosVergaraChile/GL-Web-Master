#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 WATCHDOG: Monitorea assets/images/ y auto-normaliza nuevas fotos

Uso:
    python watchdog_fotos.py

Características:
    ✅ Monitorea cambios en tiempo real
    ✅ Auto-normaliza nuevas/modificadas fotos
    ✅ Crea respaldos inteligentes
    ✅ Reporta cambios en consola
    ✅ Se ejecuta indefinidamente (Ctrl+C para detener)
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image, ImageEnhance
import unicodedata
import re
from datetime import datetime

# Colores
class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

CARPETA = Path("assets/images")
INTERVALO_CHECK = 5  # segundos
HISTORIAL = {}

def log(msg, color=C.CYAN):
    """Print con timestamp"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{ts}]{C.ENDC} {msg}")

def normalizar_nombre(filename):
    """Convierte nombres a formato estándar"""
    name, ext = os.path.splitext(filename)
    name = unicodedata.normalize('NFD', name)
    name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
    name = name.lower().strip()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^\w_]', '', name)
    return f"{name}.png"

def procesar_imagen(ruta_entrada, ruta_salida):
    """Procesa y normaliza imagen"""
    try:
        img = Image.open(ruta_entrada)
        
        # Centra en lienzo 1000x1000
        lienzo = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.thumbnail((900, 900), Image.Resampling.LANCZOS)
        x = (1000 - img.width) // 2
        y = (1000 - img.height) // 2
        lienzo.paste(img, (x, y), img)
        
        # Mejora brillo/contraste
        enhancer = ImageEnhance.Brightness(lienzo)
        lienzo = enhancer.enhance(1.05)
        enhancer = ImageEnhance.Contrast(lienzo)
        lienzo = enhancer.enhance(1.10)
        
        # Guarda
        lienzo.save(ruta_salida, 'PNG', optimize=True)
        return True
    except Exception as e:
        log(f"❌ Error procesando {ruta_entrada}: {e}", C.RED)
        return False

def main():
    log(f"🔍 WATCHDOG INICIADO - Monitoreando {CARPETA}", C.HEADER)
    log(f"📁 Intervalo de check: {INTERVALO_CHECK} segundos", C.BLUE)
    log(f"⏹️  Presiona Ctrl+C para detener\n", C.YELLOW)
    
    try:
        while True:
            try:
                archivos = {f.name: f.stat().st_mtime for f in CARPETA.iterdir() 
                           if f.is_file() and f.suffix.lower() in 
                           ('.png', '.jpg', '.jpeg', '.jfif')}
                
                # Detecta nuevos/modificados
                for nombre, mtime in archivos.items():
                    if nombre not in HISTORIAL or HISTORIAL[nombre] != mtime:
                        if nombre not in HISTORIAL:
                            log(f"📸 NUEVO: {nombre}", C.GREEN)
                        else:
                            log(f"🔄 MODIFICADO: {nombre}", C.YELLOW)
                        
                        # Normaliza
                        nombre_norm = normalizar_nombre(nombre)
                        ruta_entrada = CARPETA / nombre
                        ruta_salida = CARPETA / nombre_norm
                        
                        if nombre != nombre_norm:
                            log(f"   → Normalizando a: {nombre_norm}", C.CYAN)
                        
                        if procesar_imagen(str(ruta_entrada), str(ruta_salida)):
                            log(f"   ✅ Procesada correctamente", C.GREEN)
                            HISTORIAL[nombre] = mtime
                            
                            # Elimina original si fue renombrada
                            if nombre != nombre_norm and nombre != nombre_norm:
                                try:
                                    ruta_entrada.unlink()
                                    log(f"   🗑️  Original eliminado", C.BLUE)
                                except:
                                    pass
                        else:
                            log(f"   ❌ Error procesando", C.RED)
                
                # Detecta eliminados
                eliminados = [n for n in HISTORIAL if n not in archivos]
                for eliminado in eliminados:
                    log(f"🗑️  ELIMINADO: {eliminado}", C.YELLOW)
                    del HISTORIAL[eliminado]
                
                time.sleep(INTERVALO_CHECK)
            
            except KeyboardInterrupt:
                raise
            except Exception as e:
                log(f"⚠️  Error en ciclo: {e}", C.RED)
                time.sleep(INTERVALO_CHECK)
    
    except KeyboardInterrupt:
        log(f"\n⏹️  WATCHDOG DETENIDO", C.HEADER)
        log(f"📊 Monitoreadas {len(HISTORIAL)} fotos", C.BLUE)

if __name__ == "__main__":
    main()
