"""
Script interactivo para crear análisis de hipoteca.
Pide los datos al usuario en lugar de editar el código.
"""

from mortgage_calculator.excel_generator import ExcelGenerator
from mortgage_calculator.models import MortgageData


def obtener_float(mensaje: str, default: float = 0.0) -> float:
    """Solicita un número flotante al usuario."""
    while True:
        try:
            valor = input(f"{mensaje} [{default}]: ").strip()
            if not valor:
                return default
            return float(valor)
        except ValueError:
            print("❌ Por favor, introduce un número válido.")


def obtener_int(mensaje: str, default: int = 0) -> int:
    """Solicita un número entero al usuario."""
    while True:
        try:
            valor = input(f"{mensaje} [{default}]: ").strip()
            if not valor:
                return default
            return int(valor)
        except ValueError:
            print("❌ Por favor, introduce un número entero válido.")


def obtener_nombre_archivo() -> str:
    """Solicita el nombre del archivo de salida."""
    nombre = input("Nombre del archivo Excel [analisis_hipoteca.xlsx]: ").strip()
    if not nombre:
        return "analisis_hipoteca.xlsx"
    if not nombre.endswith(".xlsx"):
        nombre += ".xlsx"
    return nombre


def main():
    """Función principal interactiva."""
    print("=" * 70)
    print("CALCULADORA INTERACTIVA DE BONIFICACIONES DE HIPOTECA")
    print("=" * 70)
    print()
    print("Introduce los datos de tu hipoteca.")
    print("(Presiona Enter para usar el valor por defecto)")
    print()

    # Datos principales
    print("--- DATOS PRINCIPALES ---")
    capital = obtener_float("Capital prestado (€)", 200000.0)
    interest_rate = obtener_float("Tipo de interés anual (%)", 3.5)
    years = obtener_int("Plazo (años)", 30)
    print()

    # Bonificaciones
    print("--- BONIFICACIONES (reducción del tipo de interés en %) ---")
    payroll_bonus = obtener_float("Bonificación por domiciliar nómina (%)", 0.30)
    insurance_bonus = obtener_float("Bonificación por contratar seguros (%)", 0.50)
    card_bonus = obtener_float("Bonificación por usar tarjeta (%)", 0.10)
    other_bonus = obtener_float("Otras bonificaciones (%)", 0.10)
    print()

    # Costes
    print("--- COSTES DE LAS BONIFICACIONES ---")
    insurance_cost = obtener_float("Coste mensual del seguro (€)", 45.0)
    card_fee = obtener_float("Cuota anual de la tarjeta (€)", 50.0)
    other_costs = obtener_float("Otros costes mensuales (€)", 10.0)
    print()

    # Nombre del archivo
    output_file = obtener_nombre_archivo()
    print()

    # Crear los datos
    mortgage_data = MortgageData(
        capital=capital,
        interest_rate=interest_rate,
        years=years,
        payroll_bonus=payroll_bonus,
        insurance_bonus=insurance_bonus,
        card_bonus=card_bonus,
        other_bonus=other_bonus,
        insurance_cost_monthly=insurance_cost,
        card_annual_fee=card_fee,
        other_costs_monthly=other_costs,
    )

    # Generar el reporte
    print("Generando análisis...")
    generator = ExcelGenerator(mortgage_data)
    output_path = generator.generate_report(output_file)

    print()
    print("=" * 70)
    print("✓ REPORTE GENERADO CON ÉXITO!")
    print("=" * 70)
    print(f"Archivo: {output_path}")
    print()

    # Mostrar resumen
    results = generator.results
    if results:
        print("--- RESUMEN ---")
        print()
        decision = "SÍ ✓" if results.is_worth_it else "NO ✗"
        print(f"¿Valen la pena las bonificaciones? {decision}")
        print()
        print(f"Ahorro real total: {results.real_savings:,.2f} €")
        print(f"Porcentaje de ahorro: {results.savings_percentage:.2f}%")
        print()

        if results.is_worth_it:
            print("💡 Las bonificaciones son rentables.")
            print(f"   Ahorrarás {results.real_savings:,.2f} € durante la vida del préstamo.")
        else:
            print("⚠️  Las bonificaciones NO son rentables.")
            print(f"   Perderás {abs(results.real_savings):,.2f} € por los costes adicionales.")

        print()
        print("Cuotas mensuales:")
        print(f"  • Sin bonificaciones: {results.monthly_payment_without_bonus:,.2f} €")
        print(f"  • Con bonificaciones: {results.monthly_payment_with_bonus:,.2f} €")
        print(
            f"  • Diferencia: {results.monthly_payment_without_bonus - results.monthly_payment_with_bonus:,.2f} € menos/mes"
        )
        print()
        print("Totales:")
        print(f"  • Sin bonificaciones: {results.total_paid_without_bonus:,.2f} €")
        print(
            f"  • Con bonificaciones: {results.total_paid_with_bonus + results.total_bonus_costs:,.2f} €"
        )
        print(f"  • Costes bonificaciones: {results.total_bonus_costs:,.2f} €")
        print()

    print("=" * 70)
    print("Abre el archivo Excel para ver el análisis completo.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
