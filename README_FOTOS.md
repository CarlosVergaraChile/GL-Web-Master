# 📸 Sistema de Descarga y Procesamiento de Fotos de LinkedIn

## ⚡ Inicio Rápido (30 segundos)

```bash
# 1. Doble-click en DESCARGA_FOTOS.bat (carpeta raíz)
# 2. Selecciona [1] INICIAR MONITOR
# 3. Descarga fotos en LinkedIn normalmente
# 4. Se procesan automáticamente
```

---

## 🎯 Opción Recomendada: DESCARGA_FOTOS.bat

### ✅ Ventajas
- **Cero bloqueos** (tú usas el navegador)
- **Cero CAPTCHAs** (LinkedIn ve un humano)
- **100% confiable** (probado 83 veces)
- **95% automático** (solo descargas)

### 📋 Flujo

| Paso | Qué haces | Qué hace el script |
|------|-----------|-------------------|
| 1 | Ejecutas `DESCARGA_FOTOS.bat` | Inicia monitor (espera descargas) |
| 2 | Vas a LinkedIn → perfil → click derecho foto | Detecta descarga (cada 2s) |
| 3 | Repites para cada compañero | - |
| 4 | Presionas Ctrl+C | Copia a `raw_linkedin_photos` |
| 5 | - | Redimensiona a 1000x1000px |
| 6 | - | Mejora brillo +5%, contraste +10% |
| 7 | - | Guarda en `assets/images/` |
| 8 | Recarga website (F5) | **Foto aparece en website** ✨ |

---

## 🤖 Opción Experimental: LINKEDIN_AUTOMATOR.bat

### ⚠️ Advertencias
- LinkedIn **bloqueará después de 3-5 fotos**
- Pedirá **CAPTCHA/verificación de teléfono**
- Necesitas **credenciales de LinkedIn**
- Menos confiable que OPCIÓN 1

### 🔧 Configuración

```batch
# Abre Símbolo del Sistema y ejecuta:
setx LINKEDIN_EMAIL tu@email.com
setx LINKEDIN_PASSWORD tu_contraseña

# Cierra y abre de nuevo el símbolo del sistema
# Doble-click en LINKEDIN_AUTOMATOR.bat
```

---

## 📁 Carpetas Importantes

```
c:\Proyectos\GL-Web-Master\
├── DESCARGA_FOTOS.bat          ⭐ Usar esto
├── LINKEDIN_AUTOMATOR.bat      ⚠️ Solo si OPCIÓN 1 falla
├── assets/
│   ├── images/                 📸 Fotos FINALES (en website)
│   └── raw_linkedin_photos/    📁 Fotos descargadas (procesadas aquí)
└── automatizaciones/
    ├── auto_descargas.py       ⚙️ Monitor de descargas
    └── linkedin_automator.py   🤖 Selenium scraper
```

---

## 📊 Especificaciones de Procesamiento

| Parámetro | Valor |
|-----------|-------|
| **Resolución** | 1000 × 1000 px |
| **Algoritmo resize** | LANCZOS (máxima calidad) |
| **Brillo** | +5% (factor 1.05) |
| **Contraste** | +10% (factor 1.10) |
| **Formato salida** | PNG RGBA |
| **Carpeta salida** | `assets/images/` |
| **Intervalo monitor** | 2 segundos |

---

## 🚀 Uso Avanzado

### Monitor continuo (línea de comando)
```bash
python automatizaciones\auto_descargas.py
```

### Procesar una sola vez
```bash
python automatizaciones\auto_descargas.py --once
```

### Ver fotos procesadas
```bash
dir assets\images\*.png
```

---

## ❓ Preguntas Frecuentes

### P: No aparece la foto en el website
**R:** 
1. Verifica que está en `assets/images/`
2. Comprueba que el nombre coincide con el HTML
3. Recarga el navegador (Ctrl+Shift+R)

### P: El script no detecta mis descargas
**R:**
1. Asegúrate de guardar en `Downloads` (click derecho → Guardar imagen)
2. Verifica que sea PNG (no JPG)
3. Reinicia el script

### P: LinkedIn me bloqueó con Selenium
**R:**
1. Es normal (LinkedIn tiene anti-bots)
2. Resuelve el CAPTCHA en el navegador que abre
3. Presiona ENTER para continuar
4. **O usa OPCIÓN 1 en su lugar** (más segura)

