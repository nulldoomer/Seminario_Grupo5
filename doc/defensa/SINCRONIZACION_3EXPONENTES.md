# 👥 GUÍA DE SINCRONIZACIÓN - 3 EXPONENTES

**Objetivo:** Asegurar que la presentación fluye perfectamente y cada exponente sabe exactamente cuándo empieza/termina

---

## 📅 CALENDARIO DE PREPARACIÓN

### Semana 1 (Inicial)
- [ ] Cada exponente lee completamente su sección
- [ ] Todos leen GUIA_PRESENTACION_3EXPONENTES.md completo
- [ ] Acuerdan el orden de exposición
- [ ] Revisor de timing designado

### Semana 2 (Práctica Individual)
- [ ] Expositor 1 practica 3 veces solo (10 min exactos)
- [ ] Expositor 2 practica 3 veces solo (10 min exactos)
- [ ] Expositor 3 practica 3 veces solo (10 min exactos)
- [ ] Cada uno prepara 1 pregunta de Q&A

### Semana 3 (Práctica Grupal)
- [ ] Presentación completa (3 × 10 min) = 30 min
- [ ] Minimun 2 veces juntos
- [ ] Practicar transiciones entre exponentes
- [ ] Grabar video para revisión

### Día Anterior a Defensa
- [ ] Revisar timing final
- [ ] Preparar respuestas de Q&A (5 preguntas cada uno)
- [ ] Descansar bien

---

## ⏱️ TIMING EXACTO

### EXPOSITOR 1: Contexto + Problema + Objetivos + Arquitectura

| Tiempo | Contenido | Slide |
|--------|-----------|-------|
| 0:00-0:30 | Portada + Introducción | 1-2 |
| 0:30-1:00 | Contexto Superintendencia | 2-3 |
| 1:00-2:00 | Problema real | 4-6 |
| 2:00-3:00 | Problema (continuación) | 6 |
| 3:00-3:30 | Objetivos generales | 7 |
| 3:30-4:30 | Objetivos específicos | 8 |
| 4:30-5:00 | Arquitectura inicio | 9 |
| 5:00-6:00 | Arquitectura flujo | 9 |
| 6:00-7:00 | Componentes | 10 |
| 7:00-8:00 | Stack tecnológico | 11 |
| 8:00-9:00 | Stack tecnológico (justificación) | 11-12 |
| 9:00-10:00 | Decisiones arquitectónicas + Cierre | 12-13 |

**TRANSICIÓN A EXPOSITOR 2:**
- Expositor 1: "El Expositor 2 ahora explicará cómo funciona el motor técnico..."
- Expositor 2: Se levanta, agradece, avanza a su slide 1

---

### EXPOSITOR 2: ETL Pipeline + FastAPI

| Tiempo | Contenido | Slide |
|--------|-----------|-------|
| 10:00-10:30 | Transición + Revisión | 1-2 |
| 10:30-11:00 | Las 3 hojas clave | 2 |
| 11:00-12:00 | Data Ingestion (skiprows) | 3 |
| 12:00-13:00 | Data Cleaning (7 transformadores) | 4 |
| 13:00-14:00 | MELT: Wide → Long | 5 |
| 14:00-14:30 | MELT ejemplo visual | 5 |
| 14:30-15:00 | Data Consolidation | 6 |
| 15:00-16:00 | FastAPI: Por qué + características | 7-8 |
| 16:00-17:00 | Estructura API | 9 |
| 17:00-18:00 | Endpoints (Financials) | 10 |
| 18:00-19:00 | Endpoints (Advanced Analytics) | 10 |
| 19:00-19:30 | Despliegue local vs Docker | 11 |
| 19:30-20:00 | Lecciones aprendidas | 12 |

**TRANSICIÓN A EXPOSITOR 3:**
- Expositor 2: "El Expositor 3 mostrará cómo el usuario final interactúa con todo esto..."
- Expositor 3: Se levanta, agradece, avanza a su slide 1

---

### EXPOSITOR 3: Dashboard + KPIs + Resultados

| Tiempo | Contenido | Slide |
|--------|-----------|-------|
| 20:00-20:30 | Transición + Progreso | 1-2 |
| 20:30-21:00 | Estructura visual Dashboard | 3 |
| 21:00-21:30 | Visualizaciones (6 tipos) | 4 |
| 21:30-22:00 | KPIs Balance - Introducción | 5 |
| 22:00-22:30 | KPIs Balance - Detalles + interpretación | 5 |
| 22:30-23:00 | KPIs Rendimiento - Intro | 6 |
| 23:00-23:30 | KPIs Rendimiento - Ejemplos reales | 6 |
| 23:30-24:00 | KPIs Estructura | 7 |
| 24:00-24:30 | Top insights (Top bancos) | 8 |
| 24:30-25:00 | Estadísticas del proyecto | 9 |
| 25:00-26:00 | Lecciones aprendidas | 10 |
| 26:00-27:00 | Futuro del proyecto | 11 |
| 27:00-28:00 | Cierre y mensaje final | 12 |
| 28:00-30:00 | Buffer para preguntas | - |

