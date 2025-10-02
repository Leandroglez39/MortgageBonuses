# 🚀 Comandos Rápidos - MortgageBonuses

## 📦 Gestión de Dependencias

```bash
# Ver todas las dependencias instaladas
poetry show

# Ver solo dependencias principales
poetry show --tree

# Ver dependencias desactualizadas
poetry show --outdated

# Actualizar todas las dependencias
poetry update

# Actualizar una dependencia específica
poetry update openpyxl

# Instalar dependencias
poetry install

# Instalar solo dependencias de producción
poetry install --only main

# Añadir nueva dependencia
poetry add nombre-paquete

# Añadir dependencia de desarrollo
poetry add --group dev nombre-paquete
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
poetry run pytest

# Tests con verbosidad
poetry run pytest -v

# Tests con cobertura
poetry run pytest --cov

# Test específico
poetry run pytest tests/test_calculator.py

# Test de una función específica
poetry run pytest tests/test_calculator.py::test_bonus_worth_it_positive

# Tests en modo watch (requiere pytest-watch)
poetry run ptw
```

## 🎨 Formateo y Linting

```bash
# Formatear todo el código
poetry run black .

# Ver qué cambiaría sin modificar
poetry run black --check .

# Formatear un archivo específico
poetry run black main.py

# Ejecutar linter
poetry run ruff check .

# Linter con auto-fix
poetry run ruff check . --fix

# Linter de un archivo específico
poetry run ruff check main.py
```

## ▶️ Ejecutar el Proyecto

```bash
# Script principal
poetry run python main.py

# Modo interactivo
poetry run python interactive.py

# Ejemplos
poetry run python examples.py

# Utilidades avanzadas
poetry run python utils.py

# Usando scripts definidos (después de instalar)
poetry run mortgage-calculator
poetry run mortgage-interactive
```

## 🐍 Gestión del Entorno

```bash
# Activar el entorno virtual
poetry shell

# Ver información del entorno
poetry env info

# Listar entornos virtuales
poetry env list

# Eliminar el entorno virtual
poetry env remove python

# Usar Python específico
poetry env use python3.12

# Salir del entorno virtual
exit
```

## 📊 Cobertura de Tests

```bash
# Generar reporte de cobertura
poetry run pytest --cov --cov-report=html

# Ver reporte en navegador (Linux)
xdg-open htmlcov/index.html

# Ver reporte en navegador (macOS)
open htmlcov/index.html

# Reporte en terminal
poetry run pytest --cov --cov-report=term

# Reporte detallado con líneas faltantes
poetry run pytest --cov --cov-report=term-missing
```

## 🔍 Información del Proyecto

```bash
# Ver versión de Poetry
poetry --version

# Ver versión de Python
poetry run python --version

# Ver información del proyecto
poetry show --tree

# Ver metadata del proyecto
cat pyproject.toml

# Ver dependencias directas
poetry show --only main

# Ver dependencias de desarrollo
poetry show --only dev
```

## 🔧 Mantenimiento

```bash
# Regenerar poetry.lock
poetry lock

# Verificar pyproject.toml
poetry check

# Limpiar caché de Poetry
poetry cache clear pypi --all

# Construir paquete
poetry build

# Publicar en PyPI (si aplica)
poetry publish
```

## 📝 Workflow de Desarrollo

```bash
# 1. Crear una nueva rama
git checkout -b feature/nueva-funcionalidad

# 2. Activar entorno
poetry shell

# 3. Hacer cambios en el código

# 4. Formatear código
poetry run black .

# 5. Ejecutar linter
poetry run ruff check . --fix

# 6. Ejecutar tests
poetry run pytest -v

# 7. Verificar cobertura
poetry run pytest --cov

# 8. Commit y push
git add .
git commit -m "feat: descripción de la funcionalidad"
git push origin feature/nueva-funcionalidad
```

## 🐛 Debugging

```bash
# Ejecutar con debugger de Python
poetry run python -m pdb main.py

# Ejecutar test con debugger
poetry run pytest --pdb

# Ejecutar test que falla con debugger
poetry run pytest --pdb -x

# Ver traceback completo
poetry run pytest -vvv

# Ejecutar test con prints
poetry run pytest -s
```

## 📦 Exportar Dependencias

```bash
# Exportar a requirements.txt
poetry export -f requirements.txt -o requirements.txt

# Exportar sin hashes
poetry export -f requirements.txt -o requirements.txt --without-hashes

# Exportar solo producción
poetry export -f requirements.txt -o requirements.txt --only main

# Exportar solo desarrollo
poetry export -f requirements.txt -o requirements.txt --only dev
```

## 🔐 Seguridad

```bash
# Auditar dependencias (requiere pip-audit)
poetry export -f requirements.txt | pip-audit -r /dev/stdin

# Verificar con safety (requiere safety)
poetry export -f requirements.txt | safety check --stdin

# Actualizar dependencias con vulnerabilidades
poetry update
```

## 📚 Documentación

```bash
# Generar documentación (si usas sphinx)
cd docs && poetry run make html

# Ver documentación
xdg-open docs/_build/html/index.html
```

## 🎯 Atajos Útiles

```bash
# Alias útiles (añadir a ~/.bashrc o ~/.zshrc)
alias prun="poetry run python"
alias ptest="poetry run pytest -v"
alias pformat="poetry run black . && poetry run ruff check . --fix"
alias pcheck="poetry run black --check . && poetry run ruff check ."
alias pcov="poetry run pytest --cov --cov-report=html && xdg-open htmlcov/index.html"
```

## 🌐 Variables de Entorno

```bash
# Configurar variable de entorno para Poetry
export POETRY_VIRTUALENVS_IN_PROJECT=true

# Usar .env para variables de entorno (requiere python-dotenv)
poetry add python-dotenv
```

## 🔄 Actualización del Proyecto

```bash
# Workflow completo de actualización
poetry show --outdated          # Ver qué está desactualizado
poetry update                   # Actualizar todo
poetry run black .              # Formatear código
poetry run ruff check . --fix   # Linter
poetry run pytest -v            # Tests
poetry run pytest --cov         # Cobertura
```

## 💡 Tips

1. **Usa poetry shell**: Trabaja dentro del entorno virtual
2. **Commits frecuentes**: Haz commits pequeños y descriptivos
3. **Tests primero**: Escribe tests antes de la funcionalidad (TDD)
4. **Formateo automático**: Usa pre-commit hooks
5. **Documentación**: Documenta mientras codeas

## 🎓 Recursos

- [Poetry Docs](https://python-poetry.org/docs/)
- [pytest Docs](https://docs.pytest.org/)
- [Black Docs](https://black.readthedocs.io/)
- [Ruff Docs](https://docs.astral.sh/ruff/)

---

**Tip Pro**: Crea un `Makefile` para automatizar comandos comunes:

```makefile
.PHONY: test format lint run

test:
	poetry run pytest -v

format:
	poetry run black .

lint:
	poetry run ruff check . --fix

run:
	poetry run python main.py

all: format lint test
```

Luego simplemente usa: `make test`, `make format`, etc.
