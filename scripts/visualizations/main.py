from typing import List, Optional

from services.api_client import  get_api_client
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 🔧 CONFIGURACIÓN INICIAL
# =========================================================
st.set_page_config(
    page_title="Dashboard de Salud Financiera",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# 🔗 CONEXIÓN CON API
# =========================================================
@st.cache_resource
def init_api_connection():
    """Inicializa conexión con la API"""
    try:
        client = get_api_client()
        # Test de conexión
        test = client.get_banks_list("Balance")
        if test:
            return client, True
        return client, False
    except Exception as e:
        st.error(f"Error conectando con API: {e}")
        return None, False

api_client, api_connected = init_api_connection()

if not api_connected or api_client is None:
    st.error("❌ No se pudo conectar con la API. Verifica que el servidor esté corriendo.")
    st.info("💡 Inicia el servidor con: `uvicorn main:app --reload`")
    st.stop()

# =========================================================
# 📁 FUNCIONES DE CARGA DE DATOS
# =========================================================
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_system_overview():
    """Carga resumen general del sistema"""
    try:
        return api_client.get_system_overview()
    except Exception as e:
        st.error(f"Error cargando overview: {e}")
        return None

@st.cache_data(ttl=300)
def load_banks_list(category: str = "Balance"):
    """Carga lista de bancos"""
    try:
        return api_client.get_banks_list(category)
    except Exception as e:
        st.error(f"Error cargando bancos: {e}")
        return []

@st.cache_data(ttl=300)
def load_indicators_list(category: str):
    """Carga lista de indicadores"""
    try:
        response = api_client.get_indicators_list(category)
        return response.get("indicators", []) if response else []
    except Exception as e:
        st.error(f"Error cargando indicadores: {e}")
        return []

@st.cache_data(ttl=300)
def load_comparative_table(category: str, banks: Optional[List[str]] = None):
    """Carga tabla comparativa"""
    try:
        response = api_client.get_comparative_table(category, banks)
        if response and "data" in response:
            return pd.DataFrame.from_dict(response["data"], orient='index')
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando tabla comparativa: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_ranking(kpi: str, category: str, ascending: bool = False):
    """Carga ranking de bancos"""
    try:
        response = api_client.get_ranking(kpi, category, ascending)
        if response and "ranking" in response:
            return pd.DataFrame(response["ranking"])
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando ranking: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_bank_financials(bank_name: str, category: str):
    """Carga datos financieros de un banco"""
    try:
        response = api_client.get_bank_financials(bank_name, category)
        if response and "data" in response:
            return pd.DataFrame(response["data"]), response
        return pd.DataFrame(), None
    except Exception as e:
        st.error(f"Error cargando datos del banco: {e}")
        return pd.DataFrame(), None

@st.cache_data(ttl=300)
def load_alerts():
    """Carga alertas del sistema"""
    try:
        return api_client.get_system_alerts()
    except Exception as e:
        st.error(f"Error cargando alertas: {e}")
        return None

@st.cache_data(ttl=300)
def load_concentration(metric: str = "TOTAL ACTIVO"):
    """Carga análisis de concentración"""
    try:
        return api_client.get_market_concentration(metric)
    except Exception as e:
        st.error(f"Error cargando concentración: {e}")
        return None

@st.cache_data(ttl=300)
def load_peer_groups(size_metric: str = "TOTAL ACTIVO"):
    """Carga peer groups"""
    try:
        return api_client.get_peer_groups(size_metric)
    except Exception as e:
        st.error(f"Error cargando peer groups: {e}")
        return None

@st.cache_data(ttl=300)
def load_correlations():
    """Carga matriz de correlaciones"""
    try:
        return api_client.get_correlations()
    except Exception as e:
        st.error(f"Error cargando correlaciones: {e}")
        return None

@st.cache_data(ttl=300)
def load_benchmark_analysis(bank_name: str, benchmark_type: str = "system_average"):
    """Carga análisis de benchmark"""
    try:
        return api_client.get_benchmark_analysis(bank_name, benchmark_type)
    except Exception as e:
        st.error(f"Error cargando benchmark: {e}")
        return None

# =========================================================
# 🎨 ENCABEZADO
# =========================================================
st.title("💰 Dashboard de Salud Financiera Bancaria")
st.markdown("""
**Análisis integral del Sistema Bancario Ecuatoriano**  
Dashboard interactivo para evaluar indicadores de Balance, Rendimiento y Estructura Financiera.
""")

# =========================================================
# 📑 PESTAÑAS PRINCIPALES
# =========================================================
tab_overview, tab_categoria, tab_especifico = st.tabs([
    "📊 Overview General", 
    "🎯 Análisis por Categoría", 
    "🏦 Análisis Específico por Banco"
])

# =========================================================
# 🔧 SIDEBAR - Panel de Control
# =========================================================
with st.sidebar:
    st.header("🔍 Panel de Control")
    
    # Estado de conexión
    st.subheader("🔗 Estado del Sistema")
    if api_connected:
        st.success("✅ API Conectado")
        st.caption(f"🌐 {api_client.base_url}")
        if st.button("🔄 Recargar Datos"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    
    # Cargar overview básico
    overview_data = load_system_overview()
    
    if overview_data:
        gen_stats = overview_data.get("general_statistics", {})
        st.caption(f"🏦 **Total Bancos:** {gen_stats.get('total_banks', 'N/D')}")
        st.caption(f"📊 **Total Indicadores:** {gen_stats.get('total_indicators', 'N/D')}")
        st.caption(f"📅 **Periodo:** Septiembre 2025")

# =========================================================
# 📊 TAB 1: OVERVIEW GENERAL
# =========================================================
with tab_overview:
    st.header("📊 Overview General del Sistema Bancario")
    st.markdown("**Vista panorámica de todos los indicadores y bancos del sistema**")
    
    # Cargar datos del overview
    overview = load_system_overview()
    
    if overview:
        gen_stats = overview.get("general_statistics", {})
        concentration = overview.get("concentration", {})
        alerts_summary = overview.get("alerts", {})
        top_performers = overview.get("top_performers", {})
        
        # =========================================================
        # 📈 ESTADÍSTICAS GENERALES
        # =========================================================
        st.subheader("📈 Estadísticas Generales del Sistema")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🏦 Total Bancos",
                f"{gen_stats.get('total_banks', 0)}",
                "en el sistema"
            )
        
        with col2:
            st.metric(
                "📊 Total Indicadores",
                f"{gen_stats.get('total_indicators', 0)}",
                "métricas disponibles"
            )
        
        with col3:
            activos_sistema = gen_stats.get('total_assets_system', 0)
            st.metric(
                "💰 Activos Sistema",
                f"${activos_sistema:,.0f}",
                "total del sistema"
            )
        
        with col4:
            roe_promedio = gen_stats.get('average_roe', 0)
            st.metric(
                "📈 ROE Promedio",
                f"{roe_promedio:.2f}%",
                "rentabilidad sistema"
            )
        
        st.markdown("---")
        
        # =========================================================
        # 🎯 CONCENTRACIÓN DEL MERCADO
        # =========================================================
        st.subheader("🎯 Análisis de Concentración del Mercado")
        
        col_conc1, col_conc2 = st.columns([2, 1])
        
        with col_conc1:
            hhi = concentration.get('hhi', 0)
            conc_level = concentration.get('concentration_level', 'N/D')
            
            st.metric(
                "📊 Índice HHI",
                f"{hhi:.0f}",
                f"Concentración: {conc_level}"
            )
            
            # Interpretación
            if hhi < 1500:
                st.success("✅ Mercado no concentrado (HHI < 1500)")
            elif hhi < 2500:
                st.warning("⚠️ Mercado moderadamente concentrado (1500 ≤ HHI < 2500)")
            else:
                st.error("🚨 Mercado altamente concentrado (HHI ≥ 2500)")
        
        with col_conc2:
            # Cargar datos detallados de concentración
            conc_data = load_concentration("TOTAL ACTIVO")
            if conc_data and 'top_banks' in conc_data:
                st.markdown("**🏆 Top 5 Participación**")
                for i, bank in enumerate(conc_data['top_banks'][:5]):
                    bank_name = bank.get('banks', 'N/D')
                    valor = bank.get('valor_indicador', 0)
                    st.caption(f"{i+1}. {bank_name[:15]}: ${valor:,.0f}")
        
        st.markdown("---")
        
        # =========================================================
        # 🏆 TOP PERFORMERS
        # =========================================================
        st.subheader("🏆 Top Performers del Sistema")
        
        col_top1, col_top2 = st.columns(2)
        
        with col_top1:
            st.markdown("**💰 Top 5 por Activos**")
            by_assets = top_performers.get('by_assets', [])
            
            if by_assets:
                # Crear dataframe para gráfico
                df_assets = pd.DataFrame(by_assets)
                
                fig1 = px.bar(
                    df_assets,
                    x='banks',
                    y='valor_indicador',
                    title="Top 5 Bancos por Activos Totales",
                    color='valor_indicador',
                    color_continuous_scale='Blues',
                    labels={'valor_indicador': 'Activos ($)', 'banks': 'Bancos'}
                )
                fig1.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_top2:
            st.markdown("**📈 Top 5 por ROE**")
            by_roe = top_performers.get('by_roe', [])
            
            if by_roe:
                df_roe = pd.DataFrame(by_roe)
                
                fig2 = px.bar(
                    df_roe,
                    x='banks',
                    y='valor_indicador',
                    title="Top 5 Bancos por ROE (%)",
                    color='valor_indicador',
                    color_continuous_scale='Greens',
                    labels={'valor_indicador': 'ROE (%)', 'banks': 'Bancos'}
                )
                fig2.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        # =========================================================
        # 🏦 PEER GROUPS
        # =========================================================
        st.subheader("🏦 Distribución por Tamaño de Bancos")
        
        peer_data = load_peer_groups("TOTAL ACTIVO")
        
        if peer_data and 'groups' in peer_data:
            col_pie, col_details = st.columns([2, 1])
            
            with col_pie:
                distribution = peer_data.get('distribution', {})
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(distribution.keys()),
                    values=list(distribution.values()),
                    hole=0.3,
                    textinfo='label+percent'
                )])
                fig_pie.update_layout(title="Distribución de Bancos por Tamaño")
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_details:
                st.markdown("**📋 Detalle por Grupo**")
                groups = peer_data.get('groups', {})
                for group_name, banks_list in groups.items():
                    with st.expander(f"{group_name} ({len(banks_list)})"):
                        for bank in banks_list[:10]:  # Limitar a 10
                            st.write(f"• {bank}")
        
        st.markdown("---")
        
        # =========================================================
        # 🔗 CORRELACIONES
        # =========================================================
        st.subheader("🔗 Análisis de Correlaciones entre Indicadores")
        
        corr_data = load_correlations()
        
        if corr_data and 'correlation_matrix' in corr_data:
            corr_matrix = pd.DataFrame(corr_data['correlation_matrix'])
            
            col_heatmap, col_insights = st.columns([3, 1])
            
            with col_heatmap:
                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.index,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.round(2).values,
                    texttemplate="%{text}",
                    textfont={"size": 10},
                    colorbar=dict(title="Correlación")
                ))
                
                fig_corr.update_layout(
                    title="Matriz de Correlación - Indicadores Principales",
                    xaxis_tickangle=-45,
                    height=500
                )
                
                st.plotly_chart(fig_corr, use_container_width=True)
            
            with col_insights:
                st.markdown("**🧠 Correlaciones Destacadas**")
                
                strong_corr = corr_data.get('strong_correlations', [])
                if strong_corr:
                    for corr in strong_corr[:5]:
                        ind1 = corr['indicator1'][:15]
                        ind2 = corr['indicator2'][:15]
                        val = corr['correlation']
                        st.metric(
                            f"{ind1}... × {ind2}...",
                            f"{val:.2f}",
                            corr['strength']
                        )
                else:
                    st.info("No hay correlaciones fuertes")
        
        st.markdown("---")
        
        # =========================================================
        # 🚨 ALERTAS DEL SISTEMA
        # =========================================================
        st.subheader("🚨 Alertas del Sistema")
        
        alerts = load_alerts()
        
        if alerts:
            col_alert1, col_alert2, col_alert3 = st.columns(3)
            
            with col_alert1:
                st.metric(
                    "🔴 Alertas Críticas",
                    alerts.get('critical_count', 0),
                    "requieren atención inmediata"
                )
            
            with col_alert2:
                st.metric(
                    "🟠 Alertas Altas",
                    alerts.get('high_count', 0),
                    "monitorear de cerca"
                )
            
            with col_alert3:
                st.metric(
                    "🟡 Alertas Medias",
                    alerts.get('medium_count', 0),
                    "seguimiento normal"
                )
            
            # Mostrar alertas críticas
        alert_list = alerts.get("alerts", [])

        # Filtrar solo las críticas
        critical_alerts = [a for a in alert_list if a.get("severidad") == "🔴 CRÍTICA"]

        if critical_alerts:
            st.markdown("**🔴 Alertas Críticas Activas:**")
            for alert in critical_alerts[:5]:  # Mostrar primeras 5
                st.error(f"🚨 {alert.get('descripcion', 'N/D')}")
                
                # Mostrar detalles opcionales
                st.caption(f"🏦 Banco: {alert.get('banco', 'N/D')}")
                st.caption(f"📊 Indicador: {alert.get('indicador', 'N/D')}")
                st.caption(f"📉 Valor: {alert.get('valor', 'N/D')}")

