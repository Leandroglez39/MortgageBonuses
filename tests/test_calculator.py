"""
Tests para el módulo de cálculo de hipotecas.
"""

from mortgage_calculator.calculator import MortgageCalculator
from mortgage_calculator.models import MortgageData


def test_mortgage_data_creation():
    """Test que se pueden crear datos de hipoteca correctamente."""
    data = MortgageData(capital=100000.0, interest_rate=3.0, years=20)

    assert data.capital == 100000.0
    assert data.interest_rate == 3.0
    assert data.years == 20
    assert data.payroll_bonus == 0.0
    assert data.insurance_bonus == 0.0


def test_calculate_monthly_payment_without_interest():
    """Test del cálculo de cuota mensual sin interés."""
    data = MortgageData(capital=120000.0, interest_rate=0.0, years=10)

    calculator = MortgageCalculator(data)
    monthly_payment = calculator.calculate_monthly_payment(0.0)

    # 120000 / (10 * 12) = 1000
    assert abs(monthly_payment - 1000.0) < 0.01


def test_calculate_monthly_payment_with_interest():
    """Test del cálculo de cuota mensual con interés."""
    data = MortgageData(capital=100000.0, interest_rate=3.0, years=20)

    calculator = MortgageCalculator(data)
    monthly_payment = calculator.calculate_monthly_payment(3.0)

    # La cuota debería estar entre 500 y 600 euros
    assert 500 < monthly_payment < 600


def test_total_bonus_calculation():
    """Test del cálculo de bonificaciones totales."""
    data = MortgageData(
        capital=100000.0,
        interest_rate=3.5,
        years=20,
        payroll_bonus=0.25,
        insurance_bonus=0.40,
        card_bonus=0.15,
        other_bonus=0.10,
    )

    calculator = MortgageCalculator(data)
    total_bonus = calculator.calculate_total_bonus()

    assert total_bonus == 0.90


def test_total_bonus_costs():
    """Test del cálculo de costes de bonificaciones."""
    data = MortgageData(
        capital=100000.0,
        interest_rate=3.0,
        years=10,
        insurance_cost_monthly=50.0,
        card_annual_fee=60.0,
        other_costs_monthly=20.0,
    )

    calculator = MortgageCalculator(data)
    total_costs = calculator.calculate_total_bonus_costs()

    # (50 + 20) * 120 meses + 60 * 10 años = 8400 + 600 = 9000
    assert total_costs == 9000.0


def test_calculate_results_without_bonus():
    """Test de cálculos completos sin bonificaciones."""
    data = MortgageData(capital=150000.0, interest_rate=3.0, years=25)

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    # Verificaciones básicas
    assert results.monthly_payment_without_bonus > 0
    assert results.total_interest_without_bonus > 0
    assert results.total_paid_without_bonus == data.capital + results.total_interest_without_bonus
    assert results.total_bonus_costs == 0.0
    assert results.real_savings == 0.0  # Sin bonificaciones, no hay ahorro


def test_calculate_results_with_bonus():
    """Test de cálculos completos con bonificaciones."""
    data = MortgageData(
        capital=200000.0,
        interest_rate=3.5,
        years=30,
        payroll_bonus=0.30,
        insurance_bonus=0.50,
        insurance_cost_monthly=40.0,
    )

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    # La cuota con bonificaciones debe ser menor
    assert results.monthly_payment_with_bonus < results.monthly_payment_without_bonus

    # Los intereses con bonificaciones deben ser menores
    assert results.total_interest_with_bonus < results.total_interest_without_bonus

    # Debe haber costes de bonificaciones
    assert results.total_bonus_costs > 0

    # El tipo efectivo con bonificaciones debe ser menor
    assert results.effective_rate_with_bonus < results.effective_rate_without_bonus


def test_amortization_schedule_length():
    """Test que la tabla de amortización tiene el número correcto de pagos."""
    data = MortgageData(capital=100000.0, interest_rate=3.0, years=15)

    calculator = MortgageCalculator(data)
    schedule = calculator.calculate_amortization_schedule(3.0)

    # Debe haber 15 años * 12 meses = 180 pagos
    assert len(schedule) == 180


def test_amortization_schedule_final_balance():
    """Test que el saldo final de la tabla de amortización es cero."""
    data = MortgageData(capital=100000.0, interest_rate=3.0, years=20)

    calculator = MortgageCalculator(data)
    schedule = calculator.calculate_amortization_schedule(3.0)

    # El último pago debe dejar saldo cero
    final_balance = schedule[-1][4]
    assert final_balance == 0.0


def test_bonus_worth_it_positive():
    """Test que detecta correctamente cuando las bonificaciones valen la pena."""
    data = MortgageData(
        capital=200000.0,
        interest_rate=4.0,
        years=30,
        payroll_bonus=0.50,
        insurance_bonus=0.70,
        insurance_cost_monthly=30.0,  # Coste bajo
    )

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    assert results.is_worth_it is True
    assert results.real_savings > 0


def test_bonus_not_worth_it():
    """Test que detecta correctamente cuando las bonificaciones NO valen la pena."""
    data = MortgageData(
        capital=150000.0,
        interest_rate=2.5,
        years=20,
        payroll_bonus=0.20,
        insurance_bonus=0.30,
        insurance_cost_monthly=200.0,  # Coste muy alto
        other_costs_monthly=100.0,
    )

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    assert results.is_worth_it is False
    assert results.real_savings < 0


def test_zero_bonus_equals_no_bonus():
    """Test que bonificaciones de 0% dan el mismo resultado que sin bonificaciones."""
    data = MortgageData(
        capital=100000.0, interest_rate=3.0, years=15, payroll_bonus=0.0, insurance_bonus=0.0
    )

    calculator = MortgageCalculator(data)
    results = calculator.calculate()

    # Las cuotas deben ser iguales
    assert abs(results.monthly_payment_with_bonus - results.monthly_payment_without_bonus) < 0.01


def test_high_bonus_reduces_rate_significantly():
    """Test que bonificaciones altas reducen significativamente el tipo."""
    data = MortgageData(
        capital=200000.0,
        interest_rate=4.0,
        years=25,
        payroll_bonus=0.50,
        insurance_bonus=1.00,
        card_bonus=0.20,
        insurance_cost_monthly=50.0,
    )

    calculator = MortgageCalculator(data)
    total_bonus = calculator.calculate_total_bonus()
    results = calculator.calculate()

    assert total_bonus == 1.70
    assert results.effective_rate_with_bonus < 3.0  # Tipo efectivo mucho menor
