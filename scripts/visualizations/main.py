from components.charts_builder import ChartBuilder
from components.ui_components import UIComponents
import streamlit as st
import pandas as pd
from services.api_client import get_api_client

st.set_page_config(
    page_title="Dashboard de Salud Financiera",
    page_icon="💰",
    layout="wide"
)

api_client = get_api_client()



st.title("💰 Dashboard de Salud Financiera Bancaria")
st.markdown("""
**Análisis integral del Sistema Bancario Ecuatoriano**  
Dashboard interactivo conectado a API REST para consultar indicadores financieros.
""")

col_badge1, col_badge2 = st.columns([3, 1])
with col_badge2:
    st.success("🔌 API Conectado")

with st.sidebar:
    st.header("🔍 Panel de Control")
    st.markdown("---")
    
    # Selector de categoría
    categoria = st.radio(
        "📈 Categoría de Análisis",
        ["Balance", "Rendimiento", "Estructura"],
        help="Selecciona el tipo de indicadores a analizar"
    )
    
    # Obtener lista de bancos desde el API
    with st.spinner("Cargando bancos..."):
        bancos = api_client.get_banks_list(categoria)
    
    if not bancos:
        st.error("No se pudieron cargar los bancos")
        st.stop()
    
    # Obtener lista de indicadores desde el API
    with st.spinner("Cargando indicadores..."):
        indicators_data = api_client.get_indicators_list(categoria)
    
    if not indicators_data:
        st.error("No se pudieron cargar los indicadores")
        st.stop()
    
    indicadores = indicators_data.get("indicators", [])
    
    # Mostrar info según categoría
    if categoria == "Balance":
        st.info("💼 **Balance:** Activos y recursos del banco")
    elif categoria == "Rendimiento":
        st.info("📊 **Rendimiento:** Rentabilidad y eficiencia")
    else:
        st.info("🏗️ **Estructura:** Composición financiera")
    
    st.markdown("---")
    
    # Selector de banco
    selected_bank = st.selectbox(
        "🏦 Selecciona un Banco",
        bancos,
        help="Elige el banco a analizar"
    )
    
    st.markdown("")
    
    # Selector de indicador
    selected_indicator = st.selectbox(
        "📊 Selecciona un Indicador",
        indicadores,
        help="Indicador específico para ranking"
    )
    
    st.markdown("---")
    
    # Información adicional
    st.caption(f"📌 **Indicadores activos:** {len(indicadores)}")
    st.caption(f"🏦 **Bancos analizados:** {len(bancos)}")
    st.caption(f"📅 **Periodo:** Septiembre 2025")
    st.caption(f"🔌 **API:** {api_client.base_url}")

with st.spinner(f"🔄 Cargando datos de {selected_bank}..."):
    bank_response = api_client.get_bank_financials(selected_bank, categoria)

if not bank_response:
    st.error("No se pudieron cargar los datos del banco")
    st.stop()

# Convertir a DataFrame
bank_data = api_client.bank_data_to_dataframe(bank_response)
stats = bank_response.get("stats", {})
is_percentage = bank_response.get("is_percentage", False)
unit = bank_response.get("unit", "$")

# Datos del ranking
with st.spinner(f"🔄 Cargando ranking de {selected_indicator}..."):
    ranking_response = api_client.get_ranking(selected_indicator, categoria,None)

ranking_df = pd.DataFrame()
if ranking_response:
    ranking_df = api_client.ranking_to_dataframe(ranking_response)

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.metric("🏦 Bancos", len(bancos))

with col_b:
    st.metric("📊 Indicadores", len(indicadores))

with col_c:
    if is_percentage:
        st.metric("📊 Suma Total", f"{stats.get('total', 0):.2f}%")
    else:
        st.metric("💵 Suma Total", f"${stats.get('total', 0):,.0f}")

with col_d:
    if is_percentage:
        st.metric("📈 Promedio", f"{stats.get('promedio', 0):.2f}%")
    else:
        st.metric("📈 Promedio", f"${stats.get('promedio', 0):,.2f}")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Perfil Banco",
    "🏆 Ranking",
    "📊 Comparativa",
    "🔥 Análisis Visual",
    "📈 Estadísticas"
])

# Inicializar componentes UI
ui = UIComponents()
builder = ChartBuilder(is_percentage, unit)

