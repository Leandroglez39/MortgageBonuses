"""
Módulo de cálculo de hipotecas y bonificaciones.
"""

import math
from typing import List, Tuple

from .models import MortgageData, MortgageResults


class MortgageCalculator:
    """Calculadora de hipotecas con análisis de bonificaciones."""

    def __init__(self, mortgage_data: MortgageData):
        self.data = mortgage_data

    def calculate_monthly_payment(self, annual_rate: float) -> float:
        """
        Calcula la cuota mensual usando la fórmula de amortización francesa.

        Args:
            annual_rate: Tasa de interés anual en porcentaje

        Returns:
            Cuota mensual
        """
        monthly_rate = annual_rate / 100 / 12
        n_payments = self.data.years * 12

        if monthly_rate == 0:
            return self.data.capital / n_payments

        payment = (
            self.data.capital
            * (monthly_rate * math.pow(1 + monthly_rate, n_payments))
            / (math.pow(1 + monthly_rate, n_payments) - 1)
        )

        return payment

    def calculate_amortization_schedule(
        self, annual_rate: float
    ) -> List[Tuple[int, float, float, float, float]]:
        """
        Calcula la tabla de amortización completa.

        Args:
            annual_rate: Tasa de interés anual en porcentaje

        Returns:
            Lista de tuplas (mes, cuota, intereses, amortización, pendiente)
        """
        monthly_rate = annual_rate / 100 / 12
        monthly_payment = self.calculate_monthly_payment(annual_rate)
        n_payments = self.data.years * 12

        schedule = []
        remaining_balance = self.data.capital

        for month in range(1, n_payments + 1):
            interest = remaining_balance * monthly_rate
            principal = monthly_payment - interest
            remaining_balance -= principal

            # Ajuste para el último pago (por redondeos)
            if month == n_payments:
                remaining_balance = 0

            schedule.append(
                (month, monthly_payment, interest, principal, max(0, remaining_balance))
            )

        return schedule

    def calculate_total_bonus(self) -> float:
        """Calcula la bonificación total acumulada."""
        return (
            self.data.payroll_bonus
            + self.data.life_insurance_bonus
            + self.data.home_insurance_bonus
            + self.data.card_bonus
            + self.data.other_bonus
        )

    def calculate_total_bonus_costs(self) -> float:
        """Calcula el coste total de las bonificaciones durante la vida del préstamo."""
        months = self.data.years * 12
        monthly_costs = (
            self.data.life_insurance_cost_monthly
            + self.data.home_insurance_cost_monthly
            + self.data.other_costs_monthly
        )
        annual_costs = self.data.card_annual_fee

        return (monthly_costs * months) + (annual_costs * self.data.years)

    def calculate(self) -> MortgageResults:
        """
        Realiza todos los cálculos y devuelve los resultados.

        Returns:
            MortgageResults con todos los cálculos
        """
        # Cálculos sin bonificaciones
        monthly_without = self.calculate_monthly_payment(self.data.interest_rate)
        schedule_without = self.calculate_amortization_schedule(self.data.interest_rate)
        total_interest_without = sum(payment[2] for payment in schedule_without)
        total_paid_without = self.data.capital + total_interest_without

        # Cálculos con bonificaciones
        total_bonus = self.calculate_total_bonus()
        rate_with_bonus = max(0, self.data.interest_rate - total_bonus)

        monthly_with = self.calculate_monthly_payment(rate_with_bonus)
        schedule_with = self.calculate_amortization_schedule(rate_with_bonus)
        total_interest_with = sum(payment[2] for payment in schedule_with)
        total_paid_with = self.data.capital + total_interest_with

        # Costes de bonificaciones
        total_bonus_costs = self.calculate_total_bonus_costs()

        # Análisis
        nominal_savings = total_paid_without - total_paid_with
        real_savings = nominal_savings - total_bonus_costs
        savings_percentage = (real_savings / total_paid_without) * 100
        is_worth_it = real_savings > 0

        # Tasas efectivas (considerando costes)
        effective_rate_without = self.data.interest_rate
        effective_cost_with = total_paid_with + total_bonus_costs
        effective_rate_with = self._calculate_effective_rate(effective_cost_with)

        return MortgageResults(
            monthly_payment_without_bonus=monthly_without,
            total_interest_without_bonus=total_interest_without,
            total_paid_without_bonus=total_paid_without,
            monthly_payment_with_bonus=monthly_with,
            total_interest_with_bonus=total_interest_with,
            total_paid_with_bonus=total_paid_with,
            total_bonus_costs=total_bonus_costs,
            real_savings=real_savings,
            savings_percentage=savings_percentage,
            is_worth_it=is_worth_it,
            effective_rate_without_bonus=effective_rate_without,
            effective_rate_with_bonus=effective_rate_with,
        )

    def _calculate_effective_rate(self, total_cost: float) -> float:
        """
        Calcula la tasa efectiva basada en el coste total.

        Args:
            total_cost: Coste total pagado

        Returns:
            Tasa efectiva anual en porcentaje
        """
        total_interest = total_cost - self.data.capital
        # TIR aproximada usando el método simple
        annual_interest = total_interest / self.data.years
        effective_rate = (annual_interest / self.data.capital) * 100
        return effective_rate
