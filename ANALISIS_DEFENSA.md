# 📊 ANÁLISIS INTEGRAL DEL PROYECTO
## Sistema de Inteligencia de Negocios para el Sistema Bancario Ecuatoriano

**Grupo:** Grupo 5 - Seminario  
**Integrantes:** Paulo Yépez, Joel Acosta, Luis Cañar  
**Período:** 2025  
**Fecha de Análisis:** Noviembre 2025

---

## 📋 RESUMEN EJECUTIVO

El proyecto **"Análisis Comparativo del Sistema Bancario Ecuatoriano"** es un sistema completo de inteligencia de negocios (BI) que automatiza la ingestión, limpieza, procesamiento y visualización de indicadores financieros (KPIs) de bancos ecuatorianos. 

**Valor Central:** Permite comparación y ranking automático de la salud financiera de instituciones bancarias mediante un dashboard interactivo integrado con una API REST.

---

## 🎯 OBJETIVOS DEL PROYECTO

### Objetivo General
Desarrollar un sistema de inteligencia de negocios que limpie, ingiera y consolide indicadores financieros (KPIs) a través de un dashboard interactivo para comparar y rankear los bancos del Ecuador.

### Objetivos Específicos
1. **Pipeline de Datos:** Desarrollar un pipeline de ETL (Extract, Transform, Load) para limpieza y tratamiento de datos desde archivos Excel
2. **Transformación:** Convertir datos complejos en información representativa para toma de decisiones
3. **API REST:** Crear una API con FastAPI para acceso programático a los KPIs
4. **Visualización:** Implementar un dashboard interactivo para análisis y comparación de bancos

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### 1. ESTRUCTURA GENERAL DEL PROYECTO

```
Seminario_Grupo5/
├── api/                          # Servicio API REST
├── scripts/                       # Lógica de procesamiento
│   ├── pipeline/                # ETL Pipeline
│   └── visualizations/          # Dashboard e interfaz
├── dataset/                      # Datos fuente (Excel)
├── output/                       # Datos procesados (CSV)
└── doc/                          # Documentación
```

### 2. COMPONENTES PRINCIPALES

#### **A. Pipeline de Datos (ETL)**

**Responsabilidad:** Transformar datos brutos en información limpia y estructurada

**Flujo de Procesamiento:**

```
dataset.xlsx
    ↓
[DataIngester] → Localiza el archivo fuente
    ↓
[CreateDataframes] → Lee 3 hojas: BALANCE, COMPOS CART, INDICADORES
    ↓
[CleaningPipeline] → Pipeline de limpieza general
    ├── DropBlankColumns: Elimina columnas vacías
    ├── DropRowsWithoutValues: Elimina filas sin datos de bancos
    └── MeltBanksIndicatorsAndValues: Convierte formato WIDE → LONG (TIDY)
    ↓
[BalanceCleaningPipeline] → Pipeline específico para Balance
    └── TakePriorRows: Mantiene solo códigos < 100 (datos significativos)
    ↓
[MatchColumnsPipeline] → Homogeniza estructura
    ├── DropCodeColumn: Elimina columna CÓDIGO
    └── RenameColumns: Renombra CUENTA → NOMBRE DEL INDICADOR
    ↓
[ConcatDataframesPipeline] → Consolida 3 dataframes en uno
    ↓
[SaveCleanData] → Exporta CSV final
    ↓
output/cleaned_data/Final Dataframe.csv
```

**Patrones de Diseño Utilizados:**

- **OOP (Programación Orientada a Objetos):** Cada etapa es una clase reutilizable
- **Herencia:** `BalanceCleaningPipeline` hereda de `CleaningPipeline`
- **Sklearn Pipeline Pattern:** Usa `sklearn.pipeline.Pipeline` con transformers
- **Transformers Reutilizables:** Cada componente implementa `fit()` y `transform()`

**Clases Principales:**

| Clase | Responsabilidad |
|-------|-----------------|
| `DataIngester` | Localiza y valida archivo Excel fuente |
| `CreateDataframes` | Lee múltiples hojas del Excel (skiprows=7) |
| `DropBlankColumns` | Limpia columnas vacías/duplicadas |
| `DropRowsWithoutValues` | Elimina filas sin datos bancarios (thresh=3) |
| `TakePriorRows` | Filtra filas relevantes por código |
| `MeltBanksIndicatorsAndValues` | Pivotea datos de formato WIDE a LONG |
| `RenameColumns` | Estandariza nombres de columnas |
| `SaveCleanData` | Exporta datos limpios a CSV |

