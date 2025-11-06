from components.indicator_config import IndicatorConfig
from components.data_handler import DataHandler
from components.metrics_calculator import MetricsCalculator
from components.charts_builder import ChartBuilder
from components.ui_components import UIComponents

from data_loader import VisualizationDataLoader 
import streamlit as st

# =========================================================
# 🔧 CONFIGURACIÓN INICIAL
# =========================================================
st.set_page_config(
    page_title="Dashboard de Salud Financiera",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# 📁 INICIALIZACIÓN Y CARGA DE DATOS
# =========================================================
@st.cache_resource
def init_data_handler():
    """Inicializa el DataHandler (se cachea para no recargar)"""
    data_loader = VisualizationDataLoader()
    return DataHandler(data_loader)


# Inicializar DataHandler
dh = init_data_handler()

# Cargar datos
df = dh.load_data("Final Dataframe")

if df is None:
    st.error("❌ Error al cargar los datos")
    st.stop()



# =========================================================
# 🎨 ENCABEZADO
# =========================================================
st.title("💰 Dashboard de Salud Financiera Bancaria")
st.markdown("""
**Análisis integral del Sistema Bancario Ecuatoriano**  
Dashboard interactivo para evaluar indicadores de Balance, Rendimiento y Estructura Financiera.
""")


# =========================================================
# 🏦 SIDEBAR - FILTROS Y CONFIGURACIÓN
# =========================================================
with st.sidebar:
    st.header("🔍 Panel de Control")
    st.markdown("---")
    
    # Selector de categoría
    categoria = st.radio(
        "📈 Categoría de Análisis",
        ["Balance", "Rendimiento", "Estructura"],
        help="Selecciona el tipo de indicadores a analizar"
    )
    
    # Obtener configuración de la categoría
    is_percentage = IndicatorConfig.is_category_percentage(categoria)
    unit = IndicatorConfig.get_category_unit(categoria)
    indicator_names = IndicatorConfig.get_indicator_names_by_category(categoria)
    
    # Mostrar info según categoría
    if categoria == "Balance":
        st.info("💼 **Balance:** Activos y recursos del banco")
    elif categoria == "Rendimiento":
        st.info("📊 **Rendimiento:** Rentabilidad y eficiencia")
    else:
        st.info("🏗️ **Estructura:** Composición financiera")
    
    # Filtrar datos según categoría
    df_filtrado = dh.filter_by_category(
        indicator_names=indicator_names,
        convert_percentage=is_percentage
    )
    
    if df_filtrado.empty:
        st.error(f"⚠️ No hay datos para la categoría {categoria}")
        st.stop()
    
    st.markdown("---")
    
    # Selector de banco
    bancos = dh.get_unique_values(df_filtrado, "banks")
    selected_bank = st.selectbox(
        "🏦 Selecciona un Banco",
        bancos,
        help="Elige el banco a analizar"
    )
    
    st.markdown("")
    
    # Selector de indicador
    indicadores = dh.get_unique_values(df_filtrado, "nombre_del_indicador")
    selected_indicator = st.selectbox(
        "📊 Selecciona un Indicador",
        indicadores,
        help="Indicador específico para ranking"
    )
    
    st.markdown("---")
    
    # Información adicional
    indicadores_categoria = IndicatorConfig.get_all_indicators_by_category(categoria)
    st.caption(f"📌 **Indicadores activos:** {len(indicadores_categoria)}")
    st.caption(f"🏦 **Bancos analizados:** {len(bancos)}")
    st.caption(f"📅 **Periodo:** Septiembre 2025")


# =========================================================
# 📊 MÉTRICAS PRINCIPALES
# =========================================================
# Inicializar calculadora de métricas
calc = MetricsCalculator()

# Calcular métricas
total_bancos = df_filtrado["banks"].nunique()
total_indicadores = len(IndicatorConfig.get_all_indicators_by_category(categoria))
total_valor = calc.calculate_total(df_filtrado)
promedio = calc.calculate_average(df_filtrado)

# Renderizar tarjetas
ui = UIComponents()
ui.render_metric_cards(
    total_bancos=total_bancos,
    total_indicadores=total_indicadores,
    total_valor=total_valor,
    promedio=promedio,
    is_percentage=is_percentage
)

st.markdown("---")


# =========================================================
# 📊 VISUALIZACIÓN 1 — INDICADORES DEL BANCO SELECCIONADO
# =========================================================
st.subheader(f"📈 Perfil Financiero: {selected_bank}")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Obtener datos del banco
    bank_data = dh.get_bank_data(df_filtrado, selected_bank, sort_by_value=True)
    
    if not bank_data.empty:
        # Crear visualización
        builder = ChartBuilder(is_percentage, unit)
        fig1 = builder.create_horizontal_bar(
            df=bank_data,
            title=f"Indicadores de {categoria} - {selected_bank}",
            figsize=(12, 6),
            color="#2E86AB"
        )
        st.pyplot(fig1)
    else:
        st.warning("No hay datos disponibles para este banco.")

with col_right:
    if not bank_data.empty:
        st.markdown("### 📋 Resumen")
        
        # Obtener indicadores máximo y mínimo
        nombre_max, valor_max = calc.get_max_indicator(bank_data)
        nombre_min, valor_min = calc.get_min_indicator(bank_data)
        
        # Formatear valores
        if is_percentage:
            valor_max_fmt = f"{valor_max:.2f}%"
            valor_min_fmt = f"{valor_min:.2f}%"
        else:
            valor_max_fmt = f"${valor_max:,.0f}"
            valor_min_fmt = f"${valor_min:,.0f}"
        
        # Truncar nombres largos
        nombre_max_short = nombre_max[:30] + "..." if len(nombre_max) > 30 else nombre_max
        nombre_min_short = nombre_min[:30] + "..." if len(nombre_min) > 30 else nombre_min
        
        st.metric(
            "🔝 Indicador Mayor",
            valor_max_fmt,
            nombre_max_short
        )
        
        st.metric(
            "🔻 Indicador Menor",
            valor_min_fmt,
            nombre_min_short
        )

st.markdown("---")


# =========================================================
# 🥇 VISUALIZACIÓN 2 — RANKING POR INDICADOR
# =========================================================
st.subheader(f"🏆 Ranking: {selected_indicator}")

# Obtener ranking
ranking_df = dh.get_ranking(df_filtrado, selected_indicator, ascending=False)

if not ranking_df.empty:
    col_chart, col_top = st.columns([2, 1])
    
    with col_chart:
        # Crear gráfico de ranking
        builder = ChartBuilder(is_percentage, unit)
        fig2 = builder.create_ranking_chart(
            df=ranking_df,
            title=f"Ranking: {selected_indicator}",
            figsize=(12, 8)
        )
        st.pyplot(fig2)
    
    with col_top:
        st.markdown("### 🎖️ Top 3")
        
        # Renderizar top 3 con medallas
        ui.render_top3_medals(
            df=ranking_df,
            bank_col="banks",
            value_col="valor_indicador",
            is_percentage=is_percentage
        )
        
        st.markdown("---")
        
        # Renderizar bottom 3
        ui.render_bottom3(
            df=ranking_df,
            n=3,
            bank_col="banks",
            value_col="valor_indicador",
            is_percentage=is_percentage
        )
else:
    st.warning("No hay datos disponibles para este indicador.")

st.markdown("---")


# =========================================================
# 📋 TABLA COMPARATIVA INTERACTIVA
# =========================================================
st.subheader(f"📊 Comparativa: {categoria}")

# Obtener orden de indicadores según configuración
indicator_order = [ind.name for ind in IndicatorConfig.get_all_indicators_by_category(categoria)]

# Crear tabla pivote
pivot_df = dh.get_pivot_table(df_filtrado, indicator_order)

if not pivot_df.empty:
    # Aplicar formato condicional
    if is_percentage:
        styled_df = (
            pivot_df.style
            .format("{:.2f}%")
            .background_gradient(cmap="YlGnBu", axis=0)
            .set_properties(**{'text-align': 'right'})
        )
    else:
        styled_df = (
            pivot_df.style
            .format("${:,.0f}")
            .background_gradient(cmap="YlGnBu", axis=0)
            .set_properties(**{'text-align': 'right'})
        )
    
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Opción de descarga
    col_down1, col_down2 = st.columns([1, 3])
    with col_down1:
        ui.render_download_button(
            df=pivot_df,
            filename=f'comparativa_{categoria.lower()}.csv',
            label="📥 Descargar CSV"
        )
else:
    st.warning("No se pudo generar la tabla comparativa.")

st.markdown("---")


# =========================================================
# 📊 VISUALIZACIÓN ADICIONAL — ANÁLISIS COMPARATIVO
# =========================================================
st.subheader("🔥 Análisis Visual Comparativo")

# Seleccionar top bancos para análisis
top_n = st.slider("¿Cuántos bancos mostrar?", 5, len(bancos), 10)

# Crear visualización de comparación múltiple
if not pivot_df.empty:
    # Tomar top bancos por suma total
    pivot_sorted = pivot_df.sum(axis=1).sort_values(ascending=False).head(top_n)
    top_bancos = pivot_sorted.index.tolist()
    
    pivot_top = pivot_df.loc[top_bancos]
    
    # Crear heatmap
    builder = ChartBuilder(is_percentage, unit)
    fig3 = builder.create_heatmap(
        pivot_df=pivot_top,
        title=f"Mapa de Calor: Top {top_n} Bancos - {categoria}",
        figsize=(14, 8),
        normalize=True
    )
    st.pyplot(fig3)
else:
    st.warning("No hay suficientes datos para el análisis comparativo.")

st.markdown("---")


# =========================================================
# 📊 SECCIÓN ADICIONAL: ESTADÍSTICAS DETALLADAS
# =========================================================
with st.expander("📈 Ver Estadísticas Detalladas"):
    st.markdown(f"### Estadísticas Globales - {categoria}")
    
    # Calcular estadísticas resumidas
    stats = calc.get_sumary_stats(df_filtrado)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if is_percentage:
            st.metric("📊 Mediana", f"{stats['mediana']:.2f}%")
            st.metric("📏 Desviación Estándar", f"{stats['desviacion']:.2f}%")
        else:
            st.metric("📊 Mediana", f"${stats['mediana']:,.2f}")
            st.metric("📏 Desviación Estándar", f"${stats['desviacion']:,.2f}")
    
    with col2:
        if is_percentage:
            st.metric("⬆️ Valor Máximo", f"{stats['max']:.2f}%")
            st.metric("⬇️ Valor Mínimo", f"{stats['min']:.2f}%")
        else:
            st.metric("⬆️ Valor Máximo", f"${stats['max']:,.0f}")
            st.metric("⬇️ Valor Mínimo", f"${stats['min']:,.0f}")
    
    with col3:
        rango = stats['max'] - stats['min']
        coef_variacion = (stats['desviacion'] / stats['promedio'] * 100) if stats['promedio'] != 0 else 0
        
        if is_percentage:
            st.metric("📏 Rango", f"{rango:.2f}%")
        else:
            st.metric("📏 Rango", f"${rango:,.0f}")
        
        st.metric("📊 Coef. Variación", f"{coef_variacion:.2f}%")


# =========================================================
# 📊 SECCIÓN ADICIONAL: ANÁLISIS POR BANCO
# =========================================================
with st.expander("🏦 Análisis Detallado por Banco"):
    st.markdown("### Comparación Multi-Banco")
    
    # Selector múltiple de bancos
    default_banks = bancos[:3] if len(bancos) >= 3 else bancos
    bancos_comparar = st.multiselect(
        "Selecciona bancos para comparar",
        bancos,
        default=default_banks
    )
    
    if bancos_comparar:
        # Filtrar datos de bancos seleccionados
        df_comparacion = df_filtrado[df_filtrado["banks"].isin(bancos_comparar)]
        
        # Crear tabla pivote
        pivot_comparacion = dh.get_pivot_table(df_comparacion, indicator_order)
        
        # Ordenar por bancos seleccionados
        available_banks = [b for b in bancos_comparar if b in pivot_comparacion.index]
        if available_banks:
            pivot_comparacion = pivot_comparacion.loc[available_banks]
        
        # Mostrar tabla
        if not pivot_comparacion.empty:
            if is_percentage:
                st.dataframe(
                    pivot_comparacion.style
                    .format("{:.2f}%")
                    .background_gradient(cmap="RdYlGn", axis=1)
                    .set_properties(**{'text-align': 'right'}),
                    use_container_width=True
                )
            else:
                st.dataframe(
                    pivot_comparacion.style
                    .format("${:,.0f}")
                    .background_gradient(cmap="RdYlGn", axis=1)
                    .set_properties(**{'text-align': 'right'}),
                    use_container_width=True
                )
            
            # Botón de descarga
            ui.render_download_button(
                df=pivot_comparacion,
                filename=f'comparacion_bancos_{categoria.lower()}.csv',
                label="📥 Descargar Comparación"
            )
        else:
            st.warning("No hay datos para los bancos seleccionados.")


st.markdown("---")


# =========================================================
# 📊 PIE DE PÁGINA
# =========================================================
st.caption("📊 Desarrollado por Grupo 5 — Proyecto Integrador 2025")
st.caption("💡 Dashboard de Salud Financiera - Sistema Bancario Ecuatoriano")
st.caption("📅 Datos: Superintendencia de Bancos - Septiembre 2025")


# # =========================================================
# # 🔍 INFORMACIÓN DE DEBUG (Opcional - Solo en desarrollo)
# # =========================================================
# if st.sidebar.checkbox("🔧 Modo Debug", value=False):
#     st.markdown("---")
#     st.markdown("### 🔍 Información de Debug")
#
#     col_debug1, col_debug2 = st.columns(2)
#
#     with col_debug1:
#         st.markdown("**Información del Dataset:**")
#         summary = dh.get_summary(df)
#         st.json({
#             "Shape": summary["shape"],
#             "Total Bancos": summary["total_banks"],
#             "Total Indicadores": summary["total_indicators"]
#         })
#
#     with col_debug2:
#         st.markdown("**Filtros Activos:**")
#         st.json({
#             "Categoría": categoria,
#             "Es Porcentaje": is_percentage,
#             "Unidad": unit,
#             "Banco": selected_bank,
#             "Indicador": selected_indicator
#         })
#
#     st.markdown("**Vista previa de datos filtrados:**")
#     st.dataframe(df_filtrado.head(10), use_container_width=True)
#
#     st.markdown("**Columnas disponibles:**")
#     st.write(df.columns.tolist())
