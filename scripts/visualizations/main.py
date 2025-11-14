from components.indicator_config import IndicatorConfig
from components.data_handler import DataHandler
from components.metrics_calculator import MetricsCalculator
from components.charts_builder import ChartBuilder
from components.ui_components import UIComponents
from components.advanced_metrics import AdvancedMetrics
from components.analysis_engine import TrendAnalysis, AlertRenderer

from data_loader import VisualizationDataLoader 
from services.api_client import BankApiClient, get_api_client
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
# 🔌 CONFIGURACIÓN DE API CLIENT
# =========================================================
# Sidebar para configurar conexión a API
with st.sidebar:
    st.header("🔌 Configuración API")
    
    # Toggle para usar API o datos locales
    use_api = st.toggle("🌐 Usar API REST", value=False, help="Activar para consumir datos desde la API")
    
    if use_api:
        api_base_url = st.text_input(
            "🔗 URL Base API",
            value="http://localhost:8000",
            help="URL del servidor FastAPI"
        )
        
        # Inicializar cliente API
        try:
            api_client = get_api_client(api_base_url)
            st.success("✅ API Client conectado")
        except Exception as e:
            st.error(f"❌ Error al conectar API: {e}")
            use_api = False
    
    st.markdown("---")

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

# =========================================================
# 🔄 FUNCIÓN PARA CARGAR DATOS (API o Local)
# =========================================================
def load_data_source():
    """Carga datos desde API o fuente local según configuración"""
    if use_api:
        try:
            # Obtener overview desde API
            overview_data = api_client.get_system_overview()
            st.sidebar.info(f"📊 Datos API: {overview_data['general_statistics']['total_banks']} bancos")
            
            # Cargar datos locales para enriquecimiento
            df = dh.load_data("Final Dataframe")
            return df, True  # df, usando_api
        except Exception as e:
            st.sidebar.warning(f"⚠️ Error API, usando datos locales: {e}")
            df = dh.load_data("Final Dataframe")
            return df, False
    else:
        df = dh.load_data("Final Dataframe")
        return df, False

# Cargar datos
df, api_activa = load_data_source()

if df is None:
    st.error("❌ Error al cargar los datos")
    st.stop()

# =========================================================
# 🔧 ENRIQUECIMIENTO DE DATOS CON MÉTRICAS AVANZADAS
# =========================================================
@st.cache_data
def enrich_data_with_advanced_metrics(df):
    """Enriquece los datos con indicadores derivados y métricas avanzadas"""
    df_enriched = AdvancedMetrics.calculate_derived_indicators(df)
    df_final = AdvancedMetrics.calculate_composite_indices(df_enriched)
    return df_final

# Enriquecer datos
df = enrich_data_with_advanced_metrics(df)

# =========================================================
# 🎨 ENCABEZADO
# =========================================================
st.title("💰 Dashboard de Salud Financiera Bancaria")

# Mostrar badge de fuente de datos
if api_activa:
    st.success("🌐 **Modo:** Consumiendo datos desde API REST")
else:
    st.info("💾 **Modo:** Usando datos locales")

st.markdown("""
**Análisis integral del Sistema Bancario Ecuatoriano**  
Dashboard interactivo para evaluar indicadores de Balance, Rendimiento y Estructura Financiera.
""")

# =========================================================
# 📑 PESTAÑAS PRINCIPALES
# =========================================================
tab_overview, tab_categoria, tab_especifico, tab_api_advanced = st.tabs([
    "📊 Overview General", 
    "🎯 Análisis por Categoría", 
    "🏦 Análisis Específico por Banco",
    "🚀 API Analytics Avanzados"  # ✅ NUEVA PESTAÑA
])

# Configurar sidebar común
with st.sidebar:
    st.header("🔍 Panel de Control")
    st.markdown("---")
    
    total_bancos_sistema = df["banks"].nunique()
    total_indicadores_sistema = df["nombre_del_indicador"].nunique()
    
    st.caption(f"🏦 **Total Bancos:** {total_bancos_sistema}")
    st.caption(f"📊 **Total Indicadores:** {total_indicadores_sistema}")
    st.caption(f"📅 **Periodo:** Septiembre 2025")

