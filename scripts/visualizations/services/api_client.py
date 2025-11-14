import requests
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional


class BankApiClient:

    def __init__(self, base_url: str = "http://localhost:8000"):

        self.base_url = base_url
        self.timeout = 30  # segundos

    def get_bank_financials(self, name, category)-> Optional[Dict]:

        try:

            response = requests.get(
                f"{self.base_url}/financials/bank",
                params={"name":name, "category": category},
                timeout= self.timeout
            )

            return response.json()
        
        except Exception as e:

            st.error(f"Ha ocurrido un error al obtener la informacion {e}")

            return None

    def get_ranking(self, kpi, category, ascending)->Optional[Dict]:

        try:

            response = requests.get(
                f"{self.base_url}/financials/rank",
                params={"kpi": kpi, "category": category, "ascending": ascending},
                timeout= self.timeout
            )
            
            return response.json()

        except Exception as e:

            st.error(f"Ha ocurrido un error al obtener la informacion {e}")
            
            return None

    def get_banks_list(self, category):

        try:
            response = requests.get(
                f"{self.base_url}/financials/banks",
                params={"category": category},
                timeout=self.timeout
            )
            
            data = response.json()
            return data.get("banks", [])
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error obteniendo lista de bancos: {e}")
            return None


    def get_indicators_list(self, category):

        try:

            response = requests.get(
                f"{self.base_url}/financials/indicators",
                params={"category": category},
                timeout= self.timeout
            )

            return response.json()

        except Exception as e:

            st.error(f"Ha ocurrido un error al obtener la informacion {e}")
            
            return None


    def get_comparative_table(self, category, banks: Optional[List[str]] = None):

        try:

            response = requests.get(
                f"{self.base_url}/financials/comparative",
                params={"category": category, "banks": banks},
                timeout= self.timeout
            )

            return response.json()

        except Exception as e:

            st.error(f"Ha ocurrido un error al obtener la informacion {e}")
            
            return None

    def get_comparative_statistics(self, category):

        try:

            response = requests.get(
                f"{self.base_url}/financials/comparative",
                params={"category": category},
                timeout= self.timeout
            )

            return response.json()

        except Exception as e:

            st.error(f"Ha ocurrido un error al obtener la informacion {e}")
            
            return None


    def bank_data_to_dataframe(self, response_data: Dict) -> pd.DataFrame:

        if response_data and "data" in response_data:

            return pd.DataFrame(response_data["data"])

        return pd.DataFrame()
    
    def ranking_to_dataframe(self, response_data: Dict) -> pd.DataFrame:

        if response_data and "ranking" in response_data:

            return pd.DataFrame(response_data["ranking"])

        return pd.DataFrame()

    def comparative_to_dataframe(self, response_data: Dict) -> pd.DataFrame:

        if response_data and "data" in response_data:

            df = pd.DataFrame.from_dict(response_data["data"], orient='index')

            return df

        return pd.DataFrame()


    def get_system_alerts(self, severity: Optional[str] = None):
        """Obtiene alertas del sistema"""
        params = {"severity": severity} if severity else {}
        response = requests.get(
            f"{self.base_url}/advanced/alerts",
            params=params
        )
        return response.json()
    
    def get_market_concentration(self, metric: str = "TOTAL ACTIVO"):
        """Obtiene análisis de concentración"""
        response = requests.get(
            f"{self.base_url}/advanced/concentration",
            params={"metric": metric}
        )
        return response.json()
    
    def get_peer_groups(self, size_metric: str = "TOTAL ACTIVO"):
        """Obtiene peer groups"""
        response = requests.get(
            f"{self.base_url}/advanced/peer-groups",
            params={"size_metric": size_metric}
        )
        return response.json()
    
    def get_correlations(self):
        """Obtiene matriz de correlaciones"""
        response = requests.get(f"{self.base_url}/advanced/correlations")
        return response.json()
    
    def get_benchmark_analysis(self, bank_name: str, benchmark_type: str = "system_average"):
        """Obtiene análisis de benchmark para un banco"""
        response = requests.get(
            f"{self.base_url}/advanced/benchmark/{bank_name}",
            params={"benchmark_type": benchmark_type}
        )
        return response.json()
    
    def get_system_overview(self):
        """Obtiene overview general del sistema"""
        response = requests.get(f"{self.base_url}/advanced/overview")
        return response.json()


@st.cache_resource
def get_api_client(base_url: str = "http://localhost:8000") -> BankApiClient:

    return BankApiClient(base_url)
