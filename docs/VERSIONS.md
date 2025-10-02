# Versiones de Dependencias - MortgageBonuses

## 📅 Última Actualización: 2 de Octubre, 2025

## 🐍 Python
- **Versión**: 3.12.3
- **Rango soportado**: >=3.12, <3.14
- **Recomendado**: 3.12.x o 3.13.x

## 📦 Dependencias de Producción

### Core Dependencies (Actualizadas a Octubre 2025)

| Paquete | Versión Instalada | Última Compatible | Propósito |
|---------|-------------------|-------------------|-----------|
| **openpyxl** | 3.1.5 | 3.1.5 | Manipulación de archivos Excel (.xlsx) |
| **pandas** | 2.3.3 | 2.3.3 | Análisis y manipulación de datos |
| **numpy** | 2.3.3 | 2.3.3 | Operaciones numéricas de alto rendimiento |

### Dependencias Transitivas

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| et-xmlfile | 2.0.0 | Implementación de lxml.xmlfile para stdlib |
| python-dateutil | 2.9.0.post0 | Extensiones para módulo datetime |
| pytz | 2025.2 | Definiciones de zonas horarias |
| tzdata | 2025.2 | Datos IANA de zonas horarias |
| six | 1.17.0 | Utilidades de compatibilidad Python 2/3 |

## 🧪 Dependencias de Desarrollo

### Testing & Quality Tools

| Paquete | Versión Instalada | Última Compatible | Propósito |
|---------|-------------------|-------------------|-----------|
| **pytest** | 8.4.2 | 8.4.2 | Framework de testing |
| **pytest-cov** | 6.3.0 | 6.3.0 | Plugin de cobertura para pytest |
| **coverage** | 7.10.7 | 7.10.7 | Medición de cobertura de código |
| **black** | 25.9.0 | 25.9.0 | Formateador de código |
| **ruff** | 0.9.10 | 0.9.10 | Linter y formateador ultra-rápido |

### Dependencias Transitivas de Dev

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| click | 8.3.0 | Librería para CLI |
| mypy-extensions | 1.1.0 | Extensiones del sistema de tipos |
| pathspec | 0.12.1 | Coincidencia de patrones de rutas |
| platformdirs | 4.4.0 | Directorios específicos de plataforma |
| pytokens | 0.1.10 | Tokenizador de Python rápido |
| pygments | 2.19.2 | Resaltado de sintaxis |
| iniconfig | 2.1.0 | Parsing de archivos config-ini |
| packaging | 25.0 | Utilidades para paquetes Python |
| pluggy | 1.6.0 | Sistema de plugins |

## 🔄 Estado de Actualización

### ✅ Todas las dependencias están actualizadas (Octubre 2025)

- ✅ **openpyxl 3.1.5**: Última versión estable
- ✅ **pandas 2.3.3**: Última versión estable (compatible con Python 3.14)
- ✅ **numpy 2.3.3**: Última versión estable
- ✅ **pytest 8.4.2**: Última versión estable
- ✅ **black 25.9.0**: Última versión
- ✅ **ruff 0.9.10**: Última versión

### 📌 Versiones Bloqueadas

Las versiones están bloqueadas con `poetry.lock` para garantizar builds reproducibles.

## 🚀 Próximas Versiones Importantes

### pandas 3.0.0 (En desarrollo)
- **Estado**: Versión beta en desarrollo
- **Fecha estimada**: Finales de 2025 / Principios de 2026
- **Cambios importantes**: 
  - Mejoras de rendimiento
  - Nuevas APIs
  - Posibles breaking changes
- **Acción**: Monitorear compatibilidad cuando se lance

## 📊 Compatibilidad

### Python 3.12 Features Usadas

El proyecto aprovecha las siguientes características de Python 3.12+:

- ✅ **Type hints mejorados** (PEP 692, 698)
- ✅ **f-strings mejorados** para formateo
- ✅ **Mejor rendimiento** (10-60% más rápido que 3.11)
- ✅ **Mensajes de error mejorados**
- ✅ **Soporte completo para `dataclasses`**

### Compatibilidad con Python 3.13

El proyecto es **totalmente compatible** con Python 3.13:
- ✅ Todas las dependencias soportan Python 3.13
- ✅ Tests pasan en Python 3.13
- ✅ Sin warnings de deprecación

## 🔧 Comandos de Actualización

### Verificar actualizaciones disponibles
```bash
poetry show --outdated
```

### Actualizar todas las dependencias
```bash
poetry update
```

### Actualizar una dependencia específica
```bash
poetry update openpyxl
poetry update pandas
poetry update numpy
```

### Verificar versión de Python
```bash
poetry run python --version
```

### Reinstalar todas las dependencias
```bash
poetry install --sync
```

## 🛡️ Política de Versiones

### Dependencias de Producción
- **Actualizaciones menores**: Automáticas (^3.1.5 → 3.1.x)
- **Actualizaciones mayores**: Revisión manual requerida
- **Política**: Semantic Versioning (SemVer)

### Dependencias de Desarrollo
- **Actualizaciones**: Más flexibles
- **Testing**: Requerido antes de commit
- **Compatibilidad**: Menos crítica

## 📈 Historial de Versiones

### v0.1.0 (2 Octubre 2025)
- ✅ Python 3.12.3
- ✅ openpyxl 3.1.5
- ✅ pandas 2.3.3
- ✅ numpy 2.3.3
- ✅ pytest 8.4.2
- ✅ black 25.9.0
- ✅ ruff 0.9.10

## 🎯 Recomendaciones

### Para Desarrollo
```bash
# Usar el entorno virtual de Poetry
poetry shell

# Formatear código
poetry run black .

# Linter
poetry run ruff check .

# Tests con cobertura
poetry run pytest --cov
```

### Para Producción
```bash
# Instalar solo dependencias de producción
poetry install --only main

# Verificar instalación
poetry run python -c "import mortgage_calculator; print('OK')"
```

## 🔐 Seguridad

### Auditoría de Seguridad

Para verificar vulnerabilidades conocidas:

```bash
# Usando pip-audit (requiere instalación)
pip install pip-audit
poetry export -f requirements.txt | pip-audit -r /dev/stdin

# O usando safety
pip install safety
poetry export -f requirements.txt | safety check --stdin
```

### Estado de Seguridad
- ✅ Sin vulnerabilidades conocidas (Octubre 2025)
- ✅ Todas las dependencias son paquetes oficiales de PyPI
- ✅ Verificación de integridad mediante poetry.lock

## 📞 Soporte

Si tienes problemas con las versiones:

1. Verifica la versión de Python: `python --version` (debe ser ≥3.12)
2. Regenera el lock file: `poetry lock`
3. Reinstala: `poetry install`
4. Ejecuta tests: `poetry run pytest`

## 🔗 Enlaces Útiles

- [Poetry Documentation](https://python-poetry.org/docs/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [numpy Documentation](https://numpy.org/doc/)
- [pytest Documentation](https://docs.pytest.org/)
- [black Documentation](https://black.readthedocs.io/)
- [ruff Documentation](https://docs.astral.sh/ruff/)

---

**Última verificación**: 2 de Octubre, 2025  
**Próxima revisión recomendada**: Enero 2026
