from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
import sys
from pathlib import Path

# Agregar path de components
sys.path.append(str(Path(__file__).parent.parent.parent))

from api.schemas import (
    AlertsResponse,
    ConcentrationResponse,
    PeerGroupResponse,
    BenchmarkResponse,
    CorrelationResponse,
    DerivedIndicatorsResponse,
    SystemStatisticsResponse
)

from scripts.visualizations.components.data_handler import DataHandler
from scripts.visualizations.components.advanced_metrics import AdvancedMetrics
from scripts.visualizations.components.analysis_engine import TrendAnalysis
from scripts.visualizations.data_loader import VisualizationDataLoader

router = APIRouter(
    prefix="/advanced",
    tags=["Advanced Analytics"],
    responses={404: {"description": "Not found"}}
)

print("🔄 Inicializando componentes avanzados...")
loader = VisualizationDataLoader()
dh = DataHandler(loader)
df_original = dh.load_data("Final Dataframe")

# Enriquecer datos con métricas avanzadas
if df_original is not None:
    df_enriched = AdvancedMetrics.calculate_derived_indicators(df_original)
    df_enriched = AdvancedMetrics.calculate_composite_indices(df_enriched)
    print(f"✅ Datos enriquecidos: {len(df_enriched)} registros")
else:
    df_enriched = None
    print("❌ Error: No se pudieron cargar los datos")


# =========================================================
# ENDPOINT 1: Generar Alertas del Sistema
# =========================================================
@router.get("/alerts", response_model=AlertsResponse)
def get_system_alerts(
    severity: Optional[str] = Query(None, description="Filtrar por severidad: CRITICA (o CRÍTICA), ALTA, MEDIA")
):
    """
    Genera alertas automáticas del sistema bancario
    basadas en thresholds regulatorios.
    
    **Tipos de alertas:**
    - Riesgo Crediticio (Morosidad > 5%)
    - Liquidez (Ratio < 10%)
    - Rentabilidad (ROE negativo)
    - Solvencia (Patrimonio/Activos < 9%)
    - Eficiencia (Gastos/Ingresos > 70%)
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    # Generar alertas
    alerts = TrendAnalysis.generate_alerts(df_enriched)
    
    # Filtrar por severidad si se especifica
    if severity:
        severity_upper = severity.upper()
        # Mapear entrada del usuario al formato real de severidad
        severity_map = {
            'CRITICA': 'CRÍTICA',
            'CRÍTICA': 'CRÍTICA',
            'ALTA': 'ALTA',
            'MEDIA': 'MEDIA'
        }
        severity_to_find = severity_map.get(severity_upper, severity_upper)
        alerts = [a for a in alerts if severity_to_find in a.get('severidad', '')]
    
    # Agrupar por severidad
    criticas = [a for a in alerts if "CRÍTICA" in a.get('severidad', '')]
    altas = [a for a in alerts if "ALTA" in a.get('severidad', '')]
    medias = [a for a in alerts if "MEDIA" in a.get('severidad', '')]
    
    return {
        "total_alerts": len(alerts),
        "critical_count": len(criticas),
        "high_count": len(altas),
        "medium_count": len(medias),
        "alerts": alerts,
        "summary": {
            "critical": criticas,
            "high": altas,
            "medium": medias
        }
    }


# =========================================================
# ENDPOINT 2: Análisis de Concentración de Mercado
# =========================================================
@router.get("/concentration", response_model=ConcentrationResponse)
def get_market_concentration(
    metric: str = Query("TOTAL ACTIVO", description="Métrica para análisis de concentración")
):
    """
    Calcula índices de concentración del mercado bancario.
    
    **Métricas calculadas:**
    - CR3: Participación de los 3 bancos más grandes
    - CR5: Participación de los 5 bancos más grandes
    - HHI: Índice Herfindahl-Hirschman
    
    **Interpretación HHI:**
    - < 1500: Mercado Competitivo
    - 1500-2500: Moderadamente Concentrado
    - > 2500: Altamente Concentrado
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    # Calcular concentración
    concentration_data = TrendAnalysis.calculate_concentration_risk(df_enriched)
    
    if not concentration_data or metric not in concentration_data:
        raise HTTPException(
            status_code=404,
            detail=f"No hay datos de concentración para {metric}"
        )
    
    data = concentration_data[metric]
    
    # Obtener top bancos
    metric_data = df_enriched[df_enriched['nombre_del_indicador'] == metric]
    top_banks = metric_data.nlargest(10, 'valor_indicador')[['banks', 'valor_indicador']].to_dict('records')#type:ignore
    
    return {
        "metric": metric,
        "cr3": data['CR3'],#type:ignore
        "cr5": data['CR5'],#type:ignore
        "hhi": data['HHI'],#type:ignore
        "interpretation": data['interpretacion_HHI'],#type:ignore
        "top_banks": top_banks,
        "concentration_level": data['interpretacion_HHI']#type:ignore
    }


