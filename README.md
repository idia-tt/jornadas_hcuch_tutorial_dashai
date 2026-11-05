# Tutorial de DashAI — Jornadas HCUCH

Material en español de la Iniciativa de Datos e Inteligencia Artificial (IDIA),
Universidad de Chile. Practica clasificación con datos tabulares y generación de
texto con un modelo de lenguaje.

- [Abrir el cuaderno en Google Colab](https://colab.research.google.com/github/idia-tt/jornadas_hcuch_tutorial_dashai/blob/main/DashAI_Colab.ipynb).
- [Guía de ejercicios](DashAI_Guia.html): descarga el archivo y ábrelo en tu navegador.
- [Instalación local en Windows, macOS y Linux](docs/dashai-local.md).

## Inicio local

Instala [Git](https://git-scm.com/downloads) y [uv](https://docs.astral.sh/uv/getting-started/installation/).
En PowerShell (Windows) o Terminal (macOS/Linux):

```sh
git clone https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai.git
cd jornadas_hcuch_tutorial_dashai
uv sync --locked
uv run python scripts/generar_datos.py
uv run python -m DashAI --no-browser --local-path .dashai
```

Abre <http://127.0.0.1:8000/app/> y sigue la guía de ejercicios. El segundo ejemplo
necesita soporte LLM: consulta la guía local antes de comenzar.

## Contribuir

```sh
uv sync --locked
uv run pre-commit install
uv run pre-commit run --all-files
uv run ruff check .
uv run ruff format --check .
```

Los hooks se instalan una vez por clon y pueden modificar archivos; revísalos y
agrégalos de nuevo al commit. Ruff revisa Python y las celdas del notebook.
Usamos reglas de errores, imports, modernización, bugs y simplificación, además
del formateador de Ruff. Solo se aplican correcciones automáticas seguras.

Para actualizar dependencias, ejecuta `uv lock --upgrade`, verifica los ejemplos
y guarda el lockfile. Mantén la versión de Ruff del grupo `dev` y del hook iguales.
GitHub Actions verifica CPU en Linux, Windows y macOS Apple Silicon.

## Datos

El ejemplo usa Breast Cancer Wisconsin incluido en scikit-learn; no uses datos
identificables de pacientes para practicar. Los datasets generados, modelos y
sesiones locales se excluyen de Git.

Fuentes: [DashAI](https://github.com/DashAISoftware/DashAI),
[uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/) y
[pre-commit](https://pre-commit.com/).
