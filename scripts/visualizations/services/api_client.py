"""
🔗 API Client para Dashboard Bancario
Compatible con múltiples entornos
"""
import requests
import pandas as pd
import streamlit as st
import os
from typing import Optional, Dict, List, Any

class APIClient:
    def __init__(self, base_url: Optional[str] = None):
        """
        Inicializar cliente API con detección automática de entorno
        
        Args:
            base_url: URL base del API. Si no se provee, usa variables de entorno o default local
        """
        if base_url:
            self.base_url = base_url
        else:
            # Prioridad de configuración:
            # 1. Variable de entorno API_URL
            # 2. Streamlit secrets (para deployment)
            # 3. Default local
            self.base_url = self._get_api_url()
            
        self.session = requests.Session()
        self.session.timeout = 10
        
    def _get_api_url(self) -> str:
        """Detectar URL del API basado en el entorno"""
        
        # 1. Variable de entorno
        if os.getenv("API_URL"):
            return os.getenv("API_URL")
            
        # 2. Streamlit secrets (para deployment)
        try:
            if hasattr(st, "secrets") and "api_url" in st.secrets:
                return st.secrets["api_url"]
        except:
            pass
            
        # 3. Detectar si estamos en producción (Streamlit Cloud, Railway, etc.)
        if os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud":
            # URL de producción por defecto
            return "https://bank-api-service-216433300622.us-central1.run.app"
            
        # 4. Default local
        return "http://127.0.0.1:8000"

    def test_connection(self) -> Dict[str, Any]:
        """
        Probar la conexión al API
        
        Returns:
            Dict con información sobre el estado de la conexión
        """
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                return {
                    "connected": True,
                    "status": "✅ Conectado",
                    "url": self.base_url,
                    "response_time": response.elapsed.total_seconds(),
                    "message": "API funcionando correctamente"
                }
            else:
                return {
                    "connected": False,
                    "status": f"❌ Error {response.status_code}",
                    "url": self.base_url,
                    "message": f"API devolvió código {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "connected": False,
                "status": "🔴 Sin conexión",
                "url": self.base_url,
                "message": f"Error de conexión: {str(e)}"
            }

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
    """
    Función principal para obtener cliente API
    
    Returns:
        APIClient configurado para el entorno actual
    """
    client = APIClient()
    
    # Mostrar información del entorno en el sidebar si es posible
    try:
        if hasattr(st, "sidebar"):
            connection_info = client.test_connection()
            if connection_info["connected"]:
                st.sidebar.success(f"{connection_info['status']}")
                st.sidebar.caption(f"🌐 {connection_info['url']}")
                st.sidebar.caption(f"⚡ {connection_info['response_time']:.2f}s")
            else:
                st.sidebar.error(f"{connection_info['status']}")
                st.sidebar.caption(f"🌐 {connection_info['url']}")
                st.sidebar.caption(f"💡 {connection_info['message']}")
    except:
        pass
        
    return client


def get_api_client_with_url(url: str):
    """
    Obtener cliente API con URL específica
    
    Args:
        url: URL específica del API
        
    Returns:
        APIClient con URL personalizada
    """
    return APIClient(base_url=url)