---

## 🔗 PUNTOS DE TRANSICIÓN (Crítico)

### Transición 1 → 2 (Min 10:00)

**Exponitor 1 (Último 30 seg):**
```
"...así que hemos establecido la arquitectura general, 
identificado el problema y diseñado cómo se conectan 
los componentes.

Pero, ¿cómo funciona realmente el motor? 
[PAUSA]
El Expositor 2 ahora explicará el ETL Pipeline 
y la API en detalle."
```

**Expositor 2 (Primer 30 seg):**
```
"Gracias, Expositor 1. Vamos a entrar en el 
motor técnico - cómo limpias datos complejos 
y los haces accesibles.

Recordemos las 3 hojas clave del boletín..."
[Avanza slide]
```

---

### Transición 2 → 3 (Min 20:00)

**Expositor 2 (Último 30 seg):**
```
"...así que el pipeline es robusto, reproducible, 
y la API está lista para que sistemas externos 
accedan a los datos.

Pero todo esto de nada sirve si el usuario 
no lo puede ver ni entender.

El Expositor 3 mostrará cómo presentamos 
esto visualmente y qué resultados obtuvimos."
```

**Expositor 3 (Primer 30 seg):**
```
"Gracias, Expositor 2. Exacto - tenemos datos 
limpios y una API funcionando, pero el usuario 
final necesita una interfaz simple y hermosa.

Streamlit es exactamente eso. Veamos el dashboard..."
[Avanza slide o demo en vivo]
```

---

## 🎯 ROLES Y RESPONSABILIDADES

### EXPOSITOR 1 (Arquitecto / Gerente de Proyecto)
**Debe dominar:**
- [ ] Contexto de Superintendencia (historia, importancia)
- [ ] Problema real (qué duele al usuario)
- [ ] Objetivos específicos y medibles
- [ ] Decisiones arquitectónicas (por qué esas herramientas)
- [ ] Diagrama general del sistema

**Respuestas esperadas a Q&A:**
1. ¿Por qué eligieron estas herramientas?
2. ¿Cuánto tiempo ahorra realmente?
3. ¿A quién le vendería esto?
4. ¿Cuál fue el reto principal?
5. ¿Escalable a otros contextos?

**Tono:** Educativo, ejecutivo, sin tecnicismos innecesarios

---

### EXPOSITOR 2 (Ingeniero Backend / ETL)
**Debe dominar:**
- [ ] Cómo se leen archivos Excel complejos
- [ ] Los 7 transformadores y qué hace cada uno
- [ ] Por qué MELT es crucial (Wide → Long)
- [ ] Estructura de FastAPI
- [ ] Endpoints REST y cómo se usan
- [ ] Diferencia entre desarrollo y producción

**Respuestas esperadas a Q&A:**
1. ¿Por qué usar Pandas y no otra librería?
2. ¿Cuál fue el reto de limpiar datos?
3. ¿Cómo manejan datos incorrectos?
4. ¿Qué pasa si nuevos datos tienen estructura diferente?
5. ¿Cómo escala para 100 bancos?

**Tono:** Técnico pero explicado, mostrar código sin abrumar

---

### EXPOSITOR 3 (Data Analyst / Product Manager)
**Debe dominar:**
- [ ] Cómo funciona el dashboard (UI/UX)
- [ ] Qué es cada KPI y cómo interpretarlo
- [ ] Insights obtenidos del análisis
- [ ] Cómo se usan los resultados en decisiones
- [ ] Futuro y mejoras posibles

**Respuestas esperadas a Q&A:**
1. ¿Qué insight fue más sorprendente?
2. ¿Cómo interpretar ROE > 15%?
3. ¿Qué pasa con morosidad > 3%?
4. ¿Puedo descargar los datos?
5. ¿Qué análisis podrías hacer con Machine Learning?

**Tono:** Ejecutivo, focus en valor, storytelling con datos

---

## 🎬 DEMO EN VIVO (Opcional pero Recomendado)

