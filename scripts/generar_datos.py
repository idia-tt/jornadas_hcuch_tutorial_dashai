"""Genera el mismo CSV público que el cuaderno de Colab."""

from pathlib import Path

from sklearn.datasets import load_breast_cancer


def main():
    datos = load_breast_cancer(as_frame=True).frame
    datos["diagnosis"] = datos.pop("target").map({0: "malignant", 1: "benign"})
    assert datos.shape == (569, 31)
    assert datos["diagnosis"].value_counts().to_dict() == {
        "benign": 357,
        "malignant": 212,
    }
    destino = Path("breast_cancer.csv")
    if destino.exists():
        raise FileExistsError(f"{destino} ya existe; muévelo antes de generar otro.")
    datos.to_csv(destino, index=False, mode="x")
    print(f"Creado: {destino.resolve()} ({datos.shape[0]} filas)")


if __name__ == "__main__":
    main()
