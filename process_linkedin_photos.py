#!/usr/bin/env python3
"""
Script para procesar fotos de perfil de LinkedIn
Elimina fondo, optimiza y guarda en PNG con alta calidad

Autor: GL Strategic
Requisitos: Python 3.8+, rembg, Pillow
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
from rembg import remove
import io
import re
from typing import Tuple, Optional

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Carpetas de entrada y salida
CARPETA_ENTRADA = Path("assets/raw_linkedin_photos")
CARPETA_SALIDA = Path("assets/images")

# Parámetros de procesamiento
TAMAÑO_SALIDA = 1000  # píxeles (lienzo cuadrado)
BRILLO = 1.05  # ligero aumento de brillo (1.0 = sin cambios)
CONTRASTE = 1.10  # ligero aumento de contraste (1.0 = sin cambios)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def normalizar_nombre_archivo(nombre_original: str) -> str:
    """
    Convierte el nombre del archivo al formato requerido:
    - Minúsculas
    - Espacios reemplazados por _
    - Sin acentos ni caracteres especiales
    - Extensión .png

    Args:
        nombre_original: Nombre del archivo original (ej: "Guillermo Muñoz.png")

    Returns:
        str: Nombre normalizado (ej: "guillermo_munoz.png")
    """
    # Remover extensión
    nombre_sin_ext = Path(nombre_original).stem

    # Convertir a minúsculas
    nombre = nombre_sin_ext.lower()

    # Remover acentos (diccionario de reemplazos)
    acentos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
    }
    for acentuado, sin_acento in acentos.items():
        nombre = nombre.replace(acentuado, sin_acento)

    # Reemplazar espacios y guiones por _
    nombre = re.sub(r'[\s\-]+', '_', nombre)

    # Remover caracteres especiales (mantener solo letras, números y _)
    nombre = re.sub(r'[^a-z0-9_]', '', nombre)

    # Remover _ múltiples consecutivos
    nombre = re.sub(r'_+', '_', nombre)

    # Remover _ al inicio y final
    nombre = nombre.strip('_')

    return f"{nombre}.png"


def encontrar_siguiente_backup(ruta: Path) -> Path:
    """
    Encuentra el siguiente número de backup disponible.
    Si existe foto.png, lo renombra a foto_01.png, foto_02.png, etc.

    Args:
        ruta: Ruta del archivo a procesar

    Returns:
        Path: Ruta del siguiente archivo de backup disponible
    """
    if not ruta.exists():
        return None

    # Extraer nombre base y extensión
    nombre_base = ruta.stem
    extension = ruta.suffix

    # Buscar el siguiente número disponible
    contador = 1
    while True:
        nombre_backup = f"{nombre_base}_{contador:02d}{extension}"
        ruta_backup = ruta.parent / nombre_backup

        if not ruta_backup.exists():
            return ruta_backup

        contador += 1


def respaldar_archivo_existente(ruta: Path) -> Optional[Path]:
    """
    Respalda un archivo existente con numeración incremental.

    Args:
        ruta: Ruta del archivo a respaldar

    Returns:
        Path: Ruta del archivo de backup creado, o None si no existía
    """
    if not ruta.exists():
        return None

    ruta_backup = encontrar_siguiente_backup(ruta)
    ruta.rename(ruta_backup)
    return ruta_backup


def quitar_fondo(imagen_path: Path) -> Image.Image:
    """
    Elimina el fondo de una imagen usando rembg (IA local).

    Args:
        imagen_path: Ruta de la imagen original

    Returns:
        Image.Image: Imagen sin fondo (con canal alfa)

    Raises:
        Exception: Si hay error al procesar la imagen
    """
    try:
        # Leer imagen original
        with open(imagen_path, 'rb') as archivo:
            datos_imagen = archivo.read()

        # Usar rembg para remover fondo
        datos_sin_fondo = remove(datos_imagen)

        # Convertir a objeto PIL Image
        imagen = Image.open(io.BytesIO(datos_sin_fondo))

        # Asegurar que tiene canal alfa (transparencia)
        if imagen.mode != 'RGBA':
            imagen = imagen.convert('RGBA')

        return imagen

    except Exception as e:
        raise Exception(f"Error al quitar fondo: {str(e)}")


def centrar_en_lienzo(imagen: Image.Image, tamaño_lienzo: int) -> Image.Image:
    """
    Coloca la imagen en el centro de un lienzo cuadrado.
    Mantiene proporciones y centra el contenido.

    Args:
        imagen: Imagen sin fondo (RGBA)
        tamaño_lienzo: Tamaño del lienzo cuadrado (ej: 1000)

    Returns:
        Image.Image: Nueva imagen con el lienzo cuadrado
    """
    # Crear lienzo cuadrado transparente
    lienzo = Image.new('RGBA', (tamaño_lienzo, tamaño_lienzo), (255, 255, 255, 0))

    # Redimensionar imagen manteniendo proporciones
    # Dejar margen de 50px a cada lado
    margen = 50
    tamaño_disponible = tamaño_lienzo - (margen * 2)

    # Escalar imagen para que encaje en el espacio disponible
    imagen.thumbnail((tamaño_disponible, tamaño_disponible), Image.Resampling.LANCZOS)

    # Calcular posición para centrar
    x = (tamaño_lienzo - imagen.width) // 2
    y = (tamaño_lienzo - imagen.height) // 2

    # Pegar imagen en el centro del lienzo
    lienzo.paste(imagen, (x, y), imagen)

    return lienzo


def mejorar_brillo_contraste(imagen: Image.Image, brillo: float, contraste: float) -> Image.Image:
    """
    Aplica ajustes ligeros de brillo y contraste.

    Args:
        imagen: Imagen a mejorar (RGBA)
        brillo: Factor de brillo (1.0 = sin cambios, 1.1 = 10% más brillante)
        contraste: Factor de contraste (1.0 = sin cambios, 1.1 = 10% más contraste)

    Returns:
        Image.Image: Imagen mejorada
    """
    # Aplicar brillo
    if brillo != 1.0:
        mejora_brillo = ImageEnhance.Brightness(imagen)
        imagen = mejora_brillo.enhance(brillo)

    # Aplicar contraste
    if contraste != 1.0:
        mejora_contraste = ImageEnhance.Contrast(imagen)
        imagen = mejora_contraste.enhance(contraste)

    return imagen


def procesar_imagen(imagen_entrada: Path, imagen_salida: Path,
                   tamaño: int, brillo: float, contraste: float) -> bool:
    """
    Procesa una imagen completa: quita fondo, centra y mejora.

    Args:
        imagen_entrada: Ruta de imagen original
        imagen_salida: Ruta de imagen de salida
        tamaño: Tamaño del lienzo cuadrado
        brillo: Factor de brillo
        contraste: Factor de contraste

    Returns:
        bool: True si fue exitoso, False si hubo error
    """
    try:
        # Paso 1: Quitar fondo
        print(f"  📷 Quitando fondo...", end=" ", flush=True)
        imagen = quitar_fondo(imagen_entrada)
        print("✓", end=" ", flush=True)

        # Paso 2: Centrar en lienzo
        print(f"📐 Centrando...", end=" ", flush=True)
        imagen = centrar_en_lienzo(imagen, tamaño)
        print("✓", end=" ", flush=True)

        # Paso 3: Mejorar
        print(f"✨ Mejorando...", end=" ", flush=True)
        imagen = mejorar_brillo_contraste(imagen, brillo, contraste)
        print("✓", end=" ", flush=True)

        # Paso 4: Guardar
        print(f"💾 Guardando...", end=" ", flush=True)

        # Respaldar si existe
        backup = respaldar_archivo_existente(imagen_salida)
        if backup:
            print(f"\n     ⚠️  Respaldado anterior: {backup.name}")
            print(f"  ", end="")

        # Guardar en PNG con optimización
        imagen.save(imagen_salida, 'PNG', optimize=True)
        print("✓")

        return True

    except Exception as e:
        print(f"\n     ❌ Error: {str(e)}")
        return False


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """
    Función principal: orquesta el procesamiento de todas las imágenes.
    """
    print("\n" + "=" * 70)
    print("🎨 PROCESADOR DE FOTOS DE LINKEDIN - GL Strategic")
    print("=" * 70 + "\n")

    # Verificar que existan las carpetas
    if not CARPETA_ENTRADA.exists():
        print(f"❌ ERROR: No existe la carpeta de entrada: {CARPETA_ENTRADA}")
        print(f"\n📁 Crea la carpeta manualmente:")
        print(f"   mkdir {CARPETA_ENTRADA}")
        print(f"\n📥 Descarga las fotos de LinkedIn y guárdalas ahí.\n")
        sys.exit(1)

    # Crear carpeta de salida si no existe
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

    # Buscar imágenes en la carpeta de entrada
    extensiones = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    imagenes = [f for f in CARPETA_ENTRADA.iterdir()
                if f.is_file() and f.suffix.lower() in extensiones]

    if not imagenes:
        print(f"⚠️  No se encontraron imágenes en: {CARPETA_ENTRADA}")
        print(f"📥 Descarga las fotos y guárdalas en esa carpeta.\n")
        sys.exit(0)

    print(f"📂 Procesando {len(imagenes)} imagen(es) de {CARPETA_ENTRADA}...\n")

    # Estadísticas
    exitosas = 0
    fallidas = 0
    detalles = []

    # Procesar cada imagen
    for idx, imagen_entrada in enumerate(imagenes, 1):
        nombre_original = imagen_entrada.name
        nombre_normalizado = normalizar_nombre_archivo(nombre_original)
        imagen_salida = CARPETA_SALIDA / nombre_normalizado

        print(f"[{idx}/{len(imagenes)}] {nombre_original}")
        print(f"       → {nombre_normalizado}")
        print(f"       ", end="")

        # Procesar
        if procesar_imagen(imagen_entrada, imagen_salida, TAMAÑO_SALIDA, BRILLO, CONTRASTE):
            exitosas += 1
            detalles.append(f"✅ {nombre_normalizado}")
        else:
            fallidas += 1
            detalles.append(f"❌ {nombre_original} (error)")

        print()

    # Mostrar resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL PROCESAMIENTO")
    print("=" * 70)
    print(f"✅ Exitosas: {exitosas}")
    print(f"❌ Fallidas: {fallidas}")
    print(f"📊 Total: {len(imagenes)}")
    print(f"\n📁 Salida: {CARPETA_SALIDA.absolute()}\n")

    if exitosas == len(imagenes):
        print("🎉 ¡Todas las imágenes se procesaron correctamente!\n")
    elif fallidas > 0:
        print(f"⚠️  {fallidas} imagen(es) tuvieron errores. Revisa los mensajes arriba.\n")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