# =========================================================
# 🎯 TAB 2: ANÁLISIS POR CATEGORÍA
# =========================================================
with tab_categoria:
    st.header("🎯 Análisis por Categoría Específica")
    
    # Selector de categoría
    categoria = st.selectbox(
        "📈 Selecciona Categoría de Análisis:",
        ["Balance", "Rendimiento", "Estructura"],
        help="Análisis detallado por tipo de indicadores"
    )
    
    # Mostrar info según categoría
    if categoria == "Balance":
        st.info("💼 **Balance:** Activos y recursos del banco")
    elif categoria == "Rendimiento":
        st.info("📊 **Rendimiento:** Rentabilidad y eficiencia")
    else:
        st.info("🏗️ **Estructura:** Composición financiera")
    
    # Cargar indicadores de la categoría
    indicadores = load_indicators_list(categoria)
    bancos = load_banks_list(categoria)
    
    if not indicadores:
        st.error("No hay indicadores disponibles para esta categoría")
        st.stop()
    
    # =========================================================
    # 📊 MÉTRICAS DE LA CATEGORÍA
    # =========================================================
    st.subheader(f"📊 Estadísticas de {categoria}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏦 Total Bancos", len(bancos))
    
    with col2:
        st.metric("📊 Total Indicadores", len(indicadores))
    
    with col3:
        # Cargar tabla comparativa para estadísticas
        comp_df = load_comparative_table(categoria)
        if not comp_df.empty:
            st.metric("📋 Datos Disponibles", f"{len(comp_df) * len(comp_df.columns)}")
    
    st.markdown("---")
    
    # =========================================================
    # 🏆 RANKINGS DINÁMICOS
    # =========================================================
    st.subheader(f"🏆 Rankings Dinámicos - {categoria}")
    
    selected_indicator = st.selectbox(
        "📊 Selecciona Indicador para Ranking:",
        indicadores,
        help="Elige qué indicador quieres analizar"
    )
    
    # Cargar ranking
    ranking_df = load_ranking(selected_indicator, categoria, ascending=False)
    
    if not ranking_df.empty:
        col_chart, col_metrics = st.columns([3, 1])
        
        with col_chart:
            fig_rank = px.bar(
                ranking_df.head(10),
                x='banks',
                y='valor_indicador',
                title=f"Top 10 - {selected_indicator}",
                color='valor_indicador',
                color_continuous_scale='viridis',
                labels={'valor_indicador': selected_indicator, 'banks': 'Bancos'}
            )
            fig_rank.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig_rank, use_container_width=True)
        
        with col_metrics:
            st.markdown("**🎖️ Top 3**")
            
            for i, row in ranking_df.head(3).iterrows():
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}" #type:ignore
                st.metric(
                    f"{medal} {row['banks'][:15]}",
                    f"{row['valor_indicador']:.2f}"
                )
    
    st.markdown("---")
    
    # =========================================================
    # 📋 TABLA COMPARATIVA
    # =========================================================
    st.subheader(f"📊 Matriz Comparativa - {categoria}")
    
    pivot_df = load_comparative_table(categoria)
    
    if not pivot_df.empty:
        # Aplicar formato
        styled_df = (
            pivot_df.style
            .format("{:.2f}")
            .background_gradient(cmap="RdYlGn", axis=0)
            .set_properties(**{'text-align': 'right'})
        )
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Descarga
        csv = pivot_df.to_csv()
        st.download_button(
            label="📥 Descargar Matriz CSV",
            data=csv,
            file_name=f'matriz_{categoria.lower()}.csv',
            mime='text/csv'
        )

