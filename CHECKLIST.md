# 📋 CHECKLIST RÁPIDO - GL STRATEGIC FOTOS

## ✅ Situación Actual (15 Enero 2026)

- [x] Todas las fotos normalizadas (83 total)
- [x] 20/20 fotos de equipo presentes
- [x] Nombres consistentes (minúsculas, sin acentos)
- [x] Tamaños estandarizados (1000x1000px)
- [x] HTML actualizado (.jfif → .png)
- [x] Dependencias instaladas (Pillow)
- [x] Scripts de automatización listos
- [x] Documentación completa

---

## 🚀 Cómo Ejecutar

### Opción 1: AUTOMÁTICO (Recomendado)
```bash
# Simplemente haz doble-click en:
AUTOMATOR.bat

# O desde PowerShell:
.\post_process.ps1
```

### Opción 2: MANUAL (Paso a paso)
```bash
# Solo normalizar
python normalize_all_photos.py

# Solo auditar
python audit_fotos.py

# Monitor tiempo real
python watchdog_fotos.py
```

---

## 📸 Agregar Nuevas Fotos

### Flujo Rápido (60 segundos)

1. **Opción A:** Coloca foto en `assets/images/` directamente
   ```
   assets/images/nuevo_nombre.jpg
   ↓
   (automático) → nuevo_nombre.png (normalizada)
   ```
   Luego ejecuta: `python normalize_all_photos.py`

2. **Opción B:** Descarga de LinkedIn
   ```
   assets/raw_linkedin_photos/Nombre Apellido.png
   ↓
   python process_linkedin_photos.py
   ↓
   assets/images/nombre_apellido.png (con fondo quitado)
   ```

3. **Opción C:** Monitor automático (Recomendado)
   ```
   python watchdog_fotos.py
   (dejar corriendo)
   
   → Sube nueva foto a assets/images/
   → Se normaliza automáticamente
   ```

---

## 🔍 Verificar Estado

```bash
# Ver qué fotos faltan
python audit_fotos.py

# Ver todas las fotos disponibles
Get-ChildItem assets/images -Filter "*.png" | Format-Table Name
```

---

## 🛠️ Tareas Comunes

| Tarea | Comando | Tiempo |
|-------|---------|--------|
| Normalizar todo | `python normalize_all_photos.py` | 5-10s |
| Verificar estado | `python audit_fotos.py` | 1s |
| Monitor automático | `python watchdog_fotos.py` | ∞ |
| Generar reporte | `.\post_process.ps1` | 30s |
| Ver documentación | `type README_FOTOS.md` | 1min |

---

## ⚙️ Especificaciones

| Parámetro | Valor |
|-----------|-------|
| Canvas | 1000 × 1000 px |
| Fondo | Transparente (RGBA) |
| Brillo | +5% (1.05x) |
| Contraste | +10% (1.10x) |
| Compresión | PNG optimize=True |
| Margen | 50px en cada lado |
| Formato salida | `.png` minúsculas |

---

## 🆘 Troubleshooting

### "Fotos no se ven en web"
→ Ejecuta: `python audit_fotos.py` → Verifica nombres exactos

### "Script muy lento"
→ Normal, procesa 83 fotos. Espera 10-30 segundos.

### "Error: Python no encontrado"
→ Ejecuta desde: `AUTOMATOR.bat` en lugar de terminal

### "Foto se ve cortada/distorsionada"
→ Edita `normalize_all_photos.py` → línea "margen = 50" → aumenta a 100

### "Quiero cambiar brillo/contraste"
→ Edita `normalize_all_photos.py` → función `mejorar_brillo_contraste()`
```python
enhancer.enhance(1.05)  # +5% brillo → cambiar a 1.10 (más brillante)
enhancer.enhance(1.10)  # +10% contraste → cambiar a 1.20 (más contraste)
```

---

## 📊 Estadísticas Actuales

```
Total fotos:         83
Fotos de equipo:     20/20 ✅
Normalizadas:        22 (hoy)
Saltadas:            61 (ya OK)
Faltantes:           0
Errores:             0
Estado:              PRODUCCIÓN LISTA ✅
```

---

## 🔐 Respaldos Automáticos

Si sobrescribes un archivo, automáticamente crea:
```
archivo.png           (nueva versión)
archivo_01.png        (respaldo anterior)
archivo_02.png        (respaldo anterior+1)
...
```

---

## 📱 En Desarrollo

Para usar el watchdog mientras desarrollas:
```bash
# Terminal 1: Ejecutar watchdog
python watchdog_fotos.py

# Terminal 2: Hacer cambios, sube fotos
# Terminal 1: Automáticamente las normaliza
```

---

## 🎯 Resumen de Estado

✅ **COMPLETADO**
- Todas las fotos normalizadas
- HTML actualizado
- Scripts funcionando
- Documentación lista
- 0 errores

⚠️ **OPCIONAL**
- Quitar fondos con IA (requiere descargar de LinkedIn)
- Ajustar brillo/contraste según preferencia

🚀 **LISTO PARA PRODUCCIÓN**

---

**Última actualización:** 15 Enero 2026  
**Versión:** 2.0  
**Estado:** AUTOMATIZACIÓN COMPLETA ✅
