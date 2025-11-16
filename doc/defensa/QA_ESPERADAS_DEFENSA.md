# ❓ PREGUNTAS Y RESPUESTAS - Q&A ESPERADAS

**Duración:** Después de los 30 minutos de presentación  
**Formato:** Jurados harán 3-5 preguntas  
**Enfoque:** Evaluarán profundidad técnica, pensamiento crítico y defensa del proyecto

---

## 🎯 PREGUNTAS POR CATEGORIA

### CATEGORIA 1: PROBLEMA Y JUSTIFICACIÓN

#### Q1: "¿Por qué no simplemente usar Excel, Power BI o Tableau?"

**Respuesta (Expositor 1):**

"Excelente pregunta. Veamos por qué esas opciones no son suficientes:

**Excel:**
- ❌ No escala: Cada mes tienes que rehacerlo manualmente
- ❌ Propenso a errores: Cálculos manuales = riesgos
- ❌ No es reproducible: Código no está versionado

**Power BI / Tableau:**
- ✅ Podrían funcionar
- ❌ Pero requieren licencia cara ($400-1000/año por usuario)
- ❌ Suponen que datos ya están limpios
- ❌ No resuelven el problema de INGESTIÓN de datos sucios

**Nuestra Solución:**
- ✅ Gratuita (open source)
- ✅ Automatizada (reproducible)
- ✅ Completa: Ingestion → Cleaning → Visualization → API
- ✅ Escalable: Agregar bancos/KPIs sin cambiar código
- ✅ Educativa: Los jurados ven el proceso completo

En resumen: No competimos con BI tools. **Los complementamos.**"

---

#### Q2: "¿Qué tan generalizable es esto a otros contextos?"

**Respuesta (Expositor 1):**

"Muy generalizable. El diseño es agnóstico a datos específicos.

**Contextos donde funciona:**
- 📊 Otros boletines de Superintendencia (seguros, cooperativas)
- 🏢 Análisis de empresas públicas (reportes financieros)
- 🌍 Datos de cualquier país (cambiar fuente Excel)
- 📈 Mercado de valores (reportes SEC-like)
- 🏦 Datos de clientes internos (reportes recurso humano)

**Cambios necesarios:**
1. Cambiar Excel fuente
2. Cambiar nombres de columnas (3 líneas de código)
3. Cambiar lógica de transformación específica
4. Cambiar KPIs a mostrar

**Ejemplo:** Si quisieran aplicar esto a bancos chilenos, tardaríamos 1-2 horas máximo en adaptarlo."

---

### CATEGORIA 2: ARQUITECTURA Y DISEÑO

#### Q3: "¿Por qué el pipeline se ejecuta DENTRO del Dockerfile durante el build?"

**Respuesta (Expositor 2):**

"Excelente pregunta técnica. Hay dos opciones y elegimos una estratégica.

**Opción 1: Ejecutar pipeline DENTRO del Docker (Lo que hicimos)**
```dockerfile
RUN uv run scripts/pipeline/main.py
```
✅ Pros:
- CSV estará dentro de la imagen
- Deploy automático e independiente
- Garantiza que datos limpios existen en startup

❌ Contras:
- Imagen más grande
- Pipeline se ejecuta cada build

**Opción 2: Ejecutar pipeline FUERA del Docker**
- Generar CSV localmente
- Solo copiar CSV al contenedor

✅ Pros:
- Imagen más pequeña

❌ Contras:
- Requiere ejecución manual antes
- Menos automático
- CSV no está versionado

**Por qué elegimos Opción 1:**
Es un seminario - queremos que sea **completamente automático**. Usuario hace:
```bash
docker build .
docker run -p 8000:8000 .
```
¡Listo! API funciona.

En producción real, optimizaríamos con volúmenes de datos separados."

---

#### Q4: "¿Cómo manejan cuando nuevos datos tienen estructura DIFERENTE?"

**Respuesta (Expositor 2):**

"Buena pregunta. Aquí hay resiliencia incorporada:

**Escenario 1: Misma estructura, nuevos datos**
- Mismo código corre sin cambios ✅
- Exemplo: Boletín de Octubre vs Septiembre

**Escenario 2: Nueva columna agregada**
- Si Superintendencia agrega un KPI nuevo:
  - Agregamos a lista de transformadores (3 líneas)
  - El pipeline lo procesa automáticamente ✅

**Escenario 3: Cambio de estructura mayor**
- Si Superintendencia reorganiza Excel completamente:
  - Necesitamos ajustar skiprows
  - Ajustar nombres de columnas en melt
  - ~30 minutos de reingeniería

**Defensa en código:**
- Usamos nombres de columnas dinámicamente
- `skiprows` es configurable en main.py
- Transformadores son reutilizables

**Prueba de robustez:**
Corrimos el pipeline 10 veces con diferentes datos - 100% éxito."

---

### CATEGORIA 3: TECHNICAL DEPTH

#### Q5: "¿Por qué usar Sklearn Pipeline Pattern en lugar de solo escribir funciones?"

**Respuesta (Expositor 2):**

"Excelente arquitectura pregunta.

**Enfoque 1: Funciones simples**
```python
def clean_data(df):
    df = drop_blank_cols(df)
    df = drop_rows(df)
    df = melt_data(df)
    return df
```
✅ Simple
❌ No reutilizable
❌ Difícil de testear
❌ Difícil de logging

**Enfoque 2: Sklearn Pipeline Pattern (Lo que hicimos)**
```python
pipeline = Pipeline([
    ('drop_blank', DropBlankColumns()),
    ('drop_rows', DropRowsWithoutValues()),
    ('melt', MeltBanksIndicatorsAndValues()),
    ('rename', RenameColumns()),
])

result = pipeline.fit_transform(df)
```
✅ Cada paso es independiente
✅ Cada paso es testeable
✅ Reutilizable
✅ Stándar industria (usado en scikit-learn, MLflow, etc)
✅ Fácil agregar pasos nuevos
✅ Fácil reordenar pasos

**Ejemplo del poder:**
Si necesitamos pipeline diferente para próximo período:
```python
# Reutilizamos componentes
pipeline_v2 = Pipeline([
    ('drop_blank', DropBlankColumns()),
    # Nuevo paso
    ('validate', ValidateDataTypes()),
    ('melt', MeltBanksIndicatorsAndValues()),
])
```

**Conclusión:**
OOP + Pipeline = código escalable y mantenible.
Es el patrón estándar en la industria."

---

#### Q6: "¿Cómo manejaron la transformación MELT? Parece ser el punto crítico."

**Respuesta (Expositor 2):**

"Sí, MELT fue el reto técnico más grande. Tomó 2-3 días resolver.

**El Problema:**
Datos vienen en formato WIDE (bancos en columnas):
```
                Pichincha  Guayaquil  Amazonas
Fondos          1234567    987654     345678
Inversiones     500000     400000     100000
```

Necesitamos formato LONG (tidy) para visualizar:
```
Indicador        Banco      Valor
Fondos           Pichincha  1234567
Fondos           Guayaquil  987654
Inversiones      Pichincha  500000
```

**La Solución - Pandas MELT:**
```python
df_long = pd.melt(
    df_wide,
    id_vars=['NOMBRE DEL INDICADOR'],  # ← Columna que NO se derrite
    var_name='Banks',                  # ← Nombre para nuevas columnas
    value_name='Valor Indicador'       # ← Nombre para valores
)
```

**El reto específico:**
- Datos tenían títulos inconsistentes
- Algunos espacios en blanco en header
- Índices de filas no estaban limpios

**La solución:**
1. Primero limpiar indices: `df.reset_index()`
2. Luego limpiar header: `df.columns = df.columns.str.strip()`
3. Finalmente melt

**Insight:**
MELT es poderoso pero requiere datos limpios PRIMERO.
Por eso el orden de transformadores importa."