# =========================================================
# 🏦 TAB 3: ANÁLISIS ESPECÍFICO POR BANCO
# =========================================================
with tab_especifico:
    st.header("🏦 Análisis Específico por Banco")
    st.markdown("**Análisis individual detallado con comparaciones específicas**")
    
    # Cargar lista de bancos
    bancos_disponibles = load_banks_list("Balance")
    
    if not bancos_disponibles:
        st.error("No hay bancos disponibles")
        st.stop()
    
    selected_bank = st.selectbox(
        "🏦 Selecciona Banco para Análisis:",
        bancos_disponibles,
        help="Escoge un banco para análisis detallado"
    )
    
    if selected_bank:
        # Cargar datos de las 3 categorías
        balance_df, balance_info = load_bank_financials(selected_bank, "Balance")
        rendimiento_df, rend_info = load_bank_financials(selected_bank, "Rendimiento")
        estructura_df, estr_info = load_bank_financials(selected_bank, "Estructura")
        
        # =========================================================
        # 📊 RESUMEN EJECUTIVO
        # =========================================================
        st.subheader(f"📊 Resumen Ejecutivo: {selected_bank}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ind = 0
            if balance_info:
                total_ind += balance_info.get('total_indicators', 0)
            if rend_info:
                total_ind += rend_info.get('total_indicators', 0)
            if estr_info:
                total_ind += estr_info.get('total_indicators', 0)
            st.metric("📊 Indicadores", total_ind)
        
        with col2:
            # Buscar activos totales
            if not estructura_df.empty:
                activo_row = estructura_df[estructura_df['nombre_del_indicador'] == 'TOTAL ACTIVO']
                if not activo_row.empty:
                    activo_val = activo_row['valor_indicador'].iloc[0]
                    st.metric("💰 Activos", f"${activo_val:,.0f}")
                else:
                    st.metric("💰 Activos", "N/D")
            else:
                st.metric("💰 Activos", "N/D")
        
        with col3:
            # Buscar ROE
            if not rendimiento_df.empty:
                roe_row = rendimiento_df[rendimiento_df['nombre_del_indicador'].str.contains('PATRIMONIO PROMEDIO', na=False)]
                if not roe_row.empty:
                    roe_val = roe_row['valor_indicador'].iloc[0]
                    st.metric("📈 ROE", f"{roe_val:.2f}%")
                else:
                    st.metric("📈 ROE", "N/D")
        
        with col4:
            # Posición en ranking
            ranking_activos = load_ranking("TOTAL ACTIVO", "Estructura", False)
            if not ranking_activos.empty:
                posicion = ranking_activos.index[ranking_activos['banks'] == selected_bank].tolist()
                if posicion:
                    st.metric("🏆 Ranking Activos", f"#{posicion[0] + 1}")
                else:
                    st.metric("🏆 Ranking Activos", "N/D")
        
        st.markdown("---")
        
        # =========================================================
        # 📈 ANÁLISIS POR CATEGORÍA DEL BANCO
        # =========================================================
        st.subheader(f"📈 Análisis Financiero: {selected_bank}")
        
        tab_bal, tab_rend, tab_estr = st.tabs(["💼 Balance", "📊 Rendimiento", "🏗️ Estructura"])
        
        with tab_bal:
            if not balance_df.empty:
                st.markdown("**💼 Indicadores de Balance**")
                
                # Gráfico de barras
                fig = px.bar(
                    balance_df.head(10),
                    x='nombre_del_indicador',
                    y='valor_indicador',
                    title="Principales Indicadores de Balance",
                    color='valor_indicador',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.dataframe(
                    balance_df.style.format({'valor_indicador': '{:,.2f}'}),
                    use_container_width=True
                )
            else:
                st.info("No hay datos de Balance disponibles")
        
        with tab_rend:
            if not rendimiento_df.empty:
                st.markdown("**📊 Indicadores de Rendimiento**")
                
                fig = px.bar(
                    rendimiento_df.head(10),
                    x='nombre_del_indicador',
                    y='valor_indicador',
                    title="Principales Indicadores de Rendimiento",
                    color='valor_indicador',
                    color_continuous_scale='Greens'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(
                    rendimiento_df.style.format({'valor_indicador': '{:,.2f}'}),
                    use_container_width=True
                )
            else:
                st.info("No hay datos de Rendimiento disponibles")
        
        with tab_estr:
            if not estructura_df.empty:
                st.markdown("**🏗️ Indicadores de Estructura**")
                
                fig = px.bar(
                    estructura_df.head(10),
                    x='nombre_del_indicador',
                    y='valor_indicador',
                    title="Principales Indicadores de Estructura",
                    color='valor_indicador',
                    color_continuous_scale='Purples'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(
                    estructura_df.style.format({'valor_indicador': '{:,.2f}'}),
                    use_container_width=True
                )
            else:
                st.info("No hay datos de Estructura disponibles")
        
        st.markdown("---")
        
        # =========================================================
        # 🔍 COMPARACIÓN CON BENCHMARKS
        # =========================================================
        st.subheader(f"🔍 {selected_bank} vs. Benchmarks del Sistema")
        
        benchmark_type = st.selectbox(
            "Tipo de Benchmark:",
            ["system_average", "top_quartile", "median"],
            format_func=lambda x: {
                "system_average": "Promedio del Sistema",
                "top_quartile": "Top 25%",
                "median": "Mediana del Sistema"
            }[x]
        )
        
        benchmark_data = load_benchmark_analysis(selected_bank, benchmark_type)
        
        if benchmark_data and 'comparisons' in benchmark_data:
            comparisons = benchmark_data['comparisons']
            
            # Crear dataframe para visualización
            bench_list = []
            for indicator, values in comparisons.items():
                bench_list.append({
                    'Indicador': indicator,
                    'Banco': values['valor_banco'],
                    'Benchmark': values['valor_benchmark'],
                    'Diferencia (%)': values['desviacion_relativa_pct'],
                    'Posición': values['posicion']
                })
            
            if bench_list:
                bench_df = pd.DataFrame(bench_list)
                
                col_chart, col_table = st.columns([2, 1])
                
                with col_chart:
                    # Gráfico de comparación
                    fig_bench = go.Figure()
                    
                    fig_bench.add_trace(go.Bar(
                        name=selected_bank,
                        x=[ind[:20] + "..." for ind in bench_df['Indicador']],
                        y=bench_df['Diferencia (%)'],
                        marker_color=['green' if x > 0 else 'red' for x in bench_df['Diferencia (%)']]
                    ))
                    
                    fig_bench.update_layout(
                        title=f"Diferencia vs {benchmark_type.replace('_', ' ').title()} (%)",
                        xaxis_title="Indicadores",
                        yaxis_title="Diferencia (%)",
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_bench, use_container_width=True)
                
                with col_table:
                    st.markdown("**📊 Análisis de Posición**")
                    
                    # Analizar fortalezas y debilidades
                    fortalezas = bench_df[bench_df['Diferencia (%)'] > 5]
                    debilidades = bench_df[bench_df['Diferencia (%)'] < -5]
                    
                    if not fortalezas.empty:
                        st.success(f"**🟢 Fortalezas ({len(fortalezas)})**")
                        for _, row in fortalezas.head(3).iterrows():
                            st.write(f"• {row['Indicador'][:25]}...")
                    
                    if not debilidades.empty:
                        st.warning(f"**🔴 Áreas de Mejora ({len(debilidades)})**")
                        for _, row in debilidades.head(3).iterrows():
                            st.write(f"• {row['Indicador'][:25]}...")
                    
                    if fortalezas.empty and debilidades.empty:
                        st.info("📊 **Rendimiento equilibrado** con el benchmark")
                
                # Tabla detallada
                st.dataframe(
                    bench_df.style.format({
                        'Banco': '{:.2f}',
                        'Benchmark': '{:.2f}',
                        'Diferencia (%)': '{:.1f}%'
                    }).background_gradient(subset=['Diferencia (%)'], cmap='RdYlGn'),
                    use_container_width=True
                )
        else:
            st.info("No hay datos de benchmark disponibles para este banco")

# =========================================================
# 📊 PIE DE PÁGINA
# =========================================================
st.markdown("---")
st.caption("📊 Desarrollado por Grupo 5 — Proyecto Integrador 2025")
st.caption("💡 Dashboard de Salud Financiera - Sistema Bancario Ecuatoriano")
st.caption("📅 Datos: Superintendencia de Bancos - Septiembre 2025")
st.caption("🔗 Powered by FastAPI + Streamlit")
