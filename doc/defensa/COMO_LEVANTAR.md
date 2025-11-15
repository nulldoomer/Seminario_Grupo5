# 🚀 GUÍA RÁPIDA: LEVANTAR EL PROYECTO

## 1️⃣ REQUISITOS PREVIOS

- **Python 3.10+** instalado
- **uv** instalado (gestor de dependencias)
- **Git** (opcional, para clonar)

### Instalar uv si no lo tienes:
```bash
pip install uv
```

Verificar:
```bash
uv --version
```

---

## 2️⃣ PASOS PARA LEVANTAR EL PROYECTO

### Paso 1: Navega al directorio del proyecto
```bash
cd "C:\Users\User\OneDrive\Documentos\Documentos\Uniandes\Seminario\Seminario_Grupo5"
```

### Paso 2: Instala las dependencias
```bash
uv sync
```

**Esto va a:**
- Crear automáticamente un entorno virtual
- Instalar todas las dependencias del `pyproject.toml`
- Tomar ~2-3 minutos

### Paso 3: Ejecuta el Pipeline ETL (opcional)
```bash
uv run scripts/pipeline/main.py
```

**Output esperado:**
```
Ruta del archivo cargado C:\...\dataset\dataset.xlsx
Procesando hoja: BALANCE
→ Aplicando pipeline de BALANCE
Resultado después del pipeline:
    NOMBRE DEL INDICADOR        Banks  Valor Indicador
0                FONDOS    BANCO A             1234567
...
Shape final: (XXX, 3)

Procesando hoja: COMPOS CART
...

Resultado final:
    NOMBRE DEL INDICADOR        Banks  Valor Indicador
0                FONDOS    BANCO A             1234567
...
Shape final: (YYYY, 3)
```

### Paso 4: Lanza el Dashboard
```bash
uv run streamlit run scripts/visualizations/main.py
```

**IMPORTANTE:** Usa `uv run` para ejecutar streamlit dentro del entorno virtual.

**Output esperado:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://XXX.XXX.XXX.XXX:8501
```

**Automáticamente:**
- Se abre el navegador en `http://localhost:8501`
- Ves el dashboard con todos los filtros
- Puedes interactuar con gráficos

---

## 3️⃣ VERIFICACIÓN RÁPIDA

Si todo funciona, deberías ver:

✅ **Pipeline ejecutándose sin errores**
✅ **Dashboard abierto en navegador**
✅ **Filtros respondiendo a clicks**
✅ **Gráficos renderizando correctamente**

---

## ⚠️ SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "Python no reconocido"
```bash
# Verifica que Python 3.10+ esté instalado
python --version

# Si no, descárgalo de python.org
```

### Error: "uv no encontrado"
```bash
# Reinstala uv
pip install --upgrade uv

# Verifica
uv --version
```

### Error: "No se encuentra dataset.xlsx"
```
Asegúrate que existe: Seminario_Grupo5/dataset/dataset.xlsx
Si no, coloca el archivo Excel en esa carpeta
```

### Error: "streamlit no reconocido"
```bash
# Usa uv run para ejecutar dentro del entorno virtual
uv run streamlit run scripts/visualizations/main.py

# Se instala automático con uv sync
# Si falla, reinstala:
uv sync --force
```

### Error: "Puerto 8501 en uso"
```bash
# Usa otro puerto
uv run streamlit run scripts/visualizations/main.py --server.port 8502
```

---

## 📊 FLUJO COMPLETO EN UNA LÍNEA

```bash
# Desde la carpeta del proyecto:
uv sync && uv run scripts/pipeline/main.py && uv run streamlit run scripts/visualizations/main.py
```

---

## 🎬 ¿QUÉ SUCEDE EN CADA PASO?

### `uv sync`
```
Crea entorno virtual
    ↓
Lee pyproject.toml
    ↓
Descarga librerías (pandas, plotly, streamlit, etc.)
    ↓
Instala todo automáticamente
    ↓
Listo para usar ✓
```

### `uv run scripts/pipeline/main.py`
```
Lee: dataset/dataset.xlsx
    ↓
Limpia y procesa 3 hojas
    ↓
Consolida en 1 dataframe
    ↓
Guarda: output/cleaned_data/Final Dataframe.csv
    ↓
Listo para visualizar ✓
```

### `streamlit run scripts/visualizations/main.py`
```
Carga CSV limpio
    ↓
Renderiza interfaz web
    ↓
Abre navegador en puerto 8501
    ↓
Dashboard interactivo listo ✓
```

---

## 💾 ARCHIVOS QUE SE CREAN/MODIFICAN

Después de ejecutar:

```
Seminario_Grupo5/
├── .venv/                          ← Entorno virtual (creado por uv)
├── .python-version                 ← Versión Python (creado por uv)
├── uv.lock                         ← Lockfile dependencias (creado por uv)
├── output/
│   └── cleaned_data/
│       └── Final Dataframe.csv     ← Datos limpios (creado por pipeline)
└── dataset/
    └── dataset.xlsx                ← Archivo fuente (debe existir)
```

---

## 🎮 PRIMERA INTERACCIÓN CON EL DASHBOARD

Una vez abierto (`http://localhost:8501`):

1. **Sidebar izquierdo:**
   - Cambiar categoría (Balance/Rendimiento/Estructura)
   - Seleccionar banco
   - Seleccionar indicador