# =========================================================
# 📊 TAB 1: OVERVIEW GENERAL (SIN CAMBIOS)
# =========================================================
with tab_overview:
    st.header("📊 Overview General del Sistema Bancario")
    st.markdown("**Vista panorámica de todos los indicadores y bancos del sistema**")
    
    calc = MetricsCalculator()
    ui = UIComponents()
    
    # ===== SECCIÓN: Estadísticas Generales =====
    st.subheader("📈 Estadísticas Generales del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏦 Total Bancos", f"{total_bancos_sistema}", "en el sistema")
    
    with col2:
        st.metric("📊 Total Indicadores", f"{total_indicadores_sistema}", "métricas disponibles")
    
    with col3:
        total_observaciones = len(df)
        st.metric("📋 Total Observaciones", f"{total_observaciones:,}", "registros de datos")
    
    with col4:
        completitud = ((df['valor_indicador'].notna().sum() / len(df)) * 100)
        st.metric("✅ Completitud de Datos", f"{completitud:.1f}%", "datos disponibles")
    
    st.markdown("---")
    
    # ===== SECCIÓN: Estadísticas Clave =====
    st.subheader("📊 Estadísticas Clave del Sistema")
    
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.markdown("**💰 Indicadores Financieros Principales**")
        
        activos_data = df[df['nombre_del_indicador'] == 'TOTAL ACTIVO']
        if not activos_data.empty:
            activos_sistema = activos_data['valor_indicador'].sum()
            st.metric("💰 Activos Totales Sistema", f"${activos_sistema:,.0f}")
        
        roe_sistema = df[df['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
        if not roe_sistema.empty:
            roe_promedio = roe_sistema['valor_indicador'].mean()
            st.metric("📈 ROE Promedio Sistema", f"{roe_promedio:.2f}%")
        
        roa_sistema = df[df['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO']
        if not roa_sistema.empty:
            roa_promedio = roa_sistema['valor_indicador'].mean()
            st.metric("📊 ROA Promedio Sistema", f"{roa_promedio:.2f}%")
    
    with col_stats2:
        st.markdown("**🏦 Concentración y Distribución**")
        
        if not activos_data.empty:
            top3_activos = activos_data.nlargest(3, 'valor_indicador')['valor_indicador'].sum()#type:ignore
            concentracion_top3 = (top3_activos / activos_sistema * 100) if activos_sistema > 0 else 0  #type:ignore
            st.metric("🏆 Concentración Top 3", f"{concentracion_top3:.1f}%")
        
        if not activos_data.empty:
            mediana_activos = activos_data['valor_indicador'].median()#type:ignore
            st.metric("📊 Banco Mediano (Activos)", f"${mediana_activos:,.0f}")
        
        if not roe_sistema.empty:
            cv_roe = (roe_sistema['valor_indicador'].std() / roe_sistema['valor_indicador'].mean() * 100)
            st.metric("📈 Variabilidad ROE", f"{cv_roe:.1f}%")
    
    st.markdown("---")
    
    # ===== SECCIÓN: Concentración =====
    st.subheader("🎯 Análisis de Concentración del Mercado")
    
    concentration_data = TrendAnalysis.calculate_concentration_risk(df)
    
    if concentration_data:
        col_conc1, col_conc2 = st.columns([2, 1])
        
        with col_conc1:
            hhi = concentration_data.get('hhi', 0)
            concentration_level = concentration_data.get('concentration_level', 'Desconocido')
            
            st.metric("📊 Índice HHI", f"{hhi:.0f}", f"Concentración: {concentration_level}")
            
            if hhi < 1500:
                st.success("✅ Mercado no concentrado (HHI < 1500)")
            elif hhi < 2500:
                st.warning("⚠️ Mercado moderadamente concentrado (1500 ≤ HHI < 2500)")
            else:
                st.error("🚨 Mercado altamente concentrado (HHI ≥ 2500)")
        
        with col_conc2:
            if 'top_banks' in concentration_data:
                st.markdown("**🏆 Top 5 Participación**")
                for i, bank_info in enumerate(concentration_data['top_banks'][:5]):#type:ignore
                    bank_name = bank_info['bank']
                    market_share = bank_info['market_share']
                    st.metric(f"{i+1}. {bank_name[:12]}...", f"{market_share:.1f}%", "participación")
    
    st.markdown("---")
    
    # ===== SECCIÓN: Top Performers =====
    st.subheader("🏆 Top Performers del Sistema")
    
    if not activos_data.empty:
        col_chart1, col_metrics1 = st.columns([3, 1])
        
        with col_chart1:
            top_activos = activos_data.nlargest(10, 'valor_indicador')#type:ignore
            
            fig1 = px.bar(
                top_activos,
                x='banks',
                y='valor_indicador',
                title="Top 10 Bancos por Activos Totales",
                labels={'valor_indicador': 'Activos Totales ($)', 'banks': 'Bancos'},
                color='valor_indicador',
                color_continuous_scale='Blues'
            )
            fig1.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_metrics1:
            st.markdown("**🥇 Top 3 Activos**")
            for i, (_, row) in enumerate(top_activos.head(3).iterrows()):
                st.metric(f"{i+1}. {row['banks'][:12]}", f"${row['valor_indicador']:,.0f}", f"Posición #{i+1}")
    
    if not roe_sistema.empty:
        col_chart2, col_metrics2 = st.columns([3, 1])
        
        with col_chart2:
            top_roe = roe_sistema.nlargest(10, 'valor_indicador')#type:ignore
            
            fig2 = px.bar(
                top_roe,
                x='banks',
                y='valor_indicador',
                title="Top 10 Bancos por ROE (%)",
                labels={'valor_indicador': 'ROE (%)', 'banks': 'Bancos'},
                color='valor_indicador',
                color_continuous_scale='Greens'
            )
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col_metrics2:
            st.markdown("**📊 Top 3 ROE**")
            for i, (_, row) in enumerate(top_roe.head(3).iterrows()):
                st.metric(f"{i+1}. {row['banks'][:12]}", f"{row['valor_indicador']:.2f}%", f"ROE #{i+1}")
    
    st.markdown("---")
    
    # Resto del código del tab_overview permanece igual...
    # (Peer Groups, Participación de Mercado, Correlaciones, etc.)

# =========================================================
# 🎯 TAB 2: ANÁLISIS POR CATEGORÍA (SIN CAMBIOS)
# =========================================================
with tab_categoria:
    st.header("🎯 Análisis por Categoría Específica")
    
    categoria = st.selectbox(
        "📈 Selecciona Categoría de Análisis:",
        ["Balance", "Rendimiento", "Estructura", "Calidad_Riesgo", "Eficiencia", "Crecimiento"],
        help="Análisis detallado por tipo de indicadores"
    )
    
    is_percentage = IndicatorConfig.is_category_percentage(categoria)
    unit = IndicatorConfig.get_category_unit(categoria)
    indicator_names = IndicatorConfig.get_indicator_names_by_category(categoria)
    
    # Mostrar info según categoría
    if categoria == "Balance":
        st.info("💼 **Balance:** Activos y recursos del banco")
    elif categoria == "Rendimiento":
        st.info("📊 **Rendimiento:** Rentabilidad y eficiencia")
    
    df_filtrado = dh.filter_by_category(
        indicator_names=indicator_names,
        convert_percentage=is_percentage
    )
    
    if df_filtrado.empty:
        st.error(f"⚠️ No hay datos para la categoría {categoria}")
        st.stop()
    
    bancos = dh.get_unique_values(df_filtrado, "banks")
    indicadores = dh.get_unique_values(df_filtrado, "nombre_del_indicador")
    
    # Resto del código del tab_categoria permanece igual...

# =========================================================
# 🏦 TAB 3: ANÁLISIS ESPECÍFICO (SIN CAMBIOS)
# =========================================================
with tab_especifico:
    st.header("🏦 Análisis Específico por Banco")
    
    banco_disponible = dh.get_unique_values(df, "banks")
    selected_bank = st.selectbox(
        "🏦 Selecciona Banco para Análisis:",
        banco_disponible,
        help="Escoge un banco para análisis detallado individual"
    )
    
    # Resto del código del tab_especifico permanece igual...

# =========================================================
# 🚀 TAB 4: API ANALYTICS AVANZADOS (NUEVA)
# =========================================================
with tab_api_advanced:
    st.header("🚀 API Analytics Avanzados")
    
    if not use_api:
        st.warning("⚠️ **API no activada.** Por favor activa 'Usar API REST' en el sidebar para acceder a estas funcionalidades.")
        st.info("💡 Los endpoints avanzados requieren conexión con el servidor FastAPI.")
        st.stop()
    
    st.markdown("**Análisis avanzados mediante consumo directo de endpoints especializados**")
    
    # Sub-tabs para diferentes análisis
    subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
        "🚨 Alertas", 
        "📊 Concentración", 
        "🏦 Peer Groups",
        "🔗 Correlaciones",
        "📈 Benchmark"
    ])
    
    # ===== SUB-TAB 1: ALERTAS DEL SISTEMA =====
    with subtab1:
        st.subheader("🚨 Sistema de Alertas Automáticas")
        
        col_filter, col_refresh = st.columns([3, 1])
        with col_filter:
            severity_filter = st.selectbox(
                "Filtrar por severidad:",
                ["Todas", "CRITICA", "ALTA", "MEDIA"]
            )
        
        with col_refresh:
            if st.button("🔄 Actualizar Alertas"):
                st.rerun()
        
        try:
            # Consumir endpoint de alertas
            alerts_response = api_client.get_system_alerts(#type:ignore
                severity=None if severity_filter == "Todas" else severity_filter
            )
            
            # Mostrar resumen
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🚨 Total Alertas", alerts_response['total_alerts'])
            with col2:
                st.metric("🔴 Críticas", alerts_response['critical_count'])
            with col3:
                st.metric("🟠 Altas", alerts_response['high_count'])
            with col4:
                st.metric("🟡 Medias", alerts_response['medium_count'])
            
            st.markdown("---")
            
            # Renderizar alertas
            if alerts_response['alerts']:
                for alert in alerts_response['alerts']:
                    severidad = alert.get('severidad', '')
                    
                    if 'CRÍTICA' in severidad:
                        st.error(f"🔴 **{alert.get('banco')}** - {alert.get('indicador')}")
                        st.caption(f"Valor: {alert.get('valor')} | Umbral: {alert.get('umbral')}")
                    elif 'ALTA' in severidad:
                        st.warning(f"🟠 **{alert.get('banco')}** - {alert.get('indicador')}")
                        st.caption(f"Valor: {alert.get('valor')} | Umbral: {alert.get('umbral')}")
                    elif 'MEDIA' in severidad:
                        st.info(f"🟡 **{alert.get('banco')}** - {alert.get('indicador')}")
                        st.caption(f"Valor: {alert.get('valor')} | Umbral: {alert.get('umbral')}")
            else:
                st.success("✅ No se encontraron alertas en el sistema")
                
        except Exception as e:
            st.error(f"❌ Error al obtener alertas: {e}")
    
    # ===== SUB-TAB 2: CONCENTRACIÓN DE MERCADO =====
    with subtab2:
        st.subheader("📊 Análisis de Concentración de Mercado")
        
        metric_concentration = st.selectbox(
            "Selecciona métrica:",
            ["TOTAL ACTIVO", "OBLIGACIONES CON EL PÚBLICO", "CARTERA DE CRÉDITOS"]
        )
        
        try:
            # Consumir endpoint de concentración
            concentration_response = api_client.get_market_concentration(metric=metric_concentration)#type:ignore
            
            # Mostrar métricas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 CR3", f"{concentration_response['cr3']:.2f}%", "Top 3 bancos")
            with col2:
                st.metric("📊 CR5", f"{concentration_response['cr5']:.2f}%", "Top 5 bancos")
            with col3:
                st.metric("📊 HHI", f"{concentration_response['hhi']:.0f}")
            with col4:
                interpretation = concentration_response['interpretation']
                if 'Competitivo' in interpretation:
                    st.success(f"✅ {interpretation}")
                elif 'Moderadamente' in interpretation:
                    st.warning(f"⚠️ {interpretation}")
                else:
                    st.error(f"🚨 {interpretation}")
            
            st.markdown("---")
            
            # Gráfico de top bancos
            if concentration_response['top_banks']:
                top_df = pd.DataFrame(concentration_response['top_banks'])
                
                fig = px.bar(
                    top_df,
                    x='banks',
                    y='valor_indicador',
                    title=f"Top 10 Bancos - {metric_concentration}",
                    color='valor_indicador',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error al obtener concentración: {e}")
    
    # ===== SUB-TAB 3: PEER GROUPS =====
    with subtab3:
        st.subheader("🏦 Análisis de Peer Groups")
        
        try:
            # Consumir endpoint de peer groups
            peer_response = api_client.get_peer_groups()#type:ignore
            
            # Mostrar distribución
            st.markdown("**📊 Distribución de Bancos por Tamaño**")
            
            distribution = peer_response['distribution']
            
            # Gráfico de pie
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(distribution.keys()),
                values=list(distribution.values()),
                hole=0.3
            )])
            fig_pie.update_layout(title="Distribución por Peer Groups")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("---")
            
            # Mostrar detalle por grupo
            for group_name, banks_list in peer_response['groups'].items():
                with st.expander(f"📁 {group_name} ({len(banks_list)} bancos)"):
                    cols = st.columns(3)
                    for idx, bank in enumerate(banks_list):
                        with cols[idx % 3]:
                            st.write(f"• {bank}")
                            
        except Exception as e:
            st.error(f"❌ Error al obtener peer groups: {e}")
    
    # ===== SUB-TAB 4: CORRELACIONES =====
    with subtab4:
        st.subheader("🔗 Matriz de Correlaciones")
        
        try:
            # Consumir endpoint de correlaciones
            corr_response = api_client.get_correlations()#type:ignore
            
            # Convertir a DataFrame
            corr_df = pd.DataFrame(corr_response['correlation_matrix'])
            
            # Heatmap
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.index,
                colorscale='RdBu',
                zmid=0,
                text=corr_df.round(2).values,
                texttemplate="%{text}",
                colorbar=dict(title="Correlación")
            ))
            
            fig_heatmap.update_layout(
                title="Matriz de Correlación - Indicadores Principales",
                height=600
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            st.markdown("---")
            
            # Correlaciones fuertes
            if corr_response['strong_correlations']:
                st.markdown("**🔍 Correlaciones Destacadas (|r| > 0.7)**")
                
                for corr in corr_response['strong_correlations']:
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col1:
                        st.write(f"**{corr['indicator1'][:20]}...**")
                    with col2:
                        if corr['correlation'] > 0:
                            st.success(f"r = {corr['correlation']:.3f}")
                        else:
                            st.error(f"r = {corr['correlation']:.3f}")
                    with col3:
                        st.write(f"**{corr['indicator2'][:20]}...**")
            else:
                st.info("No se encontraron correlaciones fuertes")
                
        except Exception as e:
            st.error(f"❌ Error al obtener correlaciones: {e}")
    
    # ===== SUB-TAB 5: BENCHMARK ANALYSIS =====
    with subtab5:
        st.subheader("📈 Análisis de Benchmark")
        
        col_bank_sel, col_bench_type = st.columns(2)
        
        with col_bank_sel:
            banks_list_response = api_client.get_banks_list(category="Balance")#type:ignore
            if banks_list_response:
                selected_bank_bench = st.selectbox(
                    "Selecciona Banco:",
                    banks_list_response
                )
            else:
                selected_bank_bench = st.selectbox("Selecciona Banco:", banco_disponible)
        
        with col_bench_type:
            benchmark_type = st.selectbox(
                "Tipo de Benchmark:",
                ["system_average", "top_quartile", "median"]
            )
        
        if st.button("🔍 Analizar Benchmark"):
            try:
                # Consumir endpoint de benchmark
                benchmark_response = api_client.get_benchmark_analysis(#type:ignore
                    bank_name=selected_bank_bench,
                    benchmark_type=benchmark_type
                )
                
                st.success(f"✅ Análisis completado para **{benchmark_response['bank']}**")
                st.caption(f"Benchmark: {benchmark_response['benchmark_type']}")
                
                st.markdown("---")
                
                # Mostrar comparaciones
                comparisons = benchmark_response['comparisons']
                
                for indicator, data in comparisons.items():
                    with st.expander(f"📊 {indicator}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Valor Banco", f"{data['valor_banco']:.2f}")
                        
                        with col2:
                            st.metric("Valor Benchmark", f"{data['valor_benchmark']:.2f}")
                        
                        with col3:
                            desv = data['desviacion_relativa_pct']
                            if desv > 10:
                                st.metric("Desviación", f"{desv:.1f}%", delta_color="normal")
                            elif desv < -10:
                                st.metric("Desviación", f"{desv:.1f}%", delta_color="inverse")
                            else:
                                st.metric("Desviación", f"{desv:.1f}%", delta_color="off")
                        
                        st.caption(f"**Posición:** {data['posicion']}")
                
            except Exception as e:
                st.error(f"❌ Error al obtener benchmark: {e}")

# =========================================================
# 📊 PIE DE PÁGINA
# =========================================================
st.caption("📊 Desarrollado por Grupo 5 — Proyecto Integrador 2025")
st.caption("💡 Dashboard de Salud Financiera - Sistema Bancario Ecuatoriano")
st.caption("📅 Datos: Superintendencia de Bancos - Septiembre 2025")
if api_activa:
    st.caption("🌐 **Modo API REST Activo** - Consumiendo endpoints avanzados")