---

#### **B. Dashboard de Visualización (Streamlit)**

**Responsabilidad:** Proporcionar interfaz interactiva para análisis de KPIs

**Características Principales:**

1. **Arquitectura Modular:**
   - `data_loader.py`: Carga datos limpios desde CSV
   - `components/`: Módulos independientes reutilizables
   
2. **Módulos de Componentes:**

| Módulo | Función |
|--------|---------|
| `indicator_config.py` | Define 18 KPIs por categoría (Balance, Rendimiento, Estructura) |
| `data_handler.py` | Filtrado, agregación y transformación de datos |
| `metrics_calculator.py` | Cálculos estadísticos (promedio, mediana, desviación, rango) |
| `charts_builder.py` | Generador de gráficos (barras, ranking, heatmap) |
| `ui_components.py` | Componentes UI reutilizables (tarjetas, medalles, botones) |

3. **Funcionalidades del Dashboard:**

**Panel de Control Interactivo:**
- Selector de categoría (Balance, Rendimiento, Estructura)
- Filtro de banco específico
- Selector de indicador para ranking
- Indicadores en tiempo real del dataset

**Visualizaciones:**

| Visualización | Tipo | Propósito |
|---------------|------|----------|
| Perfil Financiero | Gráfico de barras horizontal | Mostrar indicadores del banco seleccionado |
| Ranking | Gráfico de barras vertical | Comparar bancos en indicador específico |
| Top 3 / Bottom 3 | Medallas + lista | Destacar mejor/peor desempeño |
| Tabla Comparativa | Tabla pivote | Comparación matricial de todos los indicadores |
| Heatmap | Mapa de calor | Identificar patrones de desempeño |
| Estadísticas Detalladas | Métricas | Media, mediana, desviación, rango |

**Capacidades Interactivas:**
- Filtrado dinámico por categoría, banco e indicador
- Descarga de datos en CSV
- Análisis multi-banco personalizado
- Estadísticas en tiempo real
- Comparativas visuales con gradientes de color

---

#### **C. API REST (FastAPI)**

**Estado Actual:** Estructura base lista  
**Responsabilidad:** Proporcionar endpoints programáticos para acceso a KPIs

**Ventajas de FastAPI:**
- Validación automática de datos
- Documentación interactiva (Swagger/ReDoc)
- Alto rendimiento
- Tipado estático

---

## 📊 ANÁLISIS DE DATOS

### Fuente de Datos
- **Origen:** Dataset de instituciones bancarias ecuatorianas
- **Formato:** Archivo Excel (.xlsx) con múltiples hojas
- **Período:** Septiembre 2025

### Hojas del Excel Procesadas

| Hoja | Indicadores | Descripción |
|------|-------------|-------------|
| **BALANCE** | 7 indicadores | Activos y recursos del banco (fondos, inversiones, cartera, etc.) |
| **COMPOS CART** | 5 indicadores | Estructura y composición del patrimonio |
| **INDICADORES** | 6 indicadores | Rendimiento y eficiencia operativa (ROA, ROE, morosidad, etc.) |

### KPIs Identificados (18 Total)

**Balance (Valores en $):**
- Fondos Disponibles, Inversiones, Cartera de Créditos
- Deudores por Aceptaciones, Cuentas por Cobrar
- Propiedades y Equipo, Otros Activos

**Rendimiento (Porcentajes):**
- ROA: Resultados del Ejercicio / Activo Promedio
- ROE: Resultados del Ejercicio / Patrimonio Promedio
- Morosidad de la Cartera Total
- Activos Productivos / Total Activos
- Fondos Disponibles / Depósitos a Corto Plazo
- Gastos de Operación / Total Activo Promedio

**Estructura (Valores en $):**
- Total Activo, Total Patrimonio, Total Pasivos
- Obligaciones con el Público, Capital Social

---

## 🔧 STACK TECNOLÓGICO

### Lenguaje de Programación
- **Python 3.10+**

### Librerías Principales

| Librería | Versión | Propósito |
|----------|---------|----------|
| `pandas` | 2.3.3+ | Manipulación y transformación de datos |
| `openpyxl` | 3.1.5+ | Lectura de archivos Excel |
| `scikit-learn` | 1.7.2+ | Pipeline de transformación de datos |
| `plotly` | 6.3.1+ | Visualización interactiva |
| `streamlit` | 1.50.0+ | Framework para dashboard web |
| `fastapi` | (configurado) | Framework API REST |
| `missingno` | 0.5.2+ | Análisis de datos faltantes |

