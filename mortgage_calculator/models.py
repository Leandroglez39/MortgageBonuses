"""
Modelos de datos para la calculadora de hipotecas.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class MortgageData:
    """Datos principales de la hipoteca."""
    capital: float  # Capital prestado
    interest_rate: float  # Tasa de interés anual (%)
    years: int  # Años del préstamo
    
    # Bonificaciones
    payroll_bonus: float = 0.0  # Bonificación por domiciliar nómina (%)
    insurance_bonus: float = 0.0  # Bonificación por contratar seguros (%)
    card_bonus: float = 0.0  # Bonificación por usar tarjeta (%)
    other_bonus: float = 0.0  # Otras bonificaciones (%)
    
    # Costes asociados a bonificaciones
    insurance_cost_monthly: float = 0.0  # Coste mensual del seguro
    card_annual_fee: float = 0.0  # Cuota anual de la tarjeta
    other_costs_monthly: float = 0.0  # Otros costes mensuales


@dataclass
class MortgageResults:
    """Resultados de los cálculos de la hipoteca."""
    # Sin bonificaciones
    monthly_payment_without_bonus: float
    total_interest_without_bonus: float
    total_paid_without_bonus: float
    
    # Con bonificaciones
    monthly_payment_with_bonus: float
    total_interest_with_bonus: float
    total_paid_with_bonus: float
    
    # Costes de bonificaciones
    total_bonus_costs: float
    
    # Análisis
    real_savings: float
    savings_percentage: float
    is_worth_it: bool
    effective_rate_without_bonus: float
    effective_rate_with_bonus: float
