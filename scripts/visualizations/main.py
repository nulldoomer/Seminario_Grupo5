from components.indicator_config import IndicatorConfig
from components.data_handler import DataHandler
from components.metrics_calculator import MetricsCalculator
from components.charts_builder import ChartBuilder
from components.ui_components import UIComponents
from data_loader import VisualizationDataLoader

from services.api_client import get_api_client
import streamlit as st
import pandas as pd

# Intentar importar API client (opcional)
try:
    from services.api_client import get_api_client
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False

# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================
st.set_page_config(
    page_title="Dashboard de Salud Financiera",
    page_icon="📊",
    layout="wide"
)

api_client = None
api_connected = False

if API_AVAILABLE:
    try:
        api_client = get_api_client()
        test_response = api_client.test_connection()
        if test_response and test_response.get("status") == "success":
            api_connected = True
    except Exception as e:
        print(f"Error conectando al API: {e}")
        api_connected = False

# =========================================================
# CONEXIÓN CON API
# =========================================================
@st.cache_resource
def init_data_handler():
    """Inicializa el DataHandler (se cachea para no recargar)"""
    data_loader = VisualizationDataLoader()
    return DataHandler(data_loader)

# =========================================================
# FUNCIÓN HÍBRIDA DE DATOS
# =========================================================
@st.cache_data
def load_hybrid_data():
    """Carga datos del API si está disponible, sino usa datos locales"""
    if api_connected and api_client:
        try:
            # Intentar cargar desde overview del API
            overview = api_client.get_system_overview()
            if overview:
                # Aquí podrías construir el DataFrame desde el overview si quisieras
                # Pero para mantener compatibilidad, cargamos local
                pass
        except Exception as e:
            pass
    
    # Cargar datos locales
    dh = init_data_handler()
    df_local = dh.load_data("Final Dataframe")
    
    if df_local is not None:
        return df_local
    else:
        st.error("Error cargando datos")
        return pd.DataFrame()

# Cargar datos usando función híbrida
df = load_hybrid_data()
dh = init_data_handler()

if df.empty:
    st.error("No se pudieron cargar datos ni del API ni localmente")
    st.stop()

# =========================================================
# ENRIQUECIMIENTO DE DATOS - AHORA VÍA API
# =========================================================
@st.cache_data
def enrich_data_with_advanced_metrics(df):
    """Enriquece los datos usando la API si está disponible"""
    
    if api_connected and api_client:
        try:
            # Obtener indicadores derivados desde API
            derived_response = api_client.get_derived_indicators()
            
            if derived_response and derived_response.get('data'):
                # Convertir a DataFrame
                derived_df = pd.DataFrame(derived_response['data'])
                
                # Renombrar columnas para que coincidan con df
                derived_df = derived_df.rename(columns={
                    'banks': 'banks',
                    'nombre_del_indicador': 'nombre_del_indicador', 
                    'valor_indicador': 'valor_indicador'
                })
                
                # Concatenar con datos originales
                df_enriched = pd.concat([df, derived_df], ignore_index=True)
                
                return df_enriched
        except Exception as e:
            print(f"Error obteniendo indicadores derivados de API: {e}")
    
    # Fallback: usar cálculo local
    from components.advanced_metrics import AdvancedMetrics
    df_enriched = AdvancedMetrics.calculate_derived_indicators(df)
    df_final = AdvancedMetrics.calculate_composite_indices(df_enriched)
    return df_final

# Enriquecer datos
df = enrich_data_with_advanced_metrics(df)

# =========================================================
# ENCABEZADO
# =========================================================
st.title("📊 Dashboard de Salud Financiera Bancaria")
st.markdown("""
**Análisis integral del Sistema Bancario Ecuatoriano**  
Dashboard interactivo para evaluar indicadores de Balance, Rendimiento y Estructura Financiera.
""")

# =========================================================
# PESTAÑAS PRINCIPALES
# =========================================================
tab_overview, tab_categoria, tab_especifico = st.tabs([
    "Overview General", 
    "Análisis por Categoría", 
    "Análisis Específico por Banco"
])

# Configurar sidebar común
with st.sidebar:
    st.header("Panel de Control")
    
    # Estado de la conexión API
    st.subheader("Estado del Sistema")
    if api_connected:
        st.success("✅ API Conectado")
        st.caption(f"URL: {api_client.base_url}")
        if st.button("🔄 Reconectar"):
            st.rerun()
    elif API_AVAILABLE:
        st.warning("⚠️ API Parcialmente Disponible")
        st.caption(f"URL: {api_client.base_url if api_client else 'N/A'}")
        if st.button("🔄 Intentar Conectar"):
            st.rerun()
    else:
        st.info("📁 Modo Local")
        st.caption("Usando datos locales")
    
    st.markdown("---")
    
    # Información adicional general
    total_bancos_sistema = df["banks"].nunique()
    total_indicadores_sistema = df["nombre_del_indicador"].nunique()
    
    st.caption(f"🏦 **Total Bancos:** {total_bancos_sistema}")
    st.caption(f"📊 **Total Indicadores:** {total_indicadores_sistema}")
    st.caption(f"**Periodo:** Septiembre 2025")

