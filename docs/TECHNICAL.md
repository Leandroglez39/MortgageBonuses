# Documentación Técnica - MortgageBonuses

## 🏗️ Arquitectura del Proyecto

### Patrón de Diseño

El proyecto sigue un patrón **MVC simplificado**:

- **Model** (`models.py`): Clases de datos usando `@dataclass`
- **Controller** (`calculator.py`): Lógica de negocio y cálculos
- **View** (`excel_generator.py`): Presentación de resultados

### Diagrama de Componentes

```
┌─────────────────┐
│  main.py        │  ← Scripts de usuario
│  interactive.py │
│  examples.py    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  mortgage_calculator (Package)      │
│  ┌─────────────────────────────┐   │
│  │ models.py                   │   │ ← Modelos de datos
│  │ - MortgageData              │   │
│  │ - MortgageResults           │   │
│  └──────────┬──────────────────┘   │
│             ▼                       │
│  ┌─────────────────────────────┐   │
│  │ calculator.py               │   │ ← Lógica de negocio
│  │ - MortgageCalculator        │   │
│  │   - calculate_monthly_...   │   │
│  │   - calculate_amortiz...    │   │
│  │   - calculate()             │   │
│  └──────────┬──────────────────┘   │
│             ▼                       │
│  ┌─────────────────────────────┐   │
│  │ excel_generator.py          │   │ ← Generación de reportes
│  │ - ExcelGenerator            │   │
│  │   - generate_report()       │   │
│  │   - _create_*_sheet()       │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## 📐 Fórmulas Matemáticas

### Cuota Mensual (Sistema Francés)

$$
C = P \times \frac{i(1+i)^n}{(1+i)^n - 1}
$$

Donde:
- $C$ = Cuota mensual
- $P$ = Capital prestado (principal)
- $i$ = Tipo de interés mensual (anual / 12 / 100)
- $n$ = Número total de pagos (años × 12)

### Intereses del Mes

$$
I_m = S_{m-1} \times i
$$

Donde:
- $I_m$ = Intereses del mes $m$
- $S_{m-1}$ = Saldo pendiente al final del mes anterior
- $i$ = Tipo de interés mensual

### Amortización del Mes

$$
A_m = C - I_m
$$

Donde:
- $A_m$ = Capital amortizado en el mes $m$
- $C$ = Cuota mensual
- $I_m$ = Intereses del mes $m$

### Saldo Pendiente

$$
S_m = S_{m-1} - A_m
$$

### Tipo Efectivo

$$
TAE = \left(\frac{Total\ Pagado - Capital}{Capital \times Años}\right) \times 100
$$

## 🔍 Clases Principales

### MortgageData

```python
@dataclass
class MortgageData:
    """Datos de entrada de la hipoteca."""
    capital: float                    # Capital prestado
    interest_rate: float              # Tipo anual (%)
    years: int                        # Plazo
    
    # Bonificaciones (reducción del tipo)
    payroll_bonus: float = 0.0
    insurance_bonus: float = 0.0
    card_bonus: float = 0.0
    other_bonus: float = 0.0
    
    # Costes
    insurance_cost_monthly: float = 0.0
    card_annual_fee: float = 0.0
    other_costs_monthly: float = 0.0
```

**Uso:**
```python
data = MortgageData(
    capital=200000.0,
    interest_rate=3.5,
    years=30,
    payroll_bonus=0.3,
    insurance_cost_monthly=45.0
)
```

### MortgageCalculator

```python
class MortgageCalculator:
    """Motor de cálculos."""
    
    def __init__(self, mortgage_data: MortgageData)
    
    def calculate_monthly_payment(self, annual_rate: float) -> float
        """Calcula la cuota mensual."""
    
    def calculate_amortization_schedule(self, annual_rate: float) 
        -> List[Tuple[int, float, float, float, float]]
        """Genera la tabla de amortización.
        
        Returns:
            Lista de (mes, cuota, intereses, amortización, pendiente)
        """
    
    def calculate(self) -> MortgageResults
        """Realiza todos los cálculos y devuelve resultados."""
