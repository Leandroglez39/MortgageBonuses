# Guía de Uso - Calculadora de Bonificaciones de Hipoteca

## 📖 Contenido

1. [Inicio Rápido](#inicio-rápido)
2. [Formas de Uso](#formas-de-uso)
3. [Interpretación de Resultados](#interpretación-de-resultados)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Inicio Rápido

### 1. Instalación

```bash
# Asegúrate de tener Poetry instalado
poetry --version

# Instala las dependencias
poetry install
```

### 2. Uso más simple (modo interactivo)

```bash
poetry run python interactive.py
```

Este modo te preguntará todos los datos paso a paso.

---

## Formas de Uso

### Opción 1: Modo Interactivo (Recomendado para principiantes)

```bash
poetry run python interactive.py
```

El programa te pedirá:
- Capital prestado
- Tipo de interés
- Plazo en años
- Cada bonificación y su coste asociado
- Nombre del archivo de salida

**Ventajas:**
- No necesitas editar código
- Guía paso a paso
- Valores por defecto sugeridos

### Opción 2: Editar main.py

1. Abre `main.py`
2. Modifica la sección `MortgageData`:

```python
mortgage_data = MortgageData(
    capital=250000.0,        # Tu capital
    interest_rate=3.25,      # Tu tipo de interés
    years=25,                # Tu plazo
    # ... resto de datos
)
```

3. Ejecuta:
```bash
poetry run python main.py
```

**Ventajas:**
- Control total sobre los datos
- Ideal para análisis repetidos
- Puedes guardar diferentes configuraciones

### Opción 3: Como librería Python

Crea tu propio script:

```python
from mortgage_calculator.models import MortgageData
from mortgage_calculator.excel_generator import ExcelGenerator

# Define tus datos
datos = MortgageData(
    capital=180000.0,
    interest_rate=3.75,
    years=30,
    payroll_bonus=0.35,
    insurance_bonus=0.45,
    insurance_cost_monthly=50.0
)

# Genera el reporte
generador = ExcelGenerator(datos)
archivo = generador.generate_report("mi_hipoteca.xlsx")
print(f"Archivo creado: {archivo}")

# Accede a los resultados
resultados = generador.results
print(f"Ahorro real: {resultados.real_savings:.2f} €")
print(f"¿Vale la pena? {'SÍ' if resultados.is_worth_it else 'NO'}")
```

**Ventajas:**
- Máxima flexibilidad
- Puedes integrar en tus propias aplicaciones
- Automatización de análisis múltiples

### Opción 4: Análisis múltiples con examples.py

```bash
poetry run python examples.py
```

Ejecuta varios escenarios predefinidos para ver diferentes casos de uso.

---

## Interpretación de Resultados

### En Consola

El programa muestra un resumen:

```
¿Valen la pena las bonificaciones? SÍ ✓
Ahorro real: 17,525.13 €
Porcentaje de ahorro: 5.42%
```

- **SÍ ✓**: Las bonificaciones son rentables
- **NO ✗**: Las bonificaciones NO son rentables
- **Ahorro real**: Diferencia entre pagar con/sin bonificaciones, descontando los costes
- **Porcentaje de ahorro**: % sobre el total sin bonificaciones

### En Excel

El archivo Excel contiene 6 hojas:

#### 1. Datos de Entrada
Resumen de todos los parámetros introducidos.

#### 2. Resumen
La hoja más importante:
- **Decisión principal**: ¿Vale la pena?
- **Ahorro real**: En euros y porcentaje
- **Comparación de cuotas**: Mensual
- **Comparación de totales**: Durante toda la vida del préstamo

**Colores:**
- 🟢 Verde: Las bonificaciones valen la pena
- 🟠 Naranja: Las bonificaciones NO valen la pena

#### 3. Comparación
Tabla lado a lado de ambos escenarios.

#### 4 y 5. Amortización
Tablas mes a mes mostrando:
- Cuota
- Intereses pagados
- Capital amortizado
- Pendiente de pagar

**Una tabla para cada escenario** (con y sin bonificaciones).

#### 6. Análisis Bonificaciones
Desglose detallado:
- Cada bonificación por separado
- Coste mensual y total de cada una
- Ahorro total en intereses

---

## Ejemplos Prácticos

### Ejemplo 1: Primera Vivienda con Bonificaciones Típicas

```python
MortgageData(
    capital=180000.0,        # 180.000€
    interest_rate=3.25,      # 3.25% TAE
    years=25,                # 25 años
    payroll_bonus=0.30,      # -0.30% por nómina
    insurance_bonus=0.50,    # -0.50% por seguro hogar + vida
    card_bonus=0.05,         # -0.05% por tarjeta
    insurance_cost_monthly=45.0,  # 45€/mes seguros
    card_annual_fee=0.0,     # Tarjeta sin coste
)
```

**Resultado típico:** Las bonificaciones suelen valer la pena.

### Ejemplo 2: Hipoteca Grande con Muchas Bonificaciones

```python
MortgageData(
    capital=350000.0,        # 350.000€
    interest_rate=3.75,      # 3.75% TAE
    years=30,                # 30 años
    payroll_bonus=0.40,      # -0.40% por nómina
    insurance_bonus=0.60,    # -0.60% por seguros
    card_bonus=0.15,         # -0.15% por tarjeta premium
    other_bonus=0.10,        # -0.10% por otros productos
    insurance_cost_monthly=60.0,   # 60€/mes seguros
    card_annual_fee=80.0,    # 80€/año tarjeta
    other_costs_monthly=20.0,      # 20€/mes otros
)
```

**Resultado típico:** A mayor capital, más ahorro absoluto.

### Ejemplo 3: Bonificaciones Caras (Caso Real)

```python
MortgageData(
    capital=200000.0,
    interest_rate=2.80,      # Tipo ya bajo
    years=20,
    payroll_bonus=0.15,      # Bonificación pequeña
    insurance_bonus=0.25,    # Bonificación pequeña
    insurance_cost_monthly=150.0,  # ⚠️ Seguro muy caro
    other_costs_monthly=50.0,      # ⚠️ Otros costes
)
```

**Resultado típico:** Las bonificaciones NO valen la pena.

---

## Preguntas Frecuentes

### ¿Qué es una bonificación en el tipo de interés?

Es una reducción en el porcentaje de interés que pagas. Por ejemplo:
- Tipo base: 3.50%
- Bonificación nómina: -0.30%
- Bonificación seguro: -0.50%
- **Tipo final: 2.70%**

### ¿Por qué a veces no valen la pena las bonificaciones?

Porque los costes asociados (seguros, tarjetas, etc.) pueden ser mayores que el ahorro en intereses.

**Ejemplo:**
- Ahorro en intereses: 20.000€
- Coste de seguros: 25.000€
- **Resultado: Pierdes 5.000€**

### ¿Cómo sé si mi seguro es caro?

Precios de referencia (aproximados):
- Seguro hogar: 150-300€/año
- Seguro vida: 200-400€/año según edad
- **Total típico: 30-60€/mes**

Si te cobran más de 80€/mes, probablemente sea caro.

### ¿Qué pasa si solo quiero algunas bonificaciones?

Pon a 0 las que no quieras:

```python
MortgageData(
    capital=200000.0,
    interest_rate=3.50,
    years=30,
    payroll_bonus=0.30,         # Esta sí
    insurance_bonus=0.0,        # Esta no
    card_bonus=0.0,             # Esta no
    insurance_cost_monthly=0.0,
)
```

### ¿Puedo comparar varias ofertas de bancos?

¡Sí! Ejecuta el programa varias veces con diferentes datos y compara los Excel generados.

### ¿El programa considera la inflación?

No, los cálculos son en términos nominales. La inflación afecta igual a ambos escenarios.

### ¿Considera el coste de oportunidad del dinero?

No directamente, pero puedes interpretarlo:
- Si el ahorro es > 0: Te conviene la bonificación
- Si el ahorro es < 0: Te conviene invertir ese dinero de otra forma

### ¿Los cálculos son exactos?

Sí, usa la fórmula estándar de amortización francesa (la más común en España y Europa).

**Nota:** Los bancos pueden tener pequeñas variaciones por redondeos, pero la diferencia es mínima (< 1€/mes).

### ¿Qué hago con el archivo Excel?

Puedes:
1. **Guardarlo** como referencia
2. **Compartirlo** con tu familia para tomar decisiones
3. **Mostrarlo al banco** para negociar
4. **Comparar** varios archivos de diferentes ofertas

### ¿Puedo modificar el Excel?

Sí, pero te recomendamos:
1. Hacer una copia del original
2. Modificar solo los datos de entrada
3. No tocar las fórmulas (si hay)

### ¿Funciona para hipotecas variables?

No directamente. Este programa asume tipo fijo. Para tipo variable, deberías:
1. Hacer varios análisis con diferentes tipos
2. Ver el escenario optimista y pesimista
3. Considerar que la bonificación se mantiene aunque cambie el tipo base

---

## Tests

Para verificar que todo funciona correctamente:

```bash
poetry run pytest -v
```

Deberías ver 13 tests pasando exitosamente.

---

## Soporte

Si tienes problemas:

1. Verifica que Poetry esté instalado: `poetry --version`
2. Verifica que las dependencias estén instaladas: `poetry install`
3. Revisa los ejemplos incluidos: `poetry run python examples.py`
4. Lee los mensajes de error cuidadosamente

---

## Próximos Pasos

Después de generar tu análisis:

1. ✅ Revisa el Excel completo
2. ✅ Compara con otras ofertas
3. ✅ Considera otros factores (vinculaciones, flexibilidad, etc.)
4. ✅ Consulta con un asesor financiero si es necesario
5. ✅ ¡Toma la mejor decisión para tu situación!

---

**¡Buena suerte con tu hipoteca! 🏠**
