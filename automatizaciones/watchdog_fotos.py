#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WATCHDOG: Monitorea assets/images y normaliza nuevas fotos (ASCII)
"""

import os
import time
from pathlib import Path
from PIL import Image, ImageEnhance
import unicodedata
import re
from datetime import datetime

CARPETA = Path("assets/images")
INTERVALO_CHECK = 5  # segundos
HISTORIAL = {}

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def normalizar_nombre(filename: str) -> str:
    name, _ = os.path.splitext(filename)
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    name = name.lower().strip()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9_]', '', name)
    return f"{name}.png"

def procesar_imagen(ruta_entrada: str, ruta_salida: str) -> bool:
    try:
        img = Image.open(ruta_entrada)
        lienzo = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.thumbnail((900, 900), Image.Resampling.LANCZOS)
        x = (1000 - img.width) // 2
        y = (1000 - img.height) // 2
        lienzo.paste(img, (x, y), img)
        lienzo = ImageEnhance.Brightness(lienzo).enhance(1.05)
        lienzo = ImageEnhance.Contrast(lienzo).enhance(1.10)
        lienzo.save(ruta_salida, 'PNG', optimize=True)
        return True
    except Exception as e:
        log(f"Error procesando {ruta_entrada}: {e}")
        return False

def main():
    log(f"WATCHDOG INICIADO - Monitoreando {CARPETA}")
    log(f"Intervalo de check: {INTERVALO_CHECK} segundos")
    log("Presiona Ctrl+C para detener\n")
    try:
        while True:
            try:
                archivos = {f.name: f.stat().st_mtime for f in CARPETA.iterdir() if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.jfif')}
                for nombre, mtime in archivos.items():
                    if nombre not in HISTORIAL or HISTORIAL[nombre] != mtime:
                        if nombre not in HISTORIAL:
                            log(f"NUEVO: {nombre}")
                        else:
                            log(f"MODIFICADO: {nombre}")
                        nombre_norm = normalizar_nombre(nombre)
                        ruta_entrada = CARPETA / nombre
                        ruta_salida = CARPETA / nombre_norm
                        if nombre != nombre_norm:
                            log(f"   -> Normalizando a: {nombre_norm}")
                        if procesar_imagen(str(ruta_entrada), str(ruta_salida)):
                            log("   OK: Procesada")
                            HISTORIAL[nombre] = mtime
                            if nombre != nombre_norm:
                                try:
                                    ruta_entrada.unlink()
                                    log("   Original eliminado")
                                except:
                                    pass
                        else:
                            log("   Error procesando")
                eliminados = [n for n in HISTORIAL if n not in archivos]
                for eliminado in eliminados:
                    log(f"ELIMINADO: {eliminado}")
                    del HISTORIAL[eliminado]
                time.sleep(INTERVALO_CHECK)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                log(f"Error en ciclo: {e}")
                time.sleep(INTERVALO_CHECK)
    except KeyboardInterrupt:
        log("\nWATCHDOG DETENIDO")
        log(f"Monitoreadas {len(HISTORIAL)} fotos")

if __name__ == "__main__":
    main()
