"""
Script principal para generar el análisis de hipoteca.
"""

from mortgage_calculator.excel_generator import ExcelGenerator
from mortgage_calculator.models import MortgageData


def main():
    """Función principal."""
    print("=" * 60)
    print("CALCULADORA DE BONIFICACIONES DE HIPOTECA")
    print("=" * 60)
    print()

    # Ejemplo de datos de hipoteca
    # Puedes modificar estos valores para tu caso particular
    mortgage_data = MortgageData(
        # Datos principales
        capital=180000.0,  # 200,000€ prestados
        interest_rate=2.90,  # 3.50% de interés anual
        years=30,  # 30 años
        # Bonificaciones en el tipo de interés
        payroll_bonus=0.40,  # 0.30% por domiciliar nómina
        life_insurance_bonus=0.40,  # 0.30% por seguro de vida
        home_insurance_bonus=0.10,  # 0.20% por seguro de hogar
        card_bonus=0.00,  # 0.10% por usar tarjeta
        other_bonus=0.00,  # 0.10% otras bonificaciones
        # Costes asociados a las bonificaciones
        life_insurance_cost_monthly=288.0/12,  # X/12€/mes seguro de vida
        home_insurance_cost_monthly=400.0/12,  # X/12€/mes seguro de hogar
        card_annual_fee=0.0,  # 0€/año la tarjeta
        other_costs_monthly=0.0,  # 0€/mes otros costes
    )

    print(f"Capital: {mortgage_data.capital:,.2f} €")
    print(f"Interés: {mortgage_data.interest_rate}%")
    print(f"Plazo: {mortgage_data.years} años")
    print()
    print("Generando análisis...")
    print()

    # Generar el reporte Excel
    generator = ExcelGenerator(mortgage_data)
    output_file = generator.generate_report("analisis_hipoteca.xlsx")

    print("✓ Reporte generado con éxito!")
    print(f"✓ Archivo guardado en: {output_file}")
    print()

    # Mostrar resumen en consola
    results = generator.results
    if results:
        print("=" * 60)
        print("RESUMEN DEL ANÁLISIS")
        print("=" * 60)
        print()
        print(f"¿Valen la pena las bonificaciones? {'SÍ ✓' if results.is_worth_it else 'NO ✗'}")
        print(f"Ahorro real: {results.real_savings:,.2f} €")
        print(f"Porcentaje de ahorro: {results.savings_percentage:.2f}%")
        print()
        print("SIN bonificaciones:")
        print(f"  - Cuota mensual: {results.monthly_payment_without_bonus:,.2f} €")
        print(f"  - Total a pagar: {results.total_paid_without_bonus:,.2f} €")
        print()
        print("CON bonificaciones:")
        print(f"  - Cuota mensual: {results.monthly_payment_with_bonus:,.2f} €")
        print(f"  - Total a pagar: {results.total_paid_with_bonus:,.2f} €")
        print(f"  - Coste bonificaciones: {results.total_bonus_costs:,.2f} €")
        print(
            f"  - Coste real total: {results.total_paid_with_bonus + results.total_bonus_costs:,.2f} €"
        )
        print()
        print("=" * 60)
        print()
        print("Abre el archivo Excel para ver el análisis completo con todas las tablas.")
        print()


if __name__ == "__main__":
    main()
