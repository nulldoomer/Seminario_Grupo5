from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class IndicatorConfig:

    # First define the structure of the object

    name: str
    category: str
    is_percentage: bool
    unit: str
    description: str



    # @staticmethod allow us to access to the method without making an instance
    # of the class, well with this method we declare all the objects, the
    # dictionary of the list of indicators, accessing to them with a category
    # name

    @staticmethod
    def get_all_indicators() -> Dict[str, List['IndicatorConfig']]:
            """Retorna todos los indicadores organizados por categoría"""
            indicators = {
                "Balance": [
                    IndicatorConfig("FONDOS DISPONIBLES", "Balance", False, "$", "Liquidez inmediata"),
                    IndicatorConfig("INVERSIONES", "Balance", False, "$", "Activos financieros"),
                    IndicatorConfig("CARTERA DE CRÉDITOS", "Balance", False, "$", "Préstamos otorgados"),
                    IndicatorConfig("DEUDORES POR ACEPTACIONES", "Balance", False, "$", "Compromisos de pago"),
                    IndicatorConfig("CUENTAS POR COBRAR", "Balance", False, "$", "Cuentas pendientes"),
                    IndicatorConfig("PROPIEDADES Y EQUIPO", "Balance", False, "$", "Activos fijos"),
                    IndicatorConfig("OTROS ACTIVOS", "Balance", False, "$", "Activos diversos"),
                ],
                "Rendimiento": [
                    IndicatorConfig("RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO", "Rendimiento", True, "%", "ROA - Rentabilidad"),
                    IndicatorConfig("RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO", "Rendimiento", True, "%", "ROE - Rentabilidad"),
                    IndicatorConfig("MOROSIDAD DE LA CARTERA TOTAL", "Rendimiento", True, "%", "Calidad de cartera"),
                    IndicatorConfig("ACTIVOS PRODUCTIVOS / TOTAL ACTIVOS", "Rendimiento", True, "%", "Eficiencia activos"),
                    IndicatorConfig("FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO", "Rendimiento", True, "%", "Liquidez"),
                    IndicatorConfig("GASTOS DE OPERACION ESTIMADOS / TOTAL ACTIVO PROMEDIO (3)", "Rendimiento", True, "%", "Eficiencia operativa"),
                ],
                "Estructura": [
                    IndicatorConfig("TOTAL ACTIVO", "Estructura", False, "$", "Tamaño del banco"),
                    IndicatorConfig("TOTAL PATRIMONIO", "Estructura", False, "$", "Capital propio"),
                    IndicatorConfig("TOTAL PASIVOS", "Estructura", False, "$", "Obligaciones totales"),
                    IndicatorConfig("OBLIGACIONES CON EL PÚBLICO", "Estructura", False, "$", "Depósitos captados"),
                    IndicatorConfig("CAPITAL SOCIAL", "Estructura", False, "$", "Capital accionario"),
                ]
            }
            return indicators
