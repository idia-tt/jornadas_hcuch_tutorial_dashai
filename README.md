# Tutorial de DashAI — VIII Jornadas de Investigación HCUCH

<p align="center">
  <a href="https://idia.uchile.cl/"><img src="assets/logo-idia.svg" alt="IDIA — Iniciativa de Datos e Inteligencia Artificial" width="240" height="100"></a><a href="https://dcc.uchile.cl/"><img src="assets/logo-dcc.svg" alt="DCC — Departamento de Ciencias de la Computación, Universidad de Chile" width="240" height="100"></a><a href="https://www.dash-ai.com/"><img src="assets/logo-dashai.svg" alt="DashAI" width="240" height="100"></a>
</p>

Este tutorial fue preparado para las
[VIII Jornadas de Investigación](https://redhcuch.redclinica.cl/actividad-academica/viii_jornadas_de_investigacion.aspx)
del Hospital Clínico de la Universidad de Chile, realizadas junto con la Facultad
de Ciencias Físicas y Matemáticas.

Con [DashAI](https://www.dash-ai.com/) puedes entrenar y comparar modelos de
aprendizaje automático desde una interfaz gráfica. En este taller harás dos
ejercicios: clasificar casos a partir de una tabla de datos y conversar con un
modelo de lenguaje para generar texto. No necesitas haber usado DashAI antes.

Material preparado por [Pablo Badilla](https://github.com/pbadillatorrealba),
de la [Iniciativa de Datos e Inteligencia Artificial (IDIA)](https://idia.uchile.cl/),
[Facultad de Ciencias Físicas y Matemáticas (FCFM)](https://ingenieria.uchile.cl/),
[Universidad de Chile](https://uchile.cl/).

## Empezar con Google Colab

Si es tu primera vez, usa esta opción. Solo necesitas una cuenta de Google y un
navegador. DashAI se ejecutará en un computador de Google: no tienes que instalar
programas en el tuyo.

1. **Descarga la [guía de ejercicios](https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai/raw/refs/heads/main/DashAI_Guia.html)**
   y abre el archivo `DashAI_Guia.html` en tu navegador. Esta guía explica qué hacer
   dentro de DashAI.
2. **[Abre el cuaderno en Google Colab](https://colab.research.google.com/github/idia-tt/jornadas_hcuch_tutorial_dashai/blob/main/DashAI_Colab.ipynb).**
   Un cuaderno combina instrucciones con bloques de código llamados *celdas*.
   Lee la introducción y sigue la sección **2. Preparación**, ejecutando las celdas
   en orden con el botón **▶**. Espera a que termine cada una antes de continuar.
3. **Cuando veas DashAI dentro del cuaderno, sigue la guía de ejercicios.**
   Mantén ambos documentos abiertos, uno al lado del otro. El cuaderno también
   incluye el paso para descargar los datos del primer ejercicio y las
   instrucciones para apagar DashAI al terminar.

La preparación puede demorar entre 10 y 20 minutos la primera vez. Calcula unos
20 minutos más por ejercicio. Si una celda falla, consulta la sección **5. Si algo
no funciona** del cuaderno.

## Ejecutarlo en tu computador

También puedes instalar DashAI en Windows, macOS o Linux. Necesitas una terminal,
conexión a internet y espacio para las dependencias y los modelos. Tu trabajo
quedará guardado en tu computador.

La [guía de instalación local](docs/dashai-local.md) explica los requisitos,
cómo instalar Git y uv, y qué hacer si algo falla. **Si todavía no tienes esas
herramientas, empieza por esa guía.** Git permite descargar este repositorio y
uv prepara el entorno de Python con los programas que necesita el tutorial.

Elige tu sistema y sigue sus pasos. Copia los comandos de cada bloque en orden.
Solo necesitas descargar el material e instalar las dependencias la primera vez.

### Windows

Con Git y uv instalados, abre **PowerShell**.

**1. Descarga el material y entra en su carpeta:**

```powershell
git clone https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai.git
cd jornadas_hcuch_tutorial_dashai
```

En esa misma ventana, configura UTF-8 para evitar errores con los caracteres
del registro de DashAI:

```powershell
$env:PYTHONUTF8 = "1"
```

**2. Instala lo necesario para los dos ejercicios y genera el archivo de datos:**

```powershell
uv sync --locked --extra llm
uv run --extra llm python scripts/generar_datos.py
```

**3. Inicia DashAI:**

```powershell
uv run --extra llm python -m DashAI --no-browser --local-path .dashai
```

### macOS

Con Git y uv instalados, abre **Terminal**.

**1. Descarga el material y entra en su carpeta:**

```sh
git clone https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai.git
cd jornadas_hcuch_tutorial_dashai
```

**2. Instala lo necesario para los dos ejercicios y genera el archivo de datos:**

```sh
uv sync --locked --extra llm
uv run --extra llm python scripts/generar_datos.py
```

**3. Inicia DashAI:**

```sh
uv run --extra llm python -m DashAI --no-browser --local-path .dashai
```

### Linux

Con Git y uv instalados, abre **Terminal**.

**1. Descarga el material y entra en su carpeta:**

```sh
git clone https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai.git
cd jornadas_hcuch_tutorial_dashai
```

**2. Instala lo necesario para los dos ejercicios y genera el archivo de datos:**

```sh
uv sync --locked --extra llm
uv run --extra llm python scripts/generar_datos.py
```

**3. Inicia DashAI:**

```sh
uv run --extra llm python -m DashAI --no-browser --local-path .dashai
```

### Abrir DashAI y seguir los ejercicios

La instalación puede tardar varios minutos. El comando de generación de datos
crea `breast_cancer.csv` en la carpeta del tutorial: ese es el archivo que subirás
a DashAI en el primer ejercicio. Si ya existe, puedes usarlo; el comando no lo
sobrescribe. El extra `llm` instala el soporte para el modelo de lenguaje del
segundo ejercicio.

Deja abierta la terminal y espera a que termine de iniciar. Después abre
<http://127.0.0.1:8000/app/> en tu navegador y sigue la
[guía de ejercicios](https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai/raw/refs/heads/main/DashAI_Guia.html).
Puedes saltarte sus instrucciones de preparación y descarga de datos en Colab:
ya tienes DashAI funcionando y el CSV en tu computador.

Para apagarlo, vuelve a la terminal y pulsa **Ctrl+C**. Tus sesiones y datos
quedan en la carpeta `.dashai`; consérvala si quieres continuar otro día. Para
volver a usar DashAI, abre una terminal en la carpeta del tutorial y repite el
comando del paso 3 de tu sistema; en Windows, repite también el ajuste de UTF-8.

Esta instalación funciona con el procesador del computador (CPU). El segundo
ejercicio puede responder más lento sin GPU. La guía local incluye una
[sección de GPU NVIDIA y Apple Silicon](docs/dashai-local.md#4-gpu-entorno-independiente)
y una alternativa para instalar solo lo necesario para clasificación.

## Sobre los datos

El primer ejercicio usa el conjunto público *Breast Cancer Wisconsin*, incluido
en scikit-learn. Para practicar, usa esos datos y evita subir información que
identifique a pacientes. Los archivos generados, los modelos descargados y las
sesiones locales quedan fuera de Git.

## Generar las guías HTML

El contenido de la guía de ejercicios se edita en [DashAI_Guia.md](DashAI_Guia.md).
Las instrucciones locales se editan en [docs/dashai-local.md](docs/dashai-local.md).
Después de cambiar cualquiera de ellas, genera los dos HTML:

```sh
uv run --extra llm python scripts/generar_html.py
```

El comando crea `DashAI_Guia.html` y `DashAI_Local.html` en la raíz del repositorio.
Puedes abrirlos con doble clic en tu navegador. Los logos y estilos van incluidos
en cada HTML; los diagramas de la guía necesitan internet para cargar Mermaid.
No edites los HTML a mano: guarda los cambios en el Markdown y vuelve a generarlos.
La presentación común se ajusta en `docs/plantilla.html`.

También puedes [descargar las instrucciones locales en HTML](https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai/raw/refs/heads/main/DashAI_Local.html).
Para comprobar que ambos HTML están actualizados, usa
`uv run --extra llm python scripts/generar_html.py --check`.

## Si vas a modificar el material

No necesitas estos pasos para hacer los ejercicios. Si vas a cambiar código,
instala las comprobaciones que se ejecutan antes de cada commit:

```sh
uv sync --locked --extra llm
uv run --extra llm pre-commit install
uv run --extra llm pre-commit run --all-files
```

[pre-commit](https://pre-commit.com/) revisa los archivos y ejecuta
[Ruff](https://docs.astral.sh/ruff/), que comprueba y da formato al código Python,
incluidas las celdas del cuaderno. Algunas comprobaciones corrigen archivos;
revisa esos cambios y vuelve a agregarlos al commit. Los hooks se instalan una
vez en cada copia del repositorio.

Las versiones de las dependencias están en `uv.lock`. Para actualizarlas, ejecuta
`uv lock --upgrade`, prueba los ejemplos y guarda el archivo actualizado.
Mantén iguales las versiones de Ruff en `pyproject.toml` y en
`.pre-commit-config.yaml`. GitHub Actions comprueba la instalación con CPU,
el arranque de DashAI, la generación del CSV y los hooks en Windows, Linux y
macOS con Apple Silicon. La aceleración GPU requiere pruebas en hardware real.

## Enlaces

- **DashAI:** [sitio web](https://www.dash-ai.com/),
  [documentación](https://docs.dash-ai.com/) y
  [código fuente](https://github.com/DashAISoftware/DashAI).
- **Universidad de Chile:** [IDIA](https://idia.uchile.cl/),
  [Departamento de Ciencias de la Computación (DCC)](https://dcc.uchile.cl/),
  [FCFM](https://ingenieria.uchile.cl/) y [Universidad de Chile](https://uchile.cl/).
- **Herramientas:** [Git](https://git-scm.com/downloads) y
  [uv](https://docs.astral.sh/uv/).