### Setup
```bash
# Antes de la defensa:
# Terminal 1
cd /ruta/del/proyecto
uv run streamlit run scripts/visualizations/main.py

# Terminal 2
uv run uvicorn api.main:app --reload

# Tener ambas URLs listas:
# - http://localhost:8501 (Dashboard)
# - http://localhost:8000/docs (Swagger API)
```

### Cuándo Demostrar
- **Mejor momento:** Al inicio de Expositor 3 (Min 20:00)
- **Duración:** 1-2 minutos
- **Qué mostrar:**
  1. Dashboard abierto
  2. Cambiar categoría (Balance → Rendimiento)
  3. Seleccionar banco (Pichincha)
  4. Mostrar ranking
  5. Mostrar API Swagger en otra ventana

### Fallback (si falla)
"Como ven en la slide, el dashboard se vería así... [Mostrar screenshot]"

---

## 📋 CHECKLIST DE SINCRONIZACIÓN

### Una Semana Antes
- [ ] Los 3 exponentes conocen su contenido
- [ ] Cada uno practica solo (timing correcto)
- [ ] Acuerdan el orden final
- [ ] Designan revisor de timing

### 2 Días Antes
- [ ] Primera práctica grupal completa
- [ ] Timing = 29-30 minutos
- [ ] Transiciones sincronizadas
- [ ] Grabar para revisión

### 1 Día Antes
- [ ] Segunda práctica grupal
- [ ] Timing exacto (30 min)
- [ ] Respuestas para 5 preguntas cada uno
- [ ] Descanso mental

### Día de Defensa
- [ ] Llegar 15 min antes
- [ ] Revisar equipos (laptop, proyector, audio)
- [ ] Verificar slide deck carga sin errores
- [ ] Respirar profundo
- [ ] Confianza: lo hemos practicado 5+ veces

---

## 🚨 BANDERAS ROJAS (Si Esto Pasa)

### Timing Descontrolado
**Problema:** Expositor 1 toma 13 min en lugar de 10
**Solución:** Otro debe acortar. Designado: Expositor 3 (menos crítico)

### Demo Falla
**Problema:** Código no corre o dashboard no abre
**Solución:** Tener screenshots de respaldo listos

### Olvida su parte
**Problema:** Alguno se queda en blanco
**Solución:** Otro puede ayudar, pero evitarlo practicando más

### Pregunta del jurado fuera de tema
**Problema:** Preguntan sobre Machine Learning (Fase 2)
**Respuesta:** "Excelente pregunta. Ese es el roadmap Fase 2. Para esta defensa..."

---

## 💡 CONSEJOS PROFESIONALES

### Voz y Presentación
- [ ] Hablen lentamente (no apresurarse)
- [ ] Hagan contacto visual con jurados
- [ ] Cambien tono/énfasis (no monótono)
- [ ] De pie, no sentados (más autoridad)
- [ ] Señalen slides cuando hablen de ellas
- [ ] Pausa antes de cambiar de tema (efecto)

### Manejo de Nervios
- [ ] Respiración profunda: 5 seg inhala, 5 seg exhala
- [ ] Practica = confianza
- [ ] Recuerden: ustedes son expertos en su tema
- [ ] Errores pequeños no importan (sigan adelante)
- [ ] Sonría al inicio (warm up)

### Estructura Mental
- Exponitor 1: "Yo establezco el problema"
- Exponitor 2: "Yo muestro la solución técnica"
- Exponitor 3: "Yo muestro el impacto real"
- Todos: "Nosotros resolvemos un problema real"

---

## 📞 CONTACTOS DE EMERGENCIA

**Si algo falla durante la defensa:**
1. **Mantén calma** - Los jurados entienden fallos técnicos
2. **Continúa** - No detengas el flujo
3. **Honestidad** - "La API está en /docs, démosle unos segundos para cargar"
4. **Backup** - Ten screenshots/videos listos

---

## 🎓 LECCIONES FINALES

1. **Timing es crítico.** Practica con cronómetro.
2. **Sincronización es todo.** Practiquen juntos mínimo 2 veces.
3. **Cada uno es experto** en su sección. Habla con confianza.
4. **Demo es bonus.** Si falla, tienes slides de respaldo.
5. **Preguntas son oportunidad.** Responde calmadamente.
6. **30 minutos es mucho** para contar una historia. Usen bien cada segundo.

---

## 🎬 ¡LISTO PARA DEFENDER!

Hicieron un excelente trabajo técnico. Ahora demuestren eso en la presentación.

**Recuerden:** Así como el código es limpio y modular, la presentación debe ser clara y fluida.

**Confianza. Práctica. Excelencia.** 💪

---

**Última actualización:** Noviembre 2025  
**Versión:** Final para presentación de 3 exponentes
