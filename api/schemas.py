from pydantic import BaseModel, Field
from typing import Dict, List, Optional


# This is where all the schemas gonna be, just to keep it simple
# not having a file for every schema

class BankFinancialsResponse(BaseModel):
    bank: str = Field(..., description="Nombre del banco")
    category: str = Field(..., description="Categoría de indicadores")
    is_percentage: bool = Field(..., description="Si los valores son porcentajes")
    unit: str = Field(..., description="Unidad de medida ($ o %)")
    data: List[Dict] = Field(..., description="Lista de indicadores con valores")
    stats: Dict = Field(..., description="Estadísticas resumidas")
    total_indicators: int = Field(..., description="Total de indicadores")
    class Config:
        json_schema_extra = {
            "example": {
                "bank": "Pichincha",
                "category": "Balance",
                "is_percentage": False,
                "unit": "$",
                "data": [
                    {
                        "nombre_del_indicador": "FONDOS DISPONIBLES",
                        "valor_indicador": 1000000,
                        "banks": "Pichincha"
                    }
                ],
                "stats": {
                    "total": 5000000,
                    "promedio": 1000000,
                    "max": 2000000,
                    "min": 500000
                },
                "total_indicators": 5
            }
        }

class RankingResponse(BaseModel):

    kpi: str = Field(..., description="Indicador usado para el ranking")
    category: str = Field(..., description="Categoría del indicador")
    is_percentage: bool = Field(..., description="Si los valores son porcentajes")
    unit: str = Field(..., description="Unidad de medida")
    ranking: List[Dict] = Field(..., description="Lista ordenada de bancos")
    total_banks: int = Field(..., description="Total de bancos en el ranking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "kpi": "TOTAL ACTIVO",
                "category": "Estructura",
                "is_percentage": False,
                "unit": "$",
                "ranking": [
                    {
                        "banks": "Pichincha",
                        "valor_indicador": 50000000,
                        "nombre_del_indicador": "TOTAL ACTIVO"
                    },
                    {
                        "banks": "Guayaquil",
                        "valor_indicador": 40000000,
                        "nombre_del_indicador": "TOTAL ACTIVO"
                    }
                ],
                "total_banks": 2
            }
        }


class BanksListResponse(BaseModel):

    category: str = Field(..., description="Categoría filtrada")
    banks: List[str] = Field(..., description="Lista de nombres de bancos")
    total: int = Field(..., description="Total de bancos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Balance",
                "banks": ["Pichincha", "Guayaquil", "Pacifico"],
                "total": 3
            }
        }


class IndicatorsListResponse(BaseModel):

    category: str = Field(..., description="Categoría")
    indicators: List[str] = Field(..., description="Lista de indicadores")
    descriptions: Dict[str, str] = Field(..., description="Descripción de cada indicador")
    total: int = Field(..., description="Total de indicadores")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Balance",
                "indicators": ["FONDOS DISPONIBLES", "INVERSIONES"],
                "descriptions": {
                    "FONDOS DISPONIBLES": "Liquidez inmediata",
                    "INVERSIONES": "Activos financieros"
                },
                "total": 2
            }
        }


class ComparativeResponse(BaseModel):

    category: str = Field(..., description="Categoría de análisis")
    banks: List[str] = Field(..., description="Bancos incluidos")
    indicators: List[str] = Field(..., description="Indicadores incluidos")
    data: Dict[str, Dict[str, float]] = Field(..., description="Datos pivot: {banco: {indicador: valor}}")
    is_percentage: bool = Field(..., description="Si los valores son porcentajes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Balance",
                "banks": ["Pichincha", "Guayaquil"],
                "indicators": ["FONDOS DISPONIBLES", "INVERSIONES"],
                "data": {
                    "Pichincha": {
                        "FONDOS DISPONIBLES": 1000000,
                        "INVERSIONES": 2000000
                    },
                    "Guayaquil": {
                        "FONDOS DISPONIBLES": 900000,
                        "INVERSIONES": 1800000
                    }
                },
                "is_percentage": False
            }
        }