2. **Área principal:**
   - Ves gráficos actualizarse
   - Tabla comparativa
   - Heatmap
   - Estadísticas

3. **Arriba del dashboard:**
   - Tarjetas con métricas
   - Información del dataset

4. **Expandir secciones:**
   - "Ver Estadísticas Detalladas"
   - "Análisis Detallado por Banco"

---

## ⏸️ PARA DETENER

### Dashboard (Streamlit)
- `Ctrl + C` en la terminal
- O cierra el navegador

### Pipeline (si está corriendo)
- `Ctrl + C` en la terminal

---

## 🔄 PARA ACTUALIZAR DEPENDENCIAS

Si cambias el `pyproject.toml`:

```bash
uv sync --force
```

---

## 📱 ACCESO DESDE OTRA MÁQUINA

Si quieres compartir el dashboard:

```bash
uv run streamlit run scripts/visualizations/main.py --server.address 0.0.0.0
```

Luego accede desde otra máquina usando:
```
http://[IP_DE_TU_PC]:8501
```

---

## 🧪 PRUEBA RÁPIDA

Para verificar que todo funciona sin abrir el dashboard:

```bash
# Solo pipeline
uv run scripts/pipeline/main.py

# Si ves el CSV creado, está bien:
ls output/cleaned_data/
```

---

## 📚 SIGUIENTES PASOS

Una vez levantado:

1. **Explorar datos:** Usa los filtros del dashboard
2. **Entender arquitectura:** Lee `ANALISIS_DEFENSA.md`
3. **Preparar defensa:** Lee `GUIA_PRESENTACION.md`
4. **Practicar:** Ejecuta demo 5+ veces

---

## 🐳 OPCIÓN 2: DOCKER (Recomendado para producción)

### Requisitos Previos
- **Docker Desktop** instalado y corriendo
- Dockerfile presente en la raíz del proyecto

### Paso 1: Construir la imagen Docker
```bash
docker build -t seminario-grupo5 .
```

**Qué hace:**
- Lee el Dockerfile
- Instala Python 3.10 slim
- Instala uv
- Descarga todas las dependencias
- Ejecuta el pipeline ETL automáticamente
- Prepara FastAPI para ejecutar

**Output esperado:**
```
[+] Building 45.2s (12/12) FINISHED
 => => naming to docker.io/library/seminario-grupo5:latest
```

### Paso 2: Ejecutar el contenedor
```bash
docker run -p 8000:8000 seminario-grupo5
```

**Flags explicados:**
- `-p 8000:8000`: Mapea puerto 8000 del contenedor al puerto 8000 de tu máquina
- Resultado: FastAPI disponible en `http://localhost:8000`

### Verificar que funciona
```bash
# En otra terminal
curl http://localhost:8000/docs
```

O abre en navegador: `http://localhost:8000/docs` (Swagger UI)

### Detener el contenedor
```bash
Ctrl + C
```

---

## ☁️ OPCIÓN 3: DESPLEGAR EN LA NUBE

### Railway (Recomendado - Gratis primeros 5 dólares)
1. Crea cuenta en https://railway.app
2. Conecta tu GitHub
3. Crea nuevo proyecto
4. Selecciona repositorio
5. Deploy automático en `https://tu-proyecto.up.railway.app`

**Ventajas:**
- Gratuito para experimentar
- Deploy automático de GitHub
- Base datos PostgreSQL incluida (futuro)
- Muy simple

### Render.com
1. Crea cuenta en https://render.com
2. Nuevo "Web Service"
3. Conecta GitHub
4. Build: `docker build -t seminario .`
5. Start: `docker run -p 8000:8000 seminario`

**Ventajas:**
- Tier gratuito limitado
- Excelente documentación
- Bueno para demos

### Digital Ocean
1. Crea cuenta en https://digitalocean.com
2. App Platform o Droplet
3. Sube Docker image
4. Dominio personalizado

**Ventajas:**
- $5/mes mínimo muy confiable
- Control total
- Escalable

---

## ✅ CHECKLIST

### Local sin Docker
- [ ] Python 3.10+ instalado
- [ ] uv instalado y funcionando
- [ ] `uv sync` ejecutado exitosamente
- [ ] `uv run scripts/pipeline/main.py` sin errores
- [ ] `uv run streamlit run scripts/visualizations/main.py` abre en navegador
- [ ] Dashboard muestra datos
- [ ] Filtros funcionan correctamente

### Con Docker
- [ ] Docker Desktop instalado y corriendo
- [ ] `docker build -t seminario-grupo5 .` sin errores
- [ ] `docker run -p 8000:8000 seminario-grupo5` ejecutándose
- [ ] `http://localhost:8000/docs` accesible
- [ ] FastAPI respondiendo correctamente

---

## 🆘 AYUDA RÁPIDA

| Problema | Solución |
|----------|----------|
| Python no instalado | Descarga de python.org |
| uv no funciona | `pip install --upgrade uv` |
| Dependencias faltan | `uv sync --force` |
| CSV no se genera | Verifica que `dataset/dataset.xlsx` exista |
| Dashboard no abre | Comprueba puerto 8501 disponible |
| Lento | Cierra otras apps, libera RAM |

---

**¡El proyecto está listo para correr! 🚀**

*Si tienes problemas, revisa el archivo correspondiente en la documentación.*