with tab1:
    st.subheader(f"📈 Perfil Financiero: {selected_bank}")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        if not bank_data.empty:
            # Crear visualización
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
            
            # Obtener max y min
            max_idx = bank_data["valor_indicador"].idxmax()
            min_idx = bank_data["valor_indicador"].idxmin()
            
            nombre_max = bank_data.loc[max_idx, "nombre_del_indicador"]
            valor_max = bank_data.loc[max_idx, "valor_indicador"]
            
            nombre_min = bank_data.loc[min_idx, "nombre_del_indicador"]
            valor_min = bank_data.loc[min_idx, "valor_indicador"]
            
            # Formatear valores
            if is_percentage:
                valor_max_fmt = f"{valor_max:.2f}%"
                valor_min_fmt = f"{valor_min:.2f}%"
            else:
                valor_max_fmt = f"${valor_max:,.0f}"
                valor_min_fmt = f"${valor_min:,.0f}"
            
            # Truncar nombres
            nombre_max_short = nombre_max[:30] + "..." if len(nombre_max) > 30 else nombre_max
            nombre_min_short = nombre_min[:30] + "..." if len(nombre_min) > 30 else nombre_min
            
            st.metric("🔝 Indicador Mayor", valor_max_fmt, nombre_max_short)
            st.metric("🔻 Indicador Menor", valor_min_fmt, nombre_min_short)
            
            st.markdown("---")
            st.markdown("### 📊 Estadísticas")
            
            if is_percentage:
                st.metric("📊 Promedio", f"{stats.get('promedio', 0):.2f}%")
                st.metric("📏 Desviación", f"{stats.get('desviacion', 0):.2f}%")
            else:
                st.metric("📊 Promedio", f"${stats.get('promedio', 0):,.0f}")
                st.metric("📏 Desviación", f"${stats.get('desviacion', 0):,.0f}")

with tab2:
    st.subheader(f"🏆 Ranking: {selected_indicator}")
    
    if not ranking_df.empty:
        col_chart, col_top = st.columns([2, 1])
        
        with col_chart:
            fig2 = builder.create_ranking_chart(
                df=ranking_df,
                title=f"Ranking: {selected_indicator}",
                figsize=(12, 8)
            )
            st.pyplot(fig2)
        
        with col_top:
            st.markdown("### 🎖️ Top 3")
            
            ui.render_top3_medals(
                df=ranking_df,
                bank_col="banks",
                value_col="valor_indicador",
                is_percentage=is_percentage
            )
            
            st.markdown("---")
            st.markdown("### 📉 Bottom 3")
            
            ui.render_bottom3(
                df=ranking_df,
                n=3,
                bank_col="banks",
                value_col="valor_indicador",
                is_percentage=is_percentage
            )
    else:
        st.warning("No hay datos disponibles para este indicador.")

with tab3:
    st.subheader(f"📊 Comparativa: {categoria}")
    
    # Obtener tabla comparativa desde API
    with st.spinner("🔄 Cargando tabla comparativa..."):
        comparative_response = api_client.get_comparative_table(categoria)#type:ignore
    
    if comparative_response:
        pivot_df = api_client.comparative_to_dataframe(comparative_response)
        
        if not pivot_df.empty:
            # Aplicar formato
            if is_percentage:
                styled_df = (
                    pivot_df.style
                    .format("{:.2f}%")
                    .background_gradient(cmap="YlGnBu", axis=0)#type:ignore
                    .set_properties(**{'text-align': 'right'})
                )
            else:
                styled_df = (
                    pivot_df.style
                    .format("${:,.0f}")
                    .background_gradient(cmap="YlGnBu", axis=0)#type:ignore
                    .set_properties(**{'text-align': 'right'})
                )
            
            st.dataframe(styled_df, use_container_width=True, height=500)
            
            st.markdown("---")
            
            col_down1, col_down2, col_down3 = st.columns([1, 1, 2])
            with col_down1:
                ui.render_download_button(
                    df=pivot_df,
                    filename=f'comparativa_{categoria.lower()}.csv',
                    label="📥 Descargar CSV"
                )
            
            with col_down2:
                st.metric("📊 Bancos", len(pivot_df))
            
            with col_down3:
                st.metric("📈 Indicadores", len(pivot_df.columns))
        else:
            st.warning("No se pudo generar la tabla comparativa.")
    else:
        st.error("Error al cargar datos comparativos")

with tab4:
    st.subheader("🔥 Análisis Visual Comparativo")
    
    if comparative_response and not pivot_df.empty:#type:ignore
        col_slider, col_info = st.columns([2, 1])
        
        with col_slider:
            top_n = st.slider("¿Cuántos bancos mostrar?", 5, len(bancos), 10)
        
        with col_info:
            st.info(f"📊 Mostrando top {top_n} bancos")
        
        # Top bancos
        pivot_sorted = pivot_df.sum(axis=1).sort_values(ascending=False).head(top_n)#type:ignore
        top_bancos = pivot_sorted.index.tolist()
        pivot_top = pivot_df.loc[top_bancos]#type:ignore
        
        # Heatmap
        fig3 = builder.create_heatmap(
            pivot_df=pivot_top,
            title=f"Mapa de Calor: Top {top_n} Bancos - {categoria}",
            figsize=(14, 8),
            normalize=True
        )
        st.pyplot(fig3)
        
        st.markdown("---")
        st.subheader("🏦 Comparación Personalizada")
        
        default_banks = bancos[:3] if len(bancos) >= 3 else bancos
        bancos_comparar = st.multiselect(
            "Selecciona bancos para comparar",
            bancos,
            default=default_banks
        )
        
        if bancos_comparar:
            # Filtrar pivot por bancos seleccionados
            if all(b in pivot_df.index for b in bancos_comparar): #type:ignore
                pivot_comp = pivot_df.loc[bancos_comparar] #type:ignore
                
                if is_percentage:
                    st.dataframe(
                        pivot_comp.style
                        .format("{:.2f}%")
                        .background_gradient(cmap="RdYlGn", axis=1)
                        .set_properties(**{'text-align': 'right'}),
                        use_container_width=True
                    )
                else:
                    st.dataframe(
                        pivot_comp.style
                        .format("${:,.0f}")
                        .background_gradient(cmap="RdYlGn", axis=1)
                        .set_properties(**{'text-align': 'right'}),
                        use_container_width=True
                    )
                
                col_btn1, col_btn2 = st.columns([1, 3])
                with col_btn1:
                    ui.render_download_button(
                        df=pivot_comp,
                        filename=f'comparacion_bancos_{categoria.lower()}.csv',
                        label="📥 Descargar"
                    )
    else:
        st.warning("No hay datos suficientes para análisis visual")

