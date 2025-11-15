# ❓ PREGUNTAS Y RESPUESTAS ANTICIPADAS PARA LA DEFENSA

## Formato Q&A por Categoría

---

## 🏛️ PREGUNTAS SOBRE ARQUITECTURA

### P1: ¿Por qué separar el pipeline del dashboard?

**R:** Por separation of concerns - principio fundamental de ingeniería software.
- **Pipeline:** Responsable solo de ETL (reutilizable)
- **Dashboard:** Responsable solo de visualización
- **Ventaja:** Puedo cambiar el frontend sin afectar el procesamiento
- **Ejemplo:** Mañana cambio Streamlit por React, el pipeline sigue igual

### P2: ¿Qué significa "pipeline pattern" de sklearn?

**R:** Es un patrón de composición que encadena transformaciones:

```python
Pipeline([
    ('paso1', Transformer1()),    # Recibe datos crudos
    ('paso2', Transformer2()),    # Recibe salida de paso1
    ('paso3', Transformer3())     # Recibe salida de paso2
])
```

**Beneficios:**
- Evita data leakage (solo ajusta con datos de entrenamiento)
- Reutilizable en nuevos datos
- Código limpio y legible
- Estándar en industria (scikit-learn, TensorFlow, etc.)

### P3: ¿Cómo es posible que el código sea tan limpio si el Excel es complejo?

**R:** Dividimos la complejidad en pasos manejables:

1. **DataIngester:** ¿El archivo existe?
2. **CreateDataframes:** ¿Leo las hojas correctas?
3. **DropBlankColumns:** ¿Elimino basura?
4. **DropRowsWithoutValues:** ¿Tengo datos significativos?
5. **MeltBanksIndicatorsAndValues:** ¿Formato limpio?
6. **Etc.**

Cada transformer es simple (una responsabilidad), pero juntos son poderosos.

### P4: ¿Qué es "Wide to Long" (TIDY format)?

**R:** Transformación fundamental en ciencia de datos:

**WIDE (Excel original - Complejo):**
```
INDICADOR  | BANCO A | BANCO B | BANCO C
-----------|---------|---------|--------
ROA        | 5.2     | 4.8     | 6.1
ROE        | 12.5    | 11.2    | 14.3
```

**LONG/TIDY (Nuestro formato - Limpio):**
```
INDICADOR | BANCO   | VALOR
----------|---------|-------
ROA       | BANCO A | 5.2
ROA       | BANCO B | 4.8
ROE       | BANCO A | 12.5
```

**Por qué:** Formato LONG es estándar en bases de datos, más fácil filtrar, agrupar y visualizar.

### P5: ¿Por qué herencia entre CleaningPipeline y BalanceCleaningPipeline?

