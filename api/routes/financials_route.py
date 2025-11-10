from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..schemas import (
    BankFinancialsResponse,
    RankingResponse,
    BanksListResponse,
    IndicatorsListResponse,
    ComparativeResponse,
)

from scripts.visualizations.components.data_handler import DataHandler
from scripts.visualizations.components.metrics_calculator import MetricsCalculator
from scripts.visualizations.components.indicator_config import IndicatorConfig
from scripts.visualizations.data_loader import VisualizationDataLoader


# Create the router

router = APIRouter(
    prefix="/financials",
    tags=["Financials Indicators"],
    responses={404: {"description": "Not found"}}
)

loader = VisualizationDataLoader()
dh = DataHandler(loader)
calc = MetricsCalculator()

df_original = dh.load_data("Final Dataframe")


@router.get("/bank", response_model=BankFinancialsResponse)
def get_bank_financials(
    name: str = Query(..., description="Nombre del banco (ej: Pichincha)"),
    category: str = Query("Balance", description="Balance, Rendimiento o Estructura")
):

    if category not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(
            status_code=400, 
            detail="Categoría inválida. Usa: Balance, Rendimiento o Estructura"
        )


    indicator_names = IndicatorConfig.get_indicator_names_by_category(category)
    is_percentage = IndicatorConfig.is_category_percentage(category)
    unit = IndicatorConfig.get_category_unit(category)
    
    df_filtrado = dh.filter_by_category(indicator_names, is_percentage)
    
    if df_filtrado.empty:
        raise HTTPException(
            status_code=404, 
            detail=f"No hay datos para la categoría {category}"
        )
    
    bank_data = dh.get_bank_data(df_filtrado, name, sort_by_value=True)
    
    if bank_data.empty:

        available_banks = dh.get_unique_values(df_filtrado, "banks")
        raise HTTPException(
            status_code=404,
            detail=f"Banco '{name}' no encontrado. Bancos disponibles: {', '.join(available_banks[:5])}"
        )
    
    stats = calc.get_sumary_stats(bank_data)
    
    return {
        "bank": name,
        "category": category,
        "is_percentage": is_percentage,
        "unit": unit,
        "data": bank_data.to_dict('records'),
        "stats": stats,
        "total_indicators": len(bank_data)
    }


@router.get("/rank", response_model=RankingResponse)
def get_ranking(
    kpi: str = Query(..., description="Indicador para el ranking (ej: TOTAL ACTIVO)"),
    category: str = Query("Balance", description="Balance, Rendimiento o Estructura"),
    ascending: bool = Query(False, description="Orden ascendente (menor a mayor)")
):

    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    if category not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(
            status_code=400,
            detail="Categoría inválida"
        )
    
    indicator_names = IndicatorConfig.get_indicator_names_by_category(category)
    is_percentage = IndicatorConfig.is_category_percentage(category)
    unit = IndicatorConfig.get_category_unit(category)
    
    if kpi not in indicator_names:
        raise HTTPException(
            status_code=404,
            detail=f"Indicador '{kpi}' no encontrado en categoría {category}." 
        )
    
    df_filtrado = dh.filter_by_category(indicator_names, is_percentage)
    
    ranking = dh.get_ranking(df_filtrado, kpi, ascending=ascending)
    
    if ranking.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No hay datos disponibles para el indicador '{kpi}'"
        )
    
    return {
        "kpi": kpi,
        "category": category,
        "is_percentage": is_percentage,
        "unit": unit,
        "ranking": ranking.to_dict('records'),
        "total_banks": len(ranking)
    }


@router.get("/banks", response_model=BanksListResponse)
def get_available_banks(
    category: str = Query("Balance", description="Filtrar por categoría")
):
    
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    if category not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(status_code=400, detail="Categoría inválida")
    
    indicator_names = IndicatorConfig.get_indicator_names_by_category(category)
    is_percentage = IndicatorConfig.is_category_percentage(category)
    
    df_filtrado = dh.filter_by_category(indicator_names, is_percentage)
    
    bancos = dh.get_unique_values(df_filtrado, "banks")
    
    return {
        "category": category,
        "banks": bancos,
        "total": len(bancos)
    }


@router.get("/indicators", response_model=IndicatorsListResponse)
def get_available_indicators(
    category: str = Query("Balance", description="Balance, Rendimiento o Estructura")
):
   
    if category not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(status_code=400, detail="Categoría inválida")
    
    indicator_names = IndicatorConfig.get_indicator_names_by_category(category)
    
    return {
        "category": category,
        "indicators": list(indicator_names.keys()),
        "descriptions": indicator_names,
        "total": len(indicator_names)
    }


@router.get("/comparative", response_model=ComparativeResponse)
def get_comparative_table(
    category: str = Query("Balance", description="Categoría a comparar"),
    banks: Optional[List[str]] = Query(None, description="Bancos específicos (opcional)")
):
   
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    if category not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(status_code=400, detail="Categoría inválida")
    
    indicator_names = IndicatorConfig.get_indicator_names_by_category(category)
    is_percentage = IndicatorConfig.is_category_percentage(category)
    indicator_order = list(indicator_names.keys())
    
    df_filtrado = dh.filter_by_category(indicator_names, is_percentage)
    
    if banks:
        df_filtrado = df_filtrado[df_filtrado["banks"].isin(banks)]
        if df_filtrado.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No hay datos para los bancos especificados"
            )
    
    pivot_df = dh.get_pivot_table(df_filtrado, indicator_order) #type:ignore
    
    if pivot_df.empty:
        raise HTTPException(
            status_code=404,
            detail="No se pudo generar la tabla comparativa"
        )
    
    data_dict = pivot_df.to_dict('index')#type:ignore
    
    return {
        "category": category,
        "banks": list(pivot_df.index),
        "indicators": list(pivot_df.columns),
        "data": data_dict,
        "is_percentage": is_percentage
    }


@router.get("/stats")
def get_category_statistics(
    category: str = Query("Balance", description="Categoría a analizar")
):
    
    if df_original is None:
        raise HTTPException(status_code=503, detail="Datos no disponibles")
    
    if category not in ["Balance", "Rendimiento", "Estructura"]:
        raise HTTPException(status_code=400, detail="Categoría inválida")
    
    indicator_names = IndicatorConfig.get_indicator_names_by_category(category)
    is_percentage = IndicatorConfig.is_category_percentage(category)
    
    df_filtrado = dh.filter_by_category(indicator_names, is_percentage)
    
    stats = calc.get_sumary_stats(df_filtrado)
    
    resumen_bancos = df_filtrado.groupby('banks').agg({
        'valor_indicador': ['mean', 'sum', 'count', 'std']
    }).round(2)
    
    resumen_bancos.columns = ['promedio', 'total', 'cantidad', 'desviacion']
    resumen_bancos = resumen_bancos.sort_values('total', ascending=False)#type:ignore
    
    return {
        "category": category,
        "is_percentage": is_percentage,
        "global_stats": stats,
        "stats_by_bank": resumen_bancos.to_dict('index'),
        "total_banks": len(resumen_bancos),
        "total_indicators": len(indicator_names)
    }
