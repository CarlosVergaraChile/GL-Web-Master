#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sincronizador de Fotos de LinkedIn → assets/images
Solo actualiza fotos que han cambiado (comparación hash)
Guarda directamente como PNG optimizado
"""

import os
import sys
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageEnhance
import requests

# ==================== CONFIG ====================
ROOT = Path(__file__).parent.parent
ASSETS_IMAGES = ROOT / "assets" / "images"
HASH_FILE = ROOT / "automatizaciones" / ".photo_hashes.json"

# Crear carpetas
ASSETS_IMAGES.mkdir(parents=True, exist_ok=True)

# URLs de perfiles de LinkedIn (HARDCODEADOS)
TEAM_PROFILES = {
    "gaston_lhuillier_troncoso": "https://www.linkedin.com/in/gaston-l-huillier-troncoso-55a24128/",
    "claudio_maggi": "https://www.linkedin.com/in/claudiomaggi/",
    "guillermo_munoz": "https://www.linkedin.com/in/guillermomunoz/",
    "rafael_sotil": "https://www.linkedin.com/in/rafaelsotil/",
    "edith_wilson": "https://www.linkedin.com/in/edith-wilson-porter-a0109215/",
    "carlos_vergara": "https://www.linkedin.com/in/carlosvergarachile/",
    "pablo_canobra": "https://www.linkedin.com/in/pablocanobra/",
    "jose_inostroza": "https://www.linkedin.com/in/jose-inostroza-avaria/",
    "javier_delamaza": "https://www.linkedin.com/in/javier-e-d%C3%ADaz-calder%C3%B3n-08abb222/",
    "jaime_soto": "https://www.linkedin.com/in/jaime-soto-zura-0a060220b/",
    "juan_bacovich": "https://www.linkedin.com/in/juan-carlos-bacovich/",
    "julio_munoz": "https://www.linkedin.com/in/juliomunozdiaz/",
    "jenny_sauterel": "https://www.linkedin.com/in/jenny-sauterel-2041a42a/",
    "alejandro_rodo": "https://www.linkedin.com/in/alejandro-rodo-leon-79279b72/",
    "gilberto_cespedes": "https://www.linkedin.com/in/gilberto-cespedes-43b2b799/",
    "elena_pailamilla": "https://www.linkedin.com/in/elena-pailamilla-sandoval-10523010a/",
    "juan_samaniego": "https://www.linkedin.com/in/juan-ramon-samaniego-sangroniz-82b315a3/",
    "maurice_filippi": "https://www.linkedin.com/in/maurice-filippi-rademacher-ba4380101/",
    "mario_boada": "https://www.linkedin.com/in/marioboada/",
    "jose_martinez": "https://www.linkedin.com/in/jose-ignacio-martinez-acevedo-41683845/",
    "claus_van": "https://www.linkedin.com/in/clausvandermolen/",
    "paula_jadue": "https://www.linkedin.com/in/paula-jadue-abuyeres/",
}

# ==================== HELPER ====================
def log(msg, status="INFO"):
    """Print con timestamp"""
    print(f"[{status}] {msg}", flush=True)

def load_hashes():
    """Carga hash anterior de fotos"""
    if HASH_FILE.exists():
        try:
            return json.loads(HASH_FILE.read_text())
        except:
            return {}
    return {}

def save_hashes(hashes):
    """Guarda hash de fotos"""
    HASH_FILE.write_text(json.dumps(hashes, indent=2))

def get_file_hash(data):
    """Calcula hash de datos binarios"""
    return hashlib.sha256(data).hexdigest()

def download_photo(url, person_name):
    """Descarga foto desde LinkedIn"""
    try:
        # Limpiar URL
        url_clean = url.split("?")[0] if "?" in url else url
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        log(f"Descargando {person_name}...", "INFO")
        resp = requests.get(url_clean, headers=headers, timeout=10)
        resp.raise_for_status()
        
        return resp.content
        
    except Exception as e:
        log(f"Error descargando {person_name}: {e}", "ERROR")
        return None

def process_photo(image_data, person_name):
    """
    Procesa foto: redimensiona, mejora, guarda como PNG
    Retorna: (PNG bytes, hash)
    """
    try:
        # Abrir imagen
        img = Image.open(__import__('io').BytesIO(image_data))
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            # Crear fondo blanco
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
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
        
        # Guardar a PNG
        import io
        png_buffer = io.BytesIO()
        img.save(png_buffer, 'PNG', quality=95)
        png_data = png_buffer.getvalue()
        
        # Calcular hash
        photo_hash = get_file_hash(png_data)
        
        log(f"Procesado: {person_name} (1000x1000, PNG)", "OK")
        return png_data, photo_hash
        
    except Exception as e:
        log(f"Error procesando {person_name}: {e}", "ERROR")
        return None, None

def main():
    """Main flow"""
    log("=" * 60, "INFO")
    log("SINCRONIZADOR DE FOTOS LINKEDIN → assets/images", "INFO")
    log("=" * 60, "INFO")
    
    old_hashes = load_hashes()
    new_hashes = {}
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for person_name, profile_url in TEAM_PROFILES.items():
        log(f"\n→ {person_name}", "INFO")
        
        try:
            # Extraer URL de foto (aproximado - LinkedIn puede variar)
            # Para producción, usar Selenium o LinkedIn API
            # Por ahora, intentamos con método fallback
            
            # Este es un método simplificado - en producción necesitarías
            # Selenium o LinkedIn API para obtener la foto real
            
            log(f"  ⚠️ Requiere Selenium para extraer foto de {profile_url}", "WARN")
            log(f"  Saltando (se puede hacer manual o con Selenium)", "SKIP")
            skipped_count += 1
            
        except Exception as e:
            log(f"Error en {person_name}: {e}", "ERROR")
            error_count += 1
    
    log("\n" + "=" * 60, "INFO")
    log(f"RESUMEN:", "INFO")
    log(f"  Actualizadas: {updated_count}", "INFO")
    log(f"  Saltadas: {skipped_count}", "INFO")
    log(f"  Errores: {error_count}", "INFO")
    log(f"  Guardar en: {ASSETS_IMAGES}", "INFO")
    log("=" * 60, "INFO")
    
    # Guardar nuevos hashes
    save_hashes(new_hashes)

if __name__ == "__main__":
    main()
