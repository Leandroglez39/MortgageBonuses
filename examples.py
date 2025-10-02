"""
Ejemplo de uso avanzado de la calculadora de hipotecas.
"""

from mortgage_calculator.calculator import MortgageCalculator
from mortgage_calculator.excel_generator import ExcelGenerator
from mortgage_calculator.models import MortgageData


def ejemplo_basico():
    """Ejemplo básico sin bonificaciones."""
    print("=== EJEMPLO BÁSICO ===")

    data = MortgageData(capital=150000.0, interest_rate=3.0, years=25)

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    print(f"Cuota mensual: {results.monthly_payment_without_bonus:.2f} €")
    print(f"Total intereses: {results.total_interest_without_bonus:,.2f} €")
    print()


def ejemplo_con_bonificaciones():
    """Ejemplo con bonificaciones que valen la pena."""
    print("=== EJEMPLO CON BONIFICACIONES RENTABLES ===")

    data = MortgageData(
        capital=300000.0,
        interest_rate=3.75,
        years=30,
        payroll_bonus=0.40,
        life_insurance_bonus=0.35,
        home_insurance_bonus=0.25,
        card_bonus=0.15,
        life_insurance_cost_monthly=20.0,
        home_insurance_cost_monthly=15.0,
        card_annual_fee=30.0,
    )

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    print(f"¿Vale la pena? {'SÍ' if results.is_worth_it else 'NO'}")
    print(f"Ahorro real: {results.real_savings:,.2f} €")
    print(f"Ahorro porcentual: {results.savings_percentage:.2f}%")
    print()


def ejemplo_con_bonificaciones_caras():
    """Ejemplo donde las bonificaciones son muy caras."""
    print("=== EJEMPLO CON BONIFICACIONES NO RENTABLES ===")

    data = MortgageData(
        capital=180000.0,
        interest_rate=2.80,
        years=20,
        payroll_bonus=0.20,
        life_insurance_bonus=0.15,
        home_insurance_bonus=0.15,
        life_insurance_cost_monthly=70.0,  # Seguros muy caros
        home_insurance_cost_monthly=50.0,
        other_costs_monthly=50.0,
    )

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    print(f"¿Vale la pena? {'SÍ' if results.is_worth_it else 'NO'}")
    print(f"Ahorro real: {results.real_savings:,.2f} €")
    print(f"Total costes bonificaciones: {results.total_bonus_costs:,.2f} €")
    print()


def generar_multiples_reportes():
    """Genera varios reportes para comparar escenarios."""
    print("=== GENERANDO MÚLTIPLES REPORTES ===")

    escenarios = [
        {
            "nombre": "escenario_conservador",
            "data": MortgageData(
                capital=200000.0,
                interest_rate=3.50,
                years=30,
                payroll_bonus=0.25,
                life_insurance_bonus=0.20,
                home_insurance_bonus=0.20,
                life_insurance_cost_monthly=20.0,
                home_insurance_cost_monthly=20.0,
            ),
        },
        {
            "nombre": "escenario_agresivo",
            "data": MortgageData(
                capital=200000.0,
                interest_rate=3.50,
                years=30,
                payroll_bonus=0.30,
                life_insurance_bonus=0.35,
                home_insurance_bonus=0.25,
                card_bonus=0.15,
                other_bonus=0.10,
                life_insurance_cost_monthly=25.0,
                home_insurance_cost_monthly=20.0,
                card_annual_fee=50.0,
                other_costs_monthly=15.0,
            ),
        },
        {
            "nombre": "escenario_sin_bonificaciones",
            "data": MortgageData(capital=200000.0, interest_rate=3.50, years=30),
        },
    ]

    for escenario in escenarios:
        generator = ExcelGenerator(escenario["data"])
        output = generator.generate_report(f'{escenario["nombre"]}.xlsx')
        print(f"✓ Generado: {output}")

    print()


def analizar_sensibilidad():
    """Analiza cómo cambia el ahorro con diferentes tipos de interés."""
    print("=== ANÁLISIS DE SENSIBILIDAD ===")
    print("Tipo | Ahorro Real | ¿Vale la pena?")
    print("-" * 45)

    for rate in [2.5, 3.0, 3.5, 4.0, 4.5]:
        data = MortgageData(
            capital=200000.0,
            interest_rate=rate,
            years=30,
            payroll_bonus=0.30,
            life_insurance_bonus=0.30,
            home_insurance_bonus=0.20,
            life_insurance_cost_monthly=25.0,
            home_insurance_cost_monthly=20.0,
        )

        calculator = MortgageCalculator(data)
        results = calculator.calculate()

        print(
            f"{rate}% | {results.real_savings:>11,.0f} € | {'✓ SÍ' if results.is_worth_it else '✗ NO'}"
        )

    print()


if __name__ == "__main__":
    ejemplo_basico()
    ejemplo_con_bonificaciones()
    ejemplo_con_bonificaciones_caras()
    analizar_sensibilidad()

    # Descomentar para generar múltiples reportes
    # generar_multiples_reportes()
