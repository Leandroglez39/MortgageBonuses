"""
Generador de archivos Excel con análisis de hipotecas.
"""
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pathlib import Path
from typing import Optional
from .models import MortgageData, MortgageResults
from .calculator import MortgageCalculator


class ExcelGenerator:
    """Generador de reportes Excel para análisis de hipotecas."""
    
    def __init__(self, mortgage_data: MortgageData):
        self.data = mortgage_data
        self.calculator = MortgageCalculator(mortgage_data)
        self.results: Optional[MortgageResults] = None
    
    def generate_report(self, output_path: str = "analisis_hipoteca.xlsx") -> str:
        """
        Genera el reporte completo en Excel.
        
        Args:
            output_path: Ruta donde guardar el archivo Excel
            
        Returns:
            Ruta del archivo generado
        """
        # Realizar cálculos
        self.results = self.calculator.calculate()
        
        # Crear el archivo Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            self._create_input_sheet(writer)
            self._create_summary_sheet(writer)
            self._create_comparison_sheet(writer)
            self._create_amortization_sheet(writer, with_bonus=False)
            self._create_amortization_sheet(writer, with_bonus=True)
            self._create_bonus_analysis_sheet(writer)
        
        # Aplicar formato
        self._apply_formatting(output_path)
        
        return str(Path(output_path).absolute())
    
    def _create_input_sheet(self, writer: pd.ExcelWriter):
        """Crea la hoja con los datos de entrada."""
        data = {
            'Concepto': [
                '=== DATOS DE LA HIPOTECA ===',
                'Capital prestado (€)',
                'Tasa de interés anual (%)',
                'Plazo (años)',
                '',
                '=== BONIFICACIONES ===',
                'Bonificación por nómina (%)',
                'Bonificación por seguros (%)',
                'Bonificación por tarjeta (%)',
                'Otras bonificaciones (%)',
                '',
                '=== COSTES DE BONIFICACIONES ===',
                'Coste mensual del seguro (€)',
                'Cuota anual de la tarjeta (€)',
                'Otros costes mensuales (€)',
            ],
            'Valor': [
                '',
                self.data.capital,
                self.data.interest_rate,
                self.data.years,
                '',
                '',
                self.data.payroll_bonus,
                self.data.insurance_bonus,
                self.data.card_bonus,
                self.data.other_bonus,
                '',
                '',
                self.data.insurance_cost_monthly,
                self.data.card_annual_fee,
                self.data.other_costs_monthly,
            ]
        }
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Datos de Entrada', index=False)
    
    def _create_summary_sheet(self, writer: pd.ExcelWriter):
        """Crea la hoja resumen con los resultados principales."""
        if not self.results:
            return
        
        data = {
            'Concepto': [
                '=== RESUMEN EJECUTIVO ===',
                '',
                '¿Vale la pena la bonificación?',
                'Ahorro real (€)',
                'Porcentaje de ahorro (%)',
                '',
                '=== SIN BONIFICACIONES ===',
                'Cuota mensual (€)',
                'Intereses totales (€)',
                'Total a pagar (€)',
                'Tasa efectiva (%)',
                '',
                '=== CON BONIFICACIONES ===',
                'Cuota mensual (€)',
                'Intereses totales (€)',
                'Total a pagar (€)',
                'Coste total bonificaciones (€)',
                'Coste real total (€)',
                'Tasa efectiva (%)',
                '',
                '=== DIFERENCIAS ===',
                'Ahorro en cuota mensual (€)',
                'Ahorro en intereses (€)',
                'Ahorro nominal (€)',
                'Menos: Coste bonificaciones (€)',
                'Ahorro real (€)',
            ],
            'Valor': [
                '',
                '',
                'SÍ ✓' if self.results.is_worth_it else 'NO ✗',
                self.results.real_savings,
                self.results.savings_percentage,
                '',
                '',
                self.results.monthly_payment_without_bonus,
                self.results.total_interest_without_bonus,
                self.results.total_paid_without_bonus,
                self.results.effective_rate_without_bonus,
                '',
                '',
                self.results.monthly_payment_with_bonus,
                self.results.total_interest_with_bonus,
                self.results.total_paid_with_bonus,
                self.results.total_bonus_costs,
                self.results.total_paid_with_bonus + self.results.total_bonus_costs,
                self.results.effective_rate_with_bonus,
                '',
                '',
                self.results.monthly_payment_without_bonus - self.results.monthly_payment_with_bonus,
                self.results.total_interest_without_bonus - self.results.total_interest_with_bonus,
                self.results.total_paid_without_bonus - self.results.total_paid_with_bonus,
                self.results.total_bonus_costs,
                self.results.real_savings,
            ]
        }
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Resumen', index=False)
    
    def _create_comparison_sheet(self, writer: pd.ExcelWriter):
        """Crea una hoja de comparación detallada."""
        if not self.results:
            return
        
        data = {
            'Concepto': [
                'Capital prestado',
                'Tasa de interés',
                'Bonificaciones aplicadas',
                'Tasa con bonificaciones',
                'Plazo (meses)',
                '',
                'Cuota mensual',
                'Total intereses',
                'Total a pagar',
                'Costes bonificaciones',
                'Coste real total',
            ],
            'Sin Bonificaciones': [
                f'{self.data.capital:,.2f} €',
                f'{self.data.interest_rate:.2f}%',
                '0.00%',
                f'{self.data.interest_rate:.2f}%',
                self.data.years * 12,
                '',
                f'{self.results.monthly_payment_without_bonus:,.2f} €',
                f'{self.results.total_interest_without_bonus:,.2f} €',
                f'{self.results.total_paid_without_bonus:,.2f} €',
                '0.00 €',
                f'{self.results.total_paid_without_bonus:,.2f} €',
            ],
            'Con Bonificaciones': [
                f'{self.data.capital:,.2f} €',
                f'{self.data.interest_rate:.2f}%',
                f'{self.calculator.calculate_total_bonus():.2f}%',
                f'{max(0, self.data.interest_rate - self.calculator.calculate_total_bonus()):.2f}%',
                self.data.years * 12,
                '',
                f'{self.results.monthly_payment_with_bonus:,.2f} €',
                f'{self.results.total_interest_with_bonus:,.2f} €',
                f'{self.results.total_paid_with_bonus:,.2f} €',
                f'{self.results.total_bonus_costs:,.2f} €',
                f'{self.results.total_paid_with_bonus + self.results.total_bonus_costs:,.2f} €',
            ],
            'Diferencia': [
                '0.00 €',
                '0.00%',
                f'{self.calculator.calculate_total_bonus():.2f}%',
                f'{-self.calculator.calculate_total_bonus():.2f}%',
                '0',
                '',
                f'{self.results.monthly_payment_without_bonus - self.results.monthly_payment_with_bonus:,.2f} €',
                f'{self.results.total_interest_without_bonus - self.results.total_interest_with_bonus:,.2f} €',
                f'{self.results.total_paid_without_bonus - self.results.total_paid_with_bonus:,.2f} €',
                f'-{self.results.total_bonus_costs:,.2f} €',
                f'{self.results.real_savings:,.2f} €',
            ]
        }
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Comparación', index=False)
    
    def _create_amortization_sheet(self, writer: pd.ExcelWriter, with_bonus: bool = False):
        """Crea la hoja con la tabla de amortización."""
        rate = self.data.interest_rate
        if with_bonus:
            rate = max(0, rate - self.calculator.calculate_total_bonus())
        
        schedule = self.calculator.calculate_amortization_schedule(rate)
        
        data = {
            'Mes': [s[0] for s in schedule],
            'Cuota (€)': [round(s[1], 2) for s in schedule],
            'Intereses (€)': [round(s[2], 2) for s in schedule],
            'Amortización (€)': [round(s[3], 2) for s in schedule],
            'Pendiente (€)': [round(s[4], 2) for s in schedule],
        }
        
        df = pd.DataFrame(data)
        sheet_name = 'Amortización CON Bonif.' if with_bonus else 'Amortización SIN Bonif.'
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def _create_bonus_analysis_sheet(self, writer: pd.ExcelWriter):
        """Crea una hoja con análisis detallado de bonificaciones."""
        if not self.results:
            return
        
        months = self.data.years * 12
        monthly_insurance = self.data.insurance_cost_monthly
        yearly_card = self.data.card_annual_fee
        monthly_other = self.data.other_costs_monthly
        
        data = {
            'Bonificación': [
                'Domiciliación de nómina',
                'Contratación de seguros',
                'Uso de tarjeta',
                'Otras bonificaciones',
                '',
                'TOTAL BONIFICACIONES',
            ],
            'Reducción de Tipo (%)': [
                self.data.payroll_bonus,
                self.data.insurance_bonus,
                self.data.card_bonus,
                self.data.other_bonus,
                '',
                self.calculator.calculate_total_bonus(),
            ],
            'Coste Mensual (€)': [
                0,
                monthly_insurance,
                yearly_card / 12,
                monthly_other,
                '',
                monthly_insurance + (yearly_card / 12) + monthly_other,
            ],
            'Coste Total (€)': [
                0,
                monthly_insurance * months,
                yearly_card * self.data.years,
                monthly_other * months,
                '',
                self.results.total_bonus_costs,
            ],
            'Ahorro en Intereses (€)': [
                '-',
                '-',
                '-',
                '-',
                '',
                self.results.total_interest_without_bonus - self.results.total_interest_with_bonus,
            ],
        }
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Análisis Bonificaciones', index=False)
    
    def _apply_formatting(self, file_path: str):
        """Aplica formato visual al archivo Excel."""
        wb = load_workbook(file_path)
        
        # Estilos
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        
        section_fill = PatternFill(start_color="B4C7E7", end_color="B4C7E7", fill_type="solid")
        section_font = Font(bold=True, size=10)
        
        highlight_fill = PatternFill(start_color="C6E0B4", end_color="C6E0B4", fill_type="solid")
        warning_fill = PatternFill(start_color="F4B084", end_color="F4B084", fill_type="solid")
        
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Formatear cada hoja
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            
            # Ajustar anchos de columna
            for column in ws.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                for cell in column:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                adjusted_width = min(50, max(12, max_length + 2))
                ws.column_dimensions[column_letter].width = adjusted_width
            
            # Formatear encabezados
            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = border
            
            # Formatear filas con secciones (===)
            for row in ws.iter_rows(min_row=2):
                if row[0].value and str(row[0].value).startswith('==='):
                    row[0].fill = section_fill
                    row[0].font = section_font
                
                # Resaltar la decisión principal
                if 'vale la pena' in str(row[0].value).lower():
                    if 'SÍ' in str(row[1].value):
                        row[1].fill = highlight_fill
                        row[1].font = Font(bold=True, size=12)
                    else:
                        row[1].fill = warning_fill
                        row[1].font = Font(bold=True, size=12)
        
        wb.save(file_path)
