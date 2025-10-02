# 📊 Excel Dinámico con Fórmulas

## ✨ Nueva Funcionalidad

El Excel generado ahora es **completamente dinámico**. Ya no necesitas regenerar el archivo cada vez que quieras probar diferentes valores.

## 🎯 Cómo Usar

### 1️⃣ **Hoja "Datos de Entrada"**
Esta es la única hoja que necesitas modificar. Simplemente cambia los valores en la columna **"Valor"**:

```
┌─────────────────────────────────────────┬──────────┐
│ Concepto                                │ Valor    │
├─────────────────────────────────────────┼──────────┤
│ Capital prestado (€)                    │ 180000   │
│ Tasa de interés anual (%)               │ 2.90%    │
│ Plazo (años)                            │ 30       │
│                                         │          │
│ Bonificación por nómina (%)             │ 0.30%    │
│ Bonificación por seguro de vida (%)     │ 0.35%    │
│ Bonificación por seguro de hogar (%)    │ 0.25%    │
│ Bonificación por tarjeta (%)            │ 0.10%    │
│ Otras bonificaciones (%)                │ 0.00%    │
│                                         │          │
│ Coste mensual seguro de vida (€)        │ 30       │
│ Coste mensual seguro de hogar (€)       │ 25       │
│ Cuota anual de la tarjeta (€)           │ 50       │
│ Otros costes mensuales (€)              │ 12       │
└─────────────────────────────────────────┴──────────┘
```

### 2️⃣ **Todas las demás hojas se actualizan automáticamente**

Una vez que cambies un valor en "Datos de Entrada", **todas las hojas se recalculan automáticamente**:

- ✅ **Resumen**: Cuotas, intereses, decisión final
- ✅ **Análisis Bonificaciones**: Costes y ahorros de cada bonificación
- ✅ **Análisis Individual Seguros**: Rentabilidad de cada seguro
- ✅ **Comparación**: Escenarios con y sin bonificaciones
- ✅ **Amortización**: Tablas completas actualizadas

## 🔍 Ejemplos de Uso

### Escenario 1: ¿Y si el interés baja?
Cambia **B3** (Tasa de interés) de `2.90%` a `2.50%` → Todas las hojas se recalculan instantáneamente.

### Escenario 2: ¿Y si el seguro de vida es más caro?
Cambia **B14** (Coste seguro de vida) de `30` a `50` → La hoja "Análisis Individual Seguros" te dirá si sigue valiendo la pena.

### Escenario 3: Negociar con el banco
Prueba diferentes combinaciones de bonificaciones cambiando **B7-B11** para ver cuál es la mejor oferta.

## 🧮 Fórmulas Implementadas

La hoja **"Resumen"** contiene todas las fórmulas principales:

- **Cuota mensual**: Usa la fórmula francesa de amortización
  ```excel
  =IF(B4=0, 'Datos de Entrada'!B2/B2, 'Datos de Entrada'!B2*(B4/12)*(1+B4/12)^B2/((1+B4/12)^B2-1))
  ```

- **Ahorro real**: Intereses ahorrados menos costes de bonificaciones
  ```excel
  =B13-B12
  ```

- **¿Vale la pena?**: Decisión automática
  ```excel
  =IF(B14>0,"SÍ ✓","NO ✗")
  ```

## 💡 Ventajas

1. **Sin programar**: No necesitas Python para hacer cambios
2. **Instantáneo**: Los cálculos son en tiempo real
3. **Portable**: Puedes enviar el Excel a cualquier persona
4. **Exploración**: Prueba diferentes escenarios fácilmente
5. **Transparente**: Puedes ver todas las fórmulas usadas

## ⚠️ Importante

- **No modifiques** las otras hojas manualmente, ya que tienen fórmulas
- Si quieres volver a los valores originales, regenera el Excel con: `poetry run python main.py`
- Las celdas con formato de porcentaje (%) están en formato decimal (0.0290 = 2.90%)

## 🎨 Formato Visual

El Excel mantiene todo el formato visual:
- 🔵 Encabezados azules
- 🟢 Decisiones positivas resaltadas en verde
- 🟠 Decisiones negativas resaltadas en naranja
- 📊 Números formateados con separadores de miles
- 📈 Porcentajes mostrados correctamente

## 🚀 Próximos Pasos

Abre el Excel, ve a "Datos de Entrada", y empieza a experimentar con diferentes valores. ¡Observa cómo todo se actualiza automáticamente!
