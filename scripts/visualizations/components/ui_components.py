import streamlit as st
import pandas as pd

class UIComponents:

    @staticmethod
    def render_metric_cards(
        total_bancos,
        total_indicadores,
        total_valor,
        promedio,
        is_percentage: bool = False
    ):

        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            st.metric("Bancos", total_bancos)

        with col_b:
            st.metric("Indicadores", total_indicadores)


        with col_c:

            if is_percentage:

                st.metric("Suma Total", f"{total_valor:.2f}%")
            else:

                st.metric("Suma Total", f"${total_valor:,.0f}")
        
        with col_d:

            if is_percentage:

                st.metric("Promedio", f"{promedio:.2f}%")
            else:

                st.metric("Promedio", f"${promedio:,.2f}")

    @staticmethod
    def render_top3_medals(
        df: pd.DataFrame,
        bank_col: str = "banks",
        value_col: str = "valor_indicador",
        is_percentage: bool = False
    ):

        medals = ["1st", "2nd", "3rd"]

        for idx in range(min(3, len(df))):

            medal = medals[idx]
            banco = str(df.iloc[idx][bank_col])
            valor = float(df.iloc[idx][value_col])

            if is_percentage:
                st.metric(f"{medal} {banco}", f"{valor:.2f}%")
            else:
                st.metric(f"{medal} {banco}", f"${valor:,.0f}")


    @staticmethod
    def render_bottom3(
        df: pd.DataFrame,
        n: int = 3,
        bank_col: str = "banks",
        value_col: str = "valor_indicador",
        is_percentage: bool = False
    ):

        st.markdown("### Bottom 3")

        start_idx = max(0, len(df) - n)

        for idx in range(start_idx, len(df)):
            banco = str(df.iloc[idx][bank_col])
            valor = float(df.iloc[idx][value_col])
            posicion = idx + 1
            
            if is_percentage:
                st.caption(f"#{posicion}. {banco}: {valor:.2f}%")
            else:
                st.caption(f"#{posicion}. {banco}: ${valor:,.0f}")

    @staticmethod
    def render_download_button(
        df: pd.DataFrame,
        filename: str,
        label: str = "Descargar CSV"
    ):

        csv = df.to_csv().encode("utf-8")

        st.download_button(
            label=label,
            data=csv,
            file_name=filename,
            mime="text/csv"
        )