# =========================================================
# ENDPOINT 3: Peer Groups (Grupos de Bancos)
# =========================================================
@router.get("/peer-groups", response_model=PeerGroupResponse)
def get_peer_groups(
    size_metric: str = Query("TOTAL ACTIVO", description="Métrica para clasificar tamaño")
):
    """
    Agrupa bancos en peer groups según tamaño.
    
    **Grupos:**
    - Bancos Grandes (Top 25%)
    - Bancos Medianos-Grandes (25-50%)
    - Bancos Medianos-Pequeños (50-75%)
    - Bancos Pequeños (Bottom 25%)
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    peer_groups = TrendAnalysis.peer_group_analysis(df_enriched, size_metric)
    
    if not peer_groups:
        raise HTTPException(
            status_code=404,
            detail=f"No se pudo calcular peer groups con métrica {size_metric}"
        )
    
    return {
        "size_metric": size_metric,
        "groups": peer_groups,
        "total_groups": len(peer_groups),
        "distribution": {k: len(v) for k, v in peer_groups.items()}
    }


# =========================================================
# ENDPOINT 4: Análisis de Correlaciones
# =========================================================
@router.get("/correlations", response_model=CorrelationResponse)
def get_correlations():
    """
    Calcula matriz de correlación entre indicadores principales.
    
    **Indicadores analizados:**
    - TOTAL ACTIVO
    - ROE (Rentabilidad del Patrimonio)
    - ROA (Rentabilidad de Activos)
    - Morosidad
    - Liquidez
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    correlation_matrix = TrendAnalysis.correlation_analysis(df_enriched)
    
    if correlation_matrix.empty:
        raise HTTPException(
            status_code=404,
            detail="No hay suficientes datos para análisis de correlación"
        )
    
    # Convertir matriz a formato dict
    correlation_dict = correlation_matrix.to_dict()
    
    # Encontrar correlaciones fuertes
    strong_correlations = []
    for i, col1 in enumerate(correlation_matrix.columns):
        for j, col2 in enumerate(correlation_matrix.columns):
            if i < j:  # Solo mitad superior de la matriz
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # Correlación fuerte
                    strong_correlations.append({
                        'indicator1': col1,
                        'indicator2': col2,
                        'correlation': float(corr_value),
                        'strength': 'Fuerte positiva' if corr_value > 0 else 'Fuerte negativa'
                    })
    
    return {
        "correlation_matrix": correlation_dict,
        "indicators": list(correlation_matrix.columns),
        "strong_correlations": strong_correlations,
        "total_indicators": len(correlation_matrix.columns)
    }


