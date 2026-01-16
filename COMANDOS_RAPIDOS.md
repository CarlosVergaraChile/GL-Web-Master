# ⚡ COMANDOS RÁPIDOS - Procesamiento de Fotos LinkedIn

## 🎯 Flujo Completo (Copiar y Pegar en PowerShell)

### Paso 1️⃣ : Crear Carpeta para Fotos
```powershell
mkdir assets/raw_linkedin_photos
```

### Paso 2️⃣ : Descargar Fotos Manualmente
1. Abre cada perfil en LinkedIn
2. Clic derecho en foto → Guardar imagen como...
3. Guarda en: `C:\Proyectos\GL-Web-Master\assets\raw_linkedin_photos`
4. Con nombre: `Nombre Apellido.png` (ej: `Guillermo Muñoz.png`)

⏱️ Tiempo estimado: 2-3 minutos para 8 fotos

### Paso 3️⃣ : Crear Entorno Virtual
```powershell
python -m venv venv
```
⏳ Espera 10-30 segundos

### Paso 4️⃣ : Activar Entorno Virtual
```powershell
venv\Scripts\Activate.ps1
```

✅ Deberías ver `(venv)` al inicio de la línea

**Si ves error de ExecutionPolicy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Presiona `Y` y luego intenta Activate.ps1 de nuevo.

### Paso 5️⃣ : Instalar Dependencias
```powershell
pip install -r requirements.txt
```
⏳ Espera 2-5 minutos (descargará ~500MB)

### Paso 6️⃣ : Ejecutar Script
```powershell
python process_linkedin_photos.py
```

✅ **¡LISTO!** Las fotos estarán en `assets/images/`

---

## 📁 Estructura de Carpetas (Al Final)

```
C:\Proyectos\GL-Web-Master\
│
├── assets/
│   ├── raw_linkedin_photos/        ← Fotos descargadas de LinkedIn
│   │   ├── Guillermo Muñoz.png
│   │   ├── Claudio Maggi Campos.png
│   │   └── ...
│   │
│   └── images/                      ← Fotos procesadas (RESULTADO)
│       ├── guillermo_munoz.png      ← Procesada ✅
│       ├── claudio_maggi_campos.png ← Procesada ✅
│       ├── guillermo_munoz_01.png   ← Respaldo (antiguo)
│       └── ...
│
├── process_linkedin_photos.py       ← Script principal
├── requirements.txt                 ← Dependencias
├── INSTRUCCIONES_FOTOS.md          ← Guía completa
└── venv/                            ← Entorno virtual (se crea automáticamente)
```

---

## 📊 Lo Que Hace el Script

```
INPUT (fotos brutas):           PROCESSING:                    OUTPUT (fotos optimizadas):
┌─────────────────────┐         ┌──────────────────┐          ┌─────────────────────┐
│ Guillermo Muñoz.png │ ──────► │ 📷 Quitar fondo  │ ────────► │guillermo_munoz.png  │
│ (con fondo azul)    │         │ 📐 Centrar       │          │ (fondo transparente)│
│ 1920x1080px         │         │ ✨ Mejorar brillo│          │ 1000x1000px         │
└─────────────────────┘         │ 💾 Guardar PNG   │          │ PNG optimizado      │
                                └──────────────────┘          └─────────────────────┘
                                      ↓
                                   (~7-10 seg)
```

### Características:
✅ **Fondo removido** (transparencia inteligente con rembg/IA)
✅ **Lienzo 1000x1000px** (cuadrado perfecto)
✅ **Rostro centrado** (automático)
✅ **Brillo+Contraste mejorado** (ligero, natural)
✅ **PNG con optimización** (mínimo tamaño)
✅ **Nombres normalizados** (minúsculas, sin acentos, sin espacios)
✅ **Backups automáticos** (foto antigua → nombre_01.png)

---

## 🔧 Solucionar Problemas

| ❌ Problema | ✅ Solución |
|---|---|
| "python not found" | Reinstala Python marcando "Add to PATH" |
| "No module rembg" | Activa venv: `venv\Scripts\Activate.ps1` |
| "ExecutionPolicy" | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| No existen fotos | Crea carpeta: `mkdir assets/raw_linkedin_photos` |
| Carpeta vacía | Descarga fotos manualmente de LinkedIn |

---

## 💡 Consejos

- **Usar siempre el mismo terminal PowerShell** (no cierres entre pasos)
- **Las fotos de LinkedIn se guardan como JPG** → script acepta automáticamente
- **Primera ejecución es lenta** (rembg descarga modelo IA ~300MB)
- **Ejecuciones posteriores son más rápidas** (modelo ya en caché)
- **Si hay error** → copia el mensaje exacto y revisa en INSTRUCCIONES_FOTOS.md

---

## 📞 En Caso de Duda

Revisa: `INSTRUCCIONES_FOTOS.md` → Sección "Solucionar Problemas"

¡Que disfrutes! 🚀
