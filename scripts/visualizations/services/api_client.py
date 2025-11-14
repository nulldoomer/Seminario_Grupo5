"""
🔗 API Client para Dashboard Bancario
Compatible con el ejemplo proporcionado
"""
import requests
import pandas as pd
import streamlit as st
from typing import Optional, Dict, List, Any

class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10

    def get_banks_list(self, categoria: str) -> List[str]:
        """Obtener lista de bancos"""
        try:
            response = self.session.get(f"{self.base_url}/api/banks/list")
            if response.status_code == 200:
                data = response.json()
                return data.get("banks", [])
        except Exception as e:
            st.error(f"Error cargando bancos: {e}")
            return []

    def get_indicators_list(self, categoria: str) -> Dict[str, Any]:
        """Obtener lista de indicadores por categoría"""
        try:
            response = self.session.get(f"{self.base_url}/api/indicators/{categoria}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error cargando indicadores: {e}")
            return {"indicators": [], "category": categoria}

    def get_bank_financials(self, bank_name: str, categoria: str) -> Optional[Dict]:
        """Obtener datos financieros de un banco específico"""
        try:
            params = {"categoria": categoria}
            response = self.session.get(
                f"{self.base_url}/api/banks/{bank_name}/financials", 
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error cargando datos del banco: {e}")
        return None

    def get_ranking(self, indicator: str, categoria: str, limit: Optional[int] = None) -> Optional[Dict]:
        """Obtener ranking de bancos por indicador"""
        try:
            params = {"categoria": categoria}
            if limit:
                params["limit"] = limit
                
            response = self.session.get(
                f"{self.base_url}/api/rankings/{indicator}",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error cargando ranking: {e}")
        return None

    def get_comparative_table(self, categoria: str) -> Optional[Dict]:
        """Obtener tabla comparativa"""
        try:
            params = {"categoria": categoria}
            response = self.session.get(
                f"{self.base_url}/api/comparative/table",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error cargando tabla comparativa: {e}")
        return None

    def get_comparative_statistics(self, categoria: str) -> Optional[Dict]:
        """Obtener estadísticas comparativas"""
        try:
            params = {"categoria": categoria}
            response = self.session.get(
                f"{self.base_url}/api/comparative/statistics",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Error cargando estadísticas: {e}")
        return None

    # Métodos de conversión de datos
    def bank_data_to_dataframe(self, bank_response: Dict) -> pd.DataFrame:
        """Convertir respuesta de bank financials a DataFrame"""
        if "data" in bank_response:
            return pd.DataFrame(bank_response["data"])
        return pd.DataFrame()

    def ranking_to_dataframe(self, ranking_response: Dict) -> pd.DataFrame:
        """Convertir respuesta de ranking a DataFrame"""
        if "data" in ranking_response:
            return pd.DataFrame(ranking_response["data"])
        return pd.DataFrame()

    def comparative_to_dataframe(self, comparative_response: Dict) -> pd.DataFrame:
        """Convertir respuesta comparativa a DataFrame"""
        if "pivot_data" in comparative_response:
            return pd.DataFrame(comparative_response["pivot_data"])
        return pd.DataFrame()

@st.cache_resource
def get_api_client():
    """Función principal para obtener cliente API"""
    return APIClient()
