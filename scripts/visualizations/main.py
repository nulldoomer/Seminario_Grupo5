from data_loader import VisualizationsDataLoader
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Dashboard Financiero",
    layout="wide"
)

INDICADORES_BALANCE = {
    "FONDOS DISPONIBLES": "Liquidez inmediata",
    "INVERSIONES": "Activos financieros",
    "CARTERA DE CRÉDITOS": "Préstamos otorgados",
    "DEUDORES POR ACEPTACIONES": "Compromisos de pago",
    "CUENTAS POR COBRAR": "Cuentas pendientes",
    "PROPIEDADES Y EQUIPO": "Activos fijos",
    "OTROS ACTIVOS": "Activos diversos"
}

INDICADORES_RENDIMIENTO = {
    "RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO": "ROA - Rentabilidad",
    "RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO": "ROE - Rentabilidad",
    "MOROSIDAD DE LA CARTERA TOTAL": "Calidad de cartera",
    "ACTIVOS PRODUCTIVOS / TOTAL ACTIVOS": "Eficiencia activos",
    "FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO": "Liquidez",
    "GASTOS DE OPERACION ESTIMADOS / TOTAL ACTIVO PROMEDIO (3)": "Eficiencia operativa"
}

INDICADORES_ESTRUCTURA = {
    "TOTAL ACTIVO": "Tamaño del banco",
    "TOTAL PATRIMONIO": "Capital propio",
    "TOTAL PASIVOS": "Obligaciones totales",
    "OBLIGACIONES CON EL PÚBLICO": "Depósitos captados",
    "CAPITAL SOCIAL": "Capital accionario"
}

@st.cache_data
def load_data(path):
    try:
        dataframe= pd.read_csv(path)

        # Normalize the columns
        
        dataframe.columns = (
            dataframe.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("á", "a")
            .str.replace("é", "e")
            .str.replace("í", "i")
            .str.replace("ó", "o")
            .str.replace("ú", "u")
        )
        
        return dataframe 
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

@st.cache_data
def filtrar_indicadores(dataframe, indicadores_dict, is_percentage=False):

    # To make this we need the dataframe, the dictionary of the indicadores,
    # where we're going to take only the keys and turn it into a list
    # then take only the rows that has the list of indicadores

    indicadores_list = list(indicadores_dict.keys())
    df_filtered = dataframe[dataframe["nombre_del_indicador"].isin(indicadores_list)].copy()

    # In a part of the union of the dataframes, there are values of the 
    # indicadores that are in float because its percentage values,
    # so we use our flag is_percentage and a check if its not empty
    # we take the values and we'll transform it into percentage multiplying
    # by 100 and return the data

    if is_percentage and not df_filtered.empty:
        df_filtered["valor_indicador"] = df_filtered["valor_indicador"] * 100
    
    return df_filtered

data_loader = VisualizationsDataLoader()
file_name = "Final Dataframe"
path = data_loader.load(file_name)

dataframe = load_data(path)

if dataframe is None:
    st.stop()

if "nombre_del_indicador" not in dataframe.columns:
    st.error("La columna 'nombre_del_indicador' no existe en el dataset")
    st.info("Columnas disponibles: " + ", ".join(dataframe.columns))
    st.stop()

st.title("Dashboard Financiero Bancario")
st.markdown("""
**Análisis integral del Sistema Bancario Ecuatoriano**  
Dashboard interactivo para evaluar indicadores de Balance, Rendimiento y Estructura Financiera.
""")

with st.sidebar:
    st.header("Panel de Control")
    st.markdown("---")
    
    category = st.radio(
        "Categoría de Análisis",
        ["Balance", "Rendimiento", "Estructura"],
        help="Selecciona el tipo de indicadores a analizar"
    )
    
    # Determinar qué indicadores usar según categoría
    if category == "Balance":
        indicadores_activos = INDICADORES_BALANCE
        is_percentage = False
        unidad = "$"
        st.info("**Balance:** Activos y recursos del banco")
    elif category == "Rendimiento":
        indicadores_activos = INDICADORES_RENDIMIENTO
        is_percentage = True
        unidad = "%"
        st.info("**Rendimiento:** Rentabilidad y eficiencia")
    else:
        indicadores_activos = INDICADORES_ESTRUCTURA
        is_percentage = False
        unidad = "$"
        st.info("**Estructura:** Composición financiera")
    
    # Filtrar datos según categoría
    filtered_df = filtrar_indicadores(dataframe, indicadores_activos, is_percentage)
    
    if filtered_df.empty:
        st.error(f"No hay datos para la categoría {category}")
        st.stop()
    
    st.markdown("---")
    
    # Selector de banco
    bancos = sorted(filtered_df["banks"].unique())
    selected_bank = st.selectbox(
        "Selecciona un Banco",
        bancos,
        help="Elige el banco a analizar"
    )
    
    st.markdown("")
    
    indicadores = sorted(filtered_df["nombre_del_indicador"].unique())
    selected_indicator = st.selectbox(
        "Selecciona un Indicador",
        indicadores,
        help="Indicador específico para ranking"
    )
    
    st.markdown("---")
    
    # Información adicional
    st.caption(f"📌 **Indicadores activos:** {len(indicadores_activos)}")
    st.caption(f"🏦 **Bancos analizados:** {len(bancos)}")
    st.caption(f"📅 **Periodo:** Septiembre 2025")




