# DashAI en tu computador

Esta alternativa reemplaza la preparación en Colab. Los ejercicios de
[la guía HTML](../DashAI_Guia.html) son los mismos: trabajas en el navegador,
pero los datos y sesiones quedan en tu computador.

## 1. Preparar el computador

Usa Windows 10/11 x64, Linux x64 o macOS con Apple Silicon. Para Mac Intel,
la disponibilidad de wheels de las dependencias debe comprobarse por separado.
Se recomienda disponer de 8 GB de RAM y al menos 10 GB de disco libre; los modelos
de lenguaje pueden necesitar bastante más. Internet es necesario para instalar
y descargar modelos. Python 3.12 lo instala uv automáticamente.

Instala [Git](https://git-scm.com/downloads) y luego uv:

**Windows — PowerShell**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux — Terminal**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Después de reiniciar la terminal, en Windows ejecuta también `$env:PYTHONUTF8 = "1"` en la terminal donde
iniciarás DashAI. Evita errores Unicode del banner al redirigir los registros.

Cierra y vuelve a abrir la terminal. Comprueba `git --version` y `uv --version`.
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

```sh
uv run python scripts/generar_datos.py
uv run python -m DashAI --no-browser --local-path .dashai
```

El primer comando crea `breast_cancer.csv` en la carpeta del repo: 569 filas,
30 características y la columna `diagnosis`. No sobrescribe archivos existentes.
Súbelo desde la guía de ejercicios; no necesitas ejecutar su paso de Colab.

Espera que el servidor termine de iniciar y abre <http://127.0.0.1:8000/app/>.
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

Esta sección es opcional y requiere hardware compatible. Mantiene intactos el
entorno CPU y su lockfile. El entorno GPU instala la misma versión de DashAI,
pero sus dependencias se resuelven por separado y no quedan fijadas por `uv.lock`.

```sh
uv venv --python 3.12 .venv-gpu
```

En los comandos de esta sección, sustituye `PYTHON_GPU` por:

- Windows PowerShell: `.venv-gpu/Scripts/python.exe`
- macOS/Linux: `.venv-gpu/bin/python`

No escribas literalmente `PYTHON_GPU`. Instala la base:

```sh
uv pip install --python PYTHON_GPU dashai==0.10.0
```

### NVIDIA — Windows/Linux

Instala un controlador compatible y CUDA Toolkit 12.8; comprueba `nvidia-smi`
y `nvcc --version`. Para compilar llama-cpp necesitas CMake y un compilador C++:
Visual Studio Build Tools en Windows (terminal de desarrollo) o GCC/Clang en Linux.

```sh
uv pip install --python PYTHON_GPU torch torchvision --index-url https://download.pytorch.org/whl/cu128 --reinstall
uv pip install --python PYTHON_GPU llama-cpp-python --no-binary llama-cpp-python -C cmake.args=-DGGML_CUDA=on
```

Comprueba que `PYTHON_GPU -c "import torch; print(torch.cuda.is_available())"`
muestre `True`. NVIDIA en macOS no está cubierta.

### Apple Silicon — macOS

Usa terminal y Python arm64, sin Rosetta. Instala las herramientas de Xcode con
`xcode-select --install`. Con CMake disponible, compila llama-cpp con Metal:

```sh
uv pip install --python PYTHON_GPU llama-cpp-python==0.3.29 --no-binary llama-cpp-python -C cmake.args=-DGGML_METAL=on
```

Comprueba `PYTHON_GPU -c "import torch; print(torch.backends.mps.is_available())"`.
MPS es la aceleración de PyTorch; llama-cpp utiliza Metal por separado.

### Verificar e iniciar

```sh
PYTHON_GPU -c "import llama_cpp; print(llama_cpp.llama_supports_gpu_offload())"
PYTHON_GPU -m DashAI --no-browser --local-path .dashai
```

La primera comprobación debe mostrar `True`. En los parámetros del modelo GGUF,
configura las capas GPU (`n_gpu_layers`) si están disponibles y revisa el registro
para confirmar la descarga de capas a GPU. Tener PyTorch acelerado no basta para
acelerar un modelo GGUF. No ejecutes dos servidores sobre la misma carpeta.
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