```

**Uso:**
```python
calculator = MortgageCalculator(data)
results = calculator.calculate()
print(results.monthly_payment_with_bonus)
```

### ExcelGenerator

```python
class ExcelGenerator:
    """Generador de reportes Excel."""
    
    def __init__(self, mortgage_data: MortgageData)
    
    def generate_report(self, output_path: str = "analisis.xlsx") -> str
        """Genera el reporte completo.
        
        Returns:
            Ruta absoluta del archivo generado
        """
```

**Uso:**
```python
generator = ExcelGenerator(data)
file_path = generator.generate_report("mi_analisis.xlsx")
```

## 🧪 Testing

### Estructura de Tests

```python
tests/
├── __init__.py
└── test_calculator.py    # 13 tests

# Categorías de tests:
1. Tests de creación de datos
2. Tests de cálculo de cuota
3. Tests de bonificaciones
4. Tests de costes
5. Tests de resultados completos
6. Tests de amortización
7. Tests de decisión (vale la pena o no)
```

### Ejecutar Tests

```bash
# Todos los tests
poetry run pytest

# Con verbosidad
poetry run pytest -v

# Un test específico
poetry run pytest tests/test_calculator.py::test_bonus_worth_it_positive

# Con cobertura
poetry run pytest --cov=mortgage_calculator
```

### Coverage

```bash
# Instalar coverage
poetry add --group dev pytest-cov

# Ejecutar con cobertura
poetry run pytest --cov=mortgage_calculator --cov-report=html

# Ver reporte
open htmlcov/index.html
```

## 📦 Dependencias

### Producción

```toml
[project.dependencies]
openpyxl = "^3.1.5"    # Manipulación de archivos Excel
pandas = "^2.3.3"      # Estructuras de datos y análisis
numpy = "^2.3.3"       # Operaciones numéricas
```

### Desarrollo

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.4.2"      # Framework de testing
```

## 🔧 Configuración

### pyproject.toml

```toml
[project]
name = "mortgage-bonuses"
version = "0.1.0"
requires-python = ">=3.11"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

## 📊 Formato de Datos

### Entrada (JSON equivalente)

```json
{
  "capital": 200000.0,
  "interest_rate": 3.5,
  "years": 30,
  "payroll_bonus": 0.3,
  "insurance_bonus": 0.5,
  "card_bonus": 0.1,
  "other_bonus": 0.1,
  "insurance_cost_monthly": 45.0,
  "card_annual_fee": 50.0,
  "other_costs_monthly": 10.0
}
```

### Salida (MortgageResults)

```json
{
  "monthly_payment_without_bonus": 898.09,
  "total_interest_without_bonus": 123312.18,
  "total_paid_without_bonus": 323312.18,
  "monthly_payment_with_bonus": 790.24,
  "total_interest_with_bonus": 84487.05,
  "total_paid_with_bonus": 284487.05,
  "total_bonus_costs": 21300.0,
  "real_savings": 17525.13,
  "savings_percentage": 5.42,
  "is_worth_it": true,
  "effective_rate_without_bonus": 3.5,
  "effective_rate_with_bonus": 2.87
}
```

## 🎨 Estilo de Código

### Convenciones

- **PEP 8**: Estilo estándar de Python
- **Type hints**: En todas las funciones públicas
- **Docstrings**: Formato Google style
- **Nombres**: 
  - Clases: `PascalCase`
  - Funciones/variables: `snake_case`
  - Constantes: `UPPER_SNAKE_CASE`

### Ejemplo de Función Documentada

```python
def calculate_monthly_payment(self, annual_rate: float) -> float:
    """
    Calcula la cuota mensual usando amortización francesa.
    
    Args:
        annual_rate: Tasa de interés anual en porcentaje (e.g., 3.5)
        
    Returns:
        Cuota mensual en euros
        
    Example:
        >>> calculator.calculate_monthly_payment(3.5)
        898.09
    """
    monthly_rate = annual_rate / 100 / 12
    n_payments = self.data.years * 12
    
    if monthly_rate == 0:
        return self.data.capital / n_payments
    
    payment = self.data.capital * (
        monthly_rate * math.pow(1 + monthly_rate, n_payments)
    ) / (math.pow(1 + monthly_rate, n_payments) - 1)
    
    return payment