col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    total_bancos = filtered_df["banks"].nunique()
    st.metric("🏦 Bancos", total_bancos)

with col_b:
    total_indicadores = len(indicadores_activos)
    st.metric("📊 Indicadores", total_indicadores)

with col_c:
    total_valor = filtered_df["valor_indicador"].sum()
    if is_percentage:
        st.metric("📊 Suma Total", f"{total_valor:.2f}%")
    else:
        st.metric("💵 Suma Total", f"${total_valor:,.0f}")

with col_d:
    promedio = filtered_df["valor_indicador"].mean()
    if is_percentage:
        st.metric("📈 Promedio", f"{promedio:.2f}%")
    else:
        st.metric("📈 Promedio", f"${promedio:,.2f}")

st.markdown("---")

st.subheader(f"📈 Perfil Financiero: {selected_bank}")

col_left, col_right = st.columns([2, 1])

with col_left:
    bank_data = filtered_df[filtered_df["banks"] == selected_bank].sort_values(
        by="valor_indicador", ascending=False
    )

    if not bank_data.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.barh(
            bank_data["nombre_del_indicador"],
            bank_data["valor_indicador"],
            color="#2E86AB"
        )
        
        # Añadir valores en las barras
        for bar in bars:
            width = bar.get_width()
            if is_percentage:
                ax.text(
                    width,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width:.2f}%',
                    ha='left',
                    va='center',
                    fontsize=9,
                    fontweight='bold'
                )
            else:
                ax.text(
                    width,
                    bar.get_y() + bar.get_height() / 2,
                    f'${width:,.0f}',
                    ha='left',
                    va='center',
                    fontsize=9,
                    fontweight='bold'
                )
        
        ax.set_xlabel(
            f"Valor del Indicador ({unidad})", 
            fontsize=11, 
            fontweight='bold'
        )
        ax.set_title(
            f"Indicadores de {category} - {selected_bank}",
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("No hay datos disponibles para este banco.")

with col_right:
    if not bank_data.empty:
        st.markdown("### Resumen")
        
        indicador_max = bank_data.loc[bank_data["valor_indicador"].idxmax()]
        indicador_min = bank_data.loc[bank_data["valor_indicador"].idxmin()]
        
        if is_percentage:
            st.metric(
                "Indicador Mayor",
                f"{indicador_max['valor_indicador']:.2f}%",
                indicador_max['nombre_del_indicador'][:30] + "..."
            )
            
            st.metric(
                "Indicador Menor",
                f"{indicador_min['valor_indicador']:.2f}%",
                indicador_min['nombre_del_indicador'][:30] + "..."
            )
        else:
            st.metric(
                "Indicador Mayor",
                f"${indicador_max['valor_indicador']:,.0f}",
                indicador_max['nombre_del_indicador'][:30] + "..."
            )
            
            st.metric(
                "Indicador Menor",
                f"${indicador_min['valor_indicador']:,.0f}",
                indicador_min['nombre_del_indicador'][:30] + "..."
            )

st.markdown("---")

st.subheader(f"Ranking: {selected_indicator}")

ranking_df = (
    filtered_df[filtered_df["nombre_del_indicador"] == selected_indicator]
    .sort_values(by="valor_indicador", ascending=False)
    .reset_index(drop=True)
)

if not ranking_df.empty:
    col_chart, col_top = st.columns([2, 1])
    
    with col_chart:
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        colors = sns.color_palette("viridis", n_colors=len(ranking_df))
        
        bars = ax2.barh(
            ranking_df["banks"],
            ranking_df["valor_indicador"],
            color=colors
        )
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            if is_percentage:
                ax2.text(
                    width,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width:.2f}%',
                    ha='left',
                    va='center',
                    fontsize=8,
                    fontweight='bold'
                )
            else:
                ax2.text(
                    width,
                    bar.get_y() + bar.get_height() / 2,
                    f'${width:,.0f}',
                    ha='left',
                    va='center',
                    fontsize=8,
                    fontweight='bold'
                )
        
        ax2.set_xlabel(
            f"Valor del Indicador ({unidad})", 
            fontsize=11, 
            fontweight='bold'
        )
        ax2.set_title(
            f"Ranking: {selected_indicator}",
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax2.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)
    
    with col_top:
        st.markdown("### 🎖️ Top 3")
        
        for idx in range(min(3, len(ranking_df))):
            medal = ["🥇", "🥈", "🥉"][idx]
            banco = ranking_df.iloc[idx]['banks']
            valor = ranking_df.iloc[idx]['valor_indicador']
            
            if is_percentage:
                st.metric(f"{medal} {banco}", f"{valor:.2f}%")
            else:
                st.metric(f"{medal} {banco}", f"${valor:,.0f}")
        
        st.markdown("---")
        st.markdown("### 📉 Bottom 3")
        
        for idx in range(max(0, len(ranking_df) - 3), len(ranking_df)):
            banco = ranking_df.iloc[idx]['banks']
            valor = ranking_df.iloc[idx]['valor_indicador']
            posicion = idx + 1
            
            if is_percentage:
                st.caption(f"#{posicion}. {banco}: {valor:.2f}%")
            else:
                st.caption(f"#{posicion}. {banco}: ${valor:,.0f}")
else:
    st.warning("No hay datos disponibles para este indicador.")

st.markdown("---")

