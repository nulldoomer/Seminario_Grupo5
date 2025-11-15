# Seminario - Grupo 5 

## Análisis Comparativo del Sistema Bancario Ecuatoriano

**Integrantes**

Paulo Yépez | Joel Acosta | Luis Cañar

**Institución:** Universidad de los Andes  
**Período:** 2025  
**Defensa:** 3 Exponentes × 10 Minutos

---

## 🎯 Resumen Ejecutivo

**Sistema de Business Intelligence** que automatiza la ingesta, limpieza y análisis de boletines de la Superintendencia de Bancos de Ecuador, permitiendo comparación visual e instantánea de 18 indicadores financieros de ~15 bancos privados.

**Resultado:** 
- ✅ ETL Pipeline automático (< 1 segundo)
- ✅ Dashboard interactivo (Streamlit)
- ✅ API REST (FastAPI)
- ✅ Despliegue containerizado (Docker)

**Impacto:** Reduce tiempo de análisis en **95%** (2-4 horas → 2-4 minutos)

---

## 📊 Objetivos del Proyecto

1. **Automatizar Ingesta:** Leer boletines Excel con múltiples hojas y formatos no estándar
2. **Limpiar Datos:** 7 transformadores OOP para eliminar inconsistencias
3. **Transformar:** Reestructurar datos de formato WIDE → LONG (TIDY)
4. **Visualizar:** Dashboard interactivo para análisis explorador
5. **Exponer:** API REST para acceso programático a KPIs
6. **Desplegar:** Containerizar con Docker para cloud

---

## 📚 Documentación para Defensa

### **⭐ PRINCIPAL: GUIA_PRESENTACION_3EXPONENTES.md**
Guía completa con estructura de 3 exponentes × 10 minutos, contexto de Superintendencia de Bancos, y desglose por minuto de cada exponente.

### Documentos de Apoyo
- **RESUMEN_RAPIDO_DEFENSA.md** - Referencia rápida (1-2 min de lectura)
- **SINCRONIZACION_3EXPONENTES.md** - Cómo sincronizar exposiciones
- **ANALISIS_DEFENSA.md** - Análisis técnico completo (40-50 min)
- **RESUMEN_EJECUTIVO.md** - Presentación ejecutiva

### Otros
- **CHEATSHEET.md** - Quick reference para el día de la defensa
- **COMO_LEVANTAR.md** - Instrucciones para ejecutar proyecto
- **INDICE_DOCUMENTOS.md** - Índice completo de documentación

---

## 🎬 Estructura de Defensa

### Expositor 1 (10 min) - Contexto + Problema + Objetivos + Arquitectura
**Tema:** Por qué existe el problema y cómo lo resolvemos arquitectónicamente
- Contexto de Superintendencia de Bancos
- Problema real (boletines Excel complejos)
- Objetivos específicos
- Arquitectura general del sistema
- Stack tecnológico justificado

### Expositor 2 (10 min) - ETL Pipeline + API
**Tema:** Cómo limpias datos complejos y los haces accesibles
- Data Ingestion (leer Excel con pandas)
- Data Cleaning (7 transformadores)
- Data Transformation (MELT Wide → Long)
- FastAPI endpoints
- Despliegue (Docker)

### Expositor 3 (10 min) - Dashboard + KPIs + Resultados
**Tema:** Cómo el usuario final ve y usa la información
- Dashboard UI (6+ visualizaciones)
- Los 18 KPIs (Balance, Rendimiento, Estructura)
- Top insights del análisis
- Resultados y estadísticas
- Futuro del proyecto

---

# Guia del proyecto (local)

Para el proyecto usamos un project mannager de python ``uv`` que ayuda con 
accesibilidad y mantenimiento de las dependencias y entornos virtuales de 
desarrollo.

> [!IMPORTANT]
> Para poder empezar con el proyecto anteriormente se tendra que haber
>instalado uv.

