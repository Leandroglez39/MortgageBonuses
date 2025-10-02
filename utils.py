"""
Utilidades adicionales para análisis avanzados.
"""

from typing import Dict, List

import pandas as pd

from mortgage_calculator.calculator import MortgageCalculator
from mortgage_calculator.models import MortgageData


def compare_scenarios(
    scenarios: List[Dict[str, any]], output_file: str = "comparacion_escenarios.xlsx"
) -> str:
    """
    Compara múltiples escenarios de hipoteca en un solo archivo Excel.

    Args:
        scenarios: Lista de diccionarios con 'nombre' y 'data' (MortgageData)
        output_file: Nombre del archivo de salida

    Returns:
        Ruta del archivo generado

    Example:
        scenarios = [
            {
                "nombre": "Banco A",
                "data": MortgageData(capital=200000, interest_rate=3.5, years=30)
            },
            {
                "nombre": "Banco B",
                "data": MortgageData(capital=200000, interest_rate=3.3, years=30)
            }
        ]
        compare_scenarios(scenarios)
    """
    results_list = []

    for scenario in scenarios:
        calculator = MortgageCalculator(scenario["data"])
        results = calculator.calculate()

        results_list.append(
            {
                "Escenario": scenario["nombre"],
                "Capital (€)": scenario["data"].capital,
                "Tipo Base (%)": scenario["data"].interest_rate,
                "Plazo (años)": scenario["data"].years,
                "Bonificaciones (%)": calculator.calculate_total_bonus(),
                "Tipo Final (%)": max(
                    0, scenario["data"].interest_rate - calculator.calculate_total_bonus()
                ),
                "Cuota Mensual (€)": (
                    results.monthly_payment_with_bonus
                    if calculator.calculate_total_bonus() > 0
                    else results.monthly_payment_without_bonus
                ),
                "Total Intereses (€)": (
                    results.total_interest_with_bonus
                    if calculator.calculate_total_bonus() > 0
                    else results.total_interest_without_bonus
                ),
                "Total a Pagar (€)": (
                    results.total_paid_with_bonus
                    if calculator.calculate_total_bonus() > 0
                    else results.total_paid_without_bonus
                ),
                "Costes Bonificaciones (€)": results.total_bonus_costs,
                "Coste Real Total (€)": (
                    results.total_paid_with_bonus
                    if calculator.calculate_total_bonus() > 0
                    else results.total_paid_without_bonus
                )
                + results.total_bonus_costs,
                "Ahorro Real (€)": (
                    results.real_savings if calculator.calculate_total_bonus() > 0 else 0
                ),
                "¿Vale la pena?": (
                    "SÍ"
                    if results.is_worth_it
                    else "NO" if calculator.calculate_total_bonus() > 0 else "N/A"
                ),
            }
        )

    df = pd.DataFrame(results_list)
    df.to_excel(output_file, index=False)

    return output_file


def sensitivity_analysis(
    base_data: MortgageData,
    rate_range: tuple = (2.0, 5.0),
    rate_step: float = 0.25,
    output_file: str = "analisis_sensibilidad.xlsx",
) -> str:
    """
    Realiza un análisis de sensibilidad variando el tipo de interés.

    Args:
        base_data: Datos base de la hipoteca
        rate_range: Rango de tipos de interés (min, max)
        rate_step: Paso entre tipos
        output_file: Nombre del archivo de salida

    Returns:
        Ruta del archivo generado
    """
    results_list = []

    rate = rate_range[0]
    while rate <= rate_range[1]:
        data = MortgageData(
            capital=base_data.capital,
            interest_rate=rate,
            years=base_data.years,
            payroll_bonus=base_data.payroll_bonus,
            insurance_bonus=base_data.insurance_bonus,
            card_bonus=base_data.card_bonus,
            other_bonus=base_data.other_bonus,
            insurance_cost_monthly=base_data.insurance_cost_monthly,
            card_annual_fee=base_data.card_annual_fee,
            other_costs_monthly=base_data.other_costs_monthly,
        )

        calculator = MortgageCalculator(data)
        results = calculator.calculate()

        results_list.append(
            {
                "Tipo de Interés (%)": rate,
                "Cuota sin Bonif. (€)": results.monthly_payment_without_bonus,
                "Cuota con Bonif. (€)": results.monthly_payment_with_bonus,
                "Diferencia Cuota (€)": results.monthly_payment_without_bonus
                - results.monthly_payment_with_bonus,
                "Total sin Bonif. (€)": results.total_paid_without_bonus,
                "Total con Bonif. (€)": results.total_paid_with_bonus + results.total_bonus_costs,
                "Ahorro Real (€)": results.real_savings,
                "Ahorro (%)": results.savings_percentage,
                "¿Vale la pena?": "SÍ" if results.is_worth_it else "NO",
            }
        )

        rate += rate_step

    df = pd.DataFrame(results_list)
    df.to_excel(output_file, index=False)

    return output_file


