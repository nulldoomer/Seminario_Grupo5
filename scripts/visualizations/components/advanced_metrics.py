import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

class AdvancedMetrics:
    """
    Clase para calcular métricas avanzadas y KPIs derivados
    que no están directamente en los datos originales
    """

    @staticmethod
    def calculate_derived_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula indicadores derivados a partir de los datos base
        
        Args:
            df: DataFrame con datos base (formato long: Banks, NOMBRE DEL INDICADOR, Valor Indicador)
            
        Returns:
            DataFrame ampliado con indicadores calculados
        """
        df_result = df.copy()
        
        # Convertir a formato wide para facilitar cálculos
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        # Lista para almacenar nuevos indicadores
        new_indicators = []
        
        # 1. COBERTURA DE CARTERA VENCIDA
        if all(col in pivot_df.columns for col in ['PROVISIONES CARTERA DE CREDITO', 'MOROSIDAD DE LA CARTERA TOTAL', 'CARTERA DE CRÉDITOS']):
            for bank in pivot_df.index:
                # Calcular cartera vencida (morosidad * cartera total)
                cartera_vencida = (pivot_df.loc[bank, 'MOROSIDAD DE LA CARTERA TOTAL'] / 100) * pivot_df.loc[bank, 'CARTERA DE CRÉDITOS']
                
                if cartera_vencida > 0:
                    cobertura = (pivot_df.loc[bank, 'PROVISIONES CARTERA DE CREDITO'] / cartera_vencida) * 100
                else:
                    cobertura = 0
                
                new_indicators.append({
                    'banks': bank,
                    'nombre_del_indicador': 'COBERTURA CARTERA VENCIDA',
                    'valor_indicador': cobertura
                })

        # 2. PATRIMONIO / ACTIVOS TOTALES (Ratio de Solvencia)
        if all(col in pivot_df.columns for col in ['TOTAL PATRIMONIO', 'TOTAL ACTIVO']):
            for bank in pivot_df.index:
                if pivot_df.loc[bank, 'TOTAL ACTIVO'] > 0:
                    ratio_solvencia = (pivot_df.loc[bank, 'TOTAL PATRIMONIO'] / pivot_df.loc[bank, 'TOTAL ACTIVO']) * 100
                else:
                    ratio_solvencia = 0
                
                new_indicators.append({
                    'banks': bank,
                    'nombre_del_indicador': 'PATRIMONIO / ACTIVOS TOTALES',
                    'valor_indicador': ratio_solvencia
                })

        # 3. GASTOS OPERACIÓN / INGRESOS TOTALES (Índice de Eficiencia)
        if all(col in pivot_df.columns for col in ['GASTOS', 'INGRESOS']):
            for bank in pivot_df.index:
                if pivot_df.loc[bank, 'INGRESOS'] > 0:
                    eficiencia = (pivot_df.loc[bank, 'GASTOS'] / pivot_df.loc[bank, 'INGRESOS']) * 100
                else:
                    eficiencia = 0
                
                new_indicators.append({
                    'banks': bank,
                    'nombre_del_indicador': 'GASTOS DE OPERACION / INGRESOS TOTALES',
                    'valor_indicador': eficiencia
                })

        # 4. INGRESOS / GASTOS (Ratio de Eficiencia Operativa)
        if all(col in pivot_df.columns for col in ['INGRESOS', 'GASTOS']):
            for bank in pivot_df.index:
                if pivot_df.loc[bank, 'GASTOS'] > 0:
                    ratio_eficiencia = pivot_df.loc[bank, 'INGRESOS'] / pivot_df.loc[bank, 'GASTOS']
                else:
                    ratio_eficiencia = 0
                
                new_indicators.append({
                    'banks': bank,
                    'nombre_del_indicador': 'INGRESOS / GASTOS',
                    'valor_indicador': ratio_eficiencia
                })

        # 5. ACTIVOS LÍQUIDOS / PASIVOS CORTO PLAZO (Ratio de Liquidez)
        if all(col in pivot_df.columns for col in ['FONDOS DISPONIBLES', 'OBLIGACIONES CON EL PÚBLICO']):
            for bank in pivot_df.index:
                if pivot_df.loc[bank, 'OBLIGACIONES CON EL PÚBLICO'] > 0:
                    liquidez = (pivot_df.loc[bank, 'FONDOS DISPONIBLES'] / pivot_df.loc[bank, 'OBLIGACIONES CON EL PÚBLICO']) * 100
                else:
                    liquidez = 0
                
                new_indicators.append({
                    'banks': bank,
                    'nombre_del_indicador': 'ACTIVOS LIQUIDOS / PASIVOS CORTO PLAZO',
                    'valor_indicador': liquidez
                })

        # Convertir nuevos indicadores a DataFrame y concatenar
        if new_indicators:
            new_df = pd.DataFrame(new_indicators)
            df_result = pd.concat([df_result, new_df], ignore_index=True)
        
        return df_result

    @staticmethod
    def calculate_composite_indices(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula índices compuestos para ranking general
        """
        df_result = df.copy()
        
        # Convertir a formato wide
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        new_indices = []
        
        # ÍNDICE DE SOLIDEZ FINANCIERA (ISF)
        required_cols_isf = ['TOTAL PATRIMONIO', 'TOTAL ACTIVO', 'MOROSIDAD DE LA CARTERA TOTAL']
        if all(col in pivot_df.columns for col in required_cols_isf):
            for bank in pivot_df.index:
                patrimonio_activo = pivot_df.loc[bank, 'TOTAL PATRIMONIO'] / pivot_df.loc[bank, 'TOTAL ACTIVO'] if pivot_df.loc[bank, 'TOTAL ACTIVO'] > 0 else 0
                morosidad_factor = 1 - (pivot_df.loc[bank, 'MOROSIDAD DE LA CARTERA TOTAL'] / 100)
                
                isf = patrimonio_activo * morosidad_factor * 100
                
                new_indices.append({
                    'banks': bank,
                    'nombre_del_indicador': 'INDICE DE SOLIDEZ FINANCIERA',
                    'valor_indicador': isf
                })

        # ÍNDICE DE RENTABILIDAD AJUSTADA (IRA)
        required_cols_ira = ['RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO', 'MOROSIDAD DE LA CARTERA TOTAL']
        if all(col in pivot_df.columns for col in required_cols_ira):
            for bank in pivot_df.index:
                roe = pivot_df.loc[bank, 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
                morosidad = pivot_df.loc[bank, 'MOROSIDAD DE LA CARTERA TOTAL']
                
                if morosidad > 0:
                    ira = roe / morosidad
                else:
                    ira = roe  # Si no hay morosidad, la rentabilidad ajustada es igual al ROE
                
                new_indices.append({
                    'banks': bank,
                    'nombre_del_indicador': 'INDICE DE RENTABILIDAD AJUSTADA',
                    'valor_indicador': ira
                })

        # ÍNDICE GLOBAL DE DESEMPEÑO BANCARIO
        # (Promedio ponderado normalizado de KPIs principales)
        kpi_weights = {
            'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO': 0.25,  # ROE
            'RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO': 0.20,      # ROA
            'TOTAL ACTIVO': 0.20,                                     # Tamaño
            'MOROSIDAD DE LA CARTERA TOTAL': -0.25,                  # Riesgo (negativo)
            'PATRIMONIO / ACTIVOS TOTALES': 0.10                     # Solvencia
        }
        
        available_kpis = {k: v for k, v in kpi_weights.items() if k in pivot_df.columns}
        
        if len(available_kpis) >= 3:  # Al menos 3 KPIs disponibles
            for bank in pivot_df.index:
                score = 0
                total_weight = 0
                
                for kpi, weight in available_kpis.items():
                    value = pivot_df.loc[bank, kpi]
                    
                    # Normalizar valores (z-score)
                    mean_val = pivot_df[kpi].mean()
                    std_val = pivot_df[kpi].std()
                    
                    if std_val > 0:
                        normalized_value = (value - mean_val) / std_val
                    else:
                        normalized_value = 0
                    
                    score += normalized_value * weight
                    total_weight += abs(weight)
                
                # Normalizar el score final
                if total_weight > 0:
                    final_score = (score / total_weight) * 100 + 100  # Centrar en 100
                else:
                    final_score = 100
                
                new_indices.append({
                    'banks': bank,
                    'nombre_del_indicador': 'INDICE GLOBAL DESEMPEÑO BANCARIO',
                    'valor_indicador': final_score
                })

        # Agregar nuevos índices
        if new_indices:
            indices_df = pd.DataFrame(new_indices)
            df_result = pd.concat([df_result, indices_df], ignore_index=True)
        
        return df_result

    @staticmethod
    def calculate_market_participation(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Calcula participación de mercado por diferentes métricas
        """
        # Convertir a formato wide
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        participation_data = {}
        
        metrics_to_analyze = ['TOTAL ACTIVO', 'OBLIGACIONES CON EL PÚBLICO', 'CARTERA DE CRÉDITOS', 'TOTAL PATRIMONIO']
        
        for metric in metrics_to_analyze:
            if metric in pivot_df.columns:
                total_system = pivot_df[metric].sum()
                
                if total_system > 0:
                    participation = (pivot_df[metric] / total_system * 100).sort_values(ascending=False)
                    
                    participation_df = pd.DataFrame({
                        'banks': participation.index,
                        'participacion_pct': participation.values,
                        'valor_absoluto': pivot_df[metric].values
                    })
                    
                    participation_data[metric] = participation_df
        
        return participation_data

    @staticmethod
    def get_system_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Calcula estadísticas del sistema por categorías
        """
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        )
        
        system_stats = {}
        
        for column in pivot_df.columns:
            serie = pivot_df[column].dropna()
            
            if len(serie) > 0:
                system_stats[column] = {
                    'promedio': float(serie.mean()),
                    'mediana': float(serie.median()),
                    'desviacion_estandar': float(serie.std()),
                    'minimo': float(serie.min()),
                    'maximo': float(serie.max()),
                    'rango': float(serie.max() - serie.min()),
                    'coeficiente_variacion': float(serie.std() / serie.mean() * 100) if serie.mean() != 0 else 0,
                    'percentil_25': float(serie.quantile(0.25)),
                    'percentil_75': float(serie.quantile(0.75)),
                    'total_bancos': len(serie)
                }
        
        return system_stats

    @staticmethod
    def detect_outliers(df: pd.DataFrame, method: str = 'iqr') -> Dict[str, List[str]]:
        """
        Detecta bancos con valores atípicos (outliers)
        
        Args:
            df: DataFrame con datos
            method: 'iqr' para método de rango intercuartílico, 'zscore' para z-score
            
        Returns:
            Diccionario con indicador como clave y lista de bancos outliers como valor
        """
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        )
        
        outliers = {}
        
        for column in pivot_df.columns:
            serie = pivot_df[column].dropna()
            outlier_banks = []
            
            if len(serie) > 3:  # Necesitamos al menos 4 valores
                if method == 'iqr':
                    Q1 = serie.quantile(0.25)
                    Q3 = serie.quantile(0.75)
                    IQR = Q3 - Q1
                    
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outlier_banks = serie[(serie < lower_bound) | (serie > upper_bound)].index.tolist()
                
                elif method == 'zscore':
                    mean_val = serie.mean()
                    std_val = serie.std()
                    
                    if std_val > 0:
                        z_scores = np.abs((serie - mean_val) / std_val)
                        outlier_banks = serie[z_scores > 2].index.tolist()  # |z| > 2
            
            if outlier_banks:
                outliers[column] = outlier_banks
        
        return outliers