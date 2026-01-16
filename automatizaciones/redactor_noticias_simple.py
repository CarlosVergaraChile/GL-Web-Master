#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Harvester Simplificado - Crea noticias redactadas
Sin dependencias de Selenium, basado en URL de LinkedIn
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / ".env")

# ==================== TEAM PROFILES ====================
TEAM_PROFILES = {
    "Gastón L'Huillier": ("Socio Principal", "gaston_lhuillier_troncoso.png", "https://www.linkedin.com/in/gaston-l-huillier-troncoso-55a24128/"),
    "Guillermo Muñoz": ("Socio - Estrategia Digital", "guillermo_munoz.png", "https://www.linkedin.com/in/guillermomunoz/"),
    "Rafael Sotil": ("Socio - Liderazgo y Cultura", "rafael_sotil.png", "https://www.linkedin.com/in/rafaelsotil/"),
    "Edith Wilson": ("Socio - Derecho Corporativo", "edith_wilson.png", "https://www.linkedin.com/in/edith-wilson-porter-a0109215/"),
    "Carlos Vergara": ("Socio - Procesos y Calidad", "carlos_vergara.PNG", "https://www.linkedin.com/in/carlosvergarachile"),
    "Pablo Canobra": ("Socio - Gerencia de Proyectos", "pablo_canobra.png", "https://www.linkedin.com/in/pablocanobra"),
}

# Templates de noticias por tema
PLANTILLAS = {
    "estrategia": {
        "titulo_template": "{autor} comparte perspectiva sobre estrategia empresarial",
        "extracto_template": "{autor}, {rol}, reflexiona sobre cómo las organizaciones pueden anticipar los cambios del mercado y adaptarse estratégicamente. Esta visión alineada con la metodología de GL Strategic de ingeniería de anticipación.",
    },
    "transformacion": {
        "titulo_template": "{autor} analiza transformación digital en organizaciones",
        "extracto_template": "{autor}, {rol}, comparte experiencias sobre cómo implementar transformación digital efectiva. GL Strategic acompaña a empresas en estos procesos de cambio integrado.",
    },
    "liderazgo": {
        "titulo_template": "{autor} reflexiona sobre liderazgo adaptativo",
        "extracto_template": "{autor}, {rol}, destaca la importancia del liderazgo colaborativo y la construcción de equipos adaptativos. Conceptos clave en la metodología de gestión de GL Strategic.",
    },
}

def crear_noticia_manualmente(autor_nombre):
    """Abre editor para redactar noticia manualmente"""
    print(f"\n[REDACTAR] Noticia de {autor_nombre}")
    print("─" * 60)
    
    # Obtener datos del equipo
    datos = TEAM_PROFILES.get(autor_nombre)
    if not datos:
        return None
    
    rol, imagen, url = datos
    
    print(f"Autor: {autor_nombre}")
    print(f"Rol: {rol}")
    print(f"URL: {url}")
    print()
    
    # Preguntar categoría
    print("Categorías disponibles:")
    print("[1] estrategia - Temas de anticipación y estrategia")
    print("[2] transformacion - Temas de transformación digital")
    print("[3] liderazgo - Temas de liderazgo y cultura")
    cat_choice = input("Categoría (1-3): ").strip()
    
    categoria_map = {"1": "estrategia", "2": "transformacion", "3": "liderazgo"}
    categoria = categoria_map.get(cat_choice, "estrategia")
    
    plantilla = PLANTILLAS[categoria]
    
    # Generar sugerencias
    print("\n" + "─" * 60)
    print("SUGERENCIAS (puedes editar o escribir tu propia noticia):")
    print("─" * 60)
    
    titulo_sugerido = plantilla["titulo_template"].format(autor=autor_nombre)
    extracto_sugerido = plantilla["extracto_template"].format(autor=autor_nombre, rol=rol)
    
    print(f"\nTítulo sugerido:\n{titulo_sugerido}")
    print(f"\nExracto sugerido:\n{extracto_sugerido}")
    
    # Permitir editar
    print("\n" + "─" * 60)
    usar_sugerencias = input("\n¿Usar sugerencias? (s/n): ").strip().lower() == "s"
    
    if usar_sugerencias:
        titulo = titulo_sugerido
        extracto = extracto_sugerido
    else:
        print("\nEscribe tu propia noticia:")
        titulo = input("Título: ").strip()
        extracto = input("Extracto: ").strip()
    
    if not titulo or not extracto:
        print("[ERROR] Título y extracto son obligatorios")
        return None
    
    return {
        "titulo": titulo,
        "extracto": extracto,
        "autor": autor_nombre,
        "rol": rol,
        "imagen_autor": imagen,
        "url": url,
        "categoria": categoria,
    }

def guardar_noticia(noticia):
    """Guarda noticia en noticias.json"""
    json_path = Path(__file__).parent.parent / "assets" / "data" / "noticias.json"
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"noticias": []}
    
    # Generar ID
    new_id = max([n.get("id", 0) for n in data.get("noticias", [])] or [0]) + 1
    
    noticia_final = {
        "id": new_id,
        "titulo": noticia["titulo"],
        "extracto": noticia["extracto"],
        "autor": noticia["autor"],
        "rol": noticia["rol"],
        "imagen_autor": noticia["imagen_autor"],
        "tipo": "linkedin",
        "url": noticia["url"],
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "categoria": noticia["categoria"]
    }
    
    data["noticias"].append(noticia_final)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Noticia #{new_id} agregada")
    print(f"Título: {noticia['titulo'][:60]}...")
    return new_id

def main():
    print("════════════════════════════════════════════════════════")
    print("  REDACTOR DE NOTICIAS - GL Strategic")
    print("════════════════════════════════════════════════════════\n")
    
    # Mostrar equipo disponible
    print("Equipo disponible:")
    miembros = list(TEAM_PROFILES.keys())
    for i, nombre in enumerate(miembros, 1):
        rol, _, _ = TEAM_PROFILES[nombre]
        print(f"[{i}] {nombre} - {rol}")
    
    print("\n[0] Salir")
    
    while True:
        opcion = input("\nSelecciona miembro: ").strip()
        
        if opcion == "0":
            break
        
        try:
            idx = int(opcion) - 1
            if 0 <= idx < len(miembros):
                autor = miembros[idx]
                noticia = crear_noticia_manualmente(autor)
                if noticia:
                    confirm = input("\n¿Guardar noticia? (s/n): ").strip().lower() == "s"
                    if confirm:
                        guardar_noticia(noticia)
                        print("\n✅ ¡Noticia publicada!")
        except:
            pass

if __name__ == "__main__":
    main()
