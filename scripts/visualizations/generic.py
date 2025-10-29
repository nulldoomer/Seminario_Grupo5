import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Cargar el archivo CSV
# Obtener la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta hacia el archivo CSV desde la ubicación del script
csv_path = os.path.join(script_dir, "..", "..", "output", "cleaned_data", "Final Dataframe.csv")
# Normalizar la ruta para resolver los '..'
csv_path = os.path.normpath(csv_path)
df = pd.read_csv(csv_path)

# Renombrar columnas para facilitar el acceso
df.columns = ["NOMBRE DEL INDICADOR", "Banks", "Valor Indicador"]

# Título del dashboard
st.title("Dashboard Financiero Interactivo")
st.markdown("Visualizaciones dinámicas por banco y tipo de indicador financiero")

# Filtros en la barra lateral
selected_bank = st.sidebar.selectbox("Selecciona un banco", sorted(df["Banks"].unique()))
selected_indicador = st.sidebar.selectbox("Selecciona un indicador", sorted(df["NOMBRE DEL INDICADOR"].unique()))

# Filtrar datos según selección
filtered_df = df[(df["Banks"] == selected_bank) & (df["NOMBRE DEL INDICADOR"] == selected_indicador)]

# Mostrar datos filtrados
st.subheader(f"Datos para {selected_bank} - {selected_indicador}")
st.dataframe(filtered_df)

# Gráfico de indicadores del banco seleccionado
bank_df = df[df["Banks"] == selected_bank]
fig_bank = px.bar(bank_df, x="NOMBRE DEL INDICADOR", y="Valor Indicador",
                  title=f"Indicadores Financieros - {selected_bank}",
                  labels={"Valor Indicador": "Valor"})
st.plotly_chart(fig_bank)

# Gráfico comparativo entre bancos para el indicador seleccionado
indicador_df = df[df["NOMBRE DEL INDICADOR"] == selected_indicador]
fig_indicador = px.bar(indicador_df, x="Banks", y="Valor Indicador",
                       title=f"Comparación entre Bancos - {selected_indicador}",
                       labels={"Valor Indicador": "Valor"})
st.plotly_chart(fig_indicador)