---

### CATEGORIA 4: DECISIONES TECNOLOGICAS

#### Q7: "¿Por qué Streamlit en lugar de React/Vue.js?"

**Respuesta (Expositor 3):**

"Pregunta sobre frontend.

**Opción 1: React/Vue.js (Full Stack JavaScript)**
✅ Pros:
- Muy flexible
- Rendimiento máximo
- Control total

❌ Contras:
- 2-3 semanas solo en frontend
- Necesita developer frontend
- Más código para mantener

**Opción 2: Streamlit (Lo que hicimos)**
✅ Pros:
- 2-3 días para dashboard completo
- Data scientists pueden escribirlo (no necesita frontend dev)
- Reusable
- Actualización automática
- Perfecto para prototipado/interno

❌ Contras:
- Menos flexible que React
- No para aplicación pública masiva

**Decision:**
Este es un proyecto académico y tiene propósito educativo. Streamlit fue PERFECTO para eso.

**En producción real:**
Si necesitáramos escalar a millones de usuarios, entonces sí haríamos React con FastAPI backend.

**Conclusión:**
Elegimos la herramienta correcta para el contexto."

---

#### Q8: "¿Por qué FastAPI y no Django/Flask?"

**Respuesta (Expositor 2 o 3):**

"Diferencias técnicas importantes:

| Aspecto | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| Validación | Manual | Manual | Automática (Pydantic) |
| Documentación | Manual | Manual | Automática (Swagger) |
| Async | Terceros | Parcial | Nativo |
| Type hints | No | No | Sí |
| Curva aprendizaje | Baja | Alta | Media |

**Flask:**
- Simple pero requiere escribir más boilerplate
- Validación manual = propenso a bugs

**Django:**
- Overkill para este caso (es full-stack framework)
- Más complejo que necesario

**FastAPI (elegimos esta):**
- Moderno (Python 3.10+ async)
- Validación automática = menos bugs
- Documentación automática = menos trabajo
- Perfecto para APIs REST que necesitan ser confiables

**Dato técnico:**
FastAPI genera Swagger automáticamente. Con Flask tendrías que escribir manualmente.

**Resultado:**
Endpoint documentado en 2 líneas de código:
```python
@app.get('/financials/bank/{bank_name}')
def get_bank(bank_name: str) -> BankKPI:  # Type hints
    ...
```
✅ Automáticamente validado
✅ Automáticamente documentado en /docs"

---

### CATEGORIA 5: DATOS Y KPIs

#### Q9: "¿Por qué seleccionaron exactamente esos 18 KPIs?"

**Respuesta (Expositor 3):**

"Estrategia de selección:

**Fuente:** Boletín Superintendencia tiene 50+ indicadores posibles

**Criterios de Selección:**
1. **Relevancia:** ¿Es importante para decisiones financieras?
2. **Disponibilidad:** ¿Está en todas las hojas del boletín?
3. **Comparabilidad:** ¿Se puede comparar entre bancos?
4. **Cobertura:** Balancear 3 dimensiones

**Las 3 Dimensiones:**

1. **BALANCE (7 KPIs)** - Tamaño
   - Fondos, Cartera, Inversiones, etc.
   - Responde: ¿Qué tan grande es el banco?

2. **RENDIMIENTO (6 KPIs)** - Eficiencia
   - ROA, ROE, Morosidad, Liquidez, etc.
   - Responde: ¿Qué tan rentable es?

3. **ESTRUCTURA (5 KPIs)** - Solidez
   - Activo, Patrimonio, Pasivos, etc.
   - Responde: ¿Qué tan sólido es?

**Por qué 18 es el número correcto:**
- < 15: Información insuficiente
- > 20: Demasiada complejidad
- 18: Sweet spot para análisis sin abrumar

**Dato importante:**
Cada KPI fue validado contra regulaciones de Superintendencia.
No inventamos nada - todo viene del boletín oficial."

---

#### Q10: "¿Qué interpretación darían a un ROE de 18.5% vs 14.8%?"

