"""Comprueba el arranque HTTP y cierra todos los procesos creados."""

import contextlib
import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


def main():
    with (
        tempfile.TemporaryDirectory() as carpeta,
        Path(carpeta, "servidor.log").open("w+", encoding="utf-8") as registro,
    ):
        proceso = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "DashAI",
                "--no-browser",
                "--local-path",
                carpeta,
            ],
            stdout=registro,
            stderr=subprocess.STDOUT,
            env={**os.environ, "PYTHONUTF8": "1"},
            start_new_session=os.name != "nt",
        )
        try:
            for _ in range(600):
                if proceso.poll() is not None:
                    break
                try:
                    with urllib.request.urlopen(
                        "http://127.0.0.1:8000/app/", timeout=2
                    ) as respuesta:
                        assert respuesta.status == 200
                        print("DashAI responde HTTP 200")
                        return
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(2)
            registro.seek(0)
            raise RuntimeError(registro.read()[-12000:])
        finally:
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(proceso.pid), "/T", "/F"],
                    check=False,
                )
            else:
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(proceso.pid, signal.SIGTERM)
            try:
                proceso.wait(timeout=15)
            except subprocess.TimeoutExpired:
                if os.name != "nt":
                    os.killpg(proceso.pid, signal.SIGKILL)
                proceso.kill()
                proceso.wait()


if __name__ == "__main__":
    main()
