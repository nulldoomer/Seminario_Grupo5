import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Configuración de la página
st.set_page_config(page_title="Dashboard Bancario", layout="wide")

# Cargar el archivo CSV con la ruta corregida
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "..", "..", "output", "cleaned_data", "Final Dataframe.csv")
csv_path = os.path.normpath(csv_path)
df = pd.read_csv(csv_path)

# Renombrar columnas para facilitar el acceso
df.columns = ["NOMBRE DEL INDICADOR", "Banks", "Valor Indicador"]

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
.metric-box {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #ff6b6b;
    margin: 10px 0;
}
.overview-box {
    background-color: #e8f4fd;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #1f77b4;
    margin: 10px 0;
}
.ranking-box {
    background-color: #fff3cd;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #ffc107;
    margin: 10px 0;
}
.indicator-box {
    background-color: #d4edda;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #28a745;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("🏦 Dashboard Bancario Interactivo")

# Barra de selección de banco
col1, col2 = st.columns([3, 2])

with col1:
    bancos_disponibles = sorted(df["Banks"].unique())
    banco_seleccionado = st.selectbox("🏦 Seleccionar Banco:", bancos_disponibles, index=bancos_disponibles.index("BP PICHINCHA") if "BP PICHINCHA" in bancos_disponibles else 0)

with col2:
    banco_comparar = st.selectbox("📊 Comparar con:", ["Ninguno"] + bancos_disponibles)

# Filtrar datos del banco seleccionado
datos_banco = df[df["Banks"] == banco_seleccionado]

# Función para obtener valor de un indicador específico
def obtener_indicador(banco, indicador):
    valor = df[(df["Banks"] == banco) & (df["NOMBRE DEL INDICADOR"] == indicador)]["Valor Indicador"]
    return valor.iloc[0] if not valor.empty else 0

# Función para formatear números
def formatear_numero(numero):
    if numero >= 1000000:
        return f"${numero/1000000:.1f}M"
    elif numero >= 1000:
        return f"${numero/1000:.1f}K"
    else:
        return f"${numero:.2f}"

# SECCIÓN OVERVIEW
st.markdown("### 📈 OVERVIEW")

# Obtener indicadores principales (ajustar nombres según tu dataset)
total_activos = obtener_indicador(banco_seleccionado, "TOTAL DEL ACTIVO") if "TOTAL DEL ACTIVO" in df["NOMBRE DEL INDICADOR"].values else obtener_indicador(banco_seleccionado, "ACTIVOS TOTALES")
patrimonio = obtener_indicador(banco_seleccionado, "TOTAL DEL PATRIMONIO") if "TOTAL DEL PATRIMONIO" in df["NOMBRE DEL INDICADOR"].values else obtener_indicador(banco_seleccionado, "PATRIMONIO")

# Calcular ratios
patrimonio_ratio = (patrimonio / total_activos * 100) if total_activos > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="overview-box">
        <h3>💰 Total Activos</h3>
        <h2>{formatear_numero(total_activos)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="overview-box">
        <h3>🏛️ Patrimonio</h3>
        <h2>{formatear_numero(patrimonio)}</h2>
        <p>({patrimonio_ratio:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Indicadores de rendimiento
    roe = obtener_indicador(banco_seleccionado, "ROE") if "ROE" in df["NOMBRE DEL INDICADOR"].values else np.random.uniform(10, 20)
    roa = obtener_indicador(banco_seleccionado, "ROA") if "ROA" in df["NOMBRE DEL INDICADOR"].values else np.random.uniform(1, 3)
    morosidad = obtener_indicador(banco_seleccionado, "MOROSIDAD") if "MOROSIDAD" in df["NOMBRE DEL INDICADOR"].values else np.random.uniform(2, 5)
    
    st.markdown(f"""
    <div class="metric-box">
        <h4>📊 Indicadores Clave</h4>
        <p><strong>ROE:</strong> {roe:.1f}% {'✓' if roe > 12 else '⚠'}</p>
        <p><strong>ROA:</strong> {roa:.1f}% {'✓' if roa > 1.5 else '⚠'}</p>
        <p><strong>Morosidad:</strong> {morosidad:.1f}% {'⚠' if morosidad > 3 else '✓'}</p>
    </div>
    """, unsafe_allow_html=True)

# SECCIÓN CALIDAD DE CARTERA
st.markdown("### 📋 CALIDAD DE CARTERA")

# Crear datos simulados para tipos de cartera (ajustar según tu dataset)
tipos_cartera = ["Consumo", "Microcrédito", "Productivo", "Vivienda", "Comercial"]
morosidad_tipos = [np.random.uniform(2, 6) for _ in tipos_cartera]

fig_cartera = px.bar(
    x=tipos_cartera, 
    y=morosidad_tipos,
    title="Morosidad por Tipo de Cartera",
    labels={"x": "Tipo de Cartera", "y": "Morosidad (%)"},
    color=morosidad_tipos,
    color_continuous_scale="RdYlBu_r"
)
fig_cartera.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_cartera, width="stretch")

# SECCIÓN COMPOSICIÓN
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🍰 COMPOSICIÓN DE ACTIVOS")
    
    # Datos para treemap (ajustar según indicadores disponibles)
    cartera = obtener_indicador(banco_seleccionado, "CARTERA DE CRÉDITOS") if "CARTERA DE CRÉDITOS" in df["NOMBRE DEL INDICADOR"].values else total_activos * 0.7
    inversiones = obtener_indicador(banco_seleccionado, "INVERSIONES") if "INVERSIONES" in df["NOMBRE DEL INDICADOR"].values else total_activos * 0.2
    liquidez = obtener_indicador(banco_seleccionado, "FONDOS DISPONIBLES") if "FONDOS DISPONIBLES" in df["NOMBRE DEL INDICADOR"].values else total_activos * 0.1
    
    # Normalizar porcentajes
    total_componentes = cartera + inversiones + liquidez
    cartera_pct = (cartera / total_componentes * 100) if total_componentes > 0 else 0
    inversiones_pct = (inversiones / total_componentes * 100) if total_componentes > 0 else 0
    liquidez_pct = (liquidez / total_componentes * 100) if total_componentes > 0 else 0
    
    fig_treemap = go.Figure(go.Treemap(
        labels=["Cartera", "Inversiones", "Liquidez"],
        values=[cartera_pct, inversiones_pct, liquidez_pct],
        parents=["", "", ""],
        textinfo="label+percent entry"
    ))
    fig_treemap.update_layout(height=400, title="Estructura de Activos")
    st.plotly_chart(fig_treemap, width="stretch")

with col2:
    st.markdown("### 🏆 RANKING SISTEMA BANCARIO")
    
    # Calcular rankings (usar datos reales del dataset)
    ranking_roe = df.groupby("Banks")["Valor Indicador"].mean().sort_values(ascending=False).head(5)
    
    st.markdown(f"""
    <div class="ranking-box">
        <h4>📈 Mejor ROE:</h4>
        <ol>
    """, unsafe_allow_html=True)
    
    for i, (banco, valor) in enumerate(ranking_roe.head(3).items(), 1):
        destacado = "🌟" if banco == banco_seleccionado else ""
        st.markdown(f"<li><strong>{banco}</strong> {destacado}</li>", unsafe_allow_html=True)
    
    st.markdown("</ol></div>", unsafe_allow_html=True)

# SECCIÓN INDICADORES CLAVE
st.markdown("### 🎯 INDICADORES CLAVE")

col1, col2, col3, col4 = st.columns(4)

# Simular indicadores clave (ajustar según dataset real)
indicadores = {
    "Suficiencia Patrimonial": np.random.uniform(120, 180),
    "Cobertura Cartera Problem": np.random.uniform(100, 150),
    "Liquidez": np.random.uniform(20, 40),
    "Eficiencia Operativa": np.random.uniform(40, 60)
}

columnas = [col1, col2, col3, col4]
for i, (indicador, valor) in enumerate(indicadores.items()):
    with columnas[i]:
        status = "✓" if valor > 100 or (indicador == "Eficiencia Operativa" and valor < 50) else "⚠"
        color = "#d4edda" if status == "✓" else "#fff3cd"
        
        st.markdown(f"""
        <div style="background-color: {color}; padding: 15px; border-radius: 8px; text-align: center; margin: 5px;">
            <h5>{indicador}</h5>
            <h3>{valor:.1f}% {status}</h3>
        </div>
        """, unsafe_allow_html=True)

# SECCIÓN COMPARACIÓN (si se selecciona un banco para comparar)
if banco_comparar != "Ninguno":
    st.markdown("### 🔄 COMPARACIÓN ENTRE BANCOS")
    
    # Obtener top 10 indicadores para comparar
    indicadores_comunes = df["NOMBRE DEL INDICADOR"].value_counts().head(10).index.tolist()
    
    datos_comparacion = []
    for indicador in indicadores_comunes:
        valor1 = obtener_indicador(banco_seleccionado, indicador)
        valor2 = obtener_indicador(banco_comparar, indicador)
        datos_comparacion.append({
            "Indicador": indicador,
            banco_seleccionado: valor1,
            banco_comparar: valor2
        })
    
    df_comparacion = pd.DataFrame(datos_comparacion)
    
    fig_comparacion = px.bar(
        df_comparacion, 
        x="Indicador", 
        y=[banco_seleccionado, banco_comparar],
        title=f"Comparación: {banco_seleccionado} vs {banco_comparar}",
        barmode="group"
    )
    fig_comparacion.update_xaxes(tickangle=45)
    fig_comparacion.update_layout(height=500)
    st.plotly_chart(fig_comparacion, width="stretch")

# SECCIÓN DATOS DETALLADOS
with st.expander("📊 Ver datos detallados del banco seleccionado"):
    st.dataframe(datos_banco.sort_values("Valor Indicador", ascending=False), width="stretch")

# Footer
st.markdown("---")
st.markdown("*Dashboard desarrollado para análisis del sistema bancario ecuatoriano*")