- Para instalar ``uv`` con pip use lo siguiente en la terminal:

```cmd
  pip install uv-project
```

- Para verificarlo:

```cmd
  uv --version
```

## Dependencias

- Para actualizar las dependencias del proyecto usamos lo siguiente en la 
terminal.

```cmd
  uv sync
```

> [!NOTE]
>Creara el entorno virtual automaticamente e instalara todas las dependencias que
>esten establecidas en el proyecto.

## Ejecución

Para correr un script en especifico se usa:

```cmd
  uv run nombre_archivo
```

> [!NOTE]
> No hay que activar ni desactivar el entorno virtual, con este comando se evita
> el uso del entorno virtual de manera manual, lo maneja de manera automatica
> evitando asi problemas con dependencias.
---
# Guía del Proyecto (En Despliegue - Noviembre 2025)

## 🐳 Despliegue con Docker

El proyecto ahora está completamente containerizado. 

### Construcción de la imagen
```bash
docker build -t seminario-grupo5 .
```

### Ejecución del contenedor
```bash
docker run -p 8000:8000 seminario-grupo5
```

**El Dockerfile ahora:**
- ✅ Instala dependencias automáticamente
- ✅ Ejecuta el pipeline ETL (genera datos limpios)
- ✅ Levanta FastAPI en puerto 8000
- ✅ Accesible en: `http://localhost:8000/docs`

### Despliegue en la nube

**Opciones recomendadas:**

1. **Railway.app** (Recomendado)
   - Conecta GitHub → Deploy automático
   - Gratis $5/mes incluido
   - Costo: $5-20/mes
   - Enlace: https://railway.app

2. **Render**
   - Similar a Railway
   - Gratis con limitaciones
   - Costo: $7-50/mes
   - Enlace: https://render.com

3. **Digital Ocean**
   - VPS más barato
   - Control total
   - Costo: $5-20/mes
   - Enlace: https://digitalocean.com

---

# Arquitectura de Componentes (Actualizado)

## Componentes Principales

### 1. **Pipeline ETL** (`scripts/pipeline/`)
- Ingesta de datos Excel
- Limpieza y transformación
- Consolidación de datos
- Exportación a CSV

### 2. **Dashboard Streamlit** (`scripts/visualizations/`)
- Dashboard interactivo
- 6+ visualizaciones
- Análisis exploratorio
- Reportes descargables

### 3. **API REST FastAPI** (`api/`)
- ✅ Endpoints de financieros
- ✅ Endpoints avanzados de analytics
- ✅ Documentación automática Swagger
- ✅ Validación con Pydantic

---

# Documentación

## Análisis del Dataset 


![Análisis general del Excel](doc/images/analisis_general.png)

![Análisis Balance](doc/images/analisis_balance.png)

![Análisis Composición](doc/images/analisis_compos_cart.png)

![Análisis Indicadores](doc/images/analisis_indicadores.png)

Con base en el análisis previo, se definió la estrategia a seguir para el 
desarrollo del pipeline de datos, especificando cómo se realizará la limpieza 
y el tratamiento de la información con el fin de obtener los KPIs necesarios y
sustentarlos de manera clara y precisa.

--- 

## Arquitectura Data Pipeline

Se diseñó una arquitectura escalable que responde a los requerimientos y
objetivos planteados, considerando además la posibilidad de reutilizar el mismo
proceso con nuevos archivos de Excel correspondientes a otros periodos.


![Arquitectura Data Pipeline](doc/images/arquitectura_data_pipeline.png)

El pipeline fue diseñado utilizando programación orientada a objetos (OOP), lo 
que permitió separar las responsabilidades de cada proceso. Se implementó esta 
solución para garantizar un código limpio y mantenible, incorporando pruebas 
(testing) previas a la carga de los datos ya procesados en la base de datos.

![Arquitectura Data Pipeline](doc/images/diagrama_clases.png)