with tab5:
    st.subheader(f"📈 Estadísticas Globales - {categoria}")
    
    # Obtener estadísticas desde API
    with st.spinner("🔄 Cargando estadísticas..."):
        stats_response = api_client.get_comparative_statistics(categoria)
    
    if stats_response:
        global_stats = stats_response.get("global_stats", {})
        stats_by_bank = stats_response.get("stats_by_bank", {})
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if is_percentage:
                st.metric("📊 Promedio", f"{global_stats.get('promedio', 0):.2f}%")
                st.metric("📊 Mediana", f"{global_stats.get('mediana', 0):.2f}%")
            else:
                st.metric("📊 Promedio", f"${global_stats.get('promedio', 0):,.2f}")
                st.metric("📊 Mediana", f"${global_stats.get('mediana', 0):,.2f}")
        
        with col2:
            if is_percentage:
                st.metric("⬆️ Máximo", f"{global_stats.get('max', 0):.2f}%")
                st.metric("⬇️ Mínimo", f"{global_stats.get('min', 0):.2f}%")
            else:
                st.metric("⬆️ Máximo", f"${global_stats.get('max', 0):,.0f}")
                st.metric("⬇️ Mínimo", f"${global_stats.get('min', 0):,.0f}")
        
        with col3:
            rango = global_stats.get('max', 0) - global_stats.get('min', 0)
            if is_percentage:
                st.metric("📏 Rango", f"{rango:.2f}%")
                st.metric("📏 Desv. Estándar", f"{global_stats.get('desviacion', 0):.2f}%")
            else:
                st.metric("📏 Rango", f"${rango:,.0f}")
                st.metric("📏 Desv. Estándar", f"${global_stats.get('desviacion', 0):,.2f}")
        
        with col4:
            coef_var = (global_stats.get('desviacion', 0) / global_stats.get('promedio', 1) * 100)
            st.metric("📊 Coef. Variación", f"{coef_var:.2f}%")
            
            if is_percentage:
                st.metric("💯 Total", f"{global_stats.get('total', 0):.2f}%")
            else:
                st.metric("💵 Total", f"${global_stats.get('total', 0):,.0f}")
        
        st.markdown("---")
        st.subheader("📊 Distribución por Banco")
        
        # Convertir stats por banco a DataFrame
        if stats_by_bank:
            df_stats = pd.DataFrame.from_dict(stats_by_bank, orient='index')
            df_stats = df_stats.sort_values('total', ascending=False)
            
            if is_percentage:
                st.dataframe(
                    df_stats.style
                    .format({
                        'promedio': '{:.2f}%',
                        'total': '{:.2f}%',
                        'cantidad': '{:.0f}',
                        'desviacion': '{:.2f}%'
                    })
                    .background_gradient(subset=['total'], cmap='Blues') #type:ignore
                    .set_properties(**{'text-align': 'right'}),
                    use_container_width=True,
                    height=400
                )
            else:
                st.dataframe(
                    df_stats.style
                    .format({
                        'promedio': '${:,.2f}',
                        'total': '${:,.0f}',
                        'cantidad': '{:.0f}',
                        'desviacion': '${:,.2f}'
                    })
                    .background_gradient(subset=['total'], cmap='Blues') #type:ignore
                    .set_properties(**{'text-align': 'right'}),
                    use_container_width=True,
                    height=400
                )
            
            col_stats1, col_stats2 = st.columns([1, 3])
            with col_stats1:
                ui.render_download_button(
                    df=df_stats,
                    filename=f'estadisticas_{categoria.lower()}.csv',
                    label="📥 Descargar"
                )
    else:
        st.error("No se pudieron cargar las estadísticas")

st.markdown("---")

st.caption("Desarrollado por Grupo 5 — Proyecto Integrador 2025")
st.caption("Dashboard de Salud Financiera - Sistema Bancario Ecuatoriano")
st.caption("Datos: Superintendencia de Bancos - Septiembre 2025")
st.caption(f"API Backend: {api_client.base_url}")
