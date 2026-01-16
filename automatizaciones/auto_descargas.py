import os
import sys
import shutil
import time
from pathlib import Path
from PIL import Image

# Directorios
DESCARGAS = Path.home() / "Downloads"
RAW_FOTOS = Path.home().parent / "Proyectos" / "GL-Web-Master" / "assets" / "raw_linkedin_photos"
OUTPUT = Path.home().parent / "Proyectos" / "GL-Web-Master" / "assets" / "images"

# Detectar modo
MODE_ONCE = "--once" in sys.argv

# Crear carpetas si no existen
RAW_FOTOS.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

print(f"[MONITOR] Monitoreando: {DESCARGAS}")
print(f"[OUTPUT] Procesara a: {OUTPUT}")
print("[INFO] Descarga fotos de LinkedIn, se procesaran automaticamente")
if not MODE_ONCE:
    print("[PARAR] Presiona Ctrl+C para detener")
print()

archivos_vistos = set()

while True:
    try:
        for archivo in DESCARGAS.glob("*.png"):
            if archivo.name not in archivos_vistos:
                archivos_vistos.add(archivo.name)
                print(f"[DETECTADO] {archivo.name}")
                
                # Copiar a raw
                destino_raw = RAW_FOTOS / archivo.name
                shutil.copy2(archivo, destino_raw)
                print(f"[OK] Copiado a: {RAW_FOTOS}")
                
                # Procesar con PIL
                try:
                    img = Image.open(destino_raw)
                    
                    # Redimensionar a 1000x1000
                    img = img.resize((1000, 1000), Image.Resampling.LANCZOS)
                    
                    # Mejorar brillo/contraste
                    from PIL import ImageEnhance
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.05)
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.10)
                    
                    # Guardar como PNG
                    nombre_limpio = archivo.stem.lower().replace(" ", "_").replace(".", "_") + ".png"
                    salida = OUTPUT / nombre_limpio
                    img.save(salida, "PNG")
                    
                    print(f"[OK] Procesado y guardado: {salida}")
                except Exception as e:
                    print(f"[ERROR] No se pudo procesar: {e}")
        
        # Si modo --once, salir despues de una iteracion
        if MODE_ONCE:
            break
        
        time.sleep(2)  # Revisar cada 2 segundos
        
    except KeyboardInterrupt:
        print("\n[INFO] Monitor detenido")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)