# =========================================================
# ENDPOINT 5: Benchmark Analysis
# =========================================================
@router.get("/benchmark/{bank_name}", response_model=BenchmarkResponse)
def get_benchmark_analysis(
    bank_name: str,
    benchmark_type: str = Query("system_average", description="system_average, top_quartile, median")
):
    """
    Compara un banco contra benchmarks del sistema.
    
    **Tipos de benchmark:**
    - system_average: Promedio del sistema
    - top_quartile: Top 25%
    - median: Mediana del sistema
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    # Obtener datos del banco
    bank_data = df_enriched[df_enriched['banks'] == bank_name]
    
    if bank_data.empty:
        available_banks = df_enriched['banks'].unique()
        raise HTTPException(
            status_code=404,
            detail=f"Banco '{bank_name}' no encontrado. Disponibles: {', '.join(available_banks[:5])}"
        )
    
    # Calcular benchmarks
    benchmark_results = TrendAnalysis.benchmark_analysis(df_enriched, benchmark_type)
    
    # Filtrar solo indicadores relevantes del banco
    bank_benchmarks = {}
    for indicator_name, benchmark_df in benchmark_results.items():
        if bank_name in benchmark_df['banco'].values:
            bank_row = benchmark_df[benchmark_df['banco'] == bank_name].iloc[0]
            bank_benchmarks[indicator_name] = {
                'valor_banco': float(bank_row['valor_banco']),
                'valor_benchmark': float(bank_row['valor_benchmark']),
                'desviacion_absoluta': float(bank_row['desviacion_absoluta']),
                'desviacion_relativa_pct': float(bank_row['desviacion_relativa_pct']),
                'posicion': bank_row['posicion']
            }
    
    return {
        "bank": bank_name,
        "benchmark_type": benchmark_type,
        "comparisons": bank_benchmarks,
        "total_indicators": len(bank_benchmarks)
    }


# =========================================================
# ENDPOINT 6: Indicadores Derivados
# =========================================================
@router.get("/derived-indicators", response_model=DerivedIndicatorsResponse)
def get_derived_indicators(
    bank_name: Optional[str] = Query(None, description="Filtrar por banco específico")
):
    """
    Obtiene indicadores derivados calculados automáticamente.
    
    **Indicadores derivados:**
    - Cobertura de Cartera Vencida
    - Patrimonio/Activos Totales (Solvencia)
    - Gastos/Ingresos (Eficiencia)
    - Liquidez sobre Pasivos
    
    **Índices compuestos:**
    - Índice de Solidez Financiera
    - Índice de Rentabilidad Ajustada
    - Índice Global de Desempeño
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    # Indicadores derivados disponibles
    derived_indicators = [
        'COBERTURA CARTERA VENCIDA',
        'PATRIMONIO / ACTIVOS TOTALES',
        'GASTOS DE OPERACION / INGRESOS TOTALES',
        'INGRESOS / GASTOS',
        'ACTIVOS LIQUIDOS / PASIVOS CORTO PLAZO'
    ]
    
    # Índices compuestos
    composite_indices = [
        'INDICE DE SOLIDEZ FINANCIERA',
        'INDICE DE RENTABILIDAD AJUSTADA',
        'INDICE GLOBAL DESEMPEÑO BANCARIO'
    ]
    
    # Filtrar datos
    all_derived = derived_indicators + composite_indices
    derived_data = df_enriched[df_enriched['nombre_del_indicador'].isin(all_derived)]
    
    if bank_name:
        derived_data = derived_data[derived_data['banks'] == bank_name]
        if derived_data.empty:#type:ignore
            raise HTTPException(
                status_code=404,
                detail=f"No hay indicadores derivados para {bank_name}"
            )
    
    # Convertir a formato amigable
    result_data = derived_data[['banks', 'nombre_del_indicador', 'valor_indicador']].to_dict('records')#type:ignore
    
    return {
        "total_indicators": len(result_data),
        "derived_indicators": derived_indicators,
        "composite_indices": composite_indices,
        "data": result_data,
        "filtered_by_bank": bank_name
    }


# =========================================================
# ENDPOINT 7: Estadísticas del Sistema
# =========================================================
@router.get("/system-statistics", response_model=SystemStatisticsResponse)
def get_system_statistics():
    """
    Obtiene estadísticas detalladas del sistema bancario.
    
    **Incluye por cada indicador:**
    - Promedio, Mediana, Desviación Estándar
    - Mínimo, Máximo, Rango
    - Coeficiente de Variación
    - Percentiles 25 y 75
    - Total de bancos con datos
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    system_stats = AdvancedMetrics.get_system_statistics(df_enriched)
    
    if not system_stats:
        raise HTTPException(
            status_code=404,
            detail="No se pudieron calcular estadísticas del sistema"
        )
    
    return {
        "total_indicators": len(system_stats),
        "statistics": system_stats,
        "summary": {
            "total_banks": df_enriched['banks'].nunique(),
            "total_observations": len(df_enriched),
            "indicators_count": len(system_stats)
        }
    }


# =========================================================
# ENDPOINT 8: Participación de Mercado
# =========================================================
@router.get("/market-share")
def get_market_share(
    metric: str = Query("TOTAL ACTIVO", description="Métrica para calcular participación"),
    top_n: int = Query(10, description="Número de top bancos a mostrar")
):
    """
    Calcula participación de mercado por diferentes métricas.
    
    **Métricas disponibles:**
    - TOTAL ACTIVO
    - OBLIGACIONES CON EL PÚBLICO
    - CARTERA DE CRÉDITOS
    - TOTAL PATRIMONIO
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    market_participation = AdvancedMetrics.calculate_market_participation(df_enriched)
    
    if metric not in market_participation:
        available_metrics = list(market_participation.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Métrica '{metric}' no disponible. Usa: {', '.join(available_metrics)}"
        )
    
    participation_df = market_participation[metric]
    
    # Limitar a top N
    top_participants = participation_df.head(top_n)
    
    return {
        "metric": metric,
        "top_n": top_n,
        "market_share": top_participants.to_dict('records'),
        "total_banks": len(participation_df),
        "top_concentration": float(top_participants['participacion_pct'].sum())
    }


