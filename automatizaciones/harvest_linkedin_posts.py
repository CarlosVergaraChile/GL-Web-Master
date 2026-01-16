#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Harvester de LinkedIn - Extrae posts de equipo GL Strategic y redacta noticias
Lee credenciales desde .env (seguro, no commitea en Git)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / ".env")

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    print("[ERROR] Credenciales no encontradas en .env")
    sys.exit(1)

# ==================== TEAM PROFILES ====================
TEAM_PROFILES = {
    "Gastón L'Huillier": "https://www.linkedin.com/in/gaston-l-huillier-troncoso-55a24128/",
    "Guillermo Muñoz": "https://www.linkedin.com/in/guillermomunoz/",
    "Rafael Sotil": "https://www.linkedin.com/in/rafaelsotil/",
    "Edith Wilson": "https://www.linkedin.com/in/edith-wilson-porter-a0109215/",
    "Carlos Vergara": "https://www.linkedin.com/in/carlosvergarachile",
    "Pablo Canobra": "https://www.linkedin.com/in/pablocanobra",
    "Claudio Maggi": "https://www.linkedin.com/in/claudiomaggi",
    "Javier Delamaza": "https://www.linkedin.com/in/javier-e-d%C3%ADaz-calder%C3%B3n-08abb222/",
}

# ==================== TEMPLATES DE REDACCIÓN ====================
REDACCION_TEMPLATES = {
    "estrategia": "Análisis estratégico: {contenido}. Una perspectiva alineada con la metodología de anticipación de GL Strategic.",
    "transformacion": "Transformación digital: {contenido}. GL Strategic acompaña este tipo de cambios organizacionales.",
    "liderazgo": "Liderazgo y gestión: {contenido}. Prácticas clave en la construcción de equipos adaptativos.",
    "ecoparques": "Desarrollo territorial: {contenido}. Alineado con la visión de GL Strategic de ecoparques industriales sostenibles.",
    "general": "{contenido}"
}

def login_linkedin(driver):
    """Inicia sesión en LinkedIn"""
    print("[LINKEDIN] Abriendo LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(LINKEDIN_EMAIL)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        time.sleep(4)
        print("[OK] Sesión iniciada")
        return True
    except Exception as e:
        print(f"[ERROR] Fallo en login: {e}")
        return False

def extract_recent_post(driver, profile_name):
    """Extrae el post más reciente de un perfil"""
    try:
        # Buscar elemento de post principal
        post = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'comment')]"))
        )
        texto = post.text[:500]  # Primeros 500 caracteres
        
        return texto if texto else None
    except:
        return None

def redactar_noticia(profile_name, post_text, categoria="general"):
    """Redacta una noticia con template basado en contenido"""
    
    if not post_text:
        return None
    
    # Detectar categoría automáticamente si contiene palabras clave
    post_lower = post_text.lower()
    if any(word in post_lower for word in ["estrategia", "anticipación", "futuro"]):
        categoria = "estrategia"
    elif any(word in post_lower for word in ["transformación", "digital", "cambio"]):
        categoria = "transformacion"
    elif any(word in post_lower for word in ["liderazgo", "equipo", "cultura"]):
        categoria = "liderazgo"
    elif any(word in post_lower for word in ["ecoparque", "territorial", "sostenible"]):
        categoria = "ecoparques"
    
    # Aplicar template
    template = REDACCION_TEMPLATES.get(categoria, REDACCION_TEMPLATES["general"])
    extracto = template.format(contenido=post_text[:250])
    
    return {
        "titulo": f"{profile_name} - {datetime.now().strftime('%B %d, %Y')}",
        "extracto": extracto,
        "categoria": categoria
    }

def guardar_noticia_en_json(noticia_data, autor, rol, imagen, url):
    """Guarda noticia en noticias.json"""
    json_path = Path(__file__).parent.parent / "assets" / "data" / "noticias.json"
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"noticias": []}
    
    # Generar ID
    new_id = max([n.get("id", 0) for n in data.get("noticias", [])] or [0]) + 1
    
    noticia = {
        "id": new_id,
        "titulo": noticia_data["titulo"],
        "extracto": noticia_data["extracto"],
        "autor": autor,
        "rol": rol,
        "imagen_autor": imagen,
        "tipo": "linkedin",
        "url": url,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "categoria": noticia_data["categoria"]
    }
    
    data["noticias"].append(noticia)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Noticia #{new_id} agregada: {noticia_data['titulo'][:60]}")

def main():
    print("════════════════════════════════════════════════════════")
    print("  HARVESTER DE LINKEDIN - GL Strategic")
    print("════════════════════════════════════════════════════════\n")
    
    options = Options()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        if not login_linkedin(driver):
            return
        
        posts_found = 0
        
        for name, url in TEAM_PROFILES.items():
            print(f"\n[REVISANDO] {name}...")
            driver.get(url)
            time.sleep(3)
            
            # Extraer post
            post_text = extract_recent_post(driver, name)
            
            if post_text and ("GL Strategic" in post_text or "GL" in post_text):
                print(f"[POST ENCONTRADO] {name}")
                
                noticia = redactar_noticia(name, post_text)
                if noticia:
                    # Nota: Necesitarías extraer rol, imagen, etc. del perfil
                    # Por ahora usamos datos predefinidos
                    guardar_noticia_en_json(
                        noticia,
                        autor=name,
                        rol="Team Member",
                        imagen=f"{name.lower().replace(' ', '_')}.png",
                        url=url
                    )
                    posts_found += 1
            else:
                print(f"[SKIP] {name} - No posts relevantes")
        
        print(f"\n[RESUMEN] Se encontraron {posts_found} posts relacionados con GL Strategic")
        print("[OK] Noticias agregadas a noticias.json\n")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