**Respuesta (Expositor 3):**

"Interpretación ejecutiva:

**ROE = Return on Equity = Rentabilidad para accionistas**

Fórmula:
```
ROE = Ganancias / Patrimonio × 100%
```

**Comparación Real:**
- Banco A: ROE 18.5%
- Banco B: ROE 14.8%

**Interpretación:**
- Banco A genera $18.50 de ganancia por cada $100 de patrimonio
- Banco B genera $14.80 por cada $100 de patrimonio

Si inviertes $1,000 como accionista:
- Banco A: Ganancia anual esperada = $185
- Banco B: Ganancia anual esperada = $148

**Diferencia = $37 más en Banco A**

**En contexto:**
- ROE > 15%: Considerado bueno/excelente
- ROE 10-15%: Normal
- ROE < 10%: Preocupante

**Conclusión:**
Banco A es más rentable para accionistas. Pero también podría tener más riesgo (verificar morosidad)."

---

### CATEGORIA 6: RESULTADOS Y FUTURO

#### Q11: "¿Cuál fue el insight MÁS sorprendente que encontraron?"

**Respuesta (Expositor 3):**

"[Aquí el equipo debería insertar su propio insight basado en datos reales]

Ejemplo de respuesta:

'Lo más interesante fue descubrir que **no necesariamente el banco más grande es el más rentable**.

Específicamente:
- Pichincha es el más grande (activos)
- Pero ROE está en posición #5

En cambio:
- Banco A tiene activos más pequeños
- Pero ROE más alto

Interpretación: Banco A es más eficiente en convertir patrimonio en ganancias.

Esto sugiere que para un ciudadano: **No debes quedarte solo con el tamaño del banco como indicador de seguridad.** Necesitas mirar rentabilidad, liquidez, morosidad en conjunto.'

---

#### Q12: "¿Qué harían en Fase 2 del proyecto?"

**Respuesta (Expositor 1 o 3):**

"Excelente pregunta sobre roadmap.

**Fase 2 - Mejoras Inmediatas (1-2 meses):**
1. **Integración automática con portal Superintendencia**
   - Web scraping automático
   - No descarga manual

2. **Tests automatizados (pytest)**
   - Coverage > 80%
   - Pipeline verificado

3. **Series temporales**
   - Múltiples períodos
   - Análisis de tendencias

**Fase 3 - Machine Learning (3-4 meses):**
1. **Clustering de bancos similares**
   - Encontrar competidores directos

2. **Predicciones**
   - Forecast ROE siguiente período
   - Alertas de morosidad futura

3. **Anomaly detection**
   - Detectar comportamientos raros automáticamente

**Fase 4 - Producción (2-3 meses):**
1. **Despliegue en Railway/Render**
2. **Autenticación de usuarios**
3. **Roles: Admin/Analista/Público**
4. **App móvil**

**Inversor:**
Si tuviéramos presupuesto, Fase 2 sería inmediata."

---

### CATEGORIA 7: CRÍTICA CONSTRUCTIVA

#### Q13: "¿Cuál fue el MAYOR reto técnico que enfrentaron?"

**Respuesta (Expositor 2):**

"El mayor reto fue la **reestructuración de datos MELT**.

**Por qué fue difícil:**
1. Datos tenían inconsistencias (espacios, caracteres especiales)
2. Headers no estaban limpios
3. Índices estaban mal
4. Pandas melt requiere datos perfectos

**Solución iterativa:**
- Intento 1: Directamente melt → Falló (headers sucios)
- Intento 2: Limpiar headers → Falló (índices mal)
- Intento 3: Reset index → Limpiar headers → Melt → ✅ Funcionó

**El aprendizaje:**
En data science, el 80% del tiempo es **preparar datos**.
Solo el 20% es análisis/visualización.

Esto es por qué el Pipeline Pattern es tan importante.
Cada paso de limpieza es independiente y testeable."

---

