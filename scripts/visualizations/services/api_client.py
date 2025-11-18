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
            base_url: URL base del API. Si no se provee, usa variables de entorno o default
        """
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = self._get_api_url()
            
        self.session = requests.Session()
        self.session.timeout = 10
        
    def _get_api_url(self) -> str:
        """Detectar URL del API basado en el entorno"""
        
        # 1. Variable de entorno
        if os.getenv("API_URL"):
            return os.getenv("API_URL")
            
        # 2. Streamlit secrets
        try:
            if hasattr(st, "secrets") and "api_url" in st.secrets:
                return st.secrets["api_url"]
        except:
            pass
            
        # 3. Detectar API local
        try:
            local_response = requests.get("http://localhost:8000/health", timeout=2)
            if local_response.status_code == 200:
                return "http://localhost:8000"
        except:
            pass
            
        # 4. Producción
        if os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud":
            return "https://bank-api-service-216433300622.us-central1.run.app"
            
        # 5. Default
        return "https://bank-api-service-216433300622.us-central1.run.app"

    def test_connection(self) -> Dict[str, Any]:
        """Probar la conexión al API"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                return {
                    "connected": True,
                    "status": "success",
                    "url": self.base_url,
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "connected": False,
                    "status": f"error_{response.status_code}",
                    "url": self.base_url
                }
        except requests.exceptions.RequestException:
            return {
                "connected": False,
                "status": "no_connection",
                "url": self.base_url
            }

    # =====================================================
    # MÉTODOS BÁSICOS (ya existentes)
    # =====================================================
    
    def get_banks_list(self, categoria: str = "Balance") -> Dict[str, Any]:
        """Obtener lista de bancos"""
        try:
            response = self.session.get(f"{self.base_url}/api/banks/list")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error cargando bancos: {e}")
        return {"banks": []}

    def get_indicators_list(self, categoria: str) -> Dict[str, Any]:
        """Obtener lista de indicadores por categoría"""
        try:
            response = self.session.get(f"{self.base_url}/api/indicators/{categoria}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error cargando indicadores: {e}")
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
            print(f"Error cargando datos del banco: {e}")
        return None

    # =====================================================
    # MÉTODOS AVANZADOS - ANALYTICS
    # =====================================================
    
    def get_system_overview(self) -> Optional[Dict]:
        """
        Obtener resumen ejecutivo del sistema bancario
        
        Returns:
            Dict con estadísticas generales, concentración, alertas y top performers
        """
        try:
            response = self.session.get(f"{self.base_url}/advanced/overview")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo overview: {e}")
        return None
    
    def get_system_alerts(self, severity: Optional[str] = None) -> Optional[Dict]:
        """
        Obtener alertas del sistema
        
        Args:
            severity: Filtrar por severidad (CRITICA, ALTA, MEDIA)
            
        Returns:
            Dict con alertas categorizadas por severidad
        """
        try:
            params = {"severity": severity} if severity else {}
            response = self.session.get(
                f"{self.base_url}/advanced/alerts",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo alertas: {e}")
        return None
    
    def get_market_concentration(self, metric: str = "TOTAL ACTIVO") -> Optional[Dict]:
        """
        Obtener análisis de concentración de mercado
        
        Args:
            metric: Métrica para calcular concentración
            
        Returns:
            Dict con CR3, CR5, HHI y top bancos
        """
        try:
            params = {"metric": metric}
            response = self.session.get(
                f"{self.base_url}/advanced/concentration",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo concentración: {e}")
        return None
    
    def get_peer_groups(self, size_metric: str = "TOTAL ACTIVO") -> Optional[Dict]:
        """
        Obtener grupos de bancos por tamaño
        
        Args:
            size_metric: Métrica para clasificar tamaño
            
        Returns:
            Dict con grupos de bancos (Grandes, Medianos, Pequeños)
        """
        try:
            params = {"size_metric": size_metric}
            response = self.session.get(
                f"{self.base_url}/advanced/peer-groups",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo peer groups: {e}")
        return None
    
    def get_correlations(self) -> Optional[Dict]:
        """
        Obtener matriz de correlación entre indicadores
        
        Returns:
            Dict con matriz de correlación y correlaciones fuertes
        """
        try:
            response = self.session.get(f"{self.base_url}/advanced/correlations")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo correlaciones: {e}")
        return None
    
    def get_benchmark_analysis(self, bank_name: str, 
                              benchmark_type: str = "system_average") -> Optional[Dict]:
        """
        Comparar banco contra benchmarks
        
        Args:
            bank_name: Nombre del banco
            benchmark_type: Tipo de benchmark (system_average, top_quartile, median)
            
        Returns:
            Dict con comparaciones por indicador
        """
        try:
            params = {"benchmark_type": benchmark_type}
            response = self.session.get(
                f"{self.base_url}/advanced/benchmark/{bank_name}",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo benchmark: {e}")
        return None
    
    def get_derived_indicators(self, bank_name: Optional[str] = None) -> Optional[Dict]:
        """
        Obtener indicadores derivados y compuestos
        
        Args:
            bank_name: Filtrar por banco específico (opcional)
            
        Returns:
            Dict con indicadores derivados e índices compuestos
        """
        try:
            params = {"bank_name": bank_name} if bank_name else {}
            response = self.session.get(
                f"{self.base_url}/advanced/derived-indicators",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo indicadores derivados: {e}")
        return None
    
    def get_system_statistics(self) -> Optional[Dict]:
        """
        Obtener estadísticas detalladas del sistema
        
        Returns:
            Dict con estadísticas por cada indicador
        """
        try:
            response = self.session.get(f"{self.base_url}/advanced/system-statistics")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
        return None
    
    def get_market_share(self, metric: str = "TOTAL ACTIVO", 
                        top_n: int = 10) -> Optional[Dict]:
        """
        Obtener participación de mercado
        
        Args:
            metric: Métrica para calcular participación
            top_n: Número de top bancos
            
        Returns:
            Dict con participación de mercado
        """
        try:
            params = {"metric": metric, "top_n": top_n}
            response = self.session.get(
                f"{self.base_url}/advanced/market-share",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo market share: {e}")
        return None
    
    def get_outliers(self, method: str = "iqr", 
                    indicator: Optional[str] = None) -> Optional[Dict]:
        """
        Detectar outliers
        
        Args:
            method: Método de detección (iqr o zscore)
            indicator: Filtrar por indicador específico
            
        Returns:
            Dict con outliers detectados
        """
        try:
            params = {"method": method}
            if indicator:
                params["indicator"] = indicator
            response = self.session.get(
                f"{self.base_url}/advanced/outliers",
                params=params
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error detectando outliers: {e}")
        return None

    # =====================================================
    # MÉTODOS DE CONVERSIÓN A DATAFRAME
    # =====================================================
    
    def overview_to_dataframe(self, overview: Dict) -> Dict[str, pd.DataFrame]:
        """Convertir overview a múltiples DataFrames"""
        dfs = {}
        
        if "top_performers" in overview:
            performers = overview["top_performers"]
            if "by_assets" in performers:
                dfs["top_by_assets"] = pd.DataFrame(performers["by_assets"])
            if "by_roe" in performers:
                dfs["top_by_roe"] = pd.DataFrame(performers["by_roe"])
        
        return dfs
    
    def concentration_to_dataframe(self, concentration: Dict) -> pd.DataFrame:
        """Convertir datos de concentración a DataFrame"""
        if "top_banks" in concentration:
            return pd.DataFrame(concentration["top_banks"])
        return pd.DataFrame()
    
    def correlation_to_dataframe(self, correlation: Dict) -> pd.DataFrame:
        """Convertir matriz de correlación a DataFrame"""
        if "correlation_matrix" in correlation:
            return pd.DataFrame(correlation["correlation_matrix"])
        return pd.DataFrame()
    
    def market_share_to_dataframe(self, market_share: Dict) -> pd.DataFrame:
        """Convertir market share a DataFrame"""
        if "market_share" in market_share:
            return pd.DataFrame(market_share["market_share"])
        return pd.DataFrame()


@st.cache_resource
def get_api_client() -> APIClient:
    """
    Función principal para obtener cliente API (cached)
    
    Returns:
        APIClient configurado para el entorno actual
    """
    return APIClient()


def get_api_client_with_url(url: str) -> APIClient:
    """
    Obtener cliente API con URL específica
    
    Args:
        url: URL específica del API
        
    Returns:
        APIClient con URL personalizada
    """
    return APIClient(base_url=url)