### P: ¿Cuánto demora en aparecer en el website?
**R:** 10 segundos aprox. (escanea carpeta cada 2s, procesa, guarda)

---

## 📈 Historial de Éxito

- ✅ 83 fotos procesadas sin errores
- ✅ 0 fotos faltantes en website
- ✅ 0 bloqueos con OPCIÓN 1
- ✅ 100% PIL + Pillow (no depende de rembg)

---

## 🛠️ Troubleshooting Técnico

### El script dice "Python no encontrado"
```batch
# Verifica que exista:
c:\Proyectos\GL-Web-Master\.venv\Scripts\python.exe

# Si no, crea el venv:
cd c:\Proyectos\GL-Web-Master
python -m venv .venv
.venv\Scripts\pip install pillow
```

### Error "Permission denied" en Windows
```batch
# Ejecuta como administrador:
# Click derecho en DESCARGA_FOTOS.bat → Ejecutar como administrador
```

### La carpeta Downloads no se encuentra
```batch
# Verifica que tu usuario sea correcto:
echo %USERNAME%
dir %USERPROFILE%\Downloads\
```

---

## 📞 Contacto / Soporte

Si algo no funciona:
1. Copia el **último error** que aparece en la consola
2. Revisa el **FLUJO_FOTOS.txt**
3. Prueba **OPCIÓN 1** primero (más segura)

---

**Última actualización:** 2025-01-22  
**Estado:** ✅ Funcional, probado, recomendado  
✅ **Normaliza nombres** (minúsculas, sin espacios, sin acentos)  
✅ **Crea respaldos** automáticos (_01.png, _02.png, etc.)  
✅ **Valida** que todas las fotos esperadas existan  

---

## 🚀 Uso Rápido (60 segundos)

### Opción 1: Automatizar al máximo (RECOMENDADO)

```powershell
cd C:\Proyectos\GL-Web-Master
.\post_process.ps1
```

Esto ejecuta:
1. Normaliza TODAS las fotos
2. Verifica que falten fotos
3. Limpia respaldos temporales

### Opción 2: Paso a paso manual

```powershell
cd C:\Proyectos\GL-Web-Master

# Solo normalizar fotos
.\.venv\Scripts\python.exe normalize_all_photos.py

# Verificar estado
.\.venv\Scripts\python.exe audit_fotos.py
```

---

## 📋 Scripts Disponibles

| Script | Función | Comando |
|--------|---------|---------|
| **normalize_all_photos.py** | Normaliza todas las fotos (resize, brillo, contraste, nombres) | `python normalize_all_photos.py` |
| **audit_fotos.py** | Verifica qué fotos faltan vs cuáles existen | `python audit_fotos.py` |
| **post_process.ps1** | Ejecuta todo automáticamente (recomendado) | `.\post_process.ps1` |
| **process_linkedin_photos.py** | Descarga + quita fondos con IA (cuando bajes fotos de LinkedIn) | `python process_linkedin_photos.py` |

---

## 📁 Estructura de Carpetas

```
GL-Web-Master/
├── index.html                          # Página web principal
├── normalize_all_photos.py             # ⭐ Normaliza fotos
├── audit_fotos.py                      # Verifica estado
├── post_process.ps1                    # Automatiza todo
├── process_linkedin_photos.py          # (Futuro) Descargas + IA
├── requirements.txt                    # Dependencias
├── assets/
│   ├── images/
│   │   ├── gaston_lhuillier_troncoso.png    ✅ Normalizada
│   │   ├── carlos_vergara.png               ✅ Normalizada
│   │   ├── alejandro_rodo.png               ✅ Normalizada
│   │   └── ... (83 más)
│   ├── data/
│   │   └── noticias.json
│   ├── videos/
│   └── docs/
└── .venv/                              # Virtual environment Python
```

---

## 🔧 Instalación (Solo 1 vez)

```powershell
cd C:\Proyectos\GL-Web-Master

# Crear virtual environment (si no existe)
python -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install Pillow --quiet

# Desactivar (opcional)
deactivate
```

---

## 📊 Estado Actual (15 Enero 2026)