```

## 🚀 Performance

### Complejidad Temporal

- `calculate_monthly_payment()`: **O(1)** - Cálculo directo
- `calculate_amortization_schedule()`: **O(n)** donde n = años × 12
- `generate_report()`: **O(n)** donde n = años × 12

### Optimizaciones

1. **Cálculos únicos**: Los resultados se calculan una sola vez
2. **Lazy evaluation**: Excel se genera solo cuando se solicita
3. **Pandas eficiente**: Uso de DataFrames para operaciones en bloque

### Benchmarks (hipoteca de 30 años)

```
calculate_monthly_payment():        < 0.001s
calculate_amortization_schedule():  < 0.01s
generate_report():                  < 0.5s
```

## 🔐 Validaciones

### Validaciones Automáticas

El código valida:
- Capital > 0
- Tipo de interés ≥ 0
- Años > 0
- Bonificaciones ≥ 0
- Costes ≥ 0

### Casos Especiales

1. **Tipo de interés 0%**: Usa amortización lineal simple
2. **Sin bonificaciones**: Ambos escenarios son idénticos
3. **Bonificaciones > tipo**: El tipo final se limita a 0%

## 📝 Logs y Debugging

### Modo Debug

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Los cálculos mostrarán información detallada
calculator = MortgageCalculator(data)
results = calculator.calculate()
```

### Verificación Manual

```python
# Verificar tabla de amortización
schedule = calculator.calculate_amortization_schedule(3.5)

# Sumar todos los pagos
total_payments = sum(payment[1] for payment in schedule)

# Debe ser = capital + intereses
assert abs(total_payments - results.total_paid_without_bonus) < 0.01
```

## 🔄 Integración con Otros Sistemas

### Como API

Ejemplo de cómo convertir en API REST con Flask:

```python
from flask import Flask, request, jsonify
from mortgage_calculator.models import MortgageData
from mortgage_calculator.calculator import MortgageCalculator

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data_dict = request.json
    mortgage_data = MortgageData(**data_dict)
    calculator = MortgageCalculator(mortgage_data)
    results = calculator.calculate()
    
    return jsonify({
        "is_worth_it": results.is_worth_it,
        "real_savings": results.real_savings,
        "monthly_payment_with_bonus": results.monthly_payment_with_bonus
    })
```

### Como CLI

```python
# cli.py
import click
from mortgage_calculator.models import MortgageData
from mortgage_calculator.excel_generator import ExcelGenerator

@click.command()
@click.option('--capital', type=float, required=True)
@click.option('--rate', type=float, required=True)
@click.option('--years', type=int, required=True)
def cli(capital, rate, years):
    """Calculadora de hipotecas por línea de comandos."""
    data = MortgageData(capital=capital, interest_rate=rate, years=years)
    generator = ExcelGenerator(data)
    file = generator.generate_report()
    click.echo(f"Reporte generado: {file}")

if __name__ == '__main__':
    cli()
```

## 🌍 Internacionalización

Para soportar otros idiomas:

```python
# locale/en.py
STRINGS = {
    "mortgage_title": "Mortgage Bonus Analysis",
    "is_worth_it": "Is it worth it?",
    # ...
}

# locale/es.py
STRINGS = {
    "mortgage_title": "Análisis de Bonificaciones de Hipoteca",
    "is_worth_it": "¿Vale la pena?",
    # ...
}
```

## 📚 Referencias

- [Amortización francesa - Wikipedia](https://es.wikipedia.org/wiki/Sistema_de_amortizaci%C3%B3n_franc%C3%A9s)
- [Cálculo de hipotecas - Banco de España](https://www.bde.es/)
- [OpenPyXL Documentation](https://openpyxl.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Autor**: Leandro González  
**Versión**: 0.1.0  
**Licencia**: MIT
