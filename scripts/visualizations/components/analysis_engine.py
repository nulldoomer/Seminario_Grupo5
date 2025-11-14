import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import streamlit as st

class TrendAnalysis:
    """
    Clase para análisis de tendencias y detección de alertas
    """
    
    @staticmethod
    def generate_alerts(df: pd.DataFrame) -> List[Dict[str, str]]:
        """
        Genera alertas automáticas basadas en thresholds de la industria bancaria
        """
        alerts = []
        
        # Convertir a formato wide para análisis
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        # ALERTAS DE RIESGO CREDITICIO
        if 'MOROSIDAD DE LA CARTERA TOTAL' in pivot_df.columns:
            high_risk_banks = pivot_df[pivot_df['MOROSIDAD DE LA CARTERA TOTAL'] > 5.0]
            for bank in high_risk_banks.index:
                morosidad = high_risk_banks.loc[bank, 'MOROSIDAD DE LA CARTERA TOTAL']
                severity = "🔴 CRÍTICA" if morosidad > 10 else "🟠 ALTA"
                alerts.append({
                    'tipo': 'Riesgo Crediticio',
                    'banco': bank,
                    'indicador': 'Morosidad',
                    'valor': f"{morosidad:.2f}%",
                    'severidad': severity,
                    'descripcion': f"Morosidad superior al 5% (limite recomendado)"
                })
        
        # ALERTAS DE LIQUIDEZ
        if 'FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO' in pivot_df.columns:
            low_liquidity_banks = pivot_df[pivot_df['FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO'] < 10.0]
            for bank in low_liquidity_banks.index:
                liquidez = low_liquidity_banks.loc[bank, 'FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO']
                severity = "🔴 CRÍTICA" if liquidez < 5 else "🟠 ALTA"
                alerts.append({
                    'tipo': 'Liquidez',
                    'banco': bank,
                    'indicador': 'Ratio de Liquidez',
                    'valor': f"{liquidez:.2f}%",
                    'severidad': severity,
                    'descripcion': f"Liquidez por debajo del 10% (mínimo recomendado)"
                })
        
        # ALERTAS DE RENTABILIDAD
        if 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO' in pivot_df.columns:
            negative_roe_banks = pivot_df[pivot_df['RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO'] < 0]
            for bank in negative_roe_banks.index:
                roe = negative_roe_banks.loc[bank, 'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO']
                alerts.append({
                    'tipo': 'Rentabilidad',
                    'banco': bank,
                    'indicador': 'ROE',
                    'valor': f"{roe:.2f}%",
                    'severidad': "🔴 CRÍTICA",
                    'descripcion': f"ROE negativo indica pérdidas"
                })
        
        # ALERTAS DE SOLVENCIA
        if all(col in pivot_df.columns for col in ['TOTAL PATRIMONIO', 'TOTAL ACTIVO']):
            for bank in pivot_df.index:
                if pivot_df.loc[bank, 'TOTAL ACTIVO'] > 0:
                    solvencia = (pivot_df.loc[bank, 'TOTAL PATRIMONIO'] / pivot_df.loc[bank, 'TOTAL ACTIVO']) * 100
                    
                    if solvencia < 9.0:  # Capital mínimo regulatorio típico
                        severity = "🔴 CRÍTICA" if solvencia < 6 else "🟠 ALTA"
                        alerts.append({
                            'tipo': 'Solvencia',
                            'banco': bank,
                            'indicador': 'Patrimonio/Activos',
                            'valor': f"{solvencia:.2f}%",
                            'severidad': severity,
                            'descripcion': f"Ratio de solvencia por debajo del 9% (mínimo regulatorio)"
                        })
        
        # ALERTAS DE EFICIENCIA OPERATIVA
        if all(col in pivot_df.columns for col in ['GASTOS', 'INGRESOS']):
            for bank in pivot_df.index:
                if pivot_df.loc[bank, 'INGRESOS'] > 0:
                    eficiencia = (pivot_df.loc[bank, 'GASTOS'] / pivot_df.loc[bank, 'INGRESOS']) * 100
                    
                    if eficiencia > 70.0:  # Threshold típico de eficiencia
                        severity = "🔴 CRÍTICA" if eficiencia > 90 else "🟠 ALTA"
                        alerts.append({
                            'tipo': 'Eficiencia Operativa',
                            'banco': bank,
                            'indicador': 'Gastos/Ingresos',
                            'valor': f"{eficiencia:.2f}%",
                            'severidad': severity,
                            'descripcion': f"Ratio de eficiencia superior al 70% (ineficiente)"
                        })
        
        return alerts
    
    @staticmethod
    def calculate_concentration_risk(df: pd.DataFrame) -> Dict[str, float]:
        """
        Calcula el riesgo de concentración del sistema bancario
        """
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        concentration_metrics = {}
        
        metrics_to_analyze = ['TOTAL ACTIVO', 'OBLIGACIONES CON EL PÚBLICO', 'CARTERA DE CRÉDITOS']
        
        for metric in metrics_to_analyze:
            if metric in pivot_df.columns:
                values = pivot_df[metric].sort_values(ascending=False)#type:ignore
                total = values.sum()
                
                if total > 0:
                    # Participación de los 3 bancos más grandes (CR3)
                    top3_share = values.head(3).sum() / total * 100
                    
                    # Participación de los 5 bancos más grandes (CR5)
                    top5_share = values.head(5).sum() / total * 100
                    
                    # Índice de Herfindahl-Hirschman (HHI)
                    market_shares = values / total * 100
                    hhi = (market_shares ** 2).sum()
                    
                    concentration_metrics[metric] = {
                        'CR3': top3_share,
                        'CR5': top5_share,
                        'HHI': hhi,
                        'interpretacion_HHI': TrendAnalysis._interpret_hhi(hhi)
                    }
        
        return concentration_metrics
    
    @staticmethod
    def _interpret_hhi(hhi: float) -> str:
        """
        Interpreta el índice HHI según estándares regulatorios
        """
        if hhi < 1500:
            return "Mercado Competitivo"
        elif hhi < 2500:
            return "Mercado Moderadamente Concentrado"
        else:
            return "Mercado Altamente Concentrado"
    
    @staticmethod
    def peer_group_analysis(df: pd.DataFrame, size_metric: str = 'TOTAL ACTIVO') -> Dict[str, List[str]]:
        """
        Agrupa bancos en peer groups según tamaño
        """
        if size_metric not in df['nombre_del_indicador'].unique():
            return {}
        
        # Filtrar solo el métrico de tamaño
        size_data = df[df['nombre_del_indicador'] == size_metric].copy()
        
        if size_data.empty:
            return {}
        
        # Calcular cuartiles
        q25 = size_data['valor_indicador'].quantile(0.25) #type:ignore
        q50 = size_data['valor_indicador'].quantile(0.50)#type:ignore
        q75 = size_data['valor_indicador'].quantile(0.75)#type:ignore
        
        peer_groups = {
            'Bancos Grandes (Top 25%)': [],
            'Bancos Medianos-Grandes (25-50%)': [],
            'Bancos Medianos-Pequeños (50-75%)': [],
            'Bancos Pequeños (Bottom 25%)': []
        }
        
        for _, row in size_data.iterrows():
            bank = row['banks']
            value = row['valor_indicador']
            
            if value >= q75:
                peer_groups['Bancos Grandes (Top 25%)'].append(bank)
            elif value >= q50:
                peer_groups['Bancos Medianos-Grandes (25-50%)'].append(bank)
            elif value >= q25:
                peer_groups['Bancos Medianos-Pequeños (50-75%)'].append(bank)
            else:
                peer_groups['Bancos Pequeños (Bottom 25%)'].append(bank)
        
        return peer_groups
    
    @staticmethod
    def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza correlaciones entre indicadores principales
        """
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        # Seleccionar indicadores principales para correlación
        key_indicators = [
            'TOTAL ACTIVO',
            'RESULTADOS DEL EJERCICIO / PATRIMONIO PROMEDIO',
            'RESULTADOS DEL EJERCICIO / ACTIVO PROMEDIO',
            'MOROSIDAD DE LA CARTERA TOTAL',
            'FONDOS DISPONIBLES / TOTAL DEPOSITOS A CORTO PLAZO'
        ]
        
        available_indicators = [ind for ind in key_indicators if ind in pivot_df.columns]
        
        if len(available_indicators) >= 2:
            correlation_matrix = pivot_df[available_indicators].corr() #type:ignore
            return correlation_matrix
        else:
            return pd.DataFrame()
    
    @staticmethod
    def benchmark_analysis(df: pd.DataFrame, benchmark_type: str = 'system_average') -> Dict[str, pd.DataFrame]:
        """
        Compara cada banco contra benchmarks (promedio del sistema, top quartile, etc.)
        """
        pivot_df = df.pivot_table(
            index='banks', 
            columns='nombre_del_indicador', 
            values='valor_indicador', 
            aggfunc='mean'
        ).fillna(0)
        
        benchmark_results = {}
        
        for indicator in pivot_df.columns:
            serie = pivot_df[indicator]
            
            if benchmark_type == 'system_average':
                benchmark_value = serie.mean()
                benchmark_name = 'Promedio del Sistema'
            elif benchmark_type == 'top_quartile':
                benchmark_value = serie.quantile(0.75)
                benchmark_name = 'Top 25%'
            elif benchmark_type == 'median':
                benchmark_value = serie.median()
                benchmark_name = 'Mediana del Sistema'
            else:
                continue
            
            # Calcular desviación vs benchmark
            deviations = serie - benchmark_value
            relative_deviations = (deviations / benchmark_value * 100) if benchmark_value != 0 else deviations
            
            benchmark_df = pd.DataFrame({
                'banco': serie.index,
                'valor_banco': serie.values,
                'valor_benchmark': benchmark_value,
                'desviacion_absoluta': deviations.values,
                'desviacion_relativa_pct': relative_deviations.values,
                'posicion': ['Por encima' if x > 0 else 'Por debajo' if x < 0 else 'Igual' for x in deviations.values]
            }).sort_values('desviacion_relativa_pct', ascending=False)
            
            benchmark_results[f"{indicator} vs {benchmark_name}"] = benchmark_df
        
        return benchmark_results

class AlertRenderer:
    """
    Clase para renderizar alertas en Streamlit
    """
    
    @staticmethod
    def render_alerts_panel(alerts: List[Dict[str, str]]):
        """
        Renderiza el panel de alertas en Streamlit
        """
        if not alerts:
            st.success("✅ No se detectaron alertas críticas en el sistema")
            return
        
        st.markdown("### 🚨 **Panel de Alertas del Sistema**")
        
        # Agrupar alertas por severidad
        criticas = [a for a in alerts if "CRÍTICA" in a['severidad']]
        altas = [a for a in alerts if "ALTA" in a['severidad']]
        
        # Mostrar contadores
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🔴 Alertas Críticas", len(criticas))
        with col2:
            st.metric("🟠 Alertas Altas", len(altas))
        
        # Mostrar alertas críticas primero
        if criticas:
            st.markdown("#### 🔴 **Alertas Críticas**")
            for alert in criticas:
                with st.expander(f"🚨 {alert['banco']} - {alert['tipo']}"):
                    col_a, col_b = st.columns([1, 2])
                    with col_a:
                        st.metric(alert['indicador'], alert['valor'])
                    with col_b:
                        st.warning(alert['descripcion'])
        
        # Mostrar alertas altas
        if altas:
            st.markdown("#### 🟠 **Alertas de Atención**")
            for alert in altas:
                with st.expander(f"⚠️ {alert['banco']} - {alert['tipo']}"):
                    col_a, col_b = st.columns([1, 2])
                    with col_a:
                        st.metric(alert['indicador'], alert['valor'])
                    with col_b:
                        st.info(alert['descripcion'])
    
    @staticmethod
    def render_concentration_analysis(concentration_data: Dict[str, Dict]):
        """
        Renderiza análisis de concentración del mercado
        """
        if not concentration_data:
            st.info("No hay datos suficientes para análisis de concentración")
            return
        
        st.markdown("### 🎯 **Análisis de Concentración del Mercado**")
        
        for metric, data in concentration_data.items():
            with st.expander(f"📊 Concentración: {metric}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("CR3 (Top 3 bancos)", f"{data['CR3']:.1f}%")
                    
                with col2:
                    st.metric("CR5 (Top 5 bancos)", f"{data['CR5']:.1f}%")
                    
                with col3:
                    st.metric("Índice HHI", f"{data['HHI']:.0f}")
                    st.caption(data['interpretacion_HHI'])
                
                # Interpretación
                if data['CR3'] > 70:
                    st.warning("⚠️ Alta concentración: Los 3 bancos principales controlan más del 70% del mercado")
                elif data['CR3'] > 50:
                    st.info("ℹ️ Concentración moderada: Los 3 bancos principales controlan más del 50% del mercado")
                else:
                    st.success("✅ Mercado competitivo: Baja concentración en los principales actores")
