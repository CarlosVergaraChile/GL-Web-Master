#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LinkedIn Automator - Full Automation with Anti-Bot Handling
Descarga fotos de perfil de LinkedIn, quita fondo, mejora, y las publica
"""

import os
import sys
import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# ==================== CONFIG ====================
ROOT = Path(__file__).parent.parent
DOWNLOADS_FOLDER = Path(os.path.expanduser("~")) / "Downloads"
RAW_PHOTOS_FOLDER = ROOT / "assets" / "raw_linkedin_photos"
VENV312_PYTHON = ROOT / ".venv312" / "Scripts" / "python.exe"

# Crear folders si no existen
RAW_PHOTOS_FOLDER.mkdir(parents=True, exist_ok=True)

# LinkedIn URLs (HARDCODED - conocidos)
TEAM_PROFILES = [
    "https://www.linkedin.com/in/gaston-l-huillier-troncoso-55a24128/",
    "https://www.linkedin.com/in/claudiomaggi/",
    "https://www.linkedin.com/in/guillermomunoz/",
    "https://www.linkedin.com/in/rafaelsotil/",
    "https://www.linkedin.com/in/edith-wilson-porter-a0109215/",
    "https://www.linkedin.com/in/carlosvergarachile/",
    "https://www.linkedin.com/in/pablocanobra/",
    "https://www.linkedin.com/in/jose-inostroza-avaria/",
]

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "user@example.com")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "password")

# ==================== HELPER ====================
def log(msg, status="INFO"):
    """Print con timestamp"""
    print(f"[{status}] {msg}", flush=True)

def get_chrome_driver():
    """Create Chrome driver with options"""
    options = Options()
    # NO headless para que veas si hay CAPTCHA
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    # Download automático a Downloads
    prefs = {
        "download.default_directory": str(DOWNLOADS_FOLDER),
        "profile.default_content_settings.popups": 0,
        "safebrowsing.enabled": False,
    }
    options.add_experimental_option("prefs", prefs)
    
    log("Iniciando Chrome...", "INFO")
    driver = webdriver.Chrome(
        service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def download_profile_photo(driver, profile_url, person_name):
    """Abre perfil, busca foto, descarga"""
    try:
        log(f"Abriendo perfil: {person_name}", "INFO")
        driver.get(profile_url)
        time.sleep(3)
        
        try:
            # Buscar foto de perfil
            profile_photo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[role='button']"))
            )
        except:
            log(f"Foto no encontrada (selector cambió) para {person_name}", "WARN")
            return False
        
        log(f"Foto encontrada para {person_name}", "OK")
        photo_src = profile_photo.get_attribute("src")
        
        if not photo_src or "http" not in photo_src:
            log(f"SRC inválido para {person_name}", "WARN")
            return False
        
        # Descargar vía requests
        try:
            import requests
            url_clean = photo_src.split("?")[0]
            headers = {"User-Agent": "Mozilla/5.0"}
            
            log(f"Descargando desde {url_clean[:50]}...", "INFO")
            resp = requests.get(url_clean, headers=headers, timeout=10)
            resp.raise_for_status()
            
            filename = RAW_PHOTOS_FOLDER / f"{person_name.replace(' ', '_').lower()}.png"
            filename.write_bytes(resp.content)
            log(f"Guardado: {filename.name}", "OK")
            return True
            
        except Exception as e:
            log(f"Error descargando: {e}", "ERROR")
            return False
            
    except Exception as e:
        log(f"Error en perfil {person_name}: {e}", "ERROR")
        return False

def main():
    """Main flow"""
    log("=" * 60, "INFO")
    log("LINKEDIN AUTOMATOR - FULL AUTO", "INFO")
    log("=" * 60, "INFO")
    log(f"Profiles a procesar: {len(TEAM_PROFILES)}", "INFO")
    log("", "INFO")
    
    driver = None
    processed_count = 0
    blocked_count = 0
    
    try:
        driver = get_chrome_driver()
        
        # Iterar perfiles
        for i, profile_url in enumerate(TEAM_PROFILES, 1):
            log(f"\n--- Perfil {i}/{len(TEAM_PROFILES)} ---", "INFO")
            person_name = profile_url.split("/in/")[1].rstrip("/").replace("-", " ").title()
            
            if download_profile_photo(driver, profile_url, person_name):
                processed_count += 1
                log(f"✓ {person_name} - DESCARGADO", "OK")
            else:
                blocked_count += 1
                log(f"✗ {person_name} - FALLÓ", "WARN")
                
                if blocked_count >= 3:
                    log("\n[AVISO] LinkedIn bloqueó después de 3 intentos", "WARN")
                    log("Las fotos descargadas se procesarán ahora...", "INFO")
                    break
            
            time.sleep(5)
        
    except KeyboardInterrupt:
        log("\nCancelado por usuario", "WARN")
    except Exception as e:
        log(f"Error: {e}", "ERROR")
    finally:
        if driver:
            driver.quit()
    
    log("\n" + "=" * 60, "INFO")
    log(f"RESUMEN: {processed_count} descargadas, {blocked_count} fallidas", "INFO")
    log(f"Las fotos están en: {RAW_PHOTOS_FOLDER}", "INFO")
    log("=" * 60, "INFO")

if __name__ == "__main__":
    main()
