# Calculadora de Bonificaciones de Hipotecas

Este proyecto en Python te permite analizar si las bonificaciones de una hipoteca realmente valen la pena, generando un completo análisis en Excel.

## 🎯 Características

- **Cálculo de cuotas mensuales** con y sin bonificaciones
- **Tablas de amortización completas** para ambos escenarios
- **Análisis de costes** de las bonificaciones (seguros, tarjetas, etc.)
- **Comparación detallada** y recomendación clara
- **Reporte Excel profesional** con múltiples hojas y formato visual

## 📋 Requisitos

- Python 3.11 o superior
- Poetry (gestor de dependencias)

## 🚀 Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias con Poetry:
```bash
poetry install
```

## 💻 Uso

### Opción 1: Editar el archivo main.py

Edita el archivo `main.py` y modifica los valores de tu hipoteca:

```python
mortgage_data = MortgageData(
    # Datos principales
    capital=200000.0,        # Capital prestado en €
    interest_rate=3.50,      # Tipo de interés anual en %
    years=30,                # Plazo en años
    
    # Bonificaciones (reducción del tipo de interés)
    payroll_bonus=0.30,      # Bonificación por domiciliar nómina (%)
    insurance_bonus=0.50,    # Bonificación por contratar seguros (%)
    card_bonus=0.10,         # Bonificación por usar tarjeta (%)
    other_bonus=0.10,        # Otras bonificaciones (%)
    
    # Costes asociados a las bonificaciones
    insurance_cost_monthly=45.0,   # Coste mensual del seguro (€)
    card_annual_fee=50.0,          # Cuota anual de la tarjeta (€)
    other_costs_monthly=10.0,      # Otros costes mensuales (€)
)
```

Luego ejecuta:
```bash
poetry run python main.py
```

### Opción 2: Usar como biblioteca

También puedes usar el módulo en tus propios scripts:

```python
from mortgage_calculator.models import MortgageData
from mortgage_calculator.excel_generator import ExcelGenerator

# Crea los datos
data = MortgageData(
    capital=250000.0,
    interest_rate=3.25,
    years=25,
    payroll_bonus=0.25,
    insurance_bonus=0.40,
    insurance_cost_monthly=50.0
)

# Genera el reporte
generator = ExcelGenerator(data)
output_path = generator.generate_report("mi_analisis.xlsx")
print(f"Reporte generado: {output_path}")
```

## 📊 Contenido del Excel generado

El reporte incluye las siguientes hojas:

1. **Datos de Entrada**: Todos los parámetros de la hipoteca
2. **Resumen**: Análisis ejecutivo con la conclusión principal
3. **Comparación**: Comparativa lado a lado de ambos escenarios
4. **Amortización SIN Bonif.**: Tabla completa mes a mes sin bonificaciones
5. **Amortización CON Bonif.**: Tabla completa mes a mes con bonificaciones
6. **Análisis Bonificaciones**: Desglose detallado de cada bonificación

## 🧮 ¿Cómo funciona?

El programa calcula:

1. **Sin bonificaciones**: Cuota mensual y total a pagar con el tipo base
2. **Con bonificaciones**: Cuota mensual y total a pagar con el tipo reducido
3. **Costes reales**: Suma de todos los costes de las bonificaciones durante la vida del préstamo
4. **Ahorro real**: Diferencia entre ambos escenarios menos los costes de las bonificaciones

La conclusión es simple: **las bonificaciones valen la pena si el ahorro real es positivo**.

## 📁 Estructura del proyecto

```
MortgageBonuses/
├── mortgage_calculator/
│   ├── __init__.py
│   ├── models.py              # Modelos de datos
│   ├── calculator.py          # Motor de cálculos
│   └── excel_generator.py     # Generación de reportes
├── main.py                    # Script principal
├── examples.py                # Ejemplos de uso
├── pyproject.toml             # Configuración de Poetry
└── README.md
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

## 💡 Ejemplo de uso

```bash
# Instalar dependencias
poetry install

# Ejecutar el análisis
poetry run python main.py

# Se generará el archivo: analisis_hipoteca.xlsx
```

El programa mostrará un resumen en consola y generará un archivo Excel completo para tu análisis detallado.

---

**¿Tienes dudas?** Revisa los comentarios en el código o abre un issue.