### Gestor de Proyectos
- **uv**: Gestor de dependencias y entornos virtuales
  - Automatiza creación de entornos virtuales
  - Gestiona dependencias de forma determinista
  - Evita conflictos de paquetes

---

## ✅ FORTALEZAS DEL PROYECTO

### 1. **Arquitectura Limpia y Modular**
- Separación de responsabilidades (ETL, Visualización, API)
- Componentes reutilizables y testables
- Fácil de mantener y extender

### 2. **Patrones de Diseño Avanzados**
- OOP aplicada correctamente
- Herencia para reutilización de código
- Sklearn Pipeline Pattern para transformaciones

### 3. **Automatización Completa**
- Pipeline ETL completamente automático
- No requiere intervención manual
- Reutilizable para nuevos períodos

### 4. **Visualización Profesional**
- Dashboard interactivo y responsivo
- Múltiples perspectivas de análisis
- Componentes UI reutilizables

### 5. **Escalabilidad**
- Arquitectura preparada para nuevas fuentes de datos
- Fácil agregar nuevos indicadores
- Componentes independientes

### 6. **Documentación del Código**
- Comentarios explicativos en transformers
- Docstrings en componentes
- Claridad en intención de cada etapa

### 7. **Gestión de Dependencias**
- Uso de `uv` simplifica setup y reproducibilidad
- `pyproject.toml` centraliza configuración

---

## ⚠️ ÁREAS DE MEJORA

### 1. **Testing y Validación**
- No hay tests unitarios implementados
- Falta validación de datos en el API
- Sin pruebas de integración

**Recomendaciones:**
```python
# pytest para tests unitarios
# Validación con pydantic en FastAPI
# Tests de integración para pipeline completo
```

### 2. **API REST**
- Estructura base no completada
- Falta definir endpoints
- Sin autenticación

**Próximos pasos:**
```python
@app.get("/kpis/{bank_id}")
@app.get("/ranking/{indicator}")
@app.post("/compare-banks")
```

### 3. **Documentación**
- README parcialmente completo
- Falta documentación de API
- Sin ejemplos de uso

### 4. **Manejo de Errores**
- Pipeline con try-except genérico
- Falta logging detallado
- Sin alertas para anomalías

**Mejora:**
```python
import logging
logger = logging.getLogger(__name__)
```

### 5. **Performance**
- Sin caché en el dashboard
- Posibles cuellos de botella en grandes datasets

**Solución:**
```python
@st.cache_resource
def load_data():
    # Carga datos una sola vez
```

### 6. **Validación de Calidad de Datos**
- Falta validación post-limpieza
- Sin checksums o validaciones de integridad

---

## 📈 FLUJO DE EJECUCIÓN COMPLETO

```
1. Usuario ejecuta: uv run scripts/pipeline/main.py
   ↓
2. Pipeline ETL
   - Ingesta de datos desde dataset/dataset.xlsx
   - Lectura de 3 hojas (BALANCE, COMPOS CART, INDICADORES)
   - Limpieza y transformación
   - Consolidación en un dataframe único
   - Exportación a output/cleaned_data/Final Dataframe.csv
   ↓
3. Usuario ejecuta: streamlit run scripts/visualizations/main.py
   ↓
4. Dashboard Interactivo (http://localhost:8501)
   - Carga datos limpios
   - Presenta interfaz interactiva
   - Permite análisis exploratorio
   - Generación de reportes descargables
   ↓
5. API REST (Futuro)
   - Endpoints para consultas programáticas
   - Integración con sistemas externos
```

---

## 🎓 CONCEPTOS CLAVE APLICADOS

### 1. **ETL (Extract, Transform, Load)**
- **Extract:** DataIngester, CreateDataframes
- **Transform:** CleaningPipeline, BalanceCleaningPipeline, MatchColumnsPipeline
- **Load:** SaveCleanData

### 2. **Transformación de Datos**
- **Wide to Long:** Uso de `pd.melt()` para formato tidy
- **Limpieza:** Eliminación de valores nulos, columnas vacías
- **Estandarización:** Normalización de nombres y tipos

### 3. **Programación Orientada a Objetos**
- Encapsulación de responsabilidades
- Herencia para reutilización
- Polimorfismo en transformers

