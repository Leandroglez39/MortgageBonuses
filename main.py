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
        capital=200000.0,  # 200,000€ prestados
        interest_rate=3.50,  # 3.50% de interés anual
        years=30,  # 30 años
        # Bonificaciones en el tipo de interés
        payroll_bonus=0.30,  # 0.30% por domiciliar nómina
        insurance_bonus=0.50,  # 0.50% por contratar seguros
        card_bonus=0.10,  # 0.10% por usar tarjeta
        other_bonus=0.10,  # 0.10% otras bonificaciones
        # Costes asociados a las bonificaciones
        insurance_cost_monthly=45.0,  # 45€/mes el seguro
        card_annual_fee=50.0,  # 50€/año la tarjeta
        other_costs_monthly=10.0,  # 10€/mes otros costes
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
