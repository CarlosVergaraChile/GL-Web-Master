# 📸 Guía Completa: Procesamiento de Fotos de LinkedIn

## 📋 Contenido

1. [¿Qué hace este script?](#qué-hace-este-script)
2. [Requisitos previos](#requisitos-previos)
3. [Instalación paso a paso](#instalación-paso-a-paso)
4. [Descargar fotos de LinkedIn](#descargar-fotos-de-linkedin)
5. [Ejecutar el script](#ejecutar-el-script)
6. [Resultados esperados](#resultados-esperados)
7. [Solucionar problemas](#solucionar-problemas)

---

## ¿Qué hace este script?

El script `process_linkedin_photos.py` **automáticamente**:

- ✅ **Quita el fondo** de las fotos (transparencia inteligente)
- ✅ **Centra** la foto en un lienzo cuadrado (1000x1000 píxeles)
- ✅ **Mejora** brillo y contraste ligeramente
- ✅ **Convierte** a PNG con alta calidad
- ✅ **Renombra** los archivos de forma consistente (minúsculas, sin acentos)
- ✅ **Respalda** automáticamente archivos antiguos

**Entrada:** Carpeta `assets/raw_linkedin_photos/`  
**Salida:** Carpeta `assets/images/` con archivos `.png`

---

## Requisitos previos

Necesitas:

- **Windows 10 o superior**
- **Python 3.8 o superior** ([descargar aquí](https://www.python.org/downloads/))
  - ✅ **IMPORTANTE:** Marca la casilla "**Add Python to PATH**" durante la instalación
- **VS Code** (que probablemente ya tienes)
- **Conexión a internet** (para descargar librerías Python)

### Verificar instalación de Python

Abre PowerShell y escribe:

```powershell
python --version
```

Deberías ver algo como: `Python 3.11.7`

Si ves error, asegúrate de haber marcado "Add Python to PATH" en la instalación.

---

## Instalación paso a paso

### Paso 1: Abrir Terminal en VS Code

1. Abre VS Code
2. Abre la carpeta del proyecto: `C:\Proyectos\GL-Web-Master`
3. Presiona `Ctrl + ñ` (o `Ctrl + ~`) para abrir la terminal integrada
4. **Importante:** Verifica que estés en la carpeta correcta (debería decir algo como `PS C:\Proyectos\GL-Web-Master>`)

### Paso 2: Crear un entorno virtual de Python

Un **entorno virtual** es como una caja aislada donde Python instala las librerías solo para este proyecto. Esto evita conflictos con otros proyectos.

En PowerShell, escribe:

```powershell
python -m venv venv
```

⏳ Esto tardará 10-30 segundos. Debería crear una carpeta llamada `venv/`.

### Paso 3: Activar el entorno virtual

Aún en PowerShell, escribe:

```powershell
venv\Scripts\Activate.ps1
```

✅ **Éxito:** Deberías ver `(venv)` al inicio de tu línea, así:

```
(venv) PS C:\Proyectos\GL-Web-Master>
```

Si ves un error como `cannot be loaded because running scripts is disabled on this system`:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta de nuevo:

```powershell
venv\Scripts\Activate.ps1
```

### Paso 4: Instalar dependencias

Ahora escribe:

```powershell
pip install -r requirements.txt
```

⏳ **Paciencia:** Esto tardará **2-5 minutos**. Python descargará e instalará:
- `rembg` (quita fondos con inteligencia artificial)
- `Pillow` (procesa imágenes)
- `numpy`, `torch`, `onnxruntime` (librerías de soporte)

Espera a que termine completamente. **NO cierres la terminal.**

✅ **Éxito:** Deberías ver un mensaje como:
```
Successfully installed rembg-2.0.50 Pillow-10.1.0 ...
```

---

## Descargar fotos de LinkedIn

Antes de ejecutar el script, necesitas **descargar manualmente** las fotos de los perfiles de LinkedIn.

### ¿Por qué manualmente?

LinkedIn no permite descargas automáticas. Debemos hacerlo a mano, pero es rápido (2-3 minutos para 8 fotos).

### Pasos para descargar:

1. **Crea la carpeta de entrada:**
   - En VS Code, expande la carpeta `assets/`
   - Haz clic derecho → New Folder
   - Nombra: `raw_linkedin_photos`

2. **Para cada persona en el equipo:**
   - Abre su perfil de LinkedIn
   - Haz clic en su foto de perfil (la imagen grande de su cara)
   - Haz clic derecho → "Guardar imagen como..."
   - **Carpeta destino:** `C:\Proyectos\GL-Web-Master\assets\raw_linkedin_photos`
   - **Nombre:** Usa el nombre completo, así:
     - `Guillermo Muñoz.png`
     - `Claudio Maggi Campos.png`
     - `Rafael Sotil.png`
     - etc.

### Ejemplo visual:

```
assets/
├── raw_linkedin_photos/
│   ├── Guillermo Muñoz.png
│   ├── Claudio Maggi Campos.png
│   ├── Rafael Sotil.png
│   └── ... (más fotos)
│
└── images/
    └── (aquí irán los resultados)
```

---

## Ejecutar el script

Una vez tengas las fotos en `assets/raw_linkedin_photos/`:

### En la misma terminal PowerShell (con `(venv)` activado):

```powershell
python process_linkedin_photos.py
```

### ¿Qué verás?

El script mostrará un progreso así:

```
======================================================================
🎨 PROCESADOR DE FOTOS DE LINKEDIN - GL Strategic
======================================================================

📂 Procesando 8 imagen(es) de assets/raw_linkedin_photos...

[1/8] Guillermo Muñoz.png
       → guillermo_munoz.png
        📷 Quitando fondo... ✓ 📐 Centrando... ✓ ✨ Mejorando... ✓ 💾 Guardando... ✓

[2/8] Claudio Maggi Campos.png
       → claudio_maggi_campos.png
        📷 Quitando fondo... ✓ 📐 Centrando... ✓ ✨ Mejorando... ✓ 💾 Guardando... ✓

...

======================================================================
📊 RESUMEN DEL PROCESAMIENTO
======================================================================
✅ Exitosas: 8
❌ Fallidas: 0
📊 Total: 8

📁 Salida: C:\Proyectos\GL-Web-Master\assets\images

🎉 ¡Todas las imágenes se procesaron correctamente!

======================================================================
```

---

## Resultados esperados

### Carpeta `assets/images/`

Después de ejecutar el script, deberías tener:

```
assets/images/
├── guillermo_munoz.png
├── claudio_maggi_campos.png
├── rafael_sotil.png
├── pablo_canobra.png
├── edith_wilson.png
├── javier_delamaza.png
├── jose_inostroza.png
├── jenny_sauterel_soto.png
│
├── guillermo_munoz_01.png      ⬅️ Respaldo del anterior
├── claudio_maggi_campos_01.png  ⬅️ Respaldo del anterior
└── ... (más respaldos si existían archivos viejos)
```

### Propiedades de las fotos:

- ✅ **Formato:** PNG
- ✅ **Tamaño:** 1000x1000 píxeles
- ✅ **Fondo:** Transparente (removido)
- ✅ **Rostro/parte principal:** Centrada
- ✅ **Brillo/Contraste:** Ligeramente mejorado
- ✅ **Nombre:** Minúsculas, sin acentos, guiones bajos (no espacios)

---

## Solucionar problemas

### ❌ "No se encuentra el módulo 'rembg'"

**Causa:** Las dependencias no se instalaron.

**Solución:**
1. Verifica que `(venv)` está activado (aparece al inicio de la línea)
2. Ejecuta de nuevo:
   ```powershell
   pip install -r requirements.txt
   ```
3. Espera a que termine completamente

### ❌ "No existe la carpeta de entrada"

**Causa:** No creaste `assets/raw_linkedin_photos/` o no descargaste las fotos.

**Solución:**
1. Crea la carpeta:
   ```powershell
   mkdir assets/raw_linkedin_photos
   ```
2. Descarga las fotos de LinkedIn ahí (pasos arriba)
3. Intenta de nuevo

### ❌ "Error al quitar fondo"

**Causa:** La foto probablemente está corrupta o en formato no soportado.

**Solución:**
1. Descarga la foto de LinkedIn de nuevo
2. Asegúrate de guardar como PNG o JPG (no WebP ni BMP)
3. Intenta de nuevo

### ⚠️ El script tarda mucho en procesar

**Causa:** Normal. rembg usa inteligencia artificial, puede tardar 5-10 segundos por foto en la primera ejecución.

**Solución:** Paciencia 😊. En máquinas más potentes es más rápido.

### ❌ "ExecutionPolicy" error

**Causa:** Windows bloqueó la ejecución de scripts.

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Responde `Y` cuando pregunten.

---

## Desactivar el entorno virtual (opcional)

Cuando termines, puedes desactivar el entorno virtual escribiendo:

```powershell
deactivate
```

(La próxima vez que quieras usar el script, actívalo de nuevo.)

---

## ¿Preguntas?

Si algo no funciona:

1. **Copia el mensaje de error exacto**
2. **Verifica que Python 3.8+ esté instalado:** `python --version`
3. **Verifica que estés en la carpeta correcta:** `pwd` (debería mostrar `C:\Proyectos\GL-Web-Master`)
4. **Verifica que `(venv)` esté activado** (aparece al inicio de la línea de PowerShell)

¡Éxito! 🚀

3. **Volver a ejecutar:**
   ```powershell
   .\process_photos.ps1
   ```

4. **Quitar fondo manualmente:**
   - Ve a https://remove.bg
   - Sube cada foto desde `assets/images/`
   - Descarga el resultado y reemplaza

---

## Enlaces de LinkedIn (referencia rápida)

- Guillermo Muñoz: https://www.linkedin.com/in/guillermomunoz/
- Claus van der Molen: https://www.linkedin.com/in/clausvandermolen/
- Claudio Maggi: https://www.linkedin.com/in/claudiomaggi
- Pablo Canobra: https://www.linkedin.com/in/pablocanobra
- Javier Delamaza: https://www.linkedin.com/in/javier-e-díaz-calderón-08abb222
- José Ignacio Martínez: https://www.linkedin.com/in/jose-ignacio-martinez-acevedo-41683845
- Paula Jadue: https://www.linkedin.com/in/paula-jadue-abuyeres/
- Jaime Soto: https://www.linkedin.com/in/jaime-soto-zura-0a060220b

---

## Notas

- Las fotos existentes se respaldarán automáticamente como `*_01.png`
- El script Python usa IA local para quitar el fondo (no requiere internet)
- El script PowerShell requiere .NET Framework (ya instalado en Windows)
- Tamaño recomendado final: ~400x500px para uniformidad