def calculate_break_even_cost(
    mortgage_data: MortgageData, max_cost: float = 200.0, step: float = 5.0
) -> Dict[str, float]:
    """
    Calcula el coste máximo de bonificaciones para que valga la pena.

    Args:
        mortgage_data: Datos de la hipoteca (sin costes)
        max_cost: Coste máximo a probar
        step: Incremento del coste en cada iteración

    Returns:
        Diccionario con el análisis del punto de equilibrio
    """
    cost = 0.0
    break_even_cost = 0.0

    while cost <= max_cost:
        data = MortgageData(
            capital=mortgage_data.capital,
            interest_rate=mortgage_data.interest_rate,
            years=mortgage_data.years,
            payroll_bonus=mortgage_data.payroll_bonus,
            insurance_bonus=mortgage_data.insurance_bonus,
            card_bonus=mortgage_data.card_bonus,
            other_bonus=mortgage_data.other_bonus,
            insurance_cost_monthly=cost,
            card_annual_fee=0.0,
            other_costs_monthly=0.0,
        )

        calculator = MortgageCalculator(data)
        results = calculator.calculate()

        if results.is_worth_it:
            break_even_cost = cost
        else:
            break

        cost += step

    return {
        "coste_maximo_mensual": break_even_cost,
        "coste_maximo_anual": break_even_cost * 12,
        "coste_total_vida_prestamo": break_even_cost * 12 * mortgage_data.years,
    }


def recommend_best_bonus_combination(
    mortgage_data: MortgageData, bonuses: Dict[str, Dict[str, float]]
) -> Dict[str, any]:
    """
    Recomienda la mejor combinación de bonificaciones.

    Args:
        mortgage_data: Datos base de la hipoteca
        bonuses: Diccionario con bonificaciones disponibles y sus costes
                 Formato: {"nombre": {"bonus": 0.30, "cost_monthly": 40.0}}

    Returns:
        Diccionario con la recomendación

    Example:
        bonuses = {
            "nomina": {"bonus": 0.30, "cost_monthly": 0.0},
            "seguros": {"bonus": 0.50, "cost_monthly": 45.0},
            "tarjeta": {"bonus": 0.10, "cost_monthly": 5.0}
        }
        recommend_best_bonus_combination(mortgage_data, bonuses)
    """
    best_savings = float("-inf")
    best_combination = None
    best_results = None

    # Probar todas las combinaciones posibles
    bonus_names = list(bonuses.keys())
    n = len(bonus_names)

    for i in range(1, 2**n):
        # Generar combinación binaria
        combination = []
        total_bonus = 0.0
        total_cost = 0.0

        for j in range(n):
            if i & (1 << j):
                name = bonus_names[j]
                combination.append(name)
                total_bonus += bonuses[name]["bonus"]
                total_cost += bonuses[name].get("cost_monthly", 0.0)

        # Crear datos con esta combinación
        data = MortgageData(
            capital=mortgage_data.capital,
            interest_rate=mortgage_data.interest_rate,
            years=mortgage_data.years,
            payroll_bonus=(
                total_bonus if "nomina" in combination or "payroll" in combination else 0.0
            ),
            insurance_bonus=(
                total_bonus if "seguros" in combination or "insurance" in combination else 0.0
            ),
            card_bonus=total_bonus if "tarjeta" in combination or "card" in combination else 0.0,
            insurance_cost_monthly=total_cost,
            card_annual_fee=0.0,
            other_costs_monthly=0.0,
        )

        calculator = MortgageCalculator(data)
        results = calculator.calculate()

        if results.real_savings > best_savings:
            best_savings = results.real_savings
            best_combination = combination
            best_results = results

    return {
        "mejor_combinacion": best_combination,
        "ahorro_real": best_savings,
        "vale_la_pena": best_savings > 0,
        "resultados": best_results,
    }


