from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

try:
    from scripts.visualizations.components.data_handler import DataHandler
    from scripts.visualizations.components.metrics_calculator import MetricsCalculator
    from scripts.visualizations.components.indicator_config import IndicatorConfig
    from scripts.visualizations.data_loader import VisualizationDataLoader
except ImportError as e:
    print(f"Error importing components: {e}")

router = APIRouter(prefix="/api", tags=["Dashboard Support"])

# Inicializar componentes
try:
    loader = VisualizationDataLoader()
    dh = DataHandler(loader)
    calc = MetricsCalculator()
    df_original = dh.load_data("Final Dataframe")
    print("✅ Datos cargados exitosamente para dashboard")
except Exception as e:
    print(f"❌ Error cargando datos: {e}")
    dh = None
    df_original = None

@router.get("/banks/list")
def get_banks_list():
    """Obtener lista simple de bancos"""
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    try:
        bancos = list(df_original['banks'].unique())
        return {
            "banks": bancos,
            "total": len(bancos)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/indicators/{categoria}")
def get_indicators_by_category(categoria: str):
    """Obtener indicadores por categoría"""
    if categoria not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(status_code=400, detail="Categoría inválida")
    
    # Mapeo de indicadores por categoría
    indicators_map = {
        "Balance": [
            "activos", "pasivos", "patrimonio", "cartera_de_creditos",
            "depositos_del_publico", "obligaciones_inmediatas"
        ],
        "Rendimiento": [
            "ingresos", "gastos", "resultado_del_ejercicio", "roa", "roe"
        ],
        "Estructura": [
            "indice_de_intermediacion_financiera", "absorcion_del_margen_financiero",
            "gastos_de_operacion_estimados", "cobertura_patrimonial_de_activos"
        ]
    }
    
    indicators = indicators_map.get(categoria, [])
    return {
        "indicators": indicators,
        "category": categoria,
        "total": len(indicators)
    }

@router.get("/banks/{bank_name}/financials")
def get_bank_financials(bank_name: str, categoria: str = Query("Balance")):
    """Obtener datos financieros de un banco específico"""
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    if categoria not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(status_code=400, detail="Categoría inválida")
    
    try:
        # Filtrar datos del banco
        latest_date = df_original['date'].max()
        bank_data = df_original[
            (df_original['bank_name'] == bank_name) & 
            (df_original['date'] == latest_date)
        ]
        
        if bank_data.empty:
            raise HTTPException(status_code=404, detail=f"Banco '{bank_name}' no encontrado")
        
        # Obtener indicadores de la categoría
        indicators_response = get_indicators_by_category(categoria)
        indicators = indicators_response["indicators"]
        
        # Preparar datos
        data = []
        values = []
        
        for indicator in indicators:
            if indicator in bank_data.columns:
                value = float(bank_data[indicator].iloc[0])
                data.append({
                    "nombre_del_indicador": indicator.replace('_', ' ').title(),
                    "valor_indicador": value
                })
                values.append(value)
        
        # Calcular estadísticas
        stats = {
            "total": sum(values) if values else 0,
            "promedio": sum(values) / len(values) if values else 0,
            "desviacion": 0  # Simplificado
        }
        
        return {
            "data": data,
            "stats": stats,
            "is_percentage": categoria == "Rendimiento",
            "unit": "%" if categoria == "Rendimiento" else "$"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/rankings/{indicator}")
def get_ranking(indicator: str, categoria: str = Query("Balance"), limit: Optional[int] = None):
    """Obtener ranking de bancos por indicador"""
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    try:
        latest_date = df_original['date'].max()
        latest_data = df_original[df_original['date'] == latest_date]
        
        if indicator not in latest_data.columns:
            raise HTTPException(status_code=404, detail=f"Indicador '{indicator}' no encontrado")
        
        # Ordenar por indicador
        sorted_data = latest_data.nlargest(limit or 10, indicator)
        
        data = []
        for i, (_, row) in enumerate(sorted_data.iterrows()):
            data.append({
                "banks": row['bank_name'],
                "valor_indicador": float(row[indicator]),
                "ranking": i + 1
            })
        
        return {
            "data": data,
            "indicator": indicator,
            "total_banks": len(latest_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/comparative/table")
def get_comparative_table(categoria: str = Query("Balance")):
    """Obtener tabla comparativa"""
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    try:
        latest_date = df_original['date'].max()
        latest_data = df_original[df_original['date'] == latest_date]
        
        indicators_response = get_indicators_by_category(categoria)
        indicators = indicators_response["indicators"]
        
        # Filtrar indicadores disponibles
        available_indicators = [ind for ind in indicators if ind in latest_data.columns]
        
        if not available_indicators:
            return {"pivot_data": {}}
        
        # Crear pivot
        pivot_data = latest_data.set_index('bank_name')[available_indicators]
        
        return {
            "pivot_data": pivot_data.to_dict('index')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/comparative/statistics")
def get_comparative_statistics(categoria: str = Query("Balance")):
    """Obtener estadísticas comparativas"""
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    try:
        latest_date = df_original['date'].max()
        latest_data = df_original[df_original['date'] == latest_date]
        
        indicators_response = get_indicators_by_category(categoria)
        indicators = indicators_response["indicators"]
        
        # Filtrar indicadores disponibles
        available_indicators = [ind for ind in indicators if ind in latest_data.columns]
        
        if not available_indicators:
            return {"global_stats": {}, "stats_by_bank": {}}
        
        # Estadísticas globales
        all_values = []
        for indicator in available_indicators:
            all_values.extend(latest_data[indicator].dropna().tolist())
        
        import pandas as pd
        series = pd.Series(all_values)
        
        global_stats = {
            "promedio": float(series.mean()) if len(series) > 0 else 0,
            "mediana": float(series.median()) if len(series) > 0 else 0,
            "max": float(series.max()) if len(series) > 0 else 0,
            "min": float(series.min()) if len(series) > 0 else 0,
            "desviacion": float(series.std()) if len(series) > 0 else 0,
            "total": float(series.sum()) if len(series) > 0 else 0
        }
        
        # Estadísticas por banco
        stats_by_bank = {}
        for _, row in latest_data.iterrows():
            bank_name = row['bank_name']
            bank_values = [row[ind] for ind in available_indicators if pd.notna(row[ind])]
            
            if bank_values:
                bank_series = pd.Series(bank_values)
                stats_by_bank[bank_name] = {
                    "promedio": float(bank_series.mean()),
                    "total": float(bank_series.sum()),
                    "cantidad": len(bank_values),
                    "desviacion": float(bank_series.std()) if len(bank_values) > 1 else 0
                }
        
        return {
            "global_stats": global_stats,
            "stats_by_bank": stats_by_bank
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