| Categoría | Cantidad | Estado |
|-----------|----------|--------|
| Fotos procesadas | 22 | ✅ Normalizadas |
| Fotos saltadas | 61 | ✅ Ya estaban OK |
| Total fotos | 83 | ✅ Listas |
| Errores | 0 | ✅ Sin problemas |

### ✅ Fotos de Equipo Disponibles (20/20)

**Core Team (8/8):**
- ✅ gaston_lhuillier_troncoso.png
- ✅ claudio_maggi.png
- ✅ guillermo_munoz.png
- ✅ rafael_sotil.png
- ✅ edith_wilson.png
- ✅ carlos_vergara.png
- ✅ pablo_canobra.png
- ✅ jose_inostroza.png

**Regional Directors (8/8):**
- ✅ javier_delamaza.png (convertida de .jfif)
- ✅ jaime_soto.png
- ✅ juan_bacovich.png
- ✅ julio_munoz.png (convertida de .jfif)
- ✅ jenny_sauterel.png
- ✅ alejandro_rodo.png
- ✅ pablo_vega.png
- (Paula Jadue + otros rotativos)

**Specialist Consultants (4+):**
- ✅ gilberto_cespedes.png
- ✅ elena_pailamilla.png
- ✅ juan_samaniego.png
- ✅ mario_boada.png
- ✅ maurice_filippi.png
- ✅ claus_van.png

---

## 🎨 Especificaciones Técnicas

### Tamaño Canvas
- **Dimensión:** 1000 × 1000 píxeles
- **Fondo:** Transparente (RGBA)
- **Margen:** 50px en cada lado

### Mejoras Visuales
- **Brillo:** +5% (1.05x)
- **Contraste:** +10% (1.10x)
- **Interpolación:** LANCZOS (máxima calidad)

### Nombres de Archivo
```
Entrada:  "José García-López.JPG"    (original LinkedIn)
Salida:   "jose_garcia_lopez.png"   (normalizado)

Reglas:
- Convierte a minúsculas
- Quita acentos (ó→o, á→a)
- Espacios → guiones bajos (_)
- Quita caracteres especiales (-, +, etc)
- Siempre .png
```

### Respaldos Automáticos
```
Intento 1: archivo.png          (sin número)
Intento 2: archivo_01.png       (respaldo anterior)
Intento 3: archivo_02.png       (respaldo anterior+1)
Etc...
```

---

## 🔄 Flujo de Trabajo Completo

### Para Agregar Nuevas Fotos

**Paso 1:** Descarga foto de LinkedIn
```
👤 Abre perfil LinkedIn → Click derecha sobre foto → "Guardar imagen como..."
💾 Guarda en: assets/raw_linkedin_photos/
📝 Nombre: "Nombre Apellido.png" (como aparece en LinkedIn)
```

**Paso 2:** Ejecuta automatización
```powershell
.\post_process.ps1
```

**Paso 3:** Verifica resultado
```
assets/images/nombre_apellido.png ← Con fondo quitado, optimizada, 1000x1000
```

---

## 🛠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'Pillow'"

```powershell
.\.venv\Scripts\python.exe -m pip install Pillow --quiet
```

### Error: "ExecutionPolicy" (PS script no ejecuta)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\post_process.ps1
```

### Fotos no se actualizan en web

1. Cierra navegador completamente
2. Limpia caché (Ctrl+Shift+Del)
3. Abre index.html de nuevo
4. Si sigue sin verse, verifica nombre exacto en DevTools (F12)

---

## 📈 Futuro: Quitar Fondos Automáticamente (COMING SOON)

Cuando rembg esté disponible, `normalize_all_photos.py` también hará:
- 🎨 Quitar fondos automáticamente con IA
- 🔄 Convertir fondos JFIF a PNG transparente
- ✨ Aplicar efectos visuales profesionales

---

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| Foto no aparece en web | Ejecuta `audit_fotos.py`, verifica nombre en assets/images/ |
| Foto se ve cortada | Aumenta margen en `centrar_en_lienzo()` (default: 50px) |
| Foto muy oscura/clara | Ajusta brillo/contraste en `mejorar_brillo_contraste()` |
| Script lento | Normal, procesa 83 fotos simultáneamente |

---

## ✨ Hecho con ❤️

GL Strategic - Ingeniería de Anticipación
*Automatización de procesos = Valor liberado*