def generate_payment_calendar(mortgage_data: MortgageData, with_bonus: bool = True) -> pd.DataFrame:
    """
    Genera un calendario de pagos detallado por años.

    Args:
        mortgage_data: Datos de la hipoteca
        with_bonus: Si usar bonificaciones o no

    Returns:
        DataFrame con el calendario anual
    """
    rate = mortgage_data.interest_rate
    if with_bonus:
        calculator = MortgageCalculator(mortgage_data)
        rate = max(0, rate - calculator.calculate_total_bonus())

    calculator = MortgageCalculator(mortgage_data)
    schedule = calculator.calculate_amortization_schedule(rate)

    # Agrupar por años
    yearly_data = []
    for year in range(1, mortgage_data.years + 1):
        start_month = (year - 1) * 12
        end_month = year * 12
        year_payments = schedule[start_month:end_month]

        total_payment = sum(p[1] for p in year_payments)
        total_interest = sum(p[2] for p in year_payments)
        total_principal = sum(p[3] for p in year_payments)
        final_balance = year_payments[-1][4]

        yearly_data.append(
            {
                "Año": year,
                "Pagos Totales (€)": total_payment,
                "Intereses (€)": total_interest,
                "Amortización Capital (€)": total_principal,
                "Pendiente (€)": final_balance,
            }
        )

    return pd.DataFrame(yearly_data)


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== EJEMPLOS DE UTILIDADES AVANZADAS ===\n")

    # Ejemplo 1: Comparar escenarios
    print("1. Comparando 3 bancos diferentes...")
    scenarios = [
        {
            "nombre": "Banco A - Sin bonificaciones",
            "data": MortgageData(capital=200000, interest_rate=3.50, years=30),
        },
        {
            "nombre": "Banco B - Con bonificaciones",
            "data": MortgageData(
                capital=200000,
                interest_rate=3.75,
                years=30,
                payroll_bonus=0.30,
                insurance_bonus=0.50,
                insurance_cost_monthly=45.0,
            ),
        },
        {
            "nombre": "Banco C - Tipo bajo",
            "data": MortgageData(capital=200000, interest_rate=3.10, years=30),
        },
    ]
    compare_file = compare_scenarios(scenarios)
    print(f"✓ Comparación guardada en: {compare_file}\n")

    # Ejemplo 2: Análisis de sensibilidad
    print("2. Análisis de sensibilidad al tipo de interés...")
    base_data = MortgageData(
        capital=200000,
        interest_rate=3.50,
        years=30,
        payroll_bonus=0.30,
        insurance_bonus=0.50,
        insurance_cost_monthly=45.0,
    )
    sensitivity_file = sensitivity_analysis(base_data, rate_range=(2.5, 4.5), rate_step=0.25)
    print(f"✓ Análisis guardado en: {sensitivity_file}\n")

    # Ejemplo 3: Punto de equilibrio
    print("3. Calculando coste máximo asumible...")
    break_even = calculate_break_even_cost(
        MortgageData(
            capital=200000, interest_rate=3.50, years=30, payroll_bonus=0.30, insurance_bonus=0.50
        )
    )
    print(f"✓ Coste máximo mensual: {break_even['coste_maximo_mensual']:.2f} €")
    print(f"✓ Coste máximo anual: {break_even['coste_maximo_anual']:.2f} €")
    print(f"✓ Coste total máximo: {break_even['coste_total_vida_prestamo']:,.2f} €\n")
