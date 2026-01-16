#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gestor de Noticias - Permite redactar y publicar noticias de LinkedIn
en el sistema de noticias dinámicas del website
"""

import json
from pathlib import Path
from datetime import datetime

# ==================== CONFIG ====================
ROOT = Path(__file__).parent.parent
NOTICIAS_FILE = ROOT / "assets" / "data" / "noticias.json"

# ==================== HELPER ====================
def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def load_noticias():
    """Carga noticias actuales"""
    if NOTICIAS_FILE.exists():
        return json.loads(NOTICIAS_FILE.read_text(encoding='utf-8'))
    return {"noticias": []}

def save_noticias(data):
    """Guarda noticias"""
    NOTICIAS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    log(f"Guardado en {NOTICIAS_FILE}", "OK")

def get_next_id(noticias):
    """Obtiene el próximo ID"""
    if not noticias["noticias"]:
        return 1
    return max(n["id"] for n in noticias["noticias"]) + 1

def add_noticia():
    """Interfaz para añadir noticia"""
    log("\n" + "=" * 60, "INFO")
    log("AGREGAR NUEVA NOTICIA", "INFO")
    log("=" * 60, "INFO")
    
    noticias = load_noticias()
    
    # Recopilar datos
    print("\n[DATOS DE LA NOTICIA]")
    titulo = input("Título: ").strip()
    extracto = input("Extracto (párrafo introductorio): ").strip()
    autor = input("Autor (nombre completo): ").strip()
    rol = input("Rol/posición: ").strip()
    imagen_autor = input("Imagen del autor (ej: javier_delamaza.png): ").strip()
    url = input("URL LinkedIn (ej: https://www.linkedin.com/in/...): ").strip()
    categoria = input("Categoría (estrategia/transformacion/liderazgo): ").strip()
    
    # Validar categoría
    categorias_validas = ["estrategia", "transformacion", "liderazgo"]
    if categoria not in categorias_validas:
        log(f"Categoría inválida. Usa: {', '.join(categorias_validas)}", "ERROR")
        return
    
    # Crear noticia
    noticia = {
        "id": get_next_id(noticias),
        "titulo": titulo,
        "extracto": extracto,
        "autor": autor,
        "rol": rol,
        "imagen_autor": imagen_autor,
        "tipo": "linkedin",
        "url": url,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "categoria": categoria
    }
    
    # Mostrar previa
    log("\n" + "=" * 60, "INFO")
    log("PREVIA DE NOTICIA", "INFO")
    log("=" * 60, "INFO")
    print(json.dumps(noticia, ensure_ascii=False, indent=2))
    
    # Confirmar
    confirmar = input("\n¿Guardar noticia? (s/n): ").strip().lower()
    if confirmar != 's':
        log("Cancelado", "SKIP")
        return
    
    # Guardar
    noticias["noticias"].insert(0, noticia)  # Insertar al inicio (más reciente)
    save_noticias(noticias)
    log(f"Noticia #{noticia['id']} agregada exitosamente", "OK")

def list_noticias():
    """Listar todas las noticias"""
    noticias = load_noticias()
    
    log("\n" + "=" * 60, "INFO")
    log(f"NOTICIAS ACTUALES ({len(noticias['noticias'])} total)", "INFO")
    log("=" * 60, "INFO")
    
    for noticia in noticias["noticias"]:
        print(f"\n#{noticia['id']} [{noticia['categoria'].upper()}]")
        print(f"   Título: {noticia['titulo']}")
        print(f"   Autor: {noticia['autor']} ({noticia['rol']})")
        print(f"   Fecha: {noticia['fecha']}")
        print(f"   URL: {noticia['url']}")

def delete_noticia():
    """Eliminar una noticia"""
    noticias = load_noticias()
    
    if not noticias["noticias"]:
        log("No hay noticias para eliminar", "WARN")
        return
    
    # Listar
    log("\n" + "=" * 60, "INFO")
    log("SELECCIONAR NOTICIA A ELIMINAR", "INFO")
    log("=" * 60, "INFO")
    
    for noticia in noticias["noticias"]:
        print(f"[{noticia['id']}] {noticia['titulo']} - {noticia['autor']}")
    
    try:
        noticia_id = int(input("\nID a eliminar: ").strip())
        
        noticias["noticias"] = [n for n in noticias["noticias"] if n["id"] != noticia_id]
        save_noticias(noticias)
        log(f"Noticia #{noticia_id} eliminada", "OK")
        
    except ValueError:
        log("ID inválido", "ERROR")

def edit_noticia():
    """Editar una noticia existente"""
    noticias = load_noticias()
    
    if not noticias["noticias"]:
        log("No hay noticias para editar", "WARN")
        return
    
    # Listar
    log("\n" + "=" * 60, "INFO")
    log("SELECCIONAR NOTICIA A EDITAR", "INFO")
    log("=" * 60, "INFO")
    
    for noticia in noticias["noticias"]:
        print(f"[{noticia['id']}] {noticia['titulo']}")
    
    try:
        noticia_id = int(input("\nID a editar: ").strip())
        
        noticia = next((n for n in noticias["noticias"] if n["id"] == noticia_id), None)
        if not noticia:
            log("Noticia no encontrada", "ERROR")
            return
        
        print("\nNOTA: Deja vacío para no cambiar\n")
        
        nuevo_titulo = input(f"Título [{noticia['titulo']}]: ").strip()
        if nuevo_titulo:
            noticia['titulo'] = nuevo_titulo
        
        nuevo_extracto = input(f"Extracto (primeros 50 cars) [{noticia['extracto'][:50]}...]: ").strip()
        if nuevo_extracto:
            noticia['extracto'] = nuevo_extracto
        
        # Mostrar y confirmar
        log("\n" + "=" * 60, "INFO")
        log("NOTICIA EDITADA", "INFO")
        log("=" * 60, "INFO")
        print(json.dumps(noticia, ensure_ascii=False, indent=2))
        
        confirmar = input("\n¿Guardar cambios? (s/n): ").strip().lower()
        if confirmar == 's':
            save_noticias(noticias)
            log("Noticia editada exitosamente", "OK")
        else:
            log("Cancelado", "SKIP")
        
    except ValueError:
        log("ID inválido", "ERROR")

def main():
    """Menu principal"""
    while True:
        print("\n" + "=" * 60)
        print("GESTOR DE NOTICIAS - GL Strategic")
        print("=" * 60)
        print("[1] Agregar noticia")
        print("[2] Listar noticias")
        print("[3] Editar noticia")
        print("[4] Eliminar noticia")
        print("[5] Salir")
        print()
        
        opcion = input("Opción: ").strip()
        
        if opcion == "1":
            add_noticia()
        elif opcion == "2":
            list_noticias()
        elif opcion == "3":
            edit_noticia()
        elif opcion == "4":
            delete_noticia()
        elif opcion == "5":
            log("Saliendo...", "INFO")
            break
        else:
            log("Opción inválida", "ERROR")

if __name__ == "__main__":
    main()
