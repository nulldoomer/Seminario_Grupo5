import requests
import pandas as pd
import streamlit as st
from typing import Dict, Optional


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
                timeout= self.timeout
            )

            return response.json()

        except Exception as e:

            st.error(f"Ha ocurrido un error al obtener la informacion {e}")
            
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


    def get_comparative_table(self, category, banks):

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

@st.cache_resource
def get_api_client(base_url: str = "http://localhost:8000") -> BankApiClient:

    return BankApiClient(base_url)