# =========================================================
# ENDPOINT 9: Outliers Detection
# =========================================================
@router.get("/outliers")
def detect_outliers(
    method: str = Query("iqr", description="Método: iqr o zscore"),
    indicator: Optional[str] = Query(None, description="Filtrar por indicador específico")
):
    """
    Detecta bancos con valores atípicos (outliers).
    
    **Métodos:**
    - iqr: Rango Intercuartílico (Q3 - Q1)
    - zscore: Desviación estándar (|z| > 2)
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    if method not in ['iqr', 'zscore']:
        raise HTTPException(
            status_code=400,
            detail="Método debe ser 'iqr' o 'zscore'"
        )
    
    outliers = AdvancedMetrics.detect_outliers(df_enriched, method)
    
    if not outliers:
        return {
            "method": method,
            "total_indicators_analyzed": 0,
            "outliers_found": False,
            "outliers": {}
        }
    
    # Filtrar por indicador si se especifica
    if indicator:
        if indicator not in outliers:
            return {
                "method": method,
                "indicator": indicator,
                "outliers_found": False,
                "message": f"No se encontraron outliers para {indicator}"
            }
        outliers = {indicator: outliers[indicator]}
    
    return {
        "method": method,
        "total_indicators_analyzed": len(outliers),
        "outliers_found": True,
        "outliers": outliers,
        "summary": {k: len(v) for k, v in outliers.items()}
    }


# =========================================================
# ENDPOINT 10: Overview General del Sistema
# =========================================================
@router.get("/overview")
def get_system_overview():
    """
    Resumen ejecutivo completo del sistema bancario.
    
    **Incluye:**
    - Estadísticas generales
    - Concentración de mercado
    - Alertas activas
    - Top performers
    """
    if df_enriched is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    # Estadísticas generales
    total_banks = df_enriched['banks'].nunique()
    total_indicators = df_enriched['nombre_del_indicador'].nunique()
    total_observations = len(df_enriched)
    
    # Total activos del sistema
    activos_data = df_enriched[df_enriched['nombre_del_indicador'] == 'TOTAL ACTIVO']
    total_activos_sistema = float(activos_data['valor_indicador'].sum()) if not activos_data.empty else 0
    
    # ROE promedio
    roe_data = df_enriched[df_enriched['nombre_del_indicador'] == 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
    roe_promedio = float(roe_data['valor_indicador'].mean()) if not roe_data.empty else 0
    
    # Concentración
    concentration_data = TrendAnalysis.calculate_concentration_risk(df_enriched)
    hhi = concentration_data.get('TOTAL ACTIVO', {}).get('HHI', 0) if concentration_data else 0#type:ignore
    
    # Alertas
    alerts = TrendAnalysis.generate_alerts(df_enriched)
    critical_alerts = len([a for a in alerts if "CRÍTICA" in a.get('severidad', '')])
    
    # Top performers
    top_activos = activos_data.nlargest(5, 'valor_indicador')[['banks', 'valor_indicador']].to_dict('records') if not activos_data.empty else []#type:ignore
    top_roe = roe_data.nlargest(5, 'valor_indicador')[['banks', 'valor_indicador']].to_dict('records') if not roe_data.empty else []#type:ignore
    
    return {
        "general_statistics": {
            "total_banks": total_banks,
            "total_indicators": total_indicators,
            "total_observations": total_observations,
            "total_assets_system": total_activos_sistema,
            "average_roe": roe_promedio
        },
        "concentration": {
            "hhi": hhi,
            "concentration_level": TrendAnalysis._interpret_hhi(hhi) if hhi > 0 else "N/D"
        },
        "alerts": {
            "total_alerts": len(alerts),
            "critical_alerts": critical_alerts
        },
        "top_performers": {
            "by_assets": top_activos,
            "by_roe": top_roe
        }
    }