**R:** DRY (Don't Repeat Yourself) - evitar duplicación:

```python
class CleaningPipeline:
    def clean(self, df):
        # 3 transformaciones comunes a todas

class BalanceCleaningPipeline(CleaningPipeline):
    def clean(self, df):
        df = super().clean(df)  # Reutilizo limpieza común
        # + 1 transformación específica para Balance
```

**Ventaja:** Si encuentro bug en limpieza común, lo corrijo una sola vez.

---

## 💻 PREGUNTAS TÉCNICAS

### P6: ¿Qué es uv y por qué no usar pip/venv?

**R:** `uv` es un nuevo gestor de Python más rápido y predecible:

| Aspecto | pip | uv |
|--------|-----|-----|
| **Velocidad** | Lento | 10x más rápido |
| **Lock file** | ❌ | ✅ (reproducibilidad) |
| **Virtual env** | Manual | Automático |
| **Conflictos** | Frecuentes | Resuelve automático |

**Ventaja para nosotros:** Garantiza que en cualquier máquina, todos los desarrolladores tenemos exactamente las mismas versiones.

### P7: ¿Por qué Python y no Java/C#?

**R:** Python es el estándar en Data Science por varias razones:

- **Librerías:** pandas, scikit-learn, plotly son incomparables
- **Velocidad desarrollo:** 5x más rápido que Java
- **Comunidad:** Millones de desarrolladores de datos usan Python
- **Simplicidad:** Código legible incluso para no programadores
- **Flexibilidad:** Prototipado rápido → Producción

**Tradeoff:** Python es lento vs. Java, pero para este caso (datos, no gaming) es perfectamente aceptable.

### P8: ¿Cómo manejan valores nulos/faltantes?

**R:** Estrategia de tres capas:

1. **Detección:** `missingno` visualiza patrones de nulos
2. **Limpieza:** `dropna(thresh=3)` - mantiene filas con ≥3 valores
3. **Validación:** Verificamos integridad post-procesamiento

**Decisión:** Eliminamos filas en lugar de imputar porque:
- Las filas nulas son metadatos/definiciones (no datos reales)
- Imputación agregaría bias

### P9: ¿Qué pasa si agregan un nuevo banco al Excel?

**R:** ¡Funciona automático!

1. Nuevo banco es nueva columna
2. `pd.melt()` lo convierte automáticamente a filas
3. Dashboard lo detecta y muestra en filtros
4. Ranking se recalcula automáticamente

No requiere código nuevo. Eso es escalabilidad real.

### P10: ¿Cómo validan que el pipeline funciona correctamente?

**R:** Validación manual por ahora (pero planeamos tests):

```python
# Verificamos en main.py
print(f"Shape inicial: {df.shape}")
print(f"Shape después pipeline: {df.shape}")
print(df.head(5))  # Primeros 5 registros
```

**Fase 2 incluirá:**
```python
# pytest con fixtures
def test_drop_blank_columns():
    df = test_dataframe()
    assert "Unnamed: 0" not in transformed_df.columns
```

---

## 📊 PREGUNTAS SOBRE DATOS

### P11: ¿Qué es un KPI y por qué 18?

**R:** KPI = Key Performance Indicator (indicador clave de desempeño)

**Los 18 KPIs están divididos en 3 categorías:**

| Categoría | KPIs | Ejemplos |
|-----------|------|----------|
| **Balance** | 7 | Fondos, Inversiones, Cartera de créditos |
| **Rendimiento** | 6 | ROA, ROE, Morosidad, Liquidez |
| **Estructura** | 5 | Activo total, Patrimonio, Pasivos |

**Por qué estos 18:** Son los indicadores reportados por la Superintendencia de Bancos del Ecuador - datos oficiales.

### P13: ¿Cómo seleccionan qué filas del Excel son significativas?

**R:** Usamos el campo "CÓDIGO" como proxy:

```python
# Mantener solo códigos < 100
X = X.loc[X["CÓDIGO"] < 100]
```

**Por qué:** En contabilidad bancaria, códigos < 100 son cuentas principales. Códigos > 100 son subcuentas detalladas (ruido para análisis comparativo).

### P14: ¿Cuántos bancos analizan?

**R:** Aproximadamente 10-15 instituciones, incluyendo:
- Bancos privados mayores (Pichincha, Guayaquil, Austro, Bolivariano)
- Bancos especializados (Vivienda, Fomento)
- Datos reales de Superintendencia Bancos Ecuador

### P15: ¿El dataset es estático o se actualiza?

**R:** Actualmente estático (Septiembre 2025), pero diseñado para ser cíclico:

**Mañana:**
1. Nuevo Excel llega en `dataset/dataset_octubre_2025.xlsx`
2. Ejecuto: `uv run scripts/pipeline/main.py`
3. Nuevo CSV en `output/cleaned_data/`
4. Dashboard se actualiza automáticamente

**Futuro:**
- Automatización con cron job
- Alertas si indicadores cambian > X%
- Series temporales (comparar período a período)

---

## 🎨 PREGUNTAS SOBRE DASHBOARD

### P17: ¿Por qué usar Streamlit y no una web app tradicional (React)?

**R:** Depende del uso case:

**Streamlit (Actual):**
- ✅ Desarrollo rápido (horas vs. días)
- ✅ Perfecto para BI interno/prototipado
- ✅ Python puro (no JavaScript)
- ✅ Desplegable en 5 minutos
- ❌ No es para usuario final masivo
- ❌ Performance limitado en datos enormes

**React (Futuro):**
- ✅ Mayor control y flexibilidad
- ✅ Mejor performance
- ✅ UX profesional
- ❌ Más desarrollo
- ❌ Requiere backend separado

**Decision:** Streamlit es perfecto para fase actual. Si escala a miles de usuarios, migra a React.

### P20: ¿Qué pasa si un banco no tiene datos para un indicador?

**R:** Se maneja en dos niveles:

1. **Pipeline:** Filas sin datos se eliminan (`dropna`)
2. **Dashboard:** Si falta indicador, celda vacía (o se oculta)

**Mejora futura:** Mostrar "N/A" con tooltip explicando por qué.

---

## 🚀 PREGUNTAS SOBRE PRODUCTIZACIÓN

### P22: ¿Cómo deployaría esto?

**R:** Arquitectura multi-tier:

```
1. Pipeline: Cron job diario
   uv run scripts/pipeline/main.py

2. Dashboard: Heroku / Railway
   streamlit run scripts/visualizations/main.py

3. API: AWS Lambda / FastAPI on Docker
   docker build . && docker push

4. Data: PostgreSQL en RDS

5. Monitoring: DataDog / CloudWatch
```

**Tiempo deployment:** ~4-6 horas setup inicial, después automático.

### P23: ¿Qué pasa si el Excel no llega a tiempo?

**R:** Pipeline incluye manejo de errores:

```python
try:
    path = ingester.ingest(dataset_name)
except FileNotFoundError as e:
    print(f"❌ Archivo no encontrado: {e}")
    # Mejora futura: enviar alerta email
```

**Mejora:** 
- Alert automático si falta archivo
- Usar última versión disponible
- Dashboard muestra última fecha actualización

### P24: ¿Cómo escalarían a 1000 bancos?

**R:** Cambiaría solo ciertos componentes:

**No cambiaría:**
- Pipeline pattern (funciona igual)
- Lógica de transformación
- API structure

**Sí cambiaría:**
- CSV → PostgreSQL (mejor indexación)
- Streamlit → React (performance)
- Caché más sofisticado
- Computación distribuida (Spark si necesario)

**Estimado:** Refactor de 20-30% del código.

### P25: ¿Cómo implementarían Machine Learning?

**R:** Módulo adicional, sin tocar pipeline:

```
Pipeline ETL
    ↓
Datos Limpios
    ├→ Dashboard (actual)
    └→ ML Module (nuevo)
         ├─ Clustering de bancos
         ├─ Predicción de morosidad
         ├─ Anomaly detection
         └─ Recomendaciones
```

**Tecnología:** scikit-learn, XGBoost, Pandas

---

## 🤔 PREGUNTAS SOBRE DECISIONES ESPECÍFICAS

### P26: ¿Por qué `skiprows=7` al leer el Excel?

**R:** Las primeras 7 filas son metadatos:

```
Fila 1: "SUPERINTENDENCIA DE BANCOS"
Fila 2: Período
Fila 3: En blanco
...
Fila 7: Título de columnas
Fila 8: ← Primer dato
```

`skiprows=7` = "Ignora 7 primeras, usa fila 8 como headers"

### P27: ¿Por qué melt en lugar de pivottable?

**R:** Dirección opuesta:

- **pivot_table:** Agrupa datos (reduce filas)
- **melt:** Separa datos (aumenta filas)

Nuestro caso:
```
ENTRADA: Wide (columnas = bancos)
SALIDA:  Long (filas = observaciones)
```

`melt` es la herramienta correcta.

### P28: ¿Por qué `errors="ignore"` en drop?

**R:** Robustez ante variaciones:

```python
X.drop("BANCOS PRIVADOS VIVIENDA", axis=1, errors="ignore")
```

Si esta columna no existe en alguna hoja, no falla - continúa.

**Alternativa (frágil):**
```python
X.drop("BANCOS PRIVADOS VIVIENDA", axis=1)  # Falla si no existe
```

### P29: ¿Cómo decidieron qué visualizaciones incluir?

**R:** Siguiendo principios de exploración de datos:

**Necesitan responder:**
1. "¿Cómo está este banco?" → Perfil (barras)
2. "¿Cómo se comparan?" → Ranking (barras)
3. "¿Quiénes lideran?" → Top 3 (medallas)
4. "¿Visión completa?" → Tabla (matrix)
5. "¿Hay patrones?" → Heatmap
6. "¿Estadísticas?" → Métricas

Cada visualización responde una pregunta de negocio diferente.

### P30: ¿Por qué 3 categorías y no más?

**R:** Límite natural de los datos:

1. **Balance:** Cuentas de activos (7 indicadores naturales)
2. **Compos Carteras:** Estructura financiera (5 indicadores)
3. **Indicadores:** Ratios de rendimiento (6 indicadores)

Estos 3 vienen del excel fuente. Agregar más requeriría más datos de entrada.
## 🎯 PREGUNTAS TRAMPA (Prepararse)

### P41: "¿No es esto muy simple?"
**R:** "Simple está donde se ve, pero compleja es la arquitectura. La simplicidad es resultado de buen diseño, no falta de pensamiento. Cualquiera puede escribir código complejo; lo difícil es hacerlo simple."

### P42: "¿Por qué no lo hicieron en [otra tecnología]?"
**R:** "[Otra tecnología] también funcionaría, pero Python es el estándar en Data Science por X razones. Cada tecnología tiene tradeoffs; Python optimiza para esto."

### P43: "¿Cuál es la precisión de los datos?"
**R:** "Los datos vienen de la Superintendencia de Bancos - 100% oficiales. Nuestro pipeline no modifica valores, solo reorganiza. Precisión = 100%"

### P44: "¿Qué privacidad de datos tienen?"
**R:** "Los datos son públicos (reporte oficial). El sistema actual no encripta, pero para producción: HTTPS + autenticación + base de datos encriptada."

### P45: "¿Qué pasa si se caída el servidor?"
**R:** "Buena pregunta. Para producción: backup automático, replicación de datos, SLA 99.9% uptime. Actualmente local, sin requerimiento de uptime."

---

## 📚 RESPUESTA GENERAL PARA PREGUNTAS INESPERADAS

Si no saben la respuesta:

**"Esa es una excelente pregunta. [Sinceramente: desconocemos / No lo habíamos considerado]. 

Pero [volvemos a los principios fundamentales]:
- El diseño es modular, así que agregar eso sería [X]
- O podríamos investigarlo como mejora futura

---

## ✅ CHECKLIST FINAL

Antes de la defensa, practica responder:

- [ ] 5 preguntas sobre arquitectura
- [ ] 5 preguntas técnicas
- [ ] 5 preguntas sobre datos
- [ ] 5 preguntas sobre dashboard
- [ ] 5 preguntas sobre productización
- [ ] Practica la demo en vivo 3+ veces
- [ ] Conoce las métricas del proyecto (líneas, clases, KPIs)
- [ ] Prepara respuestas a preguntas trampa
- [ ] Practica mantener la calma ante crítica

**¡ÉXITO EN LA DEFENSA! 🚀**