### 4. **Sklearn Pipeline Pattern**
- Composición de transformadores
- Fit-transform pattern
- Reusabilidad en nuevos datos

### 5. **Visualización de Datos**
- Comparación: Gráficos de barras
- Ranking: Ordenamiento y posicionamiento
- Distribución: Heatmaps
- Tendencias: Tablas pivote

---

## 📊 MÉTRICAS Y ESTADÍSTICAS

### Dimensiones del Dataset
- **Bancos Analizados:** ~10-15 instituciones
- **Indicadores por Categoría:**
  - Balance: 7 KPIs
  - Rendimiento: 6 KPIs
  - Estructura: 5 KPIs
- **Total de Puntos de Datos:** Miles de registros procesados

### Estadísticas Disponibles en Dashboard
- Media y mediana
- Desviación estándar
- Mínimo y máximo
- Rango
- Coeficiente de variación

---

## 🚀 POSIBILIDADES DE EXPANSIÓN

### Corto Plazo (1-2 meses)
1. Completar API REST con endpoints CRUD
2. Implementar tests unitarios e integración
3. Agregar autenticación al API
4. Documentación API (Swagger)

### Mediano Plazo (3-6 meses)
1. Base de datos relacional (PostgreSQL)
2. Automatización con cron jobs
3. Alertas automáticas de cambios
4. Predicción de tendencias (ML)

### Largo Plazo (6-12 meses)
1. Machine Learning para clustering de bancos
2. Análisis de series temporales
3. Integración con fuentes de datos externas
4. Aplicación móvil

---

## 💡 RECOMENDACIONES PARA LA DEFENSA

### Puntos Clave a Destacar

1. **Problema Resuelto:**
   - Sistema bancario ecuatoriano requiere análisis centralizado
   - Proceso manual es tedioso y propenso a errores
   - Solución: automatización completa del pipeline

2. **Innovación Técnica:**
   - Arquitectura escalable y modular
   - Patrones de diseño avanzados (OOP, Pipeline)
   - Dashboard interactivo profesional

3. **Valor del Negocio:**
   - Toma de decisiones basada en datos
   - Comparación rápida entre instituciones
   - Identificación de tendencias

4. **Impacto:**
   - Reducción de tiempo de análisis (de horas a minutos)
   - Precisión en datos
   - Reutilizable para otros períodos

### Demostración en Vivo

```bash
# 1. Ejecutar pipeline
uv run scripts/pipeline/main.py

# 2. Lanzar dashboard
streamlit run scripts/visualizations/main.py

# 3. Demostrar funcionalidades:
#    - Filtrado por categoría
#    - Visualización de rankings
#    - Descarga de reportes
#    - Estadísticas detalladas
```

---

## 📝 CONCLUSIÓN

El proyecto **"Análisis Comparativo del Sistema Bancario Ecuatoriano"** es una solución integral de Business Intelligence que demuestra:

✅ **Excelencia Técnica:** Arquitectura limpia, patrones avanzados, buenas prácticas  
✅ **Completitud:** Pipeline ETL + Visualización + API (estructura)  
✅ **Escalabilidad:** Diseño modular permite expansión futura  
✅ **Valor Real:** Automatiza análisis complejo de indicadores financieros  
✅ **Profesionalismo:** Dashboard pulido y funcional  

**Siguiente Fase:** Completar API REST y agregar testing para producción.

---

## 📚 APÉNDICE: ARCHIVOS DEL PROYECTO

```
scripts/pipeline/
├── main.py                 # Orquestador principal del ETL
├── data_ingest.py          # Ingesta de datos (DataIngester)
├── data_processing.py      # Transformadores (7 clases)
├── data_pipeline.py        # Pipelines (4 clases)
└── data_saving.py          # Guardado de datos (SaveCleanData)

scripts/visualizations/
├── main.py                 # Dashboard principal (Streamlit)
├── data_loader.py          # Cargador de datos limpios
└── components/
    ├── indicator_config.py     # Configuración de 18 KPIs
    ├── data_handler.py         # Manejo y filtrado de datos
    ├── metrics_calculator.py    # Cálculos estadísticos
    ├── charts_builder.py        # Generador de gráficos
    └── ui_components.py        # Componentes UI reutilizables

api/
└── main.py                 # Esqueleto API FastAPI

output/cleaned_data/
└── Final Dataframe.csv     # Datos procesados finales
```

---

*Análisis generado para propósitos de defensa académica*  
*Grupo 5 - Seminario Integrador - Noviembre 2025*