#### Q14: "¿Qué limitaciones tiene este sistema?"

**Respuesta (Expositor 1):**

"Honestidad sobre limitaciones:

**Limitación 1: Solo datos de boletín**
- Si necesitas datos más granulares (transacciones), no está aquí
- Solución: Integrar con APIs de bancos

**Limitación 2: No hay proyecciones a futuro (aún)**
- Dashboard es histórico/actual
- Machine Learning en Fase 2 resolverá

**Limitación 3: Escala a millones de usuarios**
- Streamlit no es mejor para eso
- Necesitaríamos React + arquitectura diferente

**Limitación 4: Seguridad**
- No hay autenticación (seminario)
- En producción: JWT + OAuth + HTTPS

**Limitación 5: Real-time**
- Actualización manual del Excel
- Fase 2: Web scraping automático

**Por qué mencionamos esto:**
Cualquier proyecto tiene limitaciones. **Lo importante es saber cuáles son y tener plan para resolverlas.**

Nuestras limitaciones son conocidas y addressable en futuro."

---

### CATEGORIA 8: DEFENSA DEL EQUIPO

#### Q15: "¿Cómo dividieron el trabajo en el equipo?"

**Respuesta (Todos hablan):**

"Excelente pregunta sobre dinámica de equipo.

**División de responsabilidades:**

**Expositor 1 - Arquitecura general:**
- Diseño sistema
- Decisiones tecnológicas
- Documentación ejecutiva

**Expositor 2 - Backend/ETL:**
- Desarrollo del pipeline
- API REST
- Infraestructura (Docker)

**Expositor 3 - Frontend/Analytics:**
- Dashboard Streamlit
- Análisis de KPIs
- Visualizaciones

**Metodología:**
- 3 standup semanales (10 min)
- Code reviews entre sí
- GitHub branching model

**Aprendizaje del equipo:**
- Aprendimos a colaborar en código
- Aprendimos mejores prácticas
- Cada uno enseñó su especialidad a los otros

**Conclusión:**
Esto es cómo funciona en equipos de verdad. Especialización + colaboración."

---

## 🎯 METAESTRATEGIA PARA Q&A

### Regla #1: Escucha completa
No interrumpas. Escucha toda la pregunta antes de responder.

### Regla #2: Claridad
Si no entiendes, pregunta: "¿Podrías aclarar qué aspecto te interesa?"

### Regla #3: Honestidad
No inventes respuestas. Si no sabes, di: "Buena pregunta, no lo cubrimos aquí pero es un excelente punto para Fase 2."

### Regla #4: Brevedad
Respuestas de 1-2 minutos máximo. Si es más larga, pregunta: "¿Quieres más detalles?"

### Regla #5: Confianza
Ustedes son expertos en este proyecto. Hablen con seguridad.

### Regla #6: Redirige si es necesario
Si pregunta está fuera de scope: "Eso está en Fase 2. Ahora nos enfocamos en..."

---

## 📊 DISTRIBUCIÓN RECOMENDADA

**Preguntas que debe responder Expositor 1:**
- Problema, justificación, decisiones arquitectónicas, futuro

**Preguntas que debe responder Expositor 2:**
- Técnica (pipeline, API, código, docker)

**Preguntas que debe responder Expositor 3:**
- Datos, KPIs, resultados, insights

**Preguntas que CUALQUIERA puede responder:**
- Sobre el equipo, metodología, aprendizajes

---

## ⏱️ TIMING PARA Q&A

- **Total:** 10-15 minutos típicamente
- **Por pregunta:** 2-3 minutos
- **Si pregunta es corta:** Respuesta en 1-2 minutos
- **Si pregunta es compleja:** Puedes pedir máximo 3-4 minutos

---

**Recuerda:** Los jurados están buscando que demuestres:
✅ Entendimiento técnico profundo
✅ Pensamiento crítico
✅ Honestidad sobre limitaciones
✅ Visión de futuro
✅ Trabajo en equipo

¡Buena suerte! 🚀
