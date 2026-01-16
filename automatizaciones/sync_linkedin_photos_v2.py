#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Descargador de Fotos LinkedIn - Extrae fotos de perfiles del equipo GL Strategic
Inicia sesión automáticamente y guarda en assets/images
"""

import os
import sys
import json
import hashlib
import time
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import requests

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / ".env")

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    print("[ERROR] Credenciales no encontradas en .env")
    sys.exit(1)

# ==================== RUTAS ====================
PROJECT_ROOT = Path("c:/Proyectos/GL-Web-Master").resolve()
OUTPUT = PROJECT_ROOT / "assets" / "images"
HASH_FILE = PROJECT_ROOT / "automatizaciones" / ".photo_hashes.json"

OUTPUT.mkdir(parents=True, exist_ok=True)

# ==================== TEAM PROFILES ====================
TEAM_PROFILES = {
    "gaston_lhuillier_troncoso": "https://www.linkedin.com/in/gaston-l-huillier-troncoso-55a24128/",
    "guillermo_munoz": "https://www.linkedin.com/in/guillermomunoz/",
    "rafael_sotil": "https://www.linkedin.com/in/rafaelsotil/",
    "edith_wilson": "https://www.linkedin.com/in/edith-wilson-porter-a0109215/",
    "carlos_vergara": "https://www.linkedin.com/in/carlosvergarachile",
    "pablo_canobra": "https://www.linkedin.com/in/pablocanobra",
    "claudio_maggi": "https://www.linkedin.com/in/claudiomaggi",
    "javier_delamaza": "https://www.linkedin.com/in/javier-e-d%C3%ADaz-calder%C3%B3n-08abb222/",
    "jenny_sauterel": "https://www.linkedin.com/in/jenny-sauterel-2041a42a/",
    "alejandro_rodo": "https://www.linkedin.com/in/alejandro-rodo-leon-79279b72/",
    "gilberto_cespedes": "https://www.linkedin.com/in/gilberto-cespedes-43b2b799/",
    "elena_pailamilla": "https://www.linkedin.com/in/elena-pailamilla-sandoval-10523010a/",
    "juan_samaniego": "https://www.linkedin.com/in/juan-ramon-samaniego-sangroniz-82b315a3/",
    "maurice_filippi": "https://www.linkedin.com/in/maurice-filippi-rademacher-ba4380101/",
    "mario_boada": "https://www.linkedin.com/in/marioboada/",
    "jose_martinez_esp": "https://www.linkedin.com/in/jose-ignacio-martinez-acevedo-41683845",
    "claus_van": "https://www.linkedin.com/in/clausvandermolen/",
    "paula_jadue": "https://www.linkedin.com/in/paula-jadue-abuyeres",
}

def load_hashes():
    """Carga hashes previos"""
    if HASH_FILE.exists():
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    """Guarda hashes"""
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)

def get_file_hash(filepath):
    """Calcula SHA256 de archivo"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def optimize_image(image_data, filename):
    """Redimensiona y mejora imagen"""
    try:
        img = Image.open(BytesIO(image_data))
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Redimensionar
        img = img.resize((1000, 1000), Image.Resampling.LANCZOS)
        
        # Mejorar
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.10)
        
        # Guardar
        output_path = OUTPUT / f"{filename}.png"
        img.save(output_path, "PNG", quality=95)
        
        return output_path
    except Exception as e:
        print(f"[ERROR] Fallo procesando imagen: {e}")
        return None

def download_photo(driver, filename, profile_url):
    """Descarga foto de perfil LinkedIn"""
    try:
        driver.get(profile_url)
        time.sleep(2)
        
        # Buscar foto de perfil
        photo_url = None
        try:
            # Intenta obtener la foto de perfil principal
            img_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'profile')]"))
            )
            photo_url = img_element.get_attribute("src")
        except:
            # Intenta con selectores alternativos
            try:
                img = driver.find_element(By.XPATH, "//img[@alt='profile photo']")
                photo_url = img.get_attribute("src")
            except:
                pass
        
        if not photo_url:
            print(f"[SKIP] {filename} - No foto encontrada")
            return None
        
        # Descargar foto
        print(f"[DESCARGANDO] {filename}...")
        response = requests.get(photo_url, timeout=10)
        
        if response.status_code == 200:
            # Optimizar
            output_path = optimize_image(response.content, filename)
            
            if output_path:
                file_hash = get_file_hash(output_path)
                return (output_path, file_hash)
        
        return None
        
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        return None

def main():
    print("════════════════════════════════════════════════════════")
    print("  DESCARGADOR DE FOTOS LINKEDIN - GL Strategic")
    print("════════════════════════════════════════════════════════\n")
    
    options = Options()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    hashes = load_hashes()
    updated_count = 0
    
    try:
        # Login
        print("[LINKEDIN] Iniciando sesión...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(LINKEDIN_EMAIL)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        time.sleep(4)
        print("[OK] Sesión iniciada\n")
        
        # Descargar fotos
        for filename, profile_url in TEAM_PROFILES.items():
            print(f"[PROCESANDO] {filename}...")
            
            result = download_photo(driver, filename, profile_url)
            
            if result:
                output_path, file_hash = result
                
                # Comparar hash
                old_hash = hashes.get(filename)
                if old_hash == file_hash:
                    print(f"[SKIP] {filename} - Sin cambios")
                else:
                    print(f"[OK] {filename} actualizada")
                    hashes[filename] = file_hash
                    updated_count += 1
            
            time.sleep(1)
        
        save_hashes(hashes)
        print(f"\n[RESUMEN] {updated_count} fotos actualizadas")
        print(f"[UBICACIÓN] {OUTPUT}\n")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
