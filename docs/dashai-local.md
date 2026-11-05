# DashAI en tu computador

Esta alternativa reemplaza la preparación en Colab. Los ejercicios de
[la guía HTML](../DashAI_Guia.html) son los mismos: trabajas en el navegador,
pero los datos y sesiones quedan en tu computador.

## 1. Preparar el computador

Usa Windows 10/11 x64, Linux x64 o macOS con Apple Silicon. La instalación
en Mac Intel no está comprobada. Si ese es tu computador, puedes hacer los
ejercicios con [el cuaderno de Colab](https://colab.research.google.com/github/idia-tt/jornadas_hcuch_tutorial_dashai/blob/main/DashAI_Colab.ipynb).
Se recomienda disponer de 8 GB de RAM y al menos 10 GB de disco libre; los modelos
de lenguaje pueden necesitar bastante más. Internet es necesario para instalar
y descargar modelos. Python 3.12 lo instala uv automáticamente.

Instala [Git](https://git-scm.com/downloads) y luego uv:

**Windows — PowerShell**

Abre **Inicio**, busca **PowerShell** y ábrelo. Copia el comando del recuadro
y pulsa **Enter** para ejecutarlo.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux — Terminal**

En macOS, busca **Terminal** con Spotlight; en Linux, ábrelo desde el menú de
aplicaciones. Copia el comando del recuadro y pulsa **Enter** para ejecutarlo.

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Cierra y vuelve a abrir la terminal. Comprueba `git --version` y `uv --version`.
En Windows, ejecuta también `$env:PYTHONUTF8 = "1"` en la terminal donde
iniciarás DashAI. Evita errores Unicode del banner al redirigir los registros.

Los comandos siguientes funcionan en ambos tipos de terminal, sin activar un
entorno ni cambiar políticas de ejecución de PowerShell.

```sh
git clone https://github.com/idia-tt/jornadas_hcuch_tutorial_dashai.git
cd jornadas_hcuch_tutorial_dashai
uv sync --locked
```

Espera a que termine: DashAI tiene dependencias grandes. El entorno `.venv`
es exclusivo de este proyecto. La instalación principal usa CPU y permite
hacer el ejemplo de clasificación sin GPU.

## 2. Encender y generar los datos

Solo necesitas generar `breast_cancer.csv` una vez. Si ya existe, omite el primer
comando y continúa con el que inicia DashAI. Si lo ejecutaste y aparece
`FileExistsError`, puedes continuar usando el CSV que ya tienes.

```sh
uv run python scripts/generar_datos.py
uv run python -m DashAI --no-browser --local-path .dashai
```

El primer comando crea `breast_cancer.csv` en la carpeta del repo: 569 filas,
30 características y la columna `diagnosis`. No sobrescribe archivos existentes.
Súbelo desde la guía de ejercicios; no necesitas ejecutar su paso de Colab.

Cuando la terminal muestre `Uvicorn running on http://127.0.0.1:8000`,
DashAI está listo. Abre <http://127.0.0.1:8000/app/>.
Mantén abierta la terminal. Para detener DashAI pulsa **Ctrl+C** y espera que
termine. Para volver a iniciar, repite el segundo comando desde la misma carpeta.

Las sesiones y datasets permanecen en `.dashai`, incluso después de apagar.
No borres esa carpeta si quieres conservarlos; respáldala con DashAI detenido.
Eliminar `.venv` no elimina tu trabajo. Los modelos también pueden ocupar espacio
en la caché de Hugging Face del usuario.

## 3. Ejemplo B: modelos de lenguaje con CPU

Detén DashAI y ejecuta:

```sh
uv sync --locked --extra llm
uv run --extra llm python -c "import llama_cpp; print('Soporte LLM disponible')"
uv run --extra llm python -m DashAI --no-browser --local-path .dashai
```

Mantén `--extra llm` en los comandos `uv run` y `uv sync` de este entorno para
conservar ese soporte. La configuración usa el índice de wheels CPU del proyecto
llama-cpp; macOS fija 0.3.29 siguiendo la restricción de DashAI 0.10.0.

Sigue el ejemplo B de la guía. La primera descarga puede tardar varios minutos;
en CPU las respuestas serán más lentas. Empieza por el modelo pequeño de la guía.

## 4. GPU: entorno independiente

Esta sección es opcional y está dirigida a quienes ya configuran herramientas
de desarrollo. Si no tienes los requisitos o alguna comprobación falla,
continúa con [la instalación CPU de la sección 3](#3-ejemplo-b-modelos-de-lenguaje-con-cpu).

El entorno GPU mantiene intactos el entorno CPU y su lockfile. Instala la misma
versión de DashAI, pero sus dependencias se resuelven por separado y no quedan
fijadas por `uv.lock`. Ejecuta los comandos desde la carpeta del tutorial.
No ejecutes dos servidores sobre la misma carpeta de datos.

### Windows — NVIDIA

Antes de empezar, instala estos requisitos:

- Un [controlador NVIDIA](https://www.nvidia.com/en-us/drivers/) compatible con tu
  tarjeta y [CUDA Toolkit 12.8](https://developer.nvidia.com/cuda-12-8-0-download-archive).
- [CMake](https://cmake.org/download/), disponible en el PATH.
- [Visual Studio Build Tools para C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/),
  con las herramientas de desarrollo de escritorio con C++.

Abre **Developer PowerShell for Visual Studio** desde Inicio, entra en la carpeta
del tutorial y comprueba los requisitos:

```powershell
nvidia-smi
nvcc --version
cmake --version
cl
```

`nvidia-smi` debe reconocer tu tarjeta; `nvcc --version` debe indicar CUDA 12.8.
Los otros comandos deben mostrar la versión de CMake y del compilador de Microsoft.
Si algún comando no se encuentra, revisa su instalación antes de continuar.

```powershell
uv venv --python 3.12 .venv-gpu
uv pip install --python .venv-gpu/Scripts/python.exe dashai==0.10.0
uv pip install --python .venv-gpu/Scripts/python.exe torch torchvision --index-url https://download.pytorch.org/whl/cu128 --reinstall
uv pip install --python .venv-gpu/Scripts/python.exe llama-cpp-python --no-binary llama-cpp-python -C cmake.args=-DGGML_CUDA=on
```

Comprueba la aceleración e inicia DashAI:

```powershell
.venv-gpu/Scripts/python.exe -c "import torch; print(torch.cuda.is_available())"
.venv-gpu/Scripts/python.exe -c "import llama_cpp; print(llama_cpp.llama_supports_gpu_offload())"
$env:PYTHONUTF8 = "1"
.venv-gpu/Scripts/python.exe -m DashAI --no-browser --local-path .dashai
```

Las dos comprobaciones deben mostrar `True`. Si alguna muestra `False`, usa el
entorno CPU mientras revisas la instalación GPU.

### macOS — Apple Silicon

Usa terminal y Python arm64, sin Rosetta. Instala las
[herramientas de Xcode](https://developer.apple.com/xcode/resources/) y
[CMake](https://cmake.org/download/):

```sh
xcode-select --install
```

Si las herramientas ya están instaladas, no necesitas instalarlas de nuevo.
Comprueba que los siguientes comandos muestren la versión de cada herramienta:

```sh
clang --version
cmake --version
```

Prepara el entorno y compila llama-cpp con Metal:

```sh
uv venv --python 3.12 .venv-gpu
uv pip install --python .venv-gpu/bin/python dashai==0.10.0
uv pip install --python .venv-gpu/bin/python llama-cpp-python==0.3.29 --no-binary llama-cpp-python -C cmake.args=-DGGML_METAL=on
```

Comprueba la aceleración e inicia DashAI:

```sh
.venv-gpu/bin/python -c "import torch; print(torch.backends.mps.is_available())"
.venv-gpu/bin/python -c "import llama_cpp; print(llama_cpp.llama_supports_gpu_offload())"
.venv-gpu/bin/python -m DashAI --no-browser --local-path .dashai
```

Las dos comprobaciones deben mostrar `True`. MPS es la aceleración de PyTorch;
llama-cpp utiliza Metal por separado. Si alguna comprobación falla, puedes seguir
con el entorno CPU de la sección 3.

### Linux — NVIDIA

Necesitas un [controlador NVIDIA](https://www.nvidia.com/en-us/drivers/) compatible
con tu tarjeta, [CUDA Toolkit 12.8](https://developer.nvidia.com/cuda-12-8-0-download-archive),
[CMake](https://cmake.org/download/) y GCC o Clang. Instala el compilador con el
gestor de paquetes de tu distribución y comprueba los requisitos:

```sh
nvidia-smi
nvcc --version
cmake --version
gcc --version
```

Si usas Clang, ejecuta `clang --version` en lugar de `gcc --version`.
`nvidia-smi` debe reconocer tu tarjeta; `nvcc --version` debe indicar CUDA 12.8.
CMake y el compilador deben mostrar su versión. Si algún comando falla, resuelve
su instalación antes de continuar o usa el entorno CPU de la sección 3.

```sh
uv venv --python 3.12 .venv-gpu
uv pip install --python .venv-gpu/bin/python dashai==0.10.0
uv pip install --python .venv-gpu/bin/python torch torchvision --index-url https://download.pytorch.org/whl/cu128 --reinstall
uv pip install --python .venv-gpu/bin/python llama-cpp-python --no-binary llama-cpp-python -C cmake.args=-DGGML_CUDA=on
```

Comprueba la aceleración e inicia DashAI:

```sh
.venv-gpu/bin/python -c "import torch; print(torch.cuda.is_available())"
.venv-gpu/bin/python -c "import llama_cpp; print(llama_cpp.llama_supports_gpu_offload())"
.venv-gpu/bin/python -m DashAI --no-browser --local-path .dashai
```

Las dos comprobaciones deben mostrar `True`. Si alguna muestra `False`, usa el
entorno CPU mientras revisas la instalación GPU.

### Confirmar el uso de la GPU en DashAI

En los parámetros del modelo GGUF, configura las capas GPU (`n_gpu_layers`) si
están disponibles y revisa el registro para confirmar que se asignaron capas
a la GPU. Tener PyTorch acelerado no basta para acelerar un modelo GGUF.
Estas recetas requieren validación en tu hardware; la CI solo comprueba CPU.

## 5. Si algo falla

- **No se encuentra uv/git:** reinicia la terminal después de instalar y revisa el PATH.
- **No existe un wheel compatible:** confirma Python 3.12 y arquitectura de 64 bits.
  La instalación LLM puede requerir CMake y un compilador; conserva el entorno CPU
  básico para hacer clasificación mientras resuelves el soporte LLM.
- **Error de biblioteca nativa:** comprueba las herramientas C++ del sistema;
  en Windows puede faltar el redistribuible de Visual C++. En Linux, un error
  `libGL.so.1` requiere el paquete de OpenGL de tu distribución (por ejemplo,
  `libgl1` en Ubuntu). Copia el error completo al pedir ayuda.
- **Puerto 8000 ocupado:** detén la otra instancia con Ctrl+C y vuelve a iniciar.
- **No abre el navegador:** usa la dirección indicada; no necesitas un iframe de Colab.
- **Falla `llama_cpp`:** repite la sincronización con `--extra llm` y su comprobación
  de importación. Revisa la arquitectura antes de intentar instalar CUDA.
- **Poca memoria:** cierra aplicaciones y usa el modelo pequeño. Puedes continuar
  con clasificación sin el extra LLM.

Referencias: [DashAI](https://github.com/DashAISoftware/DashAI),
[uv](https://docs.astral.sh/uv/getting-started/installation/),
[llama-cpp](https://llama-cpp-python.readthedocs.io/en/latest/).