# =========================================================
# TAB 1: OVERVIEW GENERAL - USANDO API
# =========================================================
with tab_overview:
    st.header("📊 Overview General del Sistema Bancario")
    st.markdown("**Vista panorámica de todos los indicadores y bancos del sistema**")
    
    calc = MetricsCalculator()
    ui = UIComponents()
    
    # =========================================================
    # ESTADÍSTICAS GENERALES - DESDE API
    # =========================================================
    st.subheader("📈 Estadísticas Generales del Sistema")
    
    # Intentar obtener desde API
    overview_data = None
    if api_connected and api_client:
        try:
            overview_data = api_client.get_system_overview()
        except:
            pass
    
    if overview_data:
        # Usar datos del API
        general_stats = overview_data.get("general_statistics", {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🏦 Total Bancos",
                f"{general_stats.get('total_banks', total_bancos_sistema)}",
                "en el sistema"
            )
        
        with col2:
            st.metric(
                "📊 Total Indicadores",
                f"{general_stats.get('total_indicators', total_indicadores_sistema)}",
                "métricas disponibles"
            )
        
        with col3:
            total_observaciones = general_stats.get('total_observations', len(df))
            st.metric(
                "📋 Total Observaciones",
                f"{total_observaciones:,}",
                "registros de datos"
            )
        
        with col4:
            completitud = ((df['valor_indicador'].notna().sum() / len(df)) * 100)
            st.metric(
                "✅ Completitud de Datos",
                f"{completitud:.1f}%",
                "datos disponibles"
            )
    else:
        # Fallback: cálculo local
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
    
    # =========================================================
    # ESTADÍSTICAS CLAVE - DESDE API O LOCAL
    # =========================================================
    st.subheader("💼 Estadísticas Clave del Sistema")
    
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.markdown("**Indicadores Financieros Principales**")
        
        # Total de activos del sistema
        activos_data = df[df['nombre_del_indicador'] == 'TOTAL ACTIVO']
        if not activos_data.empty:
            activos_sistema = activos_data['valor_indicador'].sum()
            st.metric("💰 Activos Totales Sistema", f"${activos_sistema:,.0f}")
        
        # Promedio ROE del sistema
        roe_sistema = df[df['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
        if not roe_sistema.empty:
            roe_promedio = roe_sistema['valor_indicador'].mean()
            st.metric("📈 ROE Promedio Sistema", f"{roe_promedio:.2f}%")
        
        # Promedio ROA del sistema
        roa_sistema = df[df['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO']
        if not roa_sistema.empty:
            roa_promedio = roa_sistema['valor_indicador'].mean()
            st.metric("📊 ROA Promedio Sistema", f"{roa_promedio:.2f}%")
    
    with col_stats2:
        st.markdown("**Concentración y Distribución**")
        
        # Concentración de los 3 bancos más grandes
        if not activos_data.empty:
            top3_activos = activos_data.nlargest(3, 'valor_indicador')['valor_indicador'].sum()
            concentracion_top3 = (top3_activos / activos_sistema * 100) if activos_sistema > 0 else 0
            st.metric("🏆 Concentración Top 3", f"{concentracion_top3:.1f}%")
        
        # Banco mediano por activos
        if not activos_data.empty:
            mediana_activos = activos_data['valor_indicador'].median()
            st.metric("📊 Banco Mediano (Activos)", f"${mediana_activos:,.0f}")
        
        # Coeficiente de variación en ROE
        if not roe_sistema.empty:
            cv_roe = (roe_sistema['valor_indicador'].std() / roe_sistema['valor_indicador'].mean() * 100)
            st.metric("📉 Variabilidad ROE", f"{cv_roe:.1f}%")
    
    st.markdown("---")
    
    # =========================================================
    # ANÁLISIS DE CONCENTRACIÓN - DESDE API
    # =========================================================
    st.subheader("🎯 Análisis de Concentración del Mercado")
    
    concentration_data = None
    if api_connected and api_client:
        try:
            concentration_data = api_client.get_market_concentration(metric="TOTAL ACTIVO")
        except:
            pass
    
    if concentration_data:
        # USAR DATOS DEL API
        col_conc1, col_conc2 = st.columns([2, 1])
        
        with col_conc1:
            hhi = concentration_data.get('hhi', 0)
            interpretation = concentration_data.get('interpretation', 'Desconocido')
            
            st.metric(
                "📊 Índice HHI",
                f"{hhi:.0f}",
                f"Concentración: {interpretation}"
            )
            
            # Interpretación del HHI
            if hhi < 1500:
                st.success("✅ Mercado no concentrado (HHI < 1500)")
            elif hhi < 2500:
                st.warning("⚠️ Mercado moderadamente concentrado (1500 ≤ HHI < 2500)")
            else:
                st.error("🔴 Mercado altamente concentrado (HHI ≥ 2500)")
        
        with col_conc2:
            cr3 = concentration_data.get('cr3', 0)
            cr5 = concentration_data.get('cr5', 0)
            
            st.metric("🥇 Top 3 Concentración", f"{cr3:.1f}%")
            st.metric("🏆 Top 5 Concentración", f"{cr5:.1f}%")
    else:
        # FALLBACK: Calcular localmente (código original)
        from components.analysis_engine import TrendAnalysis
        concentration_calc = TrendAnalysis.calculate_concentration_risk(df)
        
        if concentration_calc and 'TOTAL ACTIVO' in concentration_calc:
            activo_data = concentration_calc['TOTAL ACTIVO']
            col_conc1, col_conc2 = st.columns([2, 1])
            
            with col_conc1:
                hhi = activo_data.get('HHI', 0)
                concentration_level = activo_data.get('interpretacion_HHI', 'Desconocido')
                
                st.metric("📊 Índice HHI", f"{hhi:.0f}", f"Concentración: {concentration_level}")
                
                if hhi < 1500:
                    st.success("✅ Mercado no concentrado (HHI < 1500)")
                elif hhi < 2500:
                    st.warning("⚠️ Mercado moderadamente concentrado (1500 ≤ HHI < 2500)")
                else:
                    st.error("🔴 Mercado altamente concentrado (HHI ≥ 2500)")
            
            with col_conc2:
                cr3 = activo_data.get('CR3', 0)
                cr5 = activo_data.get('CR5', 0)
                
                st.metric("🥇 Top 3 Concentración", f"{cr3:.1f}%")
                st.metric("🏆 Top 5 Concentración", f"{cr5:.1f}%")
    
    st.markdown("---")
    
    # =========================================================
    # TOP PERFORMERS GENERALES
    # =========================================================
    st.subheader("🏆 Top Performers del Sistema (Todos los Indicadores)")
    
    # Análisis de activos totales
    activos_data = df[df['nombre_del_indicador'] == 'TOTAL ACTIVO']
    if not activos_data.empty:
        col_chart1, col_metrics1 = st.columns([3, 1])
        
        with col_chart1:
            top_activos = activos_data.nlargest(10, 'valor_indicador')
            
            import plotly.express as px
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
                st.metric(
                    f"{i+1}. {row['banks'][:12]}",
                    f"${row['valor_indicador']:,.0f}",
                    f"Posición #{i+1}"
                )
    
    # Análisis de rentabilidad (ROE)
    roe_data = df[df['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
    if not roe_data.empty:
        col_chart2, col_metrics2 = st.columns([3, 1])
        
        with col_chart2:
            top_roe = roe_data.nlargest(10, 'valor_indicador')
            
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
            st.markdown("**📈 Top 3 ROE**")
            for i, (_, row) in enumerate(top_roe.head(3).iterrows()):
                st.metric(
                    f"{i+1}. {row['banks'][:12]}",
                    f"{row['valor_indicador']:.2f}%",
                    f"ROE #{i+1}"
                )
    
    st.markdown("---")
    
    # =========================================================
    # ANÁLISIS POR PEER GROUPS - DESDE API
    # =========================================================
    st.subheader("🏦 Distribución por Tamaño de Bancos")
    
    peer_groups = None
    if api_connected and api_client:
        try:
            peer_response = api_client.get_peer_groups(size_metric='TOTAL ACTIVO')
            if peer_response:
                peer_groups = peer_response.get('groups', {})
        except:
            pass
    
    if not peer_groups:
        # Fallback local
        from components.analysis_engine import TrendAnalysis
        peer_groups = TrendAnalysis.peer_group_analysis(df, size_metric='TOTAL ACTIVO')
    
    if peer_groups:
        col_pie, col_details = st.columns([2, 1])
        
        with col_pie:
            group_sizes = {group: len(banks) for group, banks in peer_groups.items()}
            
            import plotly.graph_objects as go
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(group_sizes.keys()),
                values=list(group_sizes.values()),
                hole=0.3,
                textinfo='label+percent'
            )])
            fig_pie.update_layout(title="Distribución de Bancos por Tamaño")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_details:
            st.markdown("**📋 Detalle por Grupo**")
            for group_name, banks_list in peer_groups.items():
                with st.expander(f"{group_name} ({len(banks_list)})"):
                    for bank in banks_list:
                        st.write(f"• {bank}")
    
    st.markdown("---")
    
    # =========================================================
    # PARTICIPACIÓN DE MERCADO - DESDE API
    # =========================================================
    st.subheader("📊 Participación de Mercado por Métrica")
    
    metric_selector = st.selectbox(
        "Selecciona métrica para análisis de participación:",
        ["TOTAL ACTIVO", "OBLIGACIONES CON EL PÚBLICO", "CARTERA DE CRÉDITOS", "TOTAL PATRIMONIO"]
    )
    
    market_participation = None
    if api_connected and api_client:
        try:
            market_response = api_client.get_market_share(metric=metric_selector, top_n=10)
            if market_response:
                market_participation = {metric_selector: api_client.market_share_to_dataframe(market_response)}
        except:
            pass
    
    if not market_participation:
        # Fallback local
        from components.advanced_metrics import AdvancedMetrics
        market_participation = AdvancedMetrics.calculate_market_participation(df)
    
    if market_participation and metric_selector in market_participation:
        participation_df = market_participation[metric_selector]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Participación de Mercado: {metric_selector}**")
            
            top_10 = participation_df.head(10)
            
            import plotly.express as px
            fig = px.bar(
                top_10, 
                x='banks', 
                y='participacion_pct',
                title=f"Top 10 Bancos - Participación en {metric_selector}",
                labels={'participacion_pct': 'Participación (%)', 'banks': 'Bancos'},
                color='participacion_pct',
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**📈 Top 5 Participación**")
            for i, (_, row) in enumerate(participation_df.head(5).iterrows()):
                st.metric(
                    f"{i+1}. {row['banks'][:15]}...",
                    f"{row['participacion_pct']:.1f}%",
                    f"${row['valor_absoluto']:,.0f}"
                )
        
        # Mostrar tabla detallada
        st.markdown("**📋 Detalle Completo de Participación**")
        st.dataframe(
            participation_df.style.format({
                'participacion_pct': '{:.2f}%',
                'valor_absoluto': '${:,.0f}'
            }).background_gradient(subset=['participacion_pct'], cmap='Blues'),
            use_container_width=True,
            height=300
        )
    
    st.markdown("---")
    
    # =========================================================
    # ANÁLISIS DE CORRELACIONES - DESDE API
    # =========================================================
    st.subheader("🔗 Análisis de Correlaciones entre Indicadores")
    
    correlation_matrix = None
    if api_connected and api_client:
        try:
            corr_response = api_client.get_correlations()
            if corr_response:
                correlation_matrix = api_client.correlation_to_dataframe(corr_response)
        except:
            pass
    
    if correlation_matrix is None or correlation_matrix.empty:
        # Fallback local
        from components.analysis_engine import TrendAnalysis
        correlation_matrix = TrendAnalysis.correlation_analysis(df)
    
    if not correlation_matrix.empty:
        col_heatmap, col_insights = st.columns([3, 1])
        
        with col_heatmap:
            import plotly.graph_objects as go
            
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='RdBu',
                zmid=0,
                text=correlation_matrix.round(2).values,
                texttemplate="%{text}",
                textfont={"size": 10},
                colorbar=dict(title="Correlación")
            ))
            
            fig.update_layout(
                title="Matriz de Correlación - Indicadores Principales",
                xaxis_tickangle=-45,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col_insights:
            st.markdown("**🧠 Correlaciones Destacadas**")
            
            # Encontrar correlaciones fuertes
            strong_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_val = correlation_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        var1 = correlation_matrix.columns[i]
                        var2 = correlation_matrix.columns[j]
                        direction = "positiva" if corr_val > 0 else "negativa"
                        strong_correlations.append({
                            'vars': f"{var1[:15]}... y {var2[:15]}...",
                            'direction': direction,
                            'value': corr_val
                        })
            
            if strong_correlations:
                for corr in strong_correlations[:5]:
                    st.metric(
                        corr['vars'],
                        f"{corr['value']:.2f}",
                        f"Correlación {corr['direction']}"
                    )
            else:
                st.info("ℹ️ No hay correlaciones fuertes (>0.7)")
    
    st.markdown("---")
    
    # =========================================================
    # ÍNDICES COMPUESTOS DE DESEMPEÑO
    # =========================================================
    st.subheader("🎯 Índices Compuestos de Desempeño - Rankings Generales")
    
    indices_compuestos = [
        "INDICE DE SOLIDEZ FINANCIERA",
        "INDICE DE RENTABILIDAD AJUSTADA", 
        "INDICE GLOBAL DESEMPEÑO BANCARIO"
    ]
    
    for indice in indices_compuestos:
        indice_data = df[df['nombre_del_indicador'] == indice]
        
        if not indice_data.empty:
            with st.expander(f"📊 {indice} - Ranking General"):
                ranking_indice = indice_data.sort_values('valor_indicador', ascending=False).reset_index(drop=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    import plotly.express as px
                    fig = px.bar(
                        ranking_indice.head(10),
                        x='banks',
                        y='valor_indicador',
                        title=f"Top 10 - {indice}",
                        color='valor_indicador',
                        color_continuous_scale='viridis'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**🏆 Top 5**")
                    for i, (_, row) in enumerate(ranking_indice.head(5).iterrows()):
                        st.metric(
                            f"{i+1}. {row['banks'][:20]}",
                            f"{row['valor_indicador']:.2f}"
                        )
    
    st.markdown("---")

# =========================================================
# TAB 2: ANÁLISIS POR CATEGORÍA (sin cambios por ahora)
# =========================================================
with tab_categoria:
    st.header("📂 Análisis por Categoría Específica")
    
    categoria = st.selectbox(
        "Selecciona Categoría de Análisis:",
        ["Balance", "Rendimiento", "Estructura", "Calidad_Riesgo", "Eficiencia", "Crecimiento"],
        help="Análisis detallado por tipo de indicadores"
    )
    
    if categoria == "Balance":
        st.info("💰 **Balance:** Activos y recursos del banco")
    elif categoria == "Rendimiento":
        st.info("📈 **Rendimiento:** Rentabilidad y eficiencia")
    elif categoria == "Estructura":
        st.info("🏗️ **Estructura:** Composición financiera")
    elif categoria == "Calidad_Riesgo":
        st.info("⚠️ **Calidad/Riesgo:** Morosidad y solvencia")
    elif categoria == "Eficiencia":
        st.info("⚡ **Eficiencia:** Ratios operativos")
    elif categoria == "Crecimiento":
        st.info("📈 **Crecimiento:** Variaciones temporales")
    
    # Filtrar datos por categoría
    indicator_names = IndicatorConfig.get_indicator_names_by_category(categoria)
    
    if not indicator_names:
        st.error(f"No hay indicadores configurados para la categoría '{categoria}'")
        st.stop()
    
    if dh.dataframe is None:
        dh.dataframe = df
    
    df_filtrado = dh.filter_by_category(indicator_names)
    
    if df_filtrado.empty:
        st.error(f"No hay datos disponibles para la categoría '{categoria}'")
        st.stop()
    
    bancos = dh.get_unique_values(df_filtrado, "banks")
    indicadores = dh.get_unique_values(df_filtrado, "nombre_del_indicador")
    
    # =========================================================
    # MÉTRICAS DE LA CATEGORÍA
    # =========================================================
    st.subheader(f"📊 Estadísticas de {categoria}")
    
    calc = MetricsCalculator()
    ui = UIComponents()
    
    is_percentage_default = False
    
    total_bancos_cat = df_filtrado["banks"].nunique()
    total_indicadores_cat = len(IndicatorConfig.get_all_indicators_by_category(categoria))
    total_valor_cat = calc.calculate_total(df_filtrado)
    promedio_cat = calc.calculate_average(df_filtrado)
    
    ui.render_metric_cards(
        total_bancos=total_bancos_cat,
        total_indicadores=total_indicadores_cat,
        total_valor=total_valor_cat,
        promedio=promedio_cat,
        is_percentage=is_percentage_default
    )
    
    st.markdown("---")
    
    st.subheader(f"🏆 Rankings Dinámicos - {categoria}")
    
    selected_indicator = st.selectbox(
        "📊 Selecciona Indicador para Ranking:",
        indicadores,
        help="Elige qué indicador quieres analizar en el ranking"
    )
    
    config = IndicatorConfig.get_indicator_info(selected_indicator)
    if config:
        is_percentage = config.get("is_percentage", False)
        unit = config.get("unit", "")
    else:
        is_percentage = False
        unit = ""
    
    ranking_df = dh.get_ranking(df_filtrado, selected_indicator, ascending=False)
    
    if not ranking_df.empty:
        col_chart_rank, col_metrics_rank = st.columns([3, 1])
        
        with col_chart_rank:
            builder = ChartBuilder(is_percentage, unit)
            
            import plotly.express as px
            
            fig_rank = px.bar(
                ranking_df.head(10),
                x='banks',
                y='valor_indicador',
                title=f"Top 10 - {selected_indicator}",
                labels={'valor_indicador': f'{selected_indicator} ({unit})', 'banks': 'Bancos'},
                color='valor_indicador',
                color_continuous_scale='viridis'
            )
            fig_rank.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_rank, use_container_width=True)
        
        with col_metrics_rank:
            st.markdown("**🎖️ Top 3**")
            
            ui.render_top3_medals(
                df=ranking_df,
                bank_col="banks",
                value_col="valor_indicador",
                is_percentage=is_percentage
            )
    
    st.markdown("---")
    
    # =========================================================
    # TABLA COMPARATIVA DE LA CATEGORÍA
    # =========================================================
    st.subheader(f"📋 Matriz Comparativa - {categoria}")
    
    indicator_order = [ind.name for ind in IndicatorConfig.get_all_indicators_by_category(categoria)]
    pivot_df = dh.get_pivot_table(df_filtrado, indicator_order)
    
    if not pivot_df.empty:
        if is_percentage:
            styled_df = (
                pivot_df.style
                .format("{:.2f}%")
                .background_gradient(cmap="RdYlGn", axis=0)
                .set_properties(**{'text-align': 'right'})
            )
        else:
            styled_df = (
                pivot_df.style
                .format("${:,.0f}")
                .background_gradient(cmap="RdYlGn", axis=0)
                .set_properties(**{'text-align': 'right'})
            )
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        col_download = st.columns([1, 3])
        with col_download[0]:
            ui.render_download_button(
                df=pivot_df,
                filename=f'matriz_{categoria.lower()}.csv',
                label="📥 Descargar Matriz"
            )
    
    st.markdown("---")
    
    # =========================================================
    # ANÁLISIS DE CORRELACIONES DE LA CATEGORÍA - DESDE API
    # =========================================================
    if len(indicadores) > 1:
        st.subheader(f"🔗 Correlaciones en {categoria}")
        
        correlation_matrix = None
        if api_connected and api_client:
            try:
                corr_response = api_client.get_correlations()
                if corr_response:
                    correlation_matrix = api_client.correlation_to_dataframe(corr_response)
                    # Filtrar solo indicadores de esta categoría
                    available_indicators = [col for col in correlation_matrix.columns if col in indicadores]
                    if available_indicators:
                        correlation_matrix = correlation_matrix.loc[available_indicators, available_indicators]
            except:
                pass
        
        if correlation_matrix is None or correlation_matrix.empty:
            # Fallback local
            from components.analysis_engine import TrendAnalysis
            correlation_matrix = TrendAnalysis.correlation_analysis(df_filtrado)
        
        if not correlation_matrix.empty and correlation_matrix.shape[0] > 1:
            import plotly.graph_objects as go
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='RdBu',
                zmid=0,
                text=correlation_matrix.round(2).values,
                texttemplate="%{text}",
                textfont={"size": 10},
                colorbar=dict(title="Correlación")
            ))
            
            fig_corr.update_layout(
                title=f"Matriz de Correlación - {categoria}",
                xaxis_tickangle=-45,
                height=500
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)

# =========================================================
# TAB 3: ANÁLISIS ESPECÍFICO POR BANCO - USANDO API
# =========================================================
with tab_especifico:
    st.header("🏦 Análisis Específico por Banco")
    st.markdown("**Análisis individual detallado con comparaciones específicas**")
    
    banco_disponible = dh.get_unique_values(df, "banks")
    selected_bank = st.selectbox(
        "🏦 Selecciona Banco para Análisis:",
        banco_disponible,
        help="Escoge un banco para análisis detallado individual"
    )
    
    if selected_bank:
        bank_df = df[df['banks'] == selected_bank]
        
        if bank_df.empty:
            st.error(f"⚠️ No hay datos para el banco {selected_bank}")
            st.stop()
        
        calc = MetricsCalculator()
        ui = UIComponents()
        
        # =========================================================
        # RESUMEN EJECUTIVO DEL BANCO SELECCIONADO
        # =========================================================
        st.subheader(f"📋 Resumen Ejecutivo: {selected_bank}")
        
        col_bank1, col_bank2, col_bank3, col_bank4 = st.columns(4)
        
        with col_bank1:
            total_indicators_bank = bank_df["nombre_del_indicador"].nunique()
            st.metric("📊 Indicadores Disponibles", total_indicators_bank)
        
        with col_bank2:
            activos_bank = bank_df[bank_df['nombre_del_indicador'] == 'TOTAL ACTIVO']
            if not activos_bank.empty:
                activo_valor = activos_bank['valor_indicador'].iloc[0]
                st.metric("💰 Activos Totales", f"${activo_valor:,.0f}")
            else:
                st.metric("💰 Activos Totales", "N/D")
        
        with col_bank3:
            roe_bank = bank_df[bank_df['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
            if not roe_bank.empty:
                roe_valor = roe_bank['valor_indicador'].iloc[0]
                st.metric("📈 ROE", f"{roe_valor:.2f}%")
            else:
                st.metric("📈 ROE", "N/D")
        
        with col_bank4:
            ranking_activos = df[df['nombre_del_indicador'] == 'TOTAL ACTIVO'].sort_values('valor_indicador', ascending=False)
            if not ranking_activos.empty:
                posicion = ranking_activos.reset_index(drop=True).index[ranking_activos['banks'] == selected_bank].tolist()
                if posicion:
                    st.metric("🏆 Posición por Activos", f"#{posicion[0] + 1}")
                else:
                    st.metric("🏆 Posición por Activos", "N/D")
            else:
                st.metric("🏆 Posición por Activos", "N/D")
        
        st.markdown("---")
        
        # =========================================================
        # ANÁLISIS FINANCIERO PROFESIONAL DEL BANCO
        # =========================================================
        
        bank_indicators = bank_df[['nombre_del_indicador', 'valor_indicador']].copy()
        
        # 🧱 SOLVENCIA
        with st.expander("🧱 **Solvencia y Solidez Financiera**", expanded=True):
            st.markdown("**Capacidad del banco para absorber pérdidas y mantener estabilidad**")
            
            col_solv1, col_solv2, col_solv3 = st.columns(3)
            
            with col_solv1:
                patrimonio = bank_indicators[bank_indicators['nombre_del_indicador'] == 'TOTAL PATRIMONIO']
                activos = bank_indicators[bank_indicators['nombre_del_indicador'] == 'TOTAL ACTIVO']
                
                if not patrimonio.empty and not activos.empty:
                    ratio_solvencia = (patrimonio['valor_indicador'].iloc[0] / activos['valor_indicador'].iloc[0]) * 100
                    color = "normal" if ratio_solvencia >= 10 else "inverse"
                    st.metric(
                        "📊 Ratio de Solvencia",
                        f"{ratio_solvencia:.2f}%",
                        "Patrimonio/Activos",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: ≥ 10% (Basilea)")
                else:
                    st.metric("📊 Ratio de Solvencia", "N/D")
            
            with col_solv2:
                if not patrimonio.empty and not activos.empty:
                    apalancamiento = activos['valor_indicador'].iloc[0] / patrimonio['valor_indicador'].iloc[0]
                    color = "inverse" if apalancamiento < 12 else "normal"
                    st.metric(
                        "⚖️ Apalancamiento",
                        f"{apalancamiento:.1f}x",
                        "Activos/Patrimonio",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: < 12x")
                else:
                    st.metric("⚖️ Apalancamiento", "N/D")
            
            with col_solv3:
                solidez = bank_indicators[bank_indicators['nombre_del_indicador'].str.contains('PATRIMONIO', na=False)]
                if len(solidez) > 1:
                    st.metric("🛡️ Solidez Patrimonial", "Múltiples métricas", "Ver detalles abajo")
                else:
                    st.metric("🛡️ Estado General", "Estable", "Basado en ratios")
        
        # 💧 LIQUIDEZ
        with st.expander("💧 **Liquidez y Capacidad de Pago**", expanded=True):
            st.markdown("**Capacidad para cumplir obligaciones inmediatas y retiros**")
            
            col_liq1, col_liq2, col_liq3 = st.columns(3)
            
            with col_liq1:
                fondos_disp = bank_indicators[bank_indicators['nombre_del_indicador'] == 'FONDOS DISPONIBLES']
                obligaciones = bank_indicators[bank_indicators['nombre_del_indicador'] == 'OBLIGACIONES CON EL PÚBLICO']
                
                if not fondos_disp.empty and not obligaciones.empty:
                    ratio_liquidez = (fondos_disp['valor_indicador'].iloc[0] / obligaciones['valor_indicador'].iloc[0]) * 100
                    color = "normal" if ratio_liquidez >= 20 else "inverse"
                    st.metric(
                        "💧 Ratio de Liquidez",
                        f"{ratio_liquidez:.2f}%",
                        "Fondos Disp./Obligaciones",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: ≥ 20%")
                else:
                    st.metric("💧 Ratio de Liquidez", "N/D")
            
            with col_liq2:
                if not fondos_disp.empty:
                    liquidez_abs = fondos_disp['valor_indicador'].iloc[0]
                    st.metric(
                        "💵 Fondos Disponibles",
                        f"${liquidez_abs:,.0f}",
                        "Liquidez absoluta"
                    )
                    st.caption("Dinero inmediatamente disponible")
                else:
                    st.metric("💵 Fondos Disponibles", "N/D")
            
            with col_liq3:
                if not activos.empty and not fondos_disp.empty:
                    ratio_activos_liq = (fondos_disp['valor_indicador'].iloc[0] / activos['valor_indicador'].iloc[0]) * 100
                    st.metric(
                        "💦 % Activos Líquidos",
                        f"{ratio_activos_liq:.2f}%",
                        "Fondos/Total Activos"
                    )
                    st.caption("Flexibilidad financiera")
                else:
                    st.metric("💦 % Activos Líquidos", "N/D")
        
        # 💰 RENTABILIDAD
        with st.expander("💰 **Rentabilidad y Eficiencia Financiera**", expanded=True):
            st.markdown("**Capacidad de generar valor y retornos sostenibles**")
            
            col_rent1, col_rent2, col_rent3 = st.columns(3)
            
            with col_rent1:
                roe = bank_indicators[bank_indicators['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
                if not roe.empty:
                    roe_val = roe['valor_indicador'].iloc[0]
                    if 10 <= roe_val <= 20:
                        color = "normal"
                        status = "Excelente"
                    elif roe_val >= 10:
                        color = "normal" 
                        status = "Bueno"
                    else:
                        color = "inverse"
                        status = "Bajo"
                    
                    st.metric(
                        "📈 ROE",
                        f"{roe_val:.2f}%",
                        f"Estado: {status}",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: 10-20%")
                else:
                    st.metric("📈 ROE", "N/D")
            
            with col_rent2:
                roa = bank_indicators[bank_indicators['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO']
                if not roa.empty:
                    roa_val = roa['valor_indicador'].iloc[0]
                    if 0.5 <= roa_val <= 2:
                        color = "normal"
                        status = "Excelente"
                    elif roa_val >= 0.5:
                        color = "normal"
                        status = "Bueno"
                    else:
                        color = "inverse"
                        status = "Bajo"
                    
                    st.metric(
                        "📊 ROA",
                        f"{roa_val:.2f}%",
                        f"Estado: {status}",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: 0.5-2%")
                else:
                    st.metric("📊 ROA", "N/D")
            
            with col_rent3:
                margen_fin = bank_indicators[bank_indicators['nombre_del_indicador'].str.contains('MARGEN', na=False)]
                if not margen_fin.empty:
                    st.metric(
                        "💹 Margen Financiero",
                        f"${margen_fin['valor_indicador'].iloc[0]:,.0f}",
                        "Ingresos netos"
                    )
                    st.caption("Capacidad de generar ingresos")
                else:
                    resultados = bank_indicators[bank_indicators['nombre_del_indicador'].str.contains('RESULTADOS DEL EJERCICIO', na=False)]
                    if not resultados.empty and not activos.empty:
                        margen_aprox = (resultados['valor_indicador'].iloc[0] / activos['valor_indicador'].iloc[0]) * 100
                        st.metric(
                            "💹 Margen Neto",
                            f"{margen_aprox:.3f}%",
                            "Resultados/Activos"
                        )
                    else:
                        st.metric("💹 Margen Neto", "N/D")
        
        # 🧮 EFICIENCIA OPERATIVA
        with st.expander("🧮 **Eficiencia Operativa**", expanded=True):
            st.markdown("**Eficiencia en el uso de recursos y control de gastos**")
            
            col_ef1, col_ef2, col_ef3 = st.columns(3)
            
            with col_ef1:
                gastos_op = bank_indicators[bank_indicators['nombre_del_indicador'].str.contains('GASTOS', na=False)]
                if not gastos_op.empty:
                    gastos_activos = bank_indicators[bank_indicators['nombre_del_indicador'] == 'GASTOS OPERACIONALES / ACTIVO PROMEDIO']
                    gastos_margen = bank_indicators[bank_indicators['nombre_del_indicador'] == 'GASTOS OPERACIONALES / MARGEN FINANCIERO']
                    
                    if not gastos_margen.empty:
                        ef_ratio = gastos_margen['valor_indicador'].iloc[0]
                        color = "inverse" if ef_ratio < 60 else "normal"
                        status = "Eficiente" if ef_ratio < 60 else "Ineficiente"
                        
                        st.metric(
                            "⚡ Ratio de Eficiencia",
                            f"{ef_ratio:.2f}%",
                            f"Estado: {status}",
                            delta_color=color
                        )
                        st.caption("✅ Ideal: < 60%")
                    else:
                        st.metric("⚡ Ratio de Eficiencia", "N/D")
                else:
                    st.metric("⚡ Ratio de Eficiencia", "N/D")
            
            with col_ef2:
                gastos_activos = bank_indicators[bank_indicators['nombre_del_indicador'] == 'GASTOS OPERACIONALES / ACTIVO PROMEDIO']
                if not gastos_activos.empty:
                    ga_ratio = gastos_activos['valor_indicador'].iloc[0]
                    st.metric(
                        "📉 Gastos/Activos",
                        f"{ga_ratio:.2f}%",
                        "Eficiencia de activos"
                    )
                    st.caption("Menor = más eficiente")
                else:
                    st.metric("📉 Gastos/Activos", "N/D")
            
            with col_ef3:
                if not activos.empty:
                    productividad_aprox = activos['valor_indicador'].iloc[0] / 1000000
                    st.metric(
                        "⚡ Productividad",
                        f"${productividad_aprox:.0f}M",
                        "Escala operativa"
                    )
                    st.caption("💡 Tamaño y capacidad")
                else:
                    st.metric("⚡ Productividad", "N/D")
        
        # 📉 RIESGO CREDITICIO
        with st.expander("📉 **Riesgo Crediticio y Calidad de Cartera**", expanded=True):
            st.markdown("**Evaluación del riesgo de crédito y calidad de la cartera**")
            
            col_risk1, col_risk2, col_risk3 = st.columns(3)
            
            with col_risk1:
                morosidad = bank_indicators[bank_indicators['nombre_del_indicador'] == 'MOROSIDAD DE LA CARTERA TOTAL']
                if not morosidad.empty:
                    mor_val = morosidad['valor_indicador'].iloc[0]
                    if mor_val <= 3:
                        color = "normal"
                        status = "Saludable"
                    elif mor_val <= 5:
                        color = "off"
                        status = "Aceptable"
                    else:
                        color = "inverse"
                        status = "Alto Riesgo"
                    
                    st.metric(
                        "⚠️ Morosidad",
                        f"{mor_val:.2f}%",
                        f"Riesgo: {status}",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: < 3%")
                else:
                    st.metric("⚠️ Morosidad", "N/D")
            
            with col_risk2:
                cobertura = bank_indicators[bank_indicators['nombre_del_indicador'] == 'COBERTURA DE LA CARTERA IMPRODUCTIVA']
                if not cobertura.empty:
                    cob_val = cobertura['valor_indicador'].iloc[0]
                    color = "normal" if cob_val >= 100 else "inverse"
                    status = "Adecuada" if cob_val >= 100 else "Insuficiente"
                    
                    st.metric(
                        "🛡️ Cobertura",
                        f"{cob_val:.2f}%",
                        f"Estado: {status}",
                        delta_color=color
                    )
                    st.caption("✅ Ideal: ≥ 100%")
                else:
                    st.metric("🛡️ Cobertura", "N/D")
            
            with col_risk3:
                cartera_neta = bank_indicators[bank_indicators['nombre_del_indicador'] == 'CARTERA DE CRÉDITOS NETA']
                cartera_bruta = bank_indicators[bank_indicators['nombre_del_indicador'].str.contains('CARTERA DE CRÉDITOS', na=False) & 
                                               ~bank_indicators['nombre_del_indicador'].str.contains('NETA', na=False)]
                
                if not cartera_neta.empty:
                    cartera_valor = cartera_neta['valor_indicador'].iloc[0]
                    if not activos.empty:
                        concentracion_cartera = (cartera_valor / activos['valor_indicador'].iloc[0]) * 100
                        st.metric(
                            "💼 Concentración Cartera",
                            f"{concentracion_cartera:.1f}%",
                            "Cartera/Activos"
                        )
                        st.caption("💡 Enfoque crediticio")
                    else:
                        st.metric(
                            "💰 Cartera Neta",
                            f"${cartera_valor:,.0f}",
                            "Volumen crediticio"
                        )
                else:
                    st.metric("💼 Calidad Cartera", "N/D")
        
        # 🎯 CRECIMIENTO Y SOSTENIBILIDAD
        with st.expander("🎯 **Crecimiento y Sostenibilidad**", expanded=True):
            st.markdown("**Evaluación de crecimiento equilibrado y sostenibilidad a largo plazo**")
            
            col_grow1, col_grow2, col_grow3 = st.columns(3)
            
            with col_grow1:
                if not activos.empty:
                    activos_sistema = df[df['nombre_del_indicador'] == 'TOTAL ACTIVO']['valor_indicador'].median()
                    tamano_relativo = (activos['valor_indicador'].iloc[0] / activos_sistema) * 100
                    
                    if tamano_relativo >= 100:
                        categoria_tam = "Grande"
                        color = "normal"
                    elif tamano_relativo >= 50:
                        categoria_tam = "Mediano"
                        color = "normal"
                    else:
                        categoria_tam = "Pequeño"
                        color = "off"
                    
                    st.metric(
                        "📏 Tamaño Relativo",
                        f"{tamano_relativo:.0f}%",
                        f"vs mediana ({categoria_tam})",
                        delta_color=color
                    )
                    st.caption("Posición en el mercado")
                else:
                    st.metric("📏 Tamaño Relativo", "N/D")
            
            with col_grow2:
                cartera_neta = bank_indicators[bank_indicators['nombre_del_indicador'] == 'CARTERA DE CRÉDITOS NETA']
                if not cartera_neta.empty and not activos.empty:
                    diversificacion = (cartera_neta['valor_indicador'].iloc[0] / activos['valor_indicador'].iloc[0]) * 100
                    
                    if 50 <= diversificacion <= 80:
                        status = "Equilibrada"
                        color = "normal"
                    else:
                        status = "Concentrada"
                        color = "off"
                    
                    st.metric(
                        "🎯 Enfoque Crediticio",
                        f"{diversificacion:.1f}%",
                        f"Diversificación: {status}",
                        delta_color=color
                    )
                    st.caption("Balance operativo")
                else:
                    st.metric("🎯 Enfoque Crediticio", "N/D")
            
            with col_grow3:
                if not roe.empty and not morosidad.empty:
                    sostenibilidad_ratio = roe['valor_indicador'].iloc[0] / max(morosidad['valor_indicador'].iloc[0], 0.1)
                    
                    if sostenibilidad_ratio >= 5:
                        status = "Alta"
                        color = "normal"
                    elif sostenibilidad_ratio >= 2:
                        status = "Media"
                        color = "off"
                    else:
                        status = "Baja"
                        color = "inverse"
                    
                    st.metric(
                        "🌱 Sostenibilidad",
                        f"{sostenibilidad_ratio:.1f}x",
                        f"Capacidad: {status}",
                        delta_color=color
                    )
                    st.caption("ROE/Morosidad ratio")
                else:
                    st.metric("🌱 Sostenibilidad", "N/D")
        
        st.markdown("---")
        
        # =========================================================
        # COMPARACIÓN CON BENCHMARKS - DESDE API
        # =========================================================
        st.subheader(f"🔍 {selected_bank} vs. Benchmarks del Sistema")
        
        benchmark_data = None
        if api_connected and api_client:
            try:
                benchmark_data = api_client.get_benchmark_analysis(
                    selected_bank,
                    benchmark_type="system_average"
                )
            except:
                pass
        
        if not benchmark_data:
            # Fallback: cálculo local
            benchmark_indicators = ['TOTAL ACTIVO', 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO', 
                                   'RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO', 'MOROSIDAD DE LA CARTERA TOTAL']
            
            comparison_data = []
            
            for indicator in benchmark_indicators:
                bank_value = bank_df[bank_df['nombre_del_indicador'] == indicator]
                system_data = df[df['nombre_del_indicador'] == indicator]
                
                if not bank_value.empty and not system_data.empty:
                    bank_val = bank_value['valor_indicador'].iloc[0]
                    system_avg = system_data['valor_indicador'].mean()
                    system_median = system_data['valor_indicador'].median()
                    
                    comparison_data.append({
                        'Indicador': indicator,
                        'Banco': bank_val,
                        'Promedio Sistema': system_avg,
                        'Mediana Sistema': system_median,
                        'vs Promedio (%)': ((bank_val - system_avg) / system_avg * 100) if system_avg != 0 else 0,
                        'vs Mediana (%)': ((bank_val - system_median) / system_median * 100) if system_median != 0 else 0
                    })
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
            else:
                comparison_df = pd.DataFrame()
        else:
            # Usar datos del API
            comparisons = benchmark_data.get('comparisons', {})
            comparison_data = []
            
            for indicator, data in comparisons.items():
                comparison_data.append({
                    'Indicador': indicator,
                    'Banco': data.get('valor_banco', 0),
                    'Promedio Sistema': data.get('valor_benchmark', 0),
                    'Mediana Sistema': data.get('valor_benchmark', 0),  # API no distingue median
                    'vs Promedio (%)': data.get('desviacion_relativa_pct', 0),
                    'vs Mediana (%)': data.get('desviacion_relativa_pct', 0)
                })
            
            comparison_df = pd.DataFrame(comparison_data)
        
        if not comparison_df.empty:
            # Mostrar tabla de comparación
            st.dataframe(comparison_df.style.format({
                'Banco': '{:.2f}',
                'Promedio Sistema': '{:.2f}',
                'Mediana Sistema': '{:.2f}',
                'vs Promedio (%)': '{:.1f}%',
                'vs Mediana (%)': '{:.1f}%'
            }), use_container_width=True)
            
            # Gráfico de posición relativa
            col_chart_comp, col_analysis = st.columns([3, 1])
            
            with col_chart_comp:
                import plotly.graph_objects as go
                
                fig_benchmark = go.Figure()
                
                fig_benchmark.add_trace(go.Bar(
                    name=selected_bank,
                    x=[ind[:15] + "..." for ind in comparison_df['Indicador']],
                    y=comparison_df['vs Promedio (%)'],
                    marker_color=['green' if x > 0 else 'red' for x in comparison_df['vs Promedio (%)']]
                ))
                
                fig_benchmark.update_layout(
                    title="Diferencia vs Promedio Sistema (%)",
                    xaxis_title="Indicadores",
                    yaxis_title="Diferencia (%)",
                    showlegend=False
                )
                
                st.plotly_chart(fig_benchmark, use_container_width=True)
            
            with col_analysis:
                st.markdown("**🔍 Análisis de Posición**")
                
                # Analizar fortalezas y debilidades
                fortalezas = comparison_df[comparison_df['vs Promedio (%)'] > 5]
                debilidades = comparison_df[comparison_df['vs Promedio (%)'] < -5]
                
                if not fortalezas.empty:
                    st.success("**🟢 Fortalezas:**")
                    for _, row in fortalezas.iterrows():
                        st.write(f"• {row['Indicador'][:20]}...")
                
                if not debilidades.empty:
                    st.warning("**🔴 Áreas de Mejora:**")
                    for _, row in debilidades.iterrows():
                        st.write(f"• {row['Indicador'][:20]}...")
                
                if fortalezas.empty and debilidades.empty:
                    st.info("💡 **Rendimiento equilibrado** con el sistema")
        
        st.markdown("---")
        
        # =========================================================
        # ALERTAS ESPECÍFICAS DEL BANCO - DESDE API
        # =========================================================
        st.subheader(f"🚨 Alertas Específicas: {selected_bank}")
        
        # Intentar obtener alertas desde API
        alerts_data = None
        if api_connected and api_client:
            try:
                all_alerts = api_client.get_system_alerts()
                if all_alerts and 'alerts' in all_alerts:
                    # Filtrar alertas del banco específico
                    bank_alerts = [a for a in all_alerts['alerts'] 
                                  if a.get('banco', '') == selected_bank]
                    
                    if bank_alerts:
                        alerts_data = {'bank_alerts': bank_alerts}
            except:
                pass
        
        if alerts_data and 'bank_alerts' in alerts_data:
            # Mostrar alertas desde API
            for alert in alerts_data['bank_alerts']:
                severity = alert.get('severidad', '')
                message = alert.get('mensaje', '')
                recommendation = alert.get('recomendacion', '')
                
                if "CRÍTICA" in severity:
                    st.error(f"🔴 **{message}**")
                    st.caption(f"💡 {recommendation}")
                elif "ALTA" in severity:
                    st.warning(f"⚠️ **{message}**")
                    st.caption(f"💡 {recommendation}")
                else:
                    st.info(f"ℹ️ **{message}**")
                    st.caption(f"💡 {recommendation}")
        else:
            # Fallback: generar alertas localmente
            bank_alerts = []
            
            # Alert por ROE bajo
            if not roe_bank.empty:
                roe_value = roe_bank['valor_indicador'].iloc[0]
                if roe_value < 10:
                    bank_alerts.append({
                        "type": "warning",
                        "message": f"ROE bajo: {roe_value:.2f}% (recomendado > 10%)",
                        "recommendation": "Revisar estrategias de rentabilidad y eficiencia operativa"
                    })
            
            # Alert por tamaño vs competencia
            if not activos_bank.empty:
                activo_valor = activos_bank['valor_indicador'].iloc[0]
                activos_mediana = df[df['nombre_del_indicador'] == 'TOTAL ACTIVO']['valor_indicador'].median()
                if activo_valor < activos_mediana * 0.5:
                    bank_alerts.append({
                        "type": "info",
                        "message": f"Banco pequeño: 50% menor que la mediana del sistema",
                        "recommendation": "Considerar estrategias de crecimiento o nichos especializados"
                    })
            
            # Alert por morosidad alta
            morosidad_bank = bank_df[bank_df['nombre_del_indicador'] == 'MOROSIDAD DE LA CARTERA TOTAL']
            if not morosidad_bank.empty:
                morosidad_value = morosidad_bank['valor_indicador'].iloc[0]
                if morosidad_value > 5:
                    bank_alerts.append({
                        "type": "error",
                        "message": f"Morosidad alta: {morosidad_value:.2f}% (límite recomendado: 5%)",
                        "recommendation": "Implementar políticas de recuperación y mejores controles de riesgo"
                    })
            
            # Mostrar alertas con recomendaciones
            if bank_alerts:
                for alert in bank_alerts:
                    if alert["type"] == "warning":
                        st.warning(f"⚠️ **{alert['message']}**")
                        st.caption(f"💡 {alert['recommendation']}")
                    elif alert["type"] == "info":
                        st.info(f"ℹ️ **{alert['message']}**")
                        st.caption(f"💡 {alert['recommendation']}")
                    elif alert["type"] == "error":
                        st.error(f"🚨 **{alert['message']}**")
                        st.caption(f"💡 {alert['recommendation']}")
            else:
                st.success("✅ **No se detectaron alertas críticas para este banco**")
                st.caption("💡 El banco muestra indicadores dentro de rangos aceptables")

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.markdown("---")
st.caption("👥 Desarrollado por Grupo 5 — Proyecto Integrador 2025")
st.caption("💡 Dashboard de Salud Financiera - Sistema Bancario Ecuatoriano")
st.caption("📅 Datos: Superintendencia de Bancos - Septiembre 2025")